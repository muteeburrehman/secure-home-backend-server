import os
from fastapi import UploadFile
from app.core.config import settings
import shutil

async def save_uploaded_file(file: UploadFile) -> str:
    file_location = os.path.join(settings.UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_location
