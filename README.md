# Documents API

Made to store text files in a noSQL database.

**Technologies used:**
- Python
- FastAPI
- Decouple
- Motor
- MongoDB

## How to create server with uvicorn
1. First install the python packages
```python
pip install -r requirements.txt
```
2. Run the server
```python
uvicorn main:app --reload
```

## How to generate markdown documentation with Widdershins
```shell
widdershins openapi.yaml -o README.md --omitHeader --language_tabs 'python:Python'
```
---
<!-- Generator: Widdershins v4.0.1 -->
<h1 id="custom-api">Documents API v0.1.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

This is a custom API for testing purposes.

<h1 id="custom-api-documents">documents</h1>

## get_documents_documents__get

<a id="opIdget_documents_documents__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/documents/', headers = headers)

print(r.json())

```

`GET /documents/`

*Get Documents*

> Example responses

> 200 Response

```json
null
```

<h3 id="get_documents_documents__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|get all documents from database|Inline|

<h3 id="get_documents_documents__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## add_document_data_documents__post

<a id="opIdadd_document_data_documents__post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/documents/', headers = headers)

print(r.json())

```

`POST /documents/`

*Add Document Data*

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

<h3 id="add_document_data_documents__post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[DocumentSchema](#schemadocumentschema)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="add_document_data_documents__post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|add document in the database|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="add_document_data_documents__post-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## get_document_data_documents__id__get

<a id="opIdget_document_data_documents__id__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/documents/{id}', headers = headers)

print(r.json())

```

`GET /documents/{id}`

*Get Document Data*

<h3 id="get_document_data_documents__id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|any|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="get_document_data_documents__id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|get document from database from id|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get_document_data_documents__id__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## update_document_data_documents__id__put

<a id="opIdupdate_document_data_documents__id__put"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.put('/documents/{id}', headers = headers)

print(r.json())

```

`PUT /documents/{id}`

*Update Document Data*

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
  "last_updated": "2023-03-24T00:56:44.989645",
  "acess": 0,
  "type": "document"
}
```

<h3 id="update_document_data_documents__id__put-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|string|true|none|
|body|body|[UpdateDocumentSchema](#schemaupdatedocumentschema)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="update_document_data_documents__id__put-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|update document in database|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="update_document_data_documents__id__put-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## delete_document_data_documents__id__delete

<a id="opIddelete_document_data_documents__id__delete"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.delete('/documents/{id}', headers = headers)

print(r.json())

```

`DELETE /documents/{id}`

*Delete Document Data*

<h3 id="delete_document_data_documents__id__delete-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|id|path|string|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="delete_document_data_documents__id__delete-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|delete document from the database from id|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="delete_document_data_documents__id__delete-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

## get_document_data_by_name_documents_name__name__get

<a id="opIdget_document_data_by_name_documents_name__name__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/documents/name/{name}', headers = headers)

print(r.json())

```

`GET /documents/name/{name}`

*Get Document Data By Name*

<h3 id="get_document_data_by_name_documents_name__name__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|name|path|any|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="get_document_data_by_name_documents_name__name__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|get document from database from name|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="get_document_data_by_name_documents_name__name__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_DocumentSchema">DocumentSchema</h2>
<!-- backwards compatibility -->
<a id="schemadocumentschema"></a>
<a id="schema_DocumentSchema"></a>
<a id="tocSdocumentschema"></a>
<a id="tocsdocumentschema"></a>

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

DocumentSchema

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|
|path|string|true|none|none|
|content|string|true|none|none|
|date_added|string|true|none|none|
|tags|[string]|true|none|none|
|references|[string]|true|none|none|
|last_updated|string(date-time)|true|none|none|
|acess|integer|true|none|none|
|type|string|true|none|none|

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>
<!-- backwards compatibility -->
<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```

HTTPValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|[[ValidationError](#schemavalidationerror)]|false|none|none|

<h2 id="tocS_UpdateDocumentSchema">UpdateDocumentSchema</h2>
<!-- backwards compatibility -->
<a id="schemaupdatedocumentschema"></a>
<a id="schema_UpdateDocumentSchema"></a>
<a id="tocSupdatedocumentschema"></a>
<a id="tocsupdatedocumentschema"></a>

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
  "last_updated": "2023-03-24T00:56:44.989645",
  "acess": 0,
  "type": "document"
}

```

UpdateDocumentSchema

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|false|none|none|
|path|string|false|none|none|
|content|string|false|none|none|
|date_added|string|false|none|none|
|tags|[string]|false|none|none|
|references|[string]|false|none|none|
|last_updated|string(date-time)|false|none|none|
|acess|integer|false|none|none|
|type|string|false|none|none|

<h2 id="tocS_ValidationError">ValidationError</h2>
<!-- backwards compatibility -->
<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": [
    "string"
  ],
  "msg": "string",
  "type": "string"
}

```

ValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|loc|[anyOf]|true|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|integer|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|msg|string|true|none|none|
|type|string|true|none|none|

