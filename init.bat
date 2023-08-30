set mirror=https://pypi.tuna.tsinghua.edu.cn/simple

call venv\scripts\activate.bat

python -m pip install --upgrade pip -i %mirror%

python -m pip install --upgrade wget -i %mirror%
python -m pip install --upgrade fast_unzip -i %mirror%
python -m pip install --upgrade regex -i %mirror%
python -m pip install soundfile -i %mirror%
python -m pip install gradio -i %mirror%
python -m pip install imageio -i %mirror%
python -m pip install --upgrade youtube-dl -i %mirror%
python -m pip install moviepy -i %mirror%

python -m pip install --no-build-isolation -r requirements.txt -i %mirror%
python -m pip install --upgrade --force-reinstall numba -i %mirror%

python -m pip install --upgrade pyzmq -i %mirror%
python -m pip install pydantic==1.10.4 -i %mirror%
python -m pip install ruamel.yaml -i %mirror%

@REM build monotonic align
cd monotonic_align\
mkdir monotonic_align
python setup.py build_ext --inplace
cd ..
mkdir pretrained_models
@REM download data for fine-tuning
IF NOT EXIST sampled_audio4ft (
  echo "Downloading sampled_audio4ft_v2"
    python -m wget https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/sampled_audio4ft_v2.zip
    python -m fast_unzip sampled_audio4ft_v2.zip
)
@REM create necessary directories
mkdir video_data
mkdir raw_audio
mkdir denoised_audio
mkdir custom_character_voice
mkdir segmented_character_voice