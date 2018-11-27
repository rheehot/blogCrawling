import threading
import yaml
from queue import Queue
from spider import Spider
from domain import *
from general import *

stream = open('db_sync_blogspot.yml', 'r', encoding="UTF8")
data = yaml.load(stream)
NUMBER_OF_THREADS = 1
# db.yml = 1019 // db_naver_yml = 35 // db_sync_blogspot = 3
NUMBER_OF_BLOGGERS = 1

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


for person in range(NUMBER_OF_BLOGGERS):
    try:
        PROJECT_NAME = data[person]['name']
        HOMEPAGE = data[person]['blog']
        DOMAIN_NAME = data[person]['blog']
        Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

        QUEUE_FILE = 'user\\' + PROJECT_NAME + '/queue.txt'
        CRAWLED_FILE = 'user\\' + PROJECT_NAME + '/crawled.txt'
        queue = Queue()

        create_workers()
        crawl()

    except: pass
