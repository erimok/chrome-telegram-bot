from abc import abstractmethod

import telebot
from Config import Config


class Receiver:
    __chat_id: int

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
        self._key = key
        self._bot = bot

    def ask_file(self, chat_id: int):
        message = self._bot.send_message(chat_id, self._file_request_message)
        self.__chat_id = chat_id
        self._bot.register_next_step_handler(message, self.send_message)

    # TODO need to implement
    def _is_start_bot(self) -> None:
        return

    def get_reply_button_text(self) -> str:
        return self.__reply_button_text

    def get_key(self) -> str:
        return self._key


class MusicReceiver(Receiver):
    __file_type: str

    def send_message(self, message):
        if message.document is not None:
            if self.is_valid_wav(self, message.document):
                self.__file_type = 'wav'
                self._bot.send_message(message.chat.id, self._success_message)
                return self.send_to_recipient_chat(message)
            else:
                validation = self._bot.send_message(message.chat.id, self._file_request_message)
                return self._bot.register_next_step_handler(validation, self.send_message)

        if message.audio is not None:
            if self.is_valid_mp3(self, message.audio):
                self.__file_type = 'mp3'
                self._bot.send_message(message.chat.id, self._success_message)
                return self.send_to_recipient_chat(message)
            else:
                validation = self._bot.send_message(message.chat.id, self._file_request_message)
                return self._bot.register_next_step_handler(validation, self.send_message)

        validation = self._bot.send_message(message.chat.id, self._file_request_message)
        return self._bot.register_next_step_handler(validation, self.send_message)

    @staticmethod
    def is_valid_wav(self, file_array: []) -> bool:
        if file_array.mime_type is not None:
            return file_array.mime_type == 'audio/x-wav'
        else:
            return False

    @staticmethod
    def is_valid_mp3(self, audio_array: []) -> bool:
        if audio_array.mime_type is not None:
            return audio_array.mime_type == 'audio/mpeg'
        else:
            return False

    def send_to_recipient_chat(self, message):
        if self.__file_type == 'vaw':
            self.send_to_recipient_chat_wav(message)
        if self.__file_type == 'mp3':
            self.send_to_recipient_chat_mp3(message)

    def send_to_recipient_chat_wav(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_document(self._recipient_group_id, message.document.file_id)
            # TODO add contact person
        except Exception as ex:
            audio_file = self._bot.send_message(message.chat.id, '[!] error - '
                                                                 '{}'.format(str(ex)) + '. Попробуйте еще раз')
            self._bot.register_next_step_handler(audio_file, '/start')

    def send_to_recipient_chat_mp3(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_document(self._recipient_group_id, message.audio.file_id)
            # TODO add contact person
        except Exception as ex:
            audio_file = self._bot.send_message(message.chat.id, '[!] error - '
                                                                 '{}'.format(str(ex)) + '. Попробуйте еще раз')
            self._bot.register_next_step_handler(audio_file, '/start')


class FileReceiver(Receiver):
    __file_type: str

    def send_message(self, message):
        if message.photo is not None:
            self.__file_type = 'photo'
            return self.send_to_recipient_chat(message)

        if message.document is not None:
            if self.is_valid_pdf(message.document) or self.is_valid_svg(message.document):
                self.__file_type = 'document'
                return self.send_to_recipient_chat(message)

        validation = self._bot.send_message(message.chat.id, self._file_request_message)
        return self._bot.register_next_step_handler(validation, self.send_message)

    def send_to_recipient_chat(self, message):
        if self.__file_type == 'document':
            self.send_to_recipient_chat_document(message)
        if self.__file_type == 'photo':
            self.send_to_recipient_chat_photo(message)

    # TODO move to abstract
    def send_to_recipient_chat_document(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_document(self._recipient_group_id, message.document.file_id)
            # TODO add contact person
        except Exception as ex:
            file = self._bot.send_message(message.chat.id, '[!] error - '
                                                           '{}'.format(str(ex)) + '. Попробуйте еще раз')
            self._bot.register_next_step_handler(file, '/start')

    def send_to_recipient_chat_photo(self, message):
        try:
            self._bot.send_message(self._recipient_group_id, self._message_to_admin_chat)
            self._bot.send_photo(self._recipient_group_id, message.photo)
            # TODO add contact person
        except Exception as ex:
            file = self._bot.send_message(message.chat.id, '[!] error - '
                                                           '{}'.format(str(ex)) + '. Попробуйте еще раз')
            self._bot.register_next_step_handler(file, '/start')

    @staticmethod
    def is_valid_pdf(self, document: []) -> bool:
        if document.mime_type is not None:
            return document.mime_type == 'application/pdf'
        else:
            return False

    @staticmethod
    def is_valid_svg(self, document: []) -> bool:
        if document.mime_type is not None:
            return document.mime_type == 'image/svg+xml'
        else:
            return False
