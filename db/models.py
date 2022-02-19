from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
# pylint: disable=C0115, R0903

Base = declarative_base()


# таблица с юзерами
class User(Base):
    __tablename__ = 'Users'

    user_id = Column(BigInteger, primary_key=True)
    user_name = Column(String(250))
    full_name = Column(String(250))
    requests_count = Column(Integer, default=0)
