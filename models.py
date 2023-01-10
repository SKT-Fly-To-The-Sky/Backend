from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True)
    account = Column(String(50), nullable=False)


class Picture(Base):
    __tablename__ = "picture"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    image_name = Column(String(100), nullable=False)
    member = relationship("Member", backref="pictures")


if __name__ == "__main__":
    from database import SessionLocal
    db = SessionLocal()

    # m = Member(account="jung-su-lee")
    # db.add(m)
    # db.commit()

    '''
    ### C
    m = Member(account="fly2sky")
    db.add(m)
    db.commit()
    m = Member(account="jung-su-lee")
    db.add(m)
    db.commit()

    ### R
    x = db.query(User).all()
    db.query(User).filter(User.id == 1).all()
    db.query(User).get(1)
    db.query(User).filter(User.account.like('%fly%')).all()
    
    ### U
    u = db.query(User).get(1)
    u.account = 'jung-su-gi'
    db.commit()
    
    ### D
    u = db.query(User).get(1)
    db.delete(u)
    db.commit()
    
    ### C with ref
    m = db.query(Member).get(1)
    p = Picture(member=m, date=datetime.now())
    db.add(p)
    db.commit()
    print(m.pictures[0].member.account)
    '''


'''
db 초기 세팅: alembic init migrations
revision 파일 생성: alembic revision --autogenerate \
revision db에 적용: alembic upgrade head
'''
