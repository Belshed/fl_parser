import logging
import asyncio
from User import User
from Parser import Parser
from Project import Project
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

xml_url = 'https://www.fl.ru/rss/all.xml?category='
browser_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 OPR/67.0.3575.115',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}
category_id = 2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b %H:%M:%S')
logger = logging.getLogger('Parser Logger')

fh = logging.FileHandler('logs/bot_logs.log', mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

bot_token = '1078084297:AAGhNxLhFkhinnZNozIowvp42CxZSrGCLqs'

bot = Bot(token=bot_token)
dispatcher = Dispatcher(bot)

myParser = Parser(browser_headers, xml_url, category_id)
last_project = {'title': '', 'link': '', 'date': ''}
previous_projects = [last_project]

category_list = ['Все ктегории', 'Менеджмент', 'Разработка сайтов', 'Дизайн и арт', 'Все категории', 'Программирование', 'Оптимизация (SEO)', 'Переводы', 'Тексты']

new_projects = []

user = User()


def has_new_project():
    global last_project, previous_projects, new_projects

    parsed_page = myParser.parse_category()

    match_counter = 0

    for i in range(len(parsed_page)):
        try:
            if parsed_page[i].get('title') != previous_projects[i].get('title'):

                previous_projects = parsed_page

                new_projects.insert(0, parsed_page[i])
            else:
                match_counter += 1

        except IndexError:
            continue

    if match_counter == len(parsed_page):
        new_projects.clear()
        return False

    return True


def get_last_new_project():
    project = Project(new_projects[0].get('title'), new_projects[0].get('link'), new_projects[0].get('date'))

    return project.get_project()


def check_projects():
    if has_new_project():
        project_str = get_last_new_project()
        return project_str


def get_category_list():

    category_list_str = ''

    for i in range(len(category_list)):
        category_list_str += f"<b>{i}  —  {category_list[i]}</b>\n\n"

    return category_list_str


@dispatcher.callback_query_handler(lambda c: c.data)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    message_text = callback_query.data[-1]
    if message_text.isdigit() and len(message_text) == 1:
        myParser.set_category_id(message_text)
        myParser.set_extension(category_list[int(message_text)])
        user.set_next_step('category_checking')

        await bot.send_message(callback_query.from_user.id, f'Категория:\n<b>{category_list[int(message_text)]}</b>', parse_mode='html')

        while True:
            if has_new_project():
                await bot.send_message(callback_query.from_user.id, get_last_new_project(), parse_mode='html')
            await asyncio.sleep(120)


@dispatcher.message_handler(commands=['start'])
@dispatcher.async_task
async def entry_point(message: types.Message):
    user.set_user_id(message.from_user.id)
    user.set_user_name(message.from_user.username)
    user.set_chat_id(message.chat.id)
    user.set_next_step('category_choice')

    inline_keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

    for i in range(len(category_list)):
        inline_keyboard.insert(InlineKeyboardButton(str(i), callback_data=str(i)))

    await message.answer(f"Привет!\nВыбери категорию за которой хочешь следить⬇")
    await message.answer(get_category_list(), parse_mode='html', reply_markup=inline_keyboard)


@dispatcher.message_handler()
async def echo(message: types.Message):
    user.set_user_id(message.from_user.id)
    user.set_user_name(message.from_user.username)
    user.set_chat_id(message.chat.id)

    message_text = message.text.lower()

    category_button = KeyboardButton('Изменить категорию')
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(category_button)

    if message_text == 'проект':

        if has_new_project():
            await message.answer(get_last_new_project(), reply_markup=keyboard, parse_mode='html')
            return

        await message.answer('Новых проектов нет')

    elif message_text == 'изменить категорию':
        inline_keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

        for i in range(len(category_list)):
            inline_keyboard.insert(InlineKeyboardButton(str(i), callback_data=str(i)))

        await message.answer(f"Выбери категорию за которой хочешь следить⬇")
        await message.answer(get_category_list(), parse_mode='html', reply_markup=inline_keyboard)

    else:
        if user.get_next_step() == 'category_choice':
            if message_text.isdigit() and len(message_text) == 1:
                myParser.set_category_id(message_text)
                myParser.set_extension(category_list[int(message_text)])
                user.set_next_step('category_checking')

                await message.answer(f'Категория:\n<b>{category_list[int(message_text)]}</b>', parse_mode='html')

                while True:
                    if has_new_project():
                        await message.answer(get_last_new_project(), parse_mode='html')
                    await asyncio.sleep(120)
        else:
            await message.answer('Не понял, может так?', reply_markup=keyboard)


if __name__ == "__main__":
    try:
        executor.start_polling(dispatcher, skip_updates=True)

    except Exception as error:
        print(error)
