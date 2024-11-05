import sys
import inspect
from os import path as os_path, makedirs as os_makedirs
from json import load as json_load
from json import dump as json_dump
import threading
from device_manager import device_manager
from models.transcription.transcription_languages import transcription_lang
from utils import isUniqueStrings

json_serializable_vars = {}
def json_serializable(var_name):
    def decorator(func):
        json_serializable_vars[var_name] = func
        return func
    return decorator

class Config:
    _instance = None
    _config_data = {}
    _timer = None
    _debounce_time = 2

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.init_config()
            cls._instance.load_config()
        return cls._instance

    def saveConfigToFile(self):
        with open(self.PATH_CONFIG, "w", encoding="utf-8") as fp:
            json_dump(self._config_data, fp, indent=4, ensure_ascii=False)

    def saveConfig(self, key, value):
        self._config_data[key] = value

        if isinstance(self._timer, threading.Timer) and self._timer.is_alive():
            self._timer.cancel()
        self._timer = threading.Timer(self._debounce_time, self.saveConfigToFile)
        self._timer.daemon = True
        self._timer.start()

    # Read Only
    @property
    def VERSION(self):
        return self._VERSION

    @property
    def PATH_LOCAL(self):
        return self._PATH_LOCAL

    @property
    def PATH_CONFIG(self):
        return self._PATH_CONFIG

    @property
    def PATH_LOGS(self):
        return self._PATH_LOGS

    @property
    def GITHUB_URL(self):
        return self._GITHUB_URL

    @property
    def UPDATER_URL(self):
        return self._UPDATER_URL

    @property
    def BOOTH_URL(self):
        return self._BOOTH_URL

    @property
    def DOCUMENTS_URL(self):
        return self._DOCUMENTS_URL

    @property
    def DEEPL_AUTH_KEY_PAGE_URL(self):
        return self._DEEPL_AUTH_KEY_PAGE_URL

    @property
    def TRANSPARENCY_RANGE(self):
        return self._TRANSPARENCY_RANGE

    @property
    def UI_SCALING_RANGE(self):
        return self._UI_SCALING_RANGE

    @property
    def TEXTBOX_UI_SCALING_RANGE(self):
        return self._TEXTBOX_UI_SCALING_RANGE

    @property
    def MESSAGE_BOX_RATIO_RANGE(self):
        return self._MESSAGE_BOX_RATIO_RANGE

    @property
    def MAX_MIC_THRESHOLD(self):
        return self._MAX_MIC_THRESHOLD

    @property
    def MAX_SPEAKER_THRESHOLD(self):
        return self._MAX_SPEAKER_THRESHOLD

    @property
    def WATCHDOG_TIMEOUT(self):
        return self._WATCHDOG_TIMEOUT

    @property
    def WATCHDOG_INTERVAL(self):
        return self._WATCHDOG_INTERVAL

    # Read Write
    @property
    def ENABLE_TRANSLATION(self):
        return self._ENABLE_TRANSLATION

    @ENABLE_TRANSLATION.setter
    def ENABLE_TRANSLATION(self, value):
        if isinstance(value, bool):
            self._ENABLE_TRANSLATION = value

    @property
    def ENABLE_TRANSCRIPTION_SEND(self):
        return self._ENABLE_TRANSCRIPTION_SEND

    @ENABLE_TRANSCRIPTION_SEND.setter
    def ENABLE_TRANSCRIPTION_SEND(self, value):
        if isinstance(value, bool):
            self._ENABLE_TRANSCRIPTION_SEND = value

    @property
    def ENABLE_TRANSCRIPTION_RECEIVE(self):
        return self._ENABLE_TRANSCRIPTION_RECEIVE

    @ENABLE_TRANSCRIPTION_RECEIVE.setter
    def ENABLE_TRANSCRIPTION_RECEIVE(self, value):
        if isinstance(value, bool):
            self._ENABLE_TRANSCRIPTION_RECEIVE = value

    @property
    def ENABLE_FOREGROUND(self):
        return self._ENABLE_FOREGROUND

    @ENABLE_FOREGROUND.setter
    def ENABLE_FOREGROUND(self, value):
        if isinstance(value, bool):
            self._ENABLE_FOREGROUND = value

    @property
    def ENABLE_CHECK_ENERGY_SEND(self):
        return self._ENABLE_CHECK_ENERGY_SEND

    @ENABLE_CHECK_ENERGY_SEND.setter
    def ENABLE_CHECK_ENERGY_SEND(self, value):
        if isinstance(value, bool):
            self._ENABLE_CHECK_ENERGY_SEND = value

    @property
    def ENABLE_CHECK_ENERGY_RECEIVE(self):
        return self._ENABLE_CHECK_ENERGY_RECEIVE

    @ENABLE_CHECK_ENERGY_RECEIVE.setter
    def ENABLE_CHECK_ENERGY_RECEIVE(self, value):
        if isinstance(value, bool):
            self._ENABLE_CHECK_ENERGY_RECEIVE = value

    @property
    def SELECTABLE_CTRANSLATE2_WEIGHT_TYPE_DICT(self):
        return self._SELECTABLE_CTRANSLATE2_WEIGHT_TYPE_DICT

    @SELECTABLE_CTRANSLATE2_WEIGHT_TYPE_DICT.setter
    def SELECTABLE_CTRANSLATE2_WEIGHT_TYPE_DICT(self, value):
        if isinstance(value, dict):
            self._SELECTABLE_CTRANSLATE2_WEIGHT_TYPE_DICT = value

    @property
    def SELECTABLE_WHISPER_WEIGHT_TYPE_DICT(self):
        return self._SELECTABLE_WHISPER_WEIGHT_TYPE_DICT

    @SELECTABLE_WHISPER_WEIGHT_TYPE_DICT.setter
    def SELECTABLE_WHISPER_WEIGHT_TYPE_DICT(self, value):
        if isinstance(value, dict):
            self._SELECTABLE_WHISPER_WEIGHT_TYPE_DICT = value

    # Save Json Data
    ## Main Window
    @property
    @json_serializable('SELECTED_TAB_NO')
    def SELECTED_TAB_NO(self):
        return self._SELECTED_TAB_NO

    @SELECTED_TAB_NO.setter
    def SELECTED_TAB_NO(self, value):
        if isinstance(value, str):
            self._SELECTED_TAB_NO = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SELECTED_TRANSLATION_ENGINES')
    def SELECTED_TRANSLATION_ENGINES(self):
        return self._SELECTED_TRANSLATION_ENGINES

    @SELECTED_TRANSLATION_ENGINES.setter
    def SELECTED_TRANSLATION_ENGINES(self, value):
        if isinstance(value, dict):
            self._SELECTED_TRANSLATION_ENGINES = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SELECTED_YOUR_LANGUAGES')
    def SELECTED_YOUR_LANGUAGES(self):
        return self._SELECTED_YOUR_LANGUAGES

    @SELECTED_YOUR_LANGUAGES.setter
    def SELECTED_YOUR_LANGUAGES(self, value):
        try:
            if isinstance(value, dict):
                value_old = self.SELECTED_YOUR_LANGUAGES
                for k0, v0 in value.items():
                    for k1, v1 in v0.items():
                        language = v1["language"]
                        country = v1["country"]
                        if language not in list(transcription_lang.keys()) or country not in list(transcription_lang[language].keys()):
                            value[k0][k1] = value_old[k0][k1]
                self._SELECTED_YOUR_LANGUAGES = value
        except Exception:
            pass
        self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SELECTED_TARGET_LANGUAGES')
    def SELECTED_TARGET_LANGUAGES(self):
        return self._SELECTED_TARGET_LANGUAGES

    @SELECTED_TARGET_LANGUAGES.setter
    def SELECTED_TARGET_LANGUAGES(self, value):
        try:
            if isinstance(value, dict):
                value_old = self.SELECTED_TARGET_LANGUAGES
                for k0, v0 in value.items():
                    for k1, v1 in v0.items():
                        language = v1["language"]
                        country = v1["country"]
                        if language not in list(transcription_lang.keys()) or country not in list(transcription_lang[language].keys()):
                            value[k0][k1] = value_old[k0][k1]
                self._SELECTED_TARGET_LANGUAGES = value
        except Exception:
            pass
        self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SELECTED_TRANSCRIPTION_ENGINE')
    def SELECTED_TRANSCRIPTION_ENGINE(self):
        return self._SELECTED_TRANSCRIPTION_ENGINE

    @SELECTED_TRANSCRIPTION_ENGINE.setter
    def SELECTED_TRANSCRIPTION_ENGINE(self, value):
        if isinstance(value, str):
            self._SELECTED_TRANSCRIPTION_ENGINE = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('MULTI_LANGUAGE_TRANSLATION')
    def MULTI_LANGUAGE_TRANSLATION(self):
        return self._MULTI_LANGUAGE_TRANSLATION

    @MULTI_LANGUAGE_TRANSLATION.setter
    def MULTI_LANGUAGE_TRANSLATION(self, value):
        if isinstance(value, bool):
            self._MULTI_LANGUAGE_TRANSLATION = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('CONVERT_MESSAGE_TO_ROMAJI')
    def CONVERT_MESSAGE_TO_ROMAJI(self):
        return self._CONVERT_MESSAGE_TO_ROMAJI

    @CONVERT_MESSAGE_TO_ROMAJI.setter
    def CONVERT_MESSAGE_TO_ROMAJI(self, value):
        if isinstance(value, bool):
            self._CONVERT_MESSAGE_TO_ROMAJI = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('CONVERT_MESSAGE_TO_HIRAGANA')
    def CONVERT_MESSAGE_TO_HIRAGANA(self):
        return self._CONVERT_MESSAGE_TO_HIRAGANA

    @CONVERT_MESSAGE_TO_HIRAGANA.setter
    def CONVERT_MESSAGE_TO_HIRAGANA(self, value):
        if isinstance(value, bool):
            self._CONVERT_MESSAGE_TO_HIRAGANA = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('MAIN_WINDOW_SIDEBAR_COMPACT_MODE')
    def MAIN_WINDOW_SIDEBAR_COMPACT_MODE(self):
        return self._MAIN_WINDOW_SIDEBAR_COMPACT_MODE

    @MAIN_WINDOW_SIDEBAR_COMPACT_MODE.setter
    def MAIN_WINDOW_SIDEBAR_COMPACT_MODE(self, value):
        if isinstance(value, bool):
            self._MAIN_WINDOW_SIDEBAR_COMPACT_MODE = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    ## Config Window
    @property
    @json_serializable('TRANSPARENCY')
    def TRANSPARENCY(self):
        return self._TRANSPARENCY

    @TRANSPARENCY.setter
    def TRANSPARENCY(self, value):
        if isinstance(value, int):
            self._TRANSPARENCY = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('UI_SCALING')
    def UI_SCALING(self):
        return self._UI_SCALING

    @UI_SCALING.setter
    def UI_SCALING(self, value):
        if isinstance(value, int):
            self._UI_SCALING = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('TEXTBOX_UI_SCALING')
    def TEXTBOX_UI_SCALING(self):
        return self._TEXTBOX_UI_SCALING

    @TEXTBOX_UI_SCALING.setter
    def TEXTBOX_UI_SCALING(self, value):
        if isinstance(value, int):
            self._TEXTBOX_UI_SCALING = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('MESSAGE_BOX_RATIO')
    def MESSAGE_BOX_RATIO(self):
        return self._MESSAGE_BOX_RATIO

    @MESSAGE_BOX_RATIO.setter
    def MESSAGE_BOX_RATIO(self, value):
        if isinstance(value, (int, float)):
            self._MESSAGE_BOX_RATIO = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('FONT_FAMILY')
    def FONT_FAMILY(self):
        return self._FONT_FAMILY

    @FONT_FAMILY.setter
    def FONT_FAMILY(self, value):
        if isinstance(value, str):
            self._FONT_FAMILY = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('UI_LANGUAGE')
    def UI_LANGUAGE(self):
        return self._UI_LANGUAGE

    @UI_LANGUAGE.setter
    def UI_LANGUAGE(self, value):
        if isinstance(value, str):
            self._UI_LANGUAGE = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('RESTORE_MAIN_WINDOW_GEOMETRY')
    def RESTORE_MAIN_WINDOW_GEOMETRY(self):
        return self._RESTORE_MAIN_WINDOW_GEOMETRY

    @RESTORE_MAIN_WINDOW_GEOMETRY.setter
    def RESTORE_MAIN_WINDOW_GEOMETRY(self, value):
        if isinstance(value, bool):
            self._RESTORE_MAIN_WINDOW_GEOMETRY = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('MAIN_WINDOW_GEOMETRY')
    def MAIN_WINDOW_GEOMETRY(self):
        return self._MAIN_WINDOW_GEOMETRY

    @MAIN_WINDOW_GEOMETRY.setter
    def MAIN_WINDOW_GEOMETRY(self, value):
        if isinstance(value, dict) and set(value.keys()) == set(self.MAIN_WINDOW_GEOMETRY.keys()):
            for key, value in value.items():
                if isinstance(value, int):
                    self._MAIN_WINDOW_GEOMETRY[key] = value
            self.saveConfig(inspect.currentframe().f_code.co_name, self.MAIN_WINDOW_GEOMETRY)

    @property
    @json_serializable('AUTO_MIC_SELECT')
    def AUTO_MIC_SELECT(self):
        return self._AUTO_MIC_SELECT

    @AUTO_MIC_SELECT.setter
    def AUTO_MIC_SELECT(self, value):
        if isinstance(value, bool):
            self._AUTO_MIC_SELECT = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SELECTED_MIC_HOST')
    def SELECTED_MIC_HOST(self):
        return self._SELECTED_MIC_HOST

    @SELECTED_MIC_HOST.setter
    def SELECTED_MIC_HOST(self, value):
        if value in [host for host in device_manager.getMicDevices().keys()]:
            self._SELECTED_MIC_HOST = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SELECTED_MIC_DEVICE')
    def SELECTED_MIC_DEVICE(self):
        return self._SELECTED_MIC_DEVICE

    @SELECTED_MIC_DEVICE.setter
    def SELECTED_MIC_DEVICE(self, value):
        if value in [device["name"] for device in device_manager.getMicDevices()[self.SELECTED_MIC_HOST]]:
            self._SELECTED_MIC_DEVICE = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('MIC_THRESHOLD')
    def MIC_THRESHOLD(self):
        return self._MIC_THRESHOLD

    @MIC_THRESHOLD.setter
    def MIC_THRESHOLD(self, value):
        if isinstance(value, int):
            self._MIC_THRESHOLD = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('MIC_AUTOMATIC_THRESHOLD')
    def MIC_AUTOMATIC_THRESHOLD(self):
        return self._MIC_AUTOMATIC_THRESHOLD

    @MIC_AUTOMATIC_THRESHOLD.setter
    def MIC_AUTOMATIC_THRESHOLD(self, value):
        if isinstance(value, bool):
            self._MIC_AUTOMATIC_THRESHOLD = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('MIC_RECORD_TIMEOUT')
    def MIC_RECORD_TIMEOUT(self):
        return self._MIC_RECORD_TIMEOUT

    @MIC_RECORD_TIMEOUT.setter
    def MIC_RECORD_TIMEOUT(self, value):
        if isinstance(value, int):
            self._MIC_RECORD_TIMEOUT = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('MIC_PHRASE_TIMEOUT')
    def MIC_PHRASE_TIMEOUT(self):
        return self._MIC_PHRASE_TIMEOUT

    @MIC_PHRASE_TIMEOUT.setter
    def MIC_PHRASE_TIMEOUT(self, value):
        if isinstance(value, int):
            self._MIC_PHRASE_TIMEOUT = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('MIC_MAX_PHRASES')
    def MIC_MAX_PHRASES(self):
        return self._MIC_MAX_PHRASES

    @MIC_MAX_PHRASES.setter
    def MIC_MAX_PHRASES(self, value):
        if isinstance(value, int):
            self._MIC_MAX_PHRASES = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('MIC_WORD_FILTER')
    def MIC_WORD_FILTER(self):
        return self._MIC_WORD_FILTER

    @MIC_WORD_FILTER.setter
    def MIC_WORD_FILTER(self, value):
        if isinstance(value, list):
            self._MIC_WORD_FILTER = sorted(set(value), key=value.index)
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('MIC_AVG_LOGPROB')
    def MIC_AVG_LOGPROB(self):
        return self._MIC_AVG_LOGPROB

    @MIC_AVG_LOGPROB.setter
    def MIC_AVG_LOGPROB(self, value):
        if isinstance(value, (int, float)):
            self._MIC_AVG_LOGPROB = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('MIC_NO_SPEECH_PROB')
    def MIC_NO_SPEECH_PROB(self):
        return self._MIC_NO_SPEECH_PROB

    @MIC_NO_SPEECH_PROB.setter
    def MIC_NO_SPEECH_PROB(self, value):
        if isinstance(value, (int, float)):
            self._MIC_NO_SPEECH_PROB = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('AUTO_SPEAKER_SELECT')
    def AUTO_SPEAKER_SELECT(self):
        return self._AUTO_SPEAKER_SELECT

    @AUTO_SPEAKER_SELECT.setter
    def AUTO_SPEAKER_SELECT(self, value):
        if isinstance(value, bool):
            self._AUTO_SPEAKER_SELECT = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SELECTED_SPEAKER_DEVICE')
    def SELECTED_SPEAKER_DEVICE(self):
        return self._SELECTED_SPEAKER_DEVICE

    @SELECTED_SPEAKER_DEVICE.setter
    def SELECTED_SPEAKER_DEVICE(self, value):
        if value in [device["name"] for device in device_manager.getSpeakerDevices()]:
            self._SELECTED_SPEAKER_DEVICE = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SPEAKER_THRESHOLD')
    def SPEAKER_THRESHOLD(self):
        return self._SPEAKER_THRESHOLD

    @SPEAKER_THRESHOLD.setter
    def SPEAKER_THRESHOLD(self, value):
        if isinstance(value, int):
            self._SPEAKER_THRESHOLD = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SPEAKER_AUTOMATIC_THRESHOLD')
    def SPEAKER_AUTOMATIC_THRESHOLD(self):
        return self._SPEAKER_AUTOMATIC_THRESHOLD

    @SPEAKER_AUTOMATIC_THRESHOLD.setter
    def SPEAKER_AUTOMATIC_THRESHOLD(self, value):
        if isinstance(value, bool):
            self._SPEAKER_AUTOMATIC_THRESHOLD = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SPEAKER_RECORD_TIMEOUT')
    def SPEAKER_RECORD_TIMEOUT(self):
        return self._SPEAKER_RECORD_TIMEOUT

    @SPEAKER_RECORD_TIMEOUT.setter
    def SPEAKER_RECORD_TIMEOUT(self, value):
        if isinstance(value, int):
            self._SPEAKER_RECORD_TIMEOUT = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SPEAKER_PHRASE_TIMEOUT')
    def SPEAKER_PHRASE_TIMEOUT(self):
        return self._SPEAKER_PHRASE_TIMEOUT

    @SPEAKER_PHRASE_TIMEOUT.setter
    def SPEAKER_PHRASE_TIMEOUT(self, value):
        if isinstance(value, int):
            self._SPEAKER_PHRASE_TIMEOUT = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SPEAKER_MAX_PHRASES')
    def SPEAKER_MAX_PHRASES(self):
        return self._SPEAKER_MAX_PHRASES

    @SPEAKER_MAX_PHRASES.setter
    def SPEAKER_MAX_PHRASES(self, value):
        if isinstance(value, int):
            self._SPEAKER_MAX_PHRASES = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SPEAKER_AVG_LOGPROB')
    def SPEAKER_AVG_LOGPROB(self):
        return self._SPEAKER_AVG_LOGPROB

    @SPEAKER_AVG_LOGPROB.setter
    def SPEAKER_AVG_LOGPROB(self, value):
        if isinstance(value, (int, float)):
            self._SPEAKER_AVG_LOGPROB = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SPEAKER_NO_SPEECH_PROB')
    def SPEAKER_NO_SPEECH_PROB(self):
        return self._SPEAKER_NO_SPEECH_PROB

    @SPEAKER_NO_SPEECH_PROB.setter
    def SPEAKER_NO_SPEECH_PROB(self, value):
        if isinstance(value, (int, float)):
            self._SPEAKER_NO_SPEECH_PROB = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('OSC_IP_ADDRESS')
    def OSC_IP_ADDRESS(self):
        return self._OSC_IP_ADDRESS

    @OSC_IP_ADDRESS.setter
    def OSC_IP_ADDRESS(self, value):
        if isinstance(value, str):
            self._OSC_IP_ADDRESS = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('OSC_PORT')
    def OSC_PORT(self):
        return self._OSC_PORT

    @OSC_PORT.setter
    def OSC_PORT(self, value):
        if isinstance(value, int):
            self._OSC_PORT = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('AUTH_KEYS')
    def AUTH_KEYS(self):
        return self._AUTH_KEYS

    @AUTH_KEYS.setter
    def AUTH_KEYS(self, value):
        if isinstance(value, dict) and set(value.keys()) == set(self.AUTH_KEYS.keys()):
            for key, value in value.items():
                if isinstance(value, str):
                    self._AUTH_KEYS[key] = value
            self.saveConfig(inspect.currentframe().f_code.co_name, self.AUTH_KEYS)

    @property
    @json_serializable('USE_EXCLUDE_WORDS')
    def USE_EXCLUDE_WORDS(self):
        return self._USE_EXCLUDE_WORDS

    @USE_EXCLUDE_WORDS.setter
    def USE_EXCLUDE_WORDS(self, value):
        if isinstance(value, bool):
            self._USE_EXCLUDE_WORDS = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SELECTED_TRANSLATION_COMPUTE_DEVICE')
    def SELECTED_TRANSLATION_COMPUTE_DEVICE(self):
        return self._SELECTED_TRANSLATION_COMPUTE_DEVICE

    @SELECTED_TRANSLATION_COMPUTE_DEVICE.setter
    def SELECTED_TRANSLATION_COMPUTE_DEVICE(self, value):
        if isinstance(value, dict):
            self._SELECTED_TRANSLATION_COMPUTE_DEVICE = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SELECTED_TRANSCRIPTION_COMPUTE_DEVICE')
    def SELECTED_TRANSCRIPTION_COMPUTE_DEVICE(self):
        return self._SELECTED_TRANSCRIPTION_COMPUTE_DEVICE

    @SELECTED_TRANSCRIPTION_COMPUTE_DEVICE.setter
    def SELECTED_TRANSCRIPTION_COMPUTE_DEVICE(self, value):
        if isinstance(value, dict):
            self._SELECTED_TRANSCRIPTION_COMPUTE_DEVICE = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('CTRANSLATE2_WEIGHT_TYPE')
    def CTRANSLATE2_WEIGHT_TYPE(self):
        return self._CTRANSLATE2_WEIGHT_TYPE

    @CTRANSLATE2_WEIGHT_TYPE.setter
    def CTRANSLATE2_WEIGHT_TYPE(self, value):
        if isinstance(value, str):
            self._CTRANSLATE2_WEIGHT_TYPE = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('WHISPER_WEIGHT_TYPE')
    def WHISPER_WEIGHT_TYPE(self):
        return self._WHISPER_WEIGHT_TYPE

    @WHISPER_WEIGHT_TYPE.setter
    def WHISPER_WEIGHT_TYPE(self, value):
        if isinstance(value, str):
            self._WHISPER_WEIGHT_TYPE = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('AUTO_CLEAR_MESSAGE_BOX')
    def AUTO_CLEAR_MESSAGE_BOX(self):
        return self._AUTO_CLEAR_MESSAGE_BOX

    @AUTO_CLEAR_MESSAGE_BOX.setter
    def AUTO_CLEAR_MESSAGE_BOX(self, value):
        if isinstance(value, bool):
            self._AUTO_CLEAR_MESSAGE_BOX = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SEND_ONLY_TRANSLATED_MESSAGES')
    def SEND_ONLY_TRANSLATED_MESSAGES(self):
        return self._SEND_ONLY_TRANSLATED_MESSAGES

    @SEND_ONLY_TRANSLATED_MESSAGES.setter
    def SEND_ONLY_TRANSLATED_MESSAGES(self, value):
        if isinstance(value, bool):
            self._SEND_ONLY_TRANSLATED_MESSAGES = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SEND_MESSAGE_BUTTON_TYPE')
    def SEND_MESSAGE_BUTTON_TYPE(self):
        return self._SEND_MESSAGE_BUTTON_TYPE

    @SEND_MESSAGE_BUTTON_TYPE.setter
    def SEND_MESSAGE_BUTTON_TYPE(self, value):
        if isinstance(value, str):
            self._SEND_MESSAGE_BUTTON_TYPE = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('OVERLAY_SMALL_LOG')
    def OVERLAY_SMALL_LOG(self):
        return self._OVERLAY_SMALL_LOG

    @OVERLAY_SMALL_LOG.setter
    def OVERLAY_SMALL_LOG(self, value):
        if isinstance(value, bool):
            self._OVERLAY_SMALL_LOG = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('OVERLAY_SMALL_LOG_SETTINGS')
    def OVERLAY_SMALL_LOG_SETTINGS(self):
        return self._OVERLAY_SMALL_LOG_SETTINGS

    @OVERLAY_SMALL_LOG_SETTINGS.setter
    def OVERLAY_SMALL_LOG_SETTINGS(self, value):
        if isinstance(value, dict) and set(value.keys()) == set(self.OVERLAY_SMALL_LOG_SETTINGS.keys()):
            for key, value in value.items():
                match (key):
                    case "x_pos" | "y_pos" | "z_pos" | "x_rotation" | "y_rotation" | "z_rotation":
                        if isinstance(value, (int, float)):
                            self._OVERLAY_SMALL_LOG_SETTINGS[key] = float(value)
                    case "display_duration" | "fadeout_duration":
                        if isinstance(value, int):
                            self._OVERLAY_SMALL_LOG_SETTINGS[key] = value
                    case "opacity" | "ui_scaling":
                        if isinstance(value, (int, float)):
                            self._OVERLAY_SMALL_LOG_SETTINGS[key] = float(value)
            self.saveConfig(inspect.currentframe().f_code.co_name, self.OVERLAY_SMALL_LOG_SETTINGS)

    @property
    @json_serializable('SEND_MESSAGE_TO_VRC')
    def SEND_MESSAGE_TO_VRC(self):
        return self._SEND_MESSAGE_TO_VRC

    @SEND_MESSAGE_TO_VRC.setter
    def SEND_MESSAGE_TO_VRC(self, value):
        if isinstance(value, bool):
            self._SEND_MESSAGE_TO_VRC = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SEND_MESSAGE_FORMAT')
    def SEND_MESSAGE_FORMAT(self):
        return self._SEND_MESSAGE_FORMAT

    @SEND_MESSAGE_FORMAT.setter
    def SEND_MESSAGE_FORMAT(self, value):
        if isinstance(value, str):
            if isUniqueStrings(["[message]"], value) is False:
                value = "[message]"
            self._SEND_MESSAGE_FORMAT = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SEND_MESSAGE_FORMAT_WITH_T')
    def SEND_MESSAGE_FORMAT_WITH_T(self):
        return self._SEND_MESSAGE_FORMAT_WITH_T

    @SEND_MESSAGE_FORMAT_WITH_T.setter
    def SEND_MESSAGE_FORMAT_WITH_T(self, value):
        if isinstance(value, str):
            if isUniqueStrings(["[message]", "[translation]"], value) is False:
                value = "[message]([translation])"
            self._SEND_MESSAGE_FORMAT_WITH_T = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('RECEIVED_MESSAGE_FORMAT')
    def RECEIVED_MESSAGE_FORMAT(self):
        return self._RECEIVED_MESSAGE_FORMAT

    @RECEIVED_MESSAGE_FORMAT.setter
    def RECEIVED_MESSAGE_FORMAT(self, value):
        if isinstance(value, str):
            if isUniqueStrings(["[message]"], value) is False:
                value = "[message]"
            self._RECEIVED_MESSAGE_FORMAT = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('RECEIVED_MESSAGE_FORMAT_WITH_T')
    def RECEIVED_MESSAGE_FORMAT_WITH_T(self):
        return self._RECEIVED_MESSAGE_FORMAT_WITH_T

    @RECEIVED_MESSAGE_FORMAT_WITH_T.setter
    def RECEIVED_MESSAGE_FORMAT_WITH_T(self, value):
        if isinstance(value, str):
            if isUniqueStrings(["[message]", "[translation]"], value) is False:
                value = "[message]([translation])"
            self._RECEIVED_MESSAGE_FORMAT_WITH_T = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('SEND_RECEIVED_MESSAGE_TO_VRC')
    def SEND_RECEIVED_MESSAGE_TO_VRC(self):
        return self._SEND_RECEIVED_MESSAGE_TO_VRC

    @SEND_RECEIVED_MESSAGE_TO_VRC.setter
    def SEND_RECEIVED_MESSAGE_TO_VRC(self, value):
        if isinstance(value, bool):
            self._SEND_RECEIVED_MESSAGE_TO_VRC = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('LOGGER_FEATURE')
    def LOGGER_FEATURE(self):
        return self._LOGGER_FEATURE

    @LOGGER_FEATURE.setter
    def LOGGER_FEATURE(self, value):
        if isinstance(value, bool):
            self._LOGGER_FEATURE = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    @property
    @json_serializable('VRC_MIC_MUTE_SYNC')
    def VRC_MIC_MUTE_SYNC(self):
        return self._VRC_MIC_MUTE_SYNC

    @VRC_MIC_MUTE_SYNC.setter
    def VRC_MIC_MUTE_SYNC(self, value):
        if isinstance(value, bool):
            self._VRC_MIC_MUTE_SYNC = value
            self.saveConfig(inspect.currentframe().f_code.co_name, value)

    def init_config(self):
        # Read Only
        self._VERSION = "2.2.5"
        if getattr(sys, 'frozen', False):
            self._PATH_LOCAL = os_path.dirname(sys.executable)
        else:
            self._PATH_LOCAL = os_path.dirname(os_path.abspath(__file__))
        self._PATH_CONFIG = os_path.join(self._PATH_LOCAL, "config.json")
        self._PATH_LOGS = os_path.join(self._PATH_LOCAL, "logs")
        os_makedirs(self._PATH_LOGS, exist_ok=True)
        self._GITHUB_URL = "https://api.github.com/repos/misyaguziya/VRCT/releases/latest"
        self._UPDATER_URL = "https://api.github.com/repos/misyaguziya/VRCT_updater/releases/latest"
        self._BOOTH_URL = "https://misyaguziya.booth.pm/"
        self._DOCUMENTS_URL = "https://mzsoftware.notion.site/VRCT-Documents-be79b7a165f64442ad8f326d86c22246"
        self._DEEPL_AUTH_KEY_PAGE_URL = "https://www.deepl.com/ja/account/summary"
        self._TRANSPARENCY_RANGE = (40, 100)
        self._UI_SCALING_RANGE = (40, 200)
        self._TEXTBOX_UI_SCALING_RANGE = (40, 200)
        self._MESSAGE_BOX_RATIO_RANGE = (1, 99)
        self._SELECTABLE_CTRANSLATE2_WEIGHT_TYPE_DICT = {
            "small": False,
            "large": False,
        }

        self._SELECTABLE_WHISPER_WEIGHT_TYPE_DICT = {
            "tiny": False,
            "base": False,
            "small": False,
            "medium": False,
            "large-v1": False,
            "large-v2": False,
            "large-v3": False,
        }

        self._MAX_MIC_THRESHOLD = 2000
        self._MAX_SPEAKER_THRESHOLD = 4000
        self._WATCHDOG_TIMEOUT = 60
        self._WATCHDOG_INTERVAL = 20

        # Read Write
        self._ENABLE_TRANSLATION = False
        self._ENABLE_TRANSCRIPTION_SEND = False
        self._ENABLE_TRANSCRIPTION_RECEIVE = False
        self._ENABLE_FOREGROUND = False
        self._ENABLE_CHECK_ENERGY_SEND = False
        self._ENABLE_CHECK_ENERGY_RECEIVE = False

        # Save Json Data
        ## Main Window
        self._SELECTED_TAB_NO = "1"
        self._SELECTED_TRANSLATION_ENGINES = {
            "1":"CTranslate2",
            "2":"CTranslate2",
            "3":"CTranslate2",
        }
        self._SELECTED_YOUR_LANGUAGES = {
            "1":{
                "primary":{
                    "language":"Japanese",
                    "country":"Japan"
                },
            },
            "2":{
                "primary":{
                    "language":"Japanese",
                    "country":"Japan"
                },
            },
            "3":{
                "primary":{
                    "language":"Japanese",
                    "country":"Japan"
                },
            },
        }
        self._SELECTED_TARGET_LANGUAGES = {
            "1":{
                "primary":{
                    "language":"English",
                    "country":"United States",
                },
                "secondary":{
                    "language":"English",
                    "country":"United States"
                },
                "tertiary":{
                    "language":"English",
                    "country":"United States"
                },
            },
            "2":{
                "primary":{
                    "language":"English",
                    "country":"United States",
                },
                "secondary":{
                    "language":"English",
                    "country":"United States"
                },
                "tertiary":{
                    "language":"English",
                    "country":"United States"
                },
            },
            "3":{
                "primary":{
                    "language":"English",
                    "country":"United States",
                },
                "secondary":{
                    "language":"English",
                    "country":"United States"
                },
                "tertiary":{
                    "language":"English",
                    "country":"United States"
                },
            },
        }
        self._SELECTED_TRANSCRIPTION_ENGINE = "Whisper"
        self._MULTI_LANGUAGE_TRANSLATION = False
        self._CONVERT_MESSAGE_TO_ROMAJI = False
        self._CONVERT_MESSAGE_TO_HIRAGANA = False
        self._MAIN_WINDOW_SIDEBAR_COMPACT_MODE = False

        ## Config Window
        self._TRANSPARENCY = 100
        self._UI_SCALING = 100
        self._TEXTBOX_UI_SCALING = 100
        self._MESSAGE_BOX_RATIO = 10
        self._FONT_FAMILY = "Yu Gothic UI"
        self._UI_LANGUAGE = "en"
        self._RESTORE_MAIN_WINDOW_GEOMETRY = True
        self._MAIN_WINDOW_GEOMETRY = {
            "x_pos": 0,
            "y_pos": 0,
            "width": 870,
            "height": 654,
        }
        self._AUTO_MIC_SELECT = False
        self._SELECTED_MIC_HOST = device_manager.getDefaultMicDevice()["host"]["name"]
        self._SELECTED_MIC_DEVICE = device_manager.getDefaultMicDevice()["device"]["name"]
        self._MIC_THRESHOLD = 300
        self._MIC_AUTOMATIC_THRESHOLD = False
        self._MIC_RECORD_TIMEOUT = 3
        self._MIC_PHRASE_TIMEOUT = 3
        self._MIC_MAX_PHRASES = 10
        self._MIC_WORD_FILTER = []
        self._MIC_AVG_LOGPROB = -0.8
        self._MIC_NO_SPEECH_PROB = 0.6
        self._AUTO_SPEAKER_SELECT = False
        self._SELECTED_SPEAKER_DEVICE = device_manager.getDefaultSpeakerDevice()["device"]["name"]
        self._SPEAKER_THRESHOLD = 300
        self._SPEAKER_AUTOMATIC_THRESHOLD = False
        self._SPEAKER_RECORD_TIMEOUT = 3
        self._SPEAKER_PHRASE_TIMEOUT = 3
        self._SPEAKER_MAX_PHRASES = 10
        self._SPEAKER_AVG_LOGPROB = -0.8
        self._SPEAKER_NO_SPEECH_PROB = 0.6
        self._OSC_IP_ADDRESS = "127.0.0.1"
        self._OSC_PORT = 9000
        self._AUTH_KEYS = {
            "DeepL_API": None,
        }
        self._USE_EXCLUDE_WORDS = True
        self._SELECTED_TRANSLATION_COMPUTE_DEVICE = {"device": "cpu", "device_index": 0, "device_name":"cpu"}
        self._SELECTED_TRANSCRIPTION_COMPUTE_DEVICE = {"device": "cpu", "device_index": 0, "device_name":"cpu"}
        self._CTRANSLATE2_WEIGHT_TYPE = "small"
        self._WHISPER_WEIGHT_TYPE = "base"
        self._SEND_MESSAGE_FORMAT = "[message]"
        self._SEND_MESSAGE_FORMAT_WITH_T = "[message]([translation])"
        self._RECEIVED_MESSAGE_FORMAT = "[message]"
        self._RECEIVED_MESSAGE_FORMAT_WITH_T = "[message]([translation])"
        self._AUTO_CLEAR_MESSAGE_BOX = True
        self._SEND_ONLY_TRANSLATED_MESSAGES = False
        self._SEND_MESSAGE_BUTTON_TYPE = "show"
        self._OVERLAY_SMALL_LOG = False
        self._OVERLAY_SMALL_LOG_SETTINGS = {
            "x_pos": 0.0,
            "y_pos": 0.0,
            "z_pos": 0.0,
            "x_rotation": 0.0,
            "y_rotation": 0.0,
            "z_rotation": 0.0,
            "display_duration": 5,
            "fadeout_duration": 2,
            "opacity": 1.0,
            "ui_scaling": 1.0,
        }
        self._SEND_MESSAGE_TO_VRC = True
        self._SEND_RECEIVED_MESSAGE_TO_VRC = False
        self._LOGGER_FEATURE = False
        self._VRC_MIC_MUTE_SYNC = False

    def load_config(self):
        if os_path.isfile(self.PATH_CONFIG) is not False:
            with open(self.PATH_CONFIG, 'r', encoding="utf-8") as fp:
                if fp.readable() and fp.seek(0, 2) > 0:
                    fp.seek(0)
                    self._config_data = json_load(fp)

                    for key, value in self._config_data.items():
                        setattr(self, key, value)

        with open(self.PATH_CONFIG, 'w', encoding="utf-8") as fp:
            for var_name, var_func in json_serializable_vars.items():
                self._config_data[var_name] = var_func(self)
            json_dump(self._config_data, fp, indent=4, ensure_ascii=False)

config = Config()