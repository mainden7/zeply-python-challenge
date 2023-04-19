from unittest.mock import MagicMock

import pytest

from zeply_python_challenge.wallets.constants import CurrencyThreeLetterSymbol
from zeply_python_challenge.wallets.models import Wallet
from zeply_python_challenge.wallets.schemas import CreatedWalletInResponse
from zeply_python_challenge.wallets.service import generate_wallet
from zeply_python_challenge.wallets.service import get_all_wallets


@pytest.mark.asyncio
@pytest.mark.parametrize("symbol", list(CurrencyThreeLetterSymbol))
async def test_generate_wallet(symbol: str, async_session_mock) -> None:
    # Test generating a wallet for a known currency symbol
    wallet_data = await generate_wallet(async_session_mock, symbol=symbol)
    wallet = CreatedWalletInResponse(**wallet_data)
    assert wallet_data is not None
    assert wallet.symbol == symbol

    # Test that session object was called
    async_session_mock.add.assert_called()
    async_session_mock.commit.assert_called()


@pytest.mark.asyncio
async def test_generate_wallet__error(async_session_mock) -> None:
    # Test generating a wallet for an unknown currency symbol
    symbol = "UNKNOWN"
    with pytest.raises(ValueError):
        await generate_wallet(async_session_mock, symbol=symbol)


@pytest.mark.asyncio
async def test_get_all_wallets(
    wallet_in_db: Wallet, async_session_mock
) -> None:
    result_mock = MagicMock()
    result_mock.scalars.return_value.all.return_value = [wallet_in_db]
    async_session_mock.execute.return_value = result_mock
    # Test generating a wallet for a known currency symbol
    wallets = await get_all_wallets(async_session_mock)
    assert isinstance(wallets, list)
    # Test that session object was called
    async_session_mock.commit.assert_called()

# TODO: add all required tests
