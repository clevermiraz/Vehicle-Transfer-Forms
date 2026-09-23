import json
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import PROJECT_DIR, settings
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import User

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL", settings.database_url.rsplit("/", 1)[0] + "/vehicle_forms_test"
)


@pytest.fixture
def sample_data() -> dict:
    return json.loads((PROJECT_DIR / "SAMPLE_DATA.json").read_text())


@pytest.fixture
def sample_payload(sample_data) -> dict:
    """SAMPLE_DATA.json converted to the POST /api/transfers body."""
    t = {k: v for k, v in sample_data["transfer"].items()}
    return {**t, "seller": sample_data["seller"], "buyer": sample_data["buyer"], "vehicle": sample_data["vehicle"]}


@pytest.fixture
def db_session():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine, expire_on_commit=False)
    with Session() as session:
        yield session
    engine.dispose()


@pytest.fixture
def client(db_session):
    db_session.add(User(name="Test Staff", username="staff", password_hash=hash_password("staff-pass-1")))
    db_session.commit()
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_client(client):
    assert client.post("/api/auth/login", json={"username": "staff", "password": "staff-pass-1"}).status_code == 200
    return client
