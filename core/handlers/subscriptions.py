from ..config.cfg import bot
from ..utils.keyboards.inline import start_menu_kb, return_to_menu_kb, build_subscriptions_kb, subscription_kb, payment_methods_kb, build_month_kb
from ..utils.statesgroup import MenuStatesGroup, SubscriptionsStatesGroup
from ..utils.const.basic import SUBS_CAP, MENU
from ..utils.const.subscriptions import TEST_SUBSCRIBE, MEDIUM

from db.db_config import async_session
from db.db_func import get_sub, get_full_sub

from aiogram import Router
from aiogram.types import FSInputFile, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

import asyncio

router = Router()

@router.callback_query(SubscriptionsStatesGroup.subscribe)
async def sub_options(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data.startswith('subscription_'):
        data = await get_sub(async_session, callback_query.data)
        await state.update_data({'subscription': data})
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=data.description, parse_mode='HTML'), reply_markup=subscription_kb)
        await state.set_state(SubscriptionsStatesGroup.info)
    elif callback_query.data == 'back':
        await state.set_state(MenuStatesGroup.start)
        msg = await bot.send_message(chat_id=callback_query.from_user.id, text='🕙Перенаправление в меню...🕙')
        await asyncio.sleep(1)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=MENU, parse_mode='HTML'), reply_markup=start_menu_kb)
        await msg.delete()

@router.callback_query(SubscriptionsStatesGroup.info)
async def get_data_subs(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'buy':
        await state.set_state(SubscriptionsStatesGroup.month)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path=r'core\static\buy_sub.jpg'), caption='На какое количество месяцев Вы бы хотели оформить подписку?\n\nℹ️<b>При выборе START, MEDIUM или PRO действует постоянная скидка\n ◾️ 20% на 6 месяцев\n ◾️ 25% на 12 месяцев.</b>', parse_mode='HTML'), reply_markup=await build_month_kb((await state.get_data())['subscription'].name))
    elif callback_query.data == 'back':
        await state.clear()
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=SUBS_CAP, parse_mode='HTML'), reply_markup=await build_subscriptions_kb())
        await state.set_state(SubscriptionsStatesGroup.subscribe)

@router.callback_query(SubscriptionsStatesGroup.month)
async def get_data_subs(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data.startswith('month_'):
        name_sub = (await state.get_data())['subscription'].name
        sub_object = await get_full_sub(async_session=async_session, name=name_sub, month=int(callback_query.data.replace('month_', '', 1)))
        await state.update_data({'subscription': sub_object})
        await state.set_state(SubscriptionsStatesGroup.buy)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption='Выберите удобный метод оплаты', parse_mode='HTML'), reply_markup=payment_methods_kb)
    elif callback_query.data == 'back':
        data = (await state.get_data())['subscription']
        print(f'Подписка {data}')
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=data.description, parse_mode='HTML'), reply_markup=subscription_kb)
        await state.set_state(SubscriptionsStatesGroup.info)
        

@router.callback_query(MenuStatesGroup.test_sub)
async def test_sub(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'back':
        await state.set_state(MenuStatesGroup.start)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=MENU, parse_mode='HTML'), reply_markup=start_menu_kb)
    elif callback_query.data == 'more':
        await bot.edit_message_caption(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, caption=TEST_SUBSCRIBE+'\n\n'+MEDIUM, parse_mode='HTML', reply_markup=return_to_menu_kb)

