import unittest
from datetime import datetime, timezone
from collections import Counter
from src.log_stats import LogStatistics


class TestLogStatistics(unittest.TestCase):

    def setUp(self):
        """Создание экземпляра LogStatistics для использования в тестах."""
        self.log_stats = LogStatistics()
        self.sample_records = [
            {
                "resource": "/index",
                "status": 200,
                "size": 500,
                "time": datetime(2023, 10, 1, tzinfo=timezone.utc),
            },
            {
                "resource": "/about",
                "status": 404,
                "size": 250,
                "time": datetime(2023, 10, 2, tzinfo=timezone.utc),
            },
            {
                "resource": "/contact",
                "status": 200,
                "size": 1000,
                "time": datetime(2023, 10, 3, tzinfo=timezone.utc),
            },
            {
                "resource": "/index",
                "status": 500,
                "size": 150,
                "time": datetime(2023, 10, 4, tzinfo=timezone.utc),
            },
        ]

    def test_update_statistics(self):
        """
        Тестирует метод update для обновления статистики по логу.

        Ожидаемый результат:
        - Обновленные значения total_requests, resources, status_codes и response_sizes
          соответствуют переданным данным.
        """
        for record in self.sample_records:
            self.log_stats.update(record)

        self.assertEqual(self.log_stats.total_requests, 4)
        self.assertEqual(
            self.log_stats.resources, Counter({"/index": 2, "/about": 1, "/contact": 1})
        )
        self.assertEqual(self.log_stats.status_codes, Counter({200: 2, 404: 1, 500: 1}))
        self.assertEqual(self.log_stats.response_sizes, [500, 250, 1000, 150])

    def test_average_size(self):
        """
        Тестирует метод average_size для вычисления среднего размера ответа.

        Ожидаемый результат:
        - Возвращает среднее значение размера ответов.
        """
        for record in self.sample_records:
            self.log_stats.update(record)

        expected_average = (500 + 250 + 1000 + 150) / 4
        self.assertAlmostEqual(
            self.log_stats.average_size(), expected_average, places=2
        )

    def test_percentile_95(self):
        """
        Тестирует метод percentile_95 для вычисления 95-го процентиля размера ответа.

        Ожидаемый результат:
        - Возвращает значение 95-го процентиля в массиве размеров ответов.
        """
        for record in self.sample_records:
            self.log_stats.update(record)

        # 95-й процентиль в отсортированном [150, 250, 500, 1000] будет 500
        self.assertEqual(self.log_stats.percentile_95(), 500)

    def test_is_within_date_range_within_range(self):
        """
        Тестирует проверку записи лога, находящейся внутри диапазона.

        Ожидаемый результат:
        - Возвращает True, если запись времени находится в пределах заданного диапазона.
        """
        log_record = {"time": datetime(2023, 10, 1, 12, 0, tzinfo=timezone.utc)}
        from_date = "2023-10-01T00:00:00"
        to_date = "2023-10-31T00:00:00"
        self.assertTrue(
            LogStatistics.is_within_date_range(log_record, from_date, to_date)
        )

    def test_is_within_date_range_before_range(self):
        """
        Тестирует проверку записи лога, находящейся до начала диапазона.

        Ожидаемый результат:
        - Возвращает False, если запись времени находится перед заданным диапазоном.
        """
        log_record = {"time": datetime(2023, 9, 30, 12, 0, tzinfo=timezone.utc)}
        from_date = "2023-10-01T00:00:00"
        to_date = "2023-10-31T00:00:00"
        self.assertFalse(
            LogStatistics.is_within_date_range(log_record, from_date, to_date)
        )

    def test_is_within_date_range_after_range(self):
        """
        Тестирует проверку записи лога, находящейся после окончания диапазона.

        Ожидаемый результат:
        - Возвращает False, если запись времени находится после заданного диапазона.
        """
        log_record = {"time": datetime(2023, 11, 1, 12, 0, tzinfo=timezone.utc)}
        from_date = "2023-10-01T00:00:00"
        to_date = "2023-10-31T00:00:00"
        self.assertFalse(
            LogStatistics.is_within_date_range(log_record, from_date, to_date)
        )

    def test_is_within_date_range_on_start_boundary(self):
        """
        Тестирует проверку записи лога, находящейся на границе начала диапазона.

        Ожидаемый результат:
        - Возвращает True, если запись времени соответствует началу диапазона.
        """
        log_record = {"time": datetime(2023, 10, 1, 0, 0, tzinfo=timezone.utc)}
        from_date = "2023-10-01T00:00:00"
        to_date = "2023-10-31T00:00:00"
        self.assertTrue(
            LogStatistics.is_within_date_range(log_record, from_date, to_date)
        )

    def test_is_within_date_range_on_end_boundary(self):
        """
        Тестирует проверку записи лога, находящейся на границе конца диапазона.

        Ожидаемый результат:
        - Возвращает True, если запись времени соответствует окончанию диапазона.
        """
        log_record = {"time": datetime(2023, 10, 31, 23, 59, 59, tzinfo=timezone.utc)}
        from_date = "2023-10-01T00:00:00"
        to_date = "2023-10-31T00:00:00"
        self.assertTrue(
            LogStatistics.is_within_date_range(log_record, from_date, to_date)
        )


if __name__ == "__main__":
    unittest.main()
