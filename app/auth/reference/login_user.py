from flask import render_template,session, make_response, redirect,escape, url_for, request, flash
from app import bp


@bp.route('/login')
# 用户名密码验证
def login():
    errmsg = None
    user = {'username': 'demo',
            "password": 'demo123'
            }  # fake user
    if request.method == 'POST':
        if request.form['username'] != user.get('username') or \
                request.form['password'] != user.get('password'):
            errmsg = 'Invalid username/password'
        else:
            # 存储username到session
            session['username'] = request.form['username']
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return render_template("login.html", errmsg=errmsg)

    # 存储username到cookies
    # resp = make_response(render_template("index.html",title = 'Home',user=user))
    # resp.set_cookie('username', 'admin2')
    # return resp

@bp.route('/')
def index():
    # 存储username到session
    if  'username' in session:
        # 从 session 读取 username
        username = escape(session['username'])
        # 从cookies读取username
        # username = request.cookies.get('username')
        return render_template("index.html",title = 'Home',uname= username)
    else:
        return redirect(url_for('login'))



@bp.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))