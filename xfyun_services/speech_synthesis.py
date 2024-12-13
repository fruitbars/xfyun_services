import websocket
import json
import base64
import os
from xfyun_services.utils import create_url


class SpeechSynthesis:
    def __init__(self, server_url, app_id, api_key, api_secret, text, callback=None):
        """初始化语音合成服务"""
        self.server_url = server_url
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.text = text
        self.callback = callback  # 回调函数

        self.common_args = {"app_id": self.app_id}
        self.business_args = {
            "aue": "raw",  # 音频格式
            "auf": "audio/L16;rate=16000",  # 音频编码
            "vcn": "xiaoyan",  # 发音人
            "tte": "utf8"  # 文本编码
        }

    def on_message(self, websocket, message, output_file):
        """接收到 WebSocket 消息"""
        print("on_message triggered")
        try:
            message = json.loads(message)
            print(f"Received message: {message}")  # 打印收到的消息
            code = message["code"]
            sid = message["sid"]
            audio = message["data"]["audio"]
            audio = base64.b64decode(audio)
            status = message["data"]["status"]

            if status == 2:  # 结束标识
                print("WebSocket closed.")
                websocket.close()

            if code != 0:
                errMsg = message["message"]
                print(f"sid:{sid} call error:{errMsg} code is:{code}")
            else:
                # 如果有回调函数，实时发送音频数据
                if self.callback:
                    self.callback(audio)  # 调用回调函数，传递音频数据

                # 继续保存文件
                with open(output_file, 'ab') as f:
                    f.write(audio)
                print(f"Audio saved to {output_file}")  # 打印文件保存的信息
        except Exception as e:
            print("Error in parsing message:", e)

    def on_error(self, websocket, error):
        """WebSocket 错误处理"""
        print("### Error:", error)

    def on_close(self, websocket, close_status_code, close_msg):
        """WebSocket 关闭处理"""
        print("### WebSocket Closed ###")
        print(f"Close status code: {close_status_code}, Close message: {close_msg}")

    def synthesize_text(self, websocket, output_file):
        """发送文本进行语音合成"""
        self.data = {
            "status": 2,  # 合成结束
            "text": str(base64.b64encode(self.text.encode('utf-8')), "UTF8")
        }

        payload = {
            "common": self.common_args,
            "business": self.business_args,
            "data": self.data,
        }
        payload = json.dumps(payload)
        print("Sending text for synthesis...")
        websocket.send(payload)
        print("Text sent.")
        if os.path.exists(output_file):
            os.remove(output_file)

    def synthesize(self, output_file='./output.pcm'):
        """合成单个文本"""
        ws_url = create_url(self.server_url, self.api_key, self.api_secret)
        print(f"Generated WebSocket URL: {ws_url}")  # 打印生成的 URL

        # 使用同步的 websocket-client 进行连接
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(ws_url,
                                    on_message=lambda ws, msg: self.on_message(ws, msg, output_file),
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        print("WebSocket connected.")
        ws.on_open = lambda ws: self.synthesize_text(ws, output_file)
        ws.run_forever()  # 阻塞直到 WebSocket 连接关闭
