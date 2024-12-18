<p align="center">
    <img src="https://github.com/user-attachments/assets/3437d455-cc65-4fd7-a95e-b1a339404fe1" />
</p>

<h1 align="center">Подмастерье 
<h3 align="left">Podmasterye: Автоматизированная САПР для разработки ПО</h3>



Podmasterye — это комплексная система автоматизированного проектирования программного обеспечения (САПР) для сквозной автоматизации процессов разработки. Podmasterye предоставляет возможность описывать, проектировать и реализовывать приложения в единой среде, что сокращает время разработки, улучшает структурную целостность проекта и позволяет исключить ошибки на ранних этапах. Система объединяет возможности генерации архитектуры, кода, создания базы данных, а также отладки и улучшения кода с применением ИИ.
Основные возможности



Анализ архитектуры проекта: автоматическое построение архитектуры и выявление связей между компонентами.
Конвертация UX файлов в UI: генерация интерфейсных файлов из UX-структур.
Генерация переходов состояний: создание переходов между состояниями из карт состояний.
Преобразование JSON в mind map: автоматический перевод JSON данных в ментальные карты для визуализации.

<p align="center">
    <img src="https://github.com/user-attachments/assets/521cace6-b6a0-4e77-9711-978301435e3b" alt="пояснение5" width="501" height="395" />
</p>

Быстрый старт
Установка

Для начала работы склонируйте репозиторий и установите необходимые зависимости:

    bash
    
    git clone https://github.com/Roman61/podmasterye.git
    cd podmasterye
    pip install -r requirements.txt

Использование

Podmasterye управляется через команды командной строки. Вот основные команды для работы:
Команда для анализа архитектуры проекта

Анализирует архитектуру проекта и выводит ее структуру:

    bash
    
    python main.py analyze G:\lesson\diplom_project --ignore .git .venv

Аргументы:

project_path — путь к корневой директории проекта.
--ignore — список игнорируемых папок и файлов (по умолчанию: .venv, .gitignore, .idea).

Команда для конвертации UX в UI

Конвертирует UX файл (формат .bmpr) в UI компоненты для интерфейса:

    bash
    
    python main.py ux_to_ui G:\lesson\diplom_project\doc\Test_one\Test_one.bmpr G:\lesson\diplom_project\doc\Test_one\


Исходное изображение:
<p align="center">
    <img src="https://github.com/user-attachments/assets/affb63b8-a9ab-478e-a757-26f6e1509ecc" width="533" height="266" />
</p>


Результат конвертации:
<p align="center">
    <img src="https://github.com/user-attachments/assets/cab03097-1b5a-49b3-9c74-f238ede4b8cf" width="533" height="266" />
</p>

Аргументы:

ux_path — путь к UX файлу .bmpr.
output_path — директория для сохранения сгенерированных UI файлов.

Команда для генерации переходов из карты состояний

Создает переходы между состояниями на основе карты состояний, используя указанный модуль:

    bash

    python main.py generate_transitions G:\lesson\diplom_project\doc\code\state_map.py G:\lesson\Urban_university\diplom_project\doc\code\cmdHelper --key=default

Аргументы:

module_path — путь к файлу state_map.py.
output_path — папка для сохранения файлов сгенерированных классов.
--key — ключ для генерации (по умолчанию: default).

Команда для конвертации JSON в mind map

Преобразует JSON данные в формат ментальной карты, совместимый с Freeplane:

    bash

    python main.py json_to_mm G:\lesson\diplom_project\doc\components.json G:\lesson\diplom_project\doc\mind_map.mm

Аргументы:

json_path — путь к JSON файлу.
output_path — путь для сохранения mind map файла.

Основные классы и их функции

ProjectAnalyzer — анализирует архитектуру проекта и строит иерархическую структуру.
UXConverter — конвертирует UX макеты в UI компоненты, совместимые с Qt Designer.
TransitionManager — управляет состояниями и переходами, генерируя структуры классов для работы с состояниями.
JSONToMindMapConverter — преобразует JSON файл в ментальную карту для визуализации и анализа с помощью Freeplane.

Примеры использования

Вот несколько примеров для начала работы с Podmasterye:

Анализ архитектуры:

    bash
    
    python main.py analyze /path/to/your/project --ignore .git .venv

Конвертация UX в UI:

    bash

    python main.py ux_to_ui /path/to/ux/file.bmpr /path/to/save/ui/

Генерация переходов состояний:

    bash
    
    python main.py generate_transitions /path/to/state_map.py /output/path/ --key=default

Конвертация JSON в mind map:

bash

    python main.py json_to_mm /path/to/file.json /path/to/save/mindmap.mm

Задачи проекта

Интеграция этапов разработки — создание платформы для объединения описания идеи, формирования ментальных карт и генерации кода.
Генерация структуры базы данных — автоматическое создание ORM моделей и схем баз данных.
Поддержка различных форматов — работа с ментальными картами и UX/UI макетами для сохранения данных на всех этапах.

Вклад

Мы приветствуем ваш вклад в развитие Podmasterye! Пожалуйста, создавайте issues и pull requests, следуя нашим рекомендациям по оформлению и стандартам кодирования.
Лицензия

Этот проект лицензирован под MIT License.



