from sqlalchemy.orm import Session

from src.models.embedding import Embedding


def get_embedding_service(
    db: Session,
    entity_id,
    entity_type
):
    embedding = (
        db.query(Embedding)
        .filter(
            Embedding.entity_id == entity_id,
            Embedding.entity_type == entity_type
        )
        .first()
    )

    if not embedding:
        raise ValueError(
            "Embedding not found for entity"
        )

    return embedding