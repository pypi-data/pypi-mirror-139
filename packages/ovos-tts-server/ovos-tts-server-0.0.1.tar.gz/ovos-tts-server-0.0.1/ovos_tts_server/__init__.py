# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from flask import Flask, send_file
from ovos_plugin_manager.tts import load_tts_plugin
from ovos_plugin_manager.utils.tts_cache import hash_sentence

TTS = None


def get_tts(sentence):
    global TTS
    sentence_hash = hash_sentence(sentence)
    if sentence_hash in TTS.cache:  # load from cache
        audio_file, phonemes = TTS._get_from_cache(sentence, sentence_hash)
    else:  # synth + cache
        audio_file, phonemes = TTS._synth(sentence, sentence_hash)
    return audio_file.path


def create_app():
    app = Flask(__name__)

    @app.route("/synthesize/<utterance>", methods=['GET'])
    def synth(utterance):
        audio = get_tts(utterance)
        return send_file(audio, mimetype="audio/wav")

    return app


def start_tts_server(engine, port=9666, host="0.0.0.0", cache=False):
    global TTS

    # load ovos TTS plugin
    engine = load_tts_plugin(engine)

    TTS = engine(config={"persist_cache": cache})  # this will cache every synth even across reboots
    TTS.log_timestamps = True  # enable logging

    app = create_app()
    app.run(port=port, use_reloader=False, host=host)
    return app


