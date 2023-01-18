import datetime

from models.user_models import New_User_Model, New_User_Container, Update_User_Model, Update_User_Container


class UserPreparer:
    @staticmethod
    def add(*, user: New_User_Model):
        return New_User_Container(
            **user.dict(),
            created_at=datetime.datetime.utcnow())

    @staticmethod
    def update(*, _id: int, data: Update_User_Model):
        return Update_User_Container(
            **data.dict(),
            updated_at=datetime.datetime.utcnow())
