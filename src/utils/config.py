from pathlib import Path

# Project Root (Assumes running from src/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data Directories
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw_screenshots"
PROC_DIR = DATA_DIR / "processed_screenshots"
MD_DIR = DATA_DIR / "markdown_output"
TXT_DIR = DATA_DIR / "text_output"

# OCR Settings
SCALE_FACTOR = 2
