from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from db.client import db_client
from typing import get_type_hints

def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
def validate_object_id_or_false(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        return False