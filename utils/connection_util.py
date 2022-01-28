import motor.motor_asyncio

# Database setting
mongodb_uri = "mongodb://localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_uri)
database = client.fastapi
