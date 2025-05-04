import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', '5551'))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'hospital_management')

    @classmethod
    def print_config(cls):
        print("Current Configuration:")
        print(f"MYSQL_HOST: {cls.MYSQL_HOST}")
        print(f"MYSQL_PORT: {cls.MYSQL_PORT}")
        print(f"MYSQL_USER: {cls.MYSQL_USER}")
        print(f"MYSQL_DB: {cls.MYSQL_DB}")
        # Don't print the password for security reasons 