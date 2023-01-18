import datetime

from pydantic import Field, BaseModel, FilePath


class New_Image_Model(BaseModel):
    filename: str = Field(..., max_length=50)
    description: str | None = Field(None, max_length=1000)
    svs_url: str
    jpg_url: str | None
    creator_id: int


class New_Image_Container(BaseModel):
    filename: str = Field(..., max_length=50)
    description: str | None = Field(None, max_length=1000)
    creator_id: int
    image_url: str
    creator_id: int
    created_at: datetime.datetime = datetime.datetime.utcnow()
