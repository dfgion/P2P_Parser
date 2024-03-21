from typing import Any, Awaitable, Callable, Dict, Union

from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile, Message
from aiogram import BaseMiddleware
from db.db_config import async_session
from db.db_func import check_user_sub, get_user_profile
from ..utils.keyboards.inline import profile_without_sub_kb

