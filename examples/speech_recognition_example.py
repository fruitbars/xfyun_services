# examples/speech_recognition_example.py
import os
from dotenv import load_dotenv
from xfyun_services.speech_recognition import SpeechRecognition

load_dotenv()

# 获取环境变量
app_id = os.getenv("APP_ID")
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# 音频文件路径
audio_file = "examples/input/iat_pcm_16k.pcm"


# 定义回调函数
def on_recognition_result(text):
    """处理识别结果"""
    print(f"Recognized text: {text}")


# 初始化并启动语音识别
recognizer = SpeechRecognition(
    "wss://iat-api.xfyun.cn/v2/iat",
    app_id,
    api_key,
    api_secret,
    audio_file,
    callback=on_recognition_result  # 传入回调函数
)
recognizer.recognize_audio()
