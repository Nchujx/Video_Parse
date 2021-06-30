import time
import requests
import re
from hashlib import md5
import json


class YouKu:
    def __init__(self, url,cookie):
        self.url = "https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/"
        self.int_time = int(time.time()) * 1000
        # self.vid = "XNTQwMTgxMTE2"
        self.video_url = url
        # 用于存储show_id,videoId
        self.params = {}
        self.get_current_showid()
        self.cookie = cookie
        self.language = {
            "ja": "日语",
            "guoyu": "国语",
            "default": "默认",
            "yue": "粤语",
        }

    def get_current_showid(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        }
        res = requests.get(self.video_url, headers=headers).text
        current_showid = re.findall("showid: '(\d+)'", res)[0]

        video_id = re.findall("videoId: '(\d+)'", res)[0]

        self.params = {"show_id": current_showid, "videoId": video_id}

    def get_steal_params(self):
        return json.dumps({
            # 0502
            "ccode": "0502",
            "client_ip": "",
            "utid": re.findall("cna=(.*?);", self.cookie)[0],
            "client_ts": self.int_time,
            "version": "",
            "ckey": "DIl58SLFxFNndSV1GFNnMQVYkx1PP5tKe1siZu/86PR1u/Wh1Ptd+WOZsHHWxysSfAOhNJpdVWsdVJNsfJ8Sxd8WKVvNfAS8aS8fAOzYARzPyPc3JvtnPHjTdKfESTdnuTW6ZPvk2pNDh4uFzotgdMEFkzQ5wZVXl2Pf1/Y6hLK0OnCNxBj3+nb0v72gZ6b0td+WOZsHHWxysSo/0y9D2K42SaB8Y/+aD2K42SaB8Y/+ahU+WOZsHcrxysooUeND",
        })

    def get_biz_params(self):
        return json.dumps({
            "vid": re.findall("id_(.*?).html", self.video_url)[0],
            "play_ability": "",  # 写死在js里的
            "current_showid": '',
            "preferClarity": "",  # 貌似是清晰度
            "extag": "",  # 写死在js里的
            "master_m3u8": "",
            "media_type": "standard,subtitle",
            "app_ver": "",
            "drm_type": "",
            "key_index": "",

        })

    def get_ad_params(self):
        return json.dumps({
            "vs": "",
            "pver": "",
            "sver": "",
            "site": '',
            "aw": "",
            "fu": '',
            "d": "",
            "bt": "",
            "os": "",
            "osv": "",
            "dq": "",
            "atm": "",
            "partnerid": "",
            "wintype": "",
            "isvert": '',
            "vip": '',
            "p": '',
            "rst": "",
            "needbf": '',
            "avs": "",
        })

    def get_data(self):
        return json.dumps({"steal_params": self.get_steal_params(), "biz_params": self.get_biz_params(),
                           "ad_params": self.get_ad_params()})

    def join_params(self):
        data = self.get_data()
        return {
            'jsv': '',
            'appKey': '24679788',
            't': self.int_time,
            # 4272cb703bb9ac93f663288a6049b3e9_1622870089041
            'sign': md5(str(
                re.findall("m_h5_tk=(.*?)_", self.cookie)[0] + "&" + str(self.int_time) + "&" + "24679788" + "&" + str(data)).encode("utf8")).hexdigest(),
            'api': '',
            'v': '',
            'timeout': '',
            'YKPid': '',
            'YKLoginRequest': '',
            'AntiFlood': '',
            'AntiCreep': 'true',
            'type': 'jsonp',
            'dataType': 'jsonp',
            'callback': 'mtopjsonp3',
            "data": f"{data}"
        }

    def loads_jsonp(self, _jsonp):
        try:
            return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
        except:
            raise ValueError('Invalid Input')

    def start(self):
        headers = {
            "Accept": "*/*",
            "Host": "acs.youku.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "cookie": self.cookie,
            "Referer": "https://v.youku.com/"
        }
        res = requests.get(self.url, params=self.join_params(), headers=headers).text

        res = re.findall('mtopjsonp3\((.+)\)',res)[0]
        res = json.loads(res)
        print(res)
        return res

def getinfos(data):
    streams = data['data']['data']['stream']
    for stream in streams:
        info = {
            'title':data['data']['data']['video']['title'],
            'size':str(int(stream['size']/1024/1024)) + 'MB',
            'drm_type':stream['drm_type'],
            'stream_type':stream['stream_type'],
            'height*width':str(stream['height'])+'*'+str(stream['width']),
            'm3u8_url':stream['m3u8_url']
        }
        print(info)



if __name__ == '__main__':
    url = 'https://v.youku.com/v_show/id_XNTE2NjI1MDk0MA==.html?s=8d5eb13883e1414da52b&scm=20140719.manual.15358.show_8d5eb13883e1414da52b&spm=a2ha1.14919748_WEBMOVIE_JINGXUAN.drawer2.d_zj1_5&s=8d5eb13883e1414da52b'
    cookie = 'P_F=1; P_T=1624445757; cna=XbNoGOgnbwACATs0NKRwGTBX; __ysuid=1608772594241pxk; juid=01er1a6dmu64u; P_gck=NA%7CQ1MQJm6CmtdiC%2FA17lfCmw%3D%3D%7CNA%7C1618643265511; P_pck_rm=snxu%2B2gs24961539fbbaf7ZBIKrrfsJvtIYvffdH5lyfHbl2WJliDS39%2FqZxaINjX8MaWSq0zqqWp9LfvkZs3Rzesq5lSGVMz%2F46YauoVJ0XyL1FrRPSkBSvlV4B0VnljkGI37kLZDlGmbva%2F66Wtol4nl4v3800PH1q7w%3D%3D%5FV2; disrd=47244; youku_history_word=%5B%22%25E4%25B8%2583%25E5%2589%2591%22%2C%22%25E9%2592%25A2%25E9%2593%2581%25E4%25BE%25A0%22%2C%22%25E7%2599%25BD%25E9%25B9%25BF%25E5%258E%259F%25E7%2594%25B5%25E8%25A7%2586%25E5%2589%25A7%22%2C%22%25E8%259C%2598%25E8%259B%259B%25E4%25BE%25A0%22%2C%22%25E8%258B%25B1%25E9%259B%2584%25E8%25BF%259C%25E5%25BE%2581%22%5D; _m_h5_tk=30e3809bcc805eb549be326698b8fdb3_1624442851234; _m_h5_tk_enc=d9295a717b57f500f63a429a51e6923e; __ayft=1624438533134; __aysid=16244385331346Jg; __ayscnt=1; P_ck_ctl=F819022C2FC93F93A016B6E7A5BF251B; xlly_s=1; __arpvid=1624438542036vmK0lF-1624438542101; __arycid=dd-3-00; __arcms=dd-3-00; __aypstp=2; __ayspstp=2; modalFrequency={"UUID":"2"}; redMarkRead=1; __ayvstp=3; __aysvstp=3; l=eBE7hArHO5WFXs1QBOfwnurza77ttIRAguPzaNbMiOCPOh1w54uAW69qVtLeCnGVh6KJR3Wpo6PMBeYBqhbYXeQ2Z4JM9BHmn; tfstk=c34PB70tHaQPwn0CX4geOpcyrPvRZUHnCElZqoanZCU5kDnligvKis9KgXJYH0f..; isg=BKioANPQXJlpOE8s_sl7kqOHeZa60QzbD1qNd2LZsiMWvUgnCuVFaVD3sVVNjcSz'
    data = YouKu(url=url, cookie=cookie).start()
    try:
        getinfos(data)
    except:
        print(data)

