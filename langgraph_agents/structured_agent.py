from firestore_db.firebase_connect import db_clients

class StructuredAgent:
    """Fetch numeric data from Firestore based on SchemaMatcher output."""

    def run(self, user_query: str, schema: dict):
        if not schema:
            return {"value": None, "aggregation": None, "error": "No schema provided"}

        db = db_clients.get(schema["db"])
        if not db:
            return {"value": None, "aggregation": None, "error": f"DB {schema['db']} not found"}

        try:
            docs = db.collection(schema["collection"]).stream()
            values = [d.to_dict()[schema["field"]] for d in docs 
                      if schema["field"] in d.to_dict() 
                      and isinstance(d.to_dict()[schema["field"]], (int, float))]

            if not values:
                return {"value": None, "aggregation": None, "error": "No numeric data"}

            return {"value": {"count": len(values), "sum": sum(values), "average": sum(values)/len(values)},
                    "aggregation": "count/sum/average"}

        except Exception as e:
            return {"value": None, "aggregation": None, "error": str(e)}
