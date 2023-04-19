from typing import Annotated
from typing import Any

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from zeply_python_challenge.config import settings
from zeply_python_challenge.database import create_async_session
from zeply_python_challenge.response_schemas import ErrorResponseSchemas
from zeply_python_challenge.wallets.constants import CurrencyThreeLetterSymbol
from zeply_python_challenge.wallets.exceptions import WalletEntryDoesNotExist
from zeply_python_challenge.wallets.schemas import CreatedWalletInResponse
from zeply_python_challenge.wallets.schemas import FetchedWalletInResponse
from zeply_python_challenge.wallets.schemas import \
    GenerateWalletParametersInRequest
from zeply_python_challenge.wallets.service import generate_wallet
from zeply_python_challenge.wallets.service import get_all_wallets
from zeply_python_challenge.wallets.service import get_wallet_by_id
from zeply_python_challenge.wallets.service import restore_from_mnemonic
from zeply_python_challenge.wallets.service import restore_from_seed

wallets_router = APIRouter(prefix="/wallets", tags=["wallets"])


@wallets_router.get(
    "",
    responses=ErrorResponseSchemas.NOT_FOUND,
    response_model=list[FetchedWalletInResponse],
)
async def get_generated_wallets(
    sess: AsyncSession = Depends(create_async_session),
    limit: Annotated[
        int | None, Query(le=settings.MAX_ENTITIES_PER_PAGE)
    ] = 10,
    offset: int = 0,
) -> Any:
    """Get all generated wallets."""
    wallets = await get_all_wallets(sess, limit=limit, offset=offset)
    if len(wallets) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallets were not found",
        )
    return wallets


@wallets_router.get(
    "/{wallet_id}",
    responses=ErrorResponseSchemas.NOT_FOUND,
    response_model=FetchedWalletInResponse,
)
async def get_wallet(
    sess: AsyncSession = Depends(create_async_session),
    wallet_id: int = Path(...),
) -> Any:
    """Return a wallet specified with the given wallet_id."""
    wallet = await get_wallet_by_id(sess, wallet_id=wallet_id)
    if wallet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet was not found",
        )
    return wallet


@wallets_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CreatedWalletInResponse,
)
async def generate_new_wallet(
    sess: AsyncSession = Depends(create_async_session),
    params: GenerateWalletParametersInRequest = Body(...),
) -> Any:
    """Generate new wallet based on given params."""
    wallet = await generate_wallet(sess, symbol=params.currency)
    return wallet


@wallets_router.get(
    "/restore-from-seed/",
    responses=ErrorResponseSchemas.BAD_REQUEST,
    response_model=CreatedWalletInResponse,
)
async def restore_wallet_from_seed(
    sess: AsyncSession = Depends(create_async_session),
    seed: str = Query(...),
    currency: CurrencyThreeLetterSymbol = Query(...),
) -> Any:
    """Restore wallet by the seed string."""
    try:
        wallet = await restore_from_seed(sess, symbol=currency, seed=seed)
    except WalletEntryDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid seed phrase",
        )
    return wallet


@wallets_router.get(
    "/restore-from-mnemonic/",
    responses=ErrorResponseSchemas.BAD_REQUEST,
    response_model=CreatedWalletInResponse,
)
async def restore_wallet_from_mnemonic(
    sess: AsyncSession = Depends(create_async_session),
    mnemonic: str = Query(...),
    currency: CurrencyThreeLetterSymbol = Query(...),
) -> Any:
    """Restore wallet by the mnemonic string."""
    try:
        wallet = await restore_from_mnemonic(
            sess, symbol=currency, mnemonic=mnemonic
        )
    except WalletEntryDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid mnemonic phrase",
        )
    return wallet
