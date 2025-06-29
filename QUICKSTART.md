# Быстрый старт с UV

## Установка UV
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Или через pip
pip install uv
```

## Установка FFmpeg
```bash
# Windows
winget install ffmpeg

# Или скачайте с https://ffmpeg.org/download.html
```

## Быстрый запуск проекта

```bash
# Клонирование/переход в папку проекта
cd video_splitter

# Создание виртуального окружения
uv venv

# Установка зависимостей
uv pip install ffmpeg-python pandas click

# Запуск скрипта
uv run python main.py --table таблица.md --videos /путь/к/видео --output /путь/к/результатам
```

## Пример использования

```bash
# Обработка таблицы
uv run python main.py -t "таблица.md" -v "C:\Videos\Source" -o "C:\Videos\Output"
```

## Разработка

```bash
# Установка dev зависимостей
uv pip install pytest black isort

# Запуск тестов
uv run pytest

# Форматирование кода
uv run black .
uv run isort .
```

## Команды для разработчиков

```bash
# Добавление новой зависимости
uv add новая-библиотека

# Обновление зависимостей  
uv sync --upgrade

# Проверка окружения
uv pip list
```
