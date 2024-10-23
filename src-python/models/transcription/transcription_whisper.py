from os import path as os_path, makedirs as os_makedirs
from requests import get as requests_get
from typing import Callable
import torch
import huggingface_hub
from faster_whisper import WhisperModel
import logging
from utils import printLog

logger = logging.getLogger('faster_whisper')
logger.setLevel(logging.CRITICAL)

_MODELS = {
    "tiny": "Systran/faster-whisper-tiny",
    "base": "Systran/faster-whisper-base",
    "small": "Systran/faster-whisper-small",
    "medium": "Systran/faster-whisper-medium",
    "large-v1": "Systran/faster-whisper-large-v1",
    "large-v2": "Systran/faster-whisper-large-v2",
    "large-v3": "Systran/faster-whisper-large-v3",
}

_FILENAMES = [
    "config.json",
    "preprocessor_config.json",
    "model.bin",
    "tokenizer.json",
    "vocabulary.txt",
    "vocabulary.json",
]

def downloadFile(url, path, func=None):
    try:
        res = requests_get(url, stream=True)
        res.raise_for_status()
        file_size = int(res.headers.get('content-length', 0))
        total_chunk = 0
        with open(os_path.join(path), 'wb') as file:
            for chunk in res.iter_content(chunk_size=1024*2000):
                file.write(chunk)
                if isinstance(func, Callable):
                    total_chunk += len(chunk)
                    func(total_chunk/file_size)
                printLog(f"Downloading Whisper Model: {total_chunk/file_size:.0%}")

    except Exception as e:
        printLog("warning:downloadFile()", e)

def checkWhisperWeight(root, weight_type):
    path = os_path.join(root, "weights", "whisper", weight_type)
    result = False
    try:
        WhisperModel(
            path,
            device="cpu",
            device_index=0,
            compute_type="int8",
            cpu_threads=4,
            num_workers=1,
            local_files_only=True,
        )
        result = True
    except Exception:
        pass
    return result

def downloadWhisperWeight(root, weight_type, callbackFunc):
    path = os_path.join(root, "weights", "whisper", weight_type)
    os_makedirs(path, exist_ok=True)
    if checkWhisperWeight(root, weight_type) is True:
        callbackFunc(1)
        return

    for filename in _FILENAMES:
        file_path = os_path.join(path, filename)
        url = huggingface_hub.hf_hub_url(_MODELS[weight_type], filename)
        downloadFile(url, file_path, func=callbackFunc)

def getWhisperModel(root, weight_type, device="cpu", device_index=0):
    path = os_path.join(root, "weights", "whisper", weight_type)
    compute_type = "int8" if device == "cpu" else "float16"
    return WhisperModel(
        path,
        device=device,
        device_index=device_index,
        compute_type=compute_type,
        cpu_threads=4,
        num_workers=1,
        local_files_only=True,
    )

if __name__ == "__main__":
    def callback(value):
        print(value)
        pass

    downloadWhisperWeight("./", "tiny", callback)
    downloadWhisperWeight("./", "base", callback)
    downloadWhisperWeight("./", "small", callback)
    downloadWhisperWeight("./", "medium", callback)
    downloadWhisperWeight("./", "large-v1", callback)
    downloadWhisperWeight("./", "large-v2", callback)
    downloadWhisperWeight("./", "large-v3", callback)