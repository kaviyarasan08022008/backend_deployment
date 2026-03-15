from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.dependencies import connect_to_db, get_password_hash, verify_password
from api.schemas.users import UserCreate, UserBase, UserLogin
from api.models.users import User
from api.models.actions import Actions


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("")
def create_user(user: UserBase, db: Session = Depends(connect_to_db)):
    try:
        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            user_name=user.user_name,
            password=get_password_hash(user.password),
            state=user.state,
            district=user.district,
            village_town=user.village_town,
            user_role=user.user_role,
            phone_number=user.phone_number
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"id": new_user.id, "user_name": new_user.user_name, "first_name": new_user.first_name}
    except Exception as e:
        db.rollback()
        # Check for integrity error (duplicate username)
        if "UNIQUE constraint failed" in str(e) or "IntegrityError" in str(e):
             raise HTTPException(status_code=400, detail="Username already exists")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(connect_to_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}")
def update_user(
    user_id: int,
    updated_data: UserCreate,
    db: Session = Depends(connect_to_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated_data.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(connect_to_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(Actions).filter(Actions.collector_id == user_id).delete()

    db.delete(user)
    db.commit()

    return {"detail": "User deleted successfully"}

@router.post("/login")
def login(user_details: UserLogin, db: Session = Depends(connect_to_db)):
    user = db.query(User).filter(
        User.user_name == user_details.user_name,
        User.user_role == user_details.user_role
    ).first()

    if not user or not verify_password(user_details.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"id": user.id, "user_name": user.user_name, "user_role": user.user_role}