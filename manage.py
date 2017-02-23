#!/usr/bin/env python

from flask_script import Manager,Shell
from app import create_app

app = create_app('default')
print(app.url_map)
manager = Manager(app)


if __name__ == '__main__':
    print("run server")
    manager.run()
