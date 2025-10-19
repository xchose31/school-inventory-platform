from sqlalchemy import Column, Integer, String, Date, Boolean, SmallInteger, ForeignKey, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app import db

Base = db.Model


class ComPerson(Base):
    __tablename__ = 'com_persons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    patro = Column(String(100))
    gender = Column(Boolean, nullable=False, default=False)
    birthdate = Column(Date)
    snils = Column(String(11), unique=True)
    photo_file = Column(String(32), nullable=False, default='')
    photo_cache = Column(String(32), nullable=False, default='')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(),
                        onupdate=func.current_timestamp())

    # Relationships
    emp_status = relationship("EmpStatus", back_populates="person", uselist=False)
    students = relationship("StuStudent", back_populates="person")
    classteachers = relationship("StuClassteacher", back_populates="person")
    users = relationship("User", back_populates="person")

    def __repr__(self):
        return f'<User {self.surname} {self.name}>'


class EmpStatus(Base):
    __tablename__ = 'emp_status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pers_id = Column(Integer, ForeignKey('com_persons.id', ondelete='CASCADE'), unique=True, nullable=False)
    active = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(),
                        onupdate=func.current_timestamp())

    # Relationships
    person = relationship("ComPerson", back_populates="emp_status")


class StuClass(Base):
    __tablename__ = 'stu_classes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_year = Column(SmallInteger)
    letter = Column(String(4), nullable=False)
    bldg_id = Column(Integer)

    # Relationships
    students = relationship("StuStudent", back_populates="class_")
    classteachers = relationship("StuClassteacher", back_populates="class_")


class StuClassteacher(Base):
    __tablename__ = 'stu_classteachers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pers_id = Column(Integer, ForeignKey('com_persons.id', ondelete='CASCADE'), nullable=False)
    class_id = Column(Integer, ForeignKey('stu_classes.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    person = relationship("ComPerson", back_populates="classteachers")
    class_ = relationship("StuClass", back_populates="classteachers")


class StuStudent(Base):
    __tablename__ = 'stu_students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pers_id = Column(Integer, ForeignKey('com_persons.id', ondelete='CASCADE'), nullable=False)
    class_id = Column(Integer, ForeignKey('stu_classes.id', ondelete='SET NULL'))
    date_to = Column(Date)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(),
                        onupdate=func.current_timestamp())

    # Relationships
    person = relationship("ComPerson", back_populates="students")
    class_ = relationship("StuClass", back_populates="students")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    open_password = Column(String(255))
    password = Column(String(255), nullable=False)
    pers_id = Column(Integer, ForeignKey('com_persons.id', ondelete='SET NULL'))
    is_alias = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(),
                        onupdate=func.current_timestamp())

    # Relationships
    person = relationship("ComPerson", back_populates="users")