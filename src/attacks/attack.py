from random import Random

from ..database import Database
from ..manipulator import Manipulator


class Attack:
    metadata = {}

    def __init__(self, database, seed, target_players):
        self._manipulator = Manipulator(seed)
        self._target_players = target_players
        self._db = database

    def prepare(self):
        raise NotImplementedError

    def start(self, progress_callback):
        # self._manipulator.telegrams, self._target_players
        # TODO: fill message queue
        pass

    @classmethod
    def get_attack_info(cls):
        """
        :return: Serializable dict that will be sent to the UI
        """
        info = {**cls.metadata, '__name__': cls.__name__}
        info["parameters"] = []
        for name, type in cls.__init__.__annotations__.items():
            info["parameters"].append({**type.get_parameter_info(), "name": name})
        return info

