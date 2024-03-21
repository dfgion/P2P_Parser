from ..config.cfg import bot
from ..utils.const.basic import GREETING, SUBS_CAP, INSTRUCTION, MENU, SCANNER_START
from ..utils.const.subscriptions import TEST_SUBSCRIBE
from ..utils.keyboards.inline import profile_with_sub_kb, start_menu_kb, return_to_menu_kb, test_sub_kb, build_subscriptions_kb, scanner_menu_kb
from ..utils.statesgroup import MenuStatesGroup, SubscriptionsStatesGroup, ProfileStatesGroup, ScannerStatesGroup

from db.db_config import async_session
import db.db_func as df

from aiogram import F, Router
from aiogram.types import Message, FSInputFile, CallbackQuery, InputMediaPhoto
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext


router = Router()

@router.message(Command('start'))
async def start(message: Message, state: FSMContext):
    await message.answer_photo(photo=FSInputFile(path='core\static\pict1.jpg'), caption=GREETING, reply_markup=start_menu_kb, parse_mode='HTML')
    await state.set_state(MenuStatesGroup.start)
    print(message.from_user.id)
    print(message.from_user.first_name)

@router.callback_query(Command('profile'))
async def start(message: Message, state: FSMContext, have_sub: bool = None):
    await state.set_state(ProfileStatesGroup.main_page)
    if have_sub == True:
        caption = await df.get_user_profile(async_session=async_session, tg_id=message.from_user.id)
        await bot.edit_message_media(chat_id=message.from_user.id, 
                                     message_id=message.message_id, 
                                     media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), 
                                                           caption=caption, parse_mode='HTML'), 
                                     reply_markup=profile_with_sub_kb)
    # else middleware already send message
    
@router.callback_query(MenuStatesGroup.start)
async def select_option(callback_query: CallbackQuery, state: FSMContext, have_sub: bool = None):
    if callback_query.data == 'subscriptions':
        await state.set_state(SubscriptionsStatesGroup.subscribe)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=SUBS_CAP), reply_markup=await build_subscriptions_kb())
    elif callback_query.data == 'instruction':
        await state.set_state(MenuStatesGroup.instruction)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=INSTRUCTION), reply_markup=return_to_menu_kb)
    elif callback_query.data == 'profile':
        await state.set_state(ProfileStatesGroup.main_page)
        if have_sub == True:
            caption = await df.get_user_profile(async_session=async_session, tg_id=callback_query.from_user.id)
            await bot.edit_message_media(chat_id=callback_query.from_user.id, 
                                    message_id=callback_query.message.message_id, 
                                    media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), 
                                                        caption=caption, parse_mode='HTML'), 
                                    reply_markup=profile_with_sub_kb)
        # else middleware already send message
    elif callback_query.data == 'test_sub':
        await state.set_state(MenuStatesGroup.test_sub)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=TEST_SUBSCRIBE, parse_mode='HTML'), reply_markup=test_sub_kb)
    elif callback_query.data == 'start_scan':
        await state.set_data(ScannerStatesGroup.start)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=SCANNER_START, parse_mode='HTML'), reply_markup=scanner_menu_kb)
        await bot.send_message(chat_id=callback_query.from_user.id, text='🎲')

@router.callback_query(MenuStatesGroup.instruction)
async def show_instruction(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(MenuStatesGroup.start)
    await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\pict1.jpg'), caption=MENU, parse_mode='HTML'), reply_markup=start_menu_kb)


    