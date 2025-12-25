"""Test script for two-page dashboard generation."""

from pathlib import Path
from src.backend.evaluation.orchestrator import start_evaluation

# Test with the existing mahjongg folder
folder_path = Path(r"c:\Users\A22D046\Documents\Privat\MyJonggApp\mahjongg-2025-12-13")

print(f"Generating dashboard from: {folder_path}")
html_file = start_evaluation(folder_path)
print(f"Dashboard generated successfully: {html_file}")
print(f"\nOpen this file in your browser to view the dashboard!")
