# Sample Entity CRUD API

This document describes the CRUD operations available for the Sample Entity.

## Base URL

All endpoints are prefixed with `/api/v1/samples`

## Endpoints

### 1. Create Sample Entity

**POST** `/api/v1/samples/`

Create a new sample entity.

**Request Body:**
```json
{
  "required_uuid": "123e4567-e89b-12d3-a456-426614174000",
  "string_field": "example string",
  "required_jsonb": {"key": "value"},
  "optional_uuid": "123e4567-e89b-12d3-a456-426614174001",
  "optional_text": "optional text content",
  "optional_jsonb": {"optional": "data"},
  "big_int": 1
}
```

**Response:** `201 Created`
```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "required_uuid": "123e4567-e89b-12d3-a456-426614174000",
  "string_field": "example string",
  "required_jsonb": {"key": "value"},
  "optional_uuid": "123e4567-e89b-12d3-a456-426614174001",
  "optional_text": "optional text content",
  "optional_jsonb": {"optional": "data"},
  "big_int": 1,
  "is_active": true,
  "is_deleted": false,
  "created_on": "2024-11-24T10:30:00Z",
  "modified_on": "2024-11-24T10:30:00Z"
}
```

---

### 2. Get Sample Entity by ID

**GET** `/api/v1/samples/{entity_id}`

Retrieve a specific sample entity by its UUID.

**Path Parameters:**
- `entity_id` (UUID): The ID of the entity to retrieve

**Response:** `200 OK`
```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "required_uuid": "123e4567-e89b-12d3-a456-426614174000",
  "string_field": "example string",
  "required_jsonb": {"key": "value"},
  "optional_uuid": "123e4567-e89b-12d3-a456-426614174001",
  "optional_text": "optional text content",
  "optional_jsonb": {"optional": "data"},
  "big_int": 1,
  "is_active": true,
  "is_deleted": false,
  "created_on": "2024-11-24T10:30:00Z",
  "modified_on": "2024-11-24T10:30:00Z"
}
```

**Error Response:** `404 Not Found`
```json
{
  "error": {
    "message": "Sample entity with ID {entity_id} not found",
    "request_id": "..."
  }
}
```

---

### 3. List Sample Entities

**GET** `/api/v1/samples/`

Retrieve a paginated list of sample entities.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)
- `include_inactive` (bool, optional): Include inactive/deleted entities (default: false)

**Example:** `/api/v1/samples/?skip=0&limit=10&include_inactive=false`

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
      "required_uuid": "123e4567-e89b-12d3-a456-426614174000",
      "string_field": "example string",
      "required_jsonb": {"key": "value"},
      "optional_uuid": null,
      "optional_text": null,
      "optional_jsonb": null,
      "big_int": 1,
      "is_active": true,
      "is_deleted": false,
      "created_on": "2024-11-24T10:30:00Z",
      "modified_on": "2024-11-24T10:30:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10
}
```

---

### 4. Search Sample Entities

**GET** `/api/v1/samples/search/by-string`

Search sample entities by string field (case-insensitive).

**Query Parameters:**
- `q` (string, required): Search term
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100, max: 1000)

**Example:** `/api/v1/samples/search/by-string?q=example&skip=0&limit=10`

**Response:** `200 OK`
```json
[
  {
    "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "required_uuid": "123e4567-e89b-12d3-a456-426614174000",
    "string_field": "example string",
    "required_jsonb": {"key": "value"},
    "optional_uuid": null,
    "optional_text": null,
    "optional_jsonb": null,
    "big_int": 1,
    "is_active": true,
    "is_deleted": false,
    "created_on": "2024-11-24T10:30:00Z",
    "modified_on": "2024-11-24T10:30:00Z"
  }
]
```

---

### 5. Update Sample Entity (Full)

**PUT** `/api/v1/samples/{entity_id}`

Update an existing sample entity. Only provided fields will be updated.

**Path Parameters:**
- `entity_id` (UUID): The ID of the entity to update

**Request Body:** (All fields optional)
```json
{
  "required_uuid": "123e4567-e89b-12d3-a456-426614174002",
  "string_field": "updated string",
  "required_jsonb": {"updated": "value"},
  "optional_text": "updated text",
  "big_int": 2,
  "is_active": true
}
```

**Response:** `200 OK`
```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "required_uuid": "123e4567-e89b-12d3-a456-426614174002",
  "string_field": "updated string",
  "required_jsonb": {"updated": "value"},
  "optional_uuid": "123e4567-e89b-12d3-a456-426614174001",
  "optional_text": "updated text",
  "optional_jsonb": {"optional": "data"},
  "big_int": 2,
  "is_active": true,
  "is_deleted": false,
  "created_on": "2024-11-24T10:30:00Z",
  "modified_on": "2024-11-24T10:35:00Z"
}
```

---

### 6. Update Sample Entity (Partial)

**PATCH** `/api/v1/samples/{entity_id}`

Partially update an existing sample entity (alias for PUT endpoint).

Same as PUT endpoint - all fields are optional.

---

### 7. Delete Sample Entity

**DELETE** `/api/v1/samples/{entity_id}`

Delete a sample entity (soft delete by default).

**Path Parameters:**
- `entity_id` (UUID): The ID of the entity to delete

**Query Parameters:**
- `hard_delete` (bool, optional): Permanently delete from database (default: false)

**Example:** `/api/v1/samples/7c9e6679-7425-40de-944b-e07fc1f90ae7?hard_delete=false`

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Sample entity soft deleted successfully",
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
}
```

