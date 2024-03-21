import sys
sys.path.append(r'C:\Users\Даниил\Desktop\P2P_Manager')

from sqlalchemy import select, update, insert, distinct
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from db.models import User, Subscription, Stock, Coin, user_stock_coin_association_table
from db.db_config import async_session

from core.utils.const.subscriptions import START, MEDIUM, PRO

import asyncio

from pprint import pprint

async def insert_basic(async_session: async_sessionmaker[AsyncSession] = None) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    User(tg_id=114233, subscription_id=2),
                    User(tg_id=345225, subscription_id=3),
                    User(tg_id=241190, subscription_id=6),
                    Stock(name='Binance'),
                    Stock(name='Bybit'),
                    Subscription(name='📉 START', description=START, days=31, cost=2000),
                    Subscription(name='📉 START', description=START, days=183, cost=9600),
                    Subscription(name='📉 START', description=START, days=365, cost=18000),
                    Subscription(name='👨‍💻 MEDIUM', description=MEDIUM, days=31, cost=4000),
                    Subscription(name='👨‍💻 MEDIUM', description=MEDIUM, days=183, cost=19200),
                    Subscription(name='👨‍💻 MEDIUM', description=MEDIUM, days=365, cost=36000),
                    Subscription(name='🚀 PRO', description=PRO, days=31, cost=8000),
                    Subscription(name='🚀 PRO', description=PRO, days=183, cost=38400),
                    Subscription(name='🚀 PRO', description=PRO, days=365, cost=72000),
                    Coin(name='BTC'),
                    Coin(name='USDT'),
                    Coin(name='USDC'),
                    Coin(name='ETH'),
                ]   
            )
            await session.commit()

# func for recieve list of subs
async def get_subs(async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:
        return (await session.scalars(select(Subscription.name).distinct(Subscription.name, func.min(Subscription.id)).group_by(Subscription.name).order_by(func.min(Subscription.id)))).all()

# func for recieve sub
async def get_sub(async_session: async_sessionmaker[AsyncSession], name: str):
    async with async_session() as session:
        if name.startswith('subscription_'):
            name = name.replace('subscription_', '', 1)
            return (await session.scalars(select(Subscription).where(Subscription.name == name))).first()
        
async def get_full_sub(async_session: async_sessionmaker[AsyncSession], name: str, month: int = None):
    async with async_session() as session:
        days = 31 if month == 1 else 183 if month == 6 else 365
        return (await session.scalars(select(Subscription).where(Subscription.name==name, Subscription.days==days))).first()


def formatting(days) -> int:
    return days//30

async def get_month(async_session: async_sessionmaker[AsyncSession], name: str) -> list:
    async with async_session() as session:
        return [month for month in map(formatting, (await session.scalars(select(Subscription.days).where(Subscription.name == name))).all())]


async def get_user_profile(async_session: async_sessionmaker[AsyncSession], tg_id: int) -> str:
    async with async_session() as session:
        sub = (await session.scalars(select(Subscription).where(Subscription.id==(await session.scalars(select(User.subscription_id).where(User.tg_id==tg_id))).first()))).first()
        stock_markets = (await session.scalars(select(Stock.name).join(user_stock_coin_association_table, Stock.id==user_stock_coin_association_table.c.stock_id, isouter=False).join(User, User.tg_id==user_stock_coin_association_table.c.user_id, isouter=False).where(User.tg_id==tg_id))).all()
        coins = (await session.execute(select(user_stock_coin_association_table.c['id', 'currency']).where(user_stock_coin_association_table.c.user_id==tg_id))).all()
        try:
            stock_markets[0]
            stock_markets = " ".join(set(stock_markets))
        except:
            stock_markets = '❌ Не выбраны'
        try:
            coins[0]
            current_coins = '\n'
            for coin in coins:
                current_coins += f'  ◾️<b>{await session.scalar(select(Coin.name).join(user_stock_coin_association_table, user_stock_coin_association_table.c.coin_id==Coin.id).where(user_stock_coin_association_table.c.id==coin[0]))}</b>\n   └{coin[1]}\n'
        except:
            current_coins = '❌ Не выбраны' 
        try:
            sub = sub.name
        except:
            sub = '❌ Нет подписки'
        return f'Ваш профиль:\n\n├Подписка: {sub}\n├Выбранные биржи: {stock_markets}\n└Выбранные токены и фиаты для отслеживания:{current_coins}'
    
async def check_user_sub(async_session: async_sessionmaker[AsyncSession], tg_id: int) -> bool:
    async with async_session() as session:
        sub = (await session.scalars(select(Subscription).where(Subscription.id==(await session.scalars(select(User.subscription_id).where(User.tg_id==tg_id))).first()))).first()
        try:
            sub = sub.name # if object has attribute name
            return True
        except:
            return False # else
        
async def add_subscription_user(async_session: async_sessionmaker[AsyncSession], tg_id: int, sub) -> None:
    async with async_session() as session:
        await session.execute(insert(User).values(tg_id=tg_id, subscription_id=sub))
        await session.commit()


async def select_and_update_objects(async_session: async_sessionmaker[AsyncSession], name: str) -> None:
    async with async_session() as session:
        if name.startswith('subscription_'):
            result = (await session.scalars(select(Subscription).where(Subscription.name == name.replace('subscription_', '', 1)))).all()
            print(result)
        # result = (await session.scalars(select(User).where(User.tg_id==213444))).first()
        # print(result)
        # result = await session.scalars(select(Stock).where(user_stock_association_table.c.user_id==112344))
        # result = await session.scalars(select(Stock.id).where(Stock.name == 'Bybit'))
        # async with session.begin():
        #     user_stock_association_table.insert().values(user_id=1, stock_id=2)
        # result = await session.scalars(select(User).where(User.tg_id == 112344))
        # print(result.first())
        
async def get_positions(async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:
        usct = user_stock_coin_association_table
        result = (await session.execute(select(usct.c.user_id, Stock.name, Coin.name, usct.c['currency', 'type_order', 'limits', 'payment_methods']).join(Coin, Coin.id == user_stock_coin_association_table.c.coin_id, isouter=True).join(Stock, Stock.id == user_stock_coin_association_table.c.stock_id))).all()
        pprint(result)
        return result

# asyncio.run(get_positions(async_session=async_session))

