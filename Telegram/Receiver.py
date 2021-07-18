from abc import abstractmethod

import telebot
from Config import Config
from Telegram.Validation import TelegramValidation as Validation


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
        self._bot.clear_step_handler_by_chat_id(chat_id)
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

    def get_reply_button_text(self) -> str:
        return self.__reply_button_text

    def get_key(self) -> str:
        return self._key

    def forward_message(self, message) -> None:
        self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
        self._bot.forward_message(self._recipient_group_id, message.chat.id, message.message_id)
        self._bot.send_message(self._recipient_group_id,
                               self._sender_message + ' ' + get_user_link(message.from_user.username))
        self.get_thank_you_message(message)

    def send_media_group_warning(self, message) -> None:
        self._bot.send_message(message.chat.id, '⚠️⚠️⚠️ Отправляйте файлы по одному!️')


class MusicReceiver(Receiver):
    def send_message(self, message):
        if message.document is not None:
            if Validation.is_valid_wav(message.document):
                if message.media_group_id is not None:
                    self.forward_message(message)
                    return self.send_media_group_warning(message)
                else:
                    return self.forward_message(message)

        if message.audio is not None:
            if Validation.is_valid_mp3(message.audio):
                if message.media_group_id is not None:
                    self.forward_message(message)
                    return self.send_media_group_warning(message)
                else:
                    return self.forward_message(message)

        validation = self._bot.send_message(message.chat.id, self._validation_message)
        return self._bot.register_next_step_handler(validation, self.send_message)


class FileReceiver(Receiver):
    def send_message(self, message):
        if message.photo is not None:
            if message.media_group_id is not None:
                self.forward_message(message)
                return self.send_media_group_warning(message)
            else:
                return self.forward_message(message)

        if message.document is not None:
            if Validation.is_valid_pdf(message.document) or Validation.is_valid_svg(message.document):
                if message.media_group_id is not None:
                    self.forward_message(message)
                    return self.send_media_group_warning(message)
                else:
                    return self.forward_message(message)

        validation = self._bot.send_message(message.chat.id, self._validation_message)
        return self._bot.register_next_step_handler(validation, self.send_message)


class DesignReceiver(Receiver):
    def send_message(self, message):
        if message.photo is not None:
            if message.media_group_id is not None:
                self.forward_message(message)
                return self.send_media_group_warning(message)
            else:
                return self.forward_message(message)

        if message.document is not None:
            if Validation.is_valid_pdf(message.document) or Validation.is_valid_svg(
                    message.document) or Validation.is_none_compressed_image(message.document):
                if message.media_group_id is not None:
                    self.forward_message(message)
                    return self.send_media_group_warning(message)
                else:
                    return self.forward_message(message)

        validation = self._bot.send_message(message.chat.id, self._validation_message)
        return self._bot.register_next_step_handler(validation, self.send_message)


class OtherReceiver(Receiver):
    def send_message(self, message):
        print(message.text)
        if message.text == '/start':
            # TODO restart bot
            return

        if message.photo is not None:
            if message.media_group_id is not None:
                self.forward_message(message)
                return self.send_media_group_warning(message)
            else:
                return self.forward_message(message)

        if message.document is not None:
            if Validation.is_valid_pdf(message.document) or Validation.is_valid_svg(
                    message.document) or Validation.is_none_compressed_image(
                message.document) or Validation.is_valid_video_file(message.document):
                if message.media_group_id is not None:
                    self.forward_message(message)
                    return self.send_media_group_warning(message)
                else:
                    return self.forward_message(message)

        if message.content_type == 'video':
            if message.media_group_id is not None:
                self.forward_message(message)
                return self.send_media_group_warning(message)
            else:
                return self.forward_message(message)

        if message.content_type == 'animation' and message.animation.mime_type == 'video/mp4':
            if message.media_group_id is not None:
                self.forward_message(message)
                return self.send_media_group_warning(message)
            else:
                return self.forward_message(message)

        validation = self._bot.send_message(message.chat.id, self._validation_message)
        return self._bot.register_next_step_handler(validation, self.send_message)


def get_user_link(username: str) -> str:
    return '@' + username
