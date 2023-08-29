# speech_translation_1
This is a test of multi-model_app.

## code logics

### Three modules: 

`ESaudio2ENtxt`: input: ES_audio;  output: EN_text;      
model: openai/whisper-large from https://huggingface.co/openai/whisper-large.

`ENtxt2CNtxt`: input: EN_text;  output: CN_text;      
model: Helsinki-NLP/opus-mt-en-zh from https://huggingface.co/Helsinki-NLP/opus-mt-en-zh.

`CNtxt2CNaudio`: input: CN_text;  output: CN_audio;      
model: model/text2speech.pth from https://huggingface.co/espnet/kan-bayashi_csmsc_tts_train_tacotron2_raw_phn_pypinyin_g2p_phone_train.loss.best.

![Image](https://github.com/lifang535/speech_translation_1/blob/main/app.png)

Test audios are in: https://huggingface.co/datasets/mozilla-foundation/common_voice_11_0/viewer/es/train?row=19.

### Request in data transmission: 

1 * ES_audio(np.ndarray) : 1 * EN_text(str) : 1 * CN_text(str) : 1 * CN_audio(np.ndarray)

### Throughout of model: 

When the modules are 1 : 1 : 1 for inference, the process time of audios are (without request heap and batch processing):

```
ESaudio2ENtxt: [2.024, 0.687, 0.752, 0.599, 0.608, 0.614, 0.675, 0.935, 0.781, 0.880, 0.911, 0.846, 0.723, 0.919, 0.877, 0.774, 0.580, 0.763, 0.924, 0.883]

ENtxt2CNtxt:   [1.177, 0.079, 0.096, 0.080, 0.068, 0.081, 0.095, 0.119, 0.119, 0.117, 0.116, 0.109, 0.101, 0.147, 0.096, 0.068, 0.063, 0.103, 0.121, 0.190]

CNtxt2CNaudio: [2.213, 2.744, 3.083, 2.894, 1.712, 1.770, 1.794, 3.469, 3.704, 3.116, 3.382, 3.838, 3.280, 4.212, 3.167, 3.399, 1.271, 3.121, 3.229, 6.641]

latency:       [5.491, 3.444, 3.651, 3.511, 2.344, 2.283, 2.540, 4.539, 4.711, 4.475, 4.448, 4.626, 4.045, 4.991, 4.450, 4.355, 1.924, 3.994, 4.067, 7.683]
```

Throughout:
·```
throughout of ESaudio2ENtxt ≈ 1.29 req/s

throughout of ENtxt2CNtxt ≈ 9.65 req/s

throughout of CNtxt2CNaudio ≈ 0.32 req/s
```

When the modules are 1 : 1 : 2 or 1 : 1 : 3 for inference, the performance are worce than 1 : 1 : 1, and the latency are longger for each audio (almost 2 ~ 3 times).

## questions

1. Combine `ESaudio2EStxt` and `EStxt2ENtxt` to `ESaudio2ENtxt` with the model openai/whisper-large. Actually, like ES, these languages need not Relay Translation to translate, but what need to, like Javanese, is difficult to find appropriate models to make pipeline. So just use ES to simulate.

2. There is not a single sub-request, because 1 audio ~ 1 string ~ 1 translated string ~ 1 translated audio.

3. Use the `multiprocessing.set_start_method("spawn")` to prevent errors in my last code of traffic monitoring, but the sub processes start slowly. When the modules are 1 : 1 : 1 for inference, the cold start of all modules is about 20 seconds. And when setting this, `multiprocessing.lock()` causes error: 
      ```
      Traceback (most recent call last):
        File "pipeline.py", line 19, in <module>
          multiprocessing.set_start_method("spawn")
        File "/opt/conda/envs/base_copy_1/lib/python3.7/multiprocessing/context.py", line 242, in set_start_method
          raise RuntimeError('context has already been set')
      RuntimeError: context has already been set
      ```

4. `CNtxt2CNaudio` is not use gpu to speed up operations, but its performance and processing rate in the CN2audio are better than some other models using gpu like suno/bark-small from https://huggingface.co/suno/bark-small and suno/bark from https://huggingface.co/suno/bark.
