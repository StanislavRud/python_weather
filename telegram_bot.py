import telebot
import pyowm
from pyowm import OWM
from pyowm.utils.config import get_default_config
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = pyowm.OWM(OPENWEATHERMAP_API_KEY, config_dict)
mgr = owm.weather_manager()

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode=None)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome! Please input your city.")


@bot.message_handler(content_types=['text'])
def send_welcome(message):

    place = message.text

    try:
        observation = mgr.weather_at_place(place).weather

        temp_now = observation.temperature('celsius')['temp']
        temp_min = observation.temperature('celsius')['temp_min']
        temp_max = observation.temperature('celsius')['temp_max']
        temp_feels_like = observation.temperature('celsius')['feels_like']

        wind = observation.wind()['speed']
        humidity = observation.humidity

        status = observation.status.lower()

        if 'rain' in status:
            icon = "🌧️"
        elif 'clouds' in status:
            icon = '☁️'
        elif 'clear' in status or 'sun' in status:
            icon = '☀️'
        elif 'snow' in status:
            icon = '❄️'
        else:
            icon = ""

        answer = "В городе " + place + " сейчас " + observation.detailed_status + icon + "\n"
        answer += "Температура в городе сейчас: " + str(round(temp_now)) + "℃" + "\n"
        answer += "Ощущается как: " + str(round(temp_feels_like)) + "℃" + "\n"
        answer += "Минимальная температура: " + str(round(temp_min)) + "℃" + "\n"
        answer += "Максимальная температура: " + str(round(temp_max)) + "℃" + "\n"
        answer += "Скорость ветра: " + str(round(wind)) + " М/с" + "\n"
        answer += "Влажность: " + str(humidity) + " %"
    except:
        answer = "Простите, но такой город не найден..."

    bot.send_message(message.chat.id, answer)

bot.polling( none_stop = True)