from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Dict[str, Any] = None,
        order_by: str = None,
    ) -> List[ModelType]:
        query = db.query(self.model)
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
        
        if order_by:
            if order_by.startswith("-"):
                query = query.order_by(text(order_by[1:] + " DESC"))
            else:
                query = query.order_by(text(order_by))
        
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: Any) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def exists(self, db: Session, id: Any) -> bool:
        return db.query(
            db.query(self.model).filter(self.model.id == id).exists()
        ).scalar()

    def count(self, db: Session, filters: Dict[str, Any] = None) -> int:
        query = db.query(self.model)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
        return query.count()

class DatabaseUtils:
    @staticmethod
    async def check_connection(db: Session) -> bool:
        try:
            db.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    @staticmethod
    async def get_db_size(db: Session) -> Dict[str, Any]:
        """Get database size and table sizes"""
        query = text("""
            SELECT
                pg_database.datname,
                pg_size_pretty(pg_database_size(pg_database.datname)) as size
            FROM pg_database
            WHERE pg_database.datname = current_database();
        """)
        result = db.execute(query).first()
        
        table_sizes_query = text("""
            SELECT
                relname as table_name,
                pg_size_pretty(pg_total_relation_size(relid)) as total_size
            FROM pg_catalog.pg_statio_user_tables
            ORDER BY pg_total_relation_size(relid) DESC;
        """)
        table_sizes = db.execute(table_sizes_query).fetchall()
        
        return {
            "database_name": result[0],
            "database_size": result[1],
            "tables": [
                {"name": row[0], "size": row[1]}
                for row in table_sizes
            ]
        }

    @staticmethod
    async def vacuum_analyze(db: Session) -> None:
        """Run VACUUM ANALYZE to optimize database"""
        db.execute(text("VACUUM ANALYZE"))

    @staticmethod
    async def create_database_backup(db: Session, backup_path: str) -> None:
        """Create a database backup"""
        import subprocess
        import os

        db_url = db.get_bind().url
        backup_command = f"pg_dump -h {db_url.host} -p {db_url.port} -U {db_url.username} -F c -b -v -f {backup_path} {db_url.database}"
        
        env = os.environ.copy()
        env["PGPASSWORD"] = db_url.password
        
        subprocess.run(backup_command, shell=True, env=env, check=True)

    @staticmethod
    async def restore_database_backup(db: Session, backup_path: str) -> None:
        """Restore a database backup"""
        import subprocess
        import os

        db_url = db.get_bind().url
        restore_command = f"pg_restore -h {db_url.host} -p {db_url.port} -U {db_url.username} -d {db_url.database} -v {backup_path}"
        
        env = os.environ.copy()
        env["PGPASSWORD"] = db_url.password
        
        subprocess.run(restore_command, shell=True, env=env, check=True)