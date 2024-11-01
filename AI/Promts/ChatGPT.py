description_file = ""
path_to_file = ""
promts = {
    'code_by_description': {'text': (f'Хорошо, теперь давай построим максимально эффективный код всех описанных классов, '
                            f'хорошо прокомментированный, отлаженный  и рабочий.Вот описание:{description_file}'), },
    'code_full': (f'Хорошо, теперь давай реализуем максимально полный, и эффективный код всех описанных классов, '
                  f'полностью реализующий всю описанную функциональность, этот код должен быть хорошо прокомментирован, '
                  f'отлажен и работоспособен. Вот описание, если ты считаешь его не полным, разрешаю улучшить и '
                  f'расширить:{description_file}'),
    'code_': (f'Хорошо, теперь давай реализуем максимально полный, и эффективный код всех описанных классов, '
             f'полностью реализующий всю описанную функциональность, этот код должен быть хорошо прокомментирован,'
             f'отлажен и работоспособен. Ответ дай на русском языке.Вот описание, если ты считаешь его не полным, '
             f'разрешаю улучшить и расширить описание, и на его основе значительно улучшить идею, концепцию и '
             f'архитектуру файла и классов внутри, '
             f'применив способности высокоинтеллектуального уровня:{description_file}'),
    'get_description': (f'Какое назначение у этого файла и какие классы в нём должны быть?'
         f'{path_to_file}'
         f'Дай более развёрнутое описание.'),
    'update_class': (f'Хорошо, вот у нас есть файл с классом, нам нужна его новая версия более полная, '
         f'хорошо продуманная и максимально эффективная. Она должна быть тщательно и подробно прокомментирована. '
         f'Должна иметь заголовок в котором доходчиво прописан принцип работы. '
         f'Выдай пожалуйста новую версию файла с учётом всех правок, что я попросил внести. '
         f'Да, ответь пожалуйста на русском языке. {path_to_file}')

}







