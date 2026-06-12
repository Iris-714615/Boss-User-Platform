from tortoise import fields
from tortoise.models import Model
from datetime import datetime


class City(Model):
    """城市表"""
    id = fields.IntField(pk=True, auto_increment=True)
    name = fields.CharField(max_length=50, unique=True, null=False)
    is_recommend = fields.IntField(default=0)

    class Meta:
        table = "city"


# ====================== 1. 用户核心模块 ======================
class User(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    phone = fields.CharField(max_length=20, unique=True, null=False, description="手机号")
    username = fields.CharField(max_length=50, unique=True, null=False, description="用户名")
    password = fields.CharField(max_length=100, null=False, description="密码（加密）")
    total_amount = fields.DecimalField(max_digits=10, decimal_places=2, default=0.00, description="总金额")
    status = fields.IntField(default=1, description="状态 1正常 0禁用")
    avatar = fields.CharField(max_length=255, null=True, description="头像")
    resume_score = fields.IntField(default=0, description="简历得分")
    total_deliver = fields.IntField(default=0, description="总投递数")
    create_time = fields.DatetimeField(auto_now_add=True, description="添加时间")
    email = fields.CharField(max_length=100, unique=True, null=True, description="邮箱")
    real_name = fields.CharField(max_length=20, null=True, description="姓名")
    gender = fields.IntField(null=True, description="1男 2女 0未知")
    age = fields.IntField(null=True, description="年龄")
    intention_position = fields.CharField(max_length=100, null=True, description="意向职位")
    intention_city = fields.ForeignKeyField("models.City", on_delete=fields.SET_NULL, null=True, description="期望城市")
    expected_salary_min = fields.IntField(null=True, description="期望最低薪资（K/月）")
    expected_salary_max = fields.IntField(null=True, description="期望最高薪资（K/月）")
    expected_salary_type = fields.CharField(max_length=20, default="month", description="薪资类型：month-月薪 year-年薪")
    is_real = fields.IntField(default=0, description="是否认证 1已认证 0未认证")
    class Meta:
        table = "user"


class UserAuth(Model):
    """三方登录表"""
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, description="用户ID")
    auth_type = fields.CharField(max_length=20, null=False, description="wechat/dingtalk")
    openid = fields.CharField(max_length=100, unique=True, null=False, description="三方用户ID")
    token = fields.CharField(max_length=255, null=True, description="令牌")
    retoken = fields.CharField(max_length=255, null=True, description="刷新令牌")

    class Meta:
        table = "user_auth"


class UserAuthReal(Model):
    """实名认证表"""
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, unique=True, description="用户ID")
    real_name = fields.CharField(max_length=20, null=False, description="姓名")
    id_card = fields.CharField(max_length=18, unique=True, null=False, description="身份证号")
    front_img = fields.CharField(max_length=255, null=False, description="正面照片")
    # back_img = fields.CharField(max_length=255, null=False, description="反面照片")
    status = fields.IntField(default=0, description="0待审核 1通过 2拒绝")

    class Meta:
        table = "user_auth_real"


# ====================== 2. 简历模块 ======================
class Resume(Model):
    """简历表"""
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, description="用户ID")
    resume_url = fields.CharField(max_length=255, null=False, description="简历地址")
    sort = fields.IntField(default=0, description="排序")

    class Meta:
        table = "resume"


class ResumeBasic(Model):
    """简历基本信息"""
    id = fields.IntField(pk=True, auto_increment=True)
    resume = fields.ForeignKeyField("models.Resume", on_delete=fields.CASCADE, unique=True, description="简历ID")
    education = fields.CharField(max_length=20, null=True, description="学历")
    job_intention = fields.CharField(max_length=100, null=True, description="求职意向")
    salary_min = fields.IntField(null=True, description="最低期望")
    salary_max = fields.IntField(null=True, description="最高期望")

    class Meta:
        table = "resume_basic"


class ResumeWork(Model):
    """工作经历"""
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, description="用户ID")
    company_name = fields.CharField(max_length=100, null=False, description="公司名")
    industry = fields.CharField(max_length=50, null=True, description="行业")
    position = fields.CharField(max_length=50, null=True, description="职位")
    start_time = fields.DateField(null=False, description="开始时间")
    end_time = fields.DateField(null=True, description="结束时间")
    work_desc = fields.TextField(null=True, description="工作描述")
    work_result = fields.TextField(null=True, description="工作业绩")
    tags = fields.CharField(max_length=255, null=True, description="标签逗号分隔")

    class Meta:
        table = "resume_work"


