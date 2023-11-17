from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=r'C:\Users\Даниил\Desktop\P2P_Manager\venv\.env')

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()