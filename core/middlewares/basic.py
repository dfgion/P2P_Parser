import asyncio
from typing import Any, Awaitable, Callable, Dict, Union

from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile, Message
from aiogram import BaseMiddleware
from db.db_config import async_session
from db.db_func import check_user_sub, get_user_profile
from ..utils.keyboards.inline import profile_without_sub_kb

class SubAccessMiddleware(BaseMiddleware):
    async def __call__(
            self, 
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]], 
            event: CallbackQuery, 
            data: Dict[str, Any]
    ) -> Any:
        if (event.data == 'profile'):
            if (await check_user_sub(async_session=async_session, tg_id=event.from_user.id)):
                data.update({'have_sub': True})
                return await handler(event, data)
            else:
                await event.bot.edit_message_media(chat_id=event.from_user.id, 
                                    message_id=event.message.message_id, 
                                    media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), 
                                                        caption=await get_user_profile(async_session=async_session, tg_id=event.from_user.id), parse_mode='HTML'), 
                                    reply_markup=profile_without_sub_kb)
                return await handler(event, data) 
        else:
            return await handler(event, data)