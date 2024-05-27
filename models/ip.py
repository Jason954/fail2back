from pydantic import BaseModel


class Ip(BaseModel):
    ip: str
