import os
import subprocess
import re


class UIConverter:
    """
    Класс UIConverter предназначен для конвертации Qt Designer файлов с расширением .ui
    в эквивалентные файлы .py, которые можно использовать напрямую в Python проектах.
    Класс автоматически обрабатывает все .ui файлы в указанной директории,
    используя утилиту pyuic5 для выполнения преобразования.

    Атрибуты:
        ui_folder (str): Путь к папке, содержащей файлы .ui для конвертации.

    Методы:
        convert_ui_to_py(): Конвертирует все .ui файлы в заданной папке в файлы .py.
        get_py_filename(ui_file): Генерирует имя для выходного .py файла на основе имени .ui файла.
        log_conversion(ui_file, py_file): Логирует успешную конвертацию файла.
        check_pyuic5_installed(): Проверяет, установлен ли pyuic5, необходимый для работы класса.
    """

    def __init__(self, ui_folder):
        """
        Инициализирует UIConverter с указанной папкой для поиска .ui файлов.

        Параметры:
            ui_folder (str): Путь к папке с .ui файлами.
        """
        self.ui_folder = ui_folder

    def convert_ui_to_py(self):
        """
        Конвертирует все файлы .ui в указанной папке в файлы .py.
        Проверяет, установлен ли pyuic5, и обрабатывает каждый .ui файл,
        вызывая pyuic5 для генерации Python кода.
        """
        if not self.check_pyuic5_installed():
            print("Ошибка: pyuic5 не найден. Убедитесь, что утилита pyuic5 установлена.")
            return

        for filename in os.listdir(self.ui_folder):
            if filename.endswith(".ui"):
                ui_file = os.path.join(self.ui_folder, filename)
                py_file = self.get_py_filename(filename)
                try:
                    # Запускаем pyuic5 для конвертации
                    subprocess.run(["pyuic5", "-o", py_file, ui_file], check=True)
                    self.log_conversion(ui_file, py_file)
                except subprocess.CalledProcessError as e:
                    print(f"Ошибка конвертации {ui_file}: {e}")
                except Exception as e:
                    print(f"Непредвиденная ошибка с файлом {ui_file}: {e}")

    def get_py_filename(self, ui_file):
        """
        Генерирует имя выходного .py файла на основе имени .ui файла,
        удаляя ненужные символы из имени.

        Параметры:
            ui_file (str): Имя .ui файла.

        Возвращает:
            str: Имя выходного .py файла.
        """
        # Убираем ненужные символы из имени файла
        base_name = re.sub(r'\d+_', '', os.path.splitext(ui_file)[0])
        return os.path.join(self.ui_folder, f"{base_name}.py")

    def log_conversion(self, ui_file, py_file):
        """
        Логирует успешную конвертацию .ui файла в .py файл.

        Параметры:
            ui_file (str): Путь к исходному .ui файлу.
            py_file (str): Путь к выходному .py файлу.
        """
        print(f"Успешно конвертирован {ui_file} в {py_file}")

    def check_pyuic5_installed(self):
        """
        Проверяет, установлен ли pyuic5 для выполнения конвертации .ui файлов.

        Возвращает:
            bool: True, если pyuic5 установлен, иначе False.
        """
        try:
            subprocess.run(["pyuic5", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при проверке pyuic5: {e}")
            return False


if __name__ == "__main__":
    # Текущая директория, где находится скрипт
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Инициализация конвертера и запуск конвертации
    converter = UIConverter(current_dir)
    converter.convert_ui_to_py()
