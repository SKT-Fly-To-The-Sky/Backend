from models import Picture
from sqlalchemy.orm import Session


def get_picture_list(db: Session):
    picture_list = db.query(Picture)\
        .order_by(Picture.date.desc())\
        .all()
    return picture_list


def add_picture(db: Session, member_id, date, image_name):
    try:
        p = Picture(member_id=member_id, date=date, image_name=image_name)
        db.add(p)
        db.commit()
        return True
    except Exception as e:
        return e
