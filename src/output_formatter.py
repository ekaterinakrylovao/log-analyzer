def format_output(stats, files, from_date, to_date, output_format):
    if output_format == "markdown":
        return format_markdown(stats, files, from_date, to_date)
    elif output_format == "adoc":
        return format_adoc(stats, files, from_date, to_date)
    else:
        raise ValueError(f"Unsupported output format: {output_format}")


def format_markdown(stats, files, from_date, to_date):
    resources = stats.resources.most_common(10)
    status_codes = stats.status_codes.most_common()

    return f"""
#### Общая информация

|        Метрика        |        Значение        |
|:---------------------:|-----------------------:|
|       Файл(-ы)        |  {'\n|                       |  '.join(files)}
|    Начальная дата     |   {from_date or '-'}
|     Конечная дата     |   {to_date or '-'}
|  Количество запросов  |   {stats.total_requests}
| Средний размер ответа |   {stats.average_size():.2f}b
|   95p размера ответа  |   {stats.percentile_95():.2f}b

#### Запрашиваемые ресурсы

|         Ресурс         |  Количество  |
|:----------------------:|-------------:|
{"".join([f"|  {res}  |    {count}\n" for res, count in resources])}
#### Коды ответа

| Код |  Количество |
|:---:|------------:|
{"".join([f"| {code} |    {count}\n" for code, count in status_codes])}
    """


def format_adoc(stats, files, from_date, to_date):
    resources = stats.resources.most_common(10)
    status_codes = stats.status_codes.most_common()

    return f"""
== Общая информация

|=== 
|Метрика                |Значение
|Файл(-ы)               |{', '.join(files)}
|Начальная дата         |{from_date or '-'}
|Конечная дата          |{to_date or '-'}
|Количество запросов    |{stats.total_requests}
|Средний размер ответа  |{stats.average_size():.2f}b
|95p размера ответа     |{stats.percentile_95():.2f}b
|===

== Запрашиваемые ресурсы

|=== 
|Ресурс               |Количество
{"".join([f"|{res} |{count}\n" for res, count in resources])}|===

== Коды ответа

|=== 
|Код |Количество
{"".join([f"|{code} |{count}\n" for code, count in status_codes])}|===
    """
