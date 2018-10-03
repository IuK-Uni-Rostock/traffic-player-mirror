class Telegram:
    sequence_number = None
    timestamp = None
    source_addr = None
    destination_addr = None
    apci = None
    tpci = None
    priority = None
    repeated = None
    hop_count = None
    apdu = None
    payload_length = None
    cemi = None
    payload_data = None
    is_manipulated = None
    sensor_addr = None

class AckTelegram:
    sequence_number = None
    timestamp = None
    apci = None
    cemi = None
    is_manipulated = None
    sensor_addr = None

class UnknownTelegram:
    sequence_number = None
    timestamp = None
    cemi = None
    is_manipulated = None
    sensor_addr = None
