import subprocess
from ovos_plugin_manager.templates.tts import TTS, TTSValidator

def get_voice_from_lang(lang):
    if lang.startswith("de"):
        return "de-DE"
    if lang.startswith("es"):
        return "es-ES"
    if lang.startswith("fr"):
        return "fr-FR"
    if lang.startswith("it"):
        return "it-IT"
    if lang.startswith("en"):
        if "gb" in lang.lower() or "uk" in lang.lower():
            return "en-GB"
        else:
            return "en-US"

class PicoTTS(TTS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, audio_ext="wav",
                         validator=PicoTTSValidator(self))
        if not self.voice:
            self.voice = get_voice_from_lang(self.lang)

    def get_tts(self, sentence, wav_file, lang=None):
        if lang:
            voice = get_voice_from_lang(lang) or self.voice
        else:
            voice = self.voice
        subprocess.call(
            ['pico2wave', '-l', voice, "-w", wav_file, sentence])

        return wav_file, None


class PicoTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(PicoTTSValidator, self).__init__(tts)

    def validate_lang(self):
        voices = ['de-DE', 'en-GB', 'en-US', 'es-ES', 'fr-FR', 'it-IT']
        lang = self.tts.lang.split("-")[0].lower().strip()
        supported = [v.split("-")[0].lower().strip() for v in voices]
        if lang not in supported:
            raise Exception('PicoTTS only supports ' + str(voices))

    def validate_connection(self):
        try:
            subprocess.call(['pico2wave', '--help'])
        except:
            raise Exception(
                'PicoTTS is not installed. Run: '
                '\nsudo apt-get install libttspico0\n'
                'sudo apt-get install  libttspico-utils')

    def get_tts_class(self):
        return PicoTTS


if __name__ == "__main__":
    e = PicoTTS()

    ssml = """Hello world"""
    e.get_tts(ssml, "pico.wav")
