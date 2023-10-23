# python 3.9没问题，最新Python不行
import requests
from bs4 import BeautifulSoup as BS     # require: lxml
import json
import pandas as pd     # require: openpyxl
import time
import random

# 话题id，可以直接从url看
topic_idx = "97018"
# 话题下帖子数量
cnt = 653

request_url = "https://m.douban.com/rexxar/api/v2/gallery/topic/" + topic_idx + "/items?from_web=1&sort=new&start={}&count=20&status_full_text=1&guest_only=0&ck="

def save_result(res):
    df = pd.DataFrame(res, columns=['user_id', 'user_ip_location', 'date&time', 'content', 'num_like', 'num_comment', 'num_share'])
    df.index += 1
    df.to_excel("result.xlsx")

def parse_article(html):
    bs = BS(html, 'lxml')
    texts = bs.find_all('script', type='application/ld+json')

    for text in texts:
        target = json.loads(text.string, strict=False)
        if 'text' in target:
            return target['text']

    for text in texts:
        target = json.loads(text.string, strict=False)
        if '@id' in target:
            return target['@id']

    print(texts)


def parse_target_normal(target):
    # 作者id
    res = [target['author']['name']]
    # 作者ip属地
    if target['author']['loc'] is None:
        res.append('NULL')
    else:
        res.append(target['author']['loc']['name'])
    # 发布时间
    res.append(target['create_time'])
    # 正文
    res.append(target['text'])
    # 喜欢数量
    res.append(target['like_count'])
    # 评论数量
    res.append(target['comments_count'])
    # 分享数量
    res.append(target['reshares_count'])

    return res


def parse_target_article(target):
    # 作者id
    res = [target['author']['name']]
    # 作者ip属地
    if target['author']['loc'] is None:
        res.append('NULL')
    else:
        res.append(target['author']['loc']['name'])
    # 发布时间
    res.append(target['create_time'])
    # 正文
    url = target['url']
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0"}
    response = requests.get(url, headers=headers)
    text = response.text
    res.append(parse_article(text))
    # 喜欢数量
    res.append(target['likers_count'])
    # 评论数量
    res.append(target['comments_count'])
    # 分享数量
    res.append(target['reshares_count'])

    return res


def parse_target(target):
    if 'status' in target:
        return parse_target_normal(target['status'])
    else:
        return parse_target_article(target)

def main():
    all_res = []
    # 1853
    time.sleep(random.uniform(1, 10))
    for i in range(0, cnt, 20):
        base_url = request_url.format(i)
        headers = {
            'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
            'Referer': 'https://www.douban.com/gallery/topic/97018/?sort=new'}
        response = requests.get(base_url, headers=headers)
        targets = response.json()['items']
        for target in targets:
            all_res.append(parse_target(target['target']))
    save_result(all_res)



if __name__ == '__main__':
    main()
