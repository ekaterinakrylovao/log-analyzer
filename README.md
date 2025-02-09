# NGINX Log Analyzer

Этот проект представляет собой анализатор логов NGINX, который может обрабатывать локальные файлы логов или загружать их из URL. Он позволяет фильтровать и собирать статистику по запросам за определённые даты, а также предоставляет возможность фильтрации по определённым полям. Результаты можно вывести в форматах `markdown` или `adoc`.

## Запуск проекта

Чтобы запустить проект, вам потребуется [Poetry](https://python-poetry.org/). После установки Poetry выполните следующие команды в терминале:

### 1. Клонируйте репозиторий

```bash
git clone <URL_репозитория>
cd <название_репозитория>
```

### 2. Установите зависимости

```bash
poetry install
```

### 2. Запуск программы

```bash
poetry run python -m src.main
```

Но, чтобы более удобно запускать программу через команду analyzer, установите:

```bash
python setup.py install
```

После этого можно использовать ```analyzer``` как команду в терминале.

## Функции программы

Анализатор логов NGINX выполняет следующие задачи:

1. **Подсчитывает общее количество запросов** — общее количество запросов, содержащихся в анализируемых лог-файлах.
2. **Определяет наиболее часто запрашиваемые ресурсы** — выводит 10 самых часто запрашиваемых ресурсов.
3. **Определяет наиболее часто встречающиеся коды ответа** — подсчитывает количество различных кодов ответа и их частоту.
4. **Рассчитывает средний размер ответа сервера** — вычисляет средний размер всех ответов сервера в логах.
5. **Рассчитывает 95-й перцентиль размера ответа сервера** — позволяет увидеть, до какого размера входят 95% ответов сервера, что помогает выявить нетипичные или аномальные размеры ответов.

Результаты могут быть представлены в двух форматах: `markdown` и `adoc`, в зависимости от настроек пользователя.

Примерные данные, представленные в выводе программы:

```plaintext
#### Общая информация

|        Метрика        |        Значение        |
|:---------------------:|-----------------------:|
|       Файл(-ы)        |  logs\2015-05-18.txt
|                       |  logs\2015-05-19.txt
|    Начальная дата     |   -
|     Конечная дата     |   2015-05-19
|  Количество запросов  |   19
| Средний размер ответа |   24521216.84b
|   95p размера ответа  |   26318005.00b

#### Запрашиваемые ресурсы

|         Ресурс         |  Количество  |
|:----------------------:|-------------:|
| /downloads/product_2   |    19

#### Коды ответа

| Код |  Количество |
|:---:|------------:|
| 200 | 18
| 304 | 1
```

Этот формат позволяет легко получать ключевую информацию об анализируемых логах и выявлять аномалии.

## Примеры запуска

### Работа с имеющимися файлами логов

Эти примеры показывают, как анализировать файлы логов в папке logs и фильтровать их по дате и формату вывода.

- Анализ логов за период с 31 мая по 2 июня 2015 года и вывод в формате ```adoc```:

```bash
analyzer --path logs/2015* --from 2015-05-31 --to 2015-06-02 --format adoc
```

- Аналогичный анализ, но с выводом в формате ```markdown``` (```markdown``` идёт автоматически, даже если его не указать):

```bash
analyzer --path logs/2015* --from 2015-05-31 --to 2015-06-02 --format markdown
```

- Анализ конкретного файла логов

```bash
analyzer --path logs/2015-05-17.txt
```

- Анализ общего файла логов logs.txt по датам до 20 мая 2015 года:

```bash
analyzer --path logs.txt --to 2015-05-20 --format markdown
```

### Работа с URL

Эти примеры демонстрируют, как загружать логи по URL и выполнять фильтрацию.

- Загрузка логов с GitHub и фильтрация по дате:

```bash
analyzer --path https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/nginx_logs/nginx_logs --from 2015-05-17 --format adoc
```

- Загрузка и анализ логов без фильтрации:

```bash
analyzer --path https://raw.githubusercontent.com/elastic/examples/master/Common%20Data%20Formats/nginx_logs/nginx_logs
```

### UPDATE: Фильтрация по полям

Вы можете использовать фильтрацию по полям, например ```agent``` (user-agent) или ```method``` (HTTP-метод).

- Фильтрация по ```agent```, начиная с ```"Mozilla*"```:

```bash
analyzer --path logs/2015* --from 2015-05-18 --to 2015-05-19 --filter-field agent --filter-value "Mozilla*"
```

- Фильтрация по ```method``` для запросов ```GET``` за определённый период:

```bash
analyzer --path logs/2015* --from 2015-05-17 --to 2015-05-19 --filter-field method --filter-value "GET" --format adoc
```

### Помощь и параметры

Для получения справки по параметрам можно использовать команду:

```bash
analyzer --help
```

Вывод справки (адаптированный под README с ещё более подробным описанием):

```plaintext
usage: analyzer [-h] --path PATH [--from FROM_DATE] [--to TO_DATE] [--filter-field FILTER_FIELD] [--filter-value FILTER_VALUE] [--format {markdown,adoc}]

optional arguments:
  -h, --help           Показать справку по командам
  --path PATH          Путь к файлу логов или URL (поддерживает символы подстановки, такие как '*')
  --from FROM_DATE     Начальная дата для фильтрации логов (формат ISO8601)
  --to TO_DATE         Конечная дата для фильтрации логов (формат ISO8601)
  --filter-field FILTER_FIELD
                       Поле для фильтрации логов (например, "agent", "method")
  --filter-value FILTER_VALUE
                       Значение для фильтрации (поддерживает символы подстановки, например, "Mozilla*")
  --format {markdown,adoc}
                       Формат вывода отчета (по умолчанию: markdown)
```