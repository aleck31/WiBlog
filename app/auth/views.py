from flask import render_template, session, redirect, flash, url_for, request, escape, g
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db, lm
from app.models import User
from app.auth import bp
from .forms import LoginForm, RegForm, ProfileForm


@lm.user_loader
# 从数据库加载到一个用户
def load_user(id):
    return User.query.get(int(id))


@bp.route('/login/', methods={'GET', 'POST'})
def login():
    # 在一个request的生命周期中用Flask的g对象来保存和共享数据
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('main.index'))
    errmsg = None
    form = LoginForm()
    # 从 session 读取 remember_me ，代码执行效果有问题！！！
    if 'remember_me' in session:
        form.remember_me.data = escape(session['remember_me'])
        # lgform.username.data = escape(session['username'])
    if form.validate_on_submit():
        # 保存remember_me的布尔值到Flask的session中
        remember_me = form.remember_me.data
        session['remember_me'] = remember_me
        user = User.query.filter_by(username=form.username.data).first()
        # 验证用户名、密码有效性
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        # 调用Flask-Login的login_user方法注册有效的登录
        login_user(user, remember_me)
        flash('Logged in successfully.')
        if g.user.is_authenticated:
            g.user.last_login = datetime.utcnow()
            db.session.commit()
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template("/auth/login.html",
                           title='Login',
                           lg_form=form
                           )


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# 用户管理
@bp.route('/register/', methods={'GET', 'POST'})
def reg_user():
    if g.user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        role = int(form.role.data)
        u = User(username, email, role)
        if form.nickname.data is not None:
            u.nickname = form.nickname.data
        else:
            u.nickname = username   #nickname 默认值
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Congratulations! you can login by your registered account.')
        return redirect(url_for('.login'))
    return render_template('/auth/register.html',
                           title='Register',
                           form=form
                           )


@bp.route('/user/', methods={'GET', 'POST'})
@login_required
def user():
    form = ProfileForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('.user'))
    elif request.method == 'GET':
        form.email.data = g.user.email
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    posts = g.user.get_posts(all)
    return render_template('/auth/user.html',
                           title="User Profile",
                           form=form,
                           posts=posts)

