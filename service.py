from typing import Optional

from session import Session
from db import cursor, conn, commit, is_authenticated
from models import User, UserRole, UserStatus, TodoType
from utils import Response, match_password, hash_password
from validators import check_validation

session = Session()


@commit
def login(username: str, password: str):
    user: User | None = session.check_session()
    if user:
        return Response('You already logged in', 404)
    get_user_by_username = '''
    select * from users where username = %s;
    '''
    cursor.execute(get_user_by_username, (username,))
    user_data = cursor.fetchone()
    if not user_data:
        return Response('User not found', 404)
    user = User.from_tuple(user_data)

    if user.login_try_count >= 3:
        update_status_query = '''update users set status = %s where username = %s;'''
        cursor.execute(update_status_query, (UserStatus.BLOCK.value, username,))
        return Response('User is blocked', status_code=404)

    if not match_password(password, user.password):
        update_user_query = '''
        update users set login_try_count = login_try_count + 1 where username = %s;
        '''
        cursor.execute(update_user_query, (username,))
        return Response('Wrong Password', 404)
    session.add_session(user)
    return Response('User successfully logged in', 200)


@commit
def register(form):
    check_validation(form)

    check_user_on_create_query = '''
        select * from users where username = %s;
    '''
    cursor.execute(check_user_on_create_query, (form.username,))
    user_data = cursor.fetchone()
    if user_data:
        return Response('Username already registered', 404)

    register_user_query = '''
    insert into users(username, password, role, status, login_try_count)
    values (%s,%s,%s,%s,%s);
    '''
    data = (form.username, hash_password(form.password), UserRole.USER.value, UserStatus.ACTIVE.value, 0)
    cursor.execute(register_user_query, data)
    return Response('User successfully registered', status_code=200)


def logout():
    global session
    if session:
        session.session = None
        return Response('Successfully logged out', status_code=200)
    return Response('Session Not Found', status_code=404)


# CRUD TODO

@is_authenticated
@commit
def todo_add(name: str, description: Optional[str] = None):
    insert_todo = """
        insert into todo(name,description,todo_type,user_id)
        values (%s,%s,%s,%s)
    """
    cursor.execute(insert_todo, (name, description, TodoType.PERSONAL.value, session.session.id))
    return Response('Successfully inserted todo', status_code=200)
