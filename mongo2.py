
import base64
import os
from typing import Optional, List, Dict, Any
from pymongo import MongoClient
from bson import ObjectId

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "AVATARS"
COLL_NAME = "avatars"

def get_collection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLL_NAME]

def save_avatar_from_file(user_id: str, filepath: str, content_type: Optional[str] = None) -> ObjectId:
    with open(filepath, "rb") as f:
        b = f.read()
    b64 = base64.b64encode(b).decode("utf-8")
    doc = {
        "user_id": user_id,
        "filename": os.path.basename(filepath),
        "content_type": content_type or "application/octet-stream",
        "data_b64": b64
    }
    coll = get_collection()
    res = coll.insert_one(doc)
    return res.inserted_id

def save_avatar_from_bytes(user_id: str, data: bytes, filename: str = "avatar.bin", content_type: Optional[str] = None) -> ObjectId:
    b64 = base64.b64encode(data).decode("utf-8")
    doc = {
        "user_id": user_id,
        "filename": filename,
        "content_type": content_type or "application/octet-stream",
        "data_b64": b64
    }
    coll = get_collection()
    res = coll.insert_one(doc)
    return res.inserted_id

def get_avatar_bytes(doc_id: str) -> Optional[bytes]:
    coll = get_collection()
    doc = coll.find_one({"_id": ObjectId(doc_id)})
    if not doc:
        return None
    return base64.b64decode(doc["data_b64"])

def save_avatar_to_file(doc_id: str, out_path: str) -> bool:
    data = get_avatar_bytes(doc_id)
    if data is None:
        return False
    with open(out_path, "wb") as f:
        f.write(data)
    return True

def list_avatars(limit: int = 50) -> List[Dict[str, Any]]:
    coll = get_collection()
    docs = coll.find({}, {"data_b64": 0}).limit(limit)
    return list(docs)

def delete_avatar(doc_id: str) -> bool:
    coll = get_collection()
    res = coll.delete_one({"_id": ObjectId(doc_id)})
    return res.deleted_count == 1

if __name__ == "__main__":
    if os.path.exists("p1.jpg"):
        id1 = save_avatar_from_file("user1", "p1.jpg", content_type="image/jpg")
        print("Saved id:", id1)
    else:
        print("p1.jpg не найден")

    if os.path.exists("p2.jpg"):
        id2 = save_avatar_from_file("user2", "p2.jpg", content_type="image/jpg")
        print("Saved id:", id2)
    else:
        print("p2.jpg не найден")

    print("Avatars list:")
    for d in list_avatars():
        print(d)

    try:
        if id2:
            ok = save_avatar_to_file(str(id2), "out_avatar.bin")
            print("Saved to out_avatar.bin:", ok)
    except Exception as e:
        print("Ошибка при сохранении:", e)
