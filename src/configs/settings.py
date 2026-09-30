import os

from dotenv import load_dotenv

load_dotenv()

PORT = int(
    os.getenv(
        "PORT",
        8083
    )
)

HOST = os.getenv(
    "HOST",
    "0.0.0.0"
)