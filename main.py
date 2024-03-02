import csv
import re
from collections import defaultdict
from pprint import pprint

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",", quotechar='"')
    contacts_list = list(rows)

# создаем словарь для хранения уникальных записей
contacts_dict = defaultdict(list)

for contact in contacts_list[1:]:
    # разделяем ФИО на отдельные элементы
    fullname = " ".join(contact[:3]).split()
    # приводим телефон к нужному формату
    phone = re.sub(r"(\+7|8)\s*\(?(\d{3})\)?\s*-?(\d{3})-?(\d{2})-?(\d{2})(\s*\(?(доб.)?\s*(\d{4})\)?)?", r"+7(\2)\3-\4-\5 \6\8", contact[5]).strip()
    # удаляем дублирование в добавочном номере
    phone = re.sub(r"(доб. )(\d{4})\2", r"\1\2", phone) 
    
    # удаляем скобки вокруг добавочного номера
    phone = re.sub(r"\((доб. \d{4})\)", r"\1", phone)

    # проверяем, содержит ли поле телефона адрес электронной почты
    if "@" in phone:
        phone, email = phone.split(", ")
        phone = phone.replace("  ", " ").replace("доб. ", "доб.")
    else:
        email = contact[6]
    # добавляем запись в словарь
    key = tuple(fullname[:2])  # ключ - это кортеж (Фамилия, Имя)
    value = fullname[2:] + contact[3:5] + [phone] + [email]
    if key in contacts_dict:
        for i, item in enumerate(value):
            if item and not contacts_dict[key][i]:
                contacts_dict[key][i] = item
            elif item and i == len(value) - 2:  # если это поле телефона
                contacts_dict[key][i] += ", " + item  # добавляем телефон
            elif item and i == len(value) - 1:  # если это поле email
                contacts_dict[key][i] = item  # заменяем email
    else:
        contacts_dict[key] = value

# преобразуем словарь обратно в список
contacts_list = [list(key) + value for key, value in contacts_dict.items()]
contacts_list.insert(0, ["lastname", "firstname", "surname", "organization", "position", "phone", "email"])

pprint(contacts_list)

# сохраняем получившиеся данные в другой файл
with open("phonebook.csv", "w", newline='', encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    datawriter.writerows(contacts_list)
