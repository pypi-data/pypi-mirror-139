AWS_DEFAULT_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "()": "fastapi_better_logger.AwsFormatter",
            "fmt": "%(levelprefix)s %(message)s (%(filename)s:%(lineno)d)",
        },
        "access": {
            "()": "fastapi_better_logger.AwsAccessFormatter",
            "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "fastapi_better_logger.AwsLogHandler",
            "log_group_name" : "test_log_group_name",
            "log_stream_name" : "test_log_stream_name",
            "use_queues": True,
        },
        "access": {
            "formatter": "access",
            "class": "fastapi_better_logger.AwsAccessLogHandler",
            "log_group_name" : "test_log_group_name",
            "log_stream_name" : "test_log_stream_name",
            "use_queues": True,
        },
    },
    "loggers": {
        "fastapi": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "fastapi.logger": {"handlers": ["access"], "level": "DEBUG", "propagate": False},
        "uvicorn": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}