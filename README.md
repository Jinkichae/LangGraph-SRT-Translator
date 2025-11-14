# LangGraph Subtitle Translator

한국어 자막을 여러 언어로 자동 번역하는 시스템으로, LangChain과 LangGraph를 활용하여 구축되었습니다. **Layered Architecture**를 적용하여 유지보수성과 확장성을 극대화했습니다.

## 🏗️ Architecture

이 프로젝트는 **Layered Architecture** 패턴을 따릅니다:

```
┌─────────────────────────────────────────┐
│   Presentation Layer (CLI/API)          │  ← 사용자 인터페이스
├─────────────────────────────────────────┤
│   Service Layer (Business Logic)        │  ← 비즈니스 로직 조율
├─────────────────────────────────────────┤
│   Domain Layer (Core Models)            │  ← 핵심 도메인 모델
├─────────────────────────────────────────┤
│   Infrastructure Layer (Data/External)  │  ← 데이터 액세스 & 외부 서비스
└─────────────────────────────────────────┘
         Common (Shared Utilities)
```

### Layer 설명

#### 1. **Presentation Layer** (`presentation/`)
사용자와의 상호작용을 담당합니다.
- `cli/main.py`: 메인 CLI 진입점
- `cli/example_usage.py`: 다양한 사용 예제
- `cli/retry_failed.py`: 실패한 번역 재시도 도구

#### 2. **Service Layer** (`service/`)
비즈니스 로직을 조율하고 처리 파이프라인을 구성합니다.
- `orchestrator.py`: 번역 워크플로우 조율
- `pipeline/builder.py`: 파이프라인 빌더 (Builder Pattern)
- `pipeline/handlers/`: 체인 핸들러들 (Chain of Responsibility Pattern)
  - `validation_handler.py`: 요청 검증
  - `execution_handler.py`: 번역 실행 (재시도 로직)
  - `persistence_handler.py`: 결과 저장
  - `logging_handler.py`: 로깅

#### 3. **Domain Layer** (`domain/`)
핵심 비즈니스 도메인 모델을 정의합니다. 다른 레이어에 의존하지 않습니다.
- `models/translation_request.py`: 번역 요청 도메인 객체

#### 4. **Infrastructure Layer** (`infrastructure/`)
외부 서비스 및 데이터 액세스를 담당합니다.
- `repositories/subtitle_repository.py`: 자막 파일 저장소
- `executors/langgraph_executor.py`: LangGraph 실행 엔진

#### 5. **Common** (`common/`)
모든 레이어에서 사용 가능한 공통 유틸리티입니다.
- `config/`: 설정 및 상수
- `utils/`: 유틸리티 함수

## 📁 프로젝트 구조

```
langgraph_translator/
├── presentation/              # Presentation Layer
│   └── cli/
│       ├── main.py           # CLI 진입점
│       ├── example_usage.py  # 사용 예제
│       └── retry_failed.py   # 재시도 도구
│
├── service/                   # Service Layer
│   ├── orchestrator.py       # 워크플로우 조율
│   └── pipeline/
│       ├── builder.py        # 파이프라인 빌더
│       └── handlers/         # 체인 핸들러들
│
├── domain/                    # Domain Layer
│   └── models/
│       └── translation_request.py
│
├── infrastructure/            # Infrastructure Layer
│   ├── repositories/
│   │   └── subtitle_repository.py
│   └── executors/
│       └── langgraph_executor.py
│
├── common/                    # Common Layer
│   ├── config/
│   │   ├── constants.py      # 애플리케이션 상수
│   │   └── settings.py       # 설정 관리
│   └── utils/
│       ├── path_manager.py   # 경로 관리
│       ├── file_utils.py     # 파일 유틸리티
│       └── logger_utils.py   # 로거 설정
│
├── tests/                     # 테스트
├── .env                       # 환경 변수
├── requirements.txt           # 의존성
└── README.md                  # 이 문서
```

## 🚀 Quick Start

### 1. 설치

```bash
# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 설정

`.env` 파일을 생성하고 다음 내용을 입력:

```env
GROQ_API_KEY=your_groq_api_key_here
LANG_CODES=en,de,ja,es,fr
SRT_DIR=C:\path\to\your\subtitles
MODEL_PRIORITY_INDEX=3
WORKER_COUNT=6
BATCH_SIZE=12
SAVE_INTERVAL=24
```

### 3. 실행

```bash
# langgraph_translator 디렉토리로 이동
cd langgraph_translator

# 메인 번역 실행
python -m presentation.cli.main

# 또는 배치 파일 사용 (Windows)
run.bat
```

## 🌍 번역 언어 변경 방법

### 방법 1: .env 파일 수정 (권장)

`.env` 파일에서 `LANG_CODES` 값을 수정:

```env
# 단일 언어
LANG_CODES=en

# 여러 언어 (쉼표로 구분)
LANG_CODES=en,de,ja,es,fr,zh

# 지원 언어 코드:
# en: 영어, de: 독일어, ja: 일본어, es: 스페인어
# fr: 프랑스어, zh: 중국어, it: 이탈리아어, pt: 포르투갈어
# ru: 러시아어, ar: 아랍어, hi: 힌디어, ko: 한국어
```

### 방법 2: 코드에서 직접 설정

```python
from common.config.settings import SettingsManager

settings = SettingsManager(
    groq_api_key="your_api_key",
    lang_codes_str="en,de,ja",  # 원하는 언어 코드 입력
    srt_dir=r"C:\path\to\subtitles"
)
```

### 방법 3: 실행 시 임시 변경

```bash
# Windows
set LANG_CODES=en,fr,es && python -m presentation.cli.main

# Linux/Mac
LANG_CODES=en,fr,es python -m presentation.cli.main
```

## 📚 사용 예제

### 기본 사용법

```python
from common.config.settings import SettingsManager
from service.orchestrator import TranslationOrchestrator

# 설정 생성
settings = SettingsManager(
    groq_api_key="your_api_key",
    lang_codes_str="en,de,ja",  # 번역할 언어 지정
    srt_dir=r"C:\path\to\subtitles"
)

# 오케스트레이터 생성
orchestrator = TranslationOrchestrator(settings)

# 번역 실행
orchestrator.run_batch_translation()
```

### 특정 언어만 번역하기

```python
# 영어만 번역
settings = SettingsManager(
    groq_api_key="your_api_key",
    lang_codes_str="en",
    srt_dir=r"C:\path\to\subtitles"
)

# 여러 언어 번역
settings = SettingsManager(
    groq_api_key="your_api_key",
    lang_codes_str="en,ja,zh,fr,es",
    srt_dir=r"C:\path\to\subtitles"
)
```

### 커스텀 파이프라인

```python
from service.pipeline.builder import TranslationPipelineBuilder
from infrastructure.executors.langgraph_executor import LangGraphExecutor

