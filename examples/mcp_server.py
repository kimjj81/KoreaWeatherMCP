"""
MCP 서버 실행 예제
"""
import os
from dotenv import load_dotenv
from korea_weather.server import WeatherMCP

def main():
    """기상청 중기예보 MCP 서버 실행"""
    # 환경변수 로드
    load_dotenv()
    
    # API 키 확인
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        print("경고: WEATHER_API_KEY 환경변수가 설정되지 않았습니다.")
        print("API 호출 시 오류가 발생할 수 있습니다.")
    
    # MCP 서버 초기화 및 실행
    server = WeatherMCP()
    server.run()

if __name__ == "__main__":
    main() 