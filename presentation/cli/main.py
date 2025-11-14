"""Main CLI entry point for the translation application.

This is the Presentation Layer - handles user interaction and system initialization.
"""

import os
import sys
import warnings
import asyncio
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv

# Import from Service Layer
from service.orchestrator import TranslationOrchestrator

# Import from Common Layer
from common.config.settings import SettingsManager, DefaultSettings


# Suppress warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*Event loop is closed.*")
warnings.filterwarnings("ignore", message=".*coroutine.*was never awaited.*")
warnings.filterwarnings("ignore", message=".*Task exception was never retrieved.*")
warnings.filterwarnings("ignore", message=".*Importing verbose from langchain.*")

# Suppress asyncio debug warnings
import logging

logging.getLogger("asyncio").setLevel(logging.CRITICAL)

# Windows event loop policy
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Set custom asyncio exception handler to suppress event loop closure errors
def asyncio_exception_handler(loop, context):
    """Suppress event loop closure errors."""
    exception = context.get("exception")
    if exception:
        error_msg = str(exception).lower()
        # Suppress specific errors
        if any(msg in error_msg for msg in ["event loop is closed", "connection_lost"]):
            return
    # For other exceptions, use default behavior but suppress output
    pass


def main():
    """Main entry point for CLI application."""
    # Load environment variables from .env file
    # Look for .env in the project root (two levels up from this file)
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"
    load_dotenv(dotenv_path=env_path)

    # Get configuration from environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    lang_codes_str = os.getenv("LANG_CODES", "en,de")
    srt_dir = os.getenv("SRT_DIR", r"C:\langgraph_translater\a_channel\b_content")

    # Optional settings with defaults
    model_priority_index = int(os.getenv("MODEL_PRIORITY_INDEX", "0"))
    worker_count = int(
        os.getenv("WORKER_COUNT", str(DefaultSettings.DEFAULT_WORKER_COUNT))
    )
    batch_size = int(os.getenv("BATCH_SIZE", str(DefaultSettings.DEFAULT_BATCH_SIZE)))
    save_interval = int(
        os.getenv("SAVE_INTERVAL", str(DefaultSettings.DEFAULT_SAVE_INTERVAL))
    )

    # Validate required settings
    if not groq_api_key:
        print("Error: GROQ_API_KEY not found in environment variables")
        print("Please create a .env file with your GROQ_API_KEY")
        sys.exit(1)

    # Create settings
    try:
        settings = SettingsManager(
            groq_api_key=groq_api_key,
            lang_codes_str=lang_codes_str,
            srt_dir=srt_dir,
            model_priority_index=model_priority_index,
            worker_count=worker_count,
            batch_size=batch_size,
            save_interval=save_interval,
        )
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    # Create orchestrator (Service Layer)
    orchestrator = TranslationOrchestrator(settings)

    # Run translation
    orchestrator.run_batch_translation()

    print("\nTranslation completed!")


if __name__ == "__main__":
    main()
