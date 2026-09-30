from datetime import datetime


def get_time_stamp():
    now = datetime.now().astimezone()

    day_name = now.strftime("%a")
    day = now.strftime("%d")
    month = now.strftime("%b")
    year = now.strftime("%Y")

    hours = now.strftime("%H")
    minutes = now.strftime("%M")
    seconds = now.strftime("%S")

    timezone = now.strftime("%z")
    timezone = f"UTC{timezone[:3]}:{timezone[3:]}"

    return (
        f"[{day_name}, {day} {month} {year}, "
        f"{hours}:{minutes}:{seconds} {timezone}]"
    )


# Custom Time Logger Function
def log_with_time(*args):
    print(f"🕒 {get_time_stamp()}", *args)