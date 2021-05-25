class TelegramValidation:
    @staticmethod
    def is_valid_pdf(document: []) -> bool:
        if document.mime_type is not None:
            return document.mime_type == 'application/pdf'
        else:
            return False

    @staticmethod
    def is_valid_svg(document: []) -> bool:
        if document.mime_type is not None:
            return document.mime_type == 'image/svg+xml'
        else:
            return False

    @staticmethod
    def is_valid_wav(file_array: []) -> bool:
        if file_array.mime_type is not None:
            return file_array.mime_type == 'audio/x-wav'
        else:
            return False

    @staticmethod
    def is_valid_mp3(audio_array: []) -> bool:
        if audio_array.mime_type is not None:
            return audio_array.mime_type == 'audio/mpeg'
        else:
            return False
