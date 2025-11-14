"""Retry failed translations - DEPRECATED

⚠️  DEPRECATED: This file is kept for backward compatibility only.

The project has been refactored to use Layered Architecture.
Please use the new entry point instead:

    python -m presentation.cli.retry_failed

Or:
    cd presentation/cli
    python retry_failed.py

This file will redirect to the new entry point.
"""

import sys

# Redirect to new structure
print("=" * 80)
print("WARNING: DEPRECATED ENTRY POINT")
print("=" * 80)
print("This retry_failed.py is deprecated. The project has been refactored")
print("to use Layered Architecture.")
print("")
print("Please use the new entry point:")
print("  python -m presentation.cli.retry_failed")
print("")
print("Or navigate to the CLI directory:")
print("  cd presentation/cli")
print("  python retry_failed.py")
print("=" * 80)
print("")
print("Redirecting to new entry point...\n")

# Import and run from new location
try:
    from presentation.cli.retry_failed import main

    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Error: Failed to import new entry point: {e}")
    print("\nPlease ensure you are in the correct directory:")
    print("  C:\\langgraph_translater\\langgraph_translator")
    sys.exit(1)
