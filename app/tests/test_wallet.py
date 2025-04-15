from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.models import Base, TronService
from app.router import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


client = TestClient(app)


@pytest.fixture(scope="module")
def override_get_db():
    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def _get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_wallet_post(override_get_db):
    response = client.post(
        "/wallet/",
        json={"address": "TU3kjFuhtEo42tsCBtfYUAZxoqQ4yuSLQ5"}
    )
    data = response.json()
    assert response.status_code == 200
    assert "id" in data
    assert data["address"] == "TU3kjFuhtEo42tsCBtfYUAZxoqQ4yuSLQ5"
    assert "bandwidth" in data
    assert "energy" in data
    assert "trx_balance" in data
    assert "timestamp" in data

    db = SessionLocal()
    wallet = db.query(TronService).filter(TronService.address == "TU3kjFuhtEo42tsCBtfYUAZxoqQ4yuSLQ5").first()
    assert wallet is not None
    assert wallet.address == "TU3kjFuhtEo42tsCBtfYUAZxoqQ4yuSLQ5"
    db.close()


def test_post_and_get_wallet(override_get_db):
    response = client.post("/wallet/", json={"address": "TU3kjFuhtEo42tsCBtfYUAZxoqQ4yuSLQ5"})
    data = response.json()
    assert response.status_code == 200
    assert data["address"] == "TU3kjFuhtEo42tsCBtfYUAZxoqQ4yuSLQ5"
    assert isinstance(data["bandwidth"], int)
    assert isinstance(data["energy"], int)
    assert isinstance(data["trx_balance"], float)

    response_get = client.get("/wallets/?skip=0&limit=10")
    data_wallets = response_get.json()
    assert response_get.status_code == 200
    assert isinstance(data_wallets, list)
    assert any(w["address"] == "TU3kjFuhtEo42tsCBtfYUAZxoqQ4yuSLQ5" for w in data_wallets)
