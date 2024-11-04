# main.py
import argparse
import os
from pathlib import Path

from Analyzers.Architecture import ProjectAnalyzer
from Converters.Code.get_data import TransitionManager
from Converters.MentalMap.JSONToMindMapConverter import JSONToMindMapConverter
from Converters.UX.Converter import UXConverter


def main():
    parser = argparse.ArgumentParser(description="Podmasterye - инструмент автоматизации разработки.")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Подкоманда для анализа проекта
    analyze_parser = subparsers.add_parser("analyze", help="Анализ архитектуры проекта")
    analyze_parser.add_argument("project_path", type=str, help="Путь к корневой директории проекта")
    analyze_parser.add_argument("--ignore", nargs="*", default=['.venv', '.gitignore', '.idea'],
                                help="Игнорируемые элементы")

    # Подкоманда для конвертации UX в UI
    ux_convert_parser = subparsers.add_parser("ux_to_ui", help="Конвертация UX файла в UI")
    ux_convert_parser.add_argument("ux_path", type=str, help="Путь к UX файлу .bmpr")
    ux_convert_parser.add_argument("output_path", type=str, help="Директория для сохранения UI файлов")

    # Подкоманда для генерации переходов
    transition_parser = subparsers.add_parser("generate_transitions", help="Генерация переходов из state_map")
    transition_parser.add_argument("module_path", type=str, help="Путь к файлу state_map.py")
    transition_parser.add_argument("output_path", type=str,
                                   help="Директория для сохранения файлов сгенерированных классов")
    transition_parser.add_argument("--key", type=str, default="default", help="Ключ для генерации")

    # Подкоманда для конвертации JSON в ментальную карту
    json_to_mm_parser = subparsers.add_parser("json_to_mm", help="Конвертация JSON в mind map")
    json_to_mm_parser.add_argument("json_path", type=str, help="Путь к JSON файлу")
    json_to_mm_parser.add_argument("output_path", type=str, help="Путь для сохранения mind map файла")

    args = parser.parse_args()

    if args.command == "analyze":
        analyzer = ProjectAnalyzer(root_directory=args.project_path, ignore_list=args.ignore)
        analyzer.get_architecture()
        analyzer.print_architecture()

    elif args.command == "ux_to_ui":
        converter = UXConverter(db_path=args.ux_path)
        converter.bmpr_to_ui()
        converter.save_ui(args.output_path)

    elif args.command == "generate_transitions":
        module_path = Path(args.module_path)
        output_path = Path(args.output_path)
        manager = TransitionManager(module_path=module_path)
        manager.classify_and_generate_files()
        manager.save(project_path=output_path)

    elif args.command == "json_to_mm":
        with open(args.json_path, 'r', encoding='utf-8') as f:
            json_data = f.read()
        converter = JSONToMindMapConverter(json_data)
        converter.convert()
        converter.save_to_file(args.output_path)


if __name__ == "__main__":
    main()
