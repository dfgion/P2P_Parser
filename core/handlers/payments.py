import os
from dotenv import load_dotenv

from aiogram import F, Router, Bot
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile, LabeledPrice, PreCheckoutQuery, Message
from aiogram.fsm.context import FSMContext

from db.db_config import async_session
import db.db_func as df

from ..config.cfg import bot, dp
from ..utils.statesgroup import SubscriptionsStatesGroup, PaymentStatesGroup, ProfileStatesGroup, MenuStatesGroup
from ..utils.const.basic import SUBS_CAP, MENU
from ..utils.const.subscriptions import SUCCESSFUL_PAYMENT
from ..utils.keyboards.inline import build_subscriptions_kb, return_to_profile, profile_with_sub_kb, start_menu_kb

load_dotenv(dotenv_path=r'C:\Users\Даниил\Desktop\P2P_Manager\venv\.env')

router = Router()

@dp.callback_query(SubscriptionsStatesGroup.buy)
async def buy_subscription(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'back':
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=SUBS_CAP), reply_markup=await build_subscriptions_kb())
        await state.clear()
        await state.set_state(SubscriptionsStatesGroup.subscribe)
    else:
        data = await state.get_data()
        await bot.send_invoice(
            chat_id=callback_query.from_user.id,
            title=f'Покупка подписки {data["subscription"].name},',
            description=f'💳 Сразу после оплаты вы получите подписку {data["subscription"].name} на срок {data["subscription"].days//30} мес.',
            provider_token=os.getenv(callback_query.data),
            payload=f'Bought {data["subscription"].name,} {data["subscription"].days//30} month',
            currency='rub',
            prices=[
                LabeledPrice(
                    label=f'Покупка {data["subscription"].name[2:]}',
                    amount=data["subscription"].cost*100
                )
            ],
            max_tip_amount=0
        )

@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)


@router.message()
async def successful_payment(message: Message, state: FSMContext):
    await bot.send_photo(chat_id=message.from_user.id, photo=FSInputFile(path='core\static\pict1.jpg'), caption=SUCCESSFUL_PAYMENT, reply_markup=return_to_profile, parse_mode='HTML')
    await df.add_subscription_user(async_session, tg_id=message.from_user.id, sub=(await state.get_data())['subscription'].id)
    await state.set_state(PaymentStatesGroup.wait)

@router.callback_query(PaymentStatesGroup.wait)
async def end_payment(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'menu':
        await state.set_state(MenuStatesGroup.start)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=MENU, parse_mode='HTML'), reply_markup=start_menu_kb)
    elif callback_query.data == 'profile':
        await state.set_state(ProfileStatesGroup.main_page)
        caption = await df.get_user_profile(async_session=async_session, tg_id=callback_query.from_user.id)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, 
                                message_id=callback_query.message.message_id, 
                                media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), 
                                                    caption=caption, parse_mode='HTML'), 
                                reply_markup=profile_with_sub_kb)
