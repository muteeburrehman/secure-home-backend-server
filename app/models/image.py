from pydantic import BaseModel

class ImageResponse(BaseModel):
    message: str
    file_path: str
