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
```

4. .env 파일 생성

```bash
echo "WEATHER_API_KEY=발급받은_서비스키_입력" > .env
echo "WEATHER_API_ENDPOINT=https://apis.data.go.kr/1360000/MidFcstInfoService" >> .env
```

### 패키지로 설치하기

이 프로젝트를 Python 패키지로 설치하여 어디서든 사용할 수 있습니다.

#### 개발 모드로 설치 (소스 코드 변경 시 바로 반영)

```bash
# 저장소 디렉토리 내에서
source .venv/bin/activate  # 가상환경 활성화
pip install -e .
```

설치 후에는 `korea-weather-mcp` 명령어를 직접 사용하거나 Python 코드에서 모듈을 임포트할 수 있습니다.

#### 배포용 패키지 빌드

패키지를 빌드하여 배포하려면:

```bash
# 필요한 도구 설치
pip install build

# 패키지 빌드
python -m build
```

빌드가 완료되면 `dist/` 디렉토리에 다음 파일들이 생성됩니다:
- `korea_weather_mcp-0.1.0-py3-none-any.whl` (휠 패키지)
- `korea-weather-mcp-0.1.0.tar.gz` (소스 배포 파일)

#### 빌드된 패키지 설치

빌드된 패키지를 직접 설치하려면:

```bash
pip install dist/korea_weather_mcp-0.1.0-py3-none-any.whl
```

이렇게 설치하면 `korea-weather-mcp` 명령어를 어디서든 사용할 수 있습니다.

## MCP 서버 실행 방법

이 패키지는 여러 방법으로 실행할 수 있습니다:

### 방법 1: 패키지로 직접 실행

```bash
# 패키지 명령어 사용
korea-weather-mcp
```

### 방법 2: 모듈로 실행

```bash
python -m korea_weather
```

### 방법 3: 예제 스크립트 사용

examples 디렉토리의 예제 스크립트를 실행할 수 있습니다:

```bash
# MCP 서버 실행
python examples/mcp_server.py

# 기본 클라이언트 예제 실행
python examples/basic_client.py
```

## Claude Desktop에서 사용하기

Claude Desktop에서 이 MCP 서버를 사용하기 위해서는 `claude_desktop_config.json` 파일을 설정해야 합니다.

1. 홈 디렉토리에 `claude_desktop_config.json` 파일을 생성합니다:

```json
{
  "mcpServers": {
    "korea_weather": {
      "command": "python",
      "args": ["-m", "korea_weather"],
      "cwd": "/절대경로/KoreaWeatherMCP",
      "env": {
        "WEATHER_API_KEY": "발급받은_서비스키_입력"
      }
    }
  }
}
```

또는 패키지로 설치한 경우 다음과 같이 설정할 수 있습니다:

```json
{
  "mcpServers": {
    "korea_weather": {
      "command": "korea-weather-mcp",
      "env": {
        "WEATHER_API_KEY": "발급받은_서비스키_입력"
      }
    }
  }
}
```

2. `cwd` 경로를 실제 프로젝트 경로로 변경합니다 (패키지 설치 시에는 필요 없음).
3. `WEATHER_API_KEY` 값을 발급받은 서비스키로 변경합니다.
4. Claude Desktop을 다시 시작합니다.
5. Claude Desktop의 MCP 아이콘을 클릭하여 "korea_weather" 서버가 등록되었는지 확인합니다.

### 설정 파일의 위치

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

### 오류 해결

서버가 연결되지 않는 경우 다음 로그 파일을 확인하세요:

- macOS: `~/Library/Logs/Claude/mcp*.log`
- Windows: `%APPDATA%\Claude\logs\mcp*.log`

## MCP 서버 기능

MCP 서버는 다음 기능을 제공합니다:

1. **get_region_codes** - 기상청 중기예보 지역코드 목록 조회
2. **get_mid_temperature** - 특정 지역의 중기기온 조회 (getMidTa API)
3. **get_mid_land_forecast** - 특정 지역의 중기육상예보 조회 (getMidLandFcst API)
4. **get_mid_sea_forecast** - 특정 지역의 중기해상예보 조회 (getMidSeaFcst API)

## 사용 예시

Claude와의 대화에서 다음과 같이 사용할 수 있습니다:

```
사용자: 서울 지역의 중기예보를 알려주세요.

Claude: 서울 지역의 중기예보를 조회해 드리겠습니다.
(MCP 서버를 통해 정보를 조회한 후)
서울 지역의 중기예보는 다음과 같습니다:
...
```

## SSL 호환성 문제 해결

기상청 API 호출 시 SSL 오류가 발생하는 경우, 이 패키지는 자동으로 다음과 같은 설정을 적용합니다:

```python
ssl_context = ssl.create_default_context()
ssl_context.set_ciphers("DEFAULT:!TLSv1.3")  # TLSv1.3 비활성화
ssl_context.options |= ssl.OP_NO_SSLv3  # SSLv3 비활성화
```

## 패키지 구조

```
korea_weather/
├── __init__.py       # 패키지 초기화
├── __main__.py       # 메인 실행 파일
├── api.py            # 기상청 API 클라이언트
├── client.py         # 편리한 클라이언트 인터페이스
├── constants.py      # 상수 정의 (지역코드 등)
└── server.py         # MCP 서버 구현

examples/
├── basic_client.py   # 클라이언트 사용 예제
└── mcp_server.py     # MCP 서버 실행 예제
```

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.
