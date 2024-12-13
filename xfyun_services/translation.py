import base64
import json
import requests
from .utils import assemble_url


class TranslationService:
    def __init__(self, app_id, api_key, api_secret, res_id=None):
        """初始化翻译服务"""
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.res_id = res_id or "its_en_cn_word"  # 默认术语资源ID

    def translate(self, text, from_lang="cn", to_lang="en"):
        """执行翻译操作"""
        url = 'https://itrans.xf-yun.com/v1/its'
        body = {
            "header": {
                "app_id": self.app_id,
                "status": 3,
                "res_id": self.res_id
            },
            "parameter": {
                "its": {
                    "from": from_lang,
                    "to": to_lang,
                    "result": {}
                }
            },
            "payload": {
                "input_data": {
                    "encoding": "utf8",
                    "status": 3,
                    "text": base64.b64encode(text.encode("utf-8")).decode('utf-8')
                }
            }
        }

        # 使用 utils 中的 assemble_url 方法
        request_url = assemble_url(url, self.app_id, self.api_key, self.api_secret, method="POST")
        headers = {
            "X-Appid": self.app_id,
            "Content-Type": "application/json",
            "Host": "itrans.xf-yun.com"
        }

        response = requests.post(request_url, data=json.dumps(body), headers=headers)

        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}, content: {response.content.decode()}")

        result = json.loads(response.content.decode())
        translated_text = base64.b64decode(result['payload']['result']['text']).decode()
        return translated_text
