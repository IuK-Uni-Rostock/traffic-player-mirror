import mysql.connector

from .conversation import APCI_TYPES, PRIORITIES, TPCI_TYPES
from .telegram import AckTelegram, Telegram


class Database:
    def __init__(self, db_config, log_table):
        self.__log_table = log_table
        self.__con = mysql.connector.connect(**db_config)

    def close(self):
        self.__con.commit()
        self.__con.close()

    def get_telegrams(self, start_time, end_time):
        # time format: datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if self.__con.is_connected is False:
            return None

        cursor = self.__con.cursor()
        cursor.execute("SELECT sequence_number, timestamp, source_addr, destination_addr, extended_frame, priority, `repeat`, ack_req, " \
                       "confirm, system_broadcast, hop_count, tpci, tpci_sequence, apci, payload_data, payload_length, is_manipulated, " \
                       "attack_type_id, sensor_addr) " \
                       "FROM {0} WHERE timestamp >= {1} AND timestamp <= {2}".format(self.__log_table, start_time, end_time))
        rows = cursor.fetchall()

        telegrams = []
        for row in rows:
            if row[2] is None and row[3] is None: # check for ack telegram
                continue # ignore for now
                t = AckTelegram()
                t.sequence_number = row[0]
                t.timestamp = row[1]
                t.apci = row[13]
                t.is_manipulated = row[16]
                t.attack_type_id = row[17]
                t.sensor_addr = row[18]
                telegrams.append(t)
            else:
                t = Telegram()
                t.sequence_number = row[0]
                t.timestamp = row[1]
                t.source_addr = row[2]
                t.destination_addr = row[3]
                t.extended_frame = row[4]
                t.priority = row[5]
                t.repeat = row[6]
                t.ack_req = row[7]
                t.confirm = row[8]
                t.system_broadcast = row[9]
                t.hop_count = row[10]
                t.tpci = TPCI_TYPES.get(row[11])
                t.tpci_sequence = row[12]
                t.apci = APCI_TYPES.get(row[13])
                t.payload_data = row[14]
                t.payload_length = row[15]
                t.is_manipulated = row[16]
                t.attack_type_id = row[17]
                t.sensor_addr = row[18]
                telegrams.append(t)

        return telegrams
