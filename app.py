from dotenv import load_dotenv
load_dotenv()

import os
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash
from bson.objectid import ObjectId

from models import init_db, get_db
from auth import auth_bp

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('로그인이 필요합니다.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def get_similar_goals(current_goal, limit=5):
    db = get_db()
    target = current_goal['target_value']
    lower = int(target * 0.8)
    upper = int(target * 1.2)
    sims = db.goals.find({
        'user_id': {'$ne': current_goal['user_id']},
        'target_value': {'$gte': lower, '$lte': upper}
    }).sort('created_at', -1).limit(limit)
    return list(sims)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY")

    # MongoDB 연결 초기화
    init_db(app)
    # 회원가입/로그인 블루프린트 등록
    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        # 1) 비로그인 사용자는 환영 화면 (로그인/회원가입 링크) 보여주기
        if 'user_id' not in session:
            return render_template('index.html', first_goal=False)

        # 2) 로그인된 사용자는 목표가 있는지 확인
        db = get_db()
        user_id = session['user_id']
        has_goal = db.goals.find_one({'user_id': ObjectId(user_id)}) is not None

        # 2-1) 목표 없으면 첫 목표 등록 폼
        if not has_goal:
            return render_template('index.html', first_goal=True)

        # 2-2) 목표 있으면 대시보드로 이동
        return redirect(url_for('dashboard'))
    

    @app.route('/goals', methods=['POST'])
    @login_required
    def create_goal():
        db = get_db()
        user_id = session['user_id']
        title = request.form.get('title')
        target_value = int(request.form.get('target_value', 1))
        goal = {
            'user_id': ObjectId(user_id),
            'title': title,
            'target_value': target_value,
            'current_value': 0,
            'growth_stage': 1,
            'created_at': datetime.utcnow()
        }
        db.goals.insert_one(goal)
        flash('✅ 새 목표가 등록되었습니다.')
        return redirect(url_for('dashboard'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        db = get_db()
        user_id = session['user_id']
        goal = db.goals.find_one(
            {'user_id': ObjectId(user_id)},
            sort=[('created_at', -1)]
        )
        if not goal:
            flash('등록된 목표가 없습니다.')
            return redirect(url_for('index'))

        completed = goal.get('current_value', 0)
        target = goal.get('target_value', 1)
        percent = int(completed / target * 100) if target else 0

        # 목표 달성 시 유사 목표 추천
        similar_goals = get_similar_goals(goal) if completed >= target else []

        return render_template(
            'dashboard.html',
            goal=goal,
            completed=completed,
            percent=percent,
            similar_goals=similar_goals
        )

    @app.route('/goals/<goal_id>/water', methods=['POST'])
    @login_required
    def water(goal_id):
        db = get_db()
        goal = db.goals.find_one({'_id': ObjectId(goal_id)})
        if not goal:
            flash('목표를 찾을 수 없습니다.')
            return redirect(url_for('dashboard'))

        # 진행도 1 증가 (최대 target_value 까지)
        new_value = min(goal.get('current_value', 0) + 1, goal.get('target_value', 0))
        ratio = new_value / goal['target_value'] if goal.get('target_value', 0) else 0
        new_stage = min(int(ratio * 5), 5)

        db.goals.update_one(
            {'_id': ObjectId(goal_id)},
            {'$set': {
                'current_value': new_value,
                'growth_stage': new_stage
            }}
        )
        flash('💧 물주기 완료! 진행도가 1만큼 증가했습니다.')
        return redirect(url_for('dashboard'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8000))
    )
