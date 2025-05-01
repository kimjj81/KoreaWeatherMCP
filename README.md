# 기상청 중기예보 MCP 서버

기상청 중기예보 조회 OpenAPI를 활용한 MCP(Microservice Control Plane) 서버입니다.

## 소개

이 프로젝트는 기상청에서 제공하는 중기예보 조회 서비스 OpenAPI를 쉽게 활용할 수 있도록 MCP 서버로 구현한 것입니다.

- OpenAPI 제공 사이트: https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15059468
- 원본 API 엔드포인트: https://apis.data.go.kr/1360000/MidFcstInfoService

## 설치 방법

### 요구사항

- Python 3.8 이상
- pip

### 설치 단계

1. 저장소 클론

```bash
git clone https://github.com/yourusername/KoreaWeatherMCP.git
cd KoreaWeatherMCP
```

2. 가상환경 생성 및 활성화

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 또는
# .venv\Scripts\activate  # Windows
```

3. 의존성 설치

```bash
pip install -e .
```

4. .env 파일 생성

```bash
echo "WEATHER_API_KEY=발급받은_서비스키_입력" > .env
echo "WEATHER_API_ENDPOINT=https://apis.data.go.kr/1360000/MidFcstInfoService" >> .env
```

## 실행 방법

```bash
python run.py
```

서버가 `http://localhost:8000`에서 실행됩니다.

## API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 주요 API 엔드포인트

- `GET /api/v1/weather/regions` - 중기예보 지역코드 목록 조회
- `GET /api/v1/weather/temperature` - 중기기온조회 (getMidTa)
- `GET /api/v1/weather/land` - 중기육상예보조회 (getMidLandFcst)
- `GET /api/v1/weather/sea` - 중기해상예보조회 (getMidSeaFcst)

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.
