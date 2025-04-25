from sqlalchemy import Column, Integer, String, ForeignKey, Text, Time, TIMESTAMP
from sqlalchemy.orm import relationship
from db import Base, engine

class Role(Base):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'zachet'}
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'zachet'}
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey('zachet.roles.id'))

    role = relationship("Role", back_populates="users")
    oprosnik = relationship("Oprosnik", back_populates="user")

class Oprosnik(Base):
    __tablename__ = "opros"
    __table_args__ = {'schema': 'zachet'}
    id = Column(Integer, primary_key=True)
    numberoprosnik = Column(Integer, nullable=False, unique=True)
    correctanswer = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('zachet.user.id'))
    
    user = relationship("User", back_populates="oprosnik")
    

def create_tables():
    Base.metadata.create_all(engine)
    print("Таблицы успешно созданы через SQLAlchemy.")
    
if __name__ == "__main__":
    create_tables()