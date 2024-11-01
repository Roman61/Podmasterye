# Файл Demiurge/Architecture/Analyzer.py предназначен для анализа структуры проекта, включая директории и файлы,
# а также для извлечения информации о классах, функциях и переменных из Python-скриптов.
# Этот модуль позволяет разработчикам получить представление о архитектуре их проекта и
# сохранить результаты анализа в формате JSON или XML.
# Основные классы
# ProjectAnalyzer
#
#     Назначение:
#     Класс ProjectAnalyzer отвечает за анализ проектной структуры, включая обход директорий,
#     извлечение информации о Python-файлах и сохранение архитектуры проекта в различных форматах.
#     Он помогает разработчикам визуализировать структуру проекта и анализировать его компоненты.
#
#     Основные атрибуты:
#         root_directory: Путь к корневой директории проекта, которая будет проанализирована.
#         ignore_list: Список элементов (файлов и директорий), которые необходимо игнорировать при анализе.
#         architecture: Словарь, который хранит информацию о структуре проекта, включая классы,
#         функции и переменные из файлов.
#
#     Основные методы:
#
#         __init__(self, root_directory: str = None, ignore_list: List[str] = None):
#         Конструктор, который инициализирует корневую директорию и список игнорируемых элементов.
#
#         find_project_root(self, start_path: str = '.') -> Union[str, None]: Метод,
#         который находит корневую директорию проекта, проверяя наличие определенных индикаторов
#         (например, .venv, requirements.txt и т.д.).
#
#         get_architecture(self) -> None: Метод, который запускает процесс обхода директорий и
#         извлечения информации о проекте, заполняя атрибут architecture.
#
#         traverse_directory(self, dir_path: str) -> Dict[str, Union[Dict, Dict[str, dict]]]:
#         Метод для обхода директории и сбора информации о файлах и поддиректориях.
#         Он вызывает метод file_analyzer для обработки Python-файлов.
#
#         file_analyzer(self, file_path: str) -> dict: Метод для анализа отдельного Python-файла,
#         извлекая информацию о классах, функциях и переменных, используя parse_python_file_details.
#
#         parse_python_file_details(self, file_path: str) -> tuple: Метод для извлечения деталей о классах,
#         функциях и переменных из Python-файла, используя модуль ast.
#
#         print_architecture(self, architecture: Dict = None, indent: int = 0) -> None:
#         Метод для печати структуры проекта в удобочитаемом виде.
#         Рекурсивно обходит словарь архитектуры и отображает директории и файлы с отступами.
#
#         _print_file_details(self, file_name: str, details: dict, indent_str: str) -> None:
#         Вспомогательный метод для печати деталей файла, включая классы, функции и переменные.
#
#         save_architecture_to_json(self, filename: str) -> None: Метод для сохранения структуры проекта в JSON-файл.
#
#         save_architecture_to_xml(self, filename: str) -> None: Метод для сохранения структуры проекта в XML-файл.
#
# Общая логика работы класса
#
#     При инициализации класса ProjectAnalyzer задается корневая директория и список игнорируемых элементов.
#     Метод get_architecture запускает анализ проекта, извлекая информацию о файлах и директориях.
#     Информация о классах, функциях и переменных извлекается из Python-файлов с
#     помощью методов parse_python_file_details и file_analyzer.
#     Архитектура проекта может быть выведена на экран, сохранена в JSON или XML формате для дальнейшего использования.
#
# Таким образом, Analyzer.py предоставляет мощный инструмент для анализа структуры Python-проектов,
# помогая разработчикам лучше понимать свою кодовую базу и её организацию.
#


import ast
import json
import os
from typing import Dict, List, Union
import xml.etree.ElementTree as ET


