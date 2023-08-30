from fastapi import APIRouter, Query, HTTPException, status
import os
import shutil
from server.my_utils import get_abs_path

router = APIRouter(tags=["role"], prefix="/role")


@router.post("/create", status_code=201)
def create_role(role_name: str = Query(max_length=20)):
    target_dirname = get_abs_path("data", "roles", role_name)
    if not os.path.exists(target_dirname):
        os.mkdir(target_dirname)
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="already exist"
        )
    return {"msg": "create successfully"}


@router.get("/", status_code=200)
def get_roles():
    target_dirname = get_abs_path("data", "roles")
    roles = os.listdir(target_dirname)
    return {"msg": "success", "data": roles}


@router.delete("/delete", status_code=status.HTTP_200_OK)
def del_role(role_name: str):
    target_dirname = get_abs_path("data", "roles", role_name)
    if os.path.exists(target_dirname):
        shutil.rmtree(target_dirname)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="target role not exist"
        )
    return {"msg": "delete successfully"}
