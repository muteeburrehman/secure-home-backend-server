import os
from fastapi import UploadFile
from app.core.config import settings
import aiofiles



async def save_uploaded_file(file: UploadFile) -> str:
    file_location = os.path.join(settings.UPLOAD_FOLDER, file.filename)

    async with aiofiles.open(file_location, 'wb') as buffer:
        content = await file.read()
        await buffer.write(content)

    return file_location


def validate_video_size(file: UploadFile) -> bool:
    return file.size <= settings.MAX_VIDEO_SIZE
