import xml.etree.ElementTree as ET
import os


class FSMConverter:
    """
    Класс FSMConverter предназначен для преобразования XML-файлов разметки
    (в данном случае *.mm файлов Freeplane) в формат Python. Он извлекает
    состояния и переходы из диаграммы и сохраняет их в формате Python для
    последующей обработки. Класс включает методы для парсинга XML,
    удаления файла с картой состояний и записи извлеченных данных в новый файл.

    Атрибуты:
        xml_file (str): Путь к XML файлу.
        states (list): Список состояний, извлечённых из XML.
        transitions (list): Список переходов между состояниями.

    Методы:
        delete_file(file_path): Удаляет файл, если он существует.
        parse_xml(): Извлекает состояния и переходы из XML файла.
        save_to_file(file_path): Сохраняет состояния и переходы в файл.
    """

    def __init__(self, xml_file):
        """
        Инициализирует экземпляр FSMConverter с указанным XML файлом.

        Параметры:
            xml_file (str): Путь к XML файлу для парсинга.
        """
        self.xml_file = xml_file
        self.states = []
        self.transitions = []

    def delete_file(self, file_path):
        """
        Удаляет файл, если он существует.

        Параметры:
            file_path (str): Путь к файлу, который нужно удалить.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Файл {file_path} был успешно удалён.")
            else:
                print(f"Файл {file_path} не существует.")
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")

    def parse_xml(self):
        """
        Парсит XML файл для извлечения состояний и переходов.

        Проходит по каждому узлу XML структуры, выделяя состояния как
        текстовые метки узлов, и переходы как стрелки, соединяющие узлы.
        Определяет направление стрелки и обновляет список переходов
        соответствующим образом.
        """
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()

            # Извлечение всех состояний (узлов)
            for node in root.findall('.//node'):
                self.states.append({'name': node.attrib['TEXT']})

            # Извлечение всех переходов
            for node in root.findall('.//node'):
                for arrowlink in node.findall('arrowlink'):
                    trigger = arrowlink.get('MIDDLE_LABEL', 'None')
                    source = node.attrib['TEXT']
                    dest_id = arrowlink.get('DESTINATION')
                    dest_node = root.find(f".//node[@ID='{dest_id}']")

                    if dest_node is not None:
                        dest = dest_node.attrib['TEXT']
                        start_arrow = arrowlink.get('STARTARROW')
                        end_arrow = arrowlink.get('ENDARROW')

                        if start_arrow == "DEFAULT" and end_arrow == "NONE":
                            # Обратная стрелка, меняем source и dest местами
                            self.transitions.append({
                                'trigger': trigger, 'source': dest, 'dest': source
                            })
                        else:
                            # Прямая стрелка
                            self.transitions.append({
                                'trigger': trigger, 'source': source, 'dest': dest
                            })
        except ET.ParseError as e:
            print(f"Ошибка парсинга XML: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")

    def save_to_file(self, file_path='state_map.py'):
        """
        Сохраняет извлечённые состояния и переходы в файл Python.

        Параметры:
            file_path (str): Путь к файлу, в который нужно сохранить данные.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('states = [\n')
                for state in self.states:
                    f.write(f"    {{'name': '{state['name']}'}},\n")
                f.write(']\n\n')

                f.write('transitions = [\n')
                for transition in self.transitions:
                    f.write(
                        f"    {{'trigger': '{transition['trigger']}', 'source': '{transition['source']}', 'dest': '{transition['dest']}'}},\n"
                    )
                f.write(']')
            print(f"Карта состояний сохранена в {file_path}")
        except IOError as e:
            print(f"Ошибка записи в файл: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")


# Пример использования класса
if __name__ == "__main__":
    converter = FSMConverter('screen.mm')  # Укажите путь к вашему XML файлу
    converter.delete_file("state_map.py")
    converter.parse_xml()
    converter.save_to_file()
