from datetime import datetime
from random import Random

from .telegram import Telegram


class Generator:
    def __init__(self, seed):
        self._rng = Random()
        self._rng.seed(seed)

    def generate(self, types, amount):
        """Generates a random sequence of telegrams using the given telegram types."""
        assert amount > 0, "amount must be > 0"
        assert len(types) > 0, "no types available"

        result = []
        for i in range(1, amount):
            result.append(self.__create_telegram(self._rng.choice(types)))
        return result

    def __create_telegram(self, telegram_type):
        t = Telegram()
        is_group_address = True if "Group" in telegram_type else False
        t.source_addr = "{0}.{1}.{2}".format(self._rng.randint(1, 15), self._rng.randint(1, 15), self._rng.randint(1, 255))
        if is_group_address:
            t.destination_addr = "{0}/{1}/{2}".format(self._rng.randint(1, 31), self._rng.randint(1, 7), self._rng.randint(1, 255)) # 0/0/0 not allowed
        else:
            t.destination_addr = "{0}.{1}.{2}".format(self._rng.randint(1, 15), self._rng.randint(1, 15), self._rng.randint(1, 255))
        t.system_broadcast = 1 # constant
        t.repeat = 1 # constant?
        t.priority = self._rng.randint(0,3)
        t.ack_req = not is_group_address
        t.confirm = not is_group_address
        t.hop_count = self._rng.randint(1, 6)
        if is_group_address:
            t.tpci = "UDP"
            t.tpci_sequence = 0
            t.payload_data = self._rng.randint(0, 10000)
        else:
            t.tpci = "" # TODO
            t.tpci_sequence = 0
            t.payload_data = 0
        t.apci = telegram_type
        t.extended_frame = 0
        t.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        return t
