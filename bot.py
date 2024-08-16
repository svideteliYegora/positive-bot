import asyncio
import logging
import sys
import configparser
from aiogram import Bot, Dispatcher, types, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
import aiogram.exceptions
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from aiogram.enums.parse_mode import ParseMode
import text

# Получение значений из раздела Bot
API_TOKEN = '6537467286:AAEvcun5hkKYD9INATC9_-wyw-iS33Y_6mw'

# Диспетчер, бот
dp = Dispatcher()
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Словарь с фотографиями и текстом сообщений для каждого пункта
point_detail = {
    'point_minsk_main-office': [
        {
            'photo_ids': [
                'AgACAgIAAxkBAAIB82Z7tuTtNeLHdIefW0wDnxV0ZBtWAAJp3DEbscXgS5Y6PLmXUE2RAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIB9WZ7tuhQEnzikK4-Und33lbIpoumAAJq3DEbscXgS5yaxSQZngAB1QEAAwIAA3kAAzUE',
                'AgACAgIAAxkBAAIB92Z7tvDUZm0S3trdrkatLyWQwI8PAAJr3DEbscXgSwNPAWHx_7xZAQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIB-WZ7tvSzCyQLQDBtx3uxm9iBlyyoAAJs3DEbscXgSwP0JjjQqbrrAQADAgADeQADNQQ'
            ],
            'msg': text.STATIONARY_PREVENTION_CENTER_MNSK_LEVKOVA
        },
        {
            'photo_ids': [
                'AgACAgIAAxkBAAIB7WZ7tm55Yjmt74CddAITCXo6Uz9DAAJi3DEbscXgS99qy9JguhJ1AQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIB72Z7tnEJ4EVGJIhZcAVpKhAvooYYAAJj3DEbscXgSzcwi496K_k3AQADAgADeQADNQQ',
                'AgACAgIAAxkBAAIB8WZ7tnVJ0M8zsJ_7dWbe1I9XRwXoAAJl3DEbscXgS9hu6eRXpyxtAQADAgADeQADNQQ'
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

# Словарь для статистики


# keyboards
start_ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пункты профилактики', callback_data='prevention_points')],
    [InlineKeyboardButton(text='Онлайн-услуги', callback_data='online-services')],
    [InlineKeyboardButton(text='Связь с веб-аутрич', callback_data='outreach_communication')],
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
    [InlineKeyboardButton(text='НЛП-мастер, Менеджер Таня Ш', url='https://t.me/Solnce999', callback_data=None)],
    [InlineKeyboardButton(text='Юр.помощь\Веб-аутрич Аня Г', url='https://t.me/Anyagyl', callback_data=None)],
    [InlineKeyboardButton(text='Веб-аутрич Катя Р', url='https://t.me/katerosch', callback_data=None)],
    [InlineKeyboardButton(text='Веб-аутрич Митя М', url='https://t.me/Nem_pad', callback_data=None)],
    [InlineKeyboardButton(text='Веб-аутрич Игорь М', url='https://t.me/Web_Igor_M', callback_data=None)],
    [InlineKeyboardButton(text='Веб-аутрич Артур П', url='https://t.me/Den_Gaag', callback_data=None)],
    [InlineKeyboardButton(text='Веб-аутрич Егор К', url='https://t.me/flexxxLuthor', callback_data=None)],
    [InlineKeyboardButton(text='Веб-аутрич Артур С', url='https://t.me/Kordanchik', callback_data=None)],
    [InlineKeyboardButton(text='Назад', callback_data='back_start')]
])


@dp.message(F.photo)
async def img_handler(msg: Message) -> None:
    await msg.answer(text=msg.photo[-1].file_id)


@dp.message(Command('start'))
async def cmd_start_handler(msg: Message) -> None:
    await msg.answer(text=text.WELCOME, reply_markup=start_ikb)


@dp.message(Command('statistic786'))
async def cmd_statistic_handler(msg: Message) -> None:
    await msg.answer()


@dp.callback_query(F.data == 'prevention_points')
async def prevention_points_handler(cb_query: CallbackQuery) -> None:
    await cb_query.message.edit_text(text=text.CITY_SELECTION, reply_markup=cities_ikb)


@dp.callback_query(F.data == 'online-services')
async def online_services_handler(cb_query: CallbackQuery) -> None:
    await cb_query.message.edit_text(text=text.SERVICE_SELECTION, reply_markup=specialists_ikb)


@dp.callback_query(F.data.startswith('continue'))
@dp.callback_query(F.data.startswith('city'))
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


@dp.callback_query(F.data.startswith('back'))
async def back_handler(cb_query: CallbackQuery) -> None:
    cb_data = cb_query.data.split("_")[1]

    data = {
        'cities': [text.CITY_SELECTION, cities_ikb],
        'start': [text.WELCOME, start_ikb]
    }

    point = data[cb_data]
    msg_text = point[0]
    ikb = point[1]

    await cb_query.message.edit_text(text=msg_text, reply_markup=ikb)


@dp.callback_query(F.data.startswith('point'))
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


@dp.callback_query(F.data == 'outreach_communication')
async def outreach_handler(cb_query: CallbackQuery) -> None:
    await cb_query.message.edit_text(text=text.OUTREACH, reply_markup=outreach_ikb)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())