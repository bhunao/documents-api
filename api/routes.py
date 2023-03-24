from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from api.database import (
    get_document,
    get_all_documents,
    get_document_by_name,
    add_document,
    put_document,
    del_document
)
from api.models import (
    ErrorResponseModel,
    ResponseModel,
    DocumentSchema,
    UpdateDocumentSchema
)

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/", response_description="get all documents from database")
async def get_documents():
    documents = await get_all_documents()
    return ResponseModel(documents, f"[{len(documents)}] documents retrived from database")

@router.get("/{id}", response_description="get document from database from id")
async def get_document_data(id):
    document = await get_document(id)
    if document:
        return ResponseModel(document, "document [{id}] retrived scuessfully")
    return ErrorResponseModel(400, f"no document with id [{id}] was found.")

@router.get("/name/{name}", response_description="get document from database from name")
async def get_document_data_by_name(name):
    document = await get_document_by_name(name)
    if document:
        return ResponseModel(document, "document data retrived scuessfully")
    return ErrorResponseModel(400, f"no document with id [{id}] was found.")

@router.post("/", response_description="add document in the database")
async def add_document_data(document: DocumentSchema = Body(...)):
    document = jsonable_encoder(document)
    new_document = await add_document(document)
    if new_document:
        return ResponseModel(new_document, "document [{document.name}] added sucessfully")
    return ErrorResponseModel(400, "document not added")

@router.put("/{id}", response_description="update document in database")
async def update_document_data(id: str, req: UpdateDocumentSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_document = await put_document(id, req)
    if updated_document:
        return ResponseModel("document with ID: [{id}] name update is successful",
            "document name updated successfully")
    return ErrorResponseModel(404, f"There was an error updating the document [{id}]")

@router.delete("/{id}", response_description="delete document from the database from id")
async def delete_document_data(id: str):
    document = await del_document(id)
    if document:
        return ResponseModel(document, "document with ID: [{id}] removed")
    return ErrorResponseModel(404, "document with id [{id}] doesn't exist")
