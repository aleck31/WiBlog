from flask import render_template, session, redirect, flash, url_for, request, g
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import login_user, logout_user, current_user
from app import bp, db, lm, oid
from app.models import User,ROLE_USER
from flask_openid import OpenID

oid = OpenID(bp, os.path.join(BASEDIR, 'tmp'))


class LoginForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    submit = SubmitField('Submit')
    remember_me = BooleanField('Remember_me', default=False)


# 从数据库加载用户
@lm.user_loader
def load_user(uid):
    return User.query.get(int(uid))


# Flask-Login设定的全局变量current_user复制给g变量
@bp.before_request
def before_request():
    g.user = current_user


# 装饰器：oid.loginhandler 告诉Flask-OpenID这是登录视图函数
@bp.route('/login/', methods={'GET', 'POST'})
@oid.loginhandler
# openid 验证
def login():
    # 在一个request的生命周期中用Flask的g对象来保存和共享数据
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    errmsg = None
    form = LoginForm()
    if form.validate_on_submit():
        # flash('Login requested for OpenID:"' + form.openid.data + '",remember_me=' + str(form.remember_me.data))
        # 保持remember_me的布尔值到Flask的session中
        session['remember_me'] = form.remember_me.data
        # oid.try_login通过Flask-OpenID来执行用户认证
        return oid.try_login(form.openid.data, ask_for=['username', 'email'])
    return render_template("login.html",
                           title='Login',
                           lg_form=form,
                           errmsg=errmsg,
                           providers=bp.config['OPENID_PROVIDERS']
                           )


# Flask-OpenID登录回调
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    # 如果email在数据库找不到，在数据库增加一个新的用户
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        username = resp.username
        if username is None or username == "":
            username = resp.email.split('@')[0]
        user = User(username=username, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    # 从Flask session中获取remember_me的值
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    # 调用Flask-Login的login_user方法，来注册这个有效的登录
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


###################################################
# login.html
#     <script type="text/javascript">
#     function set_openid(openid, pr)
#     {
#         u = openid.search('<nickname>')
#         if (u != -1) {
#             <!--// openid requires nickname -->
#             user = prompt('Enter your ' + pr + ' nickname:')
#             openid = openid.substr(0, u) + user
#         }
#         lg_form = document.forms['login'];
#         lg_form.elements['openid'].value = openid
#     }
#     </script>