# xfyun_services

`xfyun_services` 是一个 Python 库，旨在简化调用讯飞开放平台的 API。该库目前支持翻译、语音识别、听写等功能，并提供简单易用的接口，帮助开发者快速集成这些服务。

## 功能

- **机器翻译**：支持中文与其他语言的互译，涵盖多种语言。
- **语音识别**：将音频文件转换为文本。
- **听写**：实时语音识别，支持实时转换语音为文本。
- **更多功能**：未来会支持更多的 API 能力，如情感分析、语言检测等。

## 安装

使用 `Poetry` 进行依赖管理和包管理：

1. 安装 [Poetry](https://python-poetry.org/docs/#installation)：

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. 克隆仓库并安装依赖：

    ```bash
    git clone https://github.com/your-username/xfyun_services.git
    cd xfyun_services
    poetry install
    ```

## 配置

1. 创建一个 `.env` 文件，在其中设置讯飞开放平台的 API 密钥：

    ```text
    APP_ID=your_app_id
    API_KEY=your_api_key
    API_SECRET=your_api_secret
    ```

2. 如果你还没有 API 密钥，请访问 [讯飞开放平台](https://www.xfyun.cn/) 注册并获取 `APP_ID`、`API_KEY` 和 `API_SECRET`。

## 使用示例

### 机器翻译

以下是如何使用翻译功能的示例代码：

```python
from xfyun_services.translation import TranslationService
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取环境变量
app_id = os.getenv("APP_ID")
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

# 初始化翻译服务
translator = TranslationService(app_id, api_key, api_secret)

# 翻译文本
text = "科大讯飞"
translated_text = translator.translate(text, from_lang="cn", to_lang="en")

# 输出翻译结果
print(f"Original Text: {text}")
print(f"Translated Text: {translated_text}")
