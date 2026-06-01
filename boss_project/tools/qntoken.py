def qiniu_token():  

    from qiniu import Auth
    
    #需要填写你的 Access Key 和 Secret Key
    access_key = 'DrbjmtIHF4AVCNRa0V-kg4A5US0jJuSq8bRKIB1W'
    secret_key = 'nzEbGxMtpdJypbDBdAoKyaTzLUjxPSQe28XT8y6Y'
    #构建鉴权对象
    q = Auth(access_key, secret_key)
    #要上传的空间
    bucket_name = 'c2601'
    #上传后保存的文件名
    # key = 'my-python-logo.png'
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)
    return token