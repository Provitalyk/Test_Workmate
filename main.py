import argparse
from tabulate import tabulate
from report_generator import ReportGenerator


def main():
    parser = argparse.ArgumentParser(description="Генератор отчётов из CSV‑файлов.")
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help="Пути к CSV‑файлам"
    )
    parser.add_argument(
        '--report',
        type=str,
        required=True,
        help="Тип отчёта"
    )

    args = parser.parse_args()

    try:
        generator = ReportGenerator(args.files)
        generator.load_data()
        report_data = generator.get_report(args.report)

        # Вывод в консоль через tabulate
        print(tabulate(report_data, headers="keys", tablefmt="grid"))

    except Exception as e:
        print(f"Ошибка: {e}")
        exit(1)


def test_main_with_mocked_args(mocker):
    mocker.patch('argparse.ArgumentParser.parse_args', return_value=...)
    mocker.patch('report_generator.ReportGenerator.get_report', return_value=[...])


def test_empty_csv():
    generator = ReportGenerator(['empty.csv'])
    generator.load_data()
    assert len(generator.data) == 0


if __name__ == "__main__":
    main()