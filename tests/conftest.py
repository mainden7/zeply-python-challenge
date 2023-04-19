from unittest.mock import AsyncMock

import faker as faker_
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import clear_mappers

from zeply_python_challenge.wallets.schemas import Addresses
from zeply_python_challenge.wallets.schemas import FetchedWalletInResponse

faker = faker_.Faker()


@pytest.fixture(scope="session")
def async_session_mock():
    async_session_mock = AsyncMock(spec=AsyncSession)
    yield async_session_mock
    clear_mappers()


@pytest.fixture(scope="session")
def wallet_in_db():
    wallet = FetchedWalletInResponse(
        currency=faker.currency_code(),
        created_at=faker.date_time(),
        updated_at=faker.date_time() if faker.boolean() else None,
        addresses=Addresses(
            p2pkh=faker.pystr(),
            p2sh=faker.pystr(),
            p2wpkh=faker.pystr(),
            p2wpkh_in_p2sh=faker.pystr(),
            p2wsh=faker.pystr(),
            p2wsh_in_p2sh=faker.pystr(),
        ),
    )
    return wallet
