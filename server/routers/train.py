from fastapi import APIRouter, Query, HTTPException, status
import os
import shutil
from server.my_utils import get_abs_path
from pydantic import BaseModel
import wget

router = APIRouter(tags=["train"], prefix="/train")


def use_media_data(role_name: str):
    dirname = get_abs_path("data", "roles", role_name)
    if os.path.exists(get_abs_path("custom_character_voice")):
        shutil.rmtree(get_abs_path("custom_character_voice"))
    shutil.copytree(
        os.path.join(dirname, "short_audios"),
        get_abs_path("custom_character_voice", f"{role_name}_1"),
    )
    if os.path.exists(get_abs_path("raw_audio")):
        shutil.rmtree(get_abs_path("raw_audio"))
    shutil.copytree(os.path.join(dirname, "long_audios"), get_abs_path("raw_audio"))


def clear_raw_media_data():
    shutil.rmtree(get_abs_path("custom_character_voice"))
    shutil.rmtree(get_abs_path("raw_audio"))
    # shutil.rmtree(get_abs_path("video_data"))
    # os.mkdir(get_abs_path("video_data"))


def select_pre_model(model_name: str):
    if model_name not in ["C", "CJ", "CJE"]:
        raise ValueError("model_name only support C, CJ, CJE")
    dirname = get_abs_path("data", "pre_models", model_name)
    model_dir = os.path.join(dirname, "model")
    D_model_path = os.path.join(model_dir, "D_0.pth")
    G_model_path = os.path.join(model_dir, "G_0.pth")
    config_dir = os.path.join(dirname, "config")
    config_path = os.path.join(config_dir, "finetune_speaker.json")

    if not (
        os.path.exists(D_model_path)
        and os.path.exists(G_model_path)
        and os.path.exists(config_path)
    ):
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
        print(f"pre model {model_name} not exist. start downloading")
        os.mkdir(dirname)
        os.mkdir(model_dir)
        os.mkdir(config_dir)
        if model_name == "CJ":
            wget.download(
                "https://huggingface.co/spaces/sayashi/vits-uma-genshin-honkai/resolve/main/model/D_0-p.pth",
                D_model_path,
            )
            wget.download(
                "https://huggingface.co/spaces/sayashi/vits-uma-genshin-honkai/resolve/main/model/G_0-p.pth",
                G_model_path,
            )
            wget.download(
                "https://huggingface.co/spaces/sayashi/vits-uma-genshin-honkai/resolve/main/model/config.json",
                config_path,
            )
        if model_name == "CJE":
            wget.download(
                "https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/pretrained_models/D_trilingual.pth",
                D_model_path,
            )
            wget.download(
                "https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/pretrained_models/G_trilingual.pth",
                G_model_path,
            )
            wget.download(
                "https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/configs/uma_trilingual.json",
                config_path,
            )
        if model_name == "C":
            wget.download(
                "https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/VITS-Chinese/D_0.pth",
                D_model_path,
            )
            wget.download(
                "https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/VITS-Chinese/G_0.pth",
                G_model_path,
            )
            wget.download(
                "https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/VITS-Chinese/config.json",
                config_path,
            )

        print("Download successfully")

    if os.path.exists(get_abs_path("pretrained_models")):
        shutil.rmtree(get_abs_path("pretrained_models"))
    shutil.copytree(model_dir, get_abs_path("pretrained_models"))

    if os.path.exists(get_abs_path("configs", "finetune_speaker.json")):
        os.remove(get_abs_path("configs", "finetune_speaker.json"))
    shutil.copyfile(config_path, get_abs_path("configs", "finetune_speaker.json"))

    print("select pre model successfully")


select_pre_model("CJ")


class TrainOptions(BaseModel):
    pre_model: str = "C"


@router.post("/start")
def start_train():
    return
