from datetime import timedelta
from random import Random

from .telegram import AckTelegram, Telegram


class Manipulator:
    def __init__(self, seed):
        self._rng = Random()
        self._rng.seed(seed)
        self.telegrams = []

    def adjust_time_between_telegrams(self, multiplier=1):
        """Increases or decreases the time between telegrams.

        For example:
        A multiplier of 2 doubles the time between telegrams.
        A multiplier of 0.5 halves the time between telegrams.
        """
        assert multiplier > 0, "multiplier must be > 0"
        assert len(self.telegrams) > 0, "no telegrams available"

        for idx, telegram in enumerate(self.telegrams):
            if idx > 0 and idx + 1 < len(self.telegrams):
                t_prev = self.telegrams[idx - 1].timestamp
                t_curr = telegram.timestamp
                delta = t_curr - t_prev
                adjustment = timedelta(seconds=multiplier * delta.total_seconds())
                self.telegrams[idx - 1].timestamp = t_prev - adjustment

    def filter_percentage(self, selection_rate):
        """Filters the telegrams based on the selection rate.

        For example:
        A selection_rate of 0.8 will deterministically select 80% of the telegrams and remove the remaining 20%.
        """
        assert selection_rate >= 0 and selection_rate <= 1, "selection_rate must be in range 0 <= x <= 1"
        assert len(self.telegrams) > 0, "no telegrams available"

        self.telegrams[:] = [t for t in self.telegrams if self._rng.random() < selection_rate]

    def filter_type(self, telegram_types):
        """Filters the telegrams based on selected telegram types.

        For example:
        Use telegram type ['A_GroupValue_Write'] to filter by group-value-write telegrams.
        """
        assert len(self.telegrams) > 0, "no telegrams available"
        assert len(telegram_types) > 0, "at least one telegram type must be given"

        self.telegrams[:] = [t for t in self.telegrams if t.apci in telegram_types]
