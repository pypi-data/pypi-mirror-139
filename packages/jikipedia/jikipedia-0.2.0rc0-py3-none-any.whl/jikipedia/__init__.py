import requests
import json
import execjs
import base64


class Jikipedia:
    # 获取 用户基础信息
    def __init__(self, phone: str, password: str):
        self.phone = phone
        self.password = password
        if len(phone) != 11:
            raise ValueError('手机号码长度不正确')

    # 生成 明文XID
    def generate_plaintext_xid(self):
        js = """
        function get_xid() {
            const xid = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,
            (function (name) {
              let randomInt = 16 * Math.random() | 0;
              return ("x" === name ? randomInt : 3 & randomInt | 8).toString(16)
            }));
            return xid;
        }
        """
        xid = execjs.compile(js)
        return xid.call('get_xid')

    # 加密 明文XID
    def encode_xid(self, xid=None):
        if xid is None:
            xid = self.generate_plaintext_xid()
        xid = base64.encodebytes(("jikipedia_xid_" + xid).encode('utf-8'))
        return str(xid.decode('utf-8')).strip('\n')

    # 模拟登录获取更多信息
    def login(self):
        data = {
            'password': self.password,
            'phone': self.phone
        }
        data = json.dumps(data)
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'no-cache',
            'Client': 'web',
            'Client-Version': '2.6.12k',
            'Connection': 'keep-alive',
            'Content-Length': '48',
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'api.jikipedia.com',
            'Origin': 'https://jikipedia.com',
            'Pragma': 'no-cache',
            'Referer': 'https://jikipedia.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
            'XID': self.encode_xid()
        }
        r = requests.post('https://api.jikipedia.com/wiki/phone_password_login',
                          data=data,
                          headers=header)
        if r.status_code == 412:
            raise ValueError('手机号码或密码错误')
        return json.loads(r.text)

    # 获取 Token
    def get_token(self):
        return self.login()['token']

    # 获取 搜索栏的推荐
    def get_search_recommend(self):
        s = requests.get('https://api.jikipedia.com/wiki/request_search_placeholder').text
        s = json.loads(s)
        return s

    # 调用 恶魔鸡翻译器
    def emoji(self, text):
        data = {
            'content': str(text)
        }
        data = json.dumps(data)
        head = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}
        r_p = requests.post(url='https://api.jikipedia.com/go/translate_plaintext', data=data, headers=head)
        return json.loads(r_p.text)['translation']

    # 进行 对词条 （取消）点赞
    def like(self, id, status=True):
        data = {
            'id': id,
            'status': status
        }
        data = json.dumps(data)
        header = {
            'Token': self.get_token(),
            'XID': self.encode_xid()
        }
        r = requests.post('https://api.jikipedia.com/wiki/like', data=data, headers=header)
        return r.status_code
