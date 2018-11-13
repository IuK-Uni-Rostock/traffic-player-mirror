import struct

import knxmap.utils
from knxmap.data.constants import (CEMI_APCI_TYPES, CEMI_TPCI_TYPES,
                                   TPCI_NUMBERED_CONTROL_DATA_TYPES,
                                   TPCI_UNNUMBERED_CONTROL_DATA_TYPES)
from knxmap.messages.apci import Apci
from knxmap.messages.cemi import CemiFrame
from knxmap.messages.tp import ExtendedDataRequest
from knxmap.messages.tpci import Tpci


class Telegram:
    sequence_number = None
    timestamp = None
    source_addr = None
    destination_addr = None
    extended_frame = None
    priority = None
    repeat = None
    ack_req = None
    confirm = None
    system_broadcast = None
    hop_count = None
    tpci = None
    tpci_sequence = None
    apci = None
    payload_data = None
    payload_length = None
    is_manipulated = None
    attack_type_id = None
    sensor_addr = None

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def pack(self):
        if '/' in self.destination_addr:
            group_address = True
        else:
            group_address = False

        return self.create_cemi_frame(
            source=knxmap.utils.pack_knx_address(self.source_addr),
            destination=knxmap.utils.pack_knx_group_address(self.destination_addr) if group_address else knxmap.utils.pack_knx_address(self.destination_addr),
            group_address=group_address,
            apci_type=self.apci,
            apci_data=self.payload_data,
            tpci_type=self.tpci,
            tpci_sequence=self.tpci_sequence,
            hop_count=self.hop_count,
            confirm=self.confirm,
            ack_req=self.ack_req,
            priority=self.priority,
            system_broadcast=self.system_broadcast,
            repeat=self.repeat,
            extended_frame=self.extended_frame
        )

    @staticmethod
    def create_cemi_frame(source, destination, group_address, apci_type, apci_data, tpci_type, tpci_control_type=None, tpci_sequence=0, hop_count=6, confirm=False, ack_req=False, priority=0x03, system_broadcast=True, repeat=True, extended_frame=False, data=None):
        data_request = bytearray(struct.pack('!B', ExtendedDataRequest.pack_control_field(
            confirm=confirm,
            acknowledge_req=ack_req,
            priority=priority,
            system_broadcast=system_broadcast,
            repeat_flag=repeat,
            frame_type=not extended_frame)))
        data_request.extend(struct.pack('!B', ExtendedDataRequest.pack_extended_control_field(
            hop_count=hop_count,
            address_type=group_address,
            ext_frame_format=extended_frame)))
        data_request.extend(struct.pack('!H', source))
        data_request.extend(struct.pack('!H', destination))
        data_len = 0
        if data:
            data_len = len(data)
        if apci_type:
            data_len += 1
        data_request.extend(struct.pack('!B', data_len))
        if tpci_type:
            tpci = Tpci(tpci_type=tpci_type,
                        tpci_sequence=tpci_sequence)
            tpci = tpci.pack()
            if tpci_type == 'UCD':
                tpci |= TPCI_UNNUMBERED_CONTROL_DATA_TYPES.get(tpci_control_type) << 0
            elif tpci_type == 'NCD':
                tpci |= TPCI_NUMBERED_CONTROL_DATA_TYPES.get(tpci_control_type) << 0
        if apci_type:
            apci = Apci(apci_type=apci_type,
                        apci_data=apci_data)
            apci = apci.pack()
            apci |= ((tpci >> 2) & 1) << 10
            apci |= ((tpci >> 3) & 1) << 11
            apci |= ((tpci >> 4) & 1) << 12
            apci |= ((tpci >> 5) & 1) << 13
            apci |= ((tpci >> 6) & 1) << 14
            apci |= ((tpci >> 7) & 1) << 15
            data_request.extend(struct.pack('!H', apci))
        else:
            data_request.extend(struct.pack('<H', tpci))
        if data:
            data_request.extend(data)
        cemi = CemiFrame()
        cemi = cemi.pack()
        cemi.extend(data_request)
        return cemi

    def __repr__(self):
        return """Telegram(src={source_addr}, dest={destination_addr}, extended_frame={extended_frame}, priority={priority},
         repeat={repeat}, ack_req={ack_req}, confirm={confirm}, system_broadcast={system_broadcast}, hop_count={hop_count},
         tpci={tpci}, tpci_sequence={tpci_sequence}, apci={apci}, payload_data={payload_data}, payload_length={payload_length},
         timestamp={timestamp}, is_manipulated={is_manipulated}, sensor_addr={sensor_addr})""".format(**self.__dict__)

class AckTelegram:
    sequence_number = None
    timestamp = None
    apci = None
    is_manipulated = None
    attack_type_id = None
    sensor_addr = None

class UnknownTelegram:
    sequence_number = None
    timestamp = None
    cemi = None
    sensor_addr = None
