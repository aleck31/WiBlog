import os
from config import BASEDIR


# 配置文件中只有大写名称的值才会被存储到配置对象中
class ConfSets(object):
    # Web服务器参数
    DEBUG = True
    # SERVER_NAME = "musse.local:80"
    # APPLICATION_ROOT = None

    # set the secret key.
    SECRET_KEY = os.urandom(24)
    # app.secret_key = 'A3Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    # WTF参数
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = SECRET_KEY

    # SQLALCHEMY参数
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xxxxx@localhost:3306/test?charset=utf8'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 翻页参数
    POSTS_PER_PAGE = 5

    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@myners.net']

    # Openid config
    OPENID_PROVIDERS = [
        {'name': 'OpenID.cn', 'url': 'http://openid.org.cn/<username>'},
        {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
        {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
        {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
        {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
        {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
