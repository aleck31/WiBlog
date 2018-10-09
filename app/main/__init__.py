from flask import Blueprint

bp = Blueprint('main', __name__)

# 导入视图函数
from app.main import index, posts, search