class ResumeProject(Model):
    """项目经历"""
    id = fields.IntField(pk=True, auto_increment=True)
    work = fields.ForeignKeyField("models.ResumeWork", on_delete=fields.CASCADE, description="工作经历ID")
    project_name = fields.CharField(max_length=100, null=False, description="项目名")
    position = fields.CharField(max_length=50, null=True, description="职位")
    start_time = fields.DateField(null=False)
    end_time = fields.DateField(null=True)
    task_desc = fields.TextField(null=True, description="任务描述")
    result_desc = fields.TextField(null=True, description="业绩描述")

    class Meta:
        table = "resume_project"


class ResumeEducation(Model):
    """学历信息"""
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, description="用户ID")
    school_name = fields.CharField(max_length=100, null=False, description="学校")
    major = fields.CharField(max_length=50, null=True, description="专业")
    start_time = fields.DateField(null=False)
    end_time = fields.DateField(null=True)
    type = fields.CharField(max_length=20, null=True, description="本科/大专")

    class Meta:
        table = "resume_education"


class SkillTag(Model):
    """技能标签"""
    id = fields.IntField(pk=True, auto_increment=True)
    name = fields.CharField(max_length=50, unique=True, null=False, description="标签名")
    is_enabled = fields.IntField(default=1, description="1可用 0禁用")

    class Meta:
        table = "skill_tag"


class UserSkill(Model):
    """用户技能关联"""
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    tag = fields.ForeignKeyField("models.SkillTag", on_delete=fields.CASCADE)

    class Meta:
        table = "user_skill"
        unique_together = (("user", "tag"),)


# ====================== 3. 企业模块 ======================
class Company(Model):
    """公司表"""
    id = fields.IntField(pk=True, auto_increment=True)
    name = fields.CharField(max_length=100, unique=True, null=False, description="公司名")
    intro = fields.TextField(null=True, description="介绍")
    scale = fields.CharField(max_length=50, null=True, description="规模")
    legal_person = fields.CharField(max_length=20, null=True, description="法人")
    registered_capital = fields.CharField(max_length=50, null=True, description="注册资金")
    address = fields.CharField(max_length=255, null=True, description="地址")

    class Meta:
        table = "company"


class Department(Model):
    """部门表"""
    id = fields.IntField(pk=True, auto_increment=True)
    company = fields.ForeignKeyField("models.Company", on_delete=fields.CASCADE)
    dept_name = fields.CharField(max_length=50, null=False, description="部门名")

    class Meta:
        table = "company_department"


class CompanyStaff(Model):
    """企业员工"""
    id = fields.IntField(pk=True, auto_increment=True)
    real_name = fields.CharField(max_length=20, null=False)
    username = fields.CharField(max_length=50, unique=True, null=False)
    password = fields.CharField(max_length=100, null=False)
    company = fields.ForeignKeyField("models.Company", on_delete=fields.CASCADE)
    dept = fields.ForeignKeyField("models.Department", on_delete=fields.CASCADE)

    class Meta:
        table = "company_staff"


# ====================== 4. 基础数据模块 ======================
class Industry(Model):
    """行业表"""
    id = fields.IntField(pk=True, auto_increment=True)
    name = fields.CharField(max_length=50, unique=True, null=False)
    icon = fields.CharField(max_length=255, null=True)
    total_jobs = fields.IntField(default=0)
    is_recommend = fields.IntField(default=0)

    class Meta:
        table = "industry"


