from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from googletrans import Translator
import openai

storage = MemoryStorage()


openai.api_key = 'YOUR_OPENAI_API_KEY'

model_engine = 'text-davinci-003'

bot = Bot(token='YOUR_TG_BOT_TOKEN')

dp = Dispatcher(bot=bot, storage=storage)

model = "text-davinci-003"

trans = Translator()

kb = types.ReplyKeyboardMarkup(row_width=1)

ru_en_btn = types.KeyboardButton(text='/translate_EN-RU')
en_ru_btn = types.KeyboardButton(text='/translate_RU-EN')

kb.add(ru_en_btn, en_ru_btn)

start_message = """Hello, dear user, i\'m bot translator, now I can translate text from english to russia
i\'ve been created by developer with nickname f0rk1l"""

class UserStatesGroup(StatesGroup):

    en_ru_text = State()

    ru_en_text = State()

    en_essay = State()

    ru_essay = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    await message.answer(text=start_message, reply_markup=kb)

@dp.message_handler(commands=["translate_EN-RU"])
async def translate_en_ru(message: types.Message):

    await message.answer("enter text")

    await UserStatesGroup.en_ru_text.set()

@dp.message_handler(state=UserStatesGroup.en_ru_text)
async def send_translated_ru_text(message: types.Message, state: FSMContext):

    translated_message = trans.translate(message.text, dest='ru', src='en')

    await message.answer(f'Translated message: {translated_message.text}')

    await state.finish()

@dp.message_handler(commands=['translate_RU-EN'])
async def tranlate_ru_en(message: types.Message):

    await message.answer("enter text")

    await UserStatesGroup.ru_en_text.set()

@dp.message_handler(state=UserStatesGroup.ru_en_text)
async def send_tranlated_en_text(message: types.Message, state: FSMContext):

    translated_message = trans.translate(message.text, src='ru', dest='en')

    await message.answer(f"Translated message: {translated_message.text}")

    await state.finish()

@dp.message_handler(commands=['generate_en_essay'])
async def get_theme(message: types.Message):

    await message.answer("Enter rhe theme of essay")

    await UserStatesGroup.en_essay.set()

@dp.message_handler(state=UserStatesGroup.en_essay)
async def generate_en_essay(message: types.Message, state: FSMContext):

    completions =  openai.Completion.create(
        engine=model,
        prompt=f'Write essay about {message.text}',
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    await message.answer(completions.choices[0].text)

    await state.finish()

@dp.message_handler(commands=['generate_ru_essay'])
async def generate_ru_essay(message: types.Message):

    await message.answer("Enter the theme of essay")

    await UserStatesGroup.ru_essay.set()

@dp.message_handler(state=UserStatesGroup.ru_essay)
async def generate_en_essay(message: types.Message, state: FSMContext):

    completions =  openai.Completion.create(
        engine=model,
        prompt=f'Напиши эссе на тему {message.text}',
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    await message.answer(completions.choices[0].text)

    await state.finish()
    

if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True)