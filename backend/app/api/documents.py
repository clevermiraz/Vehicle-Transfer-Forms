import io
import zipfile

from fastapi import APIRouter, HTTPException, Response, status

from app.core.config import settings
from app.core.deps import DB, CurrentUser
from app.schemas.transfer import DocumentInfo
from app.services import transfers as svc
from app.services.pdf.forms import FORMS, render, render_all, render_merged
from app.services.pdf.generator import FieldOverflowError

router = APIRouter(prefix="/api/transfers/{transfer_id}/documents", tags=["documents"])


def _pdf(content: bytes, filename: str, download: bool, media_type: str = "application/pdf") -> Response:
    disposition = "attachment" if download else "inline"
    return Response(
        content,
        media_type=media_type,
        headers={"Content-Disposition": f'{disposition}; filename="{filename}"', "Cache-Control": "no-store"},
    )


def _data(db: DB, transfer_id: int) -> dict:
    return svc.transfer_to_dict(svc.get_transfer(db, transfer_id))


@router.get("", response_model=list[DocumentInfo])
def list_documents(transfer_id: int, _: CurrentUser, db: DB):
    """All forms for this transfer, with a clear error for any form whose values do not fit."""
    data = _data(db, transfer_id)
    docs = []
    for slug, spec in FORMS.items():
        try:
            render(slug, data, settings.templates_dir)
            docs.append(DocumentInfo(slug=slug, title=spec.title))
        except FieldOverflowError as exc:
            docs.append(DocumentInfo(slug=slug, title=spec.title, error=str(exc)))
    return docs


@router.get("/all.zip")
def download_zip(transfer_id: int, _: CurrentUser, db: DB):
    pdfs = render_all(_data(db, transfer_id), settings.templates_dir)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for slug, content in pdfs.items():
            zf.writestr(FORMS[slug].filename, content)
    return _pdf(buffer.getvalue(), f"ownership-transfer-{transfer_id}.zip", True, "application/zip")


@router.get("/all.pdf")
def print_all(transfer_id: int, _: CurrentUser, db: DB, download: bool = False):
    """All forms merged into one PDF, so everything prints from a single print dialog."""
    content = render_merged(_data(db, transfer_id), settings.templates_dir)
    return _pdf(content, f"ownership-transfer-{transfer_id}.pdf", download)


@router.get("/{slug}")
def get_document(transfer_id: int, slug: str, _: CurrentUser, db: DB, download: bool = False):
    if slug not in FORMS:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Unknown form")
    content = render(slug, _data(db, transfer_id), settings.templates_dir)
    return _pdf(content, f"transfer-{transfer_id}-{FORMS[slug].filename}", download)
