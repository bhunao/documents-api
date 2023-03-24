# Documents API
This is a simple API built using FastAPI that performs CRUD (Create, Read, Update, Delete) operations on a database of documents.

## The API has the following routes:

Routes
### `GET /`

    Returns all documents from the database.

### `GET /{id}`

    Returns a specific document from the database based on the ID.

### `GET /name/{name}`

    Returns a specific document from the database based on the name.

### `POST /`

    Adds a new document to the database.

> Body parameter

```json
{
  "name": "example name",
  "path": "",
  "content": "content example lorem ipsum something something whatever",
  "date_added": "202302170314",
  "tags": [
    "example"
  ],
  "references": [
    "example"
  ],
  "last_updated": "2023-03-24T00:56:44.987644",
  "acess": 0,
  "type": "document"
}
```


### `PUT /{id}`

    Updates a specific document in the database based on the ID.

> Body parameter

```json
{
  "name": "example name",
  "path": "",
  "content": "content example lorem ipsum something something whatever",
  "date_added": "202302170314",
  "tags": [
    "example"
  ],
  "references": [
    "example"
  ],
  "last_updated": "2023-03-24T00:56:44.987644",
  "acess": 0,
  "type": "document"
}
```

### `DELETE /{id}`

    Deletes a specific document from the database based on the ID.

### Response Models

The API returns two types of response models: ResponseModel and ErrorResponseModel.

  **ResponseModel** is used to return a successful response along with the data. It has two fields: data (the data returned by the API) and message (a success message).

  **ErrorResponseModel** is used to return an error response. It has two fields: code (the error code) and message (an error message).

## Usage

1. Clone the repository.
```shell
git clone https://github.com/bhunao/documents-api
```
2. Install the dependancies using
```shell
pip install -r requirements.txt
```
3. Run uvicorn. You can then access the API at http://localhost:8000.
```shell
uvicorn main:app --reload
```
4. Access the API at http://localhost:8000.

**Dependencies:**

    - FastAPI
    - Pydantic
    - Motor
    - uvicorn

### Authors

- me [@bhunao](https://github.com/bhunao/)