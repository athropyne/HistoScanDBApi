import os
from uuid import uuid4

import slideio
import sqlalchemy.exc
from fastapi import UploadFile, File, Depends, Response
from matplotlib import pyplot as plt
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status
from starlette.responses import FileResponse

from core import config
from core.db import get_connection
from models.response_model import Response_Model
from preparers.image_preparer import ImagePreparer
from repositories.image import ImageRepository
from routes.base_router import BaseRouter
from utils.format_filename import format_filename
from utils.image_saver import ImageSaver


class ImageRouter(BaseRouter):
    def __init__(self, pathname: str):
        super().__init__(pathname)

        self.router.add_api_route(path="/Add",
                                  endpoint=self.add,
                                  methods=["POST"])

        self.router.add_api_route(path="/GetById",
                                  endpoint=self.get_by_id,
                                  methods=["GET"])

        self.router.add_api_route(path="/GetList",
                                  endpoint=self.get_list,
                                  methods=["GET"])

    """ наверное уже не понадобится"""

    # @staticmethod
    # def svs_convert(path):
    #     # image_path = os.path.join('input', 'md519.svs')
    #     slide = slideio.open_slide(path, "SVS")
    #     raw_string = slide.raw_metadata
    #     print(raw_string)
    #     print()
    #     print(raw_string.split("|"))
    #
    #     scene = slide.get_scene(0)
    #
    #     print()
    #     print(scene.name, scene.rect, scene.num_channels, scene.resolution)
    #
    #     image = scene.read_block(size=(500, 0))
    #     print(image)
    #     plt.imshow(image)
    #     # plt.savefig(os.path.join('/images', 'sample-el-1-bg.jpg'))
    # """из сгенерировнного имени svs файла получаю имя"""
    # folder_name = os.path.split(os.path.splitext(path)[0])[-1]
    #
    # """перехожу в /images"""
    # os.chdir(config.UPLOADED_IMAGES_PATH)
    #
    # """создаю папку с уникальным именем, совпадающим с именем svs файла"""
    # os.mkdir(folder_name)
    #
    # """создаю уникальное имя файла"""
    # filename = str(uuid4())+'.jpg'
    #
    # """кладу этот файл в сгенерированную папку"""
    # plt.savefig(os.path.join(folder_name, filename))

    async def add(self,
                  response: Response,
                  name: str,
                  description: str | None = None,
                  file: UploadFile = File(...),
                  connection: AsyncConnection = Depends(get_connection)):
        """генерирую уникальное имя файла"""
        filename = format_filename(file)  # name for server path

        """ генерирую путь для файла """
        url = f"{config.UPLOADED_IMAGES_PATH}{filename}"

        """сохраняю файл по пути"""
        await ImageSaver.save(url=url, file=file)

        # ImageRouter.svs_convert(path=url)

        #####################
        """
        где то тут нужно взять id  авторизованного пользователя
        """
        #####################
        user_id = 1  # пока так
        prepared_for_db = ImagePreparer.add(filename=name,  # name for db
                                            description=description,
                                            creator_id=user_id,
                                            image_url=url)
        response.status_code = status.HTTP_201_CREATED
        inserted_file_id = await ImageRepository(connection).add(container=prepared_for_db)
        return Response_Model(msg="файл успешно загружен",
                              data=dict(id=inserted_file_id))

    async def get_by_id(self,
                        response: Response,
                        file_id: int,
                        connection: AsyncConnection = Depends(get_connection)
                        ):
        file_info_cursor = await ImageRepository(connection).get_by_id(_id=file_id)
        try:
            image_info = file_info_cursor.mappings().one()
            response.status_code = status.HTTP_200_OK
            return FileResponse(image_info["image_url"])
        except sqlalchemy.exc.NoResultFound as e:
            response.status_code = status.HTTP_404_NOT_FOUND
            return Response_Model(msg="файл с таким ID не найден")

    async def get_list(self,
                       response: Response,
                       skip: int = 0,
                       limit: int = 30,
                       connection=Depends(get_connection)):
        image_list_cursor = await ImageRepository(connection).get_list(skip=skip, limit=limit)
        return Response_Model(data=[i for i in image_list_cursor.mappings()])
