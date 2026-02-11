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
def my_func(x, y):
    return x + y


@app.cell
def _():
    my_func(1, 2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Функции с аргументами по умолчанию
    """)
    return


@app.function
def my_func_with_default_args(x, y = 2):
    return x + y


@app.cell
def _():
    my_func_with_default_args(10)
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
    my_func_with_kargs(x = 1, y = 2)
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


@app.cell
def _(self):
    def MyClass():
        def __init__(x, y):
            self.x = x
            self.y = y

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


if __name__ == "__main__":
    app.run()
