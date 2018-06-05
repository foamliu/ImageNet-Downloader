import imghdr
import os
import sys
import threading
import time
from queue import Queue
from socket import error as SocketError
from socket import timeout as TimeoutError
from ssl import CertificateError

import httplib
import urllib2


class DownloadError(Exception):
    def __init__(self, message=""):
        self.message = message


def download(url, timeout=500, retry=3, sleep=0.8):
    """Downloads a file at given URL."""
    count = 0
    while True:
        try:
            f = urllib2.urlopen(url, timeout=timeout)
            if f is None:
                raise DownloadError('Cannot open URL' + url)
            content = f.read()
            f.close()
            break
        except (urllib2.HTTPError, httplib.HTTPException, CertificateError) as e:
            count += 1
            if count > retry:
                raise DownloadError()
        except (urllib2.URLError, TimeoutError, SocketError, IOError) as e:
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
    name = item.split(' ')[0]
    url = item.split(' ')[1]
    try:
        image = download(url)
        try:
            extension = imghdr.what('', image)
            if extension == "jpeg":
                extension = "jpg"
            if extension is None:
                raise DownloadError()
        except:
            raise DownloadError()
        if (sys.getsizeof(image) > min_size):
            image_name = name + '.' + extension;
            image_path = os.path.join(dir_path, image_name)
            image_file = open(image_path, 'w')
            image_file.write(image)
            image_file.close()
            print("Downloaded: {}".format(image_name))
            time.sleep(10)
    except DownloadError as e:
        print('Could not download ' + url)


def worker():
    while True:
        item = q.get()
        if item is None:
            break
        download_images(item)
        q.task_done()


if __name__ == '__main__':
    num_worker_threads = 16
    threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    fname = 'fall11_urls.txt'
    with open(fname) as f:
        lines = f.readlines()
    q = Queue()
    for item in lines:
        q.put(item)

    # block until all tasks are done
    q.join()

    # stop workers
    for i in range(num_worker_threads):
        q.put(None)
    for t in threads:
        t.join()
