# 기상청 중기예보 MCP 서버

기상청 중기예보 조회 OpenAPI를 활용한 MCP(Model Context Protocol) 서버입니다.

## 소개

이 프로젝트는 기상청에서 제공하는 중기예보 조회 서비스 OpenAPI를 Claude와 같은 AI 모델이 쉽게 활용할 수 있도록 MCP(Model Context Protocol) 서버로 구현한 것입니다.

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
pip install "mcp[cli]" httpx
```

4. .env 파일 생성

```bash
echo "WEATHER_API_KEY=발급받은_서비스키_입력" > .env
echo "WEATHER_API_ENDPOINT=https://apis.data.go.kr/1360000/MidFcstInfoService" >> .env
```

## MCP 서버 실행 방법

다음 명령을 사용하여 MCP 서버를 직접 실행할 수 있습니다:

```bash
python weather_mcp.py
```

## Claude Desktop에서 사용하기

Claude Desktop에서 이 MCP 서버를 사용하기 위해서는 `claude_desktop_config.json` 파일을 설정해야 합니다.

1. 프로젝트 루트에 `claude_desktop_config.json` 파일을 생성합니다:

```json
{
  "korea_weather": {
    "command": "python",
    "args": ["weather_mcp.py"],
    "cwd": "/경로/KoreaWeatherMCP"
  }
}
```

2. `cwd` 경로를 실제 프로젝트 경로로 변경합니다.

3. Claude Desktop을 다시 시작합니다.

4. Claude Desktop의 MCP 아이콘을 클릭하여 "korea_weather" 서버가 등록되었는지 확인합니다.

## MCP 서버 기능

MCP 서버는 다음 기능을 제공합니다:

1. **지역코드_조회** - 기상청 중기예보 지역코드 목록 조회
2. **중기기온_조회** - 특정 지역의 중기기온 조회 (getMidTa API)
3. **중기육상예보_조회** - 특정 지역의 중기육상예보 조회 (getMidLandFcst API)
4. **중기해상예보_조회** - 특정 지역의 중기해상예보 조회 (getMidSeaFcst API)

## 사용 예시

Claude와의 대화에서 다음과 같이 사용할 수 있습니다:

```
사용자: 서울 지역의 중기예보를 알려주세요.

Claude: 서울 지역의 중기예보를 조회해 드리겠습니다.
(MCP 서버를 통해 정보를 조회한 후)
서울 지역의 중기예보는 다음과 같습니다:
...
```

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.
