import unittest
import os
from dotenv import load_dotenv
from xfyun_services.translation import TranslationService


class TestTranslationService(unittest.TestCase):
    def setUp(self):
        """测试前的初始化"""
        # 加载 .env 文件中的环境变量
        load_dotenv()  # 默认会读取项目根目录下的 .env 文件

        # 从环境变量中读取配置信息
        self.app_id = os.getenv("APP_ID")
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")

        if not self.app_id or not self.api_key or not self.api_secret:
            raise ValueError("请在 .env 文件中设置 APP_ID, API_KEY, API_SECRET")

        self.service = TranslationService(self.app_id, self.api_key, self.api_secret)

    def test_translation(self):
        """测试翻译功能"""
        text_to_translate = "科大讯飞"
        translated_text = self.service.translate(text_to_translate, from_lang="cn", to_lang="en")
        self.assertIsInstance(translated_text, str)  # 检查返回值类型
        self.assertNotEqual(translated_text, text_to_translate)  # 确保翻译后的文本不等于原始文本

    def test_translation_invalid_input(self):
        """测试无效输入"""
        with self.assertRaises(Exception):  # 如果发生异常，测试通过
            self.service.translate("", from_lang="cn", to_lang="en")


if __name__ == "__main__":
    unittest.main()
