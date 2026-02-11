import marimo

__generated_with = "0.19.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # План занятия 2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Немного про окружение
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Функции
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Стандартные функции
    """)
    return


@app.function
def my_func(x, y, z, t):
    w = x - y - z
    return w


@app.cell
def _():
    my_func(1, 2, 3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Функции с аргументами по умолчанию
    """)
    return


@app.function
def my_func_with_default_args(x, y = 20):
    return x + y


@app.cell
def _():
    my_func_with_default_args(10)
    return


@app.function
def my_func100(*args):
    return args[-1]


@app.cell
def _():
    my_func100(1,2,3,4,5,1, 10000)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Функции с именованными аргументами
    """)
    return


@app.function
def my_func_with_kargs(**kvargs):
    
    return f'{kvargs}'


@app.cell
def _():
    my_func_with_kargs(x = 1, y = 2, xyz = [1,2,3])
    return


@app.function
def my_func_with_default_list(l = []):
    return l


@app.cell
def _():
    l1 = my_func_with_default_list()
    return (l1,)


@app.cell
def _(l1):
    l1
    return


@app.cell
def _(l1):
    l1.append(1)
    return


@app.cell
def _():
    l2 = my_func_with_default_list()
    return (l2,)


@app.cell
def _(l2):
    l2.append(2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    def func_name(arg1, arg2 = 1, *args, **kvargs):
        pass
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Классы
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Минимальный класс
    """)
    return


@app.class_definition
class MyClass():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def sum(self):
        return self.x + self.y + self.z

    def __m1(self):
        print('hw')


@app.cell
def _():
    mc = MyClass(1, 2, 3)
    return (mc,)


@app.cell
def _(mc):
    [mc.x, mc.y, mc.z, mc.sum()]
    return


@app.class_definition
class MyClass2(MyClass):
    def m2(self):
        self.__m1()


@app.cell
def _():
    MyClass2(1, 2, 3).m2()
    return


@app.class_definition
class A():
    def m(self):
        print('my name is A')

    def m2(self):
        print('m2 result')


@app.cell
def _():
    A().m()
    A().m2()
    return


@app.class_definition
class B(A):
    def m(self):
        print('my name is B')


@app.cell
def _():
    B().m()
    B().m2()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Свойства
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Методы
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Конструктор
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Смоделируем вместе упрощенную модель системы управления тестирование
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.class_definition
class MyUser():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def login(self):
        print('я залогинился')

    def logout(self):
        print('я разлогинился')


@app.class_definition
class MyAdmin(MyUser):
    def remove_user(self, user):
        print(f'теперь пользователь {user.name} удолен')


@app.cell
def _():
    admin1 = MyAdmin('Кирилл', 18)
    return (admin1,)


@app.cell
def _(admin1, user1):
    admin1.remove_user(user1)
    return


@app.cell
def _():
    user1 = MyUser('Евгений', 65)
    return (user1,)


@app.cell
def _(user1):
    user1.remove_user()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
