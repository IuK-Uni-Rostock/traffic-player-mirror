import mysql.connector

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
        cursor.execute("SELECT sequence_number, timestamp, source_addr, destination_addr, apci, tpci, priority, " \
                       "repeated, hop_count, apdu, payload_length, cemi, payload_data, is_manipulated, sensor_addr) " \
                       "FROM {0} WHERE timestamp >= {1} AND timestamp <= {2}".format(self.__log_table, start_time, end_time))
        rows = cursor.fetchall()

        telegrams = []
        for row in rows:
            if row[2] is None and row[3] is None: # check for ack telegram
                t = AckTelegram()
                t.sequence_number = row[0]
                t.timestamp = row[1]
                t.apci = row[4]
                t.cemi = row[11]
                t.is_manipulated = row[13]
                t.sensor_addr = row[14]
                telegrams.append(t)
            else:
                t = Telegram()
                t.sequence_number = row[0]
                t.timestamp = row[1]
                t.source_addr = row[2]
                t.destination_addr = row[3]
                t.apci = row[4]
                t.tpci = row[5]
                t.priority = row[6]
                t.repeated = row[7]
                t.hop_count = row[8]
                t.apdu = row[9]
                t.payload_length = row[10]
                t.cemi = row[11]
                t.payload_data = row[12]
                t.is_manipulated = row[13]
                t.sensor_addr = row[14]
                telegrams.append(t)

        return telegrams
