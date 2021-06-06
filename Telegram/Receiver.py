from abc import abstractmethod

import telebot
from Config import Config
from Validation import TelegramValidation as Validation


class Receiver:
    __chat_id: int

    @abstractmethod
    def send_message(self, message):
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
        message = self._bot.send_message(chat_id, self._file_request_message)
        self.__chat_id = chat_id
        self._bot.register_next_step_handler(message, self.send_message)

    def get_thank_you_message(self, message):
        self._bot.send_message(message.chat.id, self._success_message)

    def send_to_recipient_chat_wav(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_document(self._recipient_group_id, message.document.file_id)
            self._bot.send_message(self._recipient_group_id,
                                   self._sender_message + ' ' + get_user_link(message.from_user.username))
        except Exception as ex:
            self.send_exception_info(message, ex)

    def send_to_recipient_chat_mp3(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_document(self._recipient_group_id, message.audio.file_id)
            self._bot.send_message(self._recipient_group_id,
                                   self._sender_message + ' ' + get_user_link(message.from_user.username))
        except Exception as ex:
            self.send_exception_info(message, ex)

    def send_to_recipient_chat_document(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_document(self._recipient_group_id, message.document.file_id)
            self._bot.send_message(self._recipient_group_id,
                                   self._sender_message + ' ' + get_user_link(message.from_user.username))
        except Exception as ex:
            self.send_exception_info(message, ex)

    def send_to_recipient_chat_photo(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_photo(self._recipient_group_id, message.photo[-1].file_id)
            self._bot.send_message(self._recipient_group_id,
                                   self._sender_message + ' ' + get_user_link(message.from_user.username))
        except Exception as ex:
            self.send_exception_info(message, ex)

    def send_to_recipient_chat_video(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_video(self._recipient_group_id, message.video.file_id)
            self._bot.send_message(self._recipient_group_id,
                                   self._sender_message + ' ' + get_user_link(message.from_user.username))
        except Exception as ex:
            self.send_exception_info(message, ex)

    def send_to_recipient_chat_animation(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_animation(self._recipient_group_id, message.animation.file_id)
            self._bot.send_message(self._recipient_group_id,
                                   self._sender_message + ' ' + get_user_link(message.from_user.username))
        except Exception as ex:
            self.send_exception_info(message, ex)

    def send_exception_info(self, message, ex: Exception):
        file = self._bot.send_message(message.chat.id, '⚠️ error - '
                                                       '{}'.format(str(ex)) + '. Попробуйте еще раз')
        self._bot.register_next_step_handler(file, 'start')

    # TODO need to implement
    def _is_start_bot(self, message) -> None:
        return

    def get_reply_button_text(self) -> str:
        return self.__reply_button_text

    def get_key(self) -> str:
        return self._key


class MusicReceiver(Receiver):
    def send_message(self, message):
        if message.document is not None:
            if Validation.is_valid_wav(message.document):
                self.send_to_recipient_chat_wav(message)
                return self.get_thank_you_message(message)

        if message.audio is not None:
            if Validation.is_valid_mp3(message.audio):
                self.send_to_recipient_chat_mp3(message)
                return self.get_thank_you_message(message)

        validation = self._bot.send_message(message.chat.id, self._file_request_message)
        return self._bot.register_next_step_handler(validation, self.send_message)


class FileReceiver(Receiver):
    def send_message(self, message):
        if message.photo is not None:
            self.send_to_recipient_chat_photo(message)
            return self.get_thank_you_message(message)

        if message.document is not None:
            if Validation.is_valid_pdf(message.document) or Validation.is_valid_svg(message.document):
                self.send_to_recipient_chat_document(message)
                return self.get_thank_you_message(message)

        validation = self._bot.send_message(message.chat.id, self._file_request_message)
        return self._bot.register_next_step_handler(validation, self.send_message)


class DesignReceiver(Receiver):
    def send_message(self, message):
        if message.photo is not None:
            self.send_to_recipient_chat_photo(message)
            return self.get_thank_you_message(message)

        if message.document is not None:
            if Validation.is_valid_pdf(message.document) or Validation.is_valid_svg(
                    message.document) or Validation.is_none_compressed_image(message.document):
                self.send_to_recipient_chat_document(message)
                return self.get_thank_you_message(message)

        validation = self._bot.send_message(message.chat.id, self._file_request_message)
        return self._bot.register_next_step_handler(validation, self.send_message)


class OtherReceiver(Receiver):
    def send_message(self, message):
        if message.photo is not None:
            self.send_to_recipient_chat_photo(message)
            return self.get_thank_you_message(message)

        if message.document is not None:
            if Validation.is_valid_pdf(message.document) or Validation.is_valid_svg(
                    message.document) or Validation.is_none_compressed_image(message.document):
                self.send_to_recipient_chat_document(message)
                return self.get_thank_you_message(message)

        if message.content_type == 'video':
            self.send_to_recipient_chat_video(message)
            return self.get_thank_you_message(message)

        if message.content_type == 'animation' and message.animation.mime_type == 'video/mp4':
            self.send_to_recipient_chat_animation(message)
            return self.get_thank_you_message(message)

        validation = self._bot.send_message(message.chat.id, self._file_request_message)
        return self._bot.register_next_step_handler(validation, self.send_message)


def get_user_link(username: str) -> str:
    return '@' + username
