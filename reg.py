# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
with open("phonebook_raw.csv") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ
titles = contacts_list[0]
values = contacts_list[1:]

full_names = [' '.join(name[:3]).strip().split() for name in values]
for name in full_names:
  if len(name) != 3:
    name.append('')

phone_number_pattern = re.compile(r'''(\+7|8)[\s-]?
                                   \(?(\d{3})\)?[\s-]?
                                   (\d{3})[\s-]?
                                   (\d{2})[\s-]?
                                   (\d{2})[\s-]*
                                   \(?((доб.)\s(\d{4}))?\)?''', re.VERBOSE)
checked = []
to_pop = []
for index, value  in enumerate(values):
  value[0] = full_names[index][0]
  value[1] = full_names[index][1]
  value[2] = full_names[index][2]
  value[-2] = str(phone_number_pattern.sub(r'+7(\2)\3-\4-\5 \7\8', values[index][-2])).strip()

  if (value[0], value[1]) in checked:
    to_pop.append(index)
    for i, row in enumerate(values): # find duplicate
        if value[0] in row and value[1] in row:
          for j in range(len(row)): # check for missed values
            if row[j] == '':
              row[j] = value[j]
              pass
  else:
    checked.append((value[0], value[1]))
shift = 0
for index_to_pop in to_pop:
  values.pop(index_to_pop-shift)
  shift += 1

contacts_list = [titles] + values

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)