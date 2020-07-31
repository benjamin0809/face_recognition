# -*- coding:utf-8 -*-
from importlib import reload
from src.router import get_define_app

app = get_define_app()


@app.route('/', methods=['GET'])
def index():
    return 'hello world'
    # return picture_url


if __name__ == '__main__':
    app.run()





