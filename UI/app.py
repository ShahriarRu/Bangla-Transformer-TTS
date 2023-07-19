import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from flask import Flask, render_template, request, jsonify, send_file
from model.models import ForwardTransformer
from data.audio import Audio
from vocoding.predictors import HiFiGANPredictor
import io

app = Flask(__name__)

# Path to the outputs folder
OUTPUTS_FOLDER = os.path.join(os.path.dirname(__file__), 'outputs')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    # Get the text from the request
    data = request.get_json()
    text = data['text']

    # Your code for generating the audio using the TTS system
    model = ForwardTransformer.load_model('/home/alif/Desktop/Transformer TTS/ChittagongTTS/log/ljspeech/tts_swap_conv_dims.alinger_extralayer_layernorm/weights/step_55000/')
    audio = Audio.from_config(model.config)
    out = model.predict(text, speed_regulator=0.9)
    vocoder = HiFiGANPredictor.from_folder('/home/alif/Desktop/Transformer TTS/ChittagongTTS/vocoding/hifigan/en')
    wav = vocoder([out['mel'].numpy().T])[0]

    # Save the audio to the outputs folder
    output_path = os.path.join(OUTPUTS_FOLDER, 'generated_audio.wav')
    audio.save_wav(wav, output_path)

    # Return a link to the saved audio file
    return jsonify({'audio_url': '/play'})

@app.route('/play')
def play_audio():
    # Get the path to the saved audio file
    audio_path = os.path.join(OUTPUTS_FOLDER, 'generated_audio.wav')

    # Send the audio file for playback
    return send_file(audio_path, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(debug=True)