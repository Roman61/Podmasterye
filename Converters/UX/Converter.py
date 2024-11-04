# Demiurge/Converters/UX/BalsamiqWireframes/Converter.py отвечает за конвертацию *.bmpr файлов из
# Balsamiq Wireframes в JSON-формат, который может быть использован генератором кода для создания UX-интерфейсов.
# Файл также предоставляет методы для обратного преобразования из JSON в *.bmpr, а также для интеграции UX-данных с
# проектной структурой.
# Классы:
#
#     Converter:
#         Основной класс для конвертации UX-данных из *.bmpr файлов в JSON и обратно.
#         Методы:
#             bmpr_to_json(): Извлекает данные из *.bmpr файла и сохраняет их в формате JSON.
#             json_to_bmpr(): Загружает JSON-данные и преобразует их в структуру *.bmpr.
#             fetch_data_from_database(): Извлекает данные из базы SQLite внутри *.bmpr.
#             convert_to_ux_format(): Конвертирует данные в удобный формат JSON.
#             __adaptation(), decode_unicode_escape(), detect_encoding(): Вспомогательные функции для обработки
#             кодировок и структуры данных.
#
#     UXElement:
#         Представляет UI-элемент с основными свойствами, извлеченными из Balsamiq Wireframes.
#         Используется для хранения данных, таких как свойства элементов интерфейса, и может быть полезен для
#         внутреннего представления UX компонентов.
#
# Этот файл, благодаря классу Converter, обеспечивает эффективное взаимодействие между UX-дизайном и
# кодовой структурой проекта, упрощая генерацию и преобразование данных интерфейса.

import sqlite3
import json
import codecs
import chardet
import os
from lxml import etree


