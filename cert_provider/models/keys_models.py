from pydantic import BaseModel


class KeysByIPModel(BaseModel):
    ip: str
