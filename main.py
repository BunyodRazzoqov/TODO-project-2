import time


# def my_custom_decorator(func):
#     def wrapper(*args, **kwargs):
#         for i in ['A', 'B', 'C', 'D', 'E']:
#             print(i)
#         func()
#         print('Stopping')
#
#     return wrapper
#
#
# @my_custom_decorator
# def say_hello():
#     print('Hello Guys')
#
# say_hello()
# def decorator(func):
#     def wrapper(*args, **kwargs):
#         print('running before func funciton')
#         result = func(*args, **kwargs)
#         return result
#
#     return wrapper
#
#
# @decorator
# def say_hello(name):
#     return f"Hello {name}!"
#
#
# print(say_hello('John'))
def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Elapsed time: {end - start}\'s  => {func.__name__}')
        return result

    return wrapper


@timing
def primary_function(son, daraja):
    return son ** daraja


print(primary_function(2, 24244224))
