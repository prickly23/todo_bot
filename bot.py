from random import choice
from datetime import datetime

import telebot

token = ''

bot = telebot.TeleBot(token)


RANDOM_TASKS = ['Поспать', 'Погладить кота', 'Прыгнуть три раза', 'Съесть слона', 'Решить квадратное уравнение', 'Внезапно моргнуть', 'Полежать как тюлень']

todos = dict()


HELP = '''
Список доступных команд:
/show  - напечать все задачи на заданную дату
/add - добавить задачу в формате "Дата, задача"
/random - добавить на сегодня смешную задачу
/help - Напечатать help
/delete_today - удалить задачи на сегодня
/delete - удалить задачи на заданную дату
'''



def add_todo(date, task):
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]




@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id,'''Вас приветствует ToDoBot!
Вот что я умею:
/show дд.мм.гг - напечать все задачи на заданную дату
/add дд.мм.гг задача - добавить задачу в формате "Дата, задача"
/random - добавить на сегодня смешную задачу
/help - Напечатать help
/delete_today - удалить задачи на сегодня
/delete дд.мм.гг - удалить задачи на выбранную дату
''')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['random'])
def random(message):
    task = choice(RANDOM_TASKS)
    date = datetime.today().strftime('%d.%m.%y')
    add_todo(date, task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на {date}')


@bot.message_handler(commands=['add'])
def add(message):
    _, date, tail = message.text.split(maxsplit=2)
    try:
        date != datetime.strptime(date, "%d.%m.%y").strftime('%d.%m.%y')
        task = ' '.join([tail])
        add_todo(date, task)
        bot.send_message(message.chat.id, f'Задача {task} добавлена на дату {date}')
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат даты! Попробуйте ДД.ММ.ГГ')



@bot.message_handler(commands=['show'])
def print_(message):
    try:
        date = message.text.split()[1]
        date != datetime.strptime(date, "%d.%m.%y").strftime('%d.%m.%y')
        if date in todos:
            tasks = ''
            for task in todos[date]:
                tasks += f'[ ] {task}\n'
                bot.send_message(message.chat.id, tasks)
        else:
            tasks = 'Такой даты нет'
            bot.send_message(message.chat.id, tasks)
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат даты! Попробуйте ДД.ММ.ГГ')


@bot.message_handler(commands=['delete_today'])
def delete_today(message):
    try:
        date = datetime.today().strftime('%d.%m.%y')
        del todos[date]
        bot.send_message(message.chat.id, 'На сегодня задач больше нет')
    except KeyError:
        sorry = 'Задач на сегодня не было'
        bot.send_message(message.chat.id, sorry)

@bot.message_handler(commands=['delete'])
def delete(message):
    _, date = message.text.split(maxsplit=1)
    try:
        del todos[date]
        bot.send_message(message.chat.id, f'На {date} задач больше нет')
    except KeyError:
        sorry = f'Задач на {date} не было'
        bot.send_message(message.chat.id, sorry)

@bot.message_handler(commands=['show_all'])
def show_all(message):
    if todos:
        for key, value in todos.items():
            bot.send_message(message.chat.id, '{0}: {1}'.format(key, value))
    else:
        bot.send_message(message.chat.id, 'Список задач пуст')

bot.polling(none_stop=True)
