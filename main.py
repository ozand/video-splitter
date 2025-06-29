import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
import ffmpeg
import click


def parse_time_to_seconds(time_str: str) -> float:
    """
    Преобразует время в формате MM:SS или HH:MM:SS в секунды
    """
    try:
        parts = time_str.split(':')
        if len(parts) == 2:  # MM:SS
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        elif len(parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
        else:
            raise ValueError(f"Неверный формат времени: {time_str}")
    except ValueError as e:
        raise ValueError(f"Ошибка парсинга времени '{time_str}': {e}")


def parse_markdown_table(table_content: str) -> List[Dict]:
    """
    Парсит markdown таблицу и извлекает нужные данные
    """
    lines = table_content.strip().split('\n')
    
    # Находим заголовок таблицы
    header_line = None
    for i, line in enumerate(lines):
        if 'Название файла источника' in line:
            header_line = i
            break
    
    if header_line is None:
        raise ValueError("Не найден заголовок таблицы с нужными столбцами")
    
    # Парсим заголовки (убираем пустые ячейки в начале и конце)
    header_cells = [h.strip() for h in lines[header_line].split('|')]
    headers = [h for h in header_cells if h]
    
    # Ищем индексы нужных столбцов
    scene_id_idx = None
    source_file_idx = None
    start_time_idx = None
    end_time_idx = None
    
    for i, header in enumerate(headers):
        if 'Название сцены' in header or 'ID' in header:
            scene_id_idx = i
        elif 'Название файла источника' in header:
            source_file_idx = i
        elif 'Время начала' in header:
            start_time_idx = i
        elif 'Время конца' in header:
            end_time_idx = i
    
    if None in [scene_id_idx, source_file_idx, start_time_idx, end_time_idx]:
        raise ValueError("Не найдены все необходимые столбцы в таблице")
    
    # Парсим строки данных (пропускаем заголовок и разделитель)
    data_rows = []
    for line in lines[header_line + 2:]:  # +2 чтобы пропустить заголовок и разделитель
        if line.strip() and '|' in line:
            # Получаем все ячейки, сохраняя пустые для правильного подсчета позиций
            all_cells = [cell.strip() for cell in line.split('|')]
            
            # Убираем только первую и последнюю пустые ячейки (обрамляющие |)
            if all_cells and not all_cells[0]:
                all_cells.pop(0)
            if all_cells and not all_cells[-1]:
                all_cells.pop()
            
            # Ищем данные по индексам, учитывая что пустые ячейки могут быть в середине
            scene_id = ""
            source_file = ""
            start_time = ""
            end_time = ""
            
            # Безопасно получаем значения по индексам
            if scene_id_idx < len(all_cells):
                scene_id = all_cells[scene_id_idx]
            if source_file_idx < len(all_cells):
                source_file = all_cells[source_file_idx]
            if start_time_idx < len(all_cells):
                start_time = all_cells[start_time_idx]
            if end_time_idx < len(all_cells):
                end_time = all_cells[end_time_idx]
            
            # Если не удалось найти по индексам, пытаемся найти по содержимому
            if not (scene_id and source_file and start_time and end_time):
                non_empty_cells = [c for c in all_cells if c]
                temp_scene_id = ""
                temp_source_file = ""
                temp_start_time = ""
                temp_end_time = ""
                
                for cell in non_empty_cells:
                    if re.search(r'`[^`]+`', cell):  # ID сцены в кавычках
                        if not temp_scene_id:
                            temp_scene_id = cell
                        elif cell.endswith('.mp4') or '.mp4' in cell:  # Видеофайл может быть в кавычках
                            if not temp_source_file:
                                temp_source_file = cell
                    elif re.search(r'\d{2}:\d{2}', cell):  # Время
                        if not temp_start_time:
                            temp_start_time = cell
                        elif not temp_end_time:
                            temp_end_time = cell
                    elif (cell.endswith('.mp4') or cell.endswith('.avi') or cell.endswith('.mov') or 
                          cell.endswith('.mkv') or cell.endswith('.wmv') or cell.endswith('.flv') or cell.endswith('.webm')):
                        if not temp_source_file:
                            temp_source_file = cell
                
                # Используем найденные значения, если основные пустые
                if not scene_id:
                    scene_id = temp_scene_id
                if not source_file:
                    source_file = temp_source_file
                if not start_time:
                    start_time = temp_start_time
                if not end_time:
                    end_time = temp_end_time
            
            # Извлекаем ID сцены из обратных кавычек
            scene_id_match = re.search(r'`([^`]+)`', scene_id)
            if scene_id_match:
                scene_id = scene_id_match.group(1)
            
            # Убираем обратные кавычки из имени файла, если они есть
            source_file_match = re.search(r'`([^`]+)`', source_file)
            if source_file_match:
                source_file = source_file_match.group(1)
            
            # Проверяем, что все поля заполнены
            if source_file and start_time and end_time and scene_id:
                data_rows.append({
                    'scene_id': scene_id,
                    'source_file': source_file,
                    'start_time': start_time,
                    'end_time': end_time
                })
    
    return data_rows


def find_video_file(source_filename: str, video_folder: Path) -> Optional[Path]:
    """
    Находит видеофайл в указанной папке
    """
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
    
    # Прямой поиск файла
    direct_path = video_folder / source_filename
    if direct_path.exists():
        return direct_path
    
    # Поиск без расширения (если расширение отличается)
    name_without_ext = Path(source_filename).stem
    for ext in video_extensions:
        candidate = video_folder / f"{name_without_ext}{ext}"
        if candidate.exists():
            return candidate
    
    # Поиск по всем файлам в папке
    for file_path in video_folder.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in video_extensions:
            if file_path.name == source_filename or file_path.stem == name_without_ext:
                return file_path
    
    return None


def cut_video_segment(input_path: Path, output_path: Path, start_time: str, end_time: str) -> bool:
    """
    Вырезает сегмент видео с помощью ffmpeg
    """
    try:
        start_seconds = parse_time_to_seconds(start_time)
        end_seconds = parse_time_to_seconds(end_time)
        duration = end_seconds - start_seconds
        
        if duration <= 0:
            print(f"⚠️  Неверный интервал времени: {start_time} - {end_time}")
            return False
        
        # Создаем выходную папку если её нет
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Выполняем нарезку видео
        (
            ffmpeg
            .input(str(input_path), ss=start_seconds)
            .output(str(output_path), t=duration, c='copy')
            .overwrite_output()
            .run(quiet=True)
        )
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обработке видео: {e}")
        return False


@click.command()
@click.option('--table', '-t', required=True, type=click.Path(exists=True), 
              help='Путь к файлу markdown с таблицей')
@click.option('--videos', '-v', required=True, type=click.Path(exists=True), 
              help='Путь к папке с исходными видеофайлами')
@click.option('--output', '-o', required=True, type=click.Path(), 
              help='Путь к папке для сохранения результатов')
def main(table, videos, output):
    """
    Скрипт для нарезки видео на основе таблицы в формате markdown
    """
    print("🎬 Запуск обработки видео...")
    
    # Преобразуем пути
    table_path = Path(table)
    videos_path = Path(videos)
    output_path = Path(output)
    
    # Создаем выходную папку
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        # Читаем таблицу
        print(f"📋 Чтение таблицы из {table_path}")
        with open(table_path, 'r', encoding='utf-8') as f:
            table_content = f.read()
        
        # Парсим таблицу
        scenes_data = parse_markdown_table(table_content)
        print(f"✅ Найдено {len(scenes_data)} сцен для обработки")
        
        # Обрабатываем каждую сцену
        success_count = 0
        error_count = 0
        
        for i, scene in enumerate(scenes_data, 1):
            print(f"\n🎯 Обработка сцены {i}/{len(scenes_data)}: {scene['scene_id']}")
            
            # Находим исходный видеофайл
            source_video = find_video_file(scene['source_file'], videos_path)
            if not source_video:
                print(f"❌ Не найден файл: {scene['source_file']}")
                error_count += 1
                continue
            
            print(f"📁 Найден файл: {source_video}")
            
            # Определяем выходной файл
            output_file = output_path / f"{scene['scene_id']}.mp4"
            
            # Вырезаем сегмент
            print(f"✂️  Нарезка: {scene['start_time']} - {scene['end_time']}")
            if cut_video_segment(source_video, output_file, scene['start_time'], scene['end_time']):
                print(f"✅ Готово: {output_file}")
                success_count += 1
            else:
                error_count += 1
        
        # Итоговая статистика
        print(f"\n📊 Обработка завершена:")
        print(f"✅ Успешно: {success_count}")
        print(f"❌ Ошибок: {error_count}")
        
        if success_count > 0:
            print(f"📁 Результаты сохранены в: {output_path}")
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
