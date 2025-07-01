# 베이스 이미지
FROM python:3.9-slim

# 작업 디렉터리 설정
WORKDIR /app

# 종속성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# 컨테이너 내부 포트 설정
EXPOSE 5000

# 런타임 환경 변수는 docker run 시 주입
# 예: docker run --env-file .env -p 5000:5000 wish-tree:latest

# 애플리케이션 실행
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()"]
