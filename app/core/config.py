import os
from dotenv import load_dotenv
from pathlib import Path

# .env 파일 로드 시도
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# 기상청 API 설정
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
WEATHER_API_ENDPOINT = os.getenv('WEATHER_API_ENDPOINT', 'https://apis.data.go.kr/1360000/MidFcstInfoService')

# 서버 설정
API_V1_STR = '/api/v1'
PROJECT_NAME = '기상청 중기예보 MCP 서버' 