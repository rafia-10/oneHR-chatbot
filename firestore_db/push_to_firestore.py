from .extract_structured import extract_structured
from firebase_connect import db_dev, db_internal

def push_structured_to_firestore(db, db_name):
    collections = db.collections()
    for col_ref in collections:
        collection_name = col_ref.id
        structured_collection_name = f"{collection_name}_structured"
        print(f"Processing '{collection_name}' → pushing to '{structured_collection_name}' in {db_name} DB")

        for doc in col_ref.stream():
            doc_data = doc.to_dict()
            structured_fields = extract_structured(doc_data)

            # Save structured fields as a subcollection or separate collection
            db.collection(structured_collection_name).document(doc.id).set({
                "doc_id": doc.id,
                "structured_fields": structured_fields
            })

        print(f"✅ Finished pushing structured fields for collection '{collection_name}'")

push_structured_to_firestore(db_dev, "dev")
push_structured_to_firestore(db_internal, "internal")

