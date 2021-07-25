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
    def is_valid_video_file(document: []) -> bool:
        if document.mime_type is not None:
            return document.mime_type == 'video/mp4'
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

    @staticmethod
    def is_none_compressed_file(document: []) -> bool:
        if document.mime_type is not None:
            for image_type in TelegramValidation.allowed_images_type():
                if document.mime_type == image_type:
                    return True

            for video_type in TelegramValidation.allowed_videos_type():
                if document.mime_type == video_type:
                    return True

        return False

    @staticmethod
    def allowed_images_type() -> []:
        return ['image/jpeg', 'image/png', 'image/jpg', 'application/binary']

    @staticmethod
    def allowed_videos_type() -> []:
        return ['video/quicktime']
