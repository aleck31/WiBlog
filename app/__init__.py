from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_moment import Moment
from config import default


app = Flask(__name__)
# 加载配置文件
app.config.from_object(default)

# 创建db实例
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# login manager needs be set before blueprint registration
lm = LoginManager()
lm.session_protection = "strong"
lm.login_view = 'auth.login'
# lm.blueprint_login_views = {
#     'main': 'auth.login',
#     'admin': 'admin.login'
# }
lm.init_app(app)

# 为各flask扩展创建实例
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)

# 导入db models
from app import models

# 导入&注册蓝图
from app.auth import bp as bp_auth
app.register_blueprint(bp_auth, url_prefix='/auth')

from app.main import bp as bp_main
app.register_blueprint(bp_main)

from app.error import bp as bp_erro
app.register_blueprint(bp_erro)

# from admin import bp as bp_admn
# app.register_blueprint(bp_admn)

# before_request reads your session, gets user id, loads the user with user_loader and set it to current_user or
# AnonymousUser ,这里将Flask-Login设定的全局变量current_user复制给g变量
@app.before_request
def before_request():
    g.user = current_user

