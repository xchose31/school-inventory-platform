from app import app, models
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == '__main__':
    app.run(host=os.getenv("FLASK_RUN_HOST"), port=os.getenv("FLASK_RUN_PORT"), debug=False)