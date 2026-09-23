"""All forms produced for an ownership transfer, in print order."""

from pathlib import Path

from app.services.pdf.context import build_context
from app.services.pdf.generator import FormSpec, merge_pdfs, render_form
from app.services.pdf.mappings.form20 import FORM_20
from app.services.pdf.mappings.form21 import FORM_21
from app.services.pdf.mappings.form22 import FORM_22
from app.services.pdf.mappings.owner_particulars import OWNER_PARTICULARS

FORMS: dict[str, FormSpec] = {f.slug: f for f in (FORM_20, FORM_21, FORM_22, OWNER_PARTICULARS)}


def render(slug: str, data: dict, templates_dir: Path) -> bytes:
    return render_form(FORMS[slug], build_context(data), templates_dir)


def render_all(data: dict, templates_dir: Path) -> dict[str, bytes]:
    context = build_context(data)
    return {slug: render_form(spec, context, templates_dir) for slug, spec in FORMS.items()}


def render_merged(data: dict, templates_dir: Path) -> bytes:
    return merge_pdfs(list(render_all(data, templates_dir).values()))
