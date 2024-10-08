import logging
import os
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.utils.keyboard import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.enums.parse_mode import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import text

from config import data as params


API_TOKEN = os.environ['API_TOKEN']   # For get token in params Always Data
WEB_SERVER_HOST = params.WEBHOOK_HOST
WEBHOOK_PATH = params.WEBHOOK_PATH
WEBHOOK_URL = f"{WEB_SERVER_HOST}{WEBHOOK_PATH}"
WEBHOOK_SECRET = "my-secret"
WEB_SERVER_PORT = params.WEBAPP_PORT
WEBAPP_HOST = params.WEBAPP_HOST


router = Router()

logging.basicConfig(level=logging.INFO, stream=sys.stdout)



# Словарь для статистики


# keyboards
start_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пункты профилактики', callback_data='prevention_points')],
    [InlineKeyboardButton(text='Онлайн-услуги', callback_data='online-services')],
    [InlineKeyboardButton(text='Связь с веб-аутрич', callback_data='outreach')],
    [InlineKeyboardButton(text='Снижение вреда', callback_data='harm_reduction')]
])

drug_categories_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Опиоиды', callback_data='opioids')],
    [InlineKeyboardButton(text='Назад', callback_data='back_start')],
])

opioids_info_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Общая информация', callback_data='opioids_general_inf')],
    [InlineKeyboardButton(text='Что делать при передозировке?', callback_data='opioids_overdose')],
    [InlineKeyboardButton(text='Снижение вреда', callback_data='opioids_harm_reduction')],
    [InlineKeyboardButton(text='Назад', callback_data='back_drug-categories')]
])

opioids_general_inf_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Что такое опиоиды?', callback_data='opioids_what-is-it')],
    [InlineKeyboardButton(text='Как опиоиды работают?', callback_data='opioids_work')],
    [InlineKeyboardButton(text='Налоксон', callback_data='opioids_naloxone')],
    [InlineKeyboardButton(text='Как используются опиоиды?', callback_data='opioids_use')],
    [InlineKeyboardButton(text='Терапия опиоидными агонистами', callback_data='opioids_therapy')],
    [InlineKeyboardButton(text='Назад', callback_data='back_opioids-info')]
])

opioids_overdose_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Снизьте риски передозировки', callback_data='opioids_risk-reduction')],
    [InlineKeyboardButton(text='Признаки передозировки опиоидами', callback_data='opioids_overdose-signs')],
    [InlineKeyboardButton(text='Если человек не реагирует?', callback_data='opioids_person-not-react')],
    [InlineKeyboardButton(text='Первая помощь при передозировке опиоидами', callback_data='opioids_first-aid')],
    [InlineKeyboardButton(text='Назад', callback_data='back_opioids-info')]
])

opioids_harm_reduction_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подготовить место для инъекции', callback_data='opioids_injection-site')],
    [InlineKeyboardButton(text='Менять места инъекций', callback_data='opioids_prepare-injection-site')],
    [InlineKeyboardButton(text='Уменьшить шансы передозировки', callback_data='opioids_reduce-chances')],
    [InlineKeyboardButton(text='Назад', callback_data='back_opioids-info')]
])

opioids_work_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сердечно-легочная реанимация (СЛР) ', callback_data='opioids_slr')],
    [InlineKeyboardButton(text='Налоксон', callback_data='opioids_naloxone2')],
    [InlineKeyboardButton(text='Назад', callback_data='back_opioids-general-info')]
])

back_opioids_general_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='opioids_overdose')]
])

back_opioids_work_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_opioids-work')]
])

back_opioids_how_use_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_opioids-how-use')]
])

back_opioids_overdose_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='opioids_overdose')]
])

opioids_how_use_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Терапия опиоидными агонистами', callback_data='opioids_therapy2')],
    [InlineKeyboardButton(text='Связаться с наркологом', url='https://t.me/pozitivniynarkolog', callback_data='specialist_narcol')],
    [InlineKeyboardButton(text='Назад', callback_data='back_opioids-general-info')]
])

