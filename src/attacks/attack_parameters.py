from typing import Optional


class AttackParameter(object):
    def get_parameter_info(self):
        return {**self.__dict__, '__name__': self.__class__.__name__, **self._extra_info()}

    def _extra_info(self):
        return {}


class LogPlayerType(AttackParameter):
    def _extra_info(self):
        # TODO get at runtime
        return {
            "choices": ["Logplayer-1", "Logplayer-2"]
        }


class SliderType(AttackParameter):
    def __init__(self, min: int, max: int, default: Optional[int] = None):
        if default:
            self.default = default
        else:
            # Set it to 50%
            self.default = min + (max-min)/2
        self.min = min
        self.max = max


class TimeSliderType(SliderType):
    # values are in seconds
    pass