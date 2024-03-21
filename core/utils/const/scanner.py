SCAN_MENU = "👨‍💻Вы перешли в меню настройки отслеживания монет\n\nДля того, чтобы выдавать только нужную вам информацию, вы должны задать критерии сканирования бирж, а также сами биржи\n\nПараметры, которые вам нужно задать:\n\t<b>Биржи</b>\n\t<b>Монеты</b>\n\t<b>Тип ордера - Продажа\Покупка</b>\n\t<b>Способ оплаты</b>\n\t<b>Курс - определенный вами или по самой выгодной цене</b>\n<b>Диапазон, в котором мейкер работает - Лимит, к примеру, 2000-5000 usd</b>\n\nПервым делом задайте биржи, на которых будут отслеживаться монеты."

urls = {
    'binance': 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
    'bitget': 'https://www.bitget.com/v1/p2p/pub/adv/queryAdvList',
    'bybit': 'https://api2.bybit.com/fiat/otc/item/online',
    'okx': 'https://www.okx.com/v3/c2c/tradingOrders/getMarketplaceAdsPrelogin',
    'huobi': 'https://www.htx.com/-/x/otc/v1/data/trade-market',
    'gate.io': 'https://www.gate.io/ru/c2c/market',
    'mexc': 'https://p2p.mexc.com/api/market'
}