import argparse
import pytest
import tempfile
import csv
import sys
from pathlib import Path
from report_generator import ReportGenerator


# Добавляем в системный путь родительскую директорию текущего файла,
# чтобы можно было импортировать модули
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def sample_csv_data():
    """
    Возвращает образец данных для тестирования в формате списка словарей
    Каждый словарь соответствует одной строке CSV‑файла
    """
    return [
        {
            'name': 'Alex Ivanov',
            'position': 'Backend Developer',
            'completed_tasks': '45',
            'performance': '4.8',
            'skills': 'Python, Django, PostgreSQL, Docker',
            'team': 'API Team',
            'experience_years': '5'
        },
        {
            'name': 'Maria Petrova',
            'position': 'Frontend Developer',
            'completed_tasks': '38',
            'performance': '4.7',
            'skills': 'React, TypeScript, Redux, CSS',
            'team': 'Web Team',
            'experience_years': '4'
        }
    ]

@pytest.fixture
def create_temp_csv(sample_csv_data):
    """
    Создаёт временный CSV‑файл для тестов на основе переданных данных
    sample_csv_data данные для записи в CSV (из sample_csv_data)
    return путь к созданному временному файлу
    """
    # Создаём временный файл в режиме записи с отключением автоматического удаления
    with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8') as f:

        # Создаём объект DictWriter для записи словарей в CSV
        writer = csv.DictWriter(f, fieldnames=sample_csv_data[0].keys())
        
        # Записываем заголовки столбцов (ключи первого словаря)
        writer.writeheader()
        
        # Записываем все строки данных
        writer.writerows(sample_csv_data)

        # Возвращаем имя (путь) созданного файла
        return f.name

def test_load_data(create_temp_csv, sample_csv_data):
    """
    Проверяет загрузку данных из CSV‑файла в объект ReportGenerator
    create_temp_csv путь к временному CSV‑файлу 
    sample_csv_data исходные данные для сравнения
    """
    # Создаём экземпляр генератора отчётов с путём к временному файлу
    generator = ReportGenerator([create_temp_csv])

    # Загружаем данные из файла
    generator.load_data()

    # Проверяем, что количество загруженных записей совпадает с исходными данными
    assert len(generator.data) == len(sample_csv_data)

def test_generate_performance_report():
    """
    Проверяет формирование отчёта по производительности performance
    Использует искусственные данные без реального файла
    """
    # Создаём генератор отчётов без файлов данные добавляем сами
    generator = ReportGenerator([])

    # Вручную заполняем данные для тестирования
    generator.data = [
        {'position': 'DevOps', 'performance': '4.9'},
        {'position': 'DevOps', 'performance': '4.7'},
        {'position': 'QA', 'performance': '4.5'}
    ]
    # Генерируем отчёт
    report = generator.generate_performance_report()

    # Проверяем количество позиций в отчёте (2: DevOps и QA)
    assert len(report) == 2

    # Проверяем первую позицию DevOps и среднее значение 4.8
    assert report[0]['position'] == 'DevOps'
    assert report[0]['average_performance'] == 4.8

    # Проверяем вторую позицию QA и среднее значение 4.5
    assert report[1]['position'] == 'QA'
    assert report[1]['average_performance'] == 4.5

def test_get_report_invalid_type():
    """
    Проверяет обработку некорректного типа отчёта в методе get_report
    Ожидаем исключение ValueError с конкретным сообщением
    """
    # Создаём генератор отчётов без файлов
    generator = ReportGenerator([])

    # Проверяем, что при запросе неизвестного типа отчёта поднимается ValueError
    with pytest.raises(ValueError, match="Неизвестный тип отчёта: unknown"):
        generator.get_report('unknown')

def test_file_not_found():
    """
    Проверяет обработку ошибки отсутствия файла в методе load_data
    Ожидаем исключение FileNotFoundError с конкретным сообщением
    """
    # Создаём генератор отчётов с несуществующим файлом
    generator = ReportGenerator(['non_existent.csv'])

    # Проверяем, что при загрузке данных поднимается FileNotFoundError
    with pytest.raises(FileNotFoundError, match="Файл не найден: non_existent.csv"):
        generator.load_data()

def test_empty_csv():
    """
    Проверяет обработку пустого CSV‑файла только заголовки, без данных
    """
    # Создаём временный файл с заголовками
    with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8') as f:
        f.write('name,position,completed_tasks,performance,skills,team,experience_years\n')
        empty_file = f.name    # Сохраняем путь к файлу

    # Создаём генератор отчётов с этим файлом
    generator = ReportGenerator([empty_file])

    # Загружаем данные
    generator.load_data()

    # Проверяем, что список данных пуст нет строк с данными
    assert len(generator.data) == 0

def test_main_with_mocked_args(mocker):
    """
    Имитирует запуск функции main() с моками (подменёнными объектами)
    Проверяет корректность вызовов и вывода при эмуляции аргументов командной строки
    """
    # Подменяем метод parse_args у ArgumentParser, возвращая заранее заданные аргументы
    mocker.patch(
        'argparse.ArgumentParser.parse_args',
        return_value=argparse.Namespace(
            files=['dummy.csv'],
            report='performance'
        )
    )
    # Подменяем встроенную функцию open имитируя чтение файла с данными
    mocked_open = mocker.patch(
        'builtins.open',
        mocker.mock_open(read_data='name,position\nAlice,Dev')
    )
    # Подменяем метод get_report у ReportGenerator возвращая заготовленный отчёт
    mock_get_report = mocker.patch(
        'report_generator.ReportGenerator.get_report',
        return_value=[
            {'position': 'Test', 'average_performance': 5.0}
        ]
    )
    # Импортируем main из main.py
    from main import main
    # Для перехвата вывода в консоль используем StringIO
    from io import StringIO
    import sys

    
    captured_output = StringIO()    # Перенаправляем stdout в StringIO
    sys.stdout = captured_output
    try:
        main()                 # Запуск тест функции
    finally:
        sys.stdout = sys.__stdout__     # Восстанавливаем стандартный stdout

    # Получаем захваченный вывод
    output = captured_output.getvalue()

    # Проверяем наличие ожидаемых значений в выводе
    assert 'Test' in output
    assert '5' in output

    # Проверяем, что метод get_report был вызван один раз с аргументом performance
    mock_get_report.assert_called_once_with('performance')

     # Проверяем, что open был вызван один раз с ожидаемыми параметрами
    mocked_open.assert_called_once_with('dummy.csv', mode='r', encoding='utf-8')
