from fastapi import APIRouter, Query, HTTPException, status, Body
import os
import shutil
from server.my_utils import get_abs_path, rm_abs_dir, rm_abs_file
from pydantic import BaseModel
import wget

router = APIRouter(tags=["train"], prefix="/train")


def clear_raw_media_data():
    rm_abs_dir("custom_character_voice")
    rm_abs_dir("raw_audio")
    # shutil.rmtree(get_abs_path("video_data"))
    # os.mkdir(get_abs_path("video_data"))


def clear_resolced_media_data():
    rm_abs_dir("denoised_audio")
    os.mkdir(get_abs_path("denoised_audio"))
    rm_abs_dir("segmented_character_voice")
    os.mkdir(get_abs_path("segmented_character_voice"))
    rm_abs_dir("denoised_audio")
    os.mkdir(get_abs_path("denoised_audio"))
    rm_abs_dir("separated")
    os.mkdir(get_abs_path("separated"))
    rm_abs_file("long_character_anno.txt")
    rm_abs_file("short_character_anno.txt")


def use_media_data(role_name: str):
    clear_raw_media_data()
    dirname = get_abs_path("data", "roles", role_name)
    if not os.path.exists(os.path.join(dirname, "short_audios")):
        os.mkdir(os.path.join(dirname, "short_audios"))
    shutil.copytree(
        os.path.join(dirname, "short_audios"),
        get_abs_path("custom_character_voice", f"{role_name}_1"),
    )
    if not os.path.exists(os.path.join(dirname, "long_audios")):
        os.mkdir(os.path.join(dirname, "long_audios"))
    shutil.copytree(os.path.join(dirname, "long_audios"), get_abs_path("raw_audio"))


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


def process_media_data(model_name: str, whisper_size: str):
    clear_resolced_media_data()
    os.system(f"python {get_abs_path('scripts','video2audio.py')}")
    os.system(f"python {get_abs_path('scripts','denoise_audio.py')}")
    os.system(
        f"python {get_abs_path('scripts', 'long_audio_transcribe.py')} --languages {model_name} --whisper_size {whisper_size}"
    )
    os.system(
        f"python {get_abs_path('scripts', 'short_audio_transcribe.py')} --languages {model_name} --whisper_size {whisper_size}"
    )
    os.system(f"python {get_abs_path('scripts', 'resample.py')}")


@router.post("/start")
async def start_train(
    role_name: str,
    pre_model: str = Query(description="C, CJ, CJE"),
    whisper_size: str = Query(description="small, medium, large"),
    is_cont: bool = Query(description="is Continue"),
):
    if not os.path.exists(get_abs_path("data", "roles", role_name)):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "target role not exist")
    use_media_data(role_name)
    select_pre_model(pre_model)
    process_media_data(pre_model, whisper_size)

    return "success"
