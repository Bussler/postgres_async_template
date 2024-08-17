import logging

from app.config import CONFIGS

logging.basicConfig(
    level=CONFIGS.instance.LOGGER_CONFIG.level,
    format="%(asctime)s - %(levelname)s - %(module)s: %(message)s",
    datefmt="%H:%M:%S",
)

logger: logging.Logger = logging.getLogger(__name__)