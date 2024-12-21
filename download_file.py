import http.client
import urllib.parse
import threading
import time
import os
import sys
from urllib.parse import urlparse

# Проверка URL на корректность
def is_valid_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])

class FileDownloader:
    def __init__(self, url):
        self.url = 
        self.downloaded_bytes = 0  
        self.running = True  # Флаг, показывающий, идет ли скачивание
        
    # Скачивание файла
    def start_download(self):
        # Разбираем URL для получения домена и пути
        parsed_url = urllib.parse.urlparse(self.url)
        connection = http.client.HTTPConnection(parsed_url.netloc)  # Устанавливаем соединение
        connection.request("GET", parsed_url.path or "/")  # Отправляем GET-запрос
        response = connection.getresponse()  # Получаем ответ от сервера

        # Проверяем статус ответа: если не 200, выводим ошибку
        if response.status != 200:
            self.running = False
            print(f"Failed to download. HTTP status: {response.status}")
            return

        # Получаем имя файла
        filename = os.path.basename(parsed_url.path) or "downloaded_file"
        with open(filename, "wb") as file:
            # Скачиваем данные частями по 1024 байта
            while chunk := response.read(1024):
                file.write(chunk)  # Записываем по частям 
                self.downloaded_bytes += len(chunk)  # Счетчик байт

        self.running = False  
        connection.close()  

    # Прогресс скачивания
    def report_progress(self):
        # Вывод каждую секунду
        while self.running:
            print(f"Downloaded: {self.downloaded_bytes} bytes")
            time.sleep(1)  
        
        print(f"Download complete. Total bytes: {self.downloaded_bytes}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_file.py <URL>") 
        sys.exit(1)

    download_url = sys.argv[1]  # Получаем URL

    # Проверяем URL на корректность
    if not is_valid_url(download_url):
        print("file downloader: URL некорректен.")
        sys.exit(1)

    # Создаем объект для скачивания файла
    downloader = FileDownloader(download_url)

    # Поток для отображения прогресса
    progress_thread = threading.Thread(target=downloader.report_progress)
    progress_thread.start()

    downloader.start_download()

    progress_thread.join()
