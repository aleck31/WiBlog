from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from hashlib import md5
from datetime import datetime
from app import db


ROLE_USER = 0
ROLE_ADMIN = 1


# 继承userMixin的默认方法和属性
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER, nullable=False)
    password_hash = db.Column(db.String(128))
    nickname = db.Column(db.String(64))
    avatar_hash = db.Column(db.String(32))
    about_me = db.Column(db.String(140))
    last_login = db.Column(db.DateTime)
    # 实用！1、u.posts 返回u的所有posts  2、post.author 返回 p的user
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username, email, role):
        self.username = username
        self.email = email
        self.role = role

    def get_id(self):
        # return unicode(self.uid)
        return self.id

    # 密码哈希转换
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    # 获取用户posts，范围 all,1,0
    def get_posts(self, range=all):
        if range == all:
            my_posts = self.posts
        else:
            my_posts = Post.query.filter_by(author_id=self.id, status=int(range))
        return my_posts.order_by(Post.timestamp.desc())

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    body = db.Column(db.String(1024))
    # utcnow后不带()，将函数本身传递给default
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 发布状态，0-草稿，1-发布
    status = db.Column(db.SmallInteger, default=1)
    # 定义外链，此处用 表名.字段名
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.author_id = user_id

    def set_boby(self, body):
        self.body = body

    def __repr__(self):
        return '<Post {}>'.format(self.title)
        # return '<Post %r>' % self.title
