from pydantic.main import BaseModel


class Response_Model(BaseModel):
    msg: str | None
    data: dict | list[dict] | None
