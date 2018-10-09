from flask import render_template, request, url_for, redirect, flash, g
from flask_login import login_required
# from werkzeug import secure_filename
from app.main import bp
from app import app, db
from .forms import PostForm
from app.models import Post


@bp.route('/posts/', methods={'GET', 'POST'})
@login_required
def ls_posts():
    # postform to create new post
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        p = Post(title, body, g.user.id)
        p.timestamp = form.timestramp.data
        if form.draft.data:
            p.status = 0
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('.ls_posts'))
    # list posts using paginate()方法对内容分页
    page = request.args.get('page', 1, type=int)
    size = app.config['POSTS_PER_PAGE']
    posts = g.user.get_posts(1).paginate(page, size, False)
    # 生成页面导航url
    if posts.has_prev:
        prev_url = url_for('.ls_posts', page=posts.prev_num)
    else:
        prev_url = None
    # if...else...语句简化写法
    next_url = url_for('.ls_posts', page=posts.next_num) \
        if posts.has_next else None
    return render_template("posts.html",
                           title='Posts',
                           posts=posts.items,
                           next_url=next_url,
                           prev_url=prev_url,
                           np_form=form)


@bp.route('/posts/<int:post_id>')
@login_required
def show_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('不存在文章：ID_' + post_id + '！')
        return redirect(url_for('.posts'))
    # show the post with the given id, the id is an integer
    return render_template("singlepost.html",
                           post=post,
                           post_url=url_for('.show_post', post_id=post_id, _external=True))


# @app.route('/posts/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files["the_file"]
#         f.save('uploads' + secure_filename(f.filename))
#     else:
#         return
#     pass

# @app.route('/posts98234/')
# def foo3():
#     pass
#
# with app.test_request_context():
#     print(url_for('foo3'))
