import http.client
import urllib.parse
import threading
import time
import os
import sys
from urllib.parse import urlparse

def is_valid_url(url):
    	parsed_url = urlparse(url)
    	return all([parsed_url.scheme, parsed_url.netloc])

class FileDownloader:

    def __init__(self, url):
        self.url = url
        self.downloaded_bytes = 0
        self.running = True

    def start_download(self):
        parsed_url = urllib.parse.urlparse(self.url)
        connection = http.client.HTTPConnection(parsed_url.netloc)
        connection.request("GET", parsed_url.path or "/")
        response = connection.getresponse()

        if response.status != 200:
            self.running = False
            print(f"Failed to download. HTTP status: {response.status}")
            return

        filename = os.path.basename(parsed_url.path) or "downloaded_file"
        with open(filename, "wb") as file:
            while chunk := response.read(1024):
                file.write(chunk)
                self.downloaded_bytes += len(chunk)

        self.running = False
        connection.close()

    def report_progress(self):
        while self.running:
            print(f"Downloaded: {self.downloaded_bytes} bytes")
            time.sleep(1)
        print(f"Download complete. Total bytes: {self.downloaded_bytes}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Succesfull: file downloader")
        sys.exit(1)

    download_url = sys.argv[1]

    if not is_valid_url(download_url):
        print("file downloader: URL некорректен.")
        sys.exit(1)

    downloader = FileDownloader(download_url)

    progress_thread = threading.Thread(target=downloader.report_progress)
    progress_thread.start()

    downloader.start_download()
    progress_thread.join()
