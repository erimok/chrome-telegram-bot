from Config import Config
from Receiver import FileReceiver, MusicReceiver
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot

config = Config()
bot = telebot.TeleBot(config.get_token())

# TODO replace to class
receivers = {
    MusicReceiver('Beatmaker', config, bot),
    FileReceiver('Mixing', config, bot),
    FileReceiver('Designer', config, bot),
    FileReceiver('Clothes', config, bot),
    FileReceiver('Other', config, bot)
}


@bot.message_handler(commands=['start'])
def start(message):
    welcome_message = config.get_config()['Common']['welcome_message']
    bot.send_message(message.chat.id, welcome_message, reply_markup=add_reply_buttons())


def add_reply_buttons() -> telebot.types.InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    for receiver in receivers:
        markup.add(InlineKeyboardButton(
            receiver.get_reply_button_text(),
            callback_data=receiver.get_key()
        ))

    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    for receiver in receivers:
        if call.data == receiver.get_key():
            receiver.ask_file(call.from_user.id)
            break


bot.polling()
