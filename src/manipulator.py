from .telegram import AckTelegram, Telegram

class Manipulator:
    def __init__(self, seed):
        self._rng = Random()
        self._rng.seed(seed)
        self.telegrams = None

    def adjust_time_between_telegrams(multiplier=1):
        """Increases or decreases the time between telegrams.

        For example:
        A multiplier of 2 doubles the time between telegrams.
        A multiplier of 0.5 halves the time between telegrams.
        """
        assert multiplier > 0, "multiplier must be > 0"
        assert self.telegrams is not None, "telegrams must be initialized"

        for idx, telegram in enumerate(self.telegrams):
            t_curr = telegram.timestamp
            if idx + 1 < len(self.telegrams):
                t_next = self.telegrams[idx + 1].timestamp
                adjustment = multiplier * (t_next - t_curr)
                telegram.timestamp = t_curr - adjustment


    def filter_percentage(selection_rate):
        """Filters the telegrams based on the selection rate.

        For example:
        A selection_rate of 0.8 will deterministically select 80% of the telegrams and remove the remaining 20%.
        """
        assert selection_rate >= 0 and selection_rate <= 1, "selection_rate must be in range 0 <= x <= 1"
        assert self.telegrams is not None, "telegrams must be initialized"

        self.telegrams[:] = [t for t in self.telegrams if self._rng.random() < selection_rate]
