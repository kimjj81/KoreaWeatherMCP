from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, Dict, Any
import datetime

from app.services.weather_service import WeatherService
from app.schemas.weather import WeatherResponse

router = APIRouter()
weather_service = WeatherService()


def get_tmFc_now():
    """현재 시간에 적합한 발표시각 생성"""
    now = datetime.datetime.now()
    
    # 발표시각은 보통 0600과 1800이므로 해당 시간 근처인지 확인
    if 6 <= now.hour < 18:
        # 0600발표
        tmFc = now.strftime('%Y%m%d0600')
    else:
        # 1800발표
        tmFc = now.strftime('%Y%m%d1800')
    
    return tmFc


@router.get("/regions", summary="중기예보 지역코드 목록 조회")
async def get_regions():
    """
    중기예보 지역코드 목록을 조회합니다.
    """
    regions = weather_service.get_forecast_region_list()
    return {"regions": regions}


@router.get("/temperature", summary="중기기온조회", response_model=Dict[str, Any])
async def get_mid_temperature(
    regId: str = Query(..., description="예보구역코드"),
    tmFc: Optional[str] = Query(None, description="발표시각(YYYYMMDDHH24MI)"),
):
    """
    중기기온조회 API
    
    - **regId**: 예보구역코드
    - **tmFc**: 발표시각(YYYYMMDDHH24MI), 미입력 시 현재 시각 기준 최신 발표시각 사용
    """
    if not tmFc:
        tmFc = get_tmFc_now()
    
    result = weather_service.get_mid_forecast_temperature(regId, tmFc)
    
    if 'error' in result:
        raise HTTPException(status_code=500, detail=result['error'])
    
    return result


@router.get("/land", summary="중기육상예보조회", response_model=Dict[str, Any])
async def get_mid_land_forecast(
    regId: str = Query(..., description="예보구역코드"),
    tmFc: Optional[str] = Query(None, description="발표시각(YYYYMMDDHH24MI)"),
):
    """
    중기육상예보조회 API
    
    - **regId**: 예보구역코드
    - **tmFc**: 발표시각(YYYYMMDDHH24MI), 미입력 시 현재 시각 기준 최신 발표시각 사용
    """
    if not tmFc:
        tmFc = get_tmFc_now()
    
    result = weather_service.get_mid_forecast_land(regId, tmFc)
    
    if 'error' in result:
        raise HTTPException(status_code=500, detail=result['error'])
    
    return result


@router.get("/sea", summary="중기해상예보조회", response_model=Dict[str, Any])
async def get_mid_sea_forecast(
    regId: str = Query(..., description="예보구역코드"),
    tmFc: Optional[str] = Query(None, description="발표시각(YYYYMMDDHH24MI)"),
):
    """
    중기해상예보조회 API
    
    - **regId**: 예보구역코드
    - **tmFc**: 발표시각(YYYYMMDDHH24MI), 미입력 시 현재 시각 기준 최신 발표시각 사용
    """
    if not tmFc:
        tmFc = get_tmFc_now()
    
    result = weather_service.get_mid_forecast_sea(regId, tmFc)
    
    if 'error' in result:
        raise HTTPException(status_code=500, detail=result['error'])
    
    return result 