---

## Service Layer

The business logic is encapsulated in the `SampleService` class located at `src/services/sample_service.py`.

### Available Service Methods

- `create(session, entity)` - Create a new entity
- `get_by_id(session, entity_id)` - Retrieve by ID
- `get_all(session, skip, limit, include_inactive)` - List with pagination
- `count(session, include_inactive)` - Count total entities
- `update(session, entity_id, update_data)` - Update entity
- `delete(session, entity_id, hard_delete)` - Delete entity
- `search_by_string_field(session, search_term, skip, limit)` - Search by string field

### Usage Example

```python
from src.services import SampleService
from src.db.context import DbContext
from uuid import UUID

service = SampleService()

async def example():
    async with DbContext.get_session_async() as session:
        # Get entity by ID
        entity = await service.get_by_id(session, UUID("7c9e6679-7425-40de-944b-e07fc1f90ae7"))
        
        # Update entity
        updated = await service.update(
            session, 
            entity.id, 
            {"string_field": "new value"}
        )
        
        # List all entities
        entities = await service.get_all(session, skip=0, limit=10)
```

---

## Error Handling

All endpoints follow a consistent error response format:

**Error Response Structure:**
```json
{
  "error": {
    "message": "Error description",
    "request_id": "unique-request-id"
  }
}
```

**Common HTTP Status Codes:**
- `200 OK` - Successful GET, PUT, PATCH, DELETE
- `201 Created` - Successful POST
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Entity not found
- `500 Internal Server Error` - Server error

---

## Testing with cURL

### Create an entity:
```bash
curl -X POST "http://localhost:8080/api/v1/samples/" \
  -H "Content-Type: application/json" \
  -d '{
    "required_uuid": "123e4567-e89b-12d3-a456-426614174000",
    "string_field": "test",
    "required_jsonb": {"key": "value"},
    "big_int": 1
  }'
```

### Get entity by ID:
```bash
curl -X GET "http://localhost:8080/api/v1/samples/{entity_id}"
```

### List entities:
```bash
curl -X GET "http://localhost:8080/api/v1/samples/?skip=0&limit=10"
```

### Update entity:
```bash
curl -X PUT "http://localhost:8080/api/v1/samples/{entity_id}" \
  -H "Content-Type: application/json" \
  -d '{"string_field": "updated value"}'
```

### Delete entity:
```bash
curl -X DELETE "http://localhost:8080/api/v1/samples/{entity_id}?hard_delete=false"
```

---

## Interactive Documentation

Visit the following URLs when the application is running:

- **Swagger UI:** http://localhost:8080/docs
- **ReDoc:** http://localhost:8080/redoc

These provide interactive API documentation where you can test all endpoints directly in your browser.

