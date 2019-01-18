from src.attacks.attack_parameters import (LogPlayerType, MultipleChoiceType,
                                           SliderType, TextfieldType,
                                           TimeSliderType)

from src.walkgenerator import Walkgenerator
from src.attacks.attack import Attack


class WalkingPerson(Attack):
    metadata = {
        "name": "WalkingPerson",
        "icon": "mdi-vector-polyline"
    }

    def __init__(self, database,
                 target_players: LogPlayerType(),
                 running_speed: SliderType(0.1, 10),
                 jitter_in_running_speed: SliderType(0, 10, default=1),
                 start_time: TextfieldType(default="2018-11-20 09:00:00.000000"),
                 persons_per_hour: SliderType(0, 1000),
                 seed: TextfieldType(default=314159265359)):
        super().__init__(database, seed, target_players)
        self.__running_speed = running_speed
        self.__start_time = start_time
        self.__persons_per_hour = persons_per_hour
        self.__jitter_in_running_speed = jitter_in_running_speed


    def prepare(self):
        g = Walkgenerator(self._seed)
        telegrams = self._db.get_telegrams(self.__start_time, self.__end_time)
        newtelegrams = g.generate(self.__telegram_types, self.__model, self.__path, self.__running_speed, self.__start_time, self.__jitter_in_running_speed)
        if (not telegrams is None) and (not newtelegrams is None):
            self._manipulator.telegrams = telegrams
            self._manipulator.mergenewtelegrams(newtelegrams)
