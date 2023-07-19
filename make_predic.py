from model.models import ForwardTransformer
from data.audio import Audio
from vocoding.predictors import HiFiGANPredictor

import numpy as np
model = ForwardTransformer.load_model('/home/alif/Desktop/Transformer TTS/ChittagongTTS/log/ljspeech/tts_swap_conv_dims.alinger_extralayer_layernorm/weights/step_55000/')
audio = Audio.from_config(model.config)
out = model.predict('আমার সোনার বাংলা',speed_regulator=.9)
outdir = './outputs/custom_text/dekh_hoye_valo_laglo3.wav'

vocoder = HiFiGANPredictor.from_folder('/home/alif/Desktop/Transformer TTS/ChittagongTTS/vocoding/hifigan/en')
wav = vocoder([out['mel'].numpy().T])[0]
# Convert spectrogram to wav (with griffin lim)
# wav = audio.reconstruct_waveform(out['mel'].numpy().T)
audio.save_wav(wav, outdir)

