def list_embedding_service(
    db: Session,
    project_id,
    entity_type=None,
    page=1,
    limit=20
):
    query = (
        db.query(Embedding)
        .filter(
            Embedding.project_id == project_id
        )
    )

    if entity_type:
        query = query.filter(
            Embedding.entity_type == entity_type
        )

    offset = (page - 1) * limit

    return query.offset(offset).limit(limit).all()