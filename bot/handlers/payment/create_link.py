import hashlib
from urllib.parse import urlencode
import random
import string
import time
import config

async def generate_order_number():
    order_number = int(time.time() * 1000)  # Используем миллисекунды для уникального идентификатора
    return str(order_number)


async def create_link_payment(amount, comment):

    merchant_id = config.merchant_id # ID Вашего магазина
    currency = config.currency # Валюта заказа
    secret = config.secret # Секретный ключ №1 из настроек магазина
    order_id = comment # Идентификатор заказа в Вашей системе
    desc = config.desc # Описание заказа
    lang = config.lang # Язык формы

    payform = dict()

    sign = f':'.join([
        str(merchant_id),
        str(amount),
        str(currency),
        str(secret),
        str(order_id)
    ])

    params = {
        'merchant_id': merchant_id,
        'amount': amount,
        'currency': currency,
        'order_id': order_id,
        'sign': hashlib.sha256(sign.encode('utf-8')).hexdigest(),
        'desc': desc,
        'lang': lang
    }

    payform['url'] = "https://aaio.so/merchant/pay?" + urlencode(params)
    payform['comment'] = order_id
    payform['price'] = amount
    return payform



async def check_aio_payment(order_id):
    import requests, sys
    from requests.exceptions import ConnectTimeout, ReadTimeout

    url = 'https://aaio.so/api/info-pay'
    api_key = 'ZTJmZmNiZWUtNzk0OC00Yjc1LWI5ZDItMDYzYjI2MWM0YWE3Okd4SGwkJXVaM0IhTjR2TTE0bzBMVFY4NncoVyp1YkNz' # Ключ API из раздела https://aaio.io/cabinet/api
    merchant_id = '8db82490-a261-49d8-abed-ef5e0acb07c9' # ID Вашего магазина

    params = {
        'merchant_id': merchant_id,
        'order_id': order_id
    }

    headers = {
        'Accept': 'application/json',
        'X-Api-Key': api_key
    }

    try:
        response = requests.post(url, data=params, headers=headers, timeout=(15, 60))
    except ConnectTimeout:
        print('ConnectTimeout') # Не хватило времени на подключение к сайту
        sys.exit()
    except ReadTimeout:
        print('ReadTimeout') # Не хватило времени на выполнение запроса
        sys.exit()
    if(response.status_code in [200, 400, 401]):
        try:
            response_json = response.json() # Парсинг результата
            
            return response_json['status']
        except:
            print('Response code: ' + str(response.status_code)) # Вывод неизвестного кода ответа
            return False
                  
    else:
        print('Response code: ' + str(response.status_code)) # Вывод неизвестного кода ответа
        return False