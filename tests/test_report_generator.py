import argparse
import pytest
import tempfile
import csv
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from report_generator import ReportGenerator


@pytest.fixture
def sample_csv_data():
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
    """Создаем временный CSV‑файл для тестов."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sample_csv_data[0].keys())
        writer.writeheader()
        writer.writerows(sample_csv_data)
        return f.name


def test_load_data(create_temp_csv, sample_csv_data):
    generator = ReportGenerator([create_temp_csv])
    generator.load_data()
    assert len(generator.data) == len(sample_csv_data)


def test_generate_performance_report():
    generator = ReportGenerator([])
    generator.data = [
        {'position': 'DevOps', 'performance': '4.9'},
        {'position': 'DevOps', 'performance': '4.7'},
        {'position': 'QA', 'performance': '4.5'}
    ]
    report = generator.generate_performance_report()
    assert len(report) == 2
    assert report[0]['position'] == 'DevOps'
    assert report[0]['average_performance'] == 4.8
    assert report[1]['position'] == 'QA'
    assert report[1]['average_performance'] == 4.5


def test_get_report_invalid_type():
    generator = ReportGenerator([])
    with pytest.raises(ValueError, match="Неизвестный тип отчёта: unknown"):
        generator.get_report('unknown')


def test_file_not_found():
    generator = ReportGenerator(['non_existent.csv'])
    with pytest.raises(FileNotFoundError, match="Файл не найден: non_existent.csv"):
        generator.load_data()


def test_empty_csv():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, newline='', encoding='utf-8') as f:
        f.write('name,position,completed_tasks,performance,skills,team,experience_years\n')
        empty_file = f.name
    generator = ReportGenerator([empty_file])
    generator.load_data()
    assert len(generator.data) == 0


def test_main_with_mocked_args(mocker):
    """Тест main() с мокированными аргументами и чтением файла."""
    mocker.patch(
        'argparse.ArgumentParser.parse_args',
        return_value=argparse.Namespace(
            files=['dummy.csv'],
            report='performance'
        )
    )
    mocked_open = mocker.patch(
        'builtins.open',
        mocker.mock_open(read_data='name,position\nAlice,Dev')
    )
    mock_get_report = mocker.patch(
        'report_generator.ReportGenerator.get_report',
        return_value=[
            {'position': 'Test', 'average_performance': 5.0}
        ]
    )
                             # Импортируем main из main.py
    from main import main
    from io import StringIO
    import sys
    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        main()
    finally:
        sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    assert 'Test' in output
    assert '5' in output
    mock_get_report.assert_called_once_with('performance')
    mocked_open.assert_called_once_with('dummy.csv', mode='r', encoding='utf-8')
