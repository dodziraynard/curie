from .base import *

try:
    from .local_settings import *
except ImportError:
    pass

if not DEBUG:
    LOGS_ROOT = BASE_DIR / "logs/"
    Path(LOGS_ROOT).mkdir(parents=True, exist_ok=True)

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": True,
        "root": {
            "level": "INFO",
            "handlers": ["file"]
        },
        "handlers": {
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "filename": LOGS_ROOT / "system.log",
                "formatter": "app",
            },
        },
        "loggers": {
            "system": {
                "handlers": ["file"],
                "level": "INFO",
                "propagate": True
            },
        },
        "formatters": {
            "app": {
                "format": (u"%(asctime)s [%(levelname)-8s] "
                           "(%(module)s.%(funcName)s) %(message)s"),
                "datefmt":
                "%Y-%m-%d %H:%M:%S",
            },
        },
    }
