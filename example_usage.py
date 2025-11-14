"""Example usage scenarios - DEPRECATED

⚠️  DEPRECATED: This file is kept for backward compatibility only.

The project has been refactored to use Layered Architecture.
Please use the new entry point instead:

    python -m presentation.cli.example_usage

Or:
    cd presentation/cli
    python example_usage.py

This file will redirect to the new entry point.
"""

import sys

# Redirect to new structure
print("=" * 80)
print("WARNING: DEPRECATED ENTRY POINT")
print("=" * 80)
print("This example_usage.py is deprecated. The project has been refactored")
print("to use Layered Architecture.")
print("")
print("Please use the new entry point:")
print("  python -m presentation.cli.example_usage")
print("")
print("Or navigate to the CLI directory:")
print("  cd presentation/cli")
print("  python example_usage.py")
print("=" * 80)
print("")
print("Redirecting to new entry point...\n")

# Import and run from new location
try:
    from presentation.cli import example_usage

    if __name__ == "__main__":
        # Run the example menu
        from dotenv import load_dotenv
        from pathlib import Path

        # Load environment variables
        project_root = Path(__file__).parent
        env_path = project_root / ".env"
        load_dotenv(dotenv_path=env_path)

        while True:
            example_usage.print_menu()
            choice = input("\nSelect example (0-7): ").strip()

            if choice == "0":
                print("Exiting...")
                break
            elif choice == "1":
                example_usage.example_basic_usage()
            elif choice == "2":
                example_usage.example_custom_settings()
            elif choice == "3":
                example_usage.example_resume_translation()
            elif choice == "4":
                example_usage.example_manual_retry()
            elif choice == "5":
                example_usage.example_custom_pipeline()
            elif choice == "6":
                example_usage.example_batch_processing()
            elif choice == "7":
                example_usage.example_different_models()
            else:
                print("Invalid choice. Please try again.")

            input("\nPress Enter to continue...")

except ImportError as e:
    print(f"Error: Failed to import new entry point: {e}")
    print("\nPlease ensure you are in the correct directory:")
    print("  C:\\langgraph_translater\\langgraph_translator")
    sys.exit(1)
