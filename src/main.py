from dotenv import load_dotenv
load_dotenv()
from src.app import app
from src.configs.redis_client import get_redis_client
from src.configs.settings import HOST, PORT


def initialize_application():

    get_redis_client()

    print(
        "✅ Connection established with Redis Successfully"
    )

    print(
        "\n🚀 RE Model Service started successfully"
    )

    print(
        f"📡 Server running at: "
        f"http://{HOST}:{PORT}\n"
    )

    return app