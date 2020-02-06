import os
import re
import requests
from bs4 import BeautifulSoup

from flask import Flask, request, url_for, render_template 

import telebot

app = Flask(__name__)
application = app

if __name__ == "__main__":
    app.run(debug=False)

# put your telegram bot TOKEN here

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет, ' + message.from_user.first_name)


@bot.message_handler(commands=['help'])
def start(message):
    bot.reply_to(message, """\

Your help message for users here

""")

# you can use 'rasp' command for getiing the week schedule or create your own function here

@bot.message_handler(commands=['rasp'])
def rasp(message):
    bot.reply_to(message, """\
Понедельник: .......,

Вторник: ...........,

Среда: .............,

Четверг: ...........,

Пятница: ...........,

Суббота: ............
""")


@bot.message_handler(commands=['hw'])
def send_welcome(message):
    bot.reply_to(message, """\
Введите дату и номер предмета через запятую 
в формате 01.01.2019,11 
Команда /help  - коды предметов
""")
    bot.register_next_step_handler(message, homework)

# homework function is used for getting homework by using subjects's id and the date. Get the subject's id from the www.dnevnik.ru.
# Then you can you use your own subjects's name for the request in send_welcome function.

def homework(message):
    info = message.text
    date = info[0:10]
    subj = info[-2:]

    subjects = {'01': 'subject id', '02': 'subject id', '03': 'subject id', '04': 'subject id',
                '05': 'subject id', '06': 'subject id', '07': 'subject id', '08': 'subject id',
                '09': 'subject id', '10': 'subject id', '11': 'subject id',
                '12': 'subject id', '13': 'subject id', '14': 'subject id',
                '15': 'subject id', '16': 'subject id',
                '17': 'subject id', '18': 'subject id'}

    for i in subjects:
        if i == subj:
            subj = subjects.get(subj)
            break
    s = requests.Session()
    data = {'login': 'YOUR LOGIN FOR DNEVNIK.ru', 'password': 'YOUR PASSWORD', }
    url = 'https://login.dnevnik.ru/login/esia/YOUR CITY'
    s.post(url, data=data)
    
    # put your child's ID and recent year in the right positions
    
    url = f'https://children.dnevnik.ru/homework.aspx?child=<CHILD ID>&tab=&studyYear=<STUDY YEAR>&subject={subj}&datefrom={date}&dateto={date}&choose=Показать'
    h = requests.get(url, cookies=s.cookies)

    with open('homework.html', 'w') as homework:
        homework.write(h.text)
        homework.close()

    with open('homework.html') as bs:
        soup = BeautifulSoup(bs, "html.parser")
        soup.prettify()

    subj = set()
    for i in soup.findAll(class_='tac light'):
        subj.add(i.text.strip())

    hw = set()
    for i in soup.findAll(class_='breakword'):
        hw.add(i.text.strip())
    subj = str(subj)
    hw = str(hw)
    bot.reply_to(message, subj)
    bot.reply_to(message, hw)

# hw_day function is a simple way to get the homework for the 1 day.

@bot.message_handler(commands=['hwday'])
def hw_day(message):
    bot.reply_to(message, 'Введите дату в формате 01.01.2001 за которую получаем домашние задания')
    bot.register_next_step_handler(message, get_hw)

def get_hw(message):
    date = message.text
    s = requests.Session()
    data = {'login': 'YOUR LOGIN FOR DNEVNIK.ru', 'password': 'PASSWORD', }
    url = 'https://login.dnevnik.ru/login/esia/YOUR CITY'
    s.post(url, data=data)

    # put your child's ID and recent year in the right positions

    url = f'https://children.dnevnik.ru/homework.aspx?child=<CHILD ID>&tab=&studyYear=<STUDY YEAR>&subject=&datefrom={date}&dateto={date}&choose=Показать'
    h = requests.get(url, cookies=s.cookies)
    with open('homework2.html', 'w', encoding='utf8') as homework:
        homework.write(h.text)
        homework.close()

    with open('homework2.html', encoding='utf8') as bs:
        soup = BeautifulSoup(bs, "html.parser")
        soup.prettify()

    subj = set()
    for i in soup.findAll(class_='tac light'):
        subj.add(i.text.strip())

    hw = set()
    for i in soup.findAll(class_='breakword'):
        hw.add(i.text.strip())
    subj = str(subj)
    hw = str(hw)
    bot.reply_to(message, subj)
    bot.reply_to(message, hw)


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your website/' + TOKEN)
    return render_template('index.html')

# If you don't have the index.html you can use this code:

# @app.route("/")
# def webhook():
    # bot.remove_webhook()
    # bot.set_webhook(url='https://your_website/' + TOKEN)
    # return "!", 200
