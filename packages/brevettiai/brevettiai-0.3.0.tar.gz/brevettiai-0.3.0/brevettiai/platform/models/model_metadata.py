from pydantic import BaseModel
from typing import Optional
from brevettiai import Module


class ModelMetadata(BaseModel):
    id: str
    run_id: str
    name: str
    producer: str
    host_name: Optional[str] = None

    class Config:
        json_encoders = {
            Module: lambda x: x.get_config()
        }
