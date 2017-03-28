from . import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from flask import current_app
from datetime import datetime

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    building = db.Column(db.String(10))
    name = db.Column(db.String(20), unique=True)
    agreements = db.relationship('Agreement', backref='room', lazy='dynamic')

    def __repr__(self):
        return '<Room %r %r>' % (self.building,self.name)

    @staticmethod
    def insert_rooms():
        rooms = {
            "茶室": "15号楼",
            "会议室": "16号楼",
            "科创空间": "16号楼",
            "导师咨询室": "16号楼",
            "多功能室": "17号楼",
            "健心室": "17号楼"
        }
        for r in rooms:
            room = Room.query.filter_by(name=r).first()
            if room is None:
                room = Room(name=r)
            room.building = rooms[r]
            db.session.add(room)
        db.session.commit()


class Permission:
    ADD = 0x01
    DELSELF = 0x02
    ADDWEEKLY = 0x04
    DELALL = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod #初始化角色
    def insert_roles():
        roles = {
            'User': (Permission.ADD |
                     Permission.DELSELF , True),
            'HighUser': (
                Permission.ADD |
                Permission.DELSELF |
                Permission.ADDWEEKLY |
                Permission.DELALL , False),
            'Administrator': (0xff, False),
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

class Commit(db.Model):
    __tablename__ = 'commits'
    id = db.Column(db.Integer, primary_key=True)
    #op表示操作 True表示增加，False表示删除
    op = db.Column(db.Boolean, default=True)
    optime = db.Column(db.DateTime(), default=datetime.utcnow)
    agreement_id = db.Column(db.Integer, db.ForeignKey('agreements.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Commit %r>' % self.optime

    def __init__(self, **kwargs):
        super(Commit, self).__init__(**kwargs)
        if self.op==False:
            agr = Agreement.query.filter_by(id=self.agreement_id).first()
            agr.enable=False

class Agreement(db.Model):
    __tablename__ = 'agreements'
    id = db.Column(db.Integer, primary_key=True)
    enable =db.Column(db.Boolean,default=True)
    org = db.Column(db.String(64), index=True)
    tel = db.Column(db.String(64), index=True)
    number = db.Column(db.Integer,default=10)
    commits = db.relationship('Commit', backref='agreement', lazy='dynamic')
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    timeday = db.Column(db.Integer)
    fromtime = db.Column(db.Integer)
    totime = db.Column(db.Integer)

    def __repr__(self):
        return '<Agreement %r>' % self.org

class User(UserMixin,db.Model):
    #继承UserMixin类，获得flask_login提供的操作
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    urpid = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    commits = db.relationship('Commit', backref='user', lazy='dynamic')
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:   # 新建一个用户时给他分配角色
            if self.urpid == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    #包装一个变量的读取方法
    @property
    def password(self):
        raise AttributeError('你休想得到密码！')

    #包装一个变量的写入方法
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

class AnonymousUser(AnonymousUserMixin): #继承类
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

#回调函数，在登陆后从数据库获得id，并存在cookie里面
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

