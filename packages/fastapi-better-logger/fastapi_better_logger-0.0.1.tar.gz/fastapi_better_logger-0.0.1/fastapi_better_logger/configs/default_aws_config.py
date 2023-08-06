AWS_DEFAULT_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "()": "fastapi_better_logger.formatters.AwsFormatter",
            "fmt": "%(levelprefix)s %(message)s",
        },
        "access": {
            "()": "fastapi_better_logger.formatters.AwsAccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "fastapi_better_logger.handlers.AwsLogsHandler",
        },
        "access": {
            "formatter": "access",
            "class": "fastapi_better_logger.handlers.AwsLogsHandler",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}