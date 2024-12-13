# examples/translation_example.py

from xfyun_services.translation import TranslationService
import os
from dotenv import load_dotenv

# 从 .env 文件中加载 API 密钥和其他配置
load_dotenv()

# 获取环境变量
app_id = os.getenv("APP_ID")
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

if not app_id or not api_key or not api_secret:
    raise ValueError("请在 .env 文件中设置 APP_ID, API_KEY, API_SECRET")

# 初始化翻译服务
translator = TranslationService(app_id, api_key, api_secret)

# 翻译文本
text = "科大讯飞"
translated_text = translator.translate(text, from_lang="cn", to_lang="en")

# 输出翻译结果
print(f"Original Text: {text}")
print(f"Translated Text: {translated_text}")
