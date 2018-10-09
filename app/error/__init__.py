from flask import Blueprint

bp = Blueprint('error', __name__,
               # template_folder='templates',
               # static_folder='static',
               url_prefix='/admin')

from app.error import handles
