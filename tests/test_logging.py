import os
import pytest
import logging
import logging.config
from bot.config.logging_config import logging_config

@pytest.fixture
def log_file():
    log_file_path = 'bot/config/app.log'
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    yield log_file_path
    logging.shutdown()  # Ensure all logging handlers are properly closed
    if os.path.exists(log_file_path):
        os.remove(log_file_path)

def test_logging(log_file):
    # Configure logging for the test
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)

    # Log some test messages
    logger.info("This is an info message for testing.")
    logger.error("This is an error message for testing.")

    # Verify that the log messages were written to the log file
    with open(log_file, 'r') as f:
        log_contents = f.read()
        assert "This is an info message for testing." in log_contents
        assert "This is an error message for testing." in log_contents

