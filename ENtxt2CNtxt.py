import torch
import threading
import multiprocessing

from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline

from logger import logger_ENtxt2CNtxt

class ENtxt2CNtxt(multiprocessing.Process):
    def __init__(self, id, ENtxt_queue, CNtxt_queue, end_signal):
        super().__init__()
        self.id = id
        self.ENtxt_queue = ENtxt_queue
        self.CNtxt_queue = CNtxt_queue
        self.end_signal = end_signal

        self.device = None
        self.tokenizer = None
        self.model = None
        self.translation = None

    def run(self):
        logger_ENtxt2CNtxt.info(f"[ENtxt2CNtxt_{self.id}] start")

        self.end_signal.value += 1

        self.device = torch.device("cuda:1")
        self.tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-zh")
        self.model = AutoModelWithLMHead.from_pretrained("Helsinki-NLP/opus-mt-en-zh").to(self.device)
        self.translation = pipeline("translation_en_to_zh", model=self.model, tokenizer=self.tokenizer, device=1)

        while True:
            request = self.ENtxt_queue.get()
            if request.signal == -1:
                self.ENtxt_queue.put(request)
                logger_ENtxt2CNtxt.info(f"[ENtxt2CNtxt_{self.id}] get signal -1")
                self.end_signal.value -= 1
                if self.end_signal.value == 0:
                    self.CNtxt_queue.put(request)
                break
            logger_ENtxt2CNtxt.info(f"[ENtxt2CNtxt_{self.id}]: {request.text_data}")
            self.process_text(request)
    
    def process_text(self, request):
        text = request.text_data

        with torch.no_grad():
            result = self.translation(text, max_length=40)[0]["translation_text"]

        request_copy = request.copy()
        request_copy.text_data = result

        self.CNtxt_queue.put(request_copy)
