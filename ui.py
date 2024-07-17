from typing import Optional

from service import *
import service
from colorama import Fore
from db import cursor
from utils import Response
from form import UserRegisterForm


def print_response(response: Response):
    color = Fore.GREEN if response.status_code == 200 else Fore.RED
    print(color + response.data + Fore.RESET)


def login_page():
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    response = service.login(username, password)
    print_response(response)


def register_page():
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    form = UserRegisterForm(username, password)
    response = service.register(form)
    print_response(response)


def logout_page():
    response = service.logout()
    print_response(response)


def add_todo():
    name = input('Enter name: ')
    description = input('Enter description: ')
    response = service.todo_add(name, description)
    print_response(response)


def update_todo(name: str, description: Optional[str] = None):
    update_todo_query = """
            insert into todo(name,description,todo_type,user_id)
            values (%s,%s,%s,%s)
        """
    cursor.execute(update_todo_query, (name, description, TodoType.PERSONAL.value, session.session.id))
    return Response('Successfully inserted todo', status_code=200)


@commit
def delete_doto(id):
    delete_doto_query = '''
    delete from todo where todo_id=%s'''
    cursor.execute(delete_doto_query, (id,))



