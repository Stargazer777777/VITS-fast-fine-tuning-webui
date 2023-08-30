import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../video_text/video.txt")


def generate_infos():
    infos = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.replace("\n", "").replace(" ", "")
        if line == "":
            continue
        speaker, link = line.split("|")
        filename = speaker + "_" + str(random.randint(0, 1000000))
        infos.append({"link": link, "filename": filename})
    return infos


def download_video(info):
    link = info["link"]
    filename = info["filename"]
    os.system(f"youtube-dl -f 0 {link} -o ./video_data/{filename}.mp4 --no-check-certificate")


if __name__ == "__main__":
    infos = generate_infos()
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(download_video, infos)