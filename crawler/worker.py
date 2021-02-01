from threading import Thread

from utils.download import download
from utils import get_logger
from scraper import scraper
import time

# Solutions to question 1
DOWNLOAD_SET = set()

class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.worker_id = worker_id
        self.config = config
        self.frontier = frontier
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info(f"Frontier for this worker is empty. Stopping Worker {self.worker_id}.")
                break

            if tbd_url in DOWNLOAD_SET:
                continue
            DOWNLOAD_SET.add(tbd_url)
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            # time.sleep(self.config.time_delay) MORE WORK
