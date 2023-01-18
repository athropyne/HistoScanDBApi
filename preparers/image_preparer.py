import datetime

from pydantic import FilePath

from models.image_models import New_Image_Container


class ImagePreparer:
    @staticmethod
    def add(*,
            filename: str,
            description: str | None,
            image_url: str,
            creator_id: int,
            ) -> New_Image_Container:
        return New_Image_Container(
            filename=filename,
            description=description,
            image_url=image_url,
            creator_id=creator_id,
            created_at=datetime.datetime.utcnow())
