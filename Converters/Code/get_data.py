import importlib.util
import sys
from pathlib import Path
import re


class TransitionManager:
    """
    Класс TransitionManager предназначен для управления состояниями и переходами в системе.
    Он включает в себя динамическую подгрузку недостающих модулей, классификацию данных
    и автоматическое создание файлов и папок на основе структуры данных.

    Атрибуты:
        states (list): Список состояний.
        transitions (list): Список переходов между состояниями.
        screen (str): Название экрана, используемого в системе (если указано в state_map).

    Методы:
        load_state_map(module_path): Загружает данные из файла state_map.
        load_missing_dependencies(module_path): Находит и подгружает недостающие зависимости.
        classify_and_generate_files(data): Классифицирует данные и генерирует структуру файлов.
        collect_strings_by_key(data_list, key): Собирает уникальные строки по ключу.
        generate_transition_methods(target, key): Генерирует методы для переходов по ключу.
        save(key, path): Сохраняет сгенерированные файлы в указанную директорию.
    """

    def __init__(self, module_path=None):
        """Инициализирует TransitionManager и загружает state_map, если указан путь."""
        self.states = []
        self.transitions = []
        self.screen = None

        if module_path:
            self.load_state_map(module_path)

    def load_state_map(self, module_path):
        """Загружает модуль state_map из указанного пути и извлекает состояния и переходы."""
        self.load_missing_dependencies(module_path)
        module_dir = str(Path(module_path).parent)
        sys.path.insert(0, module_dir)

        try:
            spec = importlib.util.spec_from_file_location("state_map", module_path)
            state_map = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(state_map)

            self.states = [item['name'] for item in state_map.states]

            self.transitions = state_map.transitions
            self.screen = getattr(state_map, 'screen', None)

        except ModuleNotFoundError as e:
            print(f"Ошибка импорта: {e}")

        finally:
            sys.path.pop(0)

    def load_missing_dependencies(self, module_path):
        """Находит и подгружает недостающие модули, указанные в импортах файла."""
        module_dir = Path(module_path).parent

        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()

        imports = re.findall(r'from (\S+) import', content)

        for imp in imports:
            imp_path = module_dir / Path(imp.replace('.', '/'))
            if imp_path.exists() and imp_path.is_dir():
                sys.path.insert(0, str(module_dir.parent))
                break

    def classify_and_generate_files(self):
        """Классифицирует данные и генерирует структуру файлов на основе состояний."""
        # Пример классификации данных (по желанию, здесь можно уточнить логику)
        db_classes = {}
        cmd_classes = []
        cnf_classes = {}

        for item in self.states:
            parts = item.split('_')
            action = parts[0]
            data_type = parts[1] if len(parts) > 1 else None
            target = parts[2] if len(parts) > 2 else None
            if (self.__check_unique_operations(item, db_classes) or
                    self.__check_unique_operations(item, cmd_classes) or
                    self.__check_unique_operations(item, cnf_classes)):
                continue
            if action == "cmd":
                cmd_classes.append(item)
            elif action in ("read", "write") and data_type in ("db", "cnf"):
                if target:

                    class_name = target.capitalize()
                    if data_type == "db":
                        db_classes.setdefault(class_name, []).append((action, item))
                    elif data_type == "cnf":
                        cnf_classes.setdefault(class_name, []).append((action, item))

        self.db_classes = db_classes
        self.cmd_classes = cmd_classes
        self.cnf_classes = cnf_classes
        return db_classes, cmd_classes, cnf_classes

    def __check_unique_operations(self, func_name: str, permission_dict) -> bool:
        found = False  # Флаг, чтобы отследить, если значение найдено хотя бы один раз

        if isinstance(permission_dict, dict):
            # Обрабатываем если permission_dict - это словарь
            for group, permissions in permission_dict.items():
                for permission in permissions:
                    if permission[1] == func_name:
                        if found:
                            return False  # Если уже нашли, значит значение не уникально
                        found = True  # Устанавливаем флаг, что значение найдено

        elif isinstance(permission_dict, list):
            # Обрабатываем если permission_dict - это список
            for permission in permission_dict:
                if permission[1] == func_name:
                    if found:
                        return False  # Если уже нашли, значит значение не уникально
                    found = True  # Устанавливаем флаг, что значение найдено

        return found  # Если нашли только один раз, возвращаем True (уникально), иначе False


    def save(self, key, path):
        """Сохраняет сгенерированные файлы в указанную директорию на основе ключа."""
        db_classes, cmd_classes, cnf_classes = self.classify_and_generate_files()

        if key == "db":
            self._generate_db_classes(path, db_classes)
        elif key == "cmd":
            self._generate_cmd_classes(path, cmd_classes)
        elif key == "cnf":
            self._generate_cnf_classes(path, cnf_classes)

    def _generate_db_classes(self, db_dir, db_classes):
        """Создает классы для работы с базой данных, сгруппированные по таблицам."""
        db_dir.mkdir(parents=True, exist_ok=True)

        for class_name, actions in db_classes.items():  # db_classes = set(db_classes)
            file_path = db_dir / f"{class_name.lower()}.py"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"from sqlalchemy.orm import Session\n\n")
                f.write(f"class {class_name}:\n")
                f.write(f"    \"\"\"Класс для работы с таблицей {class_name.lower()} в базе данных\"\"\"\n\n")

                for action, method_name in actions:
                    if action == "read":
                        f.write(f"    def read_{class_name.lower()}(self, session: Session):\n")
                        f.write(f"        \"\"\"Чтение данных из таблицы {class_name.lower()}\"\"\"\n")
                        f.write(f"        pass\n\n")
                    elif action == "write":
                        f.write(f"    def write_{class_name.lower()}(self, session: Session, data):\n")
                        f.write(f"        \"\"\"Запись данных в таблицу {class_name.lower()}\"\"\"\n")
                        f.write(f"        pass\n\n")

    def _generate_cmd_classes(self, cmd_dir, cmd_classes):
        """Создает классы для команд системы."""
        cmd_dir.mkdir(parents=True, exist_ok=True)

        for cmd in cmd_classes:
            class_name = cmd.split('_')[1].capitalize()
            file_path = cmd_dir / f"{class_name.lower()}.py"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"class {class_name}:\n")
                f.write(f"    \"\"\"Класс для выполнения команды {cmd}\"\"\"\n\n")
                f.write(f"    def execute(self):\n")
                f.write(f"        \"\"\"Выполняет команду {cmd}\"\"\"\n")
                f.write(f"        pass\n\n")

    def _generate_cnf_classes(self, cnf_dir, cnf_classes):
        """Создает классы для работы с конфигурацией, сгруппированные по параметрам."""
        cnf_dir.mkdir(parents=True, exist_ok=True)

        for class_name, actions in cnf_classes.items():  #
            file_path = cnf_dir / f"{class_name.lower()}.py"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"class {class_name}:\n")
                f.write(f"    \"\"\"Класс для работы с параметрами конфигурации {class_name.lower()}\"\"\"\n\n")

                for action, method_name in actions:
                    if action == "read":
                        f.write(f"    def read_{class_name.lower()}(self):\n")
                        f.write(f"        \"\"\"Чтение параметров {class_name.lower()}\"\"\"\n")
                        f.write(f"        pass\n\n")
                    elif action == "write":
                        f.write(f"    def write_{class_name.lower()}(self, config_data):\n")
                        f.write(f"        \"\"\"Запись параметров {class_name.lower()}\"\"\"\n")
                        f.write(f"        pass\n\n")

    def collect_strings_by_key(self, data_list, key):
        """Собирает уникальные строки, содержащие заданный ключ."""
        return set(item for item in data_list if key.lower() in item.lower())

    def generate_transition_methods(self, target, key):
        """Генерирует методы для переходов, содержащих ключ в target."""
        return set(
            f"def transition_{transition['trigger']}(self):\n    pass\n"
            for transition in self.find_transitions_by_source(target)
            if key in transition['trigger']
        )

    def find_transitions_by_source(self, source):
        """Находит переходы для заданного источника."""
        return [transition for transition in self.transitions if transition['source'] == source]

    def collect_strings_not_key(self, data_list, key):
        """Собирает строки, которые не содержат указанный ключ."""
        filtered_items = []  # Создаём пустое множество для хранения отфильтрованных элементов

        # Цикл для фильтрации элементов
        for item in data_list:
            if key.lower() not in item.lower():  # Проверяем, содержится ли ключ в элементе
                filtered_items.append(item)  # Если не содержится, добавляем элемент в множество

        return set(filtered_items)
        # return set(item for item in data_list if key.lower() not in item['name'].lower())

    def group_by_first_key(self, data_list):
        """Группирует элементы списка по первому элементу ключа."""
        groups = {}
        for item in data_list:
            first_key = item.split('_')[0]
            if first_key not in groups:
                groups[first_key] = []
            groups[first_key].append(item)
        return groups


