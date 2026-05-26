from tortoise.models import Model
from tortoise import fields


#资源表  id  资源名称  资源路径  pid(父资源id自关联)
class Resource(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    path = fields.CharField(max_length=20,null=True,blank=True)
    pid = fields.ForeignKeyField("models.Resource",null=True,blank=True,related_name="sons")
    class Meta:
        table = "resource"
        ordering = ["id"]  

# #创建角色表  id  name  资源（多对多关系）
class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    resources = fields.ManyToManyField("models.Resource", related_name="roles")
    class Meta:
        table = "role"
        ordering = ["id"]

 
# #创建用户表  id  name mobile password role_id
class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20)
    mobile = fields.CharField(max_length=11,null=True,blank=True)
    password = fields.CharField(max_length=20)
    # role = fields.ForeignKeyField(Role,related_name="users")
    role = fields.ForeignKeyField(
        'models.Role',           # 关联的表
        related_name='users', # 反向关联名（通过班级找学生：clas.students）
        description='所属角色'
    )

    class Meta:
        table = "user"
        ordering = ["id"]  