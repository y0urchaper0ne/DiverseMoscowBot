def bolshoi_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['большой петровский театр', 'большой петровский']:
        return 'Merci! Все так 🥳'
    else: 
        return 'Oh-la-la! Не совсем 😕'


def bolshoi_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['22']:
        return 'Bravo! Из вас хороший математик 🥳'
    else: 
        return 'Oh-la-la! Не совсем 😕'

def bolshoi_to_mxat_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['мхт', 'мхт чехова', 'мхт имени чехова', 'мхт им.чехова',
                        'московский художественный театр имени чехова', 
                        'московский художественный театр',]:
        return 'Génial! Следующая остановка нашего маршрута — МХТ им. Чехова!'
    else: 
        return 'Oh-la-la! Не совсем 😕'


def mxat_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['дядя ваня']:
        return 'Parfait! Вы абсолютно правы'
    else: 
        return 'Oh-la-la! Не совсем 😕'


def mxat_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['малая сцена']:
        return 'Chic! И правда'
    else: 
        return 'Oh-la-la! Не совсем 😕'
    

def mxat_to_nations_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['театр наций', 'наций']:
        return 'Génial! Следующая точка — Театр Наций!'
    else: 
        return 'Oh-la-la! Не совсем 😕'


def nations_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['утренники']:
        return 'Bravo! Все верно 🥳'
    else: 
        return 'Oh-la-la! Не совсем 😕'


def nations_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['флюгер']:
        return 'Bien! Вы очень внимательны'
    else: 
        return 'Oh-la-la! Не совсем 😕'


def nations_to_lenkom_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['ленком', 'ленком марка захарова',
                        'ленком им. марка захарова',
                        'ленком имени марка захарова']:
        return 'Génial! Мы направляемся к Ленкому Марка Захарова!'
    else: 
        return 'Oh-la-la! Не совсем 😕'


def lenkom_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['в день свадьбы']:
        return 'Parfait! Все так 🥳'
    else: 
        return 'Oh-la-la! Не совсем 😕'


def lenkom_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['марк захаров',
                        'марка захарова',
                        'захаров', 'захарова']:
        return 'Magnifique! Вы очень наблюдательны'
    else: 
        return 'Oh-la-la! Не совсем 😕'


def lenkom_to_electro_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['электротеатр', 
                        'электротеатр станиславский',
                        'электротеатр станиславского']:
        return 'Génial! Наша финальная точка — Электротеатр Станиславский!'
    else: 
        return 'Oh-la-la! Не совсем 😕'


def electro_history_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['50']:
        return 'Parfait! Вы абсолютно правы 👏'
    else: 
        return 'Oh-la-la! Не совсем 😕'


def electro_building_question(input_text):
    user_message = str(input_text).lower()
    if user_message in ['1918']:
        return 'Chic! И правда 🤗'
    else: 
        return 'Oh-la-la! Не совсем😕'
