from urllib.parse import quote
import requests
from abc import ABC, abstractmethod

class Factory(ABC):
    @abstractmethod
    def get_url(self):
        pass
    @abstractmethod
    def callback(self,code: str):
        pass


class Dingding(Factory):
    def __init__(self):
        self.clientId = "dinghlmwxxjrijnwjicr"
        self.clientSecret = "xkIF7X_ygvVtljl8RrEctetuCPG_f4ONLMuJIgngxmy3UGqtsACu_o1HVlnudHCl"
        self.redirect_url="http://localhost:8000/auth/dingcallback"

    def get_url(self):      
        params = [
            f"redirect_uri={quote('%s' % self.redirect_url)}",
            "response_type=code",
            "client_id="+self.clientId,
            "scope=openid",
            "prompt=consent"
        ]
        url = "https://login.dingtalk.com/oauth2/auth?" + ("&".join(params))
        return url
    def callback(self,code: str):
        data = {
            "clientId": self.clientId,
            "clientSecret": self.clientSecret,
            "code": code,
            "grantType": "authorization_code"
        }
        resp = requests.post('https://api.dingtalk.com/v1.0/oauth2/userAccessToken', json=data).json()
    
        accessToken = resp.get('accessToken')
        # uid = resp.get('openId')
        # 根据accessToken获取用户信息
        headers = {"x-acs-dingtalk-access-token": accessToken}
        resp = requests.get('https://api.dingtalk.com/v1.0/contact/users/me', headers=headers).json()
        print(resp)
        name = resp.get('nick')
        phone = resp.get('mobile')
        uid = resp.get('openId')
        return {"name":name,"phone":phone,"uid":uid,"accessToken":accessToken}
    

class Qq(Factory):
    def __init__(self):
        self.clientId = "1004244532"
        self.clientSecret = "1004244532"
        self.redirect_url="http://localhost:3002/qqcallback"
    def get_url(self):
        url = "http://qq.com"
        return url
    def callback(self,code: str):
        
        return {"name":'sdfsdf',"phone":"111","uid":"2343243423","accessToken":"2343243423"}
    

class Weibo(Factory):
    def __init__(self):
        self.clientId = "1004244532"
        self.clientSecret = "1004244532"
        self.redirect_url="http://localhost:3002/qqcallback"
    def get_url(self):
        url = "http://weibo.com"
        return url
    def callback(self,code: str):
        
        return {"name":'sdfsdf',"phone":"111","uid":"2343243423","accessToken":"2343243423"}
    
class Weixin(Factory):
    def __init__(self):
        self.clientId = "1004244532"
        self.clientSecret = "1004244532"
        self.redirect_url="http://localhost:3002/qqcallback"
    def get_url(self):
        url = "http://weixin.qq.com"
        return url
    def callback(self,code: str):
        
        return {"name":'sdfsdf',"phone":"111"}
    
    
import sys
class Product:
    def get_cls_class(self,types: str):
        # 将小写的类型名转换为大写开头的类名
        class_name = types.capitalize()
        # 获取当前模块
        current_module = sys.modules[__name__]
        try:
            # 使用反射获取类对象
            target_class = getattr(current_module, class_name)
            if issubclass(target_class, Factory):
                return target_class()
        except AttributeError:
            print(f"未找到名为 {class_name} 的类。")
        return None
    
p = Product()
