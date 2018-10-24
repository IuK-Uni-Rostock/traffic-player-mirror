from src.attacks.attack_parameters import SliderType, LogPlayerType, TimeSliderType, MultipleChoiceType, TextfieldType
from .attack import Attack


class DoSAttack(Attack):
    metadata = {
        "name": "Denial of Service",
        "icon": "mdi-run-fast"
    }

    # noinspection PyUnresolvedReferences,PyTypeChecker
    def __init__(self, database,
                 target_players: LogPlayerType(),
                 workload: SliderType(0, 100),
                 duration: TimeSliderType(1, 60*60*24),  # 1s-24h
                 telegram_types: MultipleChoiceType(('Reset', 'Join')),
                 target_addresses: TextfieldType(),
                 seed=314159265359):
        super().__init__(database, seed, target_players)
        self.__workload = workload
        self.__duration = duration
        self.__telegram_types = telegram_types
        self.__target_addresses = target_addresses

    def prepare(self):
        pass
