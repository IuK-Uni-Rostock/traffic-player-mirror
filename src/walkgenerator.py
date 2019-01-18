from random import Random

from src.telegram import Telegram


class Walkgenerator:
    def __init__(self, seed):
        self._rng = Random()
        self._rng.seed(seed)

    def generate(self, model, path, running_speed, start_time, jitter):
        result = []
# TODO
        return result

    def __create_telegram(self, telegram_type, timestamp, sourceaddr, destaddr):
        t = Telegram()
        is_group_address = True
        t.source_addr = sourceaddr
        t.destination_addr = destaddr
        t.system_broadcast = 1 # constant
        t.repeat = 1 # constant?
        t.priority = 1
        t.ack_req = not is_group_address
        t.confirm = not is_group_address
        t.hop_count = 6
        t.tpci = "UDP"
        t.tpci_sequence = 0
        t.payload_data = self._rng.randint(0, 10000)
        t.apci = telegram_type
        t.extended_frame = 0
        t.timestamp = timestamp
        return t
