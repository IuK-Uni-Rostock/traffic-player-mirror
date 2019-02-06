#!/usr/bin/env python3

import argparse
from datetime import datetime
import json
from ctypes import CDLL, CFUNCTYPE, POINTER, c_int, c_void_p, c_uint, c_ubyte, pointer, create_string_buffer

import pika

from src.telegram import Telegram

ARGS = argparse.ArgumentParser(description="Sends received messages on the KNX bus. If the argument 'device' is missing, the debug mode will be used which means no telegrams will be sent to the KNX bus, they will only be output to stdout.",
                               formatter_class=argparse.ArgumentDefaultsHelpFormatter)

ARGS.add_argument('-p', '--player', action='store', dest='player_id', type=int, help='player id', required=True)
ARGS.add_argument('-q', '--queue', action='store', dest='queue_ip', type=str, help='queue ip', required=True)
ARGS.add_argument('-d', '--device', action='store', dest='device_index', type=int, help='device index (usually 0)', required=False)

kdrive = CDLL('/usr/local/lib/libkdriveExpress.so')

DEBUG = False

# the error callback pointer to function type
ERROR_CALLBACK = CFUNCTYPE(None, c_int, c_void_p)

# the event callback pointer to function type
EVENT_CALLBACK = CFUNCTYPE(None, c_int, c_uint, c_void_p)

# acccess port descriptor
ap = None


def telegram_received(channel, method, properties, body):
    t = Telegram(**json.loads(body.decode('ascii')))
    cemi = bytes(t.pack())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print("{0} {1}".format(timestamp, cemi.hex()))
    # cemi= b'\x11\x00\xBC\xE0\x35\x25\x12\x04\x01\x00\x81'
    if not DEBUG:
        kdrive.kdrive_ap_send(ap, cemi, len(cemi))


def main():
    global ap, DEBUG
    args = ARGS.parse_args()
    print("Starting traffic-player using player id {0}".format(args.player_id))

    DEBUG = args.device_index is None
    if not DEBUG:
        print("Starting live mode...")
        start_live_mode(args)
    else:
        print("No device index given, starting debug mode...")
        start_debug_mode(args)


def start_live_mode(args):
    global ap
    # Configure the logging level
    kdrive.kdrive_logger_set_level(0)

    # We register an error callback as a convenience logger function to
    # print out the error message when an error occurs.
    error_callback = ERROR_CALLBACK(on_error_callback)
    kdrive.kdrive_register_error_callback(error_callback, None)

    # We create a Access Port descriptor. This descriptor is then used for
    # all calls to that specific access port.
    ap = kdrive.kdrive_ap_create()

    # We check that we were able to allocate a new descriptor
    # This should always happen, unless a bad_alloc exception is internally thrown
    # which means the memory couldn't be allocated.
    if ap == -1:
        print('Unable to create access port')
        return

    # We register an event callback to notify of the Access Port Events
    # For example: KDRIVE_EVENT_TERMINATED
    event_callback = EVENT_CALLBACK(on_event_callback)
    kdrive.kdrive_set_event_callback(ap, event_callback, None)

    iface_count = kdrive.kdrive_ap_enum_usb(ap)
    print('Found {0} KNX USB Interfaces'.format(iface_count))

    if ((iface_count > 0) and (kdrive.kdrive_ap_open_usb(ap, args.device_index) == 0)):
        print("Using device with index {0}".format(args.device_index))
        # Connect the Packet Trace logging mechanism
        # to see the Rx and Tx packets
        # kdrive.kdrive_ap_packet_trace_connect(ap)

        connection = pika.BlockingConnection(pika.ConnectionParameters(args.queue_ip))
        channel = connection.channel()
        name = 'traffic-player-{0}'.format(args.player_id)
        channel.queue_declare(queue=name)
        channel.basic_consume(telegram_received, queue=name, no_ack=True)
        print('Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

        # close the access port
        kdrive.kdrive_ap_close(ap)
    else:
        print('No KNX USB Interfaces found, exiting...')

    # releases the access port
    kdrive.kdrive_ap_release(ap)


def start_debug_mode(args):
    connection = pika.BlockingConnection(pika.ConnectionParameters(args.queue_ip))
    channel = connection.channel()
    name = 'traffic-player-{0}'.format(args.player_id)
    channel.queue_declare(queue=name)
    channel.basic_consume(telegram_received, queue=name, no_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def on_error_callback(e, user_data):
    len = 1024
    str = create_string_buffer(len)
    kdrive.kdrive_get_error_message(e, str, len)
    print('kdrive error {0} {1}'.format(hex(e), str.value))


def on_event_callback(ap, e, user_data):
    pass


if __name__ == '__main__':
    main()
