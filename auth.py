from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 비밀번호 해시화
        pw_hash = generate_password_hash(password)
        # 중복 검사
        if db.users.find_one({'username': username}):
            flash('이미 존재하는 사용자입니다.')
            return redirect(url_for('auth.register'))
        db.users.insert_one({
            'username': username,
            'password': pw_hash
        })
        flash('회원가입이 완료되었습니다. 로그인 해주세요.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({'username': username})
        if not user or not check_password_hash(user['password'], password):
            flash('아이디 또는 비밀번호가 잘못되었습니다.')
            return redirect(url_for('auth.login'))
        session.clear()
        session['user_id'] = str(user['_id'])
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))