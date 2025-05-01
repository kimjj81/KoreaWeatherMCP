"""
기본 클라이언트 사용 예제
"""
import asyncio
import json
import os
from korea_weather.client import WeatherClient

async def main():
    """기상청 중기예보 클라이언트 예제"""
    # API 키 환경변수에서 가져오기
    api_key = os.getenv('WEATHER_API_KEY')
    
    # 클라이언트 초기화
    client = WeatherClient(api_key)
    
    # 지역코드 목록 가져오기
    region_codes = await client.get_region_codes()
    print("=== 지역코드 목록 ===")
    print(json.dumps(region_codes, indent=2, ensure_ascii=False))
    
    # 서울 지역 중기기온 예보 조회
    seoul_code = '11B00000'  # 서울, 인천, 경기도
    temperature = await client.get_temperature_forecast(seoul_code)
    print("\n=== 서울 지역 중기기온 예보 ===")
    print(json.dumps(temperature, indent=2, ensure_ascii=False))
    
    # 서울 지역 중기육상 예보 조회
    land_forecast = await client.get_land_forecast(seoul_code)
    print("\n=== 서울 지역 중기육상 예보 ===")
    print(json.dumps(land_forecast, indent=2, ensure_ascii=False))
    
    # 서해북부 중기해상 예보 조회
    sea_code = '12A00000'  # 서해 북부
    sea_forecast = await client.get_sea_forecast(sea_code)
    print("\n=== 서해북부 중기해상 예보 ===")
    print(json.dumps(sea_forecast, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main()) 