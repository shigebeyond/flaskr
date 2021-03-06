import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'password is required.'
        if error is None:
            try:
                db.execute("insert into user(username,password) values(?,?)",
                           (username, generate_password_hash(password)),
                           )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered"
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template('/auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('select * from user where username=?', (username, )).fetchone()
        if user is None:
            error = "Incorrect username"
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')


# 在登录之前先检查用户id是否存在
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'select * from user where id=?', (user_id, )
        ).fetchone()

# 注销
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 在其他视图中验证
# 用户登录以后才能创建、编辑和删除博客帖子，在每个视图中可以使用装饰器来完成这个工作。
# 装饰器返回一个新的视图，该视图包含了传递给装饰器的原视图。新的函数检查用户是否已载入，如果已载入，那么就继续正常执行原视图，否则就重定向到登录页面
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))  # 使用蓝图室，蓝图的名称会添加到函数名称的前面。这里的auth.login已被加入‘auth’
        return view(**kwargs)

    return wrapped_view