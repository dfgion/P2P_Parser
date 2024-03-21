from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from db.db_config import async_session
from db.db_func import get_subs, get_month



async def build_subscriptions_kb() -> InlineKeyboardMarkup:
    buttons = await get_subs(async_session)
    kb = [[InlineKeyboardButton(text=buttons[i], callback_data=f'subscription_{buttons[i]}')] for i in range(len(buttons))]
    kb.append([InlineKeyboardButton(text='🏛 Меню', callback_data='back')])
    return InlineKeyboardMarkup(inline_keyboard=kb)

async def build_month_kb(subscription_name) -> InlineKeyboardMarkup:
    buttons = await get_month(async_session, subscription_name)
    kb = [[InlineKeyboardButton(text=str(buttons[i]), callback_data=f'month_{buttons[i]}') for i in range(len(buttons))]]
    kb.append([InlineKeyboardButton(text='🏛 Меню', callback_data='back')])
    return InlineKeyboardMarkup(inline_keyboard=kb)

async def build_select_pos_kb(length):
    kb = [[InlineKeyboardButton(text=length[i], callback_data=f'position_{length[i]}')] for i in range(length)]
    kb.append([InlineKeyboardButton(text='🏛 Меню', callback_data='back')])
    return InlineKeyboardMarkup(inline_keyboard=kb)

scan_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🛠 Перейти к настройке', callback_data='scan_options')
    ],
    [
        InlineKeyboardButton(text='⏳ Активные позиции', callback_data='current_positions')
    ]
])

markets_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Binance', callback_data='binance')
    ],
    [
        InlineKeyboardButton(text='Bybit', callback_data='bybit')
    ],
    [
        InlineKeyboardButton(text='Bitget', callback_data='bitget')
    ],
    [
        InlineKeyboardButton(text='OKX', callback_data='okx')
    ],
    [
        InlineKeyboardButton(text='Huobi', callback_data='huobi')
    ],
    [
        InlineKeyboardButton(text='Gate.io', callback_data='gate.io')
    ],
    [
        InlineKeyboardButton(text='MEXC', callback_data='mexc')
    ],
    [
        InlineKeyboardButton(text='⬅️', callback_data='back')
    ]
])
    
scanner_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(text='🛠 Настройки отслеживания', callback_data='positions_settings')
                                                        ],
                                                        [
                                                            InlineKeyboardButton(text='⏳ Запуск отслеживания', callback_data='start_scan')
                                                        ]
                                                        ])

start_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(text='▶️ Видео-инструкция', callback_data='instruction')
                                                        ],
                                                        [
                                                            InlineKeyboardButton(text='🥢 Пробная версия', callback_data='test_sub')
                                                        ],
                                                        [
                                                            InlineKeyboardButton(text='➕ Подписки', callback_data='subscriptions')
                                                        ], 
                                                        [
                                                            InlineKeyboardButton(text='📊 Профиль', callback_data='profile')
                                                        ],
                                                        [
                                                            InlineKeyboardButton(text='Подробнее о P2P', callback_data='p2p_info')
                                                        ]
                                                        ])

test_sub_kb = InlineKeyboardMarkup(inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(text='Подробнее', callback_data='more')
                                                        ],
                                                        [
                                                            InlineKeyboardButton(text='⬅️', callback_data='back')
                                                        ]
                                                    ])

payment_methods_kb = InlineKeyboardMarkup(inline_keyboard=[
                                                            [
                                                                InlineKeyboardButton(text='Paymaster', callback_data='PAYMASTER_TOKEN')
                                                            ],
                                                            [
                                                                InlineKeyboardButton(text='Оплата криптовалютой', callback_data='CRYPTO_TOKEN')
                                                            ],
                                                            [
                                                            InlineKeyboardButton(text='⬅️', callback_data='back')
                                                            ]
                                                          ])

subscription_kb = InlineKeyboardMarkup(inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(text='Получить', callback_data='buy')
                                                        ],
                                                        [
                                                            InlineKeyboardButton(text='⬅️', callback_data='back')
                                                        ]
                                                    ])

return_to_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
                                                            [
                                                                InlineKeyboardButton(text='⬅️', callback_data='back')
                                                            ]
                                                        ])

profile_with_sub_kb = InlineKeyboardMarkup(inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(text='Настройка сканирования', callback_data='scanner_options')
                                                        ],
                                                        [
                                                            InlineKeyboardButton(text='Подписки', callback_data='subs')
                                                        ],
                                                        [
                                                            InlineKeyboardButton(text='⬅️', callback_data='back')
                                                        ]
                                                    ])
profile_without_sub_kb = InlineKeyboardMarkup(inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(text='Подписки', callback_data='subs')
                                                        ],
                                                        [
                                                            InlineKeyboardButton(text='⬅️', callback_data='back')
                                                        ]
                                                    ])

return_to_profile = InlineKeyboardMarkup(inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(text='📊 Профиль', callback_data='profile')
                                                        ],
                                                        [
                                                            InlineKeyboardButton(text='🏛 Меню', callback_data='menu')
                                                        ]
                                                    ])

return_kb = InlineKeyboardMarkup(inline_keyboard=[
                                                        [
                                                            InlineKeyboardButton(text='⬅️', callback_data='return')
                                                        ]
                                                    ])