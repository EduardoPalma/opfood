from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import dotenv_values

config = dotenv_values(".env")

class MongoClient:
    _instance = None

    def __new__(cls, uri=config["URI"], db_name=config["DB_NAME"]):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = AsyncIOMotorClient(uri)
            cls._instance._db = cls._instance._client[db_name]
        return cls._instance

    async def init_models(self, models):
        await init_beanie(database=self._db, document_models=models)

    @property
    def client(self):
        return self._client