import csv
from collections import defaultdict
from typing import List, Dict, Any


class ReportGenerator:
    def __init__(self, file_paths: List[str]):
        """
        Инициализация генератора отчётов.

        :param file_paths: список путей к CSV‑файлам
        """
        self.file_paths = file_paths
        self.data = []

    def load_data(self) -> None:
        """Загрузить данные из всех CSV‑файлов."""
        for file_path in self.file_paths:
            try:
                with open(file_path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.data.append(row)
            except FileNotFoundError:
                raise FileNotFoundError(f"Файл не найден: {file_path}")
            except Exception as e:
                raise Exception(f"Ошибка при чтении файла {file_path}: {e}")

    def generate_performance_report(self) -> List[Dict[str, Any]]:
        """Сформировать отчёт по performance."""
        position_stats = defaultdict(list)
        for row in self.data:
            position = row['position']
            performance = float(row['performance'])
            position_stats[position].append(performance)

        report = []
        for position, performances in position_stats.items():
            avg_performance = sum(performances) / len(performances)
            report.append({
                'position': position,
                'average_performance': round(avg_performance, 2)
            })

        # Сортировка по убыванию
        report.sort(key=lambda x: x['average_performance'], reverse=True)
        return report

    def get_report(self, report_type: str) -> List[Dict[str, Any]]:
        """Получить отчёт заданного типа."""
        if report_type == 'performance':
            return self.generate_performance_report()
        else:
            raise ValueError(f"Неизвестный тип отчёта: {report_type}")
