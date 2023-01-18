from fastapi import UploadFile

from core.config import UPLOADED_IMAGES_PATH


class ImageSaver:
    @staticmethod
    async def save(*, url: str, file: UploadFile):
        with open(url, "wb") as uploaded_file:
            file_content = await file.read()
            uploaded_file.write(file_content)
            uploaded_file.close()
