from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.database.db import create_tables
from app.api.server_info_routes import router as server_info_router
from app.api.home_routes import router as home_router
from app.api.device_routes import router as device_router
from app.api.schedule_routes import router as schedule_router




# Initialize the FastAPI app
app = FastAPI()

app.include_router(router)
app.include_router(auth_router, prefix="/auth")
app.include_router(server_info_router, prefix="/api")
router.include_router(home_router, prefix="/api")
router.include_router(device_router, prefix="/api")
router.include_router(schedule_router, prefix="/api")

# Allow CORS for your Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Image Upload Server"}
# Create database tables
create_tables()
# Entry point for running the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
