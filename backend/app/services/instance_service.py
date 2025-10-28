from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Instance, InstanceLog


class InstanceLifecycleService:
    """Naive lifecycle controller that mimics process management for demo purposes."""

    def __init__(self, db: Session):
        self.db = db

    def _get_instance(self, instance_id: int) -> Instance:
        instance = self.db.query(Instance).get(instance_id)
        if not instance:
            raise HTTPException(status_code=404, detail="Instance not found")
        return instance

    def _append_log(self, instance: Instance, message: str) -> None:
        log = InstanceLog(instance_id=instance.id, message=message, created_at=datetime.utcnow())
        self.db.add(log)
        self.db.commit()

    def start(self, instance_id: int) -> Instance:
        instance = self._get_instance(instance_id)
        if instance.status == "running":
            self._append_log(instance, "Instance already running")
            return instance
        instance.status = "running"
        instance.updated_at = datetime.utcnow()
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        self._append_log(instance, "Instance started")
        return instance

    def stop(self, instance_id: int) -> Instance:
        instance = self._get_instance(instance_id)
        if instance.status == "stopped":
            self._append_log(instance, "Instance already stopped")
            return instance
        instance.status = "stopped"
        instance.updated_at = datetime.utcnow()
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        self._append_log(instance, "Instance stopped")
        return instance
