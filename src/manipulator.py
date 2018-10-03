from .telegram import AckTelegram, Telegram

class Manipulator:
    def __init__(self, telegrams):
        self.__telegrams = telegrams

    def prepare_telegrams(speed_multiplier=1):
        for idx, telegram in enumerate(self.__telegrams):
            t_curr = telegram.timestamp
            t_next = self.telegrams[idx + 1].timestamp
            speed = speed_multiplier * (t_next - t_curr)
            telegram.timestamp = t_curr - speed

        return self.__telegrams
