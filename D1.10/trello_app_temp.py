import sys
import requests

#----------------------
# консольный клиент должен показывать колонки нашей доски, задачи в колонках, и уметь эти задачи между колонками перемещать.
#----------------------

# Данные авторизации в API Trello
auth_params = {
  'key': "*****",
  'token': "*****", }

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.
base_url = "https://api.trello.com/1/{}"
board_id = "******"

def read():
  # Получим данные всех колонок на доске:
  column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
  # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
  for column in column_data:
    task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
    string = 'Колонка "{}". Количество задач: {}.'.format(column['name'], len(task_data))
    print(string)
    # Получим данные всех задач в колонке и перечислим все названия

    if not task_data:
      print('\t' + 'Нет задач!')
      continue
    for task in task_data:
      print('\t' + task['name'])

def create(name, column_name):
  # Получим данные всех колонок на доске
  column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

  # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
  for column in column_data:
    if column['name'] == column_name:
      # Создадим задачу с именем _name_ в найденной колонке
      requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
    break

# creating column
def create_column(column_name):
  # Создадим задачу с именем _name_ в найденной колонке
  request = requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': column_name, **auth_params})

def move(name, column_name):
  # Получим данные всех колонок на доске
  column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

  # Среди всех колонок нужно найти задачу по имени и получить её id
  task_id = find_task(name)
  # for column in column_data:
  #   column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
  #   for task in column_tasks:
  #     if task['name'] == name:
  #       task_id = task['id']
  #       break
  #   if task_id:
  #     break

  # Теперь, когда у нас есть id задачи, которую мы хотим переместить
  # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
  for column in column_data:
    if column['name'] == column_name:
      # И выполним запрос к API для перемещения задачи в нужную колонку
      requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
      break

def find_task(name):
  # Получим данные всех колонок на доске
  column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
  # Среди всех колонок нужно найти задачи с указанным именем и добавить их в массив
  task_arr = []

  for column in column_data:
    column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
    for task in column_tasks:
      #print('\n' + task['name'])
      if task['name'] == name:
        task_arr.append(task)

    #print(len(task_arr))

  if len(task_arr) == 1:
    return task_arr[0]['id']
  elif len(task_arr)   == 0:
    print('Карточки с таким именем не найдено')
  else:
    serial_number = 0
    print('Найдено несколько карточек с таким именем:')
    for task in task_arr:
      serial_number += 1
      column_id = task['idList']
      column_name = None

      for column in column_data:
        if column['id'] == column_id:
          column_name = column['name']

      string = '{}.{}, в колонке "{}", id: {}'.format(serial_number, task['name'], column_name, task['id'])
      print('\t' + string)
    task_number = int(input('Выбирете нужную и введите ее порядковый номер'))

    return task_arr[task_number - 1]['id']



if __name__ == "__main__":
  if len(sys.argv) <= 2:
    read()
  elif sys.argv[1] == 'create':
    create(sys.argv[2], sys.argv[3])
  elif sys.argv[1] == 'move':
    move(sys.argv[2], sys.argv[3])
  elif sys.argv[1] == 'create_column':
    create_column(sys.argv[2])

# python3 trello_app.py create 'Кран' 'Нужно сделать'
# python3 trello_app.py move 'Покормить крокодилов' 'В процессе'
# python3 trello_app.py move 'Покормить крокодилов' 'Сделано'
# python3 trello_app.py read
# python3 trello_app.py create_column 'Сделано'
