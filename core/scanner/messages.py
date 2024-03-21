from core.config.cfg import bot

async def send_messages(users):
    for user in users:
        await bot.send_message(chat_id=user, text='Привет, по твоему сигналу найдена позиция!')