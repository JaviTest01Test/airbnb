import sys
import os

# Add the 'src' folder to the Python path before importing
sys.path.append(os.path.join(os.getcwd(), '..', 'src'))

import pytest
from transformations import format_date

def test_format_date_with_valid_date():
    assert format_date("2024-10-07") == "Monday 07 October 2024"

def test_format_date_with_empty_string():
    assert format_date("") == "no review"

def test_format_date_with_invalid_format():
    assert format_date("07-10-2024oiop") == "invalid date"