# 커스텀 파이프라인 구축
pipeline = (
    TranslationPipelineBuilder()
    .add_validation()
    .add_execution(executor, max_attempts=5)
    .add_persistence(repository)
    .add_logging(logger)
    .build()
)
```

### 실패한 번역 재시도

```bash
python -m presentation.cli.retry_failed
```

## 🎯 주요 기능

### 1. Layered Architecture
- **명확한 책임 분리**: 각 레이어가 독립적인 역할 수행
- **의존성 방향**: 상위 레이어 → 하위 레이어 (단방향)
- **유지보수성**: 레이어별 독립적 수정 가능
- **테스트 용이성**: 각 레이어를 독립적으로 테스트

### 2. 디자인 패턴
- **Builder Pattern**: 파이프라인 구성의 유연성
- **Chain of Responsibility**: 단계별 처리 체인
- **Repository Pattern**: 데이터 액세스 추상화
- **SOLID 원칙**: 객체지향 설계 원칙 준수

### 3. 번역 기능
- **다중 언어 동시 번역**: 여러 언어로 한 번에 번역
- **문맥 인식**: 이전/이후 자막을 문맥으로 제공
- **자동 재시도**: 실패 시 지수 백오프로 재시도
- **동시 처리**: ThreadPoolExecutor로 병렬 처리
- **진행 상황 저장**: 중단 시 재개 가능

### 4. 모니터링 & 로깅
- **토큰 추적**: API 토큰 사용량 실시간 모니터링
- **상세한 로깅**: 각 단계별 상세 로그
- **통계 출력**: 성공률, 처리 시간 등

## 🔧 설정 옵션

| 설정 | 환경변수 | 기본값 | 설명 |
|------|---------|-------|------|
| API Key | `GROQ_API_KEY` | 필수 | GROQ API 키 |
| 언어 코드 | `LANG_CODES` | `en,de` | 쉼표로 구분된 언어 코드 |
| 자막 디렉토리 | `SRT_DIR` | 필수 | 자막 파일 경로 |
| 모델 인덱스 | `MODEL_PRIORITY_INDEX` | `0` | 사용할 모델 (0-7) |
| 워커 수 | `WORKER_COUNT` | `4` | 동시 처리 스레드 수 |
| 배치 크기 | `BATCH_SIZE` | `8` | 한 번에 처리할 자막 수 |
| 저장 간격 | `SAVE_INTERVAL` | `16` | 주기적 저장 간격 |

## 📊 지원 모델

0. `llama-3.1-70b-versatile`
1. `llama-3.1-8b-instant`
2. `llama-3.2-90b-text-preview`
3. `llama-3.3-70b-versatile` (추천)
4. `llama3-70b-8192`
5. `llama3-8b-8192`
6. `openai/gpt-oss-120b`
7. `nvidia/llama-3.1-nemotron-70b-instruct`

## 🏛️ Architecture 원칙

### Layered Architecture vs Pipeline

**Layered Architecture**는 시스템을 역할과 책임에 따라 계층으로 나누는 구조입니다:
- 각 계층은 독립적 기능 수행
- 상위 계층은 하위 계층에만 의존
- 유지보수와 확장이 용이

**Pipeline**은 데이터를 여러 단계로 연속 처리하는 방식입니다:
- 각 단계는 이전 단계의 출력을 입력으로 사용
- 데이터 흐름과 처리 효율성에 초점

이 프로젝트는 **Layered Architecture**를 전체 구조로 사용하고, Service Layer 내부에서 **Pipeline (Chain of Responsibility)** 패턴을 적용합니다.

### 의존성 방향

```
Presentation Layer
    ↓
Service Layer
    ↓
Domain Layer ← Infrastructure Layer
    ↑
Common Layer (모든 레이어에서 사용)
```

- **Domain Layer**는 가장 안정적이며 다른 레이어에 의존하지 않음
- **Infrastructure Layer**는 Domain의 인터페이스를 구현
- **Service Layer**는 Domain과 Infrastructure를 조율
- **Presentation Layer**는 Service를 통해 기능 제공

## 🧪 테스트

```bash
# 단위 테스트 실행
python -m pytest tests/

# 특정 테스트 실행
python tests/test_example.py
```

## 📝 개발 가이드

### 새로운 핸들러 추가

1. `service/pipeline/handlers/`에 새 핸들러 파일 생성
2. `TranslationHandler`를 상속
3. `handle()` 메서드 구현
4. `pipeline/builder.py`에 빌더 메서드 추가

```python
from service.pipeline.handlers.base_handler import TranslationHandler
from domain.models.translation_request import TranslationRequest

class CustomHandler(TranslationHandler):
    def handle(self, request: TranslationRequest) -> TranslationRequest:
        # 커스텀 로직
        return self._call_next(request)
```

### 새로운 레이어 추가

각 레이어는 명확한 책임을 가져야 합니다:
- **Presentation**: 사용자 인터페이스만
- **Service**: 비즈니스 로직 조율만
- **Domain**: 비즈니스 규칙만
- **Infrastructure**: 외부 연동만

## 🤝 기여

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

MIT License

## 👥 저자

LangGraph Translator Team

## 🙏 감사의 말

- [LangChain](https://www.langchain.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [GROQ](https://groq.com/)

---

**Note**: 이 프로젝트는 Layered Architecture를 학습하고 적용하기 위한 프로덕션 레디 예제입니다.
