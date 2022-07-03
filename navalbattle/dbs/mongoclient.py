from models import ODM
from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

client = AsyncIOMotorClient(username="vito", password="S3cret", host="mongo")
aiomongo = AIOEngine(motor_client=client, database="navalbattle")
