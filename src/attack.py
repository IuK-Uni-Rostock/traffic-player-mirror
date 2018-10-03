from random import Random
from enum import Enum

from .database import Database
from .manipulator import Manipulator

class AttackType(Enum):
    Replay = 1
    DoS    = 2

class Attack:
    def __init__(self, attack_type, seed=314159265359):
        self.attack_type = attack_type
        self.__rng = Random()
        self.__rng.seed(seed)
        self.__db = Database(config, table)

    def initialize(self, start_time, end_time):
        telegrams = self.__db.get_telegrams(start_time, end_time)
        if not telegrams is None:
            self.__manipulator = Manipulator(telegrams)

    def start(self):
        self.__manipulator.prepare_telegrams()
        # TODO: fill message queue
