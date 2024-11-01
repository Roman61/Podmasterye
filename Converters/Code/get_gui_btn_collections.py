# Файл Demiurge/Converters/UI/QtDesigner/get_gui_btn_collections.py предназначен для поиска и
# сбора уникальных имен кнопок (объектов), начинающихся с префикса btn_, из Python файлов,
# которые представляют экраны или виджеты в приложении, созданном с помощью Qt Designer.
# Этот файл позволяет систематизировать интерфейсные элементы, что может быть полезно при дальнейшей работе с
# графическим интерфейсом.
# Назначение файла:
#
#     Поиск кнопок: Находит все уникальные имена объектов (кнопок), начинающиеся с btn_ в файлах,
#     имена которых начинаются с screen_ или widget_.
#     Систематизация: Возвращает словарь, в котором ключами являются имена файлов,
#     а значениями — списки уникальных кнопок, что упрощает доступ к этим элементам для дальнейшего анализа или работы.
#     Упрощение разработки: Помогает разработчикам получить обзор доступных кнопок в интерфейсах,
#     что может быть полезно при программировании логики взаимодействия.
#
# Классы в get_gui_btn_collections.py:
#
# Хотя данный файл представляет собой функциональный скрипт без классов,
# для улучшения структуры кода и возможности повторного использования можно предложить создание класса.
#
#     ButtonFinder
#         Методы:
#             __init__(self, folder_path): Конструктор, который принимает путь к папке для поиска файлов.
#             find_btn_objects(self): Метод для поиска всех уникальных названий кнопок в заданной папке.
#             extract_btn_names_from_file(self, file_path):
#             Метод для извлечения уникальных имен кнопок из конкретного файла.
#             format_results(self, btn_objects): Метод для форматирования результатов в удобный для вывода вид.
#
# Механизм работы:
#
#     Инициализация: При создании экземпляра ButtonFinder передается путь к папке, где будут искать файлы.
#     Поиск объектов: Метод find_btn_objects проходит по всем файлам в указанной папке и
#     вызывает метод extract_btn_names_from_file для каждого подходящего файла.
#     Извлечение имен: Метод extract_btn_names_from_file открывает файл, ищет строки, содержащие кнопки,
#     и возвращает список уникальных имен кнопок.
#     Вывод результата: В главном блоке (__main__) выводится словарь с именами файлов и
#     соответствующими кнопками в формате, удобном для чтения.
#
# Заключение:
#
# Этот файл способствует упрощению работы с графическими интерфейсами, систематизируя и
# собирая информацию о кнопках в приложениях, что может быть полезно для разработчиков,
# работающих с PyQt и Qt Designer.


import os


class ButtonFinder:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def find_btn_objects(self):
        btn_objects = {}
        for filename in os.listdir(self.folder_path):
            if (filename.startswith("screen_") or filename.startswith("widget_")) and filename.endswith(".py"):
                file_path = os.path.join(self.folder_path, filename)
                unique_btn_objects = self.extract_btn_names_from_file(file_path)
                if unique_btn_objects:
                    btn_objects[filename] = unique_btn_objects
        return btn_objects

    def extract_btn_names_from_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                unique_btn_objects = set()
                for line in file:
                    for word in line.split():
                        if "btn_" in word:
                            if word.startswith("btn_"):
                                unique_btn_objects.add(word)
                            else:
                                for subword in word.split("."):
                                    if subword.startswith("btn_"):
                                        unique_btn_objects.add(subword)
                return list(unique_btn_objects)
        except UnicodeDecodeError:
            print(f"Ошибка при чтении файла {os.path.basename(file_path)}. Пропускаем его.")
            return []


def find_btn_objects(folder_path):
    """
    Находит все уникальные названия объектов, начинающиеся с "btn_", в файлах,
    имена которых начинаются с "screen_" или "widget_", в заданной папке.
    Возвращает словарь, где ключом является имя файла,
    а значением - список уникальных названий объектов.

    Args:
        folder_path (str): Путь к папке, в которой нужно искать файлы.

    Returns:
        dict: Словарь, где ключом является имя файла, а значением - список уникальных названий объектов.
    """
    btn_objects = {}

    for filename in os.listdir(folder_path):
        if (filename.startswith("screen_") or filename.startswith("widget_")) and filename.endswith(".py"):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    unique_btn_objects = set()
                    for line in file:
                        for word in line.split():
                            if "btn_" in word:
                                if word.startswith("btn_"):
                                    unique_btn_objects.add(word)
                                else:
                                    # Пытаемся найти объект, содержащий "btn_" в середине
                                    for subword in word.split("."):
                                        if subword.startswith("btn_"):
                                            unique_btn_objects.add(subword)
                    if unique_btn_objects:
                        btn_objects[filename] = list(unique_btn_objects)
            except UnicodeDecodeError:
                print(f"Ошибка при чтении файла {filename}. Пропускаем его.")
                continue

    return btn_objects


if __name__ == "__main__":
    # Укажите путь к папке, в которой нужно искать файлы
    folder_path = "/GUI"

    btn_objects_dict = find_btn_objects(folder_path)
    print("screen = {")
    for filename, btn_objects in btn_objects_dict.items():
        filename = filename.split(".")[0]
        print(f"\t'{filename}': {btn_objects},")
    print("}")

    #  Укажите путь к папке, в которой нужно искать файлы

    folder_path = "/GUI"

    button_finder = ButtonFinder(folder_path)
    btn_objects_dict = button_finder.find_btn_objects()
    print("screen = {")
    for filename, btn_objects in btn_objects_dict.items():
        filename = filename.split(".")[0]
        print(f"\t'{filename}': {btn_objects},")
    print("}")
