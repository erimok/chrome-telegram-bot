import configparser


class Config:
    __path_to_config_file = 'config.ini'

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read(self.__path_to_config_file)

        self.__config = config
        self.__token = config['Telegram']['token']

    def get_token(self) -> str:
        return self.__token

    def get_config(self) -> configparser.ConfigParser:
        return self.__config
