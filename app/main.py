from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.database.db import create_tables

# Initialize the FastAPI app
app = FastAPI()

app.include_router(router)
app.include_router(auth_router, prefix="/auth")
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
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
