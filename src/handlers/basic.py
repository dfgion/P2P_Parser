from ..config.cfg import bot, dp
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters.command import Command
from ..utils.const.basic import GREETING

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.reply('')
