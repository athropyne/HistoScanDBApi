import sqlalchemy.exc
from fastapi import Depends
from starlette import status
from starlette.responses import Response

from core.db import get_connection
from models.response_model import Response_Model
from models.user_models import New_User_Model, Update_User_Model
from preparers.user_preparer import UserPreparer
from repositories.user import UserRepository
from routes.base_router import BaseRouter


class UserRouter(BaseRouter):
    def __init__(self, pathname: str):
        super().__init__(pathname)

        self.router.add_api_route(path="/GetById/{_id}",
                                  endpoint=self.get_by_id,
                                  methods=["GET"])
        self.router.add_api_route(path="/GetList",
                                  endpoint=self.get_list,
                                  methods=["GET"])
        self.router.add_api_route(path="/Add",
                                  endpoint=self.add,
                                  methods=["POST"])
        self.router.add_api_route(path="/Update/{_id}",
                                  endpoint=self.update,
                                  methods=["PUT"])

    async def add(self,
                  response: Response,
                  data: New_User_Model,
                  connection=Depends(get_connection)):
        prepared_for_db = UserPreparer.add(user=data)
        try:
            created_user_id = await UserRepository(connection).add(container=prepared_for_db)
            response.status_code = status.HTTP_201_CREATED
            return Response_Model(msg="пользователь успешно добавлен", data=dict(id=created_user_id))
        except sqlalchemy.exc.IntegrityError:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return Response_Model(msg="пользователь с таким email уже существует")


    async def get_by_id(self,
                        response: Response,
                        _id: int,
                        connection=Depends(get_connection)):
        user_info_cursor = await UserRepository(connection).get_by_id(_id=_id)
        try:
            user_info = user_info_cursor.mappings().one()
            response.status_code = status.HTTP_200_OK
            return Response_Model(data=user_info)
        except sqlalchemy.exc.NoResultFound:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return Response_Model(msg="пользователя с таким ID не существует")

    async def get_list(self,
                       response: Response,
                       skip: int = 0,
                       limit: int = 30,
                       connection=Depends(get_connection)):
        user_list_cursor = await UserRepository(connection).get_list(skip=skip, limit=limit)
        response.status_code = status.HTTP_200_OK
        return Response_Model(data=[i for i in user_list_cursor.mappings()])

    async def update(self,
                     response: Response,
                     _id: int,
                     data: Update_User_Model,
                     connection=Depends(get_connection)):
        prepared_for_db = UserPreparer.update(_id=_id, data=data)
        try:
            updated_row_count = await UserRepository(connection).update(_id=_id, container=prepared_for_db)
            if updated_row_count:
                response.status_code = status.HTTP_200_OK
                return Response_Model(msg="пользователь успешно изменен")
            else:
                return Response_Model(msg="пользователя с таким ID не существует")
        except sqlalchemy.exc.IntegrityError:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return Response_Model(msg="пользователь с таким email уже существует")
