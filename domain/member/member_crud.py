from db_models import Member
from sqlalchemy.orm import Session


def get_member_list(db: Session):
    member_list = db.query(Member) \
        .order_by(Member.account.desc()) \
        .all()
    return member_list


def add_member(db: Session):
    try:
        m = Member(account="jeong-su-lee")
        db.add(m)
        db.commit()
        return True
    except Exception as e:
        return e
