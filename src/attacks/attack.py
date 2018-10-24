import pika
import json

from ..database import Database
from ..manipulator import Manipulator


class Attack:
    metadata = {}

    def __init__(self, database, seed, target_players):
        self._manipulator = Manipulator(seed)
        self._target_players = target_players
        self._db = database

    def prepare(self):
        """Subclasses must define this method."""
        raise NotImplementedError

    def start(self, progress_callback):
        assert len(self._target_players) > 0, "No target players available"
        assert len(self._manipulator.telegrams) > 0, "No telegrams available"

        connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1')) # TODO change to parameter
        for idx, player in enumerate(self._target_players):
            channel = connection.channel()
            name = 'traffic-player-{0}'.format(player)
            channel.queue_declare(queue=name)

            # split telegrams equally between all target players
            for t in self._manipulator.telegrams[idx:][::len(self._target_players)]:
                channel.basic_publish(exchange='', routing_key=name, body=json.dumps(t.__dic__))

        connection.close()

    @classmethod
    def get_attack_info(cls):
        """
        :return: Serializable dict that will be sent to the UI
        """
        info = {**cls.metadata, '__name__': cls.__name__}
        info["parameters"] = []
        for name, type in cls.__init__.__annotations__.items():
            info["parameters"].append({**type.get_parameter_info(), "name": name})
        return info

