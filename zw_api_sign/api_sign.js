// import MD5 from "crypto-js/md5";

// 签名 npm install crypto-js
const MD5 = require("crypto-js/md5");

let api_sign = (token = '', data = {}) => {
    const appSecret = ''
    let sign = `${appSecret}&${token}&`;
    let keys = Object.keys(data);
    keys.sort();
    for (let i = 0; i < keys.length; i++) {
        let key = keys[i];
        if (key === 'sign') {
            continue;
        }
        sign += `${key}=${data[key]}&`;
    }
    console.log(sign);
    return MD5(sign).toString();
}

let testResult = api_sign('', {'app_key': 'asdfasdfasdfasdf',
        'app_secret': 'ssdfaffsdfasdf',
        'timestamp': '123456677',
        'nonce': 9,
        'sign': '141eaa25e6cc59e161a7f109f53856ff',
    });
console.log(testResult);

// export { api_sign };
