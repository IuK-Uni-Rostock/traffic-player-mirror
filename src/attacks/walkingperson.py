from src.attacks.attack_parameters import (LogPlayerType, MultipleChoiceType,
                                           SliderType, TextfieldType,
                                           TimeSliderType)

from src.attacks.attack import Attack
from src.walkgenerator import MotionSensor, WalkGenerator

from networkx import Graph


class WalkingPerson(Attack):
    metadata = {
        "name": "WalkingPerson",
        "icon": "mdi-vector-polyline"
    }

    def __init__(self, database,
                 target_players: LogPlayerType(),
                 walking_speed: SliderType(0.1, 10),
                 jitter: SliderType(0, 10, default=1),
                 start_time: TextfieldType(default="2018-11-20 09:00:00.000000"),
                 end_time: TextfieldType(default="2018-11-20 09:15:00.000000"),
                 scenario: MultipleChoiceType((1)),
                 seed: TextfieldType(default=314159265359)):
        super().__init__(database, seed, target_players)
        self.__walking_speed = walking_speed
        self.__jitter = jitter
        self.__start_time = start_time
        self.__end_time = end_time
        self.__scenario = scenario

    def __execute_scenario(self):
        if self.__scenario == 1:
            sensor1 = MotionSensor('3.2.1', '1/7/1', 10)
            sensor2 = MotionSensor('3.2.2', '1/7/1', 10)
            sensor3 = MotionSensor('3.2.3', '1/7/1', 10)
            sensor4 = MotionSensor('3.2.4', '1/7/1', 10)
            sensor5 = MotionSensor('3.2.5', '1/7/1', 10)
            sensor6 = MotionSensor('3.2.6', '1/7/1', 10)
            sensor7 = MotionSensor('3.2.7', '1/7/1', 10)

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
            motion_telegrams = wg.generate(self.__walking_speed, self.__jitter, 1, 12)
            return motion_telegrams
        else:
            return None

    def prepare(self):
        motion_telegrams = self.__execute_scenario()
        telegrams = self._db.get_telegrams(self.__start_time, self.__end_time)
        if (not telegrams is None) and (not motion_telegrams is None):
            self._manipulator.telegrams = telegrams
            self._manipulator.merge(motion_telegrams)
