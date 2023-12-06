from aulas.logger import LoggerFactory


class ConnectionListener:
    log = LoggerFactory.getLogger('connection_listener')

    @staticmethod
    def call(conn, addr):
        ConnectionListener.log.info(f'{addr[0]} connected to server.')


class EventListener:
    log = LoggerFactory.getLogger('event_listener')
    fun_map = {
        0b1010111: 'download_spreadsheet',  # 87
        0b1101101: 'parse_spreadsheet',  # 109
        0b1011011: 'generate_current_timetable',  # 91
    }

    @staticmethod
    def call(x: bytes):
        interpreted_data = int.from_bytes(x, byteorder='little')
        display_data = EventListener.fun_map.get(interpreted_data, hex(interpreted_data))
        EventListener.log.info(f"Received '{display_data}'.")
        return interpreted_data
