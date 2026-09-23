import pymupdf
import pytest

from app.core.config import settings
from app.services.pdf.context import build_context
from app.services.pdf.forms import FORMS, render, render_merged
from app.services.pdf.generator import FieldOverflowError


def _text(pdf: bytes) -> str:
    with pymupdf.open(stream=pdf, filetype="pdf") as doc:
        return " ".join(" ".join(page.get_text().split()) for page in doc)  # wrapped lines -> spaces


def _fonts(pdf: bytes) -> set[str]:
    with pymupdf.open(stream=pdf, filetype="pdf") as doc:
        return {f[3] for page in doc for f in page.get_fonts()}


def test_context_applies_decisions(sample_data):
    ctx = build_context(sample_data)
    assert ctx["seller.father_or_husband"] == "LATE ABDUL KARIM KHAN"  # pref = father
    assert ctx["buyer.father_or_husband"] == "PRADIP KUMAR DAS"  # pref = husband
    assert ctx["buyer.address"] == ctx["buyer.present_address"]
    assert ctx["transfer.sale_date"] == "20/09/2026"
    assert ctx["transfer.sale_price_text"] == "5,00,000/- (Five Lac)"
    assert ctx["buyer.name"] == "SHRIMATI KRISHNA RANI DAS"


@pytest.mark.parametrize("slug", list(FORMS))
def test_every_form_renders_sample_data_as_a4(sample_data, slug):
    pdf = render(slug, sample_data, settings.templates_dir)
    with pymupdf.open(stream=pdf, filetype="pdf") as doc:
        assert len(doc) == 1
        assert round(doc[0].rect.width) == 595 and round(doc[0].rect.height) == 842
    text = _text(pdf)
    assert "DHAKA METRO-GA-99-0001" in text
    assert "SHRIMATI KRISHNA RANI DAS" in text  # nothing silently dropped


def test_bangla_uses_bundled_font(sample_data):
    fonts = _fonts(render("form-22", sample_data, settings.templates_dir))
    assert any("Noto Sans Bengali" in f for f in fonts)
    assert not any("Serif" in f for f in fonts)  # MuPDF's built-in fallback must not be used


def test_templates_are_not_modified(sample_data):
    before = {p.name: p.read_bytes() for p in settings.templates_dir.glob("*.pdf")}
    render_merged(sample_data, settings.templates_dir)
    assert before == {p.name: p.read_bytes() for p in settings.templates_dir.glob("*.pdf")}


def test_merged_pdf_has_all_forms(sample_data):
    with pymupdf.open(stream=render_merged(sample_data, settings.templates_dir), filetype="pdf") as doc:
        assert len(doc) == len(FORMS)


def test_long_value_shrinks_instead_of_being_cut(sample_data):
    sample_data["buyer"]["name"] = "SHRIMATI KRISHNA RANI DAS CHOWDHURY MAJUMDER"
    assert "KRISHNA RANI DAS CHOWDHURY MAJUMDER" in _text(render("owner-particulars", sample_data, settings.templates_dir))


def test_value_too_long_raises_clear_error(sample_data):
    sample_data["seller"]["present_address"] = "VERY LONG ADDRESS " * 60
    with pytest.raises(FieldOverflowError) as exc:
        render("form-22", sample_data, settings.templates_dir)
    assert exc.value.labels == ["Seller address"]


def test_unbreakable_value_wider_than_box_raises(sample_data):
    sample_data["vehicle"]["chassis_number"] = "X" * 80
    with pytest.raises(FieldOverflowError):
        render("form-20", sample_data, settings.templates_dir)


def test_empty_optional_fields_stay_blank(sample_data):
    text = _text(render("owner-particulars", sample_data, settings.templates_dir))
    assert "NONE" not in text
