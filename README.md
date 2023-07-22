<h2 align="center">
<p>Bangla Transformer Based TTS Model</p>
</h2>

#### Non-Autoregressive

Being non-autoregressive, this Transformer model is:

- Robust: No repeats and failed attention modes for challenging sentences.
- Fast: With no autoregression, predictions take a fraction of the time.
- Controllable: It is possible to control the speed and pitch of the generated utterance.

## 📖 Contents

- [Installation](#installation)
- [API](#pre-trained-ljspeech-api)
- [Dataset](#dataset)
- [Training](#training)
  - [Aligner](#train-aligner-model)
  - [TTS](#train-tts-model)
- [Prediction](#prediction)
- [Model Weights](#model-weights)

## Installation

Make sure you have:

- Python >= 3.6

Install espeak as phonemizer backend (for macOS use brew):

```
sudo apt-get install espeak
```

Then install the rest with pip:

```
pip install -r requirements.txt
```

## Dataset

You can directly use [LJSpeech](https://keithito.com/LJ-Speech-Dataset/) to create the training dataset.

#### Configuration

- Use `config/training_config.yaml` to create [MelGAN](https://github.com/seungwonpark/melgan) or [HiFiGAN](https://github.com/jik876/hifi-gan) compatible models
  - swap the content of `data_config_wavernn.yaml` in `config/training_config.yaml` to create models compatible with [WaveRNN](https://github.com/fatchord/WaveRNN)
- **EDIT PATHS**: in `config/training_config.yaml` edit the paths to point at your dataset and log folders

#### Custom dataset

Prepare a folder containing your metadata and wav files, for instance

```
|- dataset_folder/
|   |- metadata.csv
|   |- wavs/
|       |- file1.wav
|       |- ...
```

if `metadata.csv` has the following format
`wav_file_name|transcription`
you can use the preprocessor in `data/metadata_readers.py`, otherwise add your own under the same file.

Make sure that:

- the metadata reader function name is the same as `data_name` field in `training_config.yaml`.
- the metadata file (can be anything) is specified under `metadata_path` in `training_config.yaml`

## Training

Change the `--config` argument based on the configuration of your choice.

### Train Aligner Model

#### Create training dataset

```bash
python create_training_data.py --config config/training_config.yaml
```

This will populate the training data directory (default `transformer_tts_data.ljspeech`).

#### Training

```bash
python train_aligner.py --config config/training_config.yaml
```

### Train TTS Model

#### Compute alignment dataset

First use the aligner model to create the durations dataset

```bash
python extract_durations.py --config config/training_config.yaml
```

this will add the `durations.<session name>` as well as the char-wise pitch folders to the training data directory.

#### Training

```bash
python train_tts.py --config config/training_config.yaml
```

#### Training & Model configuration

- Training and model settings can be configured in `training_config.yaml`

#### Resume or restart training

- To resume training simply use the same configuration files
- To restart training, delete the weights and/or the logs from the logs folder with the training flag `--reset_dir` (both) or `--reset_logs`, `--reset_weights`

## Prediction

### With model weights

From command line with

```commandline
python predict_tts.py -t "Please, say something." -p /path/to/weights/
```

With griffin lim vocoder

```python
from model.models import ForwardTransformer
from data.audio import Audio

model = ForwardTransformer.load_model('/path/to/weights/')
audio = Audio.from_config(model.config)
out = model.predict('আমার সোনার বাংলা')

# Convert spectrogram to wav (with griffin lim)
wav = audio.reconstruct_waveform(out['mel'].numpy().T)
```

With HiFiGAN vocoder

```
from model.models import ForwardTransformer
from data.audio import Audio
from vocoding.predictors import HiFiGANPredictor

model = ForwardTransformer.load_model('/path/to/weights/')
audio = Audio.from_config(model.config)
out = model.predict('আমার সোনার বাংলা',speed_regulator=.9)
outdir = '/path/to/output'

vocoder = HiFiGANPredictor.from_folder('/path/to/hifigan)
wav = vocoder([out['mel'].numpy().T])[0]

```

## System UI

On Web: [BanglaTTS](https://shahriarru.github.io/Bangla-Transformer-TTS/UI/templates/index.html)

UI:
[SystemUI](https://github.com/ShahriarRu/Bangla-Transformer-TTS/blob/main/ui.png)

Implementation of a non-autoregressive Transformer based neural network for Bangla Text-to-Speech (TTS). <br>
This repo is based, among others, on the following papers:

- [Neural Speech Synthesis with Transformer Network](https://arxiv.org/abs/1809.08895)
- [FastSpeech: Fast, Robust and Controllable Text to Speech](https://arxiv.org/abs/1905.09263)
- [FastSpeech 2: Fast and High-Quality End-to-End Text to Speech](https://arxiv.org/abs/2006.04558)
- [FastPitch: Parallel Text-to-speech with Pitch Prediction](https://fastpitch.github.io/)
  Github refernce repo: [TransformerTTS](https://github.com/as-ideas/TransformerTTS)

## Copyright

See [LICENSE](LICENSE) for details.

# Bangla-Transformer-TTS
