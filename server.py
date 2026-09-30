from dotenv import load_dotenv

load_dotenv()

from src.main import initialize_application


app = initialize_application()


if __name__ == "__main__":

    from src.configs.settings import HOST, PORT

    app.run(
        host=HOST,
        port=PORT,
        debug=True
    )