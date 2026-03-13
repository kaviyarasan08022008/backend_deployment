from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from api.dependencies import connect_to_db
from api.models.complaints import Complaints
from api.models.actions import Actions
from api.schemas.complaints import ComplaintResponse
from datetime import date
from typing import Optional
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)

# Configure Cloudinary
cloudinary.config( 
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.getenv('CLOUDINARY_API_KEY'), 
  api_secret = os.getenv('CLOUDINARY_API_SECRET') 
)

@router.post("", status_code=201, response_model=ComplaintResponse)
def create_complaint(
    people_id: int = Form(...),
    category: str = Form(...),
    officer_name: str = Form(...),
    designation: str = Form(...),
    village: str = Form(...),
    district: str = Form(...),
    incident_date: date = Form(...),
    description: str = Form(...),
    is_anonymous: bool = Form(False),
    contact_name: Optional[str] = Form(None),
    contact_phone: Optional[str] = Form(None),
    contact_email: Optional[str] = Form(None),
    collector_id: Optional[int] = Form(None),
    evidence: UploadFile = File(None),
    db: Session = Depends(connect_to_db)
):
    image_url = None
    if evidence:
        try:
            # Upload file to Cloudinary
            upload_result = cloudinary.uploader.upload(evidence.file)
            image_url = upload_result.get("secure_url")
        except Exception as e:
            # Raise exception so user knows why it failed
            raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

    new_complaint = Complaints(
        people_id=people_id,
        category=category,
        officer_name=officer_name,
        designation=designation,
        village=village,
        district=district,
        incident_date=incident_date,
        description=description,
        is_anonymous=is_anonymous,
        contact_name=contact_name,
        contact_phone=contact_phone,
        contact_email=contact_email,
        collector_id=collector_id,
        image_url=image_url
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return new_complaint


@router.get("", response_model=list[ComplaintResponse])
def get_all_complaints(db: Session = Depends(connect_to_db)):
    return db.query(Complaints).all()


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: int, db: Session = Depends(connect_to_db)):
    complaint = db.query(Complaints).filter(Complaints.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


@router.put("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(
    complaint_id: int,
    category: str = Form(...),
    officer_name: str = Form(...),
    designation: str = Form(...),
    village: str = Form(...),
    district: str = Form(...),
    incident_date: date = Form(...),
    description: str = Form(...),
    is_anonymous: bool = Form(False),
    contact_name: Optional[str] = Form(None),  
    contact_phone: Optional[str] = Form(None),
    contact_email: Optional[str] = Form(None),
    collector_id: Optional[int] = Form(None),
    db: Session = Depends(connect_to_db)
):
    complaint = db.query(Complaints).filter(Complaints.id == complaint_id).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    complaint.category = category
    complaint.officer_name = officer_name
    complaint.designation = designation
    complaint.village = village
    complaint.district = district
    complaint.incident_date = incident_date
    complaint.description = description
    complaint.is_anonymous = is_anonymous
    complaint.contact_name = contact_name
    complaint.contact_phone = contact_phone
    complaint.contact_email = contact_email
    complaint.collector_id = collector_id

    db.commit()
    db.refresh(complaint)

    return complaint


@router.delete("/{complaint_id}")
def delete_complaint(complaint_id: int, db: Session = Depends(connect_to_db)):
    complaint = db.query(Complaints).filter(Complaints.id == complaint_id).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Delete associated actions first to avoid FK constraint errors
    db.query(Actions).filter(Actions.complaint_id == complaint_id).delete()

    db.delete(complaint)
    db.commit()

    return {"message": "Complaint deleted successfully"}

@router.put("/{complaint_id}/status", response_model=ComplaintResponse)
def update_complaint_status(
    complaint_id: int,
    status: str = Form(...),
    db: Session = Depends(connect_to_db)
):
    complaint = db.query(Complaints).filter(Complaints.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    complaint.status = status
    db.commit()
    db.refresh(complaint)
    return complaint

# @router.get("/user/{people_id}", response_model=list[ComplaintResponse])
# def get_user_complaints(people_id: int, db: Session = Depends(connect_to_db)):
#     return db.query(Complaints).filter(Complaints.people_id == people_id).all()
