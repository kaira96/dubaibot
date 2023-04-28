import logging
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.inline_keyboard import InlineKeyboardMarkup
import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class FSMAdmin(StatesGroup):
    text = State()


class ASMAdmin(StatesGroup):
    delete = State()


API_TOKEN = '6063269554:AAGZeGopkvT5PTPlKJ7szlj_feShCZsUmsw'

keyboard = [
    [types.KeyboardButton(text='❓Вопросы❓')],
    [types.KeyboardButton(text='О нас')],
    [types.KeyboardButton(text='Контакты')],
    [types.KeyboardButton(text='Настройки')],
]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['text'], state=None)
async def register(message: types.Message):
    await message.reply('Напишите ключевые слова')
    await FSMAdmin.text.set()


@dp.message_handler(commands=['text'], state=None)
async def asewrq(message: types.Message):
    await message.reply('Напишите ключевые слова')
    await ASMAdmin.delete.set()


@dp.message_handler(state=FSMAdmin.text)
async def load_username(message: types.Message, state: FSMContext):
    with open('texts.json', 'r', encoding='utf8') as f:
        data = json.load(f)
    if message.text.lower() == 'stop':
        await message.answer(f'Спасибо, вот список ваших ключевых слов {data["message"]}')
        await state.finish()
    else:
        print(message.text)
        data['message'].append(message.text)
        with open('texts.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)
        await message.reply('Можете написать еще ключевые слова или написать stop')


@dp.message_handler(state=ASMAdmin.delete)
async def load_dasusername(message: types.Message, state: FSMContext):
    print(state)
    with open('texts.json', 'r', encoding='utf8') as f:
        data = json.load(f)
    if message.text.lower() == 'stop':
        await message.answer(f'Спасибо, вот список ваших исключенных слов {data["delete"]}')
        await state.finish()
    else:
        print(message.text)
        data['delete'].append(message.text)
        with open('texts.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)
        await message.reply('Можете написать еще исключенные слова или написать stop')

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    kb = types.ReplyKeyboardMarkup(keyboard=keyboard)
    await message.reply("Добрый день\nЯ телеграмм бот который поможет и ответит на ваши вопросы", reply_markup=kb)


@dp.message_handler()
async def echo(message: types.Message):
    with open('texts.json', 'r', encoding='utf8') as f:
        data = json.load(f)

    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    if message.text == 'Настройки':
        inline_keyboard.add(types.InlineKeyboardButton(text='✅Посмотреть ключевые слова', callback_data='show_add'), types.InlineKeyboardButton(text='✅Посмотреть ключевые слова', callback_data='show_del'))
        inline_keyboard.add(types.InlineKeyboardButton(text='✅Добавит ключевые слова', callback_data='add'), types.InlineKeyboardButton(text='✅Исключить ключевые слова', callback_data='delete'))
        inline_keyboard.add(types.InlineKeyboardButton(text='❌Удалить ключевые слова', callback_data='delete_add'), types.InlineKeyboardButton(text='❌Удалить исключенные ключевые слова', callback_data='delete_del'))
        await message.answer('Настройки Юзербота', reply_markup=inline_keyboard)
    if message.text == '❓Вопросы❓':
        for i in data['quistions'].keys():
            inline_keyboard.add(types.InlineKeyboardButton(text=i, callback_data=i))

        await message.answer('Вот ответы на твои вопросы', reply_markup=inline_keyboard)
    elif message.text == 'О нас':
        await message.answer(data['About'])
    elif message.text == 'Контакты':
        await message.answer(data['Контакты'])


@dp.callback_query_handler()
async def call_back(call: types.CallbackQuery):
    with open('texts.json', 'r', encoding='utf8') as f:
        data = json.load(f)
    if call.data == 'add':
        await register(message=call.message)
    elif call.data == 'show_add':
        await bot.send_message(chat_id=call.from_user.id, text=f'{[data["message"]]}')
    elif call.data == 'show_del':
        await bot.send_message(chat_id=call.from_user.id, text=f'{[data["delete"]]}')
    elif call.data == 'delete':
        await asewrq(message=call.message)
    elif call.data == 'delete_add':
        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        for i in data['message']:
            inline_keyboard.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'delete_add-{i}'))
        await bot.send_message(chat_id=call.from_user.id, text='Выберите ключевые слова на удаление', reply_markup=inline_keyboard)
    elif call.data == 'delete_del':
        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        for i in data['message']:
            inline_keyboard.add(types.InlineKeyboardButton(text=f'{i}', callback_data=f'delete_del-{i}'))
        await bot.send_message(chat_id=call.from_user.id, text='Выберите ключевые слова на удаление', reply_markup=inline_keyboard)
    elif 'delete_add-' in call.data:
        data['message'].remove(call.data.split('delete_add-')[-1])
        with open('texts.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)
        await bot.send_message(chat_id=call.from_user.id, text='Удалено')
    elif 'delete_del-' in call.data:
        data['message'].remove(call.data.split('delete_del-')[-1])
        with open('texts.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)
        await bot.send_message(chat_id=call.from_user.id, text='Удалено')
    else:
        with open('texts.json', 'r', encoding='utf8') as f:
            data = json.load(f)
        await bot.send_message(chat_id=call.from_user.id, text=data['quistions'][call.data])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