opioids_first_aid_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Налоксон', callback_data='opioids_naloxone3')],
    [InlineKeyboardButton(text='Сердечно-легочная реанимация (СЛР) ', callback_data='opioids_slr2')],
    [InlineKeyboardButton(text='Назад', callback_data='opioids_overdose')]
])

back_opioids_firs_aid_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='opioids_first-aid')]
])

back_opioids_harm_reduction_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='opioids_harm_reduction')]
])



cities_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Минск', callback_data='city_minsk')],
    [InlineKeyboardButton(text='Витебск', callback_data='city_vitebsk')],
    [InlineKeyboardButton(text='Пинск', callback_data='city_pinsk')],
    [InlineKeyboardButton(text='Барановичи', callback_data='city_baranovichi')],
    [InlineKeyboardButton(text='Орша', callback_data='city_orsha')],
    [InlineKeyboardButton(text='Светлогорск', callback_data='city_svetlogorsk')],
    [InlineKeyboardButton(text='Назад', callback_data='back_start')]
])

minsk_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Гл. офис (Левкова 20)', callback_data='point_minsk_main-office')],
    [InlineKeyboardButton(text='Офис 2 (Ольшевского 76 А)', callback_data='point_minsk_office-2')],
    [InlineKeyboardButton(text='Автобус 1', callback_data='point_minsk_bus-1')],
    [InlineKeyboardButton(text='Автобус 2', callback_data='point_minsk_bus-2')],
    [InlineKeyboardButton(text='Автобус 3', callback_data='point_minsk_bus-3')],
    [InlineKeyboardButton(text='Назад', callback_data='back_cities')]
])

vitebsk_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Офис 1 (Октябрьская 12)', callback_data='point_vitebsk_office-1')],
    [InlineKeyboardButton(text='Офис 2 (Берестеня 15)', callback_data='point_vitebsk_office-2')],
    [InlineKeyboardButton(text='Назад', callback_data='back_cities')]
])

pinsk_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Офис 1 (Советская 7)', callback_data='point_pinsk_office-1')],
    [InlineKeyboardButton(text='Автобус 1', callback_data='point_pinsk_bus-1')],
    [InlineKeyboardButton(text='Назад', callback_data='back_cities')]
])

baranovichi_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Офис 1 (3-й пер. Советский 3)', callback_data='point_baranovichi_office-1')],
    [InlineKeyboardButton(text='Назад', callback_data='back_cities')]
])

orsha_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Автобус 1', callback_data='point_orsha_bus-1')],
    [InlineKeyboardButton(text='Назад', callback_data='back_cities')]
])

svetlogorsk_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Офис 1 (м-н Первомайский 5)', callback_data='point_svetlogorsk_office-1')],
    [InlineKeyboardButton(text='Назад', callback_data='back_cities')]
])

specialists_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Позитивный психолог', url='https://t.me/pozitivniypsyholog', callback_data='specialist_psycho')],
    [InlineKeyboardButton(text='Дружественный нарколог', url='https://t.me/pozitivniynarkolog', callback_data='specialist_narcol')],
    [InlineKeyboardButton(text='Нестигматизирующий  инфекционист', url='https://t.me/pozitivniydoctor', callback_data='specialist_infect')],
    [InlineKeyboardButton(text='Лояльный юрист', url='https://t.me/Anyagyl', callback_data='specialist_jurist')],
    [InlineKeyboardButton(text='Заботливый хирург', url='https://t.me/pozitivniyhirurg', callback_data='specialist_surgeon')],
    [InlineKeyboardButton(text='Назад', callback_data='back_start')]
])

