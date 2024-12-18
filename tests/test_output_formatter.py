import unittest
from collections import Counter

from src.output_formatter import format_output


class TestOutputFormatter(unittest.TestCase):

    class MockStats:
        def __init__(self):
            self.total_requests = 100
            self.resources = Counter(
                {
                    "/downloads/product_1": 40,
                    "/downloads/product_2": 30,
                    "/downloads/product_3": 20,
                    "/downloads/product_4": 10,
                }
            )
            self.status_codes = Counter({200: 80, 404: 10, 500: 10})

        def average_size(self):
            return 250.0  # Пример среднего размера

        def percentile_95(self):
            return 400.0  # Пример 95-го перцентиля

    def setUp(self):
        self.stats = self.MockStats()
        self.files = ["file1.log", "file2.log"]
        self.from_date = "2023-10-01T00:00:00"
        self.to_date = "2023-10-31T23:59:59"

    def test_format_markdown(self):
        expected_output = """#### Общая информация

|        Метрика        |        Значение        |
|:---------------------:|-----------------------:|
|       Файл(-ы)        |  file1.log
|                       |  file2.log
|    Начальная дата     |   2023-10-01T00:00:00
|     Конечная дата     |   2023-10-31T23:59:59
|  Количество запросов  |   100
| Средний размер ответа |   250.00b
|   95p размера ответа  |   400.00b

#### Запрашиваемые ресурсы

|         Ресурс         |  Количество  |
|:----------------------:|-------------:|
|  /downloads/product_1  |    40
|  /downloads/product_2  |    30
|  /downloads/product_3  |    20
|  /downloads/product_4  |    10

#### Коды ответа

| Код |  Количество |
|:---:|------------:|
| 200 |    80
| 404 |    10
| 500 |    10
    """
        result = format_output(
            self.stats, self.files, self.from_date, self.to_date, "markdown"
        )
        self.assertEqual(result.strip(), expected_output.strip())

    def test_format_adoc(self):
        expected_output = """== Общая информация

|=== 
|Метрика                |Значение
|Файл(-ы)               |file1.log, file2.log
|Начальная дата         |2023-10-01T00:00:00
|Конечная дата          |2023-10-31T23:59:59
|Количество запросов    |100
|Средний размер ответа  |250.00b
|95p размера ответа     |400.00b
|===

== Запрашиваемые ресурсы

|=== 
|Ресурс               |Количество
|/downloads/product_1 |40
|/downloads/product_2 |30
|/downloads/product_3 |20
|/downloads/product_4 |10
|===

== Коды ответа

|=== 
|Код |Количество
|200 |80
|404 |10
|500 |10
|=== 
"""
        result = format_output(
            self.stats, self.files, self.from_date, self.to_date, "adoc"
        )
        self.assertEqual(result.strip(), expected_output.strip())


if __name__ == "__main__":
    unittest.main()
