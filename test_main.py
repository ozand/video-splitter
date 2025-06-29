import pytest
from main import parse_time_to_seconds, parse_markdown_table


def test_parse_time_to_seconds():
    """Тест функции парсинга времени"""
    # Тест формата MM:SS
    assert parse_time_to_seconds("02:30") == 150
    assert parse_time_to_seconds("00:05") == 5
    assert parse_time_to_seconds("10:45") == 645
    
    # Тест формата HH:MM:SS
    assert parse_time_to_seconds("01:02:30") == 3750
    assert parse_time_to_seconds("00:00:05") == 5
    assert parse_time_to_seconds("02:30:00") == 9000
    
    # Тест ошибок
    with pytest.raises(ValueError):
        parse_time_to_seconds("invalid")
    
    with pytest.raises(ValueError):
        parse_time_to_seconds("1:2:3:4")


def test_parse_markdown_table():
    """Тест функции парсинга markdown таблицы"""
    test_table = """
| Блок | Сцена в ролике | Название сцены (ID) | Название файла источника | Время начала (в источнике) | Время конца (в источнике) | Описание |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Вступление**| 1 | `SCENE_01.1` | Moscow_Russia_Aerial_Drone_4K.mp4 | 02:29 | 02:34 | Тест |
| | 1 | `SCENE_01.2` | Russia_in_4K.mp4 | 06:46 | 06:51 | Тест |
"""
    
    scenes = parse_markdown_table(test_table)
    
    assert len(scenes) == 2
    assert scenes[0]['scene_id'] == 'SCENE_01.1'
    assert scenes[0]['source_file'] == 'Moscow_Russia_Aerial_Drone_4K.mp4'
    assert scenes[0]['start_time'] == '02:29'
    assert scenes[0]['end_time'] == '02:34'
    
    assert scenes[1]['scene_id'] == 'SCENE_01.2'
    assert scenes[1]['source_file'] == 'Russia_in_4K.mp4'


if __name__ == "__main__":
    pytest.main([__file__])