outreach_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='НЛП-мастер, Менеджер Таня Ш', url='https://t.me/solnce0525', callback_data=None)],
    [InlineKeyboardButton(text='Юр.помощь\Веб-аутрич Аня Г', url='https://t.me/Anyagyl', callback_data=None)],
    [InlineKeyboardButton(text='Веб-аутрич Катя Р', url='https://t.me/katerosch', callback_data=None)],
    [InlineKeyboardButton(text='Веб-аутрич Егор К', url='https://t.me/flexxxLuthor', callback_data=None)],
    [InlineKeyboardButton(text='Веб-аутрич Митя М', url='https://t.me/nemaulatka', callback_data=None)],
    [InlineKeyboardButton(text='Веб-аутрич Игорь М', url='https://t.me/Web_Igor_M', callback_data=None)],
    [InlineKeyboardButton(text='Веб-аутрич Артур П', url='https://t.me/Den_Gaag', callback_data=None)],
    [InlineKeyboardButton(text='Веб-аутрич Артур С', url='https://t.me/Kordanchik', callback_data=None)],
    [InlineKeyboardButton(text='Назад', callback_data='back_start')]
])


# Словарь с фотографиями и текстом сообщений для каждого пункта
point_detail = {
    'point_minsk_main-office': [
        {
            'photo_ids': [
                'AgACAgIAAxkBAAIFQWb8B6fvtGCmv8LXUCBDYBtuk7FGAAJP4TEbzebhS_yGIs_P4MTHAQADAgADeQADNgQ',
                'AgACAgIAAxkBAAIFQ2b8B64UepFGBHigV9lCg9x3-yR_AAJQ4TEbzebhS3s3eYI4-5tFAQADAgADeQADNgQ',
                'AgACAgIAAxkBAAIFRWb8B7OrJwvS2bwz_TwP-feMoNJpAAJR4TEbzebhSzTPcqmLAAGS6QEAAwIAA3kAAzYE',
                'AgACAgIAAxkBAAIFR2b8B7jmymkp0z2xu3eEh2ZMcko1AAJS4TEbzebhS4Z4Z81zBloLAQADAgADeQADNgQ'
            ],
            'msg': text.STATIONARY_PREVENTION_CENTER_MNSK_LEVKOVA
        },
        {
            'photo_ids': [
                'AgACAgIAAxkBAAIFSmb8B8pozRh4zN0ZOW0AAUyUSMy6MQACU-ExG83m4Uvi71r1zpZhmwEAAwIAA3kAAzYE',
                'AgACAgIAAxkBAAIFTGb8B87UmQcAAUkeHbFkWnJDLWTwmgACVOExG83m4Usw2NP9vQdaJAEAAwIAA3kAAzYE',
                'AgACAgIAAxkBAAIFTmb8B9IaXGElTMAfEf2B256DrMlqAAJV4TEbzebhSwWg4nWRK1A2AQADAgADeQADNgQ'
            ],
            'msg': text.SOCIAL_SUPPORT_CENTER_MNSK_LEVKOVA
        }
    ],
    'point_minsk_office-2': [
        {
            'photo_ids': [
                'AgACAgIAAxkBAAICDGZ7uU3XEFoBsL123zNxGJA__L8CAAJ53DEbscXgSz3qxRnGKBJSAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAICDmZ7uVcpq1rGjXPZj8acmiKz7JnHAAJ63DEbscXgS7vHUMTeg-4gAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAICEGZ7uV1IssPUrVg1MXrnkxKgC-CFAAJ73DEbscXgS502K9tDbEEZAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAICEmZ7uWE5Wha0Lz8k8omot2aZaqZJAAJ83DEbscXgS1qvFxYFmuLzAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAICFGZ7uWn-NMxTLpcXcdlAW_aCInQmAAJ93DEbscXgS2E50UmXunfqAQADAgADeQADNQQ'
            ],
            'msg': text.STATIONARY_PREVENTION_CENTER_MNSK_OLSHEVSKOGO
        }
    ],
    'point_minsk_bus-1': [
        {
            'photo_ids': [
                'AgACAgIAAxkBAAIBymZd0wGzv-khIZTGt5a2PW9UcnLuAALB4jEbcD3xSt_cNAnJkfuAAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIBy2Zd0wNyOtrcwgRXUG3IJbL74Z0XAALC4jEbcD3xSitIzVSSRUcXAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIBzmZd0wnOGLpcrf-kdDvGXEmZpkzaAALD4jEbcD3xSiI1lcOcOhegAQADAgADeQADNQQ'
            ],
            'msg': text.MOBILE_PREVENTION_POINT_1_MNSK,
        }
    ],
    'point_minsk_bus-2': [
        {
            'photo_ids': [
                'AgACAgIAAxkBAAIB42Z7tcWxJQnFLbpdGukIPHCHX9U-AAJb3DEbscXgS3zwxzbVwidIAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIB5WZ7tcqwJ7Yu9yvtJwnf-MVz7R9ZAAJc3DEbscXgSxDlcfJCJmwNAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIB52Z7tc-TJfNLvXsasYD9bAkqZ7XyAAJd3DEbscXgS_Om_u9GFNLyAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIB6WZ7tdQnTgrMCbkoZZQZ5r94YJchAAJe3DEbscXgS4VJjGyifWZfAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIB62Z7tdjGlXuRKkKUPq4fpLppdsGJAAJf3DEbscXgSzTgC_7-E1x8AQADAgADeQADNQQ'
            ],
            'msg': text.MOBILE_PREVENTION_POINT_2_MNSK
        }
    ],
    'point_minsk_bus-3': [
        {
            'photo_ids': [
                'AgACAgIAAxkBAAIB-2Z7t19z1mI5sqvi9MFadyLY3QJ8AAJt3DEbscXgS7Pwi3NHw8L0AQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIB_WZ7t2PI4sNIBsQa3UffkTurmnpfAAJu3DEbscXgSws0BrzUmRRQAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIB_2Z7t2fDF3Ly22zIo_KsasibzoDbAAJv3DEbscXgSz01qk_LHUVnAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAICAWZ7t2wBdRkhjGghDKG4taN_tLvDAAJw3DEbscXgS1dBRVrT5WodAQADAgADeQADNQQ'
            ],
            'msg': text.MOBILE_PREVENTION_POINT_3_MNSK
        }
    ],
    'point_vitebsk_office-1': [
        {
            'photo_ids': [],
            'msg': text.STATIONARY_PREVENTION_CENTER_VTB_OKTYABRSKAYA
        }
    ],
    'point_vitebsk_office-2': [
        {
            'photo_ids': [],
            'msg': text.SOCIAL_SUPPORT_CENTER_VTB_BERESTENYA
        }
    ],
    'point_pinsk_office-1': [
        {
            'photo_ids': [
                'AgACAgIAAxkBAAIBV2ZTHs_kEhYtQwiunSpvwJdyxXQ0AAIk2TEbiaGYSkdPRGQ8QxLmAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIBWWZTHtbtgx3XqWdvh3lSVzpqdX02AAIl2TEbiaGYSrL3B5Jw2hagAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIBW2ZTHtuLUQZJSfzheU7p9iDWnSg2AAIm2TEbiaGYSugWTY3RENKfAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIBXWZTHt_LIIobXBGY6eL0U04QZcGhAAIn2TEbiaGYSkHHWP-MaV9QAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIBX2ZTHugICVZKcAakA48nD67PzNJyAAIo2TEbiaGYSrw4rRWkrs_dAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIBYWZTHu7KPRoDb4JhYBe85U-HeiPOAAIp2TEbiaGYStF8YLH_EKHsAQADAgADeQADNQQ'
            ],
            'msg': text.STATIONARY_PREVENTION_CENTER_PINSK_SOVETSKAYA
        }
    ],
    'point_pinsk_bus-1': [
        {
            'photo_ids': [],
            'msg': text.MOBILE_PREVENTION_POINT_PINSK_SOVETSKAYA
        }
    ],
    'point_baranovichi_office-1': [
        {
            'photo_ids': [
                'AgACAgIAAxkBAAIBY2ZTH7wMkYNVJAMcuEarST_cJz9RAAIx2TEbiaGYSnf6MgUX_aUwAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIBZWZTH8EWRBJ9TzUKFF_o3-AAAcEdBwACMtkxG4mhmEoNEf_rh5WqbAEAAwIAA3kAAzUE',
                'AgACAgIAAxkBAAIBZ2ZTH8TKQET3XWKIMWpIQkZnXifzAAIz2TEbiaGYSjzQrGuHrQWCAQADAgADeQADNQQ'
            ],
            'msg': text.STATIONARY_PREVENTION_CENTER_BRNVCH_SOVETSKIY
        }
    ],
    'point_orsha_bus-1': [
        {
            'photo_ids': [],
            'msg': text.MOBILE_PREVENTION_POINT_ORSHA_NAVATOROV
        }
    ],
    'point_svetlogorsk_office-1': [
        {
            'photo_ids': [],
            'msg': text.STATIONARY_PREVENTION_CENTER_SVTGRSK_PERVOMAYSKIY
        }
    ],
}

# Словарь с фотографиями и текстом для сообщений по категориям наркотиков
drug_category_details = {
    'opioids_what-is-it': {
        'photo_ids': [
            'AgACAgIAAxkBAAIFXGcE45uL9l4N8cIL4JC9bEJsXEuMAALl3DEbT-IoSHW3QThRGAm8AQADAgADeQADNgQ'
        ],
        'msg': text.OPIOIDS_AND_OPIATES,
        'ikb': back_opioids_general_ikb
        },
    'opioids_work': {
        'photo_ids': [
        ],
        'msg': text.OPIOIDS_WORK,
        'ikb': opioids_work_ikb
    },
    'opioids_naloxone': {
        'photo_ids': [
            'AgACAgIAAxkBAAIFYGcE46BdVO9DeLZ-oQEGkDcaTBDMAALn3DEbT-IoSAtEHAzoO1ClAQADAgADeQADNgQ',
        ],
        'msg': text.OPIOIDS_NALOXONE,
        'ikb': back_opioids_general_ikb
    },
    'opioids_naloxone2': {
        'photo_ids': [
            'AgACAgIAAxkBAAIFYGcE46BdVO9DeLZ-oQEGkDcaTBDMAALn3DEbT-IoSAtEHAzoO1ClAQADAgADeQADNgQ',
        ],
        'msg': text.OPIOIDS_NALOXONE,
        'ikb': back_opioids_work_ikb
    },
    'opioids_slr': {
        'photo_ids': [
            'AgACAgIAAxkBAAIFXmcE457TvYxRCQTgKzjFv4dS7eH3AALm3DEbT-IoSMGrWz2c3lYYAQADAgADeQADNgQ',
        ],
        'msg': text.OPIOIDS_SLR,
        'ikb': back_opioids_work_ikb
    },
    'opioids_use': {
        'photo_ids': [],
        'msg': text.OPIOIDS_HOW_USE,
        'ikb': opioids_how_use_ikb
    },
    'opioids_therapy': {
        'photo_ids': [],
        'msg': text.OPIOIDS_THERAPY,
        'ikb': back_opioids_general_ikb
    },
    'opioids_therapy2': {
        'photo_ids': [],
        'msg': text.OPIOIDS_THERAPY,
        'ikb': back_opioids_how_use_ikb
    },
    'opioids_risk-reduction': {
        'photo_ids': [],
        'msg': text.OPIOIDS_REDUCE_RISK,
        'ikb': back_opioids_overdose_ikb
    },
    'opioids_overdose-signs': {
        'photo_ids': [],
        'msg': text.OPIOIDS_OVERDOSE_SIGNS,
        'ikb': back_opioids_overdose_ikb
    },
    'opioids_person-not-react': {
        'photo_ids': [
            'AgACAgIAAxkBAAIFYmcE46Ml3bK3QLrVmX2M0MIERhYNAALo3DEbT-IoSG8slWCXluhgAQADAgADeAADNgQ'
        ],
        'msg': text.OPIOIDS_PERSON_NOT_REACT,
        'ikb': back_opioids_overdose_ikb
    },
    'opioids_first-aid': {
        'photo_ids': [
            'AgACAgIAAxkBAAIFZGcE46XXZoP0BNo4kqMhLIPT8ggKAALp3DEbT-IoSKUPqA2R34aXAQADAgADeQADNgQ'
        ],
        'msg': text.OPIOIDS_FIRST_AID,
        'ikb': opioids_first_aid_ikb
    },
    'opioids_naloxone3': {
        'photo_ids': [
            'AgACAgIAAxkBAAIFYGcE46BdVO9DeLZ-oQEGkDcaTBDMAALn3DEbT-IoSAtEHAzoO1ClAQADAgADeQADNgQ',
        ],
        'msg': text.OPIOIDS_NALOXONE,
        'ikb': back_opioids_firs_aid_ikb
    },
    'opioids_slr2': {
        'photo_ids': [
            'AgACAgIAAxkBAAP4ZvxccSJFeKbbk5dBMwxE_XwnhYYAAtLoMRv4BeFLR5XUF0o9Gh8BAAMCAAN5AAM2BA',
        ],
        'msg': text.OPIOIDS_SLR,
        'ikb': back_opioids_firs_aid_ikb
    },
    'opioids_injection-site': {
        'photo_ids': [],
        'msg': text.OPIOIDS_INJECTION_SITE,
        'ikb': back_opioids_harm_reduction_ikb
    },
    'opioids_prepare-injection-site': {
        'photo_ids': [],
        'msg': text.OPIOIDS_PREPARE_IJECTION_SITE,
        'ikb': back_opioids_harm_reduction_ikb
    },
    'opioids_reduce-chances': {
        'photo_ids': [],
        'msg': text.OPIOIDS_REDUCE_CHANCES,
        'ikb': back_opioids_harm_reduction_ikb
    }
}


@router.message(F.photo)
async def img_handler(msg: Message) -> None:
    await msg.answer(text=msg.photo[-1].file_id)


@router.message(Command('start'))
async def cmd_start_handler(msg: Message) -> None:
    await msg.answer(text=text.WELCOME, reply_markup=start_ikb)


@router.message(Command('statistic786'))
async def cmd_statistic_handler(msg: Message) -> None:
    await msg.answer()


@router.callback_query(F.data.in_({'prevention_points', 'online-services', 'outreach', 'harm_reduction'}))
async def services_handler(cb_query: CallbackQuery) -> None:
    dt = cb_query.data

    services = {
        'prevention_points': [text.CITY_SELECTION, cities_ikb],
        'online-services': [text.SERVICE_SELECTION, specialists_ikb],
        'outreach': [text.OUTREACH, outreach_ikb],
        'harm_reduction': [text.CATEGORY_SELECTION, drug_categories_ikb]
    }
    txt_msg, ikb = services[dt][0], services[dt][1]

    await cb_query.message.edit_text(text=txt_msg, reply_markup=ikb)


@router.callback_query(F.data.in_({'opioids',}))
async def drug_categories_handler(cb_query: CallbackQuery) -> None:
    dt = cb_query.data

    drug_categories = {
        'opioids': [text.SECTION_SELECTION.format('Опиоиды. '), opioids_info_ikb]
    }
    txt_msg, ikb = drug_categories[dt][0], drug_categories[dt][1]

    await cb_query.message.edit_text(text=txt_msg, reply_markup=ikb)


