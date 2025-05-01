from typing import Any, Optional, Dict, Union, List, cast
import httpx
from datetime import datetime
import os
import sys
import json
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# .env 파일 로드
load_dotenv()

# MCP 서버 초기화
mcp = FastMCP("KoreaWeatherForecast")

# API 설정
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
WEATHER_API_ENDPOINT = os.getenv('WEATHER_API_ENDPOINT', 'https://apis.data.go.kr/1360000/MidFcstInfoService')

# 지역 코드 정보
REGION_CODES = {
    # 중기기온 지역코드
    'temperature': {
        '11B00000': '서울, 인천, 경기도',
        '11D10000': '강원도 영서',
        '11D20000': '강원도 영동',
        '11C20000': '대전, 세종, 충청남도',
        '11C10000': '충청북도',
        '11F20000': '광주, 전라남도',
        '11F10000': '전라북도',
        '11H10000': '대구, 경상북도',
        '11H20000': '부산, 울산, 경상남도',
        '11G00000': '제주도',
    },
    # 중기육상예보 지역코드
    'land': {
        '11B00000': '서울, 인천, 경기도',
        '11D10000': '강원도 영서',
        '11D20000': '강원도 영동',
        '11C20000': '대전, 세종, 충청남도', 
        '11C10000': '충청북도',
        '11F20000': '광주, 전라남도',
        '11F10000': '전라북도',
        '11H10000': '대구, 경상북도',
        '11H20000': '부산, 울산, 경상남도',
        '11G00000': '제주도',
    },
    # 중기해상예보 지역코드
    'sea': {
        '12A00000': '서해 북부',
        '12B00000': '서해 중부',
        '12C00000': '서해 남부',
        '12D00000': '남해 서부',
        '12E00000': '남해 동부',
        '12F00000': '동해 남부',
        '12G00000': '동해 중부',
        '12H00000': '동해 북부',
        '12I00000': '제주도 해상',
        '12J00000': '울릉도, 독도 해상',
    }
}

# 로그 출력 함수 정의 - stderr로 출력
def log(message):
    print(message, file=sys.stderr, flush=True)

def get_tmFc_now():
    """현재 시간에 적합한 발표시각 생성"""
    now = datetime.now()
    
    # 발표시각은 보통 0600과 1800이므로 해당 시간 근처인지 확인
    if 6 <= now.hour < 18:
        # 0600발표
        tmFc = now.strftime('%Y%m%d0600')
    else:
        # 1800발표
        tmFc = now.strftime('%Y%m%d1800')
    
    return tmFc


async def make_api_request(service_url, params):
    """기상청 API 요청을 보내고 응답을 반환"""
    # 기본 파라미터 설정
    default_params = {
        'serviceKey': WEATHER_API_KEY,
        'dataType': 'JSON',
        'numOfRows': 10,
        'pageNo': 1
    }
    
    # 사용자 파라미터 병합
    default_params.update(params)
    
    # URL 생성
    url = f"{WEATHER_API_ENDPOINT}/{service_url}"
    
    # 로그 출력
    log(f"API 요청: {url} - 파라미터: {json.dumps(params)}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=default_params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            
            # 디버깅을 위한 로그
            log(f"API 응답: {json.dumps(data, ensure_ascii=False)[:300]}...")
            
            return data
        except Exception as e:
            # 오류 로그 
            log(f"API 요청 실패: {str(e)}")
            return {"error": str(e)}


@mcp.tool()
async def get_region_codes() -> str:
    """기상청 중기예보 지역코드 목록 조회"""
    
    log("지역코드 조회 요청됨")
    
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


@mcp.tool()
async def get_mid_temperature(region_id: str, tmFc: Optional[str] = None) -> str:
    """중기기온 조회 (getMidTa)
    
    Args:
        region_id: 지역코드 (예: 11B00000 - 서울, 인천, 경기도)
        tmFc: 발표시각 (YYYYMMDDHHMM 형식, 미입력시 현재 시각 기준)
    """
    # 발표시각이 없으면 현재 시간 기준으로 설정
    if not tmFc:
        tmFc = get_tmFc_now()
    
    log(f"중기기온 조회 요청: 지역={region_id}, 발표시각={tmFc}")
    
    # API 호출
    result = await make_api_request('getMidTa', {
        'regId': region_id,
        'tmFc': tmFc
    })
    
    if 'error' in result:
        log(f"API 오류: {result['error']}")
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
        forecast_time = tmFc
        
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
        log(f"데이터 처리 오류: {str(e)}")
        return f"데이터 처리 중 오류가 발생했습니다: {str(e)}"


@mcp.tool()
async def get_mid_land_forecast(region_id: str, tmFc: Optional[str] = None) -> str:
    """중기육상예보 조회 (getMidLandFcst)
    
    Args:
        region_id: 지역코드 (예: 11B00000 - 서울, 인천, 경기도)
        tmFc: 발표시각 (YYYYMMDDHHMM 형식, 미입력시 현재 시각 기준)
    """
    # 발표시각이 없으면 현재 시간 기준으로 설정
    if not tmFc:
        tmFc = get_tmFc_now()
    
    log(f"중기육상예보 조회 요청: 지역={region_id}, 발표시각={tmFc}")
    
    # API 호출
    result = await make_api_request('getMidLandFcst', {
        'regId': region_id,
        'tmFc': tmFc
    })
    
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
        forecast_time = tmFc
        
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
        log(f"데이터 처리 오류: {str(e)}")
        return f"데이터 처리 중 오류가 발생했습니다: {str(e)}"


@mcp.tool()
async def get_mid_sea_forecast(region_id: str, tmFc: Optional[str] = None) -> str:
    """중기해상예보 조회 (getMidSeaFcst)
    
    Args:
        region_id: 지역코드 (예: 12A00000 - 서해 북부)
        tmFc: 발표시각 (YYYYMMDDHHMM 형식, 미입력시 현재 시각 기준)
    """
    # 발표시각이 없으면 현재 시간 기준으로 설정
    if not tmFc:
        tmFc = get_tmFc_now()
    
    log(f"중기해상예보 조회 요청: 지역={region_id}, 발표시각={tmFc}")
    
    # API 호출
    result = await make_api_request('getMidSeaFcst', {
        'regId': region_id,
        'tmFc': tmFc
    })
    
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
        forecast_time = tmFc
        
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
        log(f"데이터 처리 오류: {str(e)}")
        return f"데이터 처리 중 오류가 발생했습니다: {str(e)}"


if __name__ == "__main__":
    # 서버 실행
    log("기상청 중기예보 MCP 서버를 시작합니다...")
    mcp.run(transport='stdio') 