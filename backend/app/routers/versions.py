from fastapi import APIRouter, Depends, HTTPException

from ..auth import get_current_active_user
from ..services.version_service import VersionService

router = APIRouter(prefix="/versions", tags=["versions"])
service = VersionService()


@router.get("/{software_type}", response_model=list[str])
def get_versions(software_type: str, _: str = Depends(get_current_active_user)):
    versions = service.get_versions(software_type)
    if not versions:
        raise HTTPException(status_code=404, detail="No versions available for this software type")
    return versions
