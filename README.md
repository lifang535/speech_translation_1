# speech_translation_1
This is a test of multi-model_app.

## code logics

Three modules: 

`ESaudio2ENtxt`: input: ES_audio;  output: EN_text;  model: openai/whisper-large.

`ENtxt2CNtxt`: input: EN_text;  output: CN_text;  model: Helsinki-NLP/opus-mt-en-zh.

`CNtxt2CNaudio`: input: CN_text;  output: CN_audio;  model: model/text2speech.pth (local).

![Image](https://github.com/lifang535/speech_translation_1/blob/main/app.png)

## questions

1. Combine `ESaudio2EStxt` and `EStxt2ENtxt` to `ESaudio2ENtxt` with the model openai/whisper-large.

2. There is not a single sub-request, because 1 audio ~ 1 string ~ 1 translated string ~ 1 translated audio.

3. Use the `multiprocessing.set_start_method("spawn")` to prevent errors in my last code of traffic monitoring, but the sub processes start slowly.
