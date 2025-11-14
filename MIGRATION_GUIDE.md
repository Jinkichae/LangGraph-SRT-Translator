# Migration Guide: Layered Architecture 적용

## 🎯 개요

이 프로젝트는 **Layered Architecture**로 리팩토링되었습니다. 이 문서는 기존 사용자를 위한 마이그레이션 가이드입니다.

## 📝 주요 변경사항

### 1. 디렉토리 구조 변경

**이전 구조:**
```
langgraph_translator/
├── config/
├── core/
├── handlers/
├── builders/
├── utils/
└── main.py
```

**새로운 구조:**
```
langgraph_translator/
├── presentation/          # Presentation Layer
├── service/               # Service Layer
├── domain/                # Domain Layer
├── infrastructure/        # Infrastructure Layer
└── common/                # Common utilities
```

### 2. 진입점 변경

#### 이전 방식 (여전히 작동함)
```bash
# 루트에서 실행
python langgraph_translator/main.py
python langgraph_translator/example_usage.py
python langgraph_translator/retry_failed.py
```

#### 새로운 방식 (권장)
```bash
# langgraph_translator 디렉토리에서
cd langgraph_translator

# 메인 애플리케이션
python -m presentation.cli.main

# 사용 예제
python -m presentation.cli.example_usage

# 실패한 번역 재시도
python -m presentation.cli.retry_failed
```

또는:
```bash
cd langgraph_translator/presentation/cli
python main.py
python example_usage.py
python retry_failed.py
```

### 3. Import 경로 변경

커스텀 코드를 작성하는 경우 import 경로가 변경되었습니다:

#### 이전:
```python
from config.settings import SettingsManager
from core.translation_executor import TranslationExecutor
from core.subtitle_manager import SubtitleManager
from builders.pipeline_builder import TranslationPipelineBuilder
```

#### 이후:
```python
from common.config.settings import SettingsManager
from infrastructure.executors.langgraph_executor import LangGraphExecutor
from infrastructure.repositories.subtitle_repository import SubtitleRepository
from service.pipeline.builder import TranslationPipelineBuilder
```

### 4. 클래스 이름 변경

일부 클래스 이름이 역할을 더 명확히 반영하도록 변경되었습니다:

| 이전 | 이후 | 레이어 |
|------|------|--------|
| `TranslationExecutor` | `LangGraphExecutor` | Infrastructure |
| `SubtitleManager` | `SubtitleRepository` | Infrastructure |
| `TranslationPipelineBuilder` | `TranslationPipelineBuilder` | Service |

## 🚀 빠른 시작

### 옵션 1: 구 진입점 사용 (Backward Compatibility)

기존 방식대로 실행하면 자동으로 새 구조로 리다이렉트됩니다:

```bash
cd C:\langgraph_translater
python langgraph_translator\main.py
```

### 옵션 2: 새 진입점 사용 (권장)

```bash
cd C:\langgraph_translater\langgraph_translator
python -m presentation.cli.main
```

## 📚 코드 예제

### 기본 사용법

```python
from common.config.settings import SettingsManager
from service.orchestrator import TranslationOrchestrator

# 설정 생성
settings = SettingsManager(
    groq_api_key="your_api_key",
    lang_codes_str="en,de,ja",
    srt_dir=r"C:\path\to\subtitles"
)

# 오케스트레이터 생성 및 실행
orchestrator = TranslationOrchestrator(settings)
orchestrator.run_batch_translation()
```

### 커스텀 파이프라인

```python
from service.pipeline.builder import TranslationPipelineBuilder
from infrastructure.executors.langgraph_executor import LangGraphExecutor
from infrastructure.repositories.subtitle_repository import SubtitleRepository
from common.utils.path_manager import PathManager
from common.utils.logger_utils import LoggerUtils

# 컴포넌트 초기화
logger = LoggerUtils.setup_logger("CustomPipeline")
path_manager = PathManager(settings.srt_dir)
subtitle_repo = SubtitleRepository(path_manager, settings.lang_codes_list, logger)
executor = LangGraphExecutor(settings, "llama-3.3-70b-versatile", logger)

# 파이프라인 구축
pipeline = (
    TranslationPipelineBuilder()
    .add_validation()
    .add_execution(executor, max_attempts=3)
    .add_persistence(subtitle_repo)
    .add_logging(logger)
    .build()
)
```

## 🔧 환경 설정

`.env` 파일 설정은 동일합니다:

```env
GROQ_API_KEY=your_groq_api_key_here
LANG_CODES=en,de,ja,es,fr
SRT_DIR=C:\path\to\your\subtitles
MODEL_PRIORITY_INDEX=3
WORKER_COUNT=6
BATCH_SIZE=12
SAVE_INTERVAL=24
```

## 🏗️ Architecture 이해하기

### Layered Architecture 원칙

1. **Presentation Layer** (`presentation/`)
   - 사용자 인터페이스 (CLI, API 등)
   - Service Layer만 의존

2. **Service Layer** (`service/`)
   - 비즈니스 로직 조율
   - Domain과 Infrastructure 조율

3. **Domain Layer** (`domain/`)
   - 핵심 비즈니스 모델
   - **다른 레이어에 의존하지 않음**

4. **Infrastructure Layer** (`infrastructure/`)
   - 데이터 액세스
   - 외부 서비스 (LangGraph, 파일시스템)

5. **Common** (`common/`)
   - 모든 레이어에서 사용 가능한 공통 코드

### 의존성 방향

```
Presentation → Service → Domain ← Infrastructure
                           ↑
                       Common (모두 사용)
```

## ⚠️ 주의사항

1. **구 디렉토리**: `builders/`, `config/`, `core/`, `handlers/`, `utils/` 디렉토리는 백업용으로 남겨져 있습니다. 새 구조가 정상 작동하는 것을 확인한 후 삭제하실 수 있습니다.

2. **Backward Compatibility**: 구 진입점 파일(`main.py`, `example_usage.py`, `retry_failed.py`)은 새 구조로 자동 리다이렉트되도록 설정되어 있습니다.

3. **Import 오류**: 커스텀 코드에서 import 오류가 발생하면 위의 "Import 경로 변경" 섹션을 참조하세요.

## 🐛 문제 해결

### Import 오류가 발생하는 경우

```bash
ModuleNotFoundError: No module named 'config.constants'
```

**해결방법**: 올바른 디렉토리에서 실행하고 있는지 확인하세요.

```bash
cd C:\langgraph_translater\langgraph_translator
python -m presentation.cli.main
```

### 여전히 구 경로를 사용하는 파일이 있는 경우

프로젝트 전체에서 구 import 패턴을 검색:

```bash
# Windows
findstr /s /i "from config.constants" *.py
findstr /s /i "from core." *.py

# Linux/Mac
grep -r "from config.constants" .
grep -r "from core\." .
```

## 📖 추가 문서

- `README.md`: 프로젝트 개요 및 사용법
- `ARCHITECTURE.md`: 아키텍처 상세 설명 (있는 경우)

## 💡 도움이 필요하신가요?

질문이나 문제가 있으시면 GitHub Issues를 통해 문의해주세요.

---

**마이그레이션 일자**: 2025-11-14
**버전**: 2.0.0 (Layered Architecture)
