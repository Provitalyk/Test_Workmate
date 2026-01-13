import csv
from collections import defaultdict
from typing import List, Dict, Any


class ReportGenerator:
    def __init__(self, file_paths: List[str]):
        """
        Инициализация генератора отчётов
        Параметр file_paths: список путей к CSV‑файлам
        """
        # Сохраняем список путей к CSV‑файлам, переданный при создании объекта
        self.file_paths = file_paths
        
        # Инициализируем пустой список для хранения данных из файлов
        self.data = []

    def load_data(self) -> None:
        """Загрузить данные из всех CSV‑файлов"""
        # Проходим по каждому пути к файлу из списка
        for file_path in self.file_paths:
            try:
                # Открываем файл в режиме чтения с кодировкой UTF‑8
                with open(file_path, mode='r', encoding='utf-8') as f:

                    # Создаём объект DictReader для чтения CSV в виде словарей
                    reader = csv.DictReader(f)

                    # Проходим по каждой строке (записи) в файле
                    for row in reader:
                        # Добавляем текущую строку (словарь) в общий список
                        self.data.append(row)
            except FileNotFoundError:
                raise FileNotFoundError(f"Файл не найден: {file_path}")
            except Exception as e:
                raise Exception(f"Ошибка при чтении файла {file_path}: {e}")

    def generate_performance_report(self) -> List[Dict[str, Any]]:
        """Сформировать отчёт по performance"""
        # Создаём словарь со значениями по умолчанию список для группировки данных по позициям
        position_stats = defaultdict(list)

        # Проходим по всем строкам из CSV файла
        for row in self.data:

            # Получаем значение поля position из текущей строки
            position = row['position']

            # Преобразуем значение поля performance в число с плавающей точкой
            performance = float(row['performance'])

             # Добавляем показатель производительности в список для соответствующей позиции
            position_stats[position].append(performance)

        # Пустой список для итогового отчёта
        report = []

        # Проходим по всем позициям и соответствующим спискам показателей производительности
        for position, performances in position_stats.items():
            
            # Вычисляем среднее значение производительности для позиции
            avg_performance = sum(performances) / len(performances)

            # Добавляем в отчёт словарь с позицией и средним показателем округлённым до 2 знаков
            report.append({
                'position': position,
                'average_performance': round(avg_performance, 2)
            })

        # Сортируем отчёт по среднему показателю производительности в порядке убывания
        report.sort(key=lambda x: x['average_performance'], reverse=True)

        # Возвращаем сформированный отчёт
        return report

    def get_report(self, report_type: str) -> List[Dict[str, Any]]:
        """Получить отчёт заданного типа"""
        # Если запрошен отчёт типа performance вызываем соответствующий метод
        if report_type == 'performance':
            return self.generate_performance_report()
        else:
            raise ValueError(f"Неизвестный тип отчёта: {report_type}")
