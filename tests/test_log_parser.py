import unittest
from datetime import datetime, timezone
from src.log_parser import parse_log_line


class TestLogParser(unittest.TestCase):

    def test_parse_valid_log_line(self):
        """
        Тестирует корректный разбор валидной строки логов.

        Входные данные:
        - log_line (str): Строка логов, соответствующая ожидаемому формату.

        Ожидаемый результат:
        - Возвращает словарь с данными, включая:
            - 'ip': IP-адрес (str)
            - 'time': Время запроса в формате datetime (datetime)
            - 'method': HTTP-метод (str)
            - 'resource': Запрашиваемый ресурс (str)
            - 'status': HTTP-статус (int)
            - 'size': Размер ответа (int, 0 если '-')
            - 'agent': User-Agent строки (str)
        """
        log_line = (
            '93.180.71.3 - - [17/May/2015:08:05:32 +0000] "GET /downloads/product_1 HTTP/1.1" 304 0 "-" '
            '"Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"'
        )
        expected_output = {
            "ip": "93.180.71.3",
            "time": datetime(2015, 5, 17, 8, 5, 32, tzinfo=timezone.utc),
            "method": "GET",
            "resource": "/downloads/product_1",
            "status": 304,
            "size": 0,
            "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)",
        }
        self.assertEqual(parse_log_line(log_line), expected_output)

    def test_parse_invalid_log_line(self):
        """
        Тестирует разбор недопустимой строки логов.

        Входные данные:
        - log_line (str): Строка, не соответствующая формату логов.

        Ожидаемый результат:
        - Возвращает None, так как строка не может быть разобрана.
        """
        log_line = "Invalid log line format"
        self.assertIsNone(parse_log_line(log_line))

    def test_parse_log_line_with_size_dash(self):
        """
        Тестирует разбор строки логов, где размер ответа указан как '-'.

        Входные данные:
        - log_line (str): Строка логов с размером '-'.

        Ожидаемый результат:
        - Возвращает словарь с данными, где размер будет равен 0.
        """
        log_line = (
            '93.180.71.3 - - [17/May/2015:08:05:32 +0000] "GET /downloads/product_1 HTTP/1.1" 200 - "-" '
            '"Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"'
        )
        expected_output = {
            "ip": "93.180.71.3",
            "time": datetime(2015, 5, 17, 8, 5, 32, tzinfo=timezone.utc),
            "method": "GET",
            "resource": "/downloads/product_1",
            "status": 200,
            "size": 0,  # "-" соответствует 0
            "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)",
        }
        self.assertEqual(parse_log_line(log_line), expected_output)

    def test_parse_log_line_with_nonstandard_size(self):
        """
        Тестирует разбор строки логов с нестандартным размером ответа.

        Входные данные:
        - log_line (str): Строка логов с конкретным размером ответа.

        Ожидаемый результат:
        - Возвращает словарь с данными, где размер соответствует указанному значению.
        """
        log_line = (
            '93.180.71.3 - - [17/May/2015:08:05:32 +0000] "GET /downloads/product_1 HTTP/1.1" 404 1234 "-" '
            '"Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"'
        )
        expected_output = {
            "ip": "93.180.71.3",
            "time": datetime(2015, 5, 17, 8, 5, 32, tzinfo=timezone.utc),
            "method": "GET",
            "resource": "/downloads/product_1",
            "status": 404,
            "size": 1234,
            "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)",
        }
        self.assertEqual(parse_log_line(log_line), expected_output)


if __name__ == "__main__":
    unittest.main()
