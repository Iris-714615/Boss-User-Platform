import jwt
import time
from datetime import datetime, timedelta

# JWT 配置
SECRET_KEY = '123456'  # 生产环境请使用安全的密钥
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # token 过期时间（分钟）

class myjwt:
    def __init__(self):
        pass
    def encode(self, data, expires_minutes=None):
        """
        生成 JWT token
        
        :param userid: 用户ID
        :param roleid: 用户角色IDdata: 包含用户信息的字典
        :param expires_minutes: 过期时间（分钟），默认为配置值
        :return: JWT token 字符串
        """
        if expires_minutes is None:
            expires_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        
        # 过期时间
        expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
        
        # payload 数据
        payload = {
            **data,
            'exp': expire,
            'iat': datetime.utcnow()
        }
        
        # 生成 token
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token


    def decode(self, token):
        """
        解析 JWT token，不验证过期时间
        
        :param token: JWT token 字符串
        :return: payload 字典，如果解析失败返回 None
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_exp': False})
            return payload
        except jwt.InvalidTokenError:
            return None


    def verify(self, token):
        """
        验证 JWT token（包括过期时间验证）
        
        :param token: JWT token 字符串
        :return: payload 字典，如果验证失败返回 None
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.InvalidTokenError:
            return None


    def is_token_expired(self, token):
        """
        检查 token 是否过期
        
        :param token: JWT token 字符串
        :return: True 如果过期，False 如果未过期，None 如果解析失败
        """
        payload = self.decode(token)
        if payload is None:
            return None
        
        exp = payload.get('exp')
        if exp is None:
            return False
        
        # 比较过期时间和当前时间
        return time.time() > exp


    def get_user_info_from_token(self, token):
        """
        从 token 中获取用户信息
        
        :param token: JWT token 字符串
        :return: 包含 user_id 和 role 的字典，如果失败返回 None
        """
        payload = self. verify(token)
        if payload is None:
            return None
        
        return {
            'userid': payload.get('userid'),
            'roleid': payload.get('roleid')
        }
mjwt = myjwt()