class ProjectAnalyzer:
    def __init__(self, root_directory: str = None, ignore_list: List[str] = None):
        self.root_directory = root_directory or self.find_project_root()
        self.ignore_list = ignore_list or []
        self.architecture = {}

    def find_project_root(self, start_path: str = '.') -> Union[str, None]:
        root_indicators = ['.venv', 'requirements.txt', 'pyproject.toml', '.git']
        current_path = os.path.abspath(start_path)

        while current_path:
            if any(os.path.exists(os.path.join(current_path, indicator)) for indicator in root_indicators):
                return current_path
            new_path = os.path.dirname(current_path)
            if new_path == current_path:  # Достигли корня
                break
            current_path = new_path
        return None

    def get_architecture(self) -> None:
        project_name = os.path.basename(self.root_directory)
        self.architecture[project_name] = self.traverse_directory(self.root_directory)

    def traverse_directory(self, dir_path: str) -> Dict[str, Union[Dict, Dict[str, dict]]]:
        file_tree = {}
        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)

            if item in self.ignore_list:
                continue

            if os.path.isdir(item_path):
                file_tree[item] = self.traverse_directory(item_path)
            else:
                if item.endswith('.py'):
                    file_tree[item] = self.file_analyzer(item_path)
                # Не обрабатываем не-Python файлы, такие как .txt, .md и т.д.

        return file_tree

    def file_analyzer(self, file_path: str) -> dict:
        classes, functions, variables = self.parse_python_file_details(file_path)
        return {
            'classes': classes,
            'functions': functions,
            'variables': variables
        }

    def parse_python_file(self, file_path: str) -> tuple:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                node = ast.parse(f.read(), filename=file_path)

            classes = [n.name for n in node.body if isinstance(n, ast.ClassDef)]
            functions = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            variables = [n.targets[0].id for n in node.body
                         if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)]
            return classes, functions, variables

        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            return [], [], []  # Возвращаем пустые списки в случае ошибки

    def parse_python_file_details(self, file_path: str) -> tuple:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                node = ast.parse(f.read(), filename=file_path)

            classes = []
            functions = []
            variables = []

            for item in node.body:
                if isinstance(item, ast.ClassDef):
                    # Собираем информацию о классе
                    class_info = {
                        'name': item.name,
                        'methods': [],
                        'fields': []
                    }

                    # Проходим по телу класса
                    for class_item in item.body:
                        if isinstance(class_item, ast.FunctionDef):
                            # Это метод класса
                            class_info['methods'].append(class_item.name)
                        elif isinstance(class_item, ast.Assign):
                            # Поле класса
                            for target in class_item.targets:
                                if isinstance(target, ast.Name):
                                    class_info['fields'].append(target.id)

                    classes.append(class_info)  # Добавляем информацию о классе

                elif isinstance(item, ast.FunctionDef):
                    # Это функция на уровне модуля
                    functions.append(item.name)
                elif isinstance(item, ast.Assign):
                    # Переменные на уровне модуля
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            variables.append(target.id)

            return classes, functions, variables

        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            return [], [], []  # Возвращаем пустые списки в случае ошибки

    def print_architecture(self, architecture: Dict = None, indent: int = 0) -> None:
        if architecture is None:
            architecture = self.architecture

        indent_str = "│  " * indent
        for folder, content in architecture.items():
            if isinstance(content, dict):
                print(f"{indent_str}├── {folder}/")
                self.print_architecture(content, indent + 1)
            else:  # Это файл с данными
                self._print_file_details(folder, content, indent_str)

    def _print_file_details(self, file_name: str, details: dict, indent_str: str) -> None:
        if details:
            flag = False
            print(f"{indent_str}├── {file_name}")
            for key in ['classes', 'functions', 'variables']:
                if key in details:  # Проверяем на наличие элементов через get
                    flag = True
                    print(f"{indent_str}│  ├── {key.capitalize()}: {', '.join(details[key])}")
            if not flag:
                for key in details:
                    print(f"{indent_str}│  ├── {key}")

    def save_architecture_to_json(self, filename: str) -> None:
        try:
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(self.architecture, json_file, ensure_ascii=False, indent=4)
            print(f"Architecture saved to {filename} in JSON format.")
        except Exception as e:
            print(f"Error saving architecture to JSON: {e}")

    def save_architecture_to_xml(self, filename: str) -> None:
        try:
            def build_xml_tree(data, parent):
                for key, value in data.items():
                    element = ET.SubElement(parent, key)
                    if isinstance(value, dict):
                        build_xml_tree(value, element)
                    else:
                        element.text = str(value)

            root = ET.Element('Architecture')
            build_xml_tree(self.architecture, root)

            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)
            print(f"Architecture saved to {filename} in XML format.")
        except Exception as e:
            print(f"Error saving architecture to XML: {e}")
            
            
class ProjectCreator:
    def __init__(self, architecture: Dict[str, Union[Dict, List[str]]] = None):
        self.architecture = architecture or {}
        self.current_path = ''

    def load_from_json(self, file_path: str):
        """Загружает архитектуру проекта из JSON файла."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.architecture = json.load(f)
                if len(self.architecture.items()) < 2:
                    temp = list(self.architecture.keys())
                    self.architecture = self.architecture[temp[0]]
            print(f"Project architecture loaded from {file_path}")
        except Exception as e:
            print(f"Error loading JSON file: {e}")

    def load_from_xml(self, file_path: str):
        """Загружает архитектуру проекта из XML файла."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            self.architecture = self._xml_to_dict(root)
            print(f"Project architecture loaded from {file_path}")
        except Exception as e:
            print(f"Error loading XML file: {e}")

    def _xml_to_dict(self, element):
        """Рекурсивно преобразует XML элемент в словарь."""
        result = {element.tag: {} if element.attrib else None}
        children = list(element)
        if children:
            dd = {}
            for child in children:
                child_dict = self._xml_to_dict(child)
                dd[child.tag] = child_dict[child.tag]
            result = {element.tag: dd}
        elif element.text:
            text = element.text.strip()
            result[element.tag] = text
        return result

    def create_project_structure(self, root_path: str = ""):
        if '\\' not in root_path:
            self.current_path = self.find_project_root()
            root_path = self.current_path
        """Создает структуру проекта на основе архитектуры."""
        for folder_name, contents in self.architecture.items():
            self._create_directory(root_path, folder_name, contents)

    def _create_directory(self, path, folder_name, contents):
        folder_path = os.path.join(path, folder_name)
        if '.' not in folder_name:
            os.makedirs(folder_path, exist_ok=True)
            for name, detail in contents.items():
                if '.' not in name:
                    self._create_directory(folder_path, name, detail)
                elif '.' in name:
                    self._create_python_file(folder_path, name, detail)
        elif '.' in folder_name:
            self._create_python_file(path, folder_name, contents)

    def _create_python_file(self, path, file_name, details):
        file_path = os.path.join(path, f"{file_name}")

        # Проверяем, существует ли файл
        if os.path.exists(file_path):
            print(f"Файл '{file_path}' уже существует. Игнорируем создание.")
            return

        # Если файл не существует, создаем его
        with open(file_path, 'w', encoding='utf-8') as f:
            if 'classes' in details:
                for class_info in details['classes']:
                    f.write(f"class {class_info['name']}:\n")
                    for method in class_info['methods']:
                        f.write(f"    def {method}(self):\n")
                        f.write("        pass\n\n")
            if 'functions' in details:
                for func in details['functions']:
                    f.write(f"def {func}():\n")
                    f.write("    pass\n\n")
            if 'variables' in details:
                for var in details['variables']:
                    f.write(f"{var} = None\n")

    def find_project_root(self, start_path: str = '.') -> Union[str, None]:
        root_indicators = ['.venv', 'requirements.txt', 'pyproject.toml', '.git']
        self.current_path = os.path.abspath(start_path)

        while self.current_path:
            if any(os.path.exists(os.path.join(self.current_path, indicator)) for indicator in root_indicators):
                return self.current_path
            new_path = os.path.dirname(self.current_path)
            if new_path == self.current_path:  # Достигли корня
                break
            self.current_path = new_path
        return None


# Пример использования
if __name__ == "__main__":
    ignored_items = ['.venv', '.gitignore', '.idea', 'inspectionProfiles']
    analyzer = ProjectAnalyzer(ignore_list=ignored_items)
    analyzer.get_architecture()

    # Сохраняем архитектуру в JSON и XML
    # analyzer.save_architecture_to_json('architecture.json')
    # analyzer.save_architecture_to_xml('architecture.xml')

    analyzer.print_architecture()
