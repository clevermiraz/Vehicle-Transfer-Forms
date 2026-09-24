import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import auth, documents, people, transfers, users, vehicles
from app.core.config import settings
from app.services.pdf.generator import FieldOverflowError
from app.services.transfers import ConflictError, NotFoundError

logging.basicConfig(level=logging.INFO)


class _HideQueryString(logging.Filter):
    """Search terms can be NIDs or mobile numbers: keep them out of the access log."""

    def filter(self, record: logging.LogRecord) -> bool:
        # uvicorn access log args: (client, method, path_with_query, http_version, status)
        if isinstance(record.args, tuple) and len(record.args) == 5:
            client, method, path, version, code = record.args
            record.args = (client, method, str(path).split("?", 1)[0], version, code)
        return True


logging.getLogger("uvicorn.access").addFilter(_HideQueryString())

app = FastAPI(title="Vehicle Ownership Transfer Forms")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH"],
    allow_headers=["Content-Type"],
)

for router in (auth.router, users.router, people.router, vehicles.router, transfers.router, documents.router):
    app.include_router(router)


@app.exception_handler(NotFoundError)
def _not_found(_: Request, exc: NotFoundError):
    return JSONResponse({"detail": str(exc)}, status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(ConflictError)
def _conflict(_: Request, exc: ConflictError):
    return JSONResponse({"detail": str(exc)}, status_code=status.HTTP_409_CONFLICT)


@app.exception_handler(FieldOverflowError)
def _overflow(_: Request, exc: FieldOverflowError):
    return JSONResponse({"detail": str(exc)}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.get("/api/health")
@app.head("/api/health")
def health():
    return {"status": "ok"}
