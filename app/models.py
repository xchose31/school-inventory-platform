from sqlalchemy import Column, Integer, String, Date, Boolean, SmallInteger, ForeignKey, Text, TIMESTAMP, Enum, event
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app import db
from passlib.hash import bcrypt
from enum import Enum as En

Base = db.Model
from flask_login import UserMixin
from app import login


class ComPerson(Base):
    __tablename__ = 'com_persons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String(100))
    name = Column(String(100))
    patro = Column(String(100))
    gender = Column(Boolean, default=False)
    birthdate = Column(Date)
    snils = Column(String(11), unique=True)
    photo_file = Column(String(32), default='')
    photo_cache = Column(String(32), default='')
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(),
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
    pers_id = Column(Integer, ForeignKey('com_persons.id', ondelete='CASCADE'), unique=True)
    is_teacher = Column(Integer, default=0)
    is_technician = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(),
                        onupdate=func.current_timestamp())

    # Relationships
    person = relationship("ComPerson", back_populates="emp_status")

    @property
    def active(self):
        return bool(self.is_teacher or self.is_technician)



class StuClass(Base):
    __tablename__ = 'stu_classes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_year = Column(SmallInteger)
    letter = Column(String(4))
    bldg_id = Column(Integer)

    # Relationships
    students = relationship("StuStudent", back_populates="class_")
    classteachers = relationship("StuClassteacher", back_populates="class_")


class StuClassteacher(Base):
    __tablename__ = 'stu_classteachers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pers_id = Column(Integer, ForeignKey('com_persons.id', ondelete='CASCADE'))
    class_id = Column(Integer, ForeignKey('stu_classes.id', ondelete='CASCADE'))

    # Relationships
    person = relationship("ComPerson", back_populates="classteachers")
    class_ = relationship("StuClass", back_populates="classteachers")


class StuStudent(Base):
    __tablename__ = 'stu_students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pers_id = Column(Integer, ForeignKey('com_persons.id', ondelete='CASCADE'))
    class_id = Column(Integer, ForeignKey('stu_classes.id', ondelete='SET NULL'))
    date_to = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(),
                        onupdate=func.current_timestamp())

    # Relationships
    person = relationship("ComPerson", back_populates="students")
    class_ = relationship("StuClass", back_populates="students")


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True)
    open_password = Column(String(255))
    password = Column(String(255))
    pers_id = Column(Integer, ForeignKey('com_persons.id', ondelete='SET NULL'))
    is_alias = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(),
                        onupdate=func.current_timestamp())

    def check_password(self, password):
        return bcrypt.verify(password + self.open_password, self.password)

    # Relationships
    person = relationship("ComPerson", back_populates="users")
    repair_requests = relationship('RepairRequest', back_populates='user')


class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    filepath = Column(String)
    file_type = Column(String)
    is_public = Column(Boolean)
    equipment_id = Column(Integer, ForeignKey('equipments.id'), nullable=False)
    equipment = relationship("Equipment", back_populates="materials")


class Equipment(Base):
    __tablename__ = 'equipments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    territory = Column(String(255))
    office = Column(String(255))
    description = Column(String)
    is_deleted = Column(Boolean, default=False)
    photo_path = Column(String)
    categories = Column(String)

    # Relationships
    materials = relationship("Material", back_populates="equipment", cascade="all, delete-orphan")
    repair_requests = relationship('RepairRequest', back_populates='equipment')


class RepairRequest(Base):
    __tablename__ = 'repair_requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(Integer, ForeignKey('equipments.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    comment = Column(String())
    priority = Column(String, default='средний')
    is_completed = Column(Boolean, default=False)
    completion_comment = Column(String)
    creation_date = Column(TIMESTAMP, server_default=func.current_timestamp())
    completion_date = Column(TIMESTAMP)

    equipment = relationship('Equipment', back_populates='repair_requests')
    user = relationship('User', back_populates='repair_requests')


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
