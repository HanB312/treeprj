import os
from pymongo import MongoClient
from flask import current_app


def init_db(app):
    """
    Flask 앱에 MongoDB 연결을 설정하고, app.db 속성으로 클라이언트 인스턴스를 저장
    """
    mongo_uri = os.environ.get("MONGO_URI")
    client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
    # 사용할 데이터베이스 이름: wish_tree
    app.db = client.get_database("wish_tree")


def get_db():
    """현재 Flask 애플리케이션 컨텍스트에서 MongoDB 데이터베이스 객체를 반환"""
    return current_app.db
