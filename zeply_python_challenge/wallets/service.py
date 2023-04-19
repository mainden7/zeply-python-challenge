from typing import Any

from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from zeply_python_challenge.config import settings
from zeply_python_challenge.utils import make_hash
from zeply_python_challenge.wallets.exceptions import WalletEntryDoesNotExist
from zeply_python_challenge.wallets.models import Wallet


async def generate_wallet(
    sess: AsyncSession, *, symbol: str
) -> dict[str, Any]:
    """Generate new wallet."""
    entropy = generate_entropy(strength=settings.WALLET_ENTROPY_STRENGTH)

    wallet = HDWallet(symbol=symbol)
    wallet.from_entropy(
        entropy=entropy, language=settings.WALLET_MNEMONIC_PHRASE_LANGUAGE
    )
    wallet_data = wallet.dumps()
    # for the simplicity we are using only one address
    wallet_in_db = Wallet()
    wallet_in_db.addresses = wallet_data["addresses"]
    wallet_in_db.currency = symbol
    # TODO: find a better way to store wallet unified identity
    #  tips: authorized users, sign with a master key, encrypt with better algo
    #  than is used in the function below
    wallet_in_db.mnemonic = make_hash(value=wallet_data["mnemonic"])
    wallet_in_db.seed = make_hash(value=wallet_data["seed"])

    sess.add(wallet_in_db)
    await sess.commit()
    return wallet_data


async def get_all_wallets(
    sess: AsyncSession, *, offset: int = 0, limit: int = 10
) -> list[Wallet]:
    stmt = select(Wallet).offset(offset).limit(limit)
    res = await sess.execute(stmt)
    return res.scalars().all()


async def get_wallet_by_id(
    sess: AsyncSession, *, wallet_id: int
) -> Wallet | None:
    stmt = select(Wallet).where(Wallet.id == wallet_id)
    res = await sess.execute(stmt)
    return res.scalar()


async def get_by_seed(sess: AsyncSession, *, seed: str) -> Wallet | None:
    stmt = select(Wallet).where(Wallet.seed == seed)
    res = await sess.execute(stmt)
    return res.scalar()


async def get_by_mnemonic(
    sess: AsyncSession, *, mnemonic: str
) -> Wallet | None:
    stmt = select(Wallet).where(Wallet.mnemonic == mnemonic)
    res = await sess.execute(stmt)
    return res.scalar()


async def restore_from_seed(
    sess: AsyncSession, *, symbol: str, seed: str
) -> dict[str, Any]:
    # check if that wallet exists in the database
    hashed_seed = make_hash(value=seed)
    wallet_in_db = await get_by_seed(sess, seed=hashed_seed)
    if not wallet_in_db:
        raise WalletEntryDoesNotExist("Wallet does not exist.")

    wallet = HDWallet(symbol=symbol).from_seed(seed)
    return wallet.dumps()


async def restore_from_mnemonic(
    sess: AsyncSession, *, symbol: str, mnemonic: str
) -> dict[str, Any]:
    # check if that wallet exists in the database
    hashed_mnemonic = make_hash(value=mnemonic)
    wallet_in_db = await get_by_mnemonic(sess, mnemonic=hashed_mnemonic)
    if not wallet_in_db:
        raise WalletEntryDoesNotExist("Wallet does not exist.")

    wallet = HDWallet(symbol=symbol).from_mnemonic(mnemonic)
    return wallet.dumps()
