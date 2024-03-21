from ..config.cfg import bot, dp
from ..utils.keyboards.inline import start_menu_kb, return_to_menu_kb, test_sub_kb, build_subscriptions_kb, scan_menu
from ..utils.statesgroup import ProfileStatesGroup, SubscriptionsStatesGroup, MenuStatesGroup, ScannerStatesGroup
from ..utils.const.basic import SUBS_CAP, MENU
from ..utils.const.scanner import SCAN_MENU

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(ProfileStatesGroup.main_page)
async def get_profile(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'subs':
        await state.set_state(SubscriptionsStatesGroup.subscribe)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=SUBS_CAP), reply_markup=await build_subscriptions_kb())
    elif callback_query.data == 'back':
        await state.set_state(MenuStatesGroup.start)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\p2p-begin.jpg'), caption=MENU, parse_mode='HTML'), reply_markup=start_menu_kb)
    elif callback_query.data == 'scanner_options':
        await state.set_state(ScannerStatesGroup.menu)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, media=InputMediaPhoto(media=FSInputFile(path='core\static\scanner_main.gif'), caption=SCAN_MENU, parse_mode='HTML'), reply_markup=scan_menu)
        
