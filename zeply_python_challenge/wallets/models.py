from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB

from zeply_python_challenge.database import Base
from zeply_python_challenge.database import TimeTrackMixin


class Wallet(Base, TimeTrackMixin):
    __tablename__ = "wallets"
    addresses = Column(JSONB, nullable=False)
    currency = Column(String, nullable=False)

    seed = Column(String, nullable=False)
    mnemonic = Column(String, nullable=False)
