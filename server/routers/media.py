from fastapi import APIRouter, Query, HTTPException, status, FastAPI, File, UploadFile
from typing import List
import os
import shutil
from server.my_utils import get_abs_path, rm_abs_dir, rm_abs_file, mkdir_ifnot_exist

router = APIRouter(tags=["media"], prefix="/media")


async def write_uploadfile(
    dirname: str, role_name: str, upload_files: List[UploadFile]
):
    mkdir_ifnot_exist(dirname)
    for upload_file in upload_files:
        dir_len = len(os.listdir(dirname))
        filename = f"{role_name}_{dir_len+1}-{upload_file.filename}"
        targetFile = open(os.path.join(dirname, filename), "wb")
        targetFile.write(await upload_file.read())
        targetFile.close()


@router.post("/short_audio/upload")
async def upload_short_audios(
    role_name: str, files: List[UploadFile] = File(media_type="audio")
):
    target_dirname = get_abs_path("data", "roles", role_name)
    if os.path.exists(target_dirname):
        target_dirname = os.path.join(target_dirname, "short_audios")
        await write_uploadfile(target_dirname, role_name, files)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="target role not exist"
        )
    return {"msg": "upload successfully"}


@router.get("/short_audios")
async def get_short_audios(role_name: str):
    target_dirname = get_abs_path("data", "roles", role_name)
    if not os.path.exists(target_dirname):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="target role not exist"
        )
    if not os.path.exists(os.path.join("short_audios")):
        return []
    filenames = os.listdir(target_dirname)
    res = []
    for filename in filenames:
        res.append(
            {
                "name": filename,
                "path": f"/data/roles/{role_name}/short_audios/{filename}",
            }
        )
    return {"data": res}


@router.delete("/short_audios/delete")
async def delete_short_audio(role_name: str, filename: str):
    target_file = get_abs_path("data", "roles", role_name, "short_audios", filename)
    if not os.path.exists(target_file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="target file not exist"
        )
    os.remove(target_file)
    return {"msg": "delete successfully"}


@router.post("/long_audio/upload")
async def upload_long_audios(
    role_name: str, files: List[UploadFile] = File(media_type="audio/wav")
):
    target_dirname = get_abs_path("data", "roles", role_name)
    if os.path.exists(target_dirname):
        target_dirname = os.path.join(target_dirname, "long_audios")
        await write_uploadfile(target_dirname, role_name, files)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="target role not exist"
        )
    return {"msg": "upload successfully"}


@router.get("/long_audios")
async def get_long_audios(role_name: str):
    target_dirname = get_abs_path("data", "roles", role_name)
    if not os.path.exists(target_dirname):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="target role not exist"
        )
    if not os.path.exists(os.path.join("long_audios")):
        return []
    filenames = os.listdir(target_dirname)
    res = []
    for filename in filenames:
        res.append(
            {
                "name": filename,
                "path": f"/data/roles/{role_name}/long_audios/{filename}",
            }
        )
    return {"data": res}


@router.delete("/long_audios/delete")
async def delete_long_audio(role_name: str, filename: str):
    target_file = get_abs_path("data", "roles", role_name, "long_audios", filename)
    if not os.path.exists(target_file):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="target file not exist"
        )
    os.remove(target_file)
    return {"msg": "delete successfully"}
