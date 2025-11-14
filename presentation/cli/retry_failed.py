"""Retry failed translations manually.

This is part of the Presentation Layer - CLI tool for retrying failed translations.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from common.config.settings import SettingsManager
from service.orchestrator import TranslationOrchestrator


def main():
    """Manually retry failed items."""
    # Load environment variables (from project root)
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"
    load_dotenv(dotenv_path=env_path)

    # Get configuration
    groq_api_key = os.getenv("GROQ_API_KEY")
    lang_codes_str = os.getenv("LANG_CODES", "ja")
    srt_dir = os.getenv("SRT_DIR", r"C:\langgraph_translater\a_channel\b_content")

    # Create settings
    settings = SettingsManager(
        groq_api_key=groq_api_key,
        lang_codes_str=lang_codes_str,
        srt_dir=srt_dir,
    )

    # Create orchestrator
    orchestrator = TranslationOrchestrator(settings)

    # Retry failed items (max 5 attempts per item)
    print("Searching for failed items and retrying...")
    orchestrator.manual_retry_failed(max_retries=5)

    print("\nRetry completed!")


if __name__ == "__main__":
    main()
