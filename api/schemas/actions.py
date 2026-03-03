from pydantic import BaseModel

class ActionBase(BaseModel):
    status: str          # pending / in_progress / resolved
    remarks: str

class ActionCreate(ActionBase):
    complaint_id: int
    collector_id: int

class ActionResponse(ActionBase):
    id: int
    complaint_id: int
    collector_id: int