import dotenv
import os

dotenv.load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
host = os.getenv("DB_HOST")