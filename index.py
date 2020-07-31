# -*- coding:utf-8 -*-
from importlib import reload
from src.router import get_define_app

app = get_define_app()


if __name__ == '__main__':
    app.run()





