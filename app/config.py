import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    base_url: str = os.getenv("base_url")
    authtoken: str = os.getenv("authtoken")

settings = Settings() 