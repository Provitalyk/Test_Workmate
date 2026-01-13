import argparse
from tabulate import tabulate
from report_generator import ReportGenerator


def main():
    # Создаём объект парсера
    parser = argparse.ArgumentParser(description="Генератор отчётов из CSV‑файлов.")
    
    # Добавляем аргумент --files: принимает несколько путей к CSV‑файлам
    parser.add_argument(
        '--files',
        nargs='+',         # Позволяет передать несколько значений (список файлов)
        required=True,    
        help="Пути к CSV‑файлам"    # Текст подсказки при вызове справки (-h)
    )
    
    # Добавляем аргумент --report: указывает тип отчёта
    parser.add_argument(
        '--report',
        type=str,           # Тип значения — строка
        required=True,
        help="Тип отчёта"   # Текст подсказки при вызове справки (-h)
    )
    
    # Парсим переданные аргументы командной строки
    args = parser.parse_args()
    
    try:
        # Создаём экземпляр генератора отчётов, передааем список файлов
        generator = ReportGenerator(args.files)
        
        # Загружаем данные из указанных CSV‑файлов
        generator.load_data()

        # Получаем данные отчёта заданного типа
        report_data = generator.get_report(args.report)

        # Выводим отчёт в консоль в виде таблицы с помощью библиотеки tabulate
        # headers="keys"  используем ключи словаря как заголовки столбцов
        # tablefmt="grid" формат таблицы с границами
        print(tabulate(report_data, headers="keys", tablefmt="grid"))

    except Exception as e:
        print(f"Ошибка: {e}")
        exit(1)

def test_main_with_mocked_args(mocker):
    # Тест: имитируем работу argparse подменяя метод parse_args
    # Возвращаем заранее заданные аргументы вместо реального парсинга командной строки
    mocker.patch('argparse.ArgumentParser.parse_args', return_value=...)

    # Имитируем вызов метода get_report у ReportGenerator
    # Возвращаем заготовленный результат вместо реальной генерации отчёта
    mocker.patch('report_generator.ReportGenerator.get_report', return_value=[...])

def test_empty_csv():
    # Тест: проверяем обработку пустого CSV‑файла
    # Создаём генератор отчётов с указанием пустого файла
    generator = ReportGenerator(['empty.csv'])

    # Загружаем данные из файла
    generator.load_data()

    # Проверяем, что после загрузки данных список data пуст
    assert len(generator.data) == 0


if __name__ == "__main__":
    main()
