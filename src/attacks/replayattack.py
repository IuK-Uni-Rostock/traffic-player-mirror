from .attack import Attack


class ReplayAttack(Attack):
    def __init__(self, database, target_players, replay_speed, start_time, end_time, selection_rate, seed=314159265359):
        super().__init__(database, seed, target_players)
        self.__replay_speed = replay_speed
        self.__start_time = start_time
        self.__end_time = end_time
        self.__selection_rate = selection_rate

    def prepare(self):
        telegrams = self._db.get_telegrams(self.__start_time, self.__end_time)
        if not telegrams is None:
            self._manipulator.telegrams = telegrams
            self._manipulator.adjust_time_between_telegrams(self.__replay_speed)
            self._manipulator.filter_percentage(self.__selection_rate)
