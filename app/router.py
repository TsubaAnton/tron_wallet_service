from fastapi import APIRouter, Depends, HTTPException, Query
from .schemas import WalletResponse, WalletCreate
from sqlalchemy.orm import Session
from .database import SessionLocal
from .tron import get_wallet_info
from .models import TronService

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/wallet/", response_model=WalletResponse)
def wallet_post(data: WalletCreate, db: Session = Depends(get_db)):
    try:
        info = get_wallet_info(data.address)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid address")

    wallet = TronService(
        address=info["address"],
        bandwidth=info["bandwidth"],
        energy=info["energy"],
        trx_balance=str(info["trx_balance"]),
    )
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return WalletResponse(
        id=wallet.id,
        address=wallet.address,
        bandwidth=wallet.bandwidth,
        energy=wallet.energy,
        trx_balance=wallet.trx_balance,
        timestamp=wallet.created_at.timestamp()
    )


@router.get("/wallets/", response_model=list[WalletResponse])
def read_wallets(skip: int = 0, limit: int = Query(10, le=100), db: Session = Depends(get_db)):
    wallets = db.query(TronService).offset(skip).limit(limit).all()
    return [
        WalletResponse(
            id=wallet.id,
            address=wallet.address,
            bandwidth=wallet.bandwidth,
            energy=wallet.energy,
            trx_balance=wallet.trx_balance,
            timestamp=wallet.created_at.timestamp()
        ) for wallet in wallets
    ]



