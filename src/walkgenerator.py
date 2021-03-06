from random import Random

from networkx.algorithms.shortest_paths import weighted

from src.telegram import Telegram


class MotionSensor:
    def __init__(self, source_address, destination_address, reactivation_time):
        """Initialize a new motion sensor with given source address, destination address
        and reactivation time in seconds. Motion can be simulated by calling the `activate`
        method.
        """
        self.source_address = source_address
        self.destination_address = destination_address
        self.reactivation_time = reactivation_time
        self.last_activation_time = -999999

    def activate(self, current_time):
        """Simulates detected motion and emits a new sensor event if the elapsed time since
        the last emitted sensor event is greater than the reactivation time to avoid spamming
        of unnecessary sensor events.
        """
        if current_time - self.last_activation_time >= self.reactivation_time:
            #print('{0} activated at time {1}'.format(self.__str__(), current_time))
            self.last_activation_time = current_time
            return self.__create_telegram(current_time, 1, self.source_address, self.destination_address)
        return None

    def __create_telegram(self, timestamp, payload_data, sourceaddr, destaddr):
        t = Telegram()
        is_group_address = True
        t.source_addr = sourceaddr
        t.destination_addr = destaddr
        t.system_broadcast = 1
        t.repeat = 1
        t.priority = 1
        t.ack_req = not is_group_address
        t.confirm = not is_group_address
        t.hop_count = 6
        t.tpci = "UDP"
        t.tpci_sequence = 0
        t.payload_data = payload_data
        t.apci = 'A_GroupValue_Write'
        t.extended_frame = 0
        t.timestamp = timestamp
        return t

    def __str__(self):
        return '[{0} -> {1} ; {2}]'.format(self.source_address, self.destination_address, self.reactivation_time)

class WalkGeneratorConfig:
    def __init__(self, walking_speed, jitter, start, destination, custom_path=None):
        self.walking_speed = walking_speed
        self.jitter = jitter
        self.start = start
        self.destination = destination
        self.custom_path = custom_path

class WalkGenerator:
    def __init__(self, model, seed):
        self._rng = Random()
        self._rng.seed(seed)
        self.G = model
        self.__telegram_sequence = []

    def generate_multiple(self, configs):
        """Generates a single sensor event time series for a given list of `WalkGeneratorConfig`s.
        """
        sensors = []
        for _, node in self.G.nodes(data=True):
            if 'sensor' in node:
                sensors.append(node['sensor'])

        walks = []
        for config in configs:
            walks.append(self.generate(config))

        telegrams = [walk for walk in walks][0]
        telegrams.sort(key=lambda t: t.timestamp)

        to_remove = []
        for idx, telegram in enumerate(telegrams):
            sensor = next((s for s in sensors if s.source_address == telegram.source_addr and s.destination_address == telegram.destination_addr), None)
            for tdx, t in enumerate(telegrams):
                if tdx > idx and t.timestamp <= telegram.timestamp + sensor.reactivation_time and t.source_addr == telegram.source_addr and t.destination_addr == telegram.destination_addr:
                    to_remove.append(tdx)

        for index in sorted(set(to_remove), reverse=True):
            del telegrams[index]

        return telegrams

    def generate(self, config):
        """Generates a single sensor event time series for a given `WalkGeneratorConfig`.
        """
        # path = [1,2,3,4,5,6,7,8,9,10,13,14,15,16,17,18,3,4,5,6,7,8,9,10,13,14,15,16,17,18,3,2,1]
        self.__reset()
        if config.custom_path is None:
            path = weighted.dijkstra_path(self.G, config.start, config.destination)
        else:
            path = config.custom_path

        time = 0

        last_node = path[0]
        for node in path[1:]:
            self.__move(node, time)
            distance = self.G.edges[last_node, node]['weight']
            jit = self._rng.uniform(config.jitter * -1, config.jitter)
            time += distance / (config.walking_speed + jit)
            last_node = node
        return self.__telegram_sequence

    def __reset(self):
        for _, node in self.G.nodes(data=True):
            if 'sensor' in node:
                node['sensor'].last_activation_time = -999999

    def __move(self, node, time):
        #print('Moving to node {0}'.format(node))
        node = self.G.node[node]
        if 'sensor' in node:
            result = node['sensor'].activate(time)
            if result is not None:
                self.__telegram_sequence.append(result)
