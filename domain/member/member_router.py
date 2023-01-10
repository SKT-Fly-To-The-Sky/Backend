from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.member import member_schema, member_crud

router = APIRouter(
    prefix="/api/member",
)


@router.get("/list", response_model=list[member_schema.Member])
def member_list(db: Session = Depends(get_db)):
    _member_list = member_crud.get_member_list(db)
    return _member_list
