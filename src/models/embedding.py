import re

from sqlalchemy import (
    Column,
    String,
    Text,
    Enum
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from pgvector.sqlalchemy import Vector

from src.configs.database import Base
from src.configs.enums import EntityType

from src.configs.regex import (
    MONGO_ID_REGEX
)

from src.configs.field_lengths import (
    FIELD_LENGTHS
)


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(
        UUID,
        primary_key=True
    )

    entity_id = Column(
        String,
        nullable=False
    )

    project_id = Column(
        String,
        nullable=False
    )

    entity_type = Column(
        Enum(EntityType),
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    embedding = Column(
        Vector(1024),
        nullable=False
    )

    @validates("entity_id", "project_id")
    def validate_mongo_id(
        self,
        key,
        value
    ):
        if not value:
            raise ValueError(
                f"{key} is required"
            )

        if not re.fullmatch(
            MONGO_ID_REGEX,
            value
        ):
            raise ValueError(
                f"Invalid MongoDB ID for {key}"
            )

        return value

    @validates("title")
    def validate_title(
        self,
        key,
        value
    ):
        if not value:
            raise ValueError(
                "Title is required"
            )

        value = value.strip()

        min_length = FIELD_LENGTHS[
            "titleLength"
        ]["min"]

        max_length = FIELD_LENGTHS[
            "titleLength"
        ]["max"]

        if not (
            min_length
            <= len(value)
            <= max_length
        ):
            raise ValueError(
                f"Title must be between "
                f"{min_length} and "
                f"{max_length} characters"
            )

        return value

    @validates("description")
    def validate_description(
        self,
        key,
        value
    ):
        if not value:
            raise ValueError(
                "Description is required"
            )

        value = value.strip()

        min_length = FIELD_LENGTHS[
            "descriptionLength"
        ]["min"]

        max_length = FIELD_LENGTHS[
            "descriptionLength"
        ]["max"]

        if not (
            min_length
            <= len(value)
            <= max_length
        ):
            raise ValueError(
                f"Description must be between "
                f"{min_length} and "
                f"{max_length} characters"
            )

        return value