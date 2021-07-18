# Deprecated
class BotState:
    __is_active: bool

    def __init__(self):
        self.__is_active = False

    def is_active(self) -> bool:
        return self.__is_active

    def set_activity(self, is_active: bool) -> None:
        self.__is_active = is_active
