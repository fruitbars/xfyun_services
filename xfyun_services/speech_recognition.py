# speech_recognition.py
import websocket
import json
import base64
import threading
import ssl
import time
from xfyun_services.utils import create_url


class SpeechRecognition:
    def __init__(self, server_url, app_id, api_key, api_secret, audio_file, callback=None):
        """初始化语音听写服务"""
        self.server_url = server_url
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.audio_file = audio_file
        self.callback = callback  # 添加回调函数

        self.common_args = {"app_id": self.app_id}
        self.business_args = {
            "domain": "iat",  # 语音听写领域
            "language": "zh_cn",  # 语言
            "accent": "mandarin",  # 方言
            "vinfo": 1,  # 是否返回音频信息
            "vad_eos": 10000  # 结束条件
        }

    def on_message(self, ws, message):
        """处理接收到的语音识别消息"""
        try:
            result = json.loads(message)
            if result["code"] != 0:
                print(f"Error: {result['message']}")
            else:
                # 提取识别文本
                ws_result = result["data"]["result"]["ws"]
                text = "".join([word["cw"][0]["w"] for word in ws_result if "cw" in word])

                # 如果提供了回调函数，就调用它
                if self.callback:
                    self.callback(text)
        except Exception as e:
            print(f"Error in processing message: {e}")

    def on_error(self, ws, error):
        """WebSocket 错误处理"""
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """WebSocket 关闭处理"""
        #print(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")
        pass

    def on_open(self, ws):
        """WebSocket 连接建立后执行"""

        def run(*args):
            frame_size = 8000  # 每一帧的音频大小
            interval = 0.04  # 每帧音频的间隔时间
            status = 0  # 初始状态

            with open(self.audio_file, "rb") as fp:
                while True:
                    buf = fp.read(frame_size)
                    if not buf:
                        status = 2  # 最后一帧
                    if status == 0:
                        # 第一帧
                        data = {
                            "common": self.common_args,
                            "business": self.business_args,
                            "data": {
                                "status": 0,
                                "format": "audio/L16;rate=16000",
                                "audio": str(base64.b64encode(buf), 'utf-8'),
                                "encoding": "raw"
                            }
                        }
                        ws.send(json.dumps(data))
                        status = 1  # 进入中间帧
                    elif status == 1:
                        # 中间帧
                        data = {
                            "data": {
                                "status": 1,
                                "format": "audio/L16;rate=16000",
                                "audio": str(base64.b64encode(buf), 'utf-8'),
                                "encoding": "raw"
                            }
                        }
                        ws.send(json.dumps(data))
                    elif status == 2:
                        # 最后一帧
                        data = {
                            "data": {
                                "status": 2,
                                "format": "audio/L16;rate=16000",
                                "audio": str(base64.b64encode(buf), 'utf-8'),
                                "encoding": "raw"
                            }
                        }
                        ws.send(json.dumps(data))
                        time.sleep(1)
                        break
                    time.sleep(interval)

            ws.close()

        threading.Thread(target=run).start()

    def recognize_audio(self):
        """启动语音识别流程"""
        ws_url = create_url(self.server_url, self.api_key, self.api_secret)
        ws = websocket.WebSocketApp(ws_url, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

