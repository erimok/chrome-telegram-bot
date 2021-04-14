import telebot

# Set config
api_id = 2673492
api_hash = '4f6639ab11162a9fbd9bd29ea3d90a79'
recipient_group_id = -332202964
token = '1605473986:AAGrtmJXGnhSLoxdaYe7V_Xmq8Z-g3lDXE0'
received_message = 'ℹ️ Вам были отправлены следующие данные:'
file_invalid_message = '⚠️ Разрешены только аудио файлы (mp3, wav). Загрузите, пожалуйста, файл в корретном формате'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    sent = bot.send_message(message.chat.id, "Добрый, как я могу к вам обращаться?")
    bot.register_next_step_handler(sent, get_name)


def get_name(message):
    audio_file = bot.send_message(message.chat.id,
                                  'Здравствуйте, {name}. Загрузите, пожалуйста, Ваш аудио файл (mp3, wav)'.format(
                                      name=message.text))
    bot.register_next_step_handler(audio_file, get_audio_file)


def get_audio_file(message):
    if message.document is not None:
        if is_valid_wav(message.document):
            send_file_to_recipient_chat(message)
        else:
            audio_file = bot.send_message(message.chat.id, file_invalid_message.format(name=message.text))
            bot.register_next_step_handler(audio_file, get_audio_file)

    if message.audio is not None:
        if is_valid_mp3(message.audio):
            send_audio_to_recipient_chat(message)
        else:
            audio_file = bot.send_message(message.chat.id, file_invalid_message.format(name=message.text))
            bot.register_next_step_handler(audio_file, get_audio_file)


def is_valid_wav(file_array: []) -> bool:
    if file_array.mime_type is not None:
        return file_array.mime_type == 'audio/x-wav'
    else:
        return False


def is_valid_mp3(audio_array: []) -> bool:
    # todo remove
    print(audio_array)
    return audio_array.mime_type == 'audio/mpeg'


def send_file_to_recipient_chat(message: []):
    try:
        bot.send_document(recipient_group_id, message.document.file_id)
        bot.send_message(recipient_group_id, received_message)
        bot.send_message(recipient_group_id, get_sender_account_info(message.from_user).format(parse_mode='HTML'))
        bot.send_message(message.chat.id, 'Ваши данные обрабатываются!')
    except Exception as ex:
        audio_file = bot.send_message(message.chat.id, "[!] error - {}".format(str(ex)) + '. Попробуйте еще раз')
        # todo remove
        bot.register_next_step_handler(audio_file, get_audio_file)


def send_audio_to_recipient_chat(message: []):
    try:
        bot.send_document(recipient_group_id, message.audio.file_id)
        bot.send_message(recipient_group_id, received_message)
        bot.send_message(recipient_group_id, get_sender_account_info(message.from_user).format(parse_mode='HTML'))
        bot.send_message(message.chat.id, 'Ваши данные обрабатываются!')
    except Exception as ex:
        audio_file = bot.send_message(message.chat.id, "[!] error - {}".format(str(ex)) + '. Попробуйте еще раз')
        bot.register_next_step_handler(audio_file, get_audio_file)


def get_sender_account_info(account_info) -> str:
    user = 'Сообщение отправил аккаунт: @' + account_info.username
    return user


bot.polling()
