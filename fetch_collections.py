
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime

# Convert Firestore timestamps to ISO strings
def serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return str(obj)

# ⚡ Initialize Firebase
cred = credentials.Certificate("secrets/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()



# List of all collections
collections = [
    "applicant", "attendance", "attendanceLogic", "competenceAssessment",
    "competenceValue", "customCriteria", "documentManagement", "employee",
    "employeeCompensation", "evaluationMetrics", "flexibilityParameter", "hiringNeed",
    "hrSettings", "jobApplication", "jobPost", "leaveManagement", "matchingProfile",
    "multipleChoice", "objective", "overtimeRequest", "performanceEvaluation",
    "quiz", "requestedAttendanceModification", "screeningQuestions", "shortAnswer",
    "trainingMaterial", "trainingMaterialCertification", "trainingPath", "weightDefinition"
]

all_data = []

def fetch_collection(col_name):
    col_ref = db.collection(col_name)
    docs = list(col_ref.stream())
    result = []
    for doc in docs:
        data = doc.to_dict()
        data['_id'] = doc.id
        data['_collection'] = col_name
        result.append(data)
    return result

for col in collections:
    try:
        docs = fetch_collection(col)
        print(f"Fetched {len(docs)} docs from {col}")
        all_data.extend(docs)
    except Exception as e:
        print(f"Error fetching {col}: {e}")

# Optional: save to JSON for RAG ingestion

with open("all_collections.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2, default=serialize)

print(f"Total documents fetched: {len(all_data)}")
