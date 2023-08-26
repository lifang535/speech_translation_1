import os
import time
import torch
import librosa

import threading
import multiprocessing

from request import Request
from ESaudio2ENtxt import ESaudio2ENtxt
from ENtxt2CNtxt import ENtxt2CNtxt
from CNtxt2CNaudio import CNtxt2CNaudio

if __name__ == "__main__":
    if os.path.exists("output_audios"):
        os.system("rm -r output_audios")
    os.mkdir("output_audios")

    multiprocessing.set_start_method("spawn")

    managers = []
    end_signals = []
    for i in range(3):
        managers.append(multiprocessing.Manager())
        end_signals.append(managers[i].Value("i", 0))
        
    ESaudio_queue = managers[0].Queue()
    ENtxt_queue = managers[1].Queue()
    CNtxt_queue = managers[2].Queue()

    ESaudio2ENtxts = []
    ENtxt2CNtxts = []
    CNtxt2CNaudios = []
    for i in range(3):
        ESaudio2ENtxts.append(ESaudio2ENtxt(i+1, ESaudio_queue, ENtxt_queue, end_signals[0]))
        ENtxt2CNtxts.append(ENtxt2CNtxt(i+1, ENtxt_queue, CNtxt_queue, end_signals[1]))
        CNtxt2CNaudios.append(CNtxt2CNaudio(i+1, CNtxt_queue, end_signals[2]))

    num_models = [1, 1, 1]

    for i in range(num_models[0]):
        ESaudio2ENtxts[i].start()
    for i in range(num_models[1]):
        ENtxt2CNtxts[i].start()
    for i in range(num_models[2]):
        CNtxt2CNaudios[i].start()

    # put requests from audio file into queue
    audio_dir = "input_audios"
    audio_files = os.listdir(audio_dir)
    audio_files.sort(key=lambda x: int(x.split(".")[0].split("_")[-1]))
    time.sleep(10) # wait for model initialization
    for audio_file in audio_files:
        time.sleep(10)
        audio, sr = librosa.load(os.path.join(audio_dir, audio_file), sr=16000)
        audio_id = int(audio_file.split(".")[0].split("_")[-1])
        request = Request(ids=[audio_id],
                            sub_requests=[], # TODO: no sub_requests
                            audio_data=audio,
                            text_data=None,
                            signal=None,
                            start_time=time.time())
        ESaudio_queue.put(request)
        
    # put end signal into queue
    request = Request(ids=[],
                        sub_requests=[],
                        audio_data=None,
                        text_data=None,
                        signal=-1,
                        start_time=time.time())
    ESaudio_queue.put(request)
    
    for i in range(num_models[0]):
        ESaudio2ENtxts[i].join()
    for i in range(num_models[1]):
        ENtxt2CNtxts[i].join()
    for i in range(num_models[2]):
        CNtxt2CNaudios[i].join()
