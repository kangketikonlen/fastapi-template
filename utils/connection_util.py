import os
import motor.motor_asyncio
from os.path import join
from dotenv import load_dotenv

# Load dotenv
dotenv_path = join('./', '.env')
load_dotenv(dotenv_path)

# Database setting
mongodb_uri = os.environ.get("MONGODB_URI")
client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_uri)
database = client.fastapi
