# GitHub 업로드 가이드

프로젝트를 GitHub에 업로드하기 위한 단계별 가이드입니다.

## ✅ 완료된 작업

### 1. 프로젝트 정리
- ✅ 구 디렉토리를 `_backup_old_structure/`로 이동
- ✅ Layered Architecture로 재구성
- ✅ 모든 import 경로 수정
- ✅ 불필요한 파일 정리

### 2. 문서화
- ✅ README.md 업데이트 (언어 변경 방법 포함)
- ✅ MIGRATION_GUIDE.md 추가
- ✅ LICENSE 파일 (MIT)
- ✅ .env.example 업데이트
- ✅ .gitignore 업데이트

### 3. Git 준비
- ✅ 모든 변경사항 staged
- ✅ 파일 이동 감지 완료

## 🚀 GitHub 업로드 단계

### 1단계: 현재 변경사항 커밋

```bash
cd C:\langgraph_translater\langgraph_translator

# 커밋 생성
git commit -m "Refactor: Apply Layered Architecture

- Restructured project into 4 layers: Presentation, Service, Domain, Infrastructure
- Added Common layer for shared utilities
- Updated all import paths
- Added comprehensive documentation
- Updated README with language change instructions
- Added MIGRATION_GUIDE.md for existing users
- Moved old structure to _backup_old_structure/

Breaking Changes:
- Import paths have changed
- Class names updated (SubtitleManager -> SubtitleRepository, TranslationExecutor -> LangGraphExecutor)
- New entry point: python -m presentation.cli.main
- Old entry points still work with automatic redirection"
```

### 2단계: GitHub 저장소 생성

1. GitHub (https://github.com)에 로그인
2. 새 저장소 생성 (New Repository)
   - Repository name: `langgraph-subtitle-translator`
   - Description: `AI-powered subtitle translator using LangChain & LangGraph with Layered Architecture`
   - Public 또는 Private 선택
   - **Initialize this repository 체크하지 않음** (이미 로컬에 코드가 있음)

### 3단계: 원격 저장소 연결

```bash
# 원격 저장소 추가 (GitHub에서 제공하는 URL 사용)
git remote add origin https://github.com/YOUR_USERNAME/langgraph-subtitle-translator.git

# 또는 SSH 사용
git remote add origin git@github.com:YOUR_USERNAME/langgraph-subtitle-translator.git

# 원격 저장소 확인
git remote -v
```

### 4단계: 푸시

```bash
# main 브랜치로 푸시
git push -u origin main

# 또는 master 브랜치인 경우
git push -u origin master
```

## 📋 GitHub Repository 설정

### Repository Description
```
AI-powered subtitle translator using LangChain & LangGraph with clean Layered Architecture. Supports multiple languages with context-aware translation.
```

### Topics (Keywords)
```
langchain, langgraph, ai, translation, subtitles, srt, python,
layered-architecture, clean-code, groq, llm, multilingual
```

### About 섹션 추가
- ✅ Website: (프로젝트 웹사이트가 있다면)
- ✅ Topics: 위의 키워드 추가

## 🔧 .gitignore 확인사항

다음 파일들이 제외되는지 확인:
- ✅ `.env` (API 키 보호)
- ✅ `__pycache__/`
- ✅ `*.pyc`
- ✅ `venv/`, `env/`
- ✅ `_backup_old_structure/`
- ✅ 번역된 자막 파일 (`*.srt`)

## 📝 GitHub README 미리보기

프로젝트의 README.md는 다음을 포함합니다:
- ✅ 프로젝트 개요
- ✅ Architecture 다이어그램
- ✅ Quick Start 가이드
- ✅ **번역 언어 변경 방법** (3가지)
- ✅ 사용 예제
- ✅ 설정 옵션
- ✅ 지원 모델 목록

## 🎯 푸시 후 확인사항

1. **GitHub 페이지 확인**
   - README가 제대로 렌더링되는지
   - 디렉토리 구조가 올바른지
   - .env 파일이 없는지 (보안)

2. **Clone 테스트**
   ```bash
   # 새 디렉토리에서 테스트
   git clone https://github.com/YOUR_USERNAME/langgraph-subtitle-translator.git
   cd langgraph-subtitle-translator

   # 의존성 설치
   pip install -r requirements.txt

   # .env 파일 생성
   cp .env.example .env
   # .env 파일을 편집하여 실제 값 입력

   # 실행 테스트
   python -m presentation.cli.main
   ```

3. **Issues & Pull Requests 활성화**
   - Settings → Features
   - Issues 체크
   - Pull Requests 체크

## 🌟 선택사항: GitHub Actions 설정

`.github/workflows/test.yml` 파일을 추가하여 자동 테스트:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python -m pytest tests/
```

## 📌 중요 보안 사항

### ⚠️ 절대 업로드하면 안 되는 것:
- ❌ `.env` 파일 (API 키 포함)
- ❌ 개인 자막 파일
- ❌ API 키나 비밀번호가 포함된 파일

### ✅ 업로드해도 안전한 것:
- ✅ `.env.example` (예제 파일, 실제 값 없음)
- ✅ 소스 코드
- ✅ 문서 (README, MIGRATION_GUIDE 등)
- ✅ 설정 파일 (requirements.txt, .gitignore 등)

## 🔄 업데이트 workflow

향후 업데이트 시:
```bash
# 변경사항 확인
git status

# 변경사항 추가
git add .

# 커밋
git commit -m "Update: 변경 내용 설명"

# 푸시
git push origin main
```

## 💡 문제 해결

### 푸시가 거부되는 경우
```bash
# 원격 변경사항 가져오기
git pull origin main --rebase

# 충돌 해결 후
git push origin main
```

### 대용량 파일 경고
```bash
# 파일 제거
git rm --cached large_file.xxx
git commit -m "Remove large file"
git push origin main
```

## 🎉 완료!

모든 단계를 완료하면 프로젝트가 GitHub에 성공적으로 업로드됩니다!

Repository URL: `https://github.com/YOUR_USERNAME/langgraph-subtitle-translator`
