@echo off
REM LangGraph Translator - 간단 실행 스크립트
REM
REM 사용법:
REM   run.bat           - 메인 번역 실행
REM   run.bat examples  - 사용 예제 실행
REM   run.bat retry     - 실패한 번역 재시도

REM 배치 파일이 있는 디렉토리로 이동
cd /d "%~dp0"

if "%1"=="examples" (
    echo 사용 예제 실행 중...
    python -m presentation.cli.example_usage
) else if "%1"=="retry" (
    echo 실패한 번역 재시도 중...
    python -m presentation.cli.retry_failed
) else (
    echo 메인 번역 프로그램 실행 중...
    python -m presentation.cli.main
)
