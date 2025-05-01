import requests
from urllib.parse import urlencode
import xml.etree.ElementTree as ET
import json
from app.core.config import WEATHER_API_KEY, WEATHER_API_ENDPOINT


class WeatherService:
    """기상청 중기예보 API 서비스 클래스"""

    def __init__(self):
        self.api_key = WEATHER_API_KEY
        self.base_url = WEATHER_API_ENDPOINT

    def _make_request(self, service_url, params):
        """API 요청을 보내고 응답을 반환"""
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
        url = f"{self.base_url}/{service_url}?{urlencode(default_params)}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # 에러 발생 시 예외 발생
            
            # JSON 응답일 경우
            if default_params.get('dataType') == 'JSON':
                return response.json()
            
            # XML 응답일 경우 JSON으로 변환
            root = ET.fromstring(response.content)
            result = {}
            
            # XML을 JSON으로 변환하는 간단한 로직
            for child in root:
                result[child.tag] = self._xml_to_dict(child)
                
            return result
        
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def _xml_to_dict(self, element):
        """XML 요소를 사전 형태로 변환"""
        result = {}
        
        for child in element:
            if len(child) > 0:
                result[child.tag] = self._xml_to_dict(child)
            else:
                result[child.tag] = child.text
                
        return result
    
    def get_mid_forecast_temperature(self, region_id, tmFc):
        """중기기온조회 (getMidTa)"""
        return self._make_request('getMidTa', {
            'regId': region_id,
            'tmFc': tmFc
        })
    
    def get_mid_forecast_land(self, region_id, tmFc):
        """중기육상예보조회 (getMidLandFcst)"""
        return self._make_request('getMidLandFcst', {
            'regId': region_id, 
            'tmFc': tmFc
        })
    
    def get_mid_forecast_sea(self, region_id, tmFc):
        """중기해상예보조회 (getMidSeaFcst)"""
        return self._make_request('getMidSeaFcst', {
            'regId': region_id,
            'tmFc': tmFc
        })
    
    def get_forecast_region_list(self):
        """중기예보 지역 코드 목록"""
        # 중기예보 지역 코드는 고정적이므로 하드코딩
        region_codes = {
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
        
        return region_codes 