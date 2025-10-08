#!/bin/bash
# Helper script to run the extractor with virtual environment

# Activate virtual environment
source venv/bin/activate

# Run the script with all passed arguments
python extract_media.py "$@"
