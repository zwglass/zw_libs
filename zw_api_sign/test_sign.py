from _api_sign import ApiSign

# 测试 api 签名

if __name__ == '__main__':
    params = {
        'app_key': 'asdfasdfasdfasdf',
        'app_secret': 'ssdfaffsdfasdf',
        'timestamp': '123456677',
        'nonce': 9,
        'sign': '141eaa25e6cc59e161a7f109f53856ff',
    }
    api_sign = ApiSign()
    sign = api_sign.get_sign(**params)
    valid_sign = api_sign.validate_sign(**params)
    print(sign)
    print(valid_sign)
