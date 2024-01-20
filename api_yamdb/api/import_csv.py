import csv


def import_base(model, file):
    with open(file, encoding='utf-8') as r_file:
        # Создаем объект reader, указываем символ-разделитель ",".
        file_reader = csv.reader(r_file, delimiter=",")
        # Счетчик для подсчета количества строк и вывода заголовков столбцов.
        count = 0
        fields_table = None
        result = []
        # Считывание данных из CSV файла.
        for row in file_reader:
            if count == 0:
                fields_table = row
            else:
                i = 0
                object = {}
                for field in fields_table:
                    if (
                        field == "author"
                        or field == "title_id"
                        or field == "category"
                        or field == "review_id"
                    ):
                        object[field] = None
                    elif field == "role" or field == "bio":
                        pass
                    else:
                        object[field] = row[i]
                    i += 1
                result.append(object)
            count += 1
        print("Поля в таблице", fields_table)
        print(result)
        for object in result:
            data = model(**object)
            data.save()
        print("Загрузка успешна.")
