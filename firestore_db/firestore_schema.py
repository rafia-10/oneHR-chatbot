def fetch_all_firestore_schemas(db_clients):
    """
    db_clients: dict of Firestore clients {"dev": db_dev, "internal": db_internal}
    Returns list of dicts with db, collection, field, description
    """
    schemas = []
    for db_name, db in db_clients.items():
        collections = db.collections()
        for coll in collections:
            coll_name = coll.id
            try:
                docs = coll.limit(1).stream()  # fetch a sample doc to get fields
                for doc in docs:
                    fields = doc.to_dict().keys()
                    for field in fields:
                        schemas.append({
                            "db": db_name,
                            "collection": coll_name,
                            "field": field,
                            "description": ""  # optional, can fetch from doc metadata if available
                        })
            except Exception:
                continue
    return schemas
