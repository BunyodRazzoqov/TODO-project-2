import psycopg2
from models import UserRole, UserStatus
import utils
from session import Session
from utils import Response

db_params = {
    'database': 'n48',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': 5432
}

conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

create_user_query = """create table if not exists users(
    id serial PRIMARY KEY,
    username varchar(100) unique not null,
    password varchar(255) not null,
    "role" varchar(100) not null,
    status varchar(100) not null ,
    login_try_count int not null default 0
);
"""

create_todo_query = """create table if not exists todo(
    id serial primary key,
    name varchar(100) not null,
    description varchar(100),
    todo_type varchar(100) not null,
    user_id int not null references users(id)
);
"""


def create_table():
    cursor.execute(create_user_query)
    cursor.execute(create_todo_query)


def migrate():
    insert_admin_user_query = """
    insert into users(username, password, role, status, login_try_count)
    values (%s,%s,%s,%s,%s);
    """
    user_data = ('admin', utils.hash_password('123'), UserRole.ADMIN.value, UserStatus.ACTIVE.value, 0)
    cursor.execute(insert_admin_user_query, user_data)
    conn.commit()


def init():
    create_table()
    migrate()


def commit(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        conn.commit()
        return result

    return wrapper


session = Session()


def is_authenticated(func):
    def wrapper(*args, **kwargs):
        if not session.session:
            return Response('Not authenticated', status_code=404)
        result = func(*args, **kwargs)
        return result

    return wrapper


if __name__ == '__main__':
    init()
