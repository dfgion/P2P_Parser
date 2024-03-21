from __future__ import annotations

import datetime
from typing import List

from sqlalchemy import ForeignKey, BigInteger, DATE, String, Integer, Table, Column, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(AsyncAttrs, DeclarativeBase):
    pass


user_stock_coin_association_table = Table(
    "User_Stock_Coin_Table",
    Base.metadata,
    Column("id", Integer, primary_key=True, nullable=False, autoincrement=True),
    Column("user_id", ForeignKey("users.tg_id"), nullable=False),
    Column("stock_id", ForeignKey("stock.id"), nullable=False),
    Column("coin_id", ForeignKey("coins.id"), nullable=False),
    Column("currency", String(32), nullable=False),
    Column("type_order", String(32), nullable=False),
    Column("limits", String(32), nullable=False),
    Column('payment_methods', String(64), nullable=False),
    UniqueConstraint('user_id', "stock_id", "coin_id", "type_order", name='index_unique_user_stock_coin_type'),
)

stock_coin_association_table = Table(
    "Stock_Coin_Table",
    Base.metadata,
    Column("id", Integer, primary_key=True, nullable=False, autoincrement=True),
    Column("stock_id", ForeignKey("stock.id"), nullable=False),
    Column("coin_id", ForeignKey("coins.id"), nullable=False),
    UniqueConstraint("stock_id", "coin_id", name='index_unique_stock_coin')
)

class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, nullable=False)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"))
    reg_date: Mapped[datetime.date] = mapped_column(DATE, default=datetime.date.today())
    upd_date: Mapped[datetime.date] = mapped_column(DATE, onupdate=datetime.date.today(), nullable=True)

    stock: Mapped[List[Stock]] = relationship(
        secondary=user_stock_coin_association_table, backref='users', cascade='all,delete'
    )
    
    def __repr__(self) -> str:
        return f"<User_tg_id: {self.tg_id}>"

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    users: Mapped[List[User]] = relationship()
    name: Mapped[str] = mapped_column(String(32), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(String(512), unique=False, nullable=False)
    days: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    __table_args__= (UniqueConstraint(name, description, days, name='index_unique_description_days'), )
    
    def __repr__(self) -> str:
        return f"<Subscription_name: {self.name}>"

class Stock(Base):
    __tablename__ = 'stock'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Stock market_name: {self.name}>"
    
class Coin(Base):
    __tablename__ = 'coins'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Stock market_name: {self.name}>"
