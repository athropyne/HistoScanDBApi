import datetime
import re

from pydantic import BaseModel, Field, validate_email, validator


class New_User_Model(BaseModel):
    name: str = Field(..., max_length=100, min_length=1)
    email: str = Field(..., max_length=100, min_length=5)
    password: str = Field(..., min_length=5)

    @validator("email")
    def check_email(cls, email):
        email_regex = re.compile(r'^[a-zA-Z\d]+([.-][a-zA-Z\d]+)*@[a-zA-Z\d]+(-[a-zA-Z\d]+)*\.[a-zA-Z]+$')
        if email_regex.match(email):
            return email
        raise ValueError("no valid email")


class New_User_Container(New_User_Model):
    created_at: datetime.datetime = datetime.datetime.utcnow()


class Update_User_Model(BaseModel):
    name: str | None = Field(None, max_length=100, min_length=1)
    email: str | None = Field(None, max_length=100, min_length=5)
    password: str | None = Field(None, min_length=8)


class Update_User_Container(Update_User_Model):
    updated_at: datetime.datetime = datetime.datetime.utcnow()
