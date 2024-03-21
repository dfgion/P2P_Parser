from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os
from dotenv import load_dotenv
from db.models import Base

load_dotenv(dotenv_path=r'')

engine = create_async_engine(
        url=os.getenv("URL"),
        echo=True,
    )

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def async_start() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