# ====================== 5. 职位与互动模块 ======================
class Job(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    job_name = fields.CharField(max_length=100, null=False)
    salary_range = fields.CharField(max_length=50, null=True)
    city = fields.ForeignKeyField("models.City", on_delete=fields.CASCADE)
    education = fields.CharField(max_length=20, null=True)
    work_year = fields.CharField(max_length=20, null=True)
    job_desc = fields.TextField(null=False)
    publisher = fields.ForeignKeyField("models.CompanyStaff", on_delete=fields.CASCADE)
    company = fields.ForeignKeyField("models.Company", on_delete=fields.CASCADE)
    industry = fields.ForeignKeyField("models.Industry", on_delete=fields.CASCADE)
    is_recommend = fields.IntField(default=0)
    create_time = fields.DatetimeField(auto_now_add=True)
    is_urgent = fields.IntField(default=0, description="是否急招：1-是 0-否")
    is_home_recommend = fields.IntField(default=0, description="是否首页推荐职位")
    salary_base = fields.IntField(null=True, description="基础月薪（K）")
    salary_top = fields.IntField(null=True, description="最高月薪（K）")
    salary_times = fields.IntField(default=12, description="薪资倍数（如14薪）")

    class Meta:
        table = "job"


class JobTag(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    job = fields.ForeignKeyField("models.Job", on_delete=fields.CASCADE)
    tag = fields.ForeignKeyField("models.SkillTag", on_delete=fields.CASCADE)

    class Meta:
        table = "job_tag"
        unique_together = (("job", "tag"),)


class HotSearch(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    keyword = fields.CharField(max_length=50, unique=True, null=False, description="搜索关键词")
    sort = fields.IntField(default=0, description="排序权重")
    is_enabled = fields.IntField(default=1, description="是否启用")
    search_count = fields.IntField(default=0, description="累计搜索次数")

    class Meta:
        table = "hot_search"


class UserSearchHistory(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    keyword = fields.CharField(max_length=100)
    search_type = fields.CharField(max_length=20, default="job")
    create_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_search_history"


class JobDeliver(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    job = fields.ForeignKeyField("models.Job", on_delete=fields.CASCADE)
    create_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "job_deliver"
        unique_together = (("user", "job"),)


class JobCollect(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    job = fields.ForeignKeyField("models.Job", on_delete=fields.CASCADE)
    create_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "job_collect"
        unique_together = (("user", "job"),)


class JobInterview(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    job = fields.ForeignKeyField("models.Job", on_delete=fields.CASCADE)
    interview_time = fields.DatetimeField(null=False)
    status = fields.IntField(default=0)
    is_pass = fields.IntField(null=True)
    remark = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "job_interview"


class UserFollow(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    staff = fields.ForeignKeyField("models.CompanyStaff", on_delete=fields.CASCADE)
    create_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_follow"
        unique_together = (("user", "staff"),)


# ====================== 6. 财务模块 ======================
class UserRecharge(Model):
    """充值记录"""
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    pay_type = fields.CharField(max_length=20, null=False)
    serial_no = fields.CharField(max_length=100, unique=True)
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    recharge_time = fields.DatetimeField(auto_now_add=True)
    status = fields.IntField(default=0, description="0待支付 1成功 2失败")
    pay_time = fields.DatetimeField(null=True)

    class Meta:
        table = "user_recharge"


class UserConsume(Model):
    """消费记录"""
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    remark = fields.CharField(max_length=255)
    create_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_consume"


class Coupon(Model):
    """优惠券"""
    id = fields.IntField(pk=True, auto_increment=True)
    name = fields.CharField(max_length=100)
    amount = fields.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = fields.DecimalField(max_digits=3, decimal_places=2, default=1.00)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()

    class Meta:
        table = "coupon"


class UserCoupon(Model):
    """用户优惠券"""
    id = fields.IntField(pk=True, auto_increment=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    coupon = fields.ForeignKeyField("models.Coupon", on_delete=fields.CASCADE)
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    discount = fields.DecimalField(max_digits=3, decimal_places=2)
    start_time = fields.DatetimeField()
    end_time = fields.DatetimeField()
    is_used = fields.IntField(default=0)

    class Meta:
        table = "user_coupon"


# 消息分类表    id、分类名称、添加时间、用户id
class MessageCategory(Model):
    id = fields.IntField(pk=True, auto_increment=True)
    name = fields.CharField(max_length=100,default='新对话')
    create_time = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    class Meta:
        table = "message_category"

# 消息表  id、内容、消息分类id（外键关联消息分类表）、角色、添加时间
class Message(Model):
    id = fields.IntField(pk=True,auto_increment=True)
    content = fields.TextField()
    message_category = fields.ForeignKeyField("models.MessageCategory", on_delete=fields.CASCADE)
    role = fields.CharField(max_length=100)
    create_time = fields.DatetimeField(auto_now_add=True)
    class Meta:
        table = "message"