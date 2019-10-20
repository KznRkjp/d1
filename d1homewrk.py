import requests
import sys

# import auth
# auth_params = auth.auth_params
# base_url = auth.base_url
# board_id = auth.board_id

# Данные авторизации в API Trello
auth_params = {
    'key': "",
    'token': "", }

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.
base_url = "https://api.trello.com/1/{}"
board_id = ""


def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column['name'],"(",len(task_data),")")
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

def create_col(column_name):
    r = requests.get('https://trello.com/b/'+board_id+'/reports.json',params=auth_params)
    long_board_id = r.json()['id']
    requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': long_board_id, **auth_params})

def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = []
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                #print(len(column_tasks.keys(name)))

                task_id.append(task['id'])

    # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    if len(task_id)>1:
        print("Several matches found:")
        counter = 1
        for i in task_id:
            j = requests.get(base_url.format('cards') + '/' + i, params=auth_params).json()
            k = requests.get(base_url.format('lists') + '/' + j ['idList'], params=auth_params).json()
            print(counter,': ',k['name'], '/', j['name'])
            counter+=1
        answer = input('Input number of task to move: ')
        for column in column_data:
            if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
                requests.put(base_url.format('cards') + '/' + task_id[int(answer)-1] + '/idList', data={'value': column['id'], **auth_params})
                break
def manual():
    print("Для создания задачи в списке выполните комманду: \n d1homewrk.py create \"имя списка\" \"имя задачи\" ")
    print("Для перемещения задачи между списками выполните комманду: \n d1homewrk.py move \"имя задачи\" \"имя нового списка\" ")
    print("Для создания нового списка выполните комманду: \n d1homewrk.py create_list \"имя списка\" ")

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
        manual()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_list':
        create_col(sys.argv[2])
