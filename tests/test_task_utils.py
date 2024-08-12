import pytest
from unittest.mock import patch
from bot.utils.task_utils import is_valid_datetime, get_timezone

# Test cases for is_valid_datetime
@pytest.mark.parametrize("date_string, expected", [
    ("2023-08-12 15:30:45", True), 
    ("2023-13-01 10:00:00", False),
    ("2023-01-32 10:00:00", False),
    ("2023-01-01 25:00:00", False),
    ("2023-01-01 10:61:00", False),
    ("2023-01-01 10:00:61", False),
    ("2023-01-01", False),
    ("", False),
    ("2023-08-12T15:30:45", False),
])
def test_is_valid_datetime(date_string, expected):
    assert is_valid_datetime(date_string) == expected


# Test cases for get_timezone
def test_get_timezone():
    location = (34.0522, -118.2437)
    timezone = get_timezone(location)
    
    assert timezone == "America/Los_Angeles"

    location = (34.0522, -118.2437)
    timezone = get_timezone(location)
    
    assert timezone != "Asia/Jerusalem"


