from abc import abstractmethod

import telebot
from Config import Config
from Validation import TelegramValidation


class Receiver:
    __chat_id: int
    __file_type: str

    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def send_to_recipient_chat(self, message):
        pass

    def __init__(self, key: str, config: Config, bot: telebot.TeleBot):
        self.__reply_button_text = config.get_config()[key]['reply_button_text']
        self._recipient_group_id = config.get_config()[key]['recipient_group_id']
        self._validation_message = config.get_config()[key]['validation_message']
        self._file_request_message = config.get_config()[key]['file_request_message']
        self._success_message = config.get_config()[key]['success_message']
        self._message_to_admin_chat = config.get_config()[key]['message_to_admin_chat']
        self._sender_message = config.get_config()['Common']['sender_message']
        self._key = key
        self._bot = bot

    def ask_file(self, chat_id: int):
        print('ask file')
        message = self._bot.send_message(chat_id, self._file_request_message)
        self.__chat_id = chat_id
        self._bot.register_next_step_handler(message, self.send_message)

    def get_thank_you_message(self, message):
        self._bot.send_message(message.chat.id, self._success_message)

    # TODO need to implement
    def _is_start_bot(self) -> None:
        return

    def get_reply_button_text(self) -> str:
        return self.__reply_button_text

    def get_key(self) -> str:
        return self._key


class MusicReceiver(Receiver):
    def send_message(self, message):
        if message.document is not None:
            if TelegramValidation.is_valid_wav(message.document):
                self.__file_type = 'wav'
                self.send_to_recipient_chat_wav(message)
                return self.get_thank_you_message(message)

        if message.audio is not None:
            if TelegramValidation.is_valid_mp3(message.audio):
                self.__file_type = 'mp3'
                self.send_to_recipient_chat_mp3(message)
                return self.get_thank_you_message(message)

        validation = self._bot.send_message(message.chat.id, self._file_request_message)
        return self._bot.register_next_step_handler(validation, self.send_message)

    def send_to_recipient_chat(self, message):
        if self.__file_type == 'vaw':
            self.send_to_recipient_chat_wav(message)
        if self.__file_type == 'mp3':
            self.send_to_recipient_chat_mp3(message)
        self.get_thank_you_message(message)

    # TODO rework
    def send_to_recipient_chat_wav(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_document(self._recipient_group_id, message.document.file_id)
            self._bot.send_message(self._recipient_group_id,
                                   self._sender_message + ' ' + get_user_link(message.from_user.username))
        except Exception as ex:
            audio_file = self._bot.send_message(message.chat.id, '[!] error - '
                                                                 '{}'.format(str(ex)) + '. Попробуйте еще раз')
            self._bot.register_next_step_handler(audio_file, 'start')

    def send_to_recipient_chat_mp3(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_document(self._recipient_group_id, message.audio.file_id)
            self._bot.send_message(self._recipient_group_id,
                                   self._sender_message + ' ' + get_user_link(message.from_user.username))
        except Exception as ex:
            audio_file = self._bot.send_message(message.chat.id, '[!] error - '
                                                                 '{}'.format(str(ex)) + '. Попробуйте еще раз')
            self._bot.register_next_step_handler(audio_file, 'start')


class FileReceiver(Receiver):
    def send_message(self, message):
        if message.photo is not None:
            self.__file_type = 'photo'
            self.send_to_recipient_chat_photo(message)
            return self.get_thank_you_message(message)

        if message.document is not None:
            if TelegramValidation.is_valid_pdf(message.document) or TelegramValidation.is_valid_svg(message.document):
                self.__file_type = 'document'
                self.send_to_recipient_chat_document(message)
                return self.get_thank_you_message(message)

        validation = self._bot.send_message(message.chat.id, self._file_request_message)
        return self._bot.register_next_step_handler(validation, self.send_message)

    def send_to_recipient_chat(self, message):
        if self.__file_type == 'document':
            self.send_to_recipient_chat_document(message)
        if self.__file_type == 'photo':
            self.send_to_recipient_chat_photo(message)
        self.get_thank_you_message(message)

    # TODO move to abstract
    def send_to_recipient_chat_document(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_document(self._recipient_group_id, message.document.file_id)
            self._bot.send_message(self._recipient_group_id,
                                   self._sender_message + ' ' + get_user_link(message.from_user.username))
        except Exception as ex:
            file = self._bot.send_message(message.chat.id, '[!] error - '
                                                           '{}'.format(str(ex)) + '. Попробуйте еще раз')
            self._bot.register_next_step_handler(file, 'start')

    # TODO need to fix
    def send_to_recipient_chat_photo(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_photo(self._recipient_group_id, message.photo[-1].file_id)
            self._bot.send_message(self._recipient_group_id,
                                   self._sender_message + ' ' + get_user_link(message.from_user.username))
        except Exception as ex:
            file = self._bot.send_message(message.chat.id, '[!] error - '
                                                           '{}'.format(str(ex)) + '. Попробуйте еще раз')
            self._bot.register_next_step_handler(file, 'start')


def get_user_link(username: str) -> str:
    return '@' + username
