import json
import xml.etree.ElementTree as ET
import uuid
import time


class JSONToMindMapConverter:
    """
    Класс JSONToMindMapConverter преобразует JSON-код страницы в структуру ментальной карты
    для Freeplane. Создаёт корневой узел для экрана, добавляет узлы для каждого компонента,
    описывая их основные атрибуты, включая текст, размеры и позицию.

    Методы:
        convert(json_data): Преобразует JSON-код в XML для ментальной карты Freeplane.
        add_component_node(parent, component): Добавляет узел компонента в XML-структуру.
        save_to_file(filename): Сохраняет сгенерированную XML-ментальную карту в файл.
    """

    def __init__(self, json_data):
        """
        Инициализирует конвертер с JSON-данными страницы.

        Параметры:
            json_data (dict): JSON-данные страницы для конвертации.
        """
        self.json_data = json_data
        self.root = ET.Element("map", version="freeplane 1.9.13")
        self.screen_node = None

    def convert(self):
        """
        Конвертирует JSON-данные в XML-структуру ментальной карты.

        Возвращает:
            xml.etree.ElementTree.Element: Корневой элемент XML структуры.
        """
        # Создание корневого узла для экрана
        screen_text = self.json_data['mockup']['attributes']['name']
        self.screen_node = ET.SubElement(
            self.root,
            "node",
            TEXT=screen_text,
            ID=self.generate_id(),
            CREATED=self.get_timestamp(),
            MODIFIED=self.get_timestamp(),
            STYLE="oval",
            FOLDED="false"
        )

        # Добавление узлов для каждого элемента управления
        controls = self.json_data['mockup']['controls']['control']
        for control in controls:
            self.add_component_node(self.screen_node, control)

        # Добавление стиля карты, необходимого для корректного отображения в Freeplane
        self.add_map_styles()

        return self.root

    def add_component_node(self, parent, component):
        """
        Добавляет узел для компонента интерфейса в XML-структуру.

        Параметры:
            parent (xml.etree.ElementTree.Element): Родительский узел для компонента.
            component (dict): Данные компонента для добавления.
        """
        # Определяем текст узла компонента
        component_text = component['properties']['text'] if 'properties' in component and 'text' in component[
            'properties'] else component['typeID']

        # Создание узла компонента
        component_node = ET.SubElement(
            parent,
            "node",
            TEXT=component_text,
            ID=self.generate_id(),
            CREATED=self.get_timestamp(),
            MODIFIED=self.get_timestamp(),
            STYLE="oval"
        )
        # Добавление атрибутов (ширина, высота, позиция)
        ET.SubElement(
            component_node,
            "attribute",
            NAME="Width",
            VALUE=str(component['w'])
        )
        ET.SubElement(
            component_node,
            "attribute",
            NAME="Height",
            VALUE=str(component.get('h', 'Not specified'))
        )
        ET.SubElement(
            component_node,
            "attribute",
            NAME="Position",
            VALUE=f"({component['x']}, {component['y']})"
        )

    def add_map_styles(self):
        """
        Добавляет стили в карту для корректного отображения Freeplane.
        """
        style_hook = ET.SubElement(self.root, "hook", NAME="MapStyle", background="#3c3836")
        ET.SubElement(style_hook, "properties", show_icon_for_attributes="true")

    def save_to_file(self, filename):
        """
        Сохраняет XML-структуру ментальной карты в файл.

        Параметры:
            filename (str): Имя файла для сохранения XML-структуры.
        """
        tree = ET.ElementTree(self.root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"Ментальная карта сохранена в файл {filename}")

    @staticmethod
    def generate_id():
        """
        Генерирует уникальный идентификатор для узлов.

        Возвращает:
            str: Уникальный ID.
        """
        return "ID_" + str(uuid.uuid4().int)[:10]

    @staticmethod
    def get_timestamp():
        """
        Возвращает текущий временной штамп.

        Возвращает:
            str: Временной штамп в миллисекундах.
        """
        return str(int(time.time() * 1000))


# Пример использования конвертера
if __name__ == "__main__":
    # JSON данные страницы
    json_data = {
        "mockup": {
            "controls": {
                "control": [
                    {
                        "ID": "0",
                        "typeID": "TitleWindow",
                        "zOrder": "0",
                        "w": "800",
                        "h": "480",
                        "measuredW": "450",
                        "measuredH": "400",
                        "x": "0",
                        "y": "0",
                        "properties": {
                            "text": "Доска с заметками"
                        }
                    },
                    {
                        "ID": "4",
                        "typeID": "TextArea",
                        "zOrder": "2",
                        "w": "600",
                        "h": "80",
                        "measuredW": "200",
                        "measuredH": "140",
                        "x": "10",
                        "y": "40"
                    },
                    # Другие компоненты...
                ]
            },
            "attributes": {
                "name": "Доска с заметками",
                "order": 1488661.5597810687,
                "parentID": None
            },
            "resourceID": "E9240B8F-BCCB-4648-BE6F-A756D6A39166",
            "mockupH": "480",
            "mockupW": "800",
            "measuredW": "800",
            "measuredH": "480",
            "version": "1.0"
        }
    }

    # Инициализация и запуск конвертера
    converter = JSONToMindMapConverter(json_data)
    root = converter.convert()
    converter.save_to_file("mind_map.mm")
