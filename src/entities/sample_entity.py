import enum
from typing import Optional, Dict
from uuid import UUID

from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field

from src import settings
from .base import BaseEntityMixin


class SampleEnum(enum.Enum):
    VALUE_ONE = "value_one"
    VALUE_TWO = "value_two"


class SampleEntity(BaseEntityMixin, table=True):
    __tablename__ = "sample_table"
    __table_args__ = {"schema": f"{settings.database_schema}"}


    required_uuid: UUID = Field(nullable=False) # For Foreign Key reference : Field(foreign_key=f"{settings.database_schema}.table_name.id")
    optional_uuid: Optional[UUID] = Field(default=None, nullable=True)
    string_field: str = Field(nullable=False)
    optional_text: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    required_jsonb: Dict = Field(sa_column=Column(JSONB, nullable=False))
    optional_jsonb: Optional[Dict] = Field(sa_column=Column(JSONB, nullable=True))
    big_int: int = Field(default=1, sa_column=Column(BigInteger, nullable=False, default=1))
