from hangman_app import create_app
from configurations import configurations

app = create_app()

if __name__ == "__main__":
    app.run(
        host=configurations.FLASK_HOST,
        port=configurations.FLASK_PORT,
        debug=True,
    )
