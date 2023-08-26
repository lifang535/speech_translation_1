import time
import torch
import threading
import multiprocessing

import soundfile
from espnet2.bin.tts_inference import Text2Speech

from logger import logger_CNtxt2CNaudio, logger_latency

class CNtxt2CNaudio(multiprocessing.Process):
    def __init__(self, id, CNtxt_queue, end_signal):
        super().__init__()
        self.id = id
        self.CNtxt_queue = CNtxt_queue
        self.end_signal = end_signal

        self.device = None
        self.text2speech = None

    def run(self):
        logger_CNtxt2CNaudio.info(f"[CNtxt2CNaudio_{self.id}] start")

        self.end_signal.value += 1

        self.device = torch.device("cuda:1")
        # torch.cuda.set_device(self.device)
        self.text2speech = torch.load("model/text2speech.pth")
        # preload_models()

        while True:
            request = self.CNtxt_queue.get()
            if request.signal == -1:
                self.CNtxt_queue.put(request)
                logger_CNtxt2CNaudio.info(f"[CNtxt2CNaudio_{self.id}] get signal -1")
                self.end_signal.value -= 1
                if self.end_signal.value == 0:
                    ... # TODO
                break
            logger_CNtxt2CNaudio.info(f"[CNtxt2CNaudio_{self.id}]: {request.text_data}")
            self.process_text(request)

    def process_text(self, request):
        text = request.text_data

        with torch.no_grad():
            speech = self.text2speech(text)["wav"]
        soundfile.write(f"output_audios/audio_{request.ids[0]}.wav", speech.numpy(), self.text2speech.fs, "PCM_16")

        end_time = time.time()
        latency = end_time - request.start_time
        logger_latency.info(f"[CNtxt2CNaudio_{self.id}] audio_{request.ids[0]} latency: {latency}")
