from abc import abstractmethod

import telebot
from Config import Config


class Receiver:
    __chat_id: int

    @abstractmethod
    def send_message(self):
        pass

    def __init__(self, key: str, config: Config, bot: telebot.TeleBot):
        self.__reply_button_text = config.get_config()[key]['reply_button_text']
        self.__recipient_group_id = config.get_config()[key]['recipient_group_id']
        self.__file_request_message = config.get_config()[key]['file_request_message']
        self.__key = key
        self.__bot = bot

    def ask_file(self, chat_id: int):
        message = self.__bot.send_message(chat_id, self.__file_request_message)
        self.__chat_id = chat_id
        self.__bot.register_next_step_handler(message, self.send_message)

    def get_reply_button_text(self) -> str:
        return self.__reply_button_text

    def get_key(self) -> str:
        return self.__key


class MusicReceiver(Receiver):
    def send_message(self):
        self.__bot.send_message(self.__chat_id, 'success')


class DesignReceiver(Receiver):
    def send_message(self):
        return True


class WebDesignReceiver(Receiver):
    def send_message(self):
        return True


class ClothesReceiver(Receiver):
    def send_message(self):
        return True


class OtherReceiver(Receiver):
    def send_message(self):
        return True
