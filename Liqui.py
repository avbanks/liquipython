# Andre V. Banks

"""
    Liqui API Python Wrapper
"""

import http.client
import urllib.request, urllib.parse, urllib.error
import json
import hashlib
import hmac
import time

PUBLIC = {'info', 'ticker', 'depth', 'trades'}



class Liqui(object):

    def __init__(self,api_key,api_secret,wait_for_nonce=False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.wait_for_nonce = wait_for_nonce
        self.nonce = str(time.time()).split('.')[0]

    def __signature(self, params):
        sig = hmac.new(self.api_secret.encode(), params.encode(), hashlib.sha512)
        return sig.hexdigest()

    def __api_call(self,method,params):
        if method in PUBLIC:
            pass
        params['method'] = method
        params['nonce'] = str(self.nonce)
        params = urllib.parse.urlencode(params)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                            "Key": self.api_key,
                   "Sign": self.__signature(params)}
        conn = http.client.HTTPSConnection("api.liqui.io")
        conn.request("POST", "/tapi", params, headers)
        response = conn.getresponse().read().decode()
        data = json.loads(response)
        conn.close()
        return data
 
    def get_param(self, couple, param):
        conn = http.client.HTTPSConnection("api.liqui.io")
        conn.request("GET", "/api/3/"+couple+"/"+param)
        response = conn.getresponse()
        data = json.loads(response)
        conn.close()
        return data

    def getInfo(self):
        return self.__api_call('getInfo', {})

    def TradeHistory(self, tcount=1000, tfrom_id=0, tpair=''):
        tpair=''
        params = {
            "count"	: tcount,
            "from_id"	: tfrom_id,
            "pair"	: tpair}
        return self.__api_call('TradeHistory', params)

    def ActiveOrders(self, tpair=''):
        params = {"pair": tpair}
        return self.__api_call('ActiveOrders', params)

    def OrderInfo(self, order_id):
        params = {"order_id": order_id}
        return self.__api_call('OrderInfo', params)

    def Trade(self, tpair, ttype, trate, tamount):
        params = {
         "pair"	: tpair,
         "type"	: ttype,
         "rate"	: trate,
         "amount"	: tamount}
        return self.__api_call('Trade', params)
 
    def CancelOrder(self, torder_id):
        params = {"order_id": torder_id}
        return self.__api_call('CancelOrder', params)


