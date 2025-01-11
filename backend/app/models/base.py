from datetime import datetime as DateTime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import configure_mappers
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

    @classmethod
    def configure_relationships(cls):
        """Configure all relationships for all models"""
        configure_mappers()

    def to_dict(self):
        """Convert model to dict, handling datetime fields"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, DateTime):
                value = value.isoformat() if value else None
            result[column.name] = value
        return result