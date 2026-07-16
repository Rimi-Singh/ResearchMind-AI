import logging
import os
from logging.handlers import RotatingFileHandler

# =====================================================
# Log Directory
# =====================================================

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "app.log")

os.makedirs(LOG_FOLDER, exist_ok=True)

# =====================================================
# Logger Configuration
# =====================================================

logger = logging.getLogger("ResearchMindAI")

# Prevent duplicate handlers when FastAPI reloads
if not logger.handlers:

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console Output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Log File (5 MB x 5 backups)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# =====================================================
# Reduce Third-Party Logging Noise
# =====================================================

logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
logging.getLogger("transformers").setLevel(logging.WARNING)
logging.getLogger("huggingface_hub").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("faiss").setLevel(logging.WARNING)

logger.info("Logger initialized successfully.")