from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class MidTaItem(BaseModel):
    """중기기온정보 항목"""
    regId: str = Field(..., description="예보구역코드")
    taMin3: int = Field(..., description="3일 후 최저기온")
    taMax3: int = Field(..., description="3일 후 최고기온")
    taMin4: int = Field(..., description="4일 후 최저기온")
    taMax4: int = Field(..., description="4일 후 최고기온")
    taMin5: int = Field(..., description="5일 후 최저기온")
    taMax5: int = Field(..., description="5일 후 최고기온")
    taMin6: int = Field(..., description="6일 후 최저기온")
    taMax6: int = Field(..., description="6일 후 최고기온")
    taMin7: int = Field(..., description="7일 후 최저기온")
    taMax7: int = Field(..., description="7일 후 최고기온")
    taMin8: int = Field(..., description="8일 후 최저기온")
    taMax8: int = Field(..., description="8일 후 최고기온")
    taMin9: int = Field(..., description="9일 후 최저기온")
    taMax9: int = Field(..., description="9일 후 최고기온")
    taMin10: int = Field(..., description="10일 후 최저기온")
    taMax10: int = Field(..., description="10일 후 최고기온")


class MidLandItem(BaseModel):
    """중기육상예보 항목"""
    regId: str = Field(..., description="예보구역코드")
    wf3Am: str = Field(..., description="3일 후 오전 날씨예보")
    wf3Pm: str = Field(..., description="3일 후 오후 날씨예보")
    wf4Am: str = Field(..., description="4일 후 오전 날씨예보")
    wf4Pm: str = Field(..., description="4일 후 오후 날씨예보")
    wf5Am: str = Field(..., description="5일 후 오전 날씨예보")
    wf5Pm: str = Field(..., description="5일 후 오후 날씨예보")
    wf6Am: str = Field(..., description="6일 후 오전 날씨예보")
    wf6Pm: str = Field(..., description="6일 후 오후 날씨예보")
    wf7Am: str = Field(..., description="7일 후 오전 날씨예보")
    wf7Pm: str = Field(..., description="7일 후 오후 날씨예보")
    wf8: str = Field(..., description="8일 후 날씨예보")
    wf9: str = Field(..., description="9일 후 날씨예보")
    wf10: str = Field(..., description="10일 후 날씨예보")


class MidSeaItem(BaseModel):
    """중기해상예보 항목"""
    regId: str = Field(..., description="예보구역코드")
    wf3Am: str = Field(..., description="3일 후 오전 날씨예보")
    wf3Pm: str = Field(..., description="3일 후 오후 날씨예보")
    wf4Am: str = Field(..., description="4일 후 오전 날씨예보")
    wf4Pm: str = Field(..., description="4일 후 오후 날씨예보")
    wf5Am: str = Field(..., description="5일 후 오전 날씨예보")
    wf5Pm: str = Field(..., description="5일 후 오후 날씨예보")
    wf6Am: str = Field(..., description="6일 후 오전 날씨예보")
    wf6Pm: str = Field(..., description="6일 후 오후 날씨예보")
    wf7Am: str = Field(..., description="7일 후 오전 날씨예보")
    wf7Pm: str = Field(..., description="7일 후 오후 날씨예보")
    wf8: str = Field(..., description="8일 후 날씨예보")
    wf9: str = Field(..., description="9일 후 날씨예보")
    wf10: str = Field(..., description="10일 후 날씨예보")


class WeatherResponse(BaseModel):
    """날씨 응답 모델"""
    resultCode: str = Field(..., description="결과코드")
    resultMsg: str = Field(..., description="결과메시지")
    items: List[dict] = Field(..., description="결과 항목들")
    numOfRows: int = Field(..., description="한 페이지 결과 수")
    pageNo: int = Field(..., description="페이지 번호")
    totalCount: int = Field(..., description="전체 결과 수") 