from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from models import init_db, get_db
from auth import auth_bp
from bson import ObjectId
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')
    init_db(app)
    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return redirect(url_for('auth.login'))

    @app.route('/dashboard')
    def dashboard():
        db = get_db()
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('auth.login'))
        goal = db.goals.find_one({'user_id': ObjectId(user_id)}, sort=[('created_at', -1)])
        if not goal:
            return render_template('dashboard.html', stage=0)
        return render_template(
            'dashboard.html',
            stage=goal.get('growth_stage', 1),
            current=goal.get('current_value', 0),
            target=goal.get('target_value', 0),
            goal_id=str(goal['_id'])
        )

    @app.route('/goals', methods=['POST'])
    def create_goal():
        db = get_db()
        user_id = session.get('user_id')
        data = request.form
        goal = {
            'user_id': ObjectId(user_id),
            'title': data['title'],
            'target_value': float(data['target_value']),
            'current_value': 0.0,
            'growth_stage': 1,
            'created_at': datetime.utcnow()
        }
        db.goals.insert_one(goal)
        return redirect(url_for('dashboard'))

    @app.route('/goals/<goal_id>/progress', methods=['POST'])
    def update_progress(goal_id):
        db = get_db()
        inc = float(request.form.get('increment', 0))
        goal = db.goals.find_one({'_id': ObjectId(goal_id)})
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        new_val = goal['current_value'] + inc
        ratio = min(new_val / goal['target_value'], 1.0)
        stage = int(ratio * 5) if ratio < 1 else 5
        db.goals.update_one(
            {'_id': ObjectId(goal_id)},
            {'$set': {'current_value': new_val, 'growth_stage': stage}}
        )
        return redirect(url_for('dashboard'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
