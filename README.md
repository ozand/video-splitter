# Video Splitter

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![UV](https://img.shields.io/badge/package%20manager-UV-red.svg)](https://github.com/astral-sh/uv)

Скрипт для автоматической нарезки видео на основе таблицы в формате Markdown.

## 🚀 Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/ozand/video-splitter.git
cd video-splitter

# Установка зависимостей с UV
uv venv && uv pip install ffmpeg-python pandas click

# Запуск
uv run python main.py -t table.md -v videos/ -o output/
```

## ✨ Возможности

- 📋 **Умный парсинг** markdown таблиц с гибким форматом
- ✂️ **Точная нарезка** видео с помощью ffmpeg  
- 🔍 **Автопоиск** видеофайлов в папках и подпапках
- ⚡ **Быстрая установка** с менеджером пакетов UV
- 🧪 **Покрытие тестами** для надежности
- 📊 **Подробная статистика** обработки

## 📋 Поддерживаемые форматы

- **Видео**: MP4, AVI, MOV, MKV, WMV, FLV, WebM
- **Время**: MM:SS и HH:MM:SS  
- **Таблицы**: Markdown с любым количеством столбцов

## Установка

### Предварительные требования

1. **Python 3.12+**
2. **UV** - быстрый пакетный менеджер Python:
   ```bash
   # Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Или через pip
   pip install uv
   ```

3. **FFmpeg** - для работы с видео:
   - Windows: скачайте с https://ffmpeg.org/download.html или используйте `winget install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` (Ubuntu/Debian) или аналогичный пакетный менеджер

### Установка зависимостей

```bash
# Синхронизация зависимостей (рекомендуется)
uv sync

# Или установка в текущую среду
uv pip install -e .
```

## Использование

```bash
# Через uv run (рекомендуется)
uv run python main.py --table путь/к/таблице.md --videos путь/к/папке/с/видео --output путь/к/папке/результатов

# Или если установили через pip
python main.py --table путь/к/таблице.md --videos путь/к/папке/с/видео --output путь/к/папке/результатов
```

### Параметры:
- `--table` или `-t`: Путь к файлу Markdown с таблицей
- `--videos` или `-v`: Путь к папке с исходными видеофайлами  
- `--output` или `-o`: Путь к папке для сохранения нарезанных сцен

### Пример:
```bash
# С использованием uv (рекомендуется)
uv run python main.py -t "таблица.md" -v "C:\Videos\Source" -o "C:\Videos\Output"

# Или без uv
python main.py -t "таблица.md" -v "C:\Videos\Source" -o "C:\Videos\Output"
```

## Формат таблицы

Таблица должна содержать следующие столбцы:
- **Название сцены (ID)** - ID сцены в обратных кавычках (например, `SCENE_01.1`)
- **Название файла источника** - имя видеофайла
- **Время начала (в источнике)** - время начала в формате MM:SS или HH:MM:SS
- **Время конца (в источнике)** - время окончания в формате MM:SS или HH:MM:SS

### Пример таблицы:
```markdown
| Блок | Сцена в ролике | Название сцены (ID) | Название файла источника | Время начала (в источнике) | Время конца (в источнике) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Вступление**| 1 | `SCENE_01.1` | `Moscow_Russia_Aerial_Drone_4K.mp4` | 02:29 | 02:34 |
| | 1 | `SCENE_01.2` | `Russia_in_4K.mp4` | 06:46 | 06:51 |
```

## Функции

- **Автоматический поиск видеофайлов**: Скрипт ищет файлы по точному имени, без расширения, и рекурсивно по папкам
- **Поддержка различных форматов времени**: MM:SS и HH:MM:SS
- **Обработка ошибок**: Подробные сообщения об ошибках и пропуск проблемных файлов
- **Статистика**: Отчет о количестве успешно обработанных и проблемных файлов
- **Поддержка различных видеоформатов**: mp4, avi, mov, mkv, wmv, flv, webm

## Требования к системе

- Python 3.12+
- ffmpeg (установлен в системе)
- Достаточно места на диске для выходных файлов

## Разработка

### Установка dev зависимостей

```bash
# Синхронизация с dev зависимостями
uv sync --dev

# Или добавление новых dev зависимостей
uv add --dev pytest black isort
```

### Запуск тестов

```bash
uv run pytest
```

### Форматирование кода

```bash
uv run black .
uv run isort .
```

### Быстрые команды разработки

```bash
# Запуск скрипта в dev режиме
uv run python main.py --help

# Добавление новой зависимости
uv add новая-библиотека

# Обновление зависимостей
uv sync --upgrade
```