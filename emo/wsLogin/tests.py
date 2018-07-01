from django.test import TestCase
import urllib.request
import requests
import json

# Create your tests here.
class WxLoginMethodTests(TestCase):

    def  test_login_with_openid_and_accesstoken(self):
        url = 'http://193.112.24.51:8000/wxLogin/'
        d = {'openid': 'ccaonimagebi', 'access_token': 'qunimade'}    
        r = requests.post(url, data=d)
        jsData = json.loads(r.text)
        result = {"unionid":"3838438","privilege":"超级加倍","nickname":"user19","sex":1,"headimgurl":"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1529751764221&di=7b77ae9d0598a1d996abbd83ff63b7b5&imgtype=0&src=http%3A%2F%2Fupload.mnw.cn%2F2018%2F0324%2F1521876947374.png","province":"province19","country":"country19","openid":"ccaonimagebi","city":"city19"}
        self.assertEqual(jsData,result)

    def  test_login_with_null(self):
        url = 'http://193.112.24.51:8000/wxLogin/'
        #d = {'openid': 'ccaonimagebi', 'access_token': 'qunimade'}    
        r = requests.post(url)
        jsData = json.loads(r.text)
        #print(r.text)
        result = {"opneid":""}
        self.assertEqual(jsData,result)

    def  test_login_with_openid(self):
        url = 'http://193.112.24.51:8000/wxLogin/'
        d = {'openid': 'ccaonimagebilalala'}    
        r = requests.post(url, data=d)
        #print(r.text)
        jsData = json.loads(r.text)
        result = {"access_token":""}
        self.assertEqual(jsData,result)


