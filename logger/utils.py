from django.utils import timezone


def log_system_error(function_name, message):
    # TODO: Create log models
    print(function_name, f"message: {message}")
