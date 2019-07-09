from src.attacks.attack_parameters import (LogPlayerType, MultipleChoiceType,
                                           SliderType, TextfieldType,
                                           TimeSliderType, SingleChoiceType)

from src.attacks.attack import Attack
from src.walkgenerator import MotionSensor, WalkGenerator, WalkGeneratorConfig

from networkx import Graph


class WalkingPerson(Attack):
    metadata = {
        "name": "WalkingPerson",
        "icon": "mdi-run-fast"
    }

    def __init__(self, database,
                 target_players: LogPlayerType(),
                 walking_speed: SliderType(0.1, 10),
                 jitter: SliderType(0, 10, default=1),
                 reactivation_time: SliderType(1, 60, default=10),
                 start_time: TextfieldType(default="2018-11-20 09:00:00.000000"),
                 end_time: TextfieldType(default="2018-11-20 09:15:00.000000"),
                 scenario: SingleChoiceType((1, 2)),
                 seed: TextfieldType(default=314159265359)):
        super().__init__(database, seed, target_players)
        self.__walking_speed = walking_speed
        self.__jitter = jitter
        self.__reactivation_time = reactivation_time
        self.__start_time = start_time
        self.__end_time = end_time
        self.__scenario = scenario

    def __execute_scenario(self):
        if self.__scenario == 1:
            sensor1 = MotionSensor('3.2.1', '1/7/1', self.__reactivation_time)
            sensor2 = MotionSensor('3.2.2', '1/7/1', self.__reactivation_time)
            sensor3 = MotionSensor('3.2.3', '1/7/1', self.__reactivation_time)
            sensor4 = MotionSensor('3.2.4', '1/7/1', self.__reactivation_time)
            sensor5 = MotionSensor('3.2.5', '1/7/1', self.__reactivation_time)
            sensor6 = MotionSensor('3.2.6', '1/7/1', self.__reactivation_time)
            sensor7 = MotionSensor('3.2.7', '1/7/1', self.__reactivation_time)

            G = Graph()

            G.add_node(1,  sensor=sensor1)
            G.add_node(3,  sensor=sensor2)
            G.add_node(6,  sensor=sensor3)
            G.add_node(8,  sensor=sensor4)
            G.add_node(10, sensor=sensor5)
            G.add_node(12, sensor=sensor6)
            G.add_node(15, sensor=sensor7)

            # here weight equals distance
            G.add_edge(1,  2,  weight=1)
            G.add_edge(2,  3,  weight=1)
            G.add_edge(3,  4,  weight=1)
            G.add_edge(4,  5,  weight=1)
            G.add_edge(5,  6,  weight=1)
            G.add_edge(6,  7,  weight=1)
            G.add_edge(7,  8,  weight=1)
            G.add_edge(8,  9,  weight=1)
            G.add_edge(9,  10, weight=1)
            G.add_edge(10, 11, weight=1)
            G.add_edge(11, 12, weight=1)
            G.add_edge(10, 13, weight=1)
            G.add_edge(13, 14, weight=1)
            G.add_edge(14, 15, weight=1)
            G.add_edge(15, 16, weight=1)
            G.add_edge(16, 17, weight=1)
            G.add_edge(17, 18, weight=1)
            G.add_edge(18, 3,  weight=1)

            wg = WalkGenerator(G, self._seed)
            motion_telegrams = wg.generate(WalkGeneratorConfig(self.__walking_speed, self.__jitter, 1, 12))
            return motion_telegrams
        elif self.__scenario == 2:
            sensors = [
                MotionSensor("3.5.62", "1/7/1", self.__reactivation_time),
                MotionSensor("3.5.52", "1/7/1", self.__reactivation_time),
                MotionSensor("3.5.53", "1/7/1", self.__reactivation_time),
                MotionSensor("3.5.61", "1/7/1", self.__reactivation_time),
                MotionSensor("3.5.54", "1/7/1", self.__reactivation_time),
                MotionSensor("3.5.55", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.66", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.11", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.4", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.5", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.6", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.7", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.8", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.9", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.10", "1/7/1", self.__reactivation_time),
                MotionSensor("3.5.67", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.56", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.57", "1/7/1", self.__reactivation_time),
                MotionSensor("3.5.58", "1/7/1", self.__reactivation_time),
                MotionSensor("3.5.59", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.12", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.42", "1/7/1", self.__reactivation_time),
                MotionSensor("3.3.22", "1/7/1", self.__reactivation_time),
                MotionSensor("3.3.23", "1/7/1", self.__reactivation_time),
                MotionSensor("3.3.14", "1/7/1", self.__reactivation_time),
                MotionSensor("3.3.15", "1/7/1", self.__reactivation_time),
                MotionSensor("3.3.24", "1/7/1", self.__reactivation_time),
                MotionSensor("3.3.25", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.75", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.74", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.11", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.12", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.73", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.3", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.2", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.1", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.72", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.71", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.59", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.6", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.5", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.19", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.20", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.21", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.22", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.23", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.24", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.25", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.4", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.70", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.67", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.8", "1/7/1", self.__reactivation_time),
                MotionSensor("3.2.7", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.47", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.46", "1/7/1", self.__reactivation_time),
                MotionSensor("3.6.31", "1/7/1", self.__reactivation_time)
            ]

            G = Graph()

            for s in sensors:
                G.add_node(s.source_address, sensor=s)

            G.add_edge("3.5.52", "3.5.53", weight=3.5)
            G.add_edge("3.5.52", "3.5.62", weight=5)
            G.add_edge("3.5.53", "3.5.62", weight=5)
            G.add_edge("3.5.53", "3.5.61", weight=3.5)
            G.add_edge("3.5.61", "3.5.54", weight=3.5)
            G.add_edge("3.5.54", "3.5.55", weight=5)
            G.add_edge("3.5.55", "3.6.66", weight=5.5)
            G.add_edge("3.6.66", "3.6.11", weight=4)
            G.add_edge("3.6.66", "3.6.4", weight=4)
            G.add_edge("3.6.11", "3.6.4", weight=3)
            G.add_edge("3.6.4", "3.6.5", weight=2)
            G.add_edge("3.6.5", "3.6.6", weight=2)
            G.add_edge("3.6.11", "3.6.7", weight=2)
            G.add_edge("3.6.11", "3.6.8", weight=3)
            G.add_edge("3.6.8", "3.6.9", weight=2)
            G.add_edge("3.6.9", "3.6.10", weight=2)
            G.add_edge("3.3.22", "3.6.8", weight=4)
            G.add_edge("3.3.22", "3.6.11", weight=5)
            G.add_edge("3.6.66", "3.5.67", weight=6)
            G.add_edge("3.5.67", "3.5.56", weight=3)
            G.add_edge("3.5.56", "3.5.57", weight=10)
            G.add_edge("3.5.57", "3.5.58", weight=7.5)
            G.add_edge("3.5.58", "3.5.59", weight=4)
            G.add_edge("3.5.58", "3.6.12", weight=5)
            G.add_edge("3.6.12", "3.6.42", weight=3.5)
            G.add_edge("3.6.12", "3.6.31", weight=3.5)
            G.add_edge("3.3.23", "3.3.22", weight=7)
            G.add_edge("3.3.23", "3.3.14", weight=8)
            G.add_edge("3.3.23", "3.3.24", weight=8)
            G.add_edge("3.3.14", "3.3.15", weight=3.5)
            G.add_edge("3.3.14", "3.3.24", weight=5)
            G.add_edge("3.3.24", "3.3.25", weight=10)
            G.add_edge("3.3.25", "3.2.75", weight=3.5)
            G.add_edge("3.2.75", "3.2.74", weight=6)
            G.add_edge("3.2.74", "3.2.11", weight=4)
            G.add_edge("3.2.74", "3.2.73", weight=8)
            G.add_edge("3.2.73", "3.2.11", weight=4)
            G.add_edge("3.2.73", "3.2.3", weight=3)
            G.add_edge("3.2.3", "3.2.12", weight=4)
            G.add_edge("3.2.3", "3.2.2", weight=4)
            G.add_edge("3.2.2", "3.2.1", weight=4)
            G.add_edge("3.2.1", "3.2.72", weight=3.5)
            G.add_edge("3.2.72", "3.2.71", weight=2)
            G.add_edge("3.2.72", "3.2.59", weight=5)
            G.add_edge("3.2.72", "3.2.19", weight=5)
            G.add_edge("3.2.71", "3.2.59", weight=5)
            G.add_edge("3.2.71", "3.2.19", weight=5)
            G.add_edge("3.2.71", "3.2.22", weight=4)
            G.add_edge("3.2.71", "3.2.23", weight=5)
            G.add_edge("3.2.71", "3.2.5", weight=4)
            G.add_edge("3.2.19", "3.2.20", weight=3)
            G.add_edge("3.2.20", "3.2.21", weight=2)
            G.add_edge("3.2.23", "3.2.24", weight=3)
            G.add_edge("3.2.24", "3.2.25", weight=2)
            G.add_edge("3.2.5", "3.2.23", weight=5)
            G.add_edge("3.2.5", "3.2.6", weight=5)
            G.add_edge("3.2.5", "3.2.4", weight=8)
            G.add_edge("3.2.4", "3.2.70", weight=3.5)
            G.add_edge("3.2.70", "3.2.67", weight=4)
            G.add_edge("3.2.67", "3.2.8", weight=5.5)
            G.add_edge("3.2.8", "3.2.7", weight=5.5)
            G.add_edge("3.2.7", "3.6.47", weight=3.5)
            G.add_edge("3.6.47", "3.6.46", weight=5)
            G.add_edge("3.6.46", "3.6.31", weight=6)

            wg = WalkGenerator(G, self._seed)

            persons = []
            persons.append(WalkGeneratorConfig(self.__walking_speed, self.__jitter, "3.2.6", "3.5.62"))
            persons.append(WalkGeneratorConfig(self.__walking_speed, self.__jitter, "3.5.62", "3.2.6"))

            motion_telegrams = wg.generate_multiple(persons)
            return motion_telegrams
        else:
            return None

    def prepare(self):
        motion_telegrams = self.__execute_scenario()
        telegrams = self._db.get_telegrams(self.__start_time, self.__end_time)
        if (not telegrams is None) and (not motion_telegrams is None):
            self._manipulator.telegrams = telegrams
            self._manipulator.merge(motion_telegrams)