# Пример использования TransitionManager
if __name__ == "__main__":
    # Путь к файлу state_map.py
    module_path = Path(r"G:\lesson\Urban_university\diplom_project\doc\code\state_map.py")
    # Путь к директории сохранения классов команд
    cmd_path = Path(r"G:\lesson\Urban_university\diplom_project\doc\code\cmdHelper")
    # Путь к директории сохранения классов для работы с базой данных
    db_engine_path = Path(r"G:\lesson\Urban_university\diplom_project\doc\code\dbEngine")
    # Путь к директории сохранения классов для работы с конфигурацией
    cnf_engine_path = Path(r"G:\lesson\Urban_university\diplom_project\doc\code\cnfEngine")
    # Создание экземпляра TransitionManager с загрузкой данных из state_map
    manager = TransitionManager(module_path=module_path)

    # Параметры для методов
    key = "btn_"
    target = "trigger"  # Варианты: source, trigger, dest

    # Выполнение методов и вывод результатов
    found_strings = manager.group_by_first_key(manager.states)
    found_trigger_methods = manager.generate_transition_methods(target, key)
    collect_methods = manager.collect_strings_not_key(manager.states, "screen_")

    # Классификация данных и генерация структур классов
    manager.classify_and_generate_files()
    # Создание директорий и сохранение файлов с классами.
    manager.save(key="db", path=db_engine_path)
    manager.save(key="cmd", path=cmd_path)
    manager.save(key="cnf", path=cnf_engine_path)
