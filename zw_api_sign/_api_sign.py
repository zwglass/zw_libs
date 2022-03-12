import hashlib

# 生成 api 签名

class ApiSign:
    def __init__(self, app_key: str = '', app_secret: str = ''):
        self.app_key = app_key
        self.app_secret = app_secret

    def get_sign(self, user_token = "", **params):
        # user_token: 用户 token 参数 (可选)
        # params: request dict
        # 删除 sign
        if 'sign' in params:
            del params['sign']
        # 对参数进行排序
        params_list = sorted(params.items(), key=lambda item: item[0])
        # 拼接参数
        params_str = f"{self.app_secret}&{user_token}&"
        for item in params_list:
            params_str += '%s=%s&' % (item[0], item[1])
        # 去掉最后一个 &
        # params_str = params_str[:-1]
        # 拼接 app_secret
        # params_str = f"{self.app_secret}&{user_token}&{params_str}"
        print(params_str)
        # 计算签名
        sign = self.get_md5(params_str)
        return sign

    def get_md5(self, params_str):
        md5 = hashlib.md5()
        md5.update(params_str.encode('utf-8'))
        return md5.hexdigest()

    def validate_sign(self, user_token = "", **params) -> bool:
        # 验证 api 签名 是否正确
        # user_token: 用户 token 参数 (可选)
        # params: request dict
        
        # 删除 sign
        sign_value = params.get('sign', '')
        right_sign = self.get_sign(user_token, **params)
        return sign_value == right_sign
