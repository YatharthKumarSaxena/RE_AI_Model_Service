from src.main import initialize_application
from src.configs.settings import HOST, PORT


if __name__ == "__main__":

    app = initialize_application()

    app.run(
        host=HOST,
        port=PORT,
        debug=True
    )