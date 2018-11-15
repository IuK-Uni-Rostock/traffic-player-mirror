from src.attacks.attack_parameters import (LogPlayerType, MultipleChoiceType,
                                           SliderType, TextfieldType,
                                           TimeSliderType)

from src.generator import Generator
from src.attacks.attack import Attack


class DoSAttack(Attack):
    metadata = {
        "name": "Denial of Service",
        "icon": "mdi-run-fast"
    }

    # noinspection PyUnresolvedReferences,PyTypeChecker
    def __init__(self, database,
                 target_players: LogPlayerType(),
                 workload: SliderType(1, 100),
                 duration: TimeSliderType(1, 60*60*24),  # 1s-24h
                 telegram_types: MultipleChoiceType(('A_GroupValue_Write')),
                 target_addresses: TextfieldType(),
                 seed: TextfieldType(default=314159265359)):
        super().__init__(database, seed, target_players)
        self.__workload = workload
        self.__duration = duration
        self.__telegram_types = telegram_types
        self.__target_addresses = target_addresses

    def prepare(self):
        g = Generator(self._seed)
        telegrams = g.generate(self.__telegram_types, self.__duration, self.__workload / 100)
        if not telegrams is None:
            self._manipulator.telegrams = telegrams
