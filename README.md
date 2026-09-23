# Vehicle Ownership Transfer Forms

Enter the seller, buyer, vehicle and sale details **once** and get all four filled forms
(Form 20, Form 21, Form 22, Owner's Particulars) ready to preview, download and print.

- Design and form analysis: `docs/FORM_ANALYSIS.md`
- Fake test data used for every PDF: `SAMPLE_DATA.json`
- Original PDFs (never modified): `reference_forms/`

## Run locally

| Part | Address |
|---|---|
| Website | http://localhost:3000 |
| API (FastAPI, docs at `/docs`) | http://127.0.0.1:8010 |
| PostgreSQL (Docker) | 127.0.0.1:5442 |

```bash
# 1. Database
docker compose up -d

# 2. Backend
cd backend
cp .env.example .env            # then set SECRET_KEY to a long random string
uv sync
uv run alembic upgrade head
uv run python -m app.cli create-admin admin "Shop Admin"   # asks for the password
uv run uvicorn app.main:app --host 127.0.0.1 --port 8010

# 3. Frontend (another terminal)
cd frontend
npm install
npm run dev                     # http://localhost:3000
```

Run the backend tests (they use a separate `vehicle_forms_test` database):

```bash
docker exec vehicle-forms-db psql -U vehicle_forms -c 'CREATE DATABASE vehicle_forms_test'   # once
cd backend && uv run pytest
```

## How it works

- `backend/app/services/pdf/generator.py`: one reusable engine that writes text onto the
  original PDF. It uses PyMuPDF's HTML box, which shapes Bangla correctly, and bundled Noto fonts.
  Long values shrink to fit. If a value still doesn't fit, the form reports an error.
  Text is never cut off silently.
- `backend/app/services/pdf/mappings/*.py`: only the coordinates for each form.
- `backend/app/services/pdf/context.py`: formatting rules (CAPITALS, DD/MM/YYYY, `5,00,000/- (Five Lac)`,
  father/husband choice, present address on Forms 20–22).
- Saved customers and vehicles are reused through search. Each transfer keeps its own copy of the
  details, so old documents re-print exactly the same.

## Keyboard shortcuts

- **Alt+N**: new transfer
- **Ctrl+S**: save
- **Enter**: next field
- **↑ / ↓ + Enter**: pick a search result

## Adding or adjusting a form

To nudge a value, change its `x0 / x1 / baseline` in the form's mapping file.
To add a new form, create a new mapping file and add it to `FORMS` in `services/pdf/forms.py`.
