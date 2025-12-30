from datetime import datetime
from typing import Dict

def set_audit_fields(obj: object, user_id: int, is_create: bool = True) -> object:
    now = datetime.utcnow()

    if is_create:
        # Set creation fields if not already set
        if not getattr(obj, "created_at", None):
            setattr(obj, "created_at", now)
        # Set created_by only if it is not already set    
        if not getattr(obj, "created_by", None):
            setattr(obj, "created_by", user_id)

    setattr(obj, "updated_at", now)
    setattr(obj, "updated_by", user_id)

    return obj