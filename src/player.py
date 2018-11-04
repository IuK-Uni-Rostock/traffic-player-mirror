#!/usr/bin/env python3

import argparse
import json
import sys

import pika

from telegram import Telegram

ARGS = argparse.ArgumentParser(description='Sends received messages on the KNX bus',
                               formatter_class=argparse.ArgumentDefaultsHelpFormatter)

ARGS.add_argument('-p', action='store', dest='player_id', type=int, help='player id')

if __name__ == "__main__":
    # print(Telegram.create_cemi_frame(source=0, destination=1, group_address=1, apci_type='A_GroupValue_Write', tpci_type='UDP', apci_data=1, tpci_control_type=None, tpci_sequence=0).hex())
    args = ARGS.parse_args()
    if not args.player_id:
        sys.exit(1)
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1')) # TODO change to parameter
    channel = connection.channel()
    name = 'traffic-player-{0}'.format(args.player_id)
    channel.queue_declare(queue=name)
    channel.basic_consume(telegram_received, queue=name, no_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def telegram_received(ch, method, properties, body):
    t = Telegram(**json.loads(body))
    print(" [x] Received %r" % body)
    print(t.source_addr)
    print(t.destination_addr)
    print(t.pack().hex())
