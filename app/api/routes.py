from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.upload_service import save_uploaded_file, validate_video_size

router = APIRouter()


@router.post("/upload/", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    file_type = file.content_type.split('/')[0]

    if file_type not in ["image", "video"]:
        raise HTTPException(status_code=400, detail="File must be an image or video")

    if file_type == "video" and not validate_video_size(file):
        raise HTTPException(status_code=400, detail="Video size exceeds maximum limit")

    file_path = await save_uploaded_file(file)
    return {"message": "File uploaded successfully", "file_path": file_path}