import os


class Settings:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static/uploads/")
    MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_VIDEO_TYPES = ["video/mp4", "video/mpeg", "video/quicktime"]

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


settings = Settings()