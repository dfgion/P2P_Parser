from db.db_func import get_positions
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from core.utils.const.scanner import urls
from redis import asyncio as aioredis
import asyncio
from ast import literal_eval

async def set_values(async_session: async_sessionmaker[AsyncSession]):
    r = await aioredis.from_url("redis://localhost:8730")
    info: list[tuple[int | str]] = await get_positions(async_session=async_session)
    common_data: dict[str, list] = {}
    for entry in info:
        data_to_push = {entry[0]: [
                                    {
                                    'market': entry[1], 
                                    'token': entry[2], 
                                    'fiat': entry[3],
                                    'type_order': entry[4],
                                    'limits': entry[5],
                                    'payment_method': entry[6]
                                    },
                                   ]
                        }
        if entry[0] in common_data:
            common_data[entry[0]].append(data_to_push[entry[0]][0])
        else:
            common_data.update(data_to_push)
    await r.set('positions', str(common_data))
    await r.aclose()
    
async def formatting_text(user_id: str) -> str:
    r = await aioredis.from_url("redis://localhost:8730")
    info = literal_eval((await r.get('positions')).decode('utf-8')).get(user_id)
    await r.aclose()
    if info is None:
        return 'У вас нет активных позиций'
    else:  
        text_to_send = 'Ваши позиции:\n\n'
        i = 0
        delimiter = '\n\n'
        for pos in info:
            text_to_send += f'{i}. Биржа: {pos["market"]}\nМонета: {pos["token"]}\nФиат: {pos["fiat"]}\n Тип Ордера: {pos["type_order"]}\n Лимиты: {"Не указаны" if pos["limits"] is None else pos["limits"]}\n Способы оплаты: {"Не указаны" if pos["payment_method"] is None else pos["payment_method"]}'+ delimiter
            delimiter = ''
        return text_to_send
    