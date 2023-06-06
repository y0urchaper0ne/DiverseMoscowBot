import time
import sqlite3

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from quizz import electro_building_question, electro_history_question
from location import check_location_electro
from texts.text_five import *
from levels.lvl_one import (get_building_score, get_history_score, 
                            main_menu_closed, main_menu_open, 
                            unit_menu_quizz, unit_menu_wo_quizz,
                            quizz_menu,)

# Подключение к базе данных SQLite
conn = sqlite3.connect('scores.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS scores
            (user_id INTEGER PRIMARY KEY, history_score FLOAT,
            building_score FLOAT, level FLOAT)''')


def electro_score(user_id):
    if get_building_score(user_id) == 5.0:
        building_score='Загадка на местности: ✅'
    else: building_score='Загадка на местности: ❌'
    if get_history_score(user_id) == 5.0:
        history_score='Загадка на историю: ✅'
    else: history_score='Загадка на историю: ❌' 
    return f'{history_score} \n{building_score}' 


def electro_transition(update, context):
    """Обработчик геолокации"""
    user_id = update.effective_chat.id
    response = check_location_electro(update, context)
    if response == 'True':
        c.execute("UPDATE scores SET level = level + 1.0 WHERE user_id = ?", (user_id,))
        conn.commit()
        c.execute("SELECT level FROM scores WHERE user_id = ?", (user_id,))
        update.message.reply_text(text=f'{electro_beginning}')
        time.sleep(3)
        update.message.reply_text(
            text='Про что рассказать вам — историю или здание?', 
            reply_markup=main_menu_closed)
        return 'ELECTRO_MAIN_MENU'
    update.message.reply_text(response)


def electro_main_menu(update, context):
    """Главное меню уровня"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'История 📜':
        if get_history_score(user_id) < 5.0:
            history_menu = unit_menu_quizz
        else: 
            history_menu = unit_menu_wo_quizz
        update.message.reply_text(text='Узнаем немного про историю!', reply_markup=history_menu)
        time.sleep(1)
        update.message.reply_text(
            text=f'{electro_history_text}', 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='История Электротеатра', url=electro_history_url)]]),
            )
        return 'ELECTRO_HISTORY'

    elif str(update.message.text) == 'Здание 🏛️':
        if get_building_score(user_id) < 5.0:
            building_menu = unit_menu_quizz
        else:
            building_menu = unit_menu_wo_quizz
        update.message.reply_text(text='Узнаем немного про здание!', reply_markup=building_menu)
        update.message.reply_text(
            text=f'{electro_building_text}', 
            reply_markup= InlineKeyboardMarkup([[InlineKeyboardButton(text='Здание Электротеатра', url=electro_building_url)]]),
            )
        return 'ELECTRO_BUILDING'
      
    elif str(update.message.text) == 'Перейти дальше 🔒' or str(update.message.text) == 'Перейти дальше 🔑':
        forward_menu = ReplyKeyboardMarkup([['Завершить экскурсию!']], resize_keyboard=True, one_time_keyboard=True)
        if get_building_score(user_id) < 5.0 or get_history_score(user_id) < 5.0:
            user_score = electro_score(user_id)
            update.message.reply_text(text=f'Вы решили не все загадки! \n\n{user_score}')
        elif get_building_score(user_id) >= 5.0 and get_history_score(user_id) >= 5.0:
            update.message.reply_text(
                text=f'Все хорошее рано или поздно заканчивается — как и наша прогулка, которая была' \
                    f' для меня просто замечательной. Надеюсь, и вам понравилась эта mini-экскурсия.',
                reply_markup=ReplyKeyboardRemove()) 
            time.sleep(2)
            update.message.reply_document(
                document = open('/Users/ilya/Desktop/hsetelegrambot/media/filal.pdf', 'rb'),
                caption=f'Merci за ваше участие и помощь — я бы точно не справился сам и не написал свою ' \
                    f'статью! В качестве благодарности поделюсь ею и с вами: там много того, о чем я не рассказывал.',)
            time.sleep(2)
            update.message.reply_text(
                text=f'Цените театр! Bonne chance! А я обратно во Францию — сдавать материал.',
                reply_markup=forward_menu) 
            return 'LEVEL_FIVE_END'

    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def electro_history(update, context):
    """Блок истории Электротеатра'"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'Загадка' and get_history_score(user_id) < 5.0:
        reply_markup = InlineKeyboardMarkup(quizz_menu)
        update.message.reply_photo(
            photo=open("/Users/ilya/Desktop/hsetelegrambot/media/electro_history.png", "rb"),
            caption = 'Пишите ответ внизу 👇',
            reply_markup=reply_markup)
        return 'ELECTRO_HISTORY_QUIZZ'
    elif str(update.message.text) == 'Назад':
        if get_building_score(user_id) == 5.0 and get_history_score(user_id) == 5.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'ELECTRO_MAIN_MENU'
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def electro_building(update, context):
    """Блок здания Электротеатра"""
    user_id = update.effective_chat.id

    if str(update.message.text) == 'Загадка' and get_building_score(user_id) < 5.0:
        reply_markup = InlineKeyboardMarkup(quizz_menu)
        update.message.reply_photo(
            photo=open("/Users/ilya/Desktop/hsetelegrambot/media/electro_building.png", "rb"),
            caption = 'Пишите ответ внизу 👇',
            reply_markup=reply_markup)
        return 'ELECTRO_BUILDING_QUIZZ'
    elif str(update.message.text) == 'Назад':
        if get_building_score(user_id) == 5.0 and get_history_score(user_id) == 5.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'ELECTRO_MAIN_MENU'
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')


def electro_history_quizz(update, context):
    """Вопрос по истории Электротеатра"""
    user_id = update.effective_chat.id

    text = str(update.message.text).lower()
    if text == 'назад':
        if get_building_score(user_id) == 5.0 and get_history_score(user_id) == 5.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'ELECTRO_MAIN_MENU'
    response = electro_history_question(text)
    if response == 'Parfait! Вы абсолютно правы 👏':
        c.execute("UPDATE scores SET history_score = history_score + 1.0 WHERE user_id = ?", (user_id,))
        conn.commit()
        c.execute("SELECT history_score FROM scores WHERE user_id = ?", (user_id,))
        update.message.reply_text(text=response, reply_markup=unit_menu_wo_quizz)
        return 'ELECTRO_HISTORY'
    update.message.reply_text(response)


def electro_history_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_reply_markup(reply_markup=reply_markup)
        query.message.reply_text(
            text='💡 Считается количество студентов и в оперном, и в драматическом классах', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_reply_markup()
        query.message.reply_text(
            text=f'Ответ: <tg-spoiler>50</tg-spoiler>', parse_mode='HTML')


def electro_building_quizz(update, context):
    """Вопрос про здание Электротеатра"""
    user_id = update.effective_chat.id
    text = str(update.message.text).lower()
    if text == 'назад':
        if get_building_score(user_id) == 5.0 and get_history_score(user_id) == 5.0:
            main_menu = main_menu_open
        else: main_menu = main_menu_closed
        update.message.reply_text(text='Выберите, про что хотите узнать!', reply_markup=main_menu)
        return 'ELECTRO_MAIN_MENU'
    response = electro_building_question(text)
    if response == 'Chic! И правда 🤗':
        c.execute("UPDATE scores SET building_score = building_score + 1.0 WHERE user_id = ?", (user_id,))
        conn.commit()
        c.execute("SELECT building_score FROM scores WHERE user_id = ?", (user_id,))
        update.message.reply_text(response, reply_markup=unit_menu_wo_quizz)
        return 'ELECTRO_BUILDING'
    update.message.reply_text(response)


def electro_building_quizz_menu_callback(update, context):
    """Обработчик меню с подсказкой"""
    query = update.callback_query
    query.answer()
    if query.data == 'hint':
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Показать ответ", callback_data='answer')]])
        query.edit_message_reply_markup(reply_markup=reply_markup)
        query.message.reply_text(
            text='💡 Через год после Октябрьской революции', parse_mode='HTML')    
    elif query.data == 'answer':
        query.edit_message_reply_markup()
        query.message.reply_text(
            text=f'Ответ: <tg-spoiler>1918</tg-spoiler>', parse_mode='HTML')


def level_five_end(update, context):
    """Обработчик перехода на новый уровень"""
    if str(update.message.text) == 'Завершить экскурсию!':
        update.message.reply_text(
            text=f'Экскурсия по театрам — все! Спасибо, что выбрали нас ☀️',
            reply_markup=ReplyKeyboardRemove())
        time.sleep(1)
        update.message.reply_text(
            text=f'Чтобы оставить отзыв, нажмите на \n/feedback в меню и напишите в чат свои комментарии. Мы все учтем!',)
        time.sleep(2)
        update.message.reply_text(
            text = f'А чтобы поддержать практику городских квестов и авторов в том числе, можно ' \
            f'<s>выписать чек</s> перевести любую сумму по ссылке внизу 👇 Благодарим за вклад в проект!',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Поддержать проект', url=donate_url)]]),
            parse_mode='HTML')
        return "LENKOM_TO_LENKOM_TRANSITION"
    else: update.message.reply_text(text=f'Простите, я вас не понял 🥺')
