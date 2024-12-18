import os
import unittest
from src.file_handler import (
    load_logs,
    load_logs_from_url,
    load_logs_from_file,
    load_logs_from_files,
)


class TestFileHandlerWithRealData(unittest.TestCase):

    def test_load_logs_from_file(self):
        """
        Тестирование функции load_logs_from_file.

        Проверяет, что логи успешно загружаются из файла и не являются пустыми.
        Также проверяется, что ожидаемая строка присутствует в загруженных логах.

        Входные данные:
            - Имя файла: "../logs.txt"

        Ожидаемый результат:
            - Длина загруженных логов больше 0.
            - В первых 10 строках содержится конкретная строка лога.
        """
        file_name = os.path.join(os.path.dirname(__file__), "../logs.txt")
        logs = [
            log.strip() for log in load_logs_from_file(file_name)
        ]  # Удаляем лишние пробелы и символы новой строки
        self.assertTrue(len(logs) > 0)
        self.assertIn(
            '93.180.71.3 - - [17/May/2015:08:05:32 +0000] "GET /downloads/product_1 HTTP/1.1" 304 0 "-" '
            '"Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"',
            logs[:10],
        )

    def test_load_logs_from_files(self):
        """
        Тестирование функции load_logs_from_files.

        Проверяет, что логи успешно загружаются из нескольких файлов и не являются пустыми.
        Также проверяется, что ожидаемая строка присутствует в загруженных логах.

        Входные данные:
            - Паттерн пути к файлам: "../logs/*.txt"

        Ожидаемый результат:
            - Длина загруженных логов больше 0.
            - Ожидаемая строка присутствует в загруженных логах.
        """
        path_pattern = os.path.join(os.path.dirname(__file__), "../logs/*.txt")
        logs = [
            log.strip() for log in load_logs_from_files(path_pattern)
        ]  # Удаляем лишние пробелы и символы новой
        # строки
        self.assertTrue(len(logs) > 0)
        self.assertIn(
            '93.180.71.3 - - [17/May/2015:08:05:32 +0000] "GET /downloads/product_1 HTTP/1.1" 304 0 "-" '
            '"Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"',
            logs,
        )

    def test_load_logs(self):
        """
        Тестирование функции load_logs.

        Проверяет, что логи успешно загружаются как из файла, так и из URL.
        Подтверждает, что оба источника возвращают данные и не пусты.

        Входные данные:
            - Путь к файлу: "../logs.txt"
            - URL для загрузки:
                "https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/nginx_logs/nginx_logs"

        Ожидаемый результат:
            - Длина загруженных логов из файла больше 0.
            - Длина загруженных логов из URL больше 0.
        """
        file_path = os.path.join(os.path.dirname(__file__), "../logs.txt")
        logs_from_file = [
            log.strip() for log in load_logs(file_path)
        ]  # Удаляем лишние пробелы и символы новой строки
        self.assertTrue(len(logs_from_file) > 0)

        url = "https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/nginx_logs/nginx_logs"
        logs_from_url = list(load_logs(url))
        self.assertTrue(len(logs_from_url) > 0)

    def test_load_logs_from_url(self):
        """
        Тестирование функции load_logs_from_url.

        Проверяет, что логи успешно загружаются из указанного URL и не являются пустыми.
        Также подтверждает, что первая строка лога не равна None и содержит ожидаемую информацию.

        Входные данные:
            - URL для загрузки:
                "https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/nginx_logs/nginx_logs"

        Ожидаемый результат:
            - Первая строка логов не равна None.
            - Ожидаемая строка присутствует в первой строке загруженных логов.
        """
        url = "https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/nginx_logs/nginx_logs"
        logs = load_logs_from_url(url)
        first_line = next(
            logs, None
        )  # Получаем первую строку или None, если генератор пуст
        self.assertIsNotNone(first_line)  # Проверяем, что первая строка не None
        self.assertIn(
            '93.180.71.3 - - [17/May/2015:08:05:32 +0000] "GET /downloads/product_1 HTTP/1.1" 304 0 "-" "Debian '
            'APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"',
            first_line,
        )


if __name__ == "__main__":
    unittest.main()
