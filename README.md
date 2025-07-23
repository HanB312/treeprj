
# 🌳 소원나무 키우기 프로젝트

소원나무 프로젝트는 개인이 목표를 설정하고, <br>목표 달성 과정을 시각적인 나무의 성장 단계로 표현하여 동기부여를 주는 서비스입니다.

학부 시절 미흡했던 목표 관리 로직과 DB 연동 문제를 개선하여, <br>Google Cloud Platform과 MongoDB Atlas를 활용해 개발했습니다.

---

## 📌 프로젝트 목적

* 개인의 목표 달성을 재미있고 직관적으로 돕는 서비스 제공
* 목표 설정부터 단계별 진행도를 시각적으로 제공하여 사용자의 목표 달성률 증가 유도

---

## 🎯 주요 기능

| 기능               | 상세 설명                                   |
| ---------------- | --------------------------------------- |
| 사용자 인증           | 회원가입, 로그인, 로그아웃 구현 <br>비밀번호 해시 처리       |
| 목표 설정 및 관리       | 목표 등록 및 목표 수치 입력, 목표 수정 및 달성 관리         |
| 진행도 시각화          | 진행도를 0\~5 단계의 나무 성장 이미지로 시각화            |
| 달성량 관리           | 매일 물주기 버튼으로 진행도를 1 증가시키고 퍼센트로 표시        |
| 목표 달성 시 신규 목표 추천 | 목표 달성 후 유사 목표(±20%)를 추천하여 지속적인 목표 설정 유도 |

---

## 🛠 기술 스택 및 개발 환경

| 구분            | 기술 스택 및 도구                                                       |
| ------------- | ---------------------------------------------------------------- |
| 언어 및 프레임워크    | Python, Flask                                                    |
| 데이터베이스        | MongoDB Atlas                                                    |
| 클라우드 플랫폼      | Google Cloud Platform(GCP)                                       |
| 컨테이너          | Docker, Dockerfile                                               |
| 버전 관리 및 CI/CD | GitHub, Git, GCP Cloud Build                                     |
| 패키지 관리        | pip, requirements.txt, python-dotenv, pymongo, certifi, gunicorn |
| 배포 환경         | GCP App Engine(Standard), Cloud Run                              |

---

## 🚀 프로젝트 배포 방법

### 사전 준비

1. Git 클론

```bash
git clone https://github.com/HanB312/treeprj.git
cd wish-tree
```

2. Python 가상 환경 설정

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. 환경 변수 설정 (`.env` 파일)

```env
MONGO_URI=your_mongodb_uri
SECRET_KEY=your_secret_key
```

### 로컬 실행

```bash
flask run --host=0.0.0.0 --port=8080
```

### Docker로 실행

```bash
docker build -t wish-tree:latest .
docker run -d -p 8080:5000 --env-file .env wish-tree:latest
```

---

## 📝 배운 점 및 성과

* MongoDB Atlas와 Flask 연동 과정에서 발생한 SSL/TLS 인증 문제를 OpenSSL 업그레이드 및 certifi를 활용하여 해결함
* 환경변수 관리를 python-dotenv로 자동화하여 보안을 강화하고 배포의 편의성을 높임

---

## 📂 프로젝트 구조

```plaintext
wish-tree/
├── app.py                   # 메인 애플리케이션 파일
├── auth.py                  # 회원가입/로그인 처리 모듈
├── models.py                # MongoDB 연결 모듈
├── requirements.txt         # 의존성 패키지 목록
├── Dockerfile               # Docker 이미지 정의 파일
├── app.yaml                 # App Engine 배포 설정
├── templates/               # HTML 템플릿 폴더
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
└── static/                  # 정적 파일 폴더
    ├── tree0.png ~ tree5.png
```



---

## 🖋️ 작성자 및 연락처

* 이름: 이한별
* GitHub: [GitHub Profile](https://github.com/HanB312)


