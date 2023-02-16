import json
import telebot
from telebot import types
from app.request_round import Request
from app.todo_types import Todo

class Interface(Request):
    def __init__(self, url: str):
        self.url = url
        
url = 'url'
token = 'token'
HOST = Interface(url)

bot = telebot.TeleBot(token)

def smth(msg):
    bot.send_message(msg.chat.id, 'Выполнена ли задача?')
    @bot.message_handler(content_types=['text'])
    def recieving(msg: types.Message):
        return msg.text

def get_id(msg):
    bot.send_message(msg.chat.id, 'Введите id задачи')
    @bot.message_handler(content_types=['text'])
    def recieving(msg: types.Message):
        if isinstance(msg.text, int):
            return msg.text
        else:
            bot.send_message(msg.chat.id, 'Введите число!')


def get_buttons():
    keyboard = types.ReplyKeyboardMarkup()
    for button in ['create', 'read', 'update', 'delete', 'retrieve']:
        keyboard.add(types.KeyboardButton(button))
    return keyboard

@bot.message_handler(commands=['start'])
def starting_message(msg: types.Message):
    bot.send_message(
        msg.chat.id,
        f'Hi, {msg.from_user.full_name}. Please press buttons below to work with the todo list',
        reply_markup=get_buttons()
        )

@bot.message_handler(func=lambda msg: msg.text == 'create')
def answer_to_create(msg: types.Message):
    bot.send_message(msg.chat.id, 'Введите название задачи')

    def final(msg: types.Message):
        HOST.create_todo(Todo(msg.text))
        bot.send_message(msg.chat.id, 'Успех')

    bot.register_next_step_handler(msg, final)
        

@bot.message_handler(func=lambda msg: msg.text == 'read')
def answer_to_read(msg: types.Message):
    bot.send_message(msg.chat.id, json.dumps(HOST.get_all_todos(), indent=4))

@bot.message_handler(func=lambda msg: msg.text == 'update')
def answer_to_update(msg: types.Message):
    bot.send_message(msg.chat.id, 'Введите id задачи')
    
    def get_id(msg):
        id_ = msg.text
        todo = HOST.retrieve_todo(id_)
        if todo:
            bot.send_message(msg.chat.id, 'Введите новое название, либо None')
            bot.register_next_step_handler(msg, get_title, id_, todo)
        else:
            bot.send_message(msg.chat.id, 'Нет такой задачи')

    def get_title(msg, id_, todo):
        title = msg.text if msg.text != 'None' else todo['title']
        bot.send_message(msg.chat.id, 'Выполнена ли задача?')
        bot.register_next_step_handler(msg, final, id_, todo, title)

    def final(msg, id_, todo, title):
        is_done = msg.text
        HOST.update_todo(id_, Todo(title, is_done))
        bot.send_message(msg.chat.id, 'Успех')

    bot.register_next_step_handler(msg, get_id)

@bot.message_handler(func=lambda msg: msg.text == 'delete')
def answer_to_delete(msg: types.Message):
    bot.send_message(msg.chat.id, 'Введите id задачи')

    def final(msg):
        todo = HOST.delete_todo(msg.text)
        if todo:
            bot.send_message(msg.chat.id, 'Успех!')
        else:
            bot.send_message(msg.chat.id, 'Нет такой задачи')

    bot.register_next_step_handler(msg, final)

@bot.message_handler(func=lambda msg: msg.text == 'retrieve')
def answer_to_create(msg: types.Message):
    bot.send_message(msg.chat.id, 'Введите id задачи')

    def final(msg):
            todo = HOST.retrieve_todo(msg.text)
            if todo:
                bot.send_message(msg.chat.id, json.dumps(todo, indent=4))
            else:
                bot.send_message(msg.chat.id, 'Нет такой задачи')

    bot.register_next_step_handler(msg, final)
    
bot.polling()