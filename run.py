#!flask/bin/python from app import app
from flask_script import Manager
from flask_migrate import MigrateCommand
from app import app


# 为app添加db命令用于数据库更新
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # app.debug = True
    # app.run(host='0.0.0.0')
    manager.run()
