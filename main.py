import datetime
import locale
from datetime import timedelta
from timeit import default_timer

import pytz
from aulas.logger import LoggerFactory
from aulas.pipes.digest import update_latest_cache
from aulas.pipes.scraper import temp_download
from aulas.pipes.xlsx import convert_from_excel
from aulas.server.listeners import ConnectionListener, EventListener
from aulas.server.server import Server
from dotenv import dotenv_values

log = LoggerFactory.getLogger("main")
timezone = pytz.timezone("Etc/GMT+3")
locale.setlocale(locale.LC_ALL, 'es_AR.utf8')  # Must match locale -a
env = dotenv_values()

def download():
    path, filename, extension = './resources/', 'aulas', '.xlsx'
    should_process = temp_download(env['download_path'], path, filename, extension)
    if should_process:
        log.info("Processing file...")
        elapsed_time = default_timer()
        convert_from_excel('aulas.xlsx')
        elapsed_time = default_timer() - elapsed_time
        log.info(f"Created output in {timedelta(seconds=elapsed_time)}")


if __name__ == '__main__':
    # download()
    # time = datetime.datetime.now(timezone)
    # time += timedelta()
    # update_latest_cache(time)
    try:
        server = Server(12345)
        server.add_listener('connection', ConnectionListener.call)
        server.add_listener('receive', EventListener.call)
        server.start()
    except KeyboardInterrupt:
        log.warning("User interrupted")
        exit(0)
