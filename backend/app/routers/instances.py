from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..auth import get_current_active_user
from ..database import get_db
from ..models import Instance, User
from ..services.instance_service import InstanceLifecycleService

router = APIRouter(prefix="/instances", tags=["instances"])


@router.get("", response_model=list[schemas.InstanceRead])
def list_instances(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return db.query(Instance).order_by(Instance.name).all()


@router.post("/create", response_model=schemas.InstanceRead, status_code=201)
def create_instance(
    payload: schemas.InstanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if db.query(Instance).filter(Instance.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Instance name already exists")
    instance = Instance(**payload.dict(), owner_id=current_user.id)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


@router.patch("/{instance_id}/settings", response_model=schemas.InstanceRead)
def update_instance(
    instance_id: int,
    payload: schemas.InstanceUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    instance = db.query(Instance).get(instance_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(instance, field, value)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


@router.post("/{instance_id}/start", response_model=schemas.InstanceRead)
def start_instance(
    instance_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return InstanceLifecycleService(db).start(instance_id)


@router.post("/{instance_id}/stop", response_model=schemas.InstanceRead)
def stop_instance(
    instance_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return InstanceLifecycleService(db).stop(instance_id)


@router.post("/{instance_id}/restart", response_model=schemas.InstanceRead)
def restart_instance(
    instance_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    service = InstanceLifecycleService(db)
    service.stop(instance_id)
    return service.start(instance_id)


@router.get("/{instance_id}/logs", response_model=list[schemas.InstanceLogRead])
def get_logs(
    instance_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    instance = db.query(Instance).get(instance_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    return instance.logs


@router.delete("/{instance_id}", status_code=204)
def delete_instance(
    instance_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    instance = db.query(Instance).get(instance_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    db.delete(instance)
    db.commit()
    return None
