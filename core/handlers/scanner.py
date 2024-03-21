from ..config.cfg import bot
from ..utils.keyboards.inline import build_select_pos_kb, return_kb
from ..utils.statesgroup import ScannerStatesGroup
from ..utils.redis import formatting_text

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from redis import asyncio as aioredis

from ast import literal_eval

router = Router()

class LimitsErrorException(Exception):
    pass

@router.callback_query(ScannerStatesGroup.menu)
async def get_command(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'scan_options':
        r = await aioredis.from_url("redis://localhost:8730")
        info = literal_eval((await r.get('positions')).decode('utf-8'))
        await r.aclose()
        user_positions = info[callback_query.from_user.id]
        await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите позицию, которую вы хотите поменять', reply_markup=await build_select_pos_kb(length=len(user_positions)))
        await state.set_state(ScannerStatesGroup.positions)
    elif callback_query.data == 'current_positions':
        text = formatting_text(user_id=str(callback_query.from_user.id))
        await bot.send_message(chat_id=callback_query.from_user.id, text=text, reply_markup=return_kb)
    
@router.callback_query(ScannerStatesGroup.positions)
async def get_command(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    r = await aioredis.from_url("redis://localhost:8730")
    info = literal_eval((await r.get('positions')).decode('utf-8'))
    await r.aclose()
    if callback_query.data == 'position_1':
        data.update(info[callback_query.from_user.id][0])
    elif callback_query.data == 'position_2':
        data.update(info[callback_query.from_user.id][1])
    elif callback_query.data == 'position_3':
        data.update(info[callback_query.from_user.id][2])
    await state.set_data(data)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите биржу, которую хотите отслеживать')
    await state.set_state(ScannerStatesGroup.markets)

@router.callback_query(ScannerStatesGroup.markets)
async def get_started(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data.update({'market': callback_query.data})
    await state.set_data(data)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите монету, которую хотите отслеживать')
    await state.set_state(ScannerStatesGroup.token)
    
@router.callback_query(ScannerStatesGroup.token)
async def get_started(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data.update({'token': callback_query.data})
    await state.set_data(data)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите фиат, по которому будет отслеживаться монета')
    await state.set_state(ScannerStatesGroup.fiat)
    
@router.callback_query(ScannerStatesGroup.fiat)
async def get_started(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data.update({'fiat': callback_query.data})
    await state.set_data(data)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Выберите тип ордера, который хотите отслеживать')
    await state.set_state(ScannerStatesGroup.type_order)
    
@router.callback_query(ScannerStatesGroup.type_order)
async def get_started(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data.update({'type_order': callback_query.data})
    await state.set_data(data)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Введите лимиты, в пределах которых вы хотите отслеживать монету в формате 1000-10000, где 1000 - нижняя граница, а 10000 - верхняя граница\nЛибо введите "-", если хотите оставить пустым')
    await state.set_state(ScannerStatesGroup.limits)
    
@router.callback_query(ScannerStatesGroup.limits)
async def get_started(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        limits = message.text.split('-')
        list(map(int, limits))
        if limits[0] < limits[1]:
            data.update({'limits': message.text})
            await state.set_data(data)
            await bot.send_message(chat_id=message.from_user.id, text='Выберите метод оплаты, который хотите отслеживать')
            await state.set_state(ScannerStatesGroup.payment_method)
        else:
            raise LimitsErrorException
    except:
        await bot.send_message(chat_id=message.from_user.id, text='Введите лимиты в правильном формате')
        await bot.send_message(chat_id=message.from_user.id, text='Введите лимиты, в пределах которых вы хотите отслеживать монету в формате 1000-10000, где 1000 - нижняя граница, а 10000 - верхняя граница\nЛибо введите "-", если хотите оставить пустым')

@router.callback_query(ScannerStatesGroup.payment_method)
async def get_started(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data.update({'payment_method': callback_query.data})
    await state.set_data(data)
    