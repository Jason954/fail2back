from pydantic import BaseModel


class Action(BaseModel):
    name: str

