"""
MCP 클라이언트 예제 모듈
"""
from typing import List, Dict, Any, Optional
from korea_weather.api import WeatherAPI

class WeatherClient:
    """기상청 중기예보 클라이언트"""
    
    def __init__(self, api_key: Optional[str] = None, api_endpoint: Optional[str] = None):
        """
        클라이언트 초기화
        
        Args:
            api_key: 기상청 API 키 (없으면 환경변수에서 가져옴)
            api_endpoint: 기상청 API 엔드포인트 (없으면 기본값 사용)
        """
        self.api = WeatherAPI(api_key, api_endpoint)
    
    async def get_region_codes(self) -> Dict[str, Dict[str, str]]:
        """
        지역코드 조회
        
        Returns:
            지역코드 정보
        """
        return self.api.get_region_codes()
    
    async def get_temperature_forecast(self, region_id: str, forecast_time: Optional[str] = None) -> Dict[str, Any]:
        """
        중기기온 예보 조회
        
        Args:
            region_id: 지역코드 (예: 11B00000 - 서울, 인천, 경기도)
            forecast_time: 발표시각 (YYYYMMDDHHMM 형식, 미입력시 현재 시각 기준)
            
        Returns:
            중기기온 예보 정보
        """
        return await self.api.get_mid_temperature(region_id, forecast_time)
    
    async def get_land_forecast(self, region_id: str, forecast_time: Optional[str] = None) -> Dict[str, Any]:
        """
        중기육상 예보 조회
        
        Args:
            region_id: 지역코드 (예: 11B00000 - 서울, 인천, 경기도) 
            forecast_time: 발표시각 (YYYYMMDDHHMM 형식, 미입력시 현재 시각 기준)
            
        Returns:
            중기육상 예보 정보
        """
        return await self.api.get_mid_land_forecast(region_id, forecast_time)
    
    async def get_sea_forecast(self, region_id: str, forecast_time: Optional[str] = None) -> Dict[str, Any]:
        """
        중기해상 예보 조회
        
        Args:
            region_id: 지역코드 (예: 12A00000 - 서해 북부)
            forecast_time: 발표시각 (YYYYMMDDHHMM 형식, 미입력시 현재 시각 기준)
            
        Returns:
            중기해상 예보 정보
        """
        return await self.api.get_mid_sea_forecast(region_id, forecast_time) 