from src.attacks.attack_parameters import (LogPlayerType, MultipleChoiceType,
                                           SliderType, TextfieldType,
                                           TimeSliderType, SingleChoiceType)

from src.generator import Generator
from src.attacks.attack import Attack


class DoSAttack(Attack):
    metadata = {
        "name": "Denial of Service",
        "icon": "mdi-nuke"
    }

    def __init__(self, database,
                 target_players: LogPlayerType(),
                 workload: SliderType(1, 100),
                 duration: SliderType(1, 600), # 1s to 10min
                 telegram_types: MultipleChoiceType(('A_GroupValue_Write')),
                 target: SingleChoiceType(('Random', 'LED Strips')),
                 seed: TextfieldType(default=314159265359)):
        super().__init__(database, seed, target_players)
        self.__workload = workload / 100
        self.__duration = duration
        self.__telegram_types = telegram_types
        self.__target = target

    def prepare(self):
        g = Generator(self._seed)
        telegrams = g.generate(self.__telegram_types, self.__target, self.__duration, self.__workload)
        if not telegrams is None:
            self._manipulator.telegrams = telegrams
