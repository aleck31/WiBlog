from flask import render_template, url_for, request
from app.main import bp
from app import app, lm
from app.models import Post


@bp.route('/')
@bp.route('/index/')
# 增加login_required装饰器,表明该页面只有登录用户才能访问
def index():
    lm.login_message = '请登录！'
    # 使用 paginate()方法对posts内容进行分页显示
    page = request.args.get('page', 1, type=int)
    size = app.config['POSTS_PER_PAGE']
    posts = Post.query.filter_by(status=1).order_by(Post.timestamp.desc()).paginate(page, size, False)
    # 生成页面导航url
    prev_url = url_for('.index', page=posts.prev_num) \
        if posts.has_prev else None
    next_url = url_for('.index', page=posts.next_num) \
        if posts.has_next else None
    return render_template("index.html",
                           title='Home',
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url)
