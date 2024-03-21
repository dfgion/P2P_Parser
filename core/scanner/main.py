from pprint import pprint
from redis import asyncio as aioredis
from ast import literal_eval
from core.utils.const.scanner import urls
from .messages import send_messages
import asyncio
import aiohttp



async def manage_scanning() -> None:
    while True:
        r = await aioredis.from_url("redis://localhost:8730")
        await r.aclose()
        try:
            info = literal_eval((await r.get('positions')).decode('utf-8'))
            info = await adaptation(information=info)
            for scan, users in info.items():
                await scanning(scanning_info=scan, users=users)
            await asyncio.sleep(10)
            break
        except Exception as e:
            print(e)
            print('Exception on server side. In part of scanning')
            break
            
async def scanning(scanning_info: dict, users: set[str]) -> None:
    market = scanning_info[0].lower()
    params, url = convertating(scanning_info)
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=params) as response:
            res = await response.json()
            if market == 'binance':
                if scanning_info[3].upper() == 'SELL':
                    if float(res['data'][0]['adv']['price']) >= float(scanning_info['price']):
                        await send_messages(users=users)    
                # If order_type is not "SELL", it means that the order is exactly "BUY", and we can skip the block with else and immediately write the second condition. All the conditions listed below are fulfilled in accordance with this rule.
                elif float(res['data'][0]['adv']['price']) <= float(scanning_info['price']):
                        await send_messages(users=users)   
            elif scanning_info[0] == 'Bitget':
                if scanning_info[3].upper() == 'SELL':
                    if float(res[something]) >= float(scanning_info['price']):
                        await send_messages(users=users)     
                elif float(res[something]) <= float(scanning_info['price']):
                        await send_messages(users=users)  
            elif scanning_info[0] == 'OKX':
                if scanning_info[3].upper() == 'SELL':
                    if float(res[something]) >= float(scanning_info['price']):
                        await send_messages(users=users)     
                elif float(res[something]) <= float(scanning_info['price']):
                        await send_messages(users=users)  
            elif scanning_info[0] == 'Bybit':
                if scanning_info[3].upper() == 'SELL':
                    if float(res[something]) >= float(scanning_info['price']):
                        await send_messages(users=users)     
                elif float(res[something]) <= float(scanning_info['price']):
                        await send_messages(users=users)  
            elif scanning_info[0] == 'Gate.io':
                if scanning_info[3].upper() == 'SELL':
                    if float(res[something]) >= float(scanning_info['price']):
                        await send_messages(users=users)     
                elif float(res[something]) <= float(scanning_info['price']):
                        await send_messages(users=users)  
            elif scanning_info[0] == 'Huobi':
                if scanning_info[3].upper() == 'SELL':
                    if float(res[something]) >= float(scanning_info['price']):
                        await send_messages(users=users)     
                elif float(res[something]) <= float(scanning_info['price']):
                        await send_messages(users=users)  
            elif scanning_info[0] == 'Bybit':
                if scanning_info[3].upper() == 'SELL':
                    if float(res[something]) >= float(scanning_info['price']):
                        await send_messages(users=users)     
                elif float(res[something]) <= float(scanning_info['price']):
                        await send_messages(users=users)    
            
                    
def convertating(scanning_info: dict) -> tuple[dict, list]:
    print(scanning_info)
    if scanning_info[0].lower() == 'binance':
        params = {
                    'asset': scanning_info[1], 
                    'countries': [],
                    'fiat': "USD", 
                    'page': 1, 
                    'proMerchantAds': 'false',
                    'publisherType': 'merchant',
                    'rows': 10,
                    'shieldMerchantAds': 'false',
                    'tradeType': scanning_info[3].upper()
                }
        url = urls[scanning_info[0].lower()]
        return (params, url)
    elif scanning_info[0] == 'Bitget':
        pass
    elif scanning_info[0] == 'OKX':
        pass
    elif scanning_info[0] == 'Bybit':
        pass
    elif scanning_info[0] == 'Gate.io':
        pass
    elif scanning_info[0] == 'Huobi':
        pass
    elif scanning_info[0] == 'Bybit':
        pass
        
    
async def adaptation(information: dict):
    result = {}
    for u, positions in information.items():
        for pos in positions:
            if tuple(pos.values()) in result:
                result[tuple(pos.values())].add(str(u))
            else:
                result.update({tuple(pos.values()): {str(u), }})
    return result

asyncio.run(manage_scanning())