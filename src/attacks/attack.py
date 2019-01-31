import pika
import json
import time

from src.database import Database
from src.manipulator import Manipulator


class Attack:
    metadata = {}

    def __init__(self, database, seed, target_players):
        self._seed = seed
        self._manipulator = Manipulator(seed)
        self._target_players = target_players
        self._db = database

    def prepare(self):
        """Subclasses must define this method."""
        raise NotImplementedError

    def start(self, progress_callback):
        # TODO: use new thread or async io
        assert len(self._target_players) > 0, "No target players available"
        assert len(self._manipulator.telegrams) > 0, "No telegrams available"

        all_telegrams = len(self._manipulator.telegrams)
        sent_telegrams = 0
        connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1')) # TODO change to parameter

        player_queues = []
        for player in self._target_players):
            channel = connection.channel()
            name = 'traffic-player-{0}'.format(player)
            channel.queue_declare(queue=name)
            player_queues.append((name, channel))

        last_telegram_timestamp = self._manipulator.telegrams[0]
        for idx, telegram in enumerate(self._manipulator.telegrams):
            # split telegrams equally between all target players
            queue_id = idx % len(self._target_players)
            timespan = telegram.timestamp - last_telegram_timestamp
            if timespan.total_seconds() > 0:
                time.sleep(timespan.total_seconds())
            player_queues[queue_id][1].basic_publish(exchange='', routing_key=player_queues[queue_id][0], body=json.dumps(t.__dict__, default=str))
            sent_telegrams += 1
            last_telegram_timestamp = telegram.timestamp
            # FIXME: report progress
            # progress_callback((sent_telegrams / all_telegrams) * 100)

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
