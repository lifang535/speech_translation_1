import torch
import threading
import multiprocessing

from transformers import WhisperProcessor, WhisperForConditionalGeneration

from logger import logger_ESaudio2ENtxt

class ESaudio2ENtxt(multiprocessing.Process):
    def __init__(self, id, ESaudio_queue, ENtxt_queue, end_signal):
        super().__init__()
        self.id = id
        self.ESaudio_queue = ESaudio_queue
        self.ENtxt_queue = ENtxt_queue
        self.end_signal = end_signal

        self.device = None
        self.processor = None
        self.model = None

    def run(self):
        logger_ESaudio2ENtxt.info(f"[ESaudio2ENtxt_{self.id}] start")

        self.end_signal.value += 1

        self.device = torch.device("cuda:0")
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-large")
        self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large").to(self.device)

        while True:
            request = self.ESaudio_queue.get()
            if request.signal == -1:
                self.ESaudio_queue.put(request)
                logger_ESaudio2ENtxt.info(f"[ESaudio2ENtxt_{self.id}] get signal -1")
                self.end_signal.value -= 1
                if self.end_signal.value == 0:
                    self.ENtxt_queue.put(request)
                break
            logger_ESaudio2ENtxt.info(f"[ESaudio2ENtxt_{self.id}]: {request.ids[0]}")
            self.process_audio(request)

    def process_audio(self, request):
        audio = request.audio_data
        sr = 16000

        input_features = self.processor(audio, sampling_rate=sr, return_tensors="pt").to(self.device)

        with torch.no_grad():
            transcription = self.model.generate(input_features.input_features)
        transcription_text = self.processor.batch_decode(transcription, skip_special_tokens=True)[0]

        request_copy = request.copy()
        request_copy.text_data = transcription_text

        self.ENtxt_queue.put(request_copy)
