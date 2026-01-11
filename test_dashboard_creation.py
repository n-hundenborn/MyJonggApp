"""Test script for two-page dashboard generation."""

from pathlib import Path
from src.backend.evaluation.orchestrator import start_evaluation

# Test with an existing and filled mahjongg folder
folder_path = Path(__file__).parent / "testfolder"

print(f"Generating dashboard from: {folder_path}")
html_file = start_evaluation(folder_path)
print(f"Dashboard generated successfully: {html_file}")
print(f"\nOpen this file in your browser to view the dashboard!")
