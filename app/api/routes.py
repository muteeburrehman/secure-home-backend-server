from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.upload_service import save_uploaded_file

router = APIRouter()


@router.post("/upload/", status_code=201)
async def upload_image(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Save the file
    file_path = await save_uploaded_file(file)
    return {"message": "File uploaded successfully", "file_path": file_path}
