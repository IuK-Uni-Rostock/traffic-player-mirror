from src.attacks.attack_parameters import (LogPlayerType, MultipleChoiceType,
                                           SliderType, TextfieldType,
                                           TimeSliderType)

from src.attacks.attack import Attack


class ReplayAttack(Attack):
    metadata = {
        "name": "Replay",
        "icon": "mdi-rewind"
    }

    def __init__(self, database,
                 target_players: LogPlayerType(),
                 replay_speed: SliderType(0.1, 10),
                 start_time: TextfieldType(default="2018-11-20 09:00:00.000000"),
                 end_time: TextfieldType(default="2018-11-20 09:15:00.000000"),
                 selection_rate: SliderType(0, 100),
                 seed: TextfieldType(default=314159265359)):
        super().__init__(database, seed, target_players)
        self.__replay_speed = replay_speed
        self.__start_time = start_time
        self.__end_time = end_time
        self.__selection_rate = selection_rate / 100

    def prepare(self):
        telegrams = self._db.get_telegrams(self.__start_time, self.__end_time)
        if not telegrams is None:
            self._manipulator.telegrams = telegrams
            self._manipulator.adjust_time_between_telegrams(self.__replay_speed)
            self._manipulator.filter_percentage(self.__selection_rate)
