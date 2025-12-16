#Импортирование_необходимых_библиотек
from telebot import *
from telebot import types as pg

#Подключение_к_нашему_боту
bot = TeleBot(open("token.txt").read()) #Создайте в папке с ботом txt файл и поместите в него токен вашего бота

#Блок_установленных_команд
commands = [pg.BotCommand("reviews", "обзоры"),
            pg.BotCommand("start", "документация") ]
bot.set_my_commands(commands)

#Создание_кнопки_для_удаления_постов
markup_delete = pg.InlineKeyboardMarkup()
btn_delete = pg.InlineKeyboardButton("удалить", callback_data="delete")
markup_delete.add(btn_delete)

#Хранение_информации_о_названии_фильма_и_соответсующих_ему_мнение_и_постер
movies = {"🦸‍♂️Супермен": ["Супермен.jpg"], "🦸‍♀️Супергерл": ["Супергерл.txt"], "Человек-паук": ["Человек-паук.txt"]}
#По моей задумке на первом месте листа соответсвующего ключа стоит постер фильма, а потом мнение

#Handler_команды_reviews
@bot.message_handler(commands = ["reviews"])
def handle_reviews(message):
    bot.delete_message(message.chat.id, message.message_id)
    markup = pg.InlineKeyboardMarkup(row_width=3)
    buttons = []
    for movie_name in movies.keys():
        btn = types.InlineKeyboardButton(movie_name, callback_data= f"{movie_name}")
        buttons.append(btn)
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i + 1])
        else:
            markup.add(buttons[i])
    bot.send_message(message.chat.id, "✨Выберите обзор фильма✨", reply_markup=markup)

#Handler_команды_documentations
@bot.message_handler(commands = ["start"])
def handle_documentation(message):
    bot.delete_message(message.chat.id, message.message_id)
    info = open("documentation.txt", "r", encoding="utf-8")
    content = info.read()
    bot.send_message(message.chat.id, content, reply_markup=markup_delete)
    info.close()

@bot.callback_query_handler(func=lambda call: call.data == "delete")
def delete_post(call):
    bot.delete_message(call.message.chat.id, call.message.id)

#Handler_callback_запросов
@bot.callback_query_handler(func=lambda call: True)
def callback_review(call):
    opinion = open(f"{movies[call.data][0]}", "rb")
    bot.send_photo(call.message.chat.id, opinion, "папв", reply_markup=markup_delete)









#Бесконечный_цикл_работы_бота
bot.infinity_polling()