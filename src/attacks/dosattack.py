from .attack import Attack


class DoSAttack(Attack):
    metadata = {
        "name": "Denial of Service",
        "icon": "mdi-run-fast"
    }

    def __init__(self, database, target_players, workload, duration, telegram_types, target_addresses,
                 seed=314159265359):
        super().__init__(database, seed, target_players)
        self.__workload = workload
        self.__duration = duration
        self.__telegram_types = telegram_types
        self.__target_addresses = target_addresses

    def prepare(self):
        pass
