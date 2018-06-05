import codecs
import http.client
import imghdr
import os
import sys
import threading
import time
import urllib.request
from queue import Queue
from socket import error as SocketError
from socket import timeout as TimeoutError
from ssl import CertificateError

from console_progressbar import ProgressBar


class DownloadError(Exception):
    def __init__(self, message=""):
        self.message = message


def download(url, timeout=500, retry=3, sleep=0.8):
    """Downloads a file at given URL."""
    count = 0
    while True:
        try:
            f = urllib.request.urlopen(url, timeout=timeout)
            if f is None:
                raise DownloadError('Cannot open URL' + url)
            content = f.read()
            f.close()
            break
        except (urllib.request.HTTPError, http.client.HTTPException, CertificateError) as e:
            count += 1
            if count > retry:
                raise DownloadError()
        except (urllib.request.URLError, TimeoutError, SocketError, IOError) as e:
            count += 1
            if count > retry:
                raise DownloadError()
            time.sleep(sleep)
    return content


def make_directory(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def download_images(item, dir_path='data'):
    min_size = 1000
    make_directory(dir_path)
    tokens = item.split('\t')
    name = tokens[0]
    url = tokens[1]
    try:
        image = download(url)
        try:
            extension = imghdr.what('', image)
            if extension == "jpeg":
                extension = "jpg"
            if extension is None:
                return
        except:
            pass
            # raise DownloadError()
        if (sys.getsizeof(image) > min_size):
            image_name = name + '.' + extension;
            image_path = os.path.join(dir_path, image_name)
            image_file = open(image_path, 'wb')
            image_file.write(image)
            image_file.close()
            # print("Downloaded: {}".format(image_name))
            time.sleep(10)
    except DownloadError as e:
        pass
        # print('Could not download ' + url)
    except:
        pass


def worker(q):
    while True:
        item = q.get()
        if item is None:
            break
        download_images(item)
        q.task_done()


if __name__ == '__main__':
    fname = 'fall11_urls.txt'
    print('Loading image urls...')
    with codecs.open(fname, "r", encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    print('{} urls loaded'.format(len(lines)))

    q = Queue()
    for item in lines:
        q.put(item)
    print('{} urls enqueued'.format(q.qsize()))

    threadLock = threading.Lock()
    num_worker_threads = 256
    threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker, args=(q,))
        t.start()
        threads.append(t)

    pb = ProgressBar(total=len(lines), prefix='Downloading images', suffix='', decimals=3, length=50, fill='=')
    while True:
        if q.qsize() == 0:
            break
        pb.print_progress_bar(len(lines) - q.qsize())
        time.sleep(500)

    # block until all tasks are done
    q.join()

    # stop workers
    for i in range(num_worker_threads):
        q.put(None)
    for t in threads:
        t.join()
