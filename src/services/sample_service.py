import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from src.entities.sample_entity import SampleEntity


class SampleService:
    """
    Service class for handling business logic related to SampleEntity.
    Encapsulates all CRUD operations and business rules.
    """

    def __init__(self):
        self.__logger__ = logging.getLogger(__name__)

    async def create(self, session: AsyncSession, entity: SampleEntity) -> SampleEntity:
        """
        Create a new sample entity.

        Args:
            session: Database session
            entity: SampleEntity instance to create

        Returns:
            Created SampleEntity with generated ID

        Raises:
            Exception: If creation fails
        """
        try:
            session.add(entity)
            await session.flush()
            await session.refresh(entity)
            self.__logger__.info(f"Created sample entity with ID: {entity.id}")
            return entity
        except Exception as e:
            self.__logger__.exception(f"Error creating sample entity: {e}")
            raise

    async def get_by_id(self, session: AsyncSession, entity_id: UUID) -> Optional[SampleEntity]:
        """
        Retrieve a sample entity by ID.

        Args:
            session: Database session
            entity_id: UUID of the entity to retrieve

        Returns:
            SampleEntity if found, None otherwise
        """
        try:
            statement = select(SampleEntity).where(
                SampleEntity.id == entity_id,
                SampleEntity.is_deleted == False,
                SampleEntity.is_active == True
            )
            result = await session.exec(statement)
            entity = result.scalar_one_or_none()

            if entity:
                self.__logger__.info(f"Retrieved sample entity with ID: {entity_id}")
            else:
                self.__logger__.warning(f"Sample entity not found with ID: {entity_id}")

            return entity
        except Exception as e:
            self.__logger__.exception(f"Error retrieving sample entity by ID {entity_id}: {e}")
            raise

    async def get_all(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        include_inactive: bool = False
    ) -> List[SampleEntity]:
        """
        Retrieve all sample entities with pagination.

        Args:
            session: Database session
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            include_inactive: Whether to include inactive/deleted entities

        Returns:
            List of SampleEntity instances
        """
        try:
            statement = select(SampleEntity)

            if not include_inactive:
                statement = statement.where(
                    SampleEntity.is_deleted == False,
                    SampleEntity.is_active == True
                )

            statement = statement.offset(skip).limit(limit).order_by(SampleEntity.created_on.desc())

            result = await session.exec(statement)
            entities = result.scalars().all()

            self.__logger__.info(f"Retrieved {len(entities)} sample entities (skip={skip}, limit={limit})")
            return list(entities)
        except Exception as e:
            self.__logger__.exception(f"Error retrieving sample entities: {e}")
            raise

    async def count(self, session: AsyncSession, include_inactive: bool = False) -> int:
        """
        Count total number of sample entities.

        Args:
            session: Database session
            include_inactive: Whether to include inactive/deleted entities

        Returns:
            Total count of entities
        """
        try:
            statement = select(func.count(SampleEntity.id))

            if not include_inactive:
                statement = statement.where(
                    SampleEntity.is_deleted == False,
                    SampleEntity.is_active == True
                )

            result = await session.exec(statement)
            count = result.scalar_one()

            self.__logger__.info(f"Total sample entities count: {count}")
            return count
        except Exception as e:
            self.__logger__.exception(f"Error counting sample entities: {e}")
            raise

    async def update(
        self,
        session: AsyncSession,
        entity_id: UUID,
        update_data: dict
    ) -> Optional[SampleEntity]:
        """
        Update a sample entity.

        Args:
            session: Database session
            entity_id: UUID of the entity to update
            update_data: Dictionary containing fields to update

        Returns:
            Updated SampleEntity if found, None otherwise

        Raises:
            Exception: If update fails
        """
        try:
            entity = await self.get_by_id(session, entity_id)

            if not entity:
                self.__logger__.warning(f"Cannot update - sample entity not found with ID: {entity_id}")
                return None

            # Update only provided fields
            for field, value in update_data.items():
                if hasattr(entity, field) and field not in ['id', 'created_on']:
                    setattr(entity, field, value)

            await session.flush()
            await session.refresh(entity)

            self.__logger__.info(f"Updated sample entity with ID: {entity_id}")
            return entity
        except Exception as e:
            self.__logger__.exception(f"Error updating sample entity {entity_id}: {e}")
            raise

    async def delete(self, session: AsyncSession, entity_id: UUID, hard_delete: bool = False) -> bool:
        """
        Delete a sample entity (soft delete by default).

        Args:
            session: Database session
            entity_id: UUID of the entity to delete
            hard_delete: If True, permanently delete from database; if False, soft delete

        Returns:
            True if deleted successfully, False if not found

        Raises:
            Exception: If delete fails
        """
        try:
            entity = await self.get_by_id(session, entity_id)

            if not entity:
                self.__logger__.warning(f"Cannot delete - sample entity not found with ID: {entity_id}")
                return False

            if hard_delete:
                await session.delete(entity)
                self.__logger__.info(f"Hard deleted sample entity with ID: {entity_id}")
            else:
                entity.is_deleted = True
                entity.is_active = False
                await session.flush()
                self.__logger__.info(f"Soft deleted sample entity with ID: {entity_id}")

            return True
        except Exception as e:
            self.__logger__.exception(f"Error deleting sample entity {entity_id}: {e}")
            raise

    async def search_by_string_field(
        self,
        session: AsyncSession,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[SampleEntity]:
        """
        Search sample entities by string field (case-insensitive).

        Args:
            session: Database session
            search_term: Term to search for in string_field
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of matching SampleEntity instances
        """
        try:
            statement = select(SampleEntity).where(
                SampleEntity.string_field.ilike(f"%{search_term}%"),
                SampleEntity.is_deleted == False,
                SampleEntity.is_active == True
            ).offset(skip).limit(limit).order_by(SampleEntity.created_on.desc())

            result = await session.exec(statement)
            entities = result.scalars().all()

            self.__logger__.info(
                f"Search for '{search_term}' returned {len(entities)} results"
            )
            return list(entities)
        except Exception as e:
            self.__logger__.exception(f"Error searching sample entities: {e}")
            raise

