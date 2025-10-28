from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="admin")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    instances = relationship("Instance", back_populates="owner")


class Instance(Base):
    __tablename__ = "instances"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    instance_type = Column(String(20), nullable=False)
    software = Column(String(50), nullable=False)
    version = Column(String(20), nullable=False)
    status = Column(String(20), default="stopped")
    autostart = Column(Boolean, default=False)
    autorestart_on_crash = Column(Boolean, default=True)
    memory_limit = Column(Integer, nullable=True)
    java_args = Column(String(255), nullable=True)
    max_players = Column(Integer, nullable=True)
    port = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", back_populates="instances")
    logs = relationship("InstanceLog", back_populates="instance", cascade="all, delete-orphan")


class InstanceLog(Base):
    __tablename__ = "instance_logs"

    id = Column(Integer, primary_key=True, index=True)
    instance_id = Column(Integer, ForeignKey("instances.id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    instance = relationship("Instance", back_populates="logs")
