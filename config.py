from loguru import logger

API_PREFIX: str = "/api/gateway"


logger.add(
    "authentication_logs.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} {level} {message} in {name} {line}",
    level="DEBUG",
    rotation="10 MB",
    compression="zip",
    serialize=True,
)
