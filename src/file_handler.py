import glob
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Задаю размер буфера для накопления строк перед передачей в основной поток
BUFFER_SIZE = 100


def load_logs(path):
    if path.startswith("http"):
        return load_logs_from_url(path)
    else:
        return load_logs_from_files(path)


def load_logs_from_url(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    for line in response.iter_lines(decode_unicode=True):
        if line:
            yield line


def load_logs_from_file(file_name):
    """Чтение логов из локального файла с использованием буфера."""
    buffer = []
    with open(file_name, "r") as f:
        for line in f:
            buffer.append(line)
            if len(buffer) >= BUFFER_SIZE:
                yield from buffer
                buffer.clear()
        if buffer:
            yield from buffer


def load_logs_from_files(path):
    files = glob.glob(path)
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(load_logs_from_file, file): file for file in files}
        for future in as_completed(futures):
            file = futures[future]
            try:
                for line in future.result():
                    yield line
            except Exception as e:
                print(f"Error processing file {file}: {e}")
