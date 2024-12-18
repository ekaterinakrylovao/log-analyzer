import logging
import platform
import argparse
import glob
from src.file_handler import load_logs
from src.log_parser import parse_log_line
from src.log_stats import LogStatistics
from src.output_formatter import format_output

logging.basicConfig()
logger = logging.getLogger(__name__)


def get_log_file_list(path_pattern):
    return glob.glob(path_pattern)


def main() -> None:
    logger.info(platform.python_version())

    parser = argparse.ArgumentParser(description="NGINX Log Analyzer")
    parser.add_argument(
        "--path", required=True, help="Path or URL to log files (can include wildcards)"
    )
    parser.add_argument(
        "--from",
        dest="from_date",
        help="Start date for filtering logs (ISO8601 format)",
    )
    parser.add_argument(
        "--to", dest="to_date", help="End date for filtering logs (ISO8601 format)"
    )
    parser.add_argument(
        "--filter-field", help='Field to filter logs by (e.g., "agent", "method")'
    )
    parser.add_argument(
        "--filter-value",
        help='Value to filter logs by (supports wildcards, e.g., "Mozilla*")',
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "adoc"],
        default="markdown",
        help="Output format",
    )

    args = parser.parse_args()

    # Загрузка логов
    log_files = get_log_file_list(args.path) or [args.path]
    stats = LogStatistics()
    processed_files = []

    for log_file in log_files:
        logs = load_logs(log_file)
        file_has_valid_logs = False

        for log_line in logs:
            log_record = parse_log_line(log_line)
            if log_record:

                # Проверяем диапазон дат
                if stats.is_within_date_range(log_record, args.from_date, args.to_date):
                    # Проверка фильтрации
                    if args.filter_field and args.filter_value:
                        field_value = log_record.get(args.filter_field)

                        if field_value:
                            # Если использовать '*' для поиска
                            if args.filter_value.replace("*", "") in field_value:
                                stats.update(log_record)
                                file_has_valid_logs = True
                    else:
                        stats.update(log_record)
                        file_has_valid_logs = True

        if file_has_valid_logs:
            processed_files.append(log_file)

    # Формирование отчета
    report = format_output(
        stats, processed_files, args.from_date, args.to_date, args.format
    )
    print(report)


if __name__ == "__main__":
    main()
