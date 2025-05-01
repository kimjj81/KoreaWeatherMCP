"""
메인 실행 모듈
"""
import sys
from korea_weather.server import WeatherMCP

def main():
    """MCP 서버 실행"""
    server = WeatherMCP()
    server.run()

if __name__ == "__main__":
    sys.exit(main()) 