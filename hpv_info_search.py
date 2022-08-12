import requests
import json

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Host': 'Host: wxapidg.bendibao.com',
    'content-type': 'application/json',
    'Referer':
    'https://servicewechat.com/wx2efc0705600eb6db/130/page-frame.html'
}


def get_latest_info():
    info_url = r'https://wxapidg.bendibao.com/smartprogram/zhuanti.php?platform=wx&version=21.12.06&action=jiujia&citycode=cd'
    response = requests.get(url=info_url, headers=headers)
    places = json.loads(response.text).get('data').get('website').get('place')
    infos = []
    for place in places:
        infos.append({
            'id': place.get('id'),
            'city': place.get('cityname'),
            'location': place.get('name'),
            'number': place.get('minge'),
            'time': place.get('yy_time'),
            'platform': place.get('platform'),
            'method': place.get('method')
        })
    return infos


def push_wechat(infos):
    Thm_key = 'SCT165093T1jxRYxH3zaIHAK1SNiWYgBKP'
    Hxy_key = 'SCT165102TjqmfaAWX6rhUUxtQ0wqDmP6B'
    push_url = 'https://sc.ftqq.com/{key}.send'
    desp = ''
    desp += '| 地址 | 时间 | 数量 | 抢票方法 | 抢票平台 |\n'
    desp += '| :-: | :-: | :-: | :-: | :-: |\n'

    for info in infos:
        if not info['city'] == '成都':
            continue
        desp += '| ' + info['location'] + ' | ' + info['time'] + ' | ' + info[
            'number'] + ' | ' + info['method'] + ' | ' + info[
                'platform'] + ' |\n'
    data = {'title': 'hpv查询结果', 'channel': 9, 'desp': desp}
    requests.post(url=push_url.format(key=Thm_key), data=data)
    requests.post(url=push_url.format(key=Hxy_key), data=data)


if __name__ == '__main__':
    infos = get_latest_info()
    push_wechat(infos=infos)