class UXConverter:
    '''
     description: Converter UX bmpr-to-json for code generator
     input: sqlite database as bmpr file by Balsamiq Wireframes
     output: json file ux formate
     developer: Roman Korolev
     contact: Orodunaar@mail.ru
    '''

    def __init__(self, path):
        self.db_path = path
        self.ux_format = {
            "branches": [],
            "resources": [],
            "comments": [],
            "users": [],
            "thumbnails": [],
            "info": {}
        }
        self.ui_format = {}

    def decode_unicode_escape(self, text):
        """Преобразует кодировку 'unicode_escape' в формат 'utf-8'."""
        try:
            # Сначала проверяем, является ли текст строкой
            if isinstance(text, str):
                # Кодируем в байты
                byte_data = text.encode('utf-8')
                local_type = self.detect_encoding(byte_data)

                # Проверяем кодировку
                if local_type[0] == 'unicode_escape' and local_type[1] > 0.6:
                    # Декодируем с использованием unicode_escape
                    return codecs.decode(byte_data, 'unicode_escape')
                else:
                    return text
            else:
                # print(f"Ошибка декодирования: ожидается строка, но получен тип {type(text)}")
                return text
        except Exception as e:
            print(f"Ошибка декодирования: {e}")
            return text

    def detect_encoding(self, byte_data):
        """Определяет кодировку данных."""
        if isinstance(byte_data, bytes) or isinstance(byte_data, bytearray):
            result = chardet.detect(byte_data)
            return result['encoding'], result['confidence']
        else:
            print(f"Ошибка определения кодировки: ожидаются байты или bytearray, но получен тип {type(byte_data)}")
            return None, 0

    def convert_to_ux_format(self, data):
        # Конвертируем ветки
        for branch in data["branches"]:
            branch_attributes = json.loads(branch[1])  # предполагаем, что ATTRIBUTES в формате JSON
            branch_attributes["name"] = self.decode_unicode_escape(branch_attributes.get("name", ""))
            self.ux_format["branches"].append({
                "id": branch[0],
                "attributes": branch_attributes
            })

        # Конвертируем ресурсы
        for resource in data["resources"]:
            resource_attributes = json.loads(resource[2])
            resource_attributes["name"] = self.decode_unicode_escape(resource_attributes.get("name", ""))

            # Декодируем поле 'data', если оно есть
            resource_data = resource[3]
            if isinstance(resource_data, str):
                try:
                    resource_data = json.loads(resource_data)  # Пробуем разобрать JSON
                except json.JSONDecodeError as e:
                    print(f"Ошибка декодирования JSON: {e}")
                    resource_data = {}

                # Декодируем, если это строка
                resource_data = self.decode_unicode_escape(resource_data)

            self.ux_format["resources"].append({
                "id": resource[0],
                "branchId": resource[1],
                "attributes": resource_attributes,
                "data": resource_data
            })

        # Конвертируем комментарии
        for comment in data["comments"]:
            comment_attributes = json.loads(comment[5])
            comment_attributes["name"] = self.decode_unicode_escape(comment_attributes.get("name", ""))

            self.ux_format["comments"].append({

                "id": comment[0],
                "branchId": comment[1],
                "resourceId": comment[2],
                "data": self.decode_unicode_escape(comment[3]),  # Декодируем, если это строка
                "userId": comment[4],
                "attributes": comment_attributes
            })

            # Конвертируем пользователей
            for user in data["users"]:
                user_attributes = json.loads(user[1])
                user_attributes["name"] = self.decode_unicode_escape(user_attributes.get("name", ""))

                self.ux_format["users"].append({
                    "id": user[0],
                    "attributes": user_attributes
                })

            # Конвертируем миниатюры
            for thumbnail in data["thumbnails"]:
                thumbnail_attributes = json.loads(thumbnail[1])
                thumbnail_attributes["name"] = self.decode_unicode_escape(thumbnail_attributes.get("name", ""))

                self.ux_format["thumbnails"].append({
                    "id": thumbnail[0],
                    "attributes": thumbnail_attributes
                })

            # Конвертируем информацию
            for info in data["info"]:
                self.ux_format["info"][info[0]] = self.decode_unicode_escape(info[1])  # Декодируем, если это строка

            return self.ux_format

    def __adaptation(self):
        # Обработка данных
        for table_name, table_data in self.ux_format.items():
            print(f"Обработка таблицы: {table_name}")
            self.process_table(table_data)

    # def json_to_bmpr(self, input_file_path):
    #    self.__open(input_file_path)

    def bmpr_to_json(self):
        # Получаем данные
        data = self.fetch_data_from_database()

        # Конвертируем данные
        self.convert_to_ux_format(data)

        self.__adaptation()

    def fetch_data_from_database(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Считываем данные из всех таблиц
        branches = cursor.execute("SELECT * FROM BRANCHES").fetchall()
        resources = cursor.execute("SELECT * FROM RESOURCES").fetchall()
        comments = cursor.execute("SELECT * FROM COMMENTS").fetchall()
        users = cursor.execute("SELECT * FROM USERS").fetchall()
        thumbnails = cursor.execute("SELECT * FROM THUMBNAILS").fetchall()
        info = cursor.execute("SELECT * FROM INFO").fetchall()

        connection.close()

        return {
            "branches": branches,
            "resources": resources,
            "comments": comments,
            "users": users,
            "thumbnails": thumbnails,
            "info": info
        }

    def decode_unicode_string(self, s):
        try:
            return s.encode('latin1').decode('unicode_escape')
        except Exception as e:
            # print(f"Ошибка при декодировании строки: {s} - {e}")
            return s

    def process_table(self, table_data):
        for item in table_data:
            for key, value in item.items():
                if key in ['text', 'name']:
                    item[key] = self.decode_unicode_string(value)
                elif isinstance(value, dict):
                    self.process_table([value])
                elif isinstance(value, list):
                    self.process_table(value)

    def __open(self, input_file_path=""):
        # Чтение данных из файла
        with open(input_file_path, "r", encoding="utf-8") as f:
            self.ux_format = json.load(f)

    def save_ui(self, xml_file_path):
        # Конвертация и сохранение в файл
        if isinstance(self.ui_format, dict):
            for _, key in enumerate(self.ui_format):
                ui_xml = self.ui_format[key]
                with open(xml_file_path+key+'.ui', "wb") as file:
                    file.write(ui_xml)

    def save_json(self, output_file_path=""):
        # Запись откорректированных данных в новый файл
        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(self.ux_format, f, ensure_ascii=False, indent=2)
            print(f"Данные успешно записаны в {output_file_path}")

    def __create_database_if_not_exists(self, db_file):
        # Проверка на существование файла базы данных
        if not os.path.exists(db_file):
            print(f"Файл '{db_file}' не найден. Создаю новый файл базы данных...")
            # Подключение к базе данных (создание, если файл не существует)
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            # Создание таблицы BRANCHES
            cursor.execute('''CREATE TABLE IF NOT EXISTS BRANCHES (
                                ID VARCHAR(255) PRIMARY KEY, 
                                ATTRIBUTES TEXT)''')

            # Создание таблицы USERS
            cursor.execute('''CREATE TABLE IF NOT EXISTS USERS (
                                ID VARCHAR(255) PRIMARY KEY, 
                                ATTRIBUTES TEXT)''')

            # Создание таблицы RESOURCES
            cursor.execute('''CREATE TABLE IF NOT EXISTS RESOURCES (
                                ID VARCHAR(255), 
                                BRANCHID VARCHAR(255), 
                                ATTRIBUTES TEXT, 
                                DATA LONGTEXT, 
                                PRIMARY KEY (ID, BRANCHID), 
                                FOREIGN KEY (BRANCHID) REFERENCES BRANCHES(ID))''')

            # Создание таблицы THUMBNAILS
            cursor.execute('''CREATE TABLE IF NOT EXISTS THUMBNAILS (
                                ID VARCHAR(255) PRIMARY KEY, 
                                ATTRIBUTES MEDIUMTEXT)''')

            # Создание таблицы INFO
            cursor.execute('''CREATE TABLE IF NOT EXISTS INFO (
                                NAME VARCHAR(255) PRIMARY KEY, 
                                VALUE TEXT)''')

            # Создание таблицы COMMENTS
            cursor.execute('''CREATE TABLE IF NOT EXISTS COMMENTS (
                                ID VARCHAR(255) PRIMARY KEY, 
                                BRANCHID VARCHAR(255), 
                                RESOURCEID VARCHAR(255), 
                                DATA LONGTEXT, 
                                USERID VARCHAR(255), 
                                ATTRIBUTES TEXT, 
                                FOREIGN KEY (USERID) REFERENCES USERS(ID), 
                                FOREIGN KEY (RESOURCEID, BRANCHID) REFERENCES RESOURCES(ID, BRANCHID))''')

            # Сохранение изменений и закрытие соединения
            conn.commit()
            conn.close()
            print(f"База данных '{db_file}' успешно создана.")
        else:
            print(f"Файл базы данных '{db_file}' уже существует.")

    def populate_database_from_json(self, json_file, db_file):
        # Проверка на существование базы данных и создание её, если не существует
        self.create_database_if_not_exists(db_file)

        # Открываем JSON файл и читаем его содержимое
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Подключаемся к базе данных SQLite
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Наполняем таблицу BRANCHES
        for branch in data.get('branches', []):
            self.insert_branch(cursor, branch)

        # Наполняем таблицу RESOURCES
        for resource in data.get('resources', []):
            self.insert_resource(cursor, resource)

        # Если есть другие данные (comments, users и т.д.), добавляем их
        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

    def create_database_if_not_exists(self, db_file):
        if not os.path.exists(db_file):
            print(f"Файл '{db_file}' не найден. Создаю новый файл базы данных...")
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()

            # Создание структуры таблиц
            cursor.execute('''CREATE TABLE IF NOT EXISTS BRANCHES (
                                ID VARCHAR(255) PRIMARY KEY, 
                                ATTRIBUTES TEXT)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS USERS (
                                ID VARCHAR(255) PRIMARY KEY, 
                                ATTRIBUTES TEXT)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS RESOURCES (
                                ID VARCHAR(255), 
                                BRANCHID VARCHAR(255), 
                                ATTRIBUTES TEXT, 
                                DATA LONGTEXT, 
                                PRIMARY KEY (ID, BRANCHID), 
                                FOREIGN KEY (BRANCHID) REFERENCES BRANCHES(ID))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS THUMBNAILS (
                                ID VARCHAR(255) PRIMARY KEY, 
                                ATTRIBUTES MEDIUMTEXT)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS INFO (
                                NAME VARCHAR(255) PRIMARY KEY, 
                                VALUE TEXT)''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS COMMENTS (
                                ID VARCHAR(255) PRIMARY KEY, 
                                BRANCHID VARCHAR(255), 
                                RESOURCEID VARCHAR(255), 
                                DATA LONGTEXT, 
                                USERID VARCHAR(255), 
                                ATTRIBUTES TEXT, 
                                FOREIGN KEY (USERID) REFERENCES USERS(ID), 
                                FOREIGN KEY (RESOURCEID, BRANCHID) REFERENCES RESOURCES(ID, BRANCHID))''')

            conn.commit()
            conn.close()
            print(f"База данных '{db_file}' успешно создана.")
        else:
            print(f"Файл базы данных '{db_file}' уже существует.")

    def insert_branch(self, cursor, branch):
        attributes_json = json.dumps(branch.get('attributes', {}))
        cursor.execute('''
            INSERT INTO BRANCHES (ID, ATTRIBUTES)
            VALUES (?, ?)
        ''', (branch.get('id'), attributes_json))

    def insert_resource(self, cursor, resource):
        attributes_json = json.dumps(resource.get('attributes', {}))
        data_json = json.dumps(resource.get('data', {}))
        cursor.execute('''
            INSERT INTO RESOURCES (ID, BRANCHID, ATTRIBUTES, DATA)
            VALUES (?, ?, ?, ?)
        ''', (resource.get('id'), resource.get('branchId'), attributes_json, data_json))

    def json_to_bmpr(self, json_file):
        # Чтение данных из JSON файла
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Создание базы данных, если она не существует
        self.create_database_if_not_exists(self.db_path)

        # Подключаемся к базе данных
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Наполнение базовых таблиц данными
        self.insert_branches(cursor, data.get("branches", []))
        self.insert_resources(cursor, data.get("resources", []))
        self.insert_comments(cursor, data.get("comments", []))
        self.insert_users(cursor, data.get("users", []))
        self.insert_thumbnails(cursor, data.get("thumbnails", []))
        self.insert_info(cursor, data.get("info", {}))

        # Сохраняем изменения
        conn.commit()
        conn.close()

    def insert_branches(self, cursor, branches):
        for branch in branches:
            attributes = json.dumps(branch["attributes"], ensure_ascii=False)  # Конвертация атрибутов в JSON
            cursor.execute('''
                INSERT INTO BRANCHES (ID, ATTRIBUTES)
                VALUES (?, ?)
                ON CONFLICT(ID) DO UPDATE SET ATTRIBUTES=excluded.ATTRIBUTES
            ''', (branch["id"], attributes))

    def insert_resources(self, cursor, resources):
        for resource in resources:
            attributes = json.dumps(resource["attributes"], ensure_ascii=False)  # Конвертация атрибутов в JSON
            data = json.dumps(resource["data"], ensure_ascii=False)  # Конвертация данных в JSON
            cursor.execute('''
                INSERT INTO RESOURCES (ID, BRANCHID, ATTRIBUTES, DATA)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(ID, BRANCHID) DO UPDATE SET ATTRIBUTES=excluded.ATTRIBUTES, DATA=excluded.DATA
            ''', (resource["id"], resource["branchId"], attributes, data))

    def insert_comments(self, cursor, comments):
        for comment in comments:
            attributes = json.dumps(comment["attributes"], ensure_ascii=False)  # Конвертация атрибутов в JSON
            data = comment.get("data", "")
            cursor.execute('''
                INSERT INTO COMMENTS (ID, BRANCHID, RESOURCEID, DATA, USERID, ATTRIBUTES)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(ID) DO UPDATE SET DATA=excluded.DATA, ATTRIBUTES=excluded.ATTRIBUTES
            ''', (comment["id"], comment["branchId"], comment["resourceId"], data, comment["userId"], attributes))

    def insert_users(self, cursor, users):
        for user in users:
            attributes = json.dumps(user["attributes"], ensure_ascii=False)  # Конвертация атрибутов в JSON
            cursor.execute('''
                INSERT INTO USERS (ID, ATTRIBUTES)
                VALUES (?, ?)
                ON CONFLICT(ID) DO UPDATE SET ATTRIBUTES=excluded.ATTRIBUTES
            ''', (user["id"], attributes))

    def insert_thumbnails(self, cursor, thumbnails):
        for thumbnail in thumbnails:
            attributes = json.dumps(thumbnail["attributes"], ensure_ascii=False)  # Конвертация атрибутов в JSON
            cursor.execute('''
                INSERT INTO THUMBNAILS (ID, ATTRIBUTES)
                VALUES (?, ?)
                ON CONFLICT(ID) DO UPDATE SET ATTRIBUTES=excluded.ATTRIBUTES
            ''', (thumbnail["id"], attributes))

    def insert_info(self, cursor, info):
        for key, value in info.items():
            cursor.execute('''
                INSERT INTO INFO (NAME, VALUE)
                VALUES (?, ?)
                ON CONFLICT(NAME) DO UPDATE SET VALUE=excluded.VALUE
            ''', (key, value))

    # Функция для конвертации JSON в XML .ui формат
    def json_to_ui(self, json_datas=''):
        if not json_datas:
            json_datas = self.ux_format['resources']

        json_list = {}
        for data in json_datas:
            json_data = data['data']
            if "mockup" not in json_data:
                continue
            root = etree.Element("ui", version="4.0")

            # Основной класс формы
            widget_class = etree.SubElement(root, "class")
            widget_class.text = "Form"
            form_widget = etree.SubElement(root, "widget", attrib={"class": "QWidget", "name": "Form"})

            # Задание размеров формы
            geometry = etree.SubElement(form_widget, "property", name="geometry")
            rect = etree.SubElement(geometry, "rect")
            width = json_data["mockup"].get("mockupW")
            height = json_data["mockup"].get("mockupH")
            etree.SubElement(rect, "x").text = "0"
            etree.SubElement(rect, "y").text = "0"
            etree.SubElement(rect, "width").text = width
            etree.SubElement(rect, "height").text = height

            # Название окна
            window_title = etree.SubElement(form_widget, "property", name="windowTitle")
            if "mockup" in json_data and "attributes" in json_data["mockup"]:
                title_text = json_data["mockup"]["attributes"].get("name")
                etree.SubElement(window_title, "string").text = title_text

            # Создание виджетов на основе JSON данных
            widget_mapping = {
                "Button": "QPushButton",
                "RadioButton": "QRadioButton",
                "CheckBox": "QCheckBox",
                "ComboBox": "QComboBox",
                "Label": "QLabel",
                "TextInput": "QLineEdit",
                "TextArea": "QPlainTextEdit",
                "HSlider": "QSlider",
                "VSlider": "QSlider",
                "VSplitter": "Line",
                "HSplitter": "Line",
                "VerticalScrollBar": "QScrollBar",
                "HorizontalScrollBar": "QScrollBar",
                "MenuBar": "QMenuBar",
                "TabBar": "QTabWidget",
                "List": "QListView",
                "Tooltip": "QToolTip",
                "Calendar": "QCalendarWidget",
                "ProgressBar": "QProgressBar",
                "Image": "QGraphicsView",
                "NumericStepper": "QSpinBox",
                "FieldSet": "QGroupBox",
                "Canvas": "QWidget",
                "SubTitle": "QLabel",
                "Webcam": "QLabel",
                "Icon": "QLabel",
                "Title": "QLabel",  # Для отображения текста заголовка
            }
            if not json_data["mockup"]["controls"]:
                continue
            json_data_controls = json_data["mockup"]["controls"]["control"]

            for control in json_data_controls:
                control_type = control["typeID"]
                if "TitleWindow" in control_type and "properties" in control:
                    widget_class.text = control["properties"]["text"]
                    etree.SubElement(rect, "width").text = control["w"]
                    etree.SubElement(rect, "height").text = control["measuredH"]
                    form_widget.attrib["name"] = control["properties"]["text"]
                    continue
                widget_class_name = widget_mapping.get(control_type, "QWidget")
                widget = etree.SubElement(form_widget, "widget",
                                          attrib={"class": widget_class_name,
                                                  "name": f"{control_type}_{control['ID']}"})

                # Задание свойств виджета
                geometry = etree.SubElement(widget, "property", name="geometry")
                rect = etree.SubElement(geometry, "rect")
                etree.SubElement(rect, "x").text = control.get("x")
                etree.SubElement(rect, "y").text = control.get("y")
                if control.get("w") and control.get("h"):
                    etree.SubElement(rect, "width").text = control.get("w")
                    etree.SubElement(rect, "height").text = control.get("h")
                else:
                    etree.SubElement(rect, "width").text = control.get("measuredW")
                    etree.SubElement(rect, "height").text = control.get("measuredH")

                if "H" in control_type[0]:
                    etree.SubElement(rect, "width").text = control.get("w")
                    etree.SubElement(rect, "height").text = control.get("measuredH")
                    property_orientation = etree.SubElement(widget, "property", name="orientation")
                    enum = etree.SubElement(property_orientation, "enum")
                    enum.text = "Qt::Horizontal"
                elif "V" in control_type[0]:
                    etree.SubElement(rect, "height").text = control.get("h")
                    etree.SubElement(rect, "width").text = control.get("measuredW")
                    property_orientation = etree.SubElement(widget, "property", name="orientation")
                    enum = etree.SubElement(property_orientation, "enum")
                    enum.text = "Qt::Vertical"
                # Установка текста, если есть
                if "properties" in control and "text" in control["properties"]:
                    text = etree.SubElement(widget, "property", name="text")
                    etree.SubElement(text, "string").text = control["properties"]["text"]
            key = data['attributes']['name']
            if "New Wireframe" in key:
                continue
            json_list[key] = (
                etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=True))
            self.ui_format = json_list
        # Возвращаем строку XML с форматированием
        return json_list

    def bmpr_to_ui(self):
        self.bmpr_to_json()
        self.json_to_ui()


class UXElement:
    def __init__(self, properties):
        self.properties = properties

    def __repr__(self):
        return f"UXElement(properties={self.properties})"


# Пример использования
if __name__ == "__main__":
    # Укажите путь к ux файлу
    db_path = 'G:\\lesson\\diplom_project\\doc\\Test_one\\Test_one.bmpr'
    # Путь к сохранения ui файлу
    xml_file_path = "G:\\lesson\\diplom_project\\doc\\Test_one\\"

    converter = UXConverter(db_path)
    converter.bmpr_to_ui()
    converter.save_ui(xml_file_path)

    # Пример использования:
    # populator = DatabasePopulator('database.bmpr')
    # converter.json_to_bmpr('Collection_component.json')
