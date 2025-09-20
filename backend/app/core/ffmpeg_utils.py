import subprocess
from pathlib import Path
from .config import FFMPEG_PATH

def run_cmd(cmd):
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode())
    return proc.stdout.decode()

def trim_video(input_path: str, output_path: str, start: float, end: float):
    duration = end - start
    cmd = f'{FFMPEG_PATH} -y -ss {start} -i "{input_path}" -t {duration} -c copy "{output_path}"'
    return run_cmd(cmd)

def add_image_watermark(input_path: str, output_path: str, watermark_path: str, x='main_w-overlay_w-10', y='10'):
    cmd = (
        f'{FFMPEG_PATH} -y -i "{input_path}" -i "{watermark_path}" '
        f'-filter_complex "overlay={x}:{y}" -c:a copy "{output_path}"'
    )
    return run_cmd(cmd)

def add_text_overlay(input_path: str, output_path: str, text: str, fontfile: str, x='10', y='10', fontsize=24, start=0, end=None):
    # start/end in seconds: use enable='between(t,start,end)'
    enable = f"enable='between(t,{start},{end})'" if end is not None else ""
    drawtext = f"drawtext=fontfile='{fontfile}':text='{text}':x={x}:y={y}:fontsize={fontsize}:{enable}"
    cmd = f'{FFMPEG_PATH} -y -i "{input_path}" -vf "{drawtext}" -c:a copy "{output_path}"'
    return run_cmd(cmd)

def transcode_quality(input_path: str, output_path: str, resolution: str):
    # resolution like "1920x1080", "1280x720", "854x480"
    cmd = f'{FFMPEG_PATH} -y -i "{input_path}" -vf scale={resolution} -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k "{output_path}"'
    return run_cmd(cmd)
