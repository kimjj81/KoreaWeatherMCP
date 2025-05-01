"""
기상청 API 클라이언트 모듈
"""
from typing import Any, Dict, Optional, cast
import httpx
import ssl
import json
import os
from datetime import datetime
from .constants import REGION_CODES

class WeatherAPI:
    """기상청 중기예보 API 클라이언트"""
    
    def __init__(self, api_key: Optional[str] = None, api_endpoint: Optional[str] = None):
        """
        기상청 API 클라이언트 초기화
        
        Args:
            api_key: 기상청 API 키 (없으면 환경변수에서 가져옴)
            api_endpoint: 기상청 API 엔드포인트 (없으면 기본값 사용)
        """
        self.api_key = api_key or os.getenv('WEATHER_API_KEY', '')
        self.api_endpoint = api_endpoint or os.getenv(
            'WEATHER_API_ENDPOINT', 
            'https://apis.data.go.kr/1360000/MidFcstInfoService'
        )
        
        # SSL 컨텍스트 설정
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.set_ciphers("DEFAULT:!TLSv1.3")  # TLSv1.3 비활성화
        self.ssl_context.options |= ssl.OP_NO_SSLv3  # SSLv3 비활성화
    
    async def request(self, service_url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        API 요청 보내기
        
        Args:
            service_url: 서비스 URL (예: getMidTa)
            params: 요청 파라미터
            
        Returns:
            API 응답 (딕셔너리)
        """
        # 기본 파라미터 설정
        default_params = {
            'serviceKey': self.api_key,
            'dataType': 'JSON',
            'numOfRows': 10,
            'pageNo': 1
        }
        
        # 사용자 파라미터 병합
        default_params.update(params)
        
        # URL 생성
        url = f"{self.api_endpoint}/{service_url}"
        
        try:
            async with httpx.AsyncClient(verify=self.ssl_context) as client:
                response = await client.get(url, params=default_params, timeout=30.0)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_current_forecast_time(self) -> str:
        """
        현재 시간에 적합한 발표시각 생성
        
        Returns:
            발표시각 (YYYYMMDDHHMM 형식)
        """
        now = datetime.now()
        
        # 발표시각은 보통 0600과 1800이므로 해당 시간 근처인지 확인
        if 6 <= now.hour < 18:
            # 0600발표
            return now.strftime('%Y%m%d0600')
        else:
            # 1800발표
            return now.strftime('%Y%m%d1800')
    
    async def get_mid_temperature(self, region_id: str, tmFc: Optional[str] = None) -> Dict[str, Any]:
        """
        중기기온 조회 (getMidTa)
        
        Args:
            region_id: 지역코드 (예: 11B00000 - 서울, 인천, 경기도)
            tmFc: 발표시각 (YYYYMMDDHHMM 형식, 미입력시 현재 시각 기준)
            
        Returns:
            중기기온 정보
        """
        if not tmFc:
            tmFc = self.get_current_forecast_time()
            
        return await self.request('getMidTa', {
            'regId': region_id,
            'tmFc': tmFc
        })
    
    async def get_mid_land_forecast(self, region_id: str, tmFc: Optional[str] = None) -> Dict[str, Any]:
        """
        중기육상예보 조회 (getMidLandFcst)
        
        Args:
            region_id: 지역코드 (예: 11B00000 - 서울, 인천, 경기도)
            tmFc: 발표시각 (YYYYMMDDHHMM 형식, 미입력시 현재 시각 기준)
            
        Returns:
            중기육상예보 정보
        """
        if not tmFc:
            tmFc = self.get_current_forecast_time()
            
        return await self.request('getMidLandFcst', {
            'regId': region_id,
            'tmFc': tmFc
        })
    
    async def get_mid_sea_forecast(self, region_id: str, tmFc: Optional[str] = None) -> Dict[str, Any]:
        """
        중기해상예보 조회 (getMidSeaFcst)
        
        Args:
            region_id: 지역코드 (예: 12A00000 - 서해 북부)
            tmFc: 발표시각 (YYYYMMDDHHMM 형식, 미입력시 현재 시각 기준)
            
        Returns:
            중기해상예보 정보
        """
        if not tmFc:
            tmFc = self.get_current_forecast_time()
            
        return await self.request('getMidSeaFcst', {
            'regId': region_id,
            'tmFc': tmFc
        })
    
    def get_region_codes(self) -> Dict[str, Dict[str, str]]:
        """
        지역코드 목록 조회
        
        Returns:
            지역코드 딕셔너리
        """
        return REGION_CODES 