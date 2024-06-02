from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from worklog.settings import settings

MONGO_ID_REGEX = r"^[a-f\d]{24}$"

mongo_uri = f"mongodb://{settings.mongo_initdb_root_username}:{settings.mongo_initdb_root_password}@{settings.mongo_host}:27017/"


def get_db() -> AsyncIOMotorDatabase:
    """
    Get MongoDB vs mock based on the setting
    """
    if settings.testing:
        from mongomock_motor import AsyncMongoMockClient

        return AsyncMongoMockClient().worklogDb
    return AsyncIOMotorClient(mongo_uri).worklogDb


db = get_db()
