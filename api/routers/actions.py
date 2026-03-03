from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import connect_to_db
from models.actions import Actions
from schemas.actions import ActionCreate, ActionResponse

router = APIRouter(
    prefix="/actions",
    tags=["Actions"]
)
@router.get("/")
def get_all_actions(dbs: Session = Depends(connect_to_db)):
    return dbs.query(Actions).all()


@router.post("/", response_model=ActionResponse)
def create_action(
    action: ActionCreate,
    db: Session = Depends(connect_to_db)
):
    new_action = Actions(**action.dict())
    db.add(new_action)
    db.commit()
    db.refresh(new_action)
    return new_action


@router.get("/complaint/{complaint_id}", response_model=list[ActionResponse])
def get_actions_by_complaint(
    complaint_id: int,
    db: Session = Depends(connect_to_db)
):
    return db.query(Actions).filter(
        Actions.complaint_id == complaint_id
    ).all()