@router.callback_query(F.data.in_({'opioids_general_inf', 'opioids_overdose', 'opioids_harm_reduction'}))
async def opioids_handler(cb_query: CallbackQuery) -> None:
    dt = cb_query.data
    opioids = 'Опиоиды. '
    inf = {
        'opioids_general_inf': [text.GENERAL_INFO.format(opioids), opioids_general_inf_ikb],
        'opioids_overdose': [text.OVERDOSE.format(opioids), opioids_overdose_ikb],
        'opioids_harm_reduction': [text.HARM_REDUCTION.format(opioids), opioids_harm_reduction_ikb]
    }
    txt_msg, ikb = inf[dt][0], inf[dt][1]
    await cb_query.message.edit_text(text=txt_msg, reply_markup=ikb)


@router.callback_query(F.data.in_({
    'opioids_what-is-it', 'opioids_work', 'opioids_naloxone', 'opioids_naloxone2', 'opioids_use', 'opioids_therapy',
    'opioids_therapy2', 'opioids_slr', 'opioids_risk-reduction', 'opioids_overdose-signs', 'opioids_person-not-react',
    'opioids_first-aid', 'opioids_naloxone3', 'opioids_slr2', 'opioids_injection-site',
    'opioids_prepare-injection-site', 'opioids_reduce-chances'
}))
async def opioid_general_inf_handler(cb_query: CallbackQuery) -> None:
    dt = cb_query.data

    await cb_query.message.delete()

    # получаем текст и id изображения
    drug_data = drug_category_details[dt]

    msg_text = drug_data['msg']
    photo_ids = drug_data['photo_ids']
    ikb = drug_data['ikb']
    if photo_ids:
        media = [InputMediaPhoto(media=photo_ids[0], caption=msg_text, parse_mode='HTML')]
        for photo_id in photo_ids[1:]:
            media.append(InputMediaPhoto(media=photo_id))
        await cb_query.bot.send_media_group(cb_query.from_user.id, media, )
        await cb_query.message.answer(text=text.SELECT_ACTION, reply_markup=ikb)
    else:
        await cb_query.message.answer(text=msg_text, reply_markup=ikb)


@router.callback_query(F.data.startswith('continue'))
@router.callback_query(F.data.startswith('city'))
async def cities_handler(cb_query: CallbackQuery) -> None:
    city = cb_query.data.split("_")[1]
    ikb_dict = {
        'minsk': minsk_ikb,
        'vitebsk': vitebsk_ikb,
        'pinsk': pinsk_ikb,
        'orsha': orsha_ikb,
        'baranovichi': baranovichi_ikb,
        'svetlogorsk': svetlogorsk_ikb
    }
    ikb = ikb_dict[city]
    await cb_query.message.edit_text(text=text.POINT_SELECTION, reply_markup=ikb)


@router.callback_query(F.data.startswith('back'))
async def back_handler(cb_query: CallbackQuery) -> None:
    cb_data = cb_query.data.split("_")[1]

    data = {
        'cities': [text.CITY_SELECTION, cities_ikb],
        'start': [text.WELCOME, start_ikb],
        'drug-categories': [text.CATEGORY_SELECTION, drug_categories_ikb],
        'opioids-info': [text.SECTION_SELECTION.format('Опиоиды. '), opioids_info_ikb],
        'opioids-work': [text.OPIOIDS_WORK, opioids_work_ikb],
        'opioids-how-use': [text.OPIOIDS_HOW_USE, opioids_how_use_ikb],
    }
    print(cb_query.data)
    print(data)
    print(cb_data)
    msg_text, ikb = data[cb_data][0], data[cb_data][1]
    await cb_query.message.edit_text(text=msg_text, reply_markup=ikb)


@router.callback_query(F.data.startswith('point'))
async def city_point_handler(cb_query: CallbackQuery) -> None:
    city = cb_query.data.split("_")[1]
    point_data = point_detail[cb_query.data]

    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data=f'continue_{city}')]
    ])

    await cb_query.message.delete()

    for item in point_data:
        photo_ids = item['photo_ids']
        msg_text = item['msg']

        if photo_ids:
            media = [InputMediaPhoto(media=photo_ids[0], caption=msg_text)]
            for photo_id in photo_ids[1:]:
                media.append(InputMediaPhoto(media=photo_id))
            await cb_query.bot.send_media_group(cb_query.from_user.id, media, )
        else:
            await cb_query.message.answer(text=msg_text)
    await cb_query.message.answer(text=text.CONTINUE, reply_markup=ikb)



async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
    logging.info('Bot starting successfully!')


def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Register startup hook to initialize webhook
    dp.startup.register(on_startup)

    # Initialize Bot instance with default bot properties which will be passed to all API calls
    # bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # And finally start webserver
    web.run_app(app, host=WEBAPP_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
