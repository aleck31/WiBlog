from flask import render_template, make_response
from app.error import bp
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
import logging


# 自定义404错误页面
@bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('/error/err404.html'), 404


@bp.app_errorhandler(500)
def internal_server_error(error):
    # db.session.rollback()
    return render_template('/error/err500.html'), 500


# 函数 make_response()获取在视图中得到的响应对象
# def page_not_found(error):
#     resp = make_response(render_template('err404.html'), 404)
#     resp.headers['X-Something'] = 'XXXXXX-XXXX'
#     return resp


# active email logger when running without debug mode
# if not app.debug:
#     if app.config['MAIL_SERVER']:
#         auth = None
#         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
#             auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
#         secure = None
#         if app.config['MAIL_USE_TLS']:
#             secure = ()
#         mail_handler = SMTPHandler(
#             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
#             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
#             toaddrs=app.config['ADMINS'], subject='Microblog Failure',
#             credentials=auth, secure=secure)
#         mail_handler.setLevel(logging.ERROR)
#         app.logger.addHandler(mail_handler)


# log file
# if not os.path.exists('logs'):
#     os.mkdir('logs')
# file_handler = RotatingFileHandler('logs/musse.log',
#                                  maxBytes=102400,
#                                   backupCount=3)
# file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
# # 日志级别支持：DEBUG, INFO, WARNING, ERROR, CRITICAL
# file_handler.setLevel(logging.INFO)
# app.logger.addHandle(file_handler)
