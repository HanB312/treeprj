from dotenv import load_dotenv
load_dotenv()

import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
from bson import ObjectId

# 환경 변수로 설정된 MONGO_URI 사용
client = MongoClient(os.environ.get("MONGO_URI"))

db = client["wish_tree"]

# 1) 비밀번호 해시 생성 (모두 동일한 비밀번호 사용)
encrypted_pwd = generate_password_hash("test123")

# 2) 사용자 5명 생성
test_users = []
for i in range(1, 6):
    test_users.append({
        "_id": ObjectId(),
        "username": f"user{i}",
        "password": encrypted_pwd
    })
b = db
b.users.insert_many(test_users)

# 3) 각 사용자 별 2개 목표 생성 (총 10개)
test_goals = []
for user in test_users:
    for idx in range(1, 3):
        target = 100.0 * idx
        current = 10.0 * (idx - 1)
        ratio = min(current / target, 1.0)
        stage = int(ratio * 5) if ratio < 1 else 5
        test_goals.append({
            "_id": ObjectId(),
            "user_id": user["_id"],
            "title": f"Goal{idx}_for_{user['username']}",
            "target_value": target,
            "current_value": current,
            "growth_stage": max(stage, 1),
            "created_at": datetime.utcnow()
        })
    
# 목표 삽입
b.goals.insert_many(test_goals)

from pprint import pprint
pprint({
    "users_inserted": len(test_users),
    "goals_inserted": len(test_goals)
})