
from fastapi import FastAPI, Form, File ,UploadFile
from api.routers import users, complaints, actions
from api.db.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
import cloudinary
import cloudinary.uploader
import shutil
import uuid
from datetime import date
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    
    allow_credentials=False,
    allow_methods=["*"],      
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(complaints.router)
app.include_router(actions.router)

