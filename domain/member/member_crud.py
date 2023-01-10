from models import Member
from sqlalchemy.orm import Session


def get_member_list(db: Session):
    member_list = db.query(Member)\
        .order_by(Member.account.desc())\
        .all()
    return member_list
