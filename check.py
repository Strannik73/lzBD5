import os, base64
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
coll = client["AVATARS"]["avatars"]

os.makedirs("avatars_out", exist_ok=True)
for doc in coll.find({}):
    _id = str(doc["_id"])
    name = doc.get("filename") or f"{_id}.bin"
    out = os.path.join("avatars_out", name)
    with open(out, "wb") as f:
        f.write(base64.b64decode(doc["data_b64"]))
print("Экспорт завершён в папку avatars_out")