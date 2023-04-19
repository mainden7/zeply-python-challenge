import datetime

from pydantic import BaseModel

from zeply_python_challenge.wallets.constants import CurrencyThreeLetterSymbol


class Addresses(BaseModel):
    p2pkh: str
    p2sh: str
    p2wpkh: str
    p2wpkh_in_p2sh: str
    p2wsh: str
    p2wsh_in_p2sh: str


class CreatedWalletInResponse(BaseModel):
    cryptocurrency: str
    symbol: str
    network: str
    strength: int | None
    entropy: str | None
    mnemonic: str | None
    language: str | None
    passphrase: str | None = None
    seed: str
    root_xprivate_key: str
    root_xpublic_key: str
    xprivate_key: str
    xpublic_key: str
    uncompressed: str
    compressed: str
    chain_code: str
    private_key: str
    public_key: str
    wif: str
    finger_print: str
    semantic: str
    path: str | None
    hash: str
    addresses: Addresses


class FetchedWalletInResponse(BaseModel):
    currency: str
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    addresses: Addresses

    class Config:  # noqa: D106
        orm_mode = True


class GenerateWalletParametersInRequest(BaseModel):
    currency: CurrencyThreeLetterSymbol
