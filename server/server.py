from fastapi import FastAPI
from aiogram.types import Update

from contextlib import asynccontextmanager

import uvicorn

import aiofiles
import sys
sys.path.append(r'')

from core.config.cfg import bot, dp

@asynccontextmanager
async def on_startup():
    # webhook_url = f"WEBHOOK"
    # webhook_info = await bot.get_webhook_info()
    # if webhook_info.url != webhook_url:
    #     await bot.set_webhook(url=webhook_url)
    yield
              
@asynccontextmanager
async def on_shutdown() -> None:
    await bot.session.close()
    yield
    
app = FastAPI(on_startup=[on_startup], on_shutdown=[on_shutdown])

      
@app.post('/webhook')
async def telegram_webhook(update: dict):
    webhook_info = await bot.get_webhook_info()
    current_id = webhook_info.last_error_date
    async with aiofiles.open('server\last_update.log', 'r') as f:
        previous_id = await f.readline()
    if int(previous_id) < int(current_id):
        await dp.feed_webhook_update(bot=bot, update=Update(**update)) 
        async with aiofiles.open('server\last_update.log', 'w') as f:
            await f.write(str(current_id))
            
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9999)
            
    

    
    
