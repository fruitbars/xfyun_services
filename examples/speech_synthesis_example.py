from xfyun_services.speech_synthesis import SpeechSynthesis
import os
from dotenv import load_dotenv

load_dotenv()

# 获取环境变量
app_id = os.getenv("APP_ID")
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# 多个文本的合成
texts_to_synthesize = [
    "这是第一个语音合成示例",
    "这是第二个语音合成示例",
    "这是第三个语音合成示例"
]

# 逐个处理文本
for i, text in enumerate(texts_to_synthesize):
    print(f"Synthesizing text {i + 1}: {text}")
    tts = SpeechSynthesis("wss://tts-api.xfyun.cn/v2/tts", app_id, api_key, api_secret, text)
    output_file = f"examples/output/output_{i + 1}.pcm"  # 自定义输出文件名
    tts.synthesize(output_file=output_file)  # 顺序执行
