import csv
import re
import pandas as pd


def main():
    # читаем адресную книгу в формате CSV в список contacts_list
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)


    # TODO 1: выполните пункты 1-3 ДЗ
    # ваш код
    pattern_name = r"^(\w+)[,\s](\w+)[,\s](\w+|)"
    for i in contacts_list:
        result = re.search(pattern_name, ",".join(map(str, i)))
        i[0] = result.group(1)
        i[1] = result.group(2)
        i[2] = result.group(3)

    pattern_phone = r"(\+7|8)[\s?(]+(\d{3})[)\-\s]+(\d{3})-(\d{2})-?(\d{2})([\s(]+(доб.)\s(\d+))?|" \
                    r"(\+7|8)(\d{3})(\d{3})(\d{2})(\d{2})"
    for i in contacts_list:
        result = re.search(pattern_phone, str(i))
        if result:
            if result.group(1) and not result.group(6):
                i[5] = f"+7({result.group(2)}){result.group(3)}-{result.group(4)}-{result.group(5)}"
            elif result.group(9):
                i[5] = f"+7({result.group(10)}){result.group(11)}-{result.group(12)}-{result.group(12)}"
            elif result.group(6):
                i[5] = f"+7({result.group(2)}){result.group(3)}-{result.group(4)}-{result.group(5)} " \
                       f"{result.group(7)}{result.group(8)}"

    dict_contacts_list = {}
    new_contacts_list = []
    for i in range(1, len(contacts_list)):
        dict_contacts_list[i] = dict(zip(contacts_list[0], contacts_list[i]))
        new_contacts_list.append(dict_contacts_list[i])

    df = pd.DataFrame(new_contacts_list)

    grouped_df = df.groupby(['lastname', 'firstname']).aggregate(lambda x: ''.join(map(str, x)))

    # TODO 2: сохраните получившиеся данные в другой файл
    grouped_df.to_csv("phonebook.csv", sep=',', encoding='utf-8')


if __name__ == '__main__':
    main()
