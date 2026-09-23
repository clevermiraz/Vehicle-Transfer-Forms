"""Fill the original PDF forms by writing text on top of them.

Text is placed with PyMuPDF's HTML box (MuPDF Story + HarfBuzz), which shapes Bangla
correctly. Plain `insert_text` must not be used: it breaks Bangla conjuncts and vowel signs.
"""

import html
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import pymupdf

FONTS_DIR = Path(__file__).parent / "fonts"
_ARCHIVE = pymupdf.Archive(str(FONTS_DIR))
_SIZE_STEP = 0.5


@dataclass(frozen=True)
class Box:
    """Where one canonical value is written.

    `baseline` is the text baseline of the first row. Continuation rows are `pitch` points
    apart and start at `x0`. The first row starts at `x0 + indent` (after the printed label).
    """

    key: str
    label: str
    x0: float
    x1: float
    baseline: float
    rows: int = 1
    indent: float = 0
    pitch: float = 24.5
    size: float = 11
    min_size: float = 7
    page: int = 0


@dataclass(frozen=True)
class FormSpec:
    slug: str
    title: str
    template: str
    boxes: list[Box]
    pages: list[int] = field(default_factory=lambda: [0])  # template pages to keep

    @property
    def filename(self) -> str:
        return f"{self.slug}.pdf"


class FieldOverflowError(Exception):
    """A value is too long for its space on the form, even at the minimum font size."""

    def __init__(self, form: FormSpec, labels: list[str]):
        self.form = form
        self.labels = labels
        super().__init__(f"Too long for {form.title}: {', '.join(labels)}. Please shorten.")


def _css(size: float, pitch: float, indent: float) -> str:
    return f"""
    @font-face {{ font-family: latin; src: url(NotoSans-Regular.ttf); }}
    @font-face {{ font-family: bengali; src: url(NotoSansBengali-Regular.ttf); }}
    body, div {{ margin: 0; padding: 0; }}
    * {{ font-family: latin; font-size: {size}pt; line-height: {pitch}pt; color: #000; }}
    .bn {{ font-family: bengali; }}
    div {{ text-indent: {indent}pt; }}
    """


def _is_bengali(ch: str) -> bool:
    # Bengali block, danda/double danda, and zero-width (non-)joiners used in conjuncts.
    return "\u0980" <= ch <= "\u09ff" or ch in "\u0964\u0965\u200c\u200d"


def _markup(text: str) -> str:
    """Wrap Bangla runs in <span class="bn">.

    MuPDF does not fall back through a CSS font-family list per character: glyphs missing from
    the first font come from its own built-in fonts. So each script gets its font explicitly.
    Spaces stay with the run before them.
    """
    runs: list[tuple[bool, str]] = []
    for ch in text:
        bengali = runs[-1][0] if ch.isspace() and runs else _is_bengali(ch)
        if runs and runs[-1][0] == bengali:
            runs[-1] = (bengali, runs[-1][1] + ch)
        else:
            runs.append((bengali, ch))
    return "".join(f'<span class="bn">{html.escape(r)}</span>' if bn else html.escape(r) for bn, r in runs)


@lru_cache
def _baseline_offset(size: float, pitch: float) -> float:
    """Distance from the top of an HTML line box to the text baseline (measured, not guessed)."""
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_htmlbox(pymupdf.Rect(0, 0, 300, pitch), "<div>H</div>", css=_css(size, pitch, 0), archive=_ARCHIVE)
    span = page.get_text("dict")["blocks"][0]["lines"][0]["spans"][0]
    return span["origin"][1]


def _fits(content: str, css: str, box: Box) -> bool:
    """Lay the text out on a scratch page with spare room and check the real result.

    insert_htmlbox's own "did it fit" signal is not reliable: it can report success while
    silently dropping a wrapped last line. It also never breaks a long word, which would
    run past the right edge. So we measure used height and widest line ourselves.
    """
    doc = pymupdf.open()
    page = doc.new_page(width=box.x1 - box.x0 + 200, height=(box.rows + 10) * box.pitch)
    width = box.x1 - box.x0
    spare, _ = page.insert_htmlbox(
        pymupdf.Rect(0, 0, width, page.rect.height), content, css=css, archive=_ARCHIVE, scale_low=1
    )
    used_height = page.rect.height - spare
    lines = [line["bbox"] for block in page.get_text("dict")["blocks"] for line in block.get("lines", [])]
    widest = max((bbox[2] for bbox in lines), default=0)
    return spare >= 0 and used_height <= box.rows * box.pitch + 0.1 and widest <= width + 0.5


def _write(page: pymupdf.Page, box: Box, text: str) -> bool:
    """Write text at the largest size that fits; line spacing stays on the form's rows.
    Returns False (and writes nothing) if it does not fit even at `min_size`."""
    content = f"<div>{_markup(text)}</div>"
    size = box.size
    while size >= box.min_size:
        css = _css(size, box.pitch, box.indent)
        if _fits(content, css, box):
            top = box.baseline - _baseline_offset(size, box.pitch)
            rect = pymupdf.Rect(box.x0, top, box.x1, top + box.rows * box.pitch + 0.1)
            page.insert_htmlbox(rect, content, css=css, archive=_ARCHIVE, scale_low=1)
            return True
        size -= _SIZE_STEP
    return False


def render_form(spec: FormSpec, context: dict[str, str], templates_dir: Path) -> bytes:
    """Return the filled PDF. The template file itself is only read, never modified."""
    doc = pymupdf.open(templates_dir / spec.template)
    if len(doc) != len(spec.pages):
        doc.select(spec.pages)
    overflow = []
    for box in spec.boxes:
        text = context.get(box.key)
        if text and not _write(doc[box.page], box, text):
            overflow.append(box.label)
    if overflow:
        raise FieldOverflowError(spec, overflow)
    doc.subset_fonts()
    return doc.tobytes(garbage=3, deflate=True)


def merge_pdfs(pdfs: list[bytes]) -> bytes:
    merged = pymupdf.open()
    for data in pdfs:
        with pymupdf.open(stream=data, filetype="pdf") as part:
            merged.insert_pdf(part)
    return merged.tobytes(garbage=3, deflate=True)
