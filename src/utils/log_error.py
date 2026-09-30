from src.utils.time_stamps import log_with_time

def error_message(err):
    log_with_time("🛑 Error occurred:")
    log_with_time(
        "File Name and Line Number where this error occurred is displayed below:- "
    )

    print(err.__traceback__)

    log_with_time("Error Message is displayed below:- ")
    print(str(err))


def log_middleware_error(middleware_name, reason):

    log_with_time(
        f"❌ [{middleware_name}Middleware] Error: {reason} "
    )