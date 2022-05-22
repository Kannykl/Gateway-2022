from loguru import logger

logger.add(
    "authentication_logs.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} {level} {message} in {name} {line}",
    level="DEBUG",
    rotation="10 MB",
    compression="zip",
    serialize=True,
)
