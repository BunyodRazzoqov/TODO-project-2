from ui import login_page, register_page, logout_page, add_todo

while True:
    print('Login to page => 1')
    print('Register page => 2')
    print('Logout page   => 3')
    print('Add todo page => 4')
    print('Exit          => 5')
    choice = input('enter your choice : ')
    if choice == '1':
        login_page()
    elif choice == '2':
        register_page()
    elif choice == '3':
        logout_page()
    elif choice == '4':
        add_todo()
    elif choice == '5':
        break
