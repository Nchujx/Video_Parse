import requests
import time
import re
import execjs
from urllib.parse import quote
import json
import logging

class tencent:
    def __init__(self, url,cookie):
        self.url = url
        self.cookie = cookie
        self.headers = {
            'Cookie':cookie,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36¬"
        }
        self.int_time = int(time.time())
        self.cookie_dict = {}
        self.parse_cookie()
        self.platform = '10901'

    def parse_cookie(self):
        if self.cookie:
            for i in self.cookie.split(";"):
                kv = i.split("=")
                self.cookie_dict[kv[0].strip()] = kv[1]

    def get_vid_coverid(self):
        vid = 'm0030872c5z'
        coverid = 'wzx7pbebgpxlqqr'
        # response = requests.get(url=url).text
        # vid = re.findall('vid=(.+?)&', response)[1]
        # coverid = re.findall('"cover_id":"(.+?)"',response)[0]
        return vid,coverid

    def get_adparams(self):
        pf = ""
        ad_type = ""
        pf_ex = ""
        url = ""
        refer = ""
        ty = ""
        plugin = ""
        v = ""
        vid,coverid = self.get_vid_coverid()
        pt = ""
        flowid = f"3c0feb2957e78d96c93a87023a4d0f7a_{self.platform}"
        vptag = ""
        pu = ""
        chid = ""
        adaptor = ""
        dtype = ""
        live = ""
        resp_type = ""
        guid = ""
        req_type = ''
        appversion = ""
        uid = self.cookie_dict['vqq_vuserid']
        tkn = self.cookie_dict['vqq_vusession']
        lt = ""
        platform = self.platform
        opid = self.cookie_dict['vqq_openid']
        atkn = self.cookie_dict['vqq_access_token']
        appid = self.cookie_dict['vqq_appid']
        tpid = ""
        result = f"pf={pf}&ad_type={ad_type}&pf_ex={pf_ex}&url={url}&refer={refer}&ty={ty}&plugin={plugin}&v={v}&coverid={coverid}&vid={vid}&pt={pt}&flowid={flowid}&vptag={vptag}&pu={pu}&chid={chid}&adaptor={adaptor}&dtype={dtype}&live={live}&resp_type={resp_type}&guid={guid}&req_type={req_type}&from=0&appversion={appversion}&uid={uid}&tkn={tkn}&lt={lt}&platform={platform}&opid={opid}&atkn={atkn}&appid={appid}&tpid={tpid}"
        return result

    def get_vinfoparams(self):
        spsrt = ""
        charge = ""
        defaultfmt = ""
        otype = "ojson"
        guid = ""
        # 随机数 + platform
        flowid = f"3c0feb2957e78d96c93a87023a4d0f7a_{self.platform}"
        platform = self.platform
        sdtfrom = ""
        defnpayver = ""
        appVer = "3.5.57"
        host = ""
        ehost = quote(self.url)
        refer = ""
        sphttps = ""
        tm = self.int_time
        spwm = ""
        logintoken = quote(str({"main_login": self.cookie_dict['main_login'], "openid": self.cookie_dict['vqq_openid'],
                                "appid": self.cookie_dict['vqq_appid'],
                                "access_token": self.cookie_dict['vqq_access_token'],
                                "vuserid": self.cookie_dict['vqq_vuserid'],
                                "vusession": self.cookie_dict['vqq_vusession']}))
        vid,coverid = self.get_vid_coverid()
        defn = "fhd"
        fhdswitch = ""
        show1080p = ""
        isHLS = ""
        dtype = "3"
        sphls = "2"
        spgzip = ""
        dlver = ""
        drm = ""
        hdcp = ""
        spau = ""
        spaudio = ""
        defsrc = ""
        encryptVer = "9.1"
        cKey = self.get_cKey(platform, appVer, vid, guid, tm)
        # print('cKey:',cKey)
        fp2p = ""
        spadseg = ""
        # result = f"spsrt={spsrt}&charge={charge}&defaultfmt={defaultfmt}&otype={otype}&guid={guid}&flowid={flowid}&platform={platform}&sdtfrom={sdtfrom}&defnpayver={defnpayver}&appVer={appVer}&host={host}&ehost={ehost}&refer={refer}&sphttps={sphttps}&tm={tm}&spwm={spwm}&logintoken={logintoken}&vid={vid}&defn={defn}&fhdswitch={fhdswitch}&show1080p={show1080p}&isHLS={isHLS}&dtype={dtype}&sphls={sphls}&spgzip={spgzip}&dlver={dlver}&drm={drm}&hdcp={hdcp}&spau={spau}&spaudio={spaudio}&defsrc={defsrc}&encryptVer={encryptVer}&cKey={cKey}&fp2p=1&spadseg=3"
        result = f"spsrt={spsrt}&charge={charge}&defaultfmt={defaultfmt}&otype={otype}&guid={guid}&flowid={flowid}&platform={platform}&sdtfrom={sdtfrom}&defnpayver={defnpayver}&appVer={appVer}&host={host}&ehost={ehost}&refer={refer}&sphttps={sphttps}&tm={tm}&spwm={spwm}&logintoken={logintoken}&vid={vid}&defn={defn}&fhdswitch={fhdswitch}&show1080p={show1080p}&isHLS={isHLS}&dtype={dtype}&sphls={sphls}&spgzip={spgzip}&dlver={dlver}&drm={drm}&hdcp={hdcp}&spau={spau}&spaudio={spaudio}&defsrc={defsrc}&encryptVer={encryptVer}&cKey={cKey}&fp2p={fp2p}&spadseg={spadseg}"

        return result

    def get_cKey(self, platform, version, vid, guid, tm):
        file = 'getck.js'
        ctx = execjs.compile(open(file).read())
        params = ctx.call("getckey", platform, version, vid, '', guid,
                          tm)
        return params

    def get_buid(self):
        return "vinfoad"

    def start(self):
        ad_params = self.get_adparams()
        vinfoparams = self.get_vinfoparams()
        buid = self.get_buid()
        params = {"buid": buid,
                  "adparam": ad_params,
                  "vinfoparam": vinfoparams}
        res = requests.post("https://vd.l.qq.com/proxyhttp", headers=self.headers, json=params).json()
        return res

def getinfos(data):
    infos = []
    vinfo = json.loads(data['vinfo'])
    print(vinfo)
    fis = vinfo['fl']['fi']
    for fi in fis:
        info = {
            'title':"",
            'cname':fi['cname'],
            'fs':str(int(fi['fs']/1024/1024)) + 'MB',
            'url':""
        }
        infos.append(info)
    title = vinfo['vl']['vi'][0]['ti']
    uis = vinfo['vl']['vi'][0]['ul']['ui']
    for i in range(len(uis)):
        infos[i]['url'] = uis[i]['url']
        infos[i]['title'] = title
    for info in infos:
        print(info)


def run(url,cookie):
    data = tencent(url, cookie).start()
    getinfos(data)

if __name__ == '__main__':
    print('腾讯视频解析')
    cookie = input('输入Cookie:')
    if cookie == '':
     cookie = '_gcl_au=1.1.1733749175.1618888088; _ga=GA1.1.1925505353.1618888088; tvfe_boss_uuid=1ad10da1fe1d7adb; guid=3b43e1a451593fac; __lt__cid=a1cdf34d-c20c-4fae-964e-325b939896c9; _fbp=fb.1.1618888206780.905648655; _ga_5NSWYK5E9J=GS1.1.1618888087.1.1.1618888289.0; lang_code=1491963; video_guid=5f10f9991f9a2869; wetv_lang=zh-cn; wetv_pt=v; video_appid=1200004; pgv_pvid=7426643550; country_code=153505; _ga_ZZRPPC4YSC=GS1.1.1622462112.2.1.1622462193.0'
    while True:
        url = input('输入网址：')
        try:
            data = tencent(url, cookie).start()
            getinfos(data)
        except Exception as e:
            logging.exception(e)




