from dotenv import load_dotenv
import os

load_dotenv(override=False)
DB_CONFIG = dict(
    host = os.getenv('DB_IPADDRESS'),
    database = os.getenv('DB_DATABASE'),
    user = os.getenv('DB_USERNAME'),
    password = os.getenv('DB_PASSWORD'),
    connection_timeout = 10
)
# print(DB_CONFIG)