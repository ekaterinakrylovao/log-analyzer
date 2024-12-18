import sys
from unittest.mock import patch
from src.main import main


def test_main() -> None:
    # Подготовка аргументов командной строки
    test_args = [
        'src/main.py',
        '--path', 'logs/2015*',
        '--from', '2015-05-18',
        '--to', '2015-05-19',
        '--filter-field', 'agent',
        '--filter-value', 'Mozilla*',
        '--format', 'markdown'
    ]

    with patch.object(sys, 'argv', test_args):
        main()  # Вызов основной функции
