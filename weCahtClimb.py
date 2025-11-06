import datetime
import hashlib
import json
import os
import random
import sys
import time

from curl_cffi import requests


def printf(text):
    ti = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print(f'[{ti}]: {text}')
    sys.stdout.flush()


def getFileContent(path):
    if os.path.exists(path) and os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    else:
        raise Exception(f'无法找到文件：{path}')


def generate_random_str(randomlength=16):
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str


def md5(content):
    md = hashlib.md5()
    md.update(content.encode())
    return md.hexdigest()


def getNowTimeStr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def getTimestamp():
    return str(round(time.time() * 1000))





def main():
    try:
        ip_address = '123.110.' + str(random.randint(1, 254)) + '.' + str(random.randint(1, 254))
        url = f'{host}/tfcopr/gamedoubleninth/initgame?session_id={session_id}&csrf_token={csrf_token}'
        ua = "Mozilla/5.0 (Linux; Android 10; CDY-AN90 Build/HUAWEICDY-AN90; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2691 MMWEBSDK/200801 Mobile Safari/537.36 MMWEBID/4006 MicroMessenger/7.0.18.1740(0x2700123B) Process/toolsmp WeChat/arm64 NetType/4G Language/zh_CN ABI/arm64"
        headers = {
            "Referer": 'https://gtimg.wechatpay.cn/',
            "User-Agent": ua,
            "wepaytest-proxyip": "1127643299",
            'X-Forwarded-For': ip_address,
            'X-Real-IP': ip_address
        }
        data = {"act_id": "1005"}
        res = requests.post(url=url, json=data, headers=headers, timeout=5)
        printf(f'{res.text}')
        js = json.loads(res.text)

        data = {"act_id":"1005"}
        url = f'{host}/tfcopr/activity/startuseractivity?session_id={session_id}&csrf_token={csrf_token}'
        res = requests.post(url=url, json=data, headers=headers, timeout=5)
        printf(f'{res.text}')

        user_game_double_ninth = js['data']['user_game_double_ninth']
        game_id = user_game_double_ninth['game_id']
        game_script = user_game_double_ninth['game_script']
        game_map = game_script['game_map']
        map_len = game_map['map_len']
        point_item_list = game_map['point_item_list']
        score_recore_list = []
        sumScore = 0
        sumLeng = 0
        for point_item in point_item_list:
            prop_type = point_item['prop_type']
            if prop_type == 'PROP_TYPE_EMPTY':
                continue
            prop_id = point_item['prop_id']
            score = point_item['score']
            score_recore = {"score": score, "fetch_time": round(time.time())}
            score_recore_list.append(score_recore)
            sumScore += score
            sumLeng+=1
            #time.sleep(0.08)
        printf(f'预测得分：{sumScore}')
        data = {"game_id": game_id,
                "game_report_info": {"total_score": sumScore, "total_prop_count": len(score_recore_list),
                                     "score_recore_list": score_recore_list},
                "display_info": "{\"couplet\":[\"菊香盈袖里\",\"和气满堂间\"]}"}
        url = f'{host}/tfcopr/gamedoubleninth/reportresult?session_id={session_id}&csrf_token={csrf_token}'
        res = requests.post(url=url, json=data, headers=headers, timeout=5)
        printf(f'{res.text}')
        js = json.loads(res.text)
        score = js['data']['user_game_double_ninth']['score']
        printf(f'得分：{score}')
    except Exception as e:
        printf(f'运行报错：{e}')


if __name__ == '__main__':

    host = 'https://action.weixin.qq.com'
    session_id = 'i_ZYnsEcbUaMa2earpiwY6OL01zO'
    csrf_token = 'MjG05xmmW28xCoUz'
    while True:
        main()
