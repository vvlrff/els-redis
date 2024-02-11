from pydantic import BaseModel


class InputUserMessage(BaseModel):
    id: str
    login: str
    password: str