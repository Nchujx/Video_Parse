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
        self.defn = "fhd"
        self.dtype = "3"
        self.sphls = "2"


    def parse_cookie(self):
        if self.cookie:
            for i in self.cookie.split(";"):
                kv = i.split("=")
                self.cookie_dict[kv[0].strip()] = kv[1]

    def get_vid_coverid(self):
        response = requests.get(url=url).text
        vid = re.findall('vid=(.+?)&', response)[1]
        # coverid = re.findall('"cover_id":"(.+?)"',response)[0]
        return vid

    def get_adparams(self):
        pf = ""
        ad_type = ""
        pf_ex = ""
        url = ""
        refer = ""
        ty = ""
        plugin = ""
        v = ""
        vid= self.get_vid_coverid()
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
        result = f"pf={pf}&ad_type={ad_type}&pf_ex={pf_ex}&url={url}&refer={refer}&ty={ty}&plugin={plugin}&v={v}&vid={vid}&pt={pt}&flowid={flowid}&vptag={vptag}&pu={pu}&chid={chid}&adaptor={adaptor}&dtype={dtype}&live={live}&resp_type={resp_type}&guid={guid}&req_type={req_type}&from=0&appversion={appversion}&uid={uid}&tkn={tkn}&lt={lt}&platform={platform}&opid={opid}&atkn={atkn}&appid={appid}&tpid={tpid}"
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
        vid = self.get_vid_coverid()
        defn = self.defn
        fhdswitch = ""
        show1080p = ""
        isHLS = ""
        dtype = self.dtype
        sphls = self.sphls
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
    #
    print('腾讯视频解析')
    cookie = input('输入Cookie:')
    if cookie == '':
        cookie = 'ts_uid=5313142320; video_platform=2; video_guid=a2a0ec403cb3ada6; login_remember=qq; tvfe_search_uid=25b5a6a2-9071-471e-b3a9-86edb5f3a05a; txv_boss_uuid=a831fe9a-5f2f-81e2-6753-152e18a4989a; last_refresh_vuserid=320266178; ts_refer=m.v.qq.com/; last_refresh_time=1623327400765; tvfe_boss_uuid=ecdcd81de0ab7c1f; pgv_pvid=4001883338; RK=y+DhymWORh; ptcz=8a5c04aba85feb516cbec5ecda04682765b382bd27e4d91947e4d9535d7db942; bucket_id=9231008; main_login=qq; vqq_vuserid=1425233597; vqq_access_token=F779F45E4A8836AC10AEDC09CB890A36; vqq_openid=B423A6DCC6325B36C2A29541409A04CF; vqq_appid=101483052; qq_nick=%E7%BB%86%E6%B0%B4%E6%B5%81%E9%95%BF; qq_head=http://thirdqq.qlogo.cn/g?b=oidb&k=PS3QOQHdMa25YFGJVgyehw&s=140&t=1557434674; lw_nick=%E7%BB%86%E6%B0%B4%E6%B5%81%E9%95%BF|0|http://thirdqq.qlogo.cn/g?b=oidb&k=PS3QOQHdMa25YFGJVgyehw&s=140&t=1557434674|0; vqq_vusession=bdYQn2v2RWYb_F_sKG29gA..; uid=75942176; pgv_info=ssid=s3502909248; ts_last=v.qq.com/x/cover/mzc00200bvr1rz1.html; ad_play_index=90'
    while True:
        url = input('输入网址：')
        try:
            data = tencent(url, cookie).start()
            getinfos(data)
        except Exception as e:
            logging.exception(e)




