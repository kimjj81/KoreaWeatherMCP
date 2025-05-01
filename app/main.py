from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.routes import api_router
from app.core.config import API_V1_STR, PROJECT_NAME

# FastAPI 앱 생성
app = FastAPI(
    title=PROJECT_NAME,
    description="기상청 중기예보 조회 MCP 서버 API",
    version="0.1.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영시에는 안전한 도메인 목록으로 변경 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(api_router, prefix=API_V1_STR)


@app.get("/", tags=["root"])
async def root():
    """루트 엔드포인트"""
    return {
        "message": "기상청 중기예보 MCP 서버에 오신 것을 환영합니다.",
        "documentation": "/docs",
    }


# 직접 실행 시 Uvicorn으로 서버 실행
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 