"""
MCP 서버 구현 모듈
"""
import os
import sys
import json
from typing import Dict, Any, Optional, List, cast, Literal
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from .api import WeatherAPI
from .constants import REGION_CODES

# .env 파일 로드
load_dotenv()

class WeatherMCP:
    """기상청 중기예보 MCP 서버"""
    
    def __init__(self, server_name: str = "KoreaWeatherForecast"):
        """
        MCP 서버 초기화
        
        Args:
            server_name: MCP 서버 이름
        """
        self.mcp = FastMCP(server_name)
        self.api = WeatherAPI()
        self._register_tools()
        
    def _register_tools(self):
        """MCP 도구 등록"""
        # 지역코드 조회
        @self.mcp.tool()
        async def get_region_codes() -> str:
            """기상청 중기예보 지역코드 목록 조회"""
            result = "## 기상청 중기예보 지역코드 목록\n\n"
            
            # 중기기온 지역코드
            result += "### 중기기온 지역코드\n"
            for code, name in REGION_CODES['temperature'].items():
                result += f"- {code}: {name}\n"
            
            # 중기육상예보 지역코드
            result += "\n### 중기육상예보 지역코드\n"
            for code, name in REGION_CODES['land'].items():
                result += f"- {code}: {name}\n"
            
            # 중기해상예보 지역코드
            result += "\n### 중기해상예보 지역코드\n"
            for code, name in REGION_CODES['sea'].items():
                result += f"- {code}: {name}\n"
            
            return result
        
        # 중기기온 조회
        @self.mcp.tool()
        async def get_mid_temperature(region_id: str, tmFc: Optional[str] = None) -> str:
            """중기기온 조회 (getMidTa)
            
            Args:
                region_id: 지역코드 (예: 11B00000 - 서울, 인천, 경기도)
                tmFc: 발표시각 (YYYYMMDDHHMM 형식, 미입력시 현재 시각 기준)
            """
            result = await self.api.get_mid_temperature(region_id, tmFc)
            
            if 'error' in result:
                return f"오류가 발생했습니다: {result['error']}"
            
            try:
                # 명시적 타입 캐스팅으로 처리
                response = cast(Dict[str, Any], result.get('response', {}))
                
                # 안전하게 중첩된 값 접근
                header = cast(Dict[str, Any], response.get('header', {}))
                resultCode = header.get('resultCode')
                
                if resultCode != '00':
                    resultMsg = header.get('resultMsg', '알 수 없는 오류')
                    return f"API 오류: {resultMsg}"
                
                body = cast(Dict[str, Any], response.get('body', {}))
                items = body.get('items', {})
                
                if not items or not items.get('item'):
                    return "해당 지역의 중기기온 정보가 없습니다."
                
                # 중기기온 정보 추출
                ta_item = cast(Dict[str, Any], items.get('item', [{}])[0])
                
                # 결과 포맷팅
                region_name = REGION_CODES['temperature'].get(region_id, region_id)
                forecast_time = tmFc or self.api.get_current_forecast_time()
                
                result_str = f"## 중기기온예보: {region_name} (발표: {forecast_time})\n\n"
                
                # 3일 후부터 10일 후까지 기온 정보 추가
                for day in range(3, 11):
                    min_temp = ta_item.get(f'taMin{day}')
                    max_temp = ta_item.get(f'taMax{day}')
                    
                    result_str += f"### {day}일 후\n"
                    result_str += f"- 최저기온: {min_temp}°C\n"
                    result_str += f"- 최고기온: {max_temp}°C\n\n"
                
                return result_str
                
            except Exception as e:
                return f"데이터 처리 중 오류가 발생했습니다: {str(e)}"
        
        # 중기육상예보 조회
        @self.mcp.tool()
        async def get_mid_land_forecast(region_id: str, tmFc: Optional[str] = None) -> str:
            """중기육상예보 조회 (getMidLandFcst)
            
            Args:
                region_id: 지역코드 (예: 11B00000 - 서울, 인천, 경기도)
                tmFc: 발표시각 (YYYYMMDDHHMM 형식, 미입력시 현재 시각 기준)
            """
            result = await self.api.get_mid_land_forecast(region_id, tmFc)
            
            if 'error' in result:
                return f"오류가 발생했습니다: {result['error']}"
            
            try:
                # 명시적 타입 캐스팅으로 처리
                response = cast(Dict[str, Any], result.get('response', {}))
                
                # 안전하게 중첩된 값 접근
                header = cast(Dict[str, Any], response.get('header', {}))
                resultCode = header.get('resultCode')
                
                if resultCode != '00':
                    resultMsg = header.get('resultMsg', '알 수 없는 오류')
                    return f"API 오류: {resultMsg}"
                
                body = cast(Dict[str, Any], response.get('body', {}))
                items = body.get('items', {})
                
                if not items or not items.get('item'):
                    return "해당 지역의 중기육상예보 정보가 없습니다."
                
                # 중기육상예보 정보 추출
                land_item = cast(Dict[str, Any], items.get('item', [{}])[0])
                
                # 결과 포맷팅
                region_name = REGION_CODES['land'].get(region_id, region_id)
                forecast_time = tmFc or self.api.get_current_forecast_time()
                
                result_str = f"## 중기육상예보: {region_name} (발표: {forecast_time})\n\n"
                
                # 3일 후부터 7일 후까지 오전/오후 예보
                for day in range(3, 8):
                    am_weather = land_item.get(f'wf{day}Am')
                    pm_weather = land_item.get(f'wf{day}Pm')
                    
                    result_str += f"### {day}일 후\n"
                    result_str += f"- 오전: {am_weather}\n"
                    result_str += f"- 오후: {pm_weather}\n\n"
                
                # 8일 후부터 10일 후까지 종일 예보
                for day in range(8, 11):
                    weather = land_item.get(f'wf{day}')
                    
                    result_str += f"### {day}일 후\n"
                    result_str += f"- 날씨: {weather}\n\n"
                
                return result_str
                
            except Exception as e:
                return f"데이터 처리 중 오류가 발생했습니다: {str(e)}"
        
        # 중기해상예보 조회
        @self.mcp.tool()
        async def get_mid_sea_forecast(region_id: str, tmFc: Optional[str] = None) -> str:
            """중기해상예보 조회 (getMidSeaFcst)
            
            Args:
                region_id: 지역코드 (예: 12A00000 - 서해 북부)
                tmFc: 발표시각 (YYYYMMDDHHMM 형식, 미입력시 현재 시각 기준)
            """
            result = await self.api.get_mid_sea_forecast(region_id, tmFc)
            
            if 'error' in result:
                return f"오류가 발생했습니다: {result['error']}"
            
            try:
                # 명시적 타입 캐스팅으로 처리
                response = cast(Dict[str, Any], result.get('response', {}))
                
                # 안전하게 중첩된 값 접근
                header = cast(Dict[str, Any], response.get('header', {}))
                resultCode = header.get('resultCode')
                
                if resultCode != '00':
                    resultMsg = header.get('resultMsg', '알 수 없는 오류')
                    return f"API 오류: {resultMsg}"
                
                body = cast(Dict[str, Any], response.get('body', {}))
                items = body.get('items', {})
                
                if not items or not items.get('item'):
                    return "해당 지역의 중기해상예보 정보가 없습니다."
                
                # 중기해상예보 정보 추출
                sea_item = cast(Dict[str, Any], items.get('item', [{}])[0])
                
                # 결과 포맷팅
                region_name = REGION_CODES['sea'].get(region_id, region_id)
                forecast_time = tmFc or self.api.get_current_forecast_time()
                
                result_str = f"## 중기해상예보: {region_name} (발표: {forecast_time})\n\n"
                
                # 3일 후부터 7일 후까지 오전/오후 예보
                for day in range(3, 8):
                    am_weather = sea_item.get(f'wf{day}Am')
                    pm_weather = sea_item.get(f'wf{day}Pm')
                    
                    result_str += f"### {day}일 후\n"
                    result_str += f"- 오전: {am_weather}\n"
                    result_str += f"- 오후: {pm_weather}\n\n"
                
                # 8일 후부터 10일 후까지 종일 예보
                for day in range(8, 11):
                    weather = sea_item.get(f'wf{day}')
                    
                    result_str += f"### {day}일 후\n"
                    result_str += f"- 날씨: {weather}\n\n"
                
                return result_str
                
            except Exception as e:
                return f"데이터 처리 중 오류가 발생했습니다: {str(e)}"
    
    def log(self, message: str):
        """로그 출력 (stderr로 출력)"""
        print(message, file=sys.stderr, flush=True)
    
    def run(self, transport: Literal['stdio', 'sse'] = 'stdio'):
        """MCP 서버 실행"""
        self.log("기상청 중기예보 MCP 서버를 시작합니다...")
        self.mcp.run(transport=transport) 