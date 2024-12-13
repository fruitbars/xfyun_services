import hashlib
import base64
import hmac
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
from urllib.parse import urlencode, urlparse


def sha256base64(data):
    """计算 sha256 哈希并进行 base64 编码"""
    sha256 = hashlib.sha256()
    sha256.update(data)
    return base64.b64encode(sha256.digest()).decode('utf-8')


def get_current_timestamp():
    """获取当前时间戳"""
    return int(mktime(datetime.now().timetuple()))


def parse_url(url):
    """解析 URL，提取主机和路径"""
    stidx = url.index("://")
    host = url[stidx + 3:]
    schema = url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise Exception(f"Invalid request URL: {url}")
    path = host[edidx:]
    host = host[:edidx]
    return host, path


def assemble_url(url, app_id, api_key, api_secret, method="POST"):
    """构建并签名请求 URL"""
    host, path = parse_url(url)
    timestamp = get_current_timestamp()

    # 生成 HMAC 签名
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))

    signature_origin = f"host: {host}\ndate: {date}\n{method} {path} HTTP/1.1"
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode('utf-8')

    # 创建 Authorization 字段
    authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')

    # 拼接 URL 和请求参数
    request_url = f"{url}?{urlencode({'host': host, 'date': date, 'authorization': authorization, 'timestamp': str(timestamp)})}"

    return request_url


def create_url(url,  api_key, api_secret):
    """通用的创建WebSocket请求URL方法"""

    # 从url中提取api_host
    parsed_url = urlparse(url)
    api_host = parsed_url.hostname  # 提取域名部分

    # 生成RFC1123格式的时间戳
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))

    # 拼接签名原始字符串
    signature_origin = f"host: {api_host}\n"
    signature_origin += f"date: {date}\n"
    signature_origin += f"GET {parsed_url.path} HTTP/1.1"

    # 使用HMAC-SHA256进行加密
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

    # 生成Authorization
    authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

    # 拼接WebSocket请求URL
    v = {
        "authorization": authorization,
        "date": date,
        "host": api_host
    }

    return url + '?' + urlencode(v)