from typing import List

import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

from api.api_logging import logger


MONGO_DETAILS = config("URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.warehouse
document_collection = database.get_collection("documents")

# helpers
def document_helper(document) -> dict:
    return {
        "id": str(document.get("_id")),
        "path": document.get("path", ""),
        "name": document.get("name"),
        "content": document.get("content"),
        "date_added": document.get("date_added", ""),
        "tags": document.get("tags", ""),
        "references": document.get("references", ""),
        "last_updated": document.get("last_updated", ""),
        "acess": document.get("acess", 0),
        "type": document.get("type", "") ,
    }

async def get_all_documents() -> List[dict]:
    result = [ document_helper(document) async for document in document_collection.find()]
    logger.info(f"found [{len(result)}] documents")
    return result

async def get_document(id: str) -> dict:
    document = await document_collection.find_one({"_id": ObjectId(str(id))})
    if document:
        logger.info(f"document with id [{id}] found")
        return document_helper(document)
    logger.info(f"document with id [{id}] was not found")
    return

async def get_document_by_name(name: str) -> dict:
    document = await document_collection.find_one({"name": name})
    if document:
        logger.debug(f"document [{name}] found on database")
        return document_helper(document)

    logger.debug(f"document [{name}] was not found on database")
    return

async def add_document(document_data: dict) -> dict:
    name = document_data["name"]
    if await get_document_by_name(name):
        logger.debug(f"theres already a document with that name [{name}]")
        return None

    document = await document_collection.insert_one(document_data)
    new_document = await document_collection.find_one( {"_id": document.inserted_id})
    logger.debug(f"document [{name}] added to database")
    return document_helper(new_document)

async def put_document(id: str, data: dict) -> dict:
    if len(data) < 1:
        logger.info("theres 0 documents on database, can't update")
        return
    
    document = await document_collection.find_one({"_id": ObjectId(str(id))})
    if document:
        updated_document = await document_collection.update_one(
            {"_id": ObjectId(str(id))}, {"$set": data}
        )
        logger.info("document [{updated_document.name}] with id [{id}] was updated.")
        return updated_document
    
    logger.info(f"document with id [{id}] was not found")
    return 

async def del_document(id: str) -> dict:
    document = await document_collection.find_one({"_id": ObjectId(str(id))})
    if document:
        await document_collection.delete_one({"_id": ObjectId(str(id))})
        logger.info(f"document with id [{id}] was deleted")
        return document

    logger.info(f"document with id [{id}] was deleted")
    return 