from collections import Counter
from datetime import datetime, timedelta


class LogStatistics:
    """
    Класс для сбора и анализа статистики логов.

    Этот класс собирает статистику по количеству запросов, запрашиваемым ресурсам,
    кодам статусов и размерам ответов, а также предоставляет методы для анализа этих данных.

    Attributes:
        total_requests (int): Общее количество запросов.
        resources (Counter): Счётчик ресурсов, запрашиваемых в логах.
        status_codes (Counter): Счётчик кодов статусов ответов.
        response_sizes (list): Список размеров ответов.

    Methods:
        update(log_record):
            Обновляет статистику на основе предоставленной записи лога.

        is_within_date_range(log_record, from_date=None, to_date=None):
            Проверяет, находится ли время записи лога в заданном диапазоне дат.

        average_size():
            Вычисляет средний размер ответов.

        percentile_95():
            Вычисляет 95-й процентиль размеров ответов.
    """

    def __init__(self):
        """
        Инициализирует экземпляр класса LogStatistics.
        """
        self.total_requests = 0
        self.resources = Counter()
        self.status_codes = Counter()
        self.response_sizes = []

    def update(self, log_record):
        """
        Обновляет статистику на основе предоставленной записи лога.

        Args:
            log_record (dict): Запись лога, содержащая информацию о запросе,
                               включая ресурс, код статуса и размер ответа.
        """
        self.total_requests += 1
        self.resources[log_record["resource"]] += 1
        self.status_codes[log_record["status"]] += 1
        self.response_sizes.append(log_record["size"])

    @staticmethod
    def is_within_date_range(log_record, from_date=None, to_date=None):
        """
        Проверяет, находится ли время записи лога в заданном диапазоне дат.

        Args:
            log_record (dict): Запись лога, содержащая информацию о времени запроса.
            from_date (str, optional): Начальная дата в формате ISO8601.
            to_date (str, optional): Конечная дата в формате ISO8601.

        Returns:
            bool: True, если время записи лога находится в диапазоне, иначе False.
        """
        log_time = log_record["time"].replace(
            tzinfo=None
        )  # Приводим log_time к offset-naive

        # Преобразуем строки в datetime без timezone, если даты заданы
        if from_date is not None:
            from_date = datetime.fromisoformat(from_date)
        if to_date is not None:
            # Увеличиваем конечную дату на один день, чтобы включить её
            to_date = datetime.fromisoformat(to_date) + timedelta(days=1)

        # Проверка диапазонов дат
        if from_date and to_date:
            return from_date <= log_time < to_date  # Конец диапазона включен
        elif from_date:
            return log_time >= from_date
        elif to_date:
            return log_time < to_date
        return True  # Если даты не указаны, возвращаем True

    def average_size(self):
        """
        Вычисляет средний размер ответов.

        Returns:
            float: Средний размер ответа, или 0, если ответов нет.
        """
        return (
            sum(self.response_sizes) / len(self.response_sizes)
            if self.response_sizes
            else 0
        )

    def percentile_95(self):
        """
        Вычисляет 95-й процентиль размеров ответов.

        Returns:
            float: 95-й процентиль размеров ответов, или 0, если ответов нет.
        """
        if not self.response_sizes:
            return 0
        sorted_sizes = sorted(self.response_sizes)
        index = int(len(sorted_sizes) * 0.95) - 1
        return sorted_sizes[index]
