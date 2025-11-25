from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from src.db.context import DbContext
from src.entities.sample_entity import SampleEntity
from src.services import SampleService
from .schemas import (
    SampleEntityCreate,
    SampleEntityUpdate,
    SampleEntityResponse,
    SampleEntityListResponse,
    DeleteResponse
)

router = APIRouter()
sample_service = SampleService()


@router.post(
    "/",
    response_model=SampleEntityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new sample entity",
    description="Create a new sample entity with the provided data"
)
async def create_sample_entity(entity_data: SampleEntityCreate):
    """
    Create a new sample entity.

    - **required_uuid**: Required UUID field
    - **string_field**: Required string field
    - **required_jsonb**: Required JSONB field
    - **optional_uuid**: Optional UUID field
    - **optional_text**: Optional text field
    - **optional_jsonb**: Optional JSONB field
    - **big_int**: Big integer field (default: 1)
    """
    async with DbContext.get_session_async() as session:
        entity = SampleEntity(**entity_data.model_dump())
        created_entity = await sample_service.create(session, entity)
        return created_entity


@router.get(
    "/{entity_id}",
    response_model=SampleEntityResponse,
    summary="Get sample entity by ID",
    description="Retrieve a specific sample entity by its UUID"
)
async def get_sample_entity(entity_id: UUID):
    """
    Get a sample entity by ID.

    - **entity_id**: UUID of the entity to retrieve
    """
    async with DbContext.get_session_async() as session:
        entity = await sample_service.get_by_id(session, entity_id)

        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sample entity with ID {entity_id} not found"
            )

        return entity


@router.get(
    "/",
    response_model=SampleEntityListResponse,
    summary="List sample entities",
    description="Retrieve a paginated list of sample entities"
)
async def list_sample_entities(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    include_inactive: bool = Query(False, description="Include inactive/deleted entities")
):
    """
    List sample entities with pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    - **include_inactive**: Include inactive/deleted entities (default: false)
    """
    async with DbContext.get_session_async() as session:
        entities = await sample_service.get_all(session, skip, limit, include_inactive)
        total = await sample_service.count(session, include_inactive)

        return SampleEntityListResponse(
            items=entities,
            total=total,
            skip=skip,
            limit=limit
        )


@router.get(
    "/search/by-string",
    response_model=list[SampleEntityResponse],
    summary="Search sample entities",
    description="Search sample entities by string field"
)
async def search_sample_entities(
    q: str = Query(..., min_length=1, description="Search term"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Search sample entities by string field (case-insensitive).

    - **q**: Search term
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    """
    async with DbContext.get_session_async() as session:
        entities = await sample_service.search_by_string_field(session, q, skip, limit)
        return entities


@router.put(
    "/{entity_id}",
    response_model=SampleEntityResponse,
    summary="Update sample entity",
    description="Update an existing sample entity"
)
async def update_sample_entity(entity_id: UUID, entity_data: SampleEntityUpdate):
    """
    Update a sample entity.

    - **entity_id**: UUID of the entity to update
    - All fields are optional; only provided fields will be updated
    """
    async with DbContext.get_session_async() as session:
        # Filter out None values to only update provided fields
        update_data = {k: v for k, v in entity_data.model_dump().items() if v is not None}

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )

        updated_entity = await sample_service.update(session, entity_id, update_data)

        if not updated_entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sample entity with ID {entity_id} not found"
            )

        return updated_entity


@router.patch(
    "/{entity_id}",
    response_model=SampleEntityResponse,
    summary="Partially update sample entity",
    description="Partially update an existing sample entity"
)
async def patch_sample_entity(entity_id: UUID, entity_data: SampleEntityUpdate):
    """
    Partially update a sample entity (alias for PUT endpoint).

    - **entity_id**: UUID of the entity to update
    - All fields are optional; only provided fields will be updated
    """
    return await update_sample_entity(entity_id, entity_data)


@router.delete(
    "/{entity_id}",
    response_model=DeleteResponse,
    summary="Delete sample entity",
    description="Delete a sample entity (soft delete by default)"
)
async def delete_sample_entity(
    entity_id: UUID,
    hard_delete: bool = Query(False, description="Permanently delete from database")
):
    """
    Delete a sample entity.

    - **entity_id**: UUID of the entity to delete
    - **hard_delete**: If true, permanently delete from database; if false, soft delete (default: false)
    """
    async with DbContext.get_session_async() as session:
        success = await sample_service.delete(session, entity_id, hard_delete)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sample entity with ID {entity_id} not found"
            )

        delete_type = "permanently deleted" if hard_delete else "soft deleted"
        return DeleteResponse(
            success=True,
            message=f"Sample entity {delete_type} successfully",
            id=entity_id
        )

