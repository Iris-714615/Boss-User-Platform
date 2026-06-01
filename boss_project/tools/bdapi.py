import requests
class BaiDuApi:
    def __init__(self):
        self.API_KEY = "0I3WAsPxmq7M9FaVfcQv4drR"
        self.SECRET_KEY = "EE4KBH6Fu7N5O5kd71RaT7vGJ4yQARdH"

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.API_KEY, "client_secret": self.SECRET_KEY}
        return str(requests.post(url, params=params).json().get("access_token"))

    def font_ocr(self,imgurl:str):            
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + self.get_access_token()        
        payload='url='+imgurl+'&detect_direction=false&paragraph=false&probability=false&multidirectional_recognize=false'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
        
        response.encoding = "utf-8"
        print(response.text)
        return response.text


    def idcard(self,imgurl:str):
        
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/idcard?access_token=" + self.get_access_token()
        
        payload='id_card_side=front&url=%s&detect_ps=false&detect_risk=false&detect_quality=false&detect_photo=false&detect_card=false&detect_direction=false&detect_screenshot=false' % imgurl
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
        
        response.encoding = "utf-8"
        print(response.text)
        return response.text


bdapi = BaiDuApi()
# import json

# res = bdapi.font_ocr("http://tfxnqdgub.hb-bkt.clouddn.com/FrVh9mcLoYlBJUd9nQ7ujgbD-pgP")
# res = json.loads(res)
# name = res["words_result"][0]["words"][-2:]
# idcard = res["words_result"][1]["words"][-18:]
# print(name,idcard)
# bdapi.idcard("http://tfxjmphsh.hn-bkt.clouddn.com/lneNn0xBIwoG6E9kp02qvzM6APcP")