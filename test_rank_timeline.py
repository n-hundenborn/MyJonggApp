"""Test script for the rank timeline chart implementation."""
from pathlib import Path
from src.backend.evaluation.orchestrator import start_evaluation

# Test with the existing data folder
test_folder = Path(r"c:\Users\Nick\Documents\Sandkasten\MyJonggApp\mahjongg-2025-12-21")

print(f"Starting evaluation for folder: {test_folder}")
html_file = start_evaluation(test_folder)
print(f"HTML dashboard generated at: {html_file}")
print(f"Open the file in a browser to view the rank timeline chart.")
