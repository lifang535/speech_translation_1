import logging

logger_ESaudio2ENtxt = logging.getLogger('logger_ESaudio2ENtxt')
logger_ESaudio2ENtxt.setLevel(logging.INFO)
fh_ESaudio2ENtxt = logging.FileHandler('logs/ESaudio2ENtxt.log', mode='w')
fh_ESaudio2ENtxt.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh_ESaudio2ENtxt.setFormatter(formatter)
logger_ESaudio2ENtxt.addHandler(fh_ESaudio2ENtxt)

logger_ENtxt2CNtxt = logging.getLogger('logger_ENtxt2CNtxt')
logger_ENtxt2CNtxt.setLevel(logging.INFO)
fh_ENtxt2CNtxt = logging.FileHandler('logs/ENtxt2CNtxt.log', mode='w')
fh_ENtxt2CNtxt.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh_ENtxt2CNtxt.setFormatter(formatter)
logger_ENtxt2CNtxt.addHandler(fh_ENtxt2CNtxt)

logger_CNtxt2CNaudio = logging.getLogger('logger_CNtxt2CNaudio')
logger_CNtxt2CNaudio.setLevel(logging.INFO)
fh_CNtxt2CNaudio = logging.FileHandler('logs/CNtxt2CNaudio.log', mode='w')
fh_CNtxt2CNaudio.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh_CNtxt2CNaudio.setFormatter(formatter)
logger_CNtxt2CNaudio.addHandler(fh_CNtxt2CNaudio)

logger_latency = logging.getLogger('logger_latency')
logger_latency.setLevel(logging.INFO)
fh_latency = logging.FileHandler('logs/latency.log', mode='w')
fh_latency.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh_latency.setFormatter(formatter)
logger_latency.addHandler(fh_latency)

# pip install sacremoses
