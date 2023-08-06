""" Модуль дескрипторов """

from weakref import WeakKeyDictionary


class Port:
    """
    Дескриптор для значения атрибута порта.
    В случае, если задаётся значение вне заданного диапазона целых числ,
    выбрасывается исключение.
    """

    def __init__(self, logger):
        self.__logger = logger
        self.__values = WeakKeyDictionary()

    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            self.__logger.critical(
                f'Invalid port value {value}. Allowed range is [1024..65535]')
            raise ValueError(f'Invalid port value: {value}')
        self.__values[instance] = value

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self.__values.get(instance, 0)
