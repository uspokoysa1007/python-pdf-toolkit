# python-pdf-toolkit

Автономная утилита для инспекции, анализа структуры и генерации PDF-документов на Python 3.

## Возможности
- Инспекция структуры любого PDF-файла без сторонних библиотек:
  - Версия формата (`%PDF-1.x`).
  - Метаданные (Title, Author, Producer, CreationDate).
  - Подсчет страниц (`/Count`, `/Page` объекты).
  - Список встроенных объектов (`obj ... endobj`), потоков данных (`stream`) и шрифтов.
- Генератор валидных PDF-документов с нуля (`create-sample`).
- Дамп структуры объектов и таблицы перекрестных ссылок (xref).

## Использование
```bash
# Создать тестовый PDF-файл
python toolkit.py create-sample sample.pdf

# Инспекция и анализ PDF-файла
python toolkit.py info sample.pdf

# Быстрый запуск из releases:
./releases/python-pdf-toolkit.bat
```
