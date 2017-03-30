#!/usr/bin/env python
import os
""""""
#首字母大写都是类，小写都是对象
from app import create_app, db
#从app/__init__.py（后面的就不加）中导入应用和数据库
from app.models import User, Role, Commit , Agreement , Room
#从app.models（数据库模型）中导入用户和角色
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#如果已经定义了环境变量flask_config，则从中读取配置，否则使用默认值


from flask_script import Manager, Shell
manager = Manager(app) #Manger是一个管理类，通过这个类生成一个对象
#manager启动程序的对象

from flask_migrate import Migrate, MigrateCommand
migrate = Migrate(app, db)
#数据库迁移对象

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Commit=Commit , Agreement=Agreement , Room=Room )
#默认有runserver，我们增加了shell和db选项
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def init_test():
    db.drop_all()
    db.create_all()
    Role.insert_roles()
    Room.insert_rooms()
    print("wwwwwwwwwwwwwwwwwww")
    users = {
        "16300240019": "严佳雯",
        "15307130371": "王佳羽",
        "16307130026": "张天翔"
    }
    for id in users:
        user = User(urpid=id)
        user.username = users[id]
        user.password = id
        db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
