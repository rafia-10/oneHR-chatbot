from fields2push_dev import fields_to_push_dev
from fields2push_internal import fields_to_push_internal
from firebase_connect import db_dev, db_internal


def prepare_for_qdrant(doc, fields_map):
    prepared = {}
    for key, fields in fields_map.items():
        if key not in doc:
            continue
        for field in fields:
            value = doc[key].get(field)
            if isinstance(value, list):
                # list of dicts?
                if len(value) > 0 and isinstance(value[0], dict):
                    # join text fields from each dict
                    value_text = " ".join(v for d in value for v in d.values() if isinstance(v, str))
                else:
                    # simple list of strings
                    value_text = " ".join(str(v) for v in value)
            elif isinstance(value, dict):
                # just take text values
                value_text = " ".join(str(v) for v in value.values() if isinstance(v, str))
            else:
                value_text = str(value) if value is not None else ""
            prepared[f"{key}_{field}"] = value_text
    return prepared




def fetch_and_prepare(db,fields_to_push):
    all_prepared = {}
    for coll_name, fields in fields_to_push.items():
        docs_snapshots = db.collection(coll_name).get()
        docs = [doc.to_dict() for doc in docs_snapshots]

        prepared_docs = [
            prepare_for_qdrant({coll_name: doc}, {coll_name: fields})
            for doc in docs
        ]
        all_prepared[coll_name] = prepared_docs
    return all_prepared

# For onehr-dev
all_prepared_dev = fetch_and_prepare(db_dev,fields_to_push_dev)

# For onehr-internal
all_prepared_internal = fetch_and_prepare(db_internal,fields_to_push_internal)

