import json
import requests
from app.todo_types import Todo


class Request:

    def get_all_todos(self) -> list:
        response = requests.get(self.url + 'todo/all/')
        if response.status_code == 200:
            return json.loads(response.text)
        raise Exception('Сервер упал')

    def create_todo(self, data: Todo):
        responce = requests.post(self.url + 'todo/create/', data=data)
        if responce.status_code == 200:
            return
        raise Exception('Сервер упал')

    def retrieve_todo(self, id_: int) -> dict:
        responce = requests.get(self.url + f'todo/{id_}/')
        if responce.status_code == 200:
            return json.loads(responce.text)
        elif responce.status_code == 404:
            raise 0
        raise Exception('Непредвиденная ошибка')

    def delete_todo(self, id_: int):
        responce = requests.delete(self.url + f'todo/{id_}/delete/')
        if responce.status_code == 200:
            return 1
        elif responce.status_code == 404:
            return 0
        raise Exception('Непредвиденная ошибка')

    def update_todo(self, id_: int, data: Todo):
        responce = requests.put(self.url + f'todo/{id_}/update/', data=data)
        if responce.status_code == 200:
            return
        elif responce.status_code == 404:
            raise 0
        print(responce.status_code)
        # raise Exception('Непредвиденная ошибка')
