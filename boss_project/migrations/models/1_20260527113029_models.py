from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `city` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL UNIQUE,
    `is_recommend` INT NOT NULL DEFAULT 0
) CHARACTER SET utf8mb4 COMMENT='城市表';
        CREATE TABLE IF NOT EXISTS `company` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL UNIQUE COMMENT '公司名',
    `intro` LONGTEXT COMMENT '介绍',
    `scale` VARCHAR(50) COMMENT '规模',
    `legal_person` VARCHAR(20) COMMENT '法人',
    `registered_capital` VARCHAR(50) COMMENT '注册资金',
    `address` VARCHAR(255) COMMENT '地址'
) CHARACTER SET utf8mb4 COMMENT='公司表';
        CREATE TABLE IF NOT EXISTS `company_department` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `dept_name` VARCHAR(50) NOT NULL COMMENT '部门名',
    `company_id` INT NOT NULL,
    CONSTRAINT `fk_company__company_e4db1251` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='部门表';
        CREATE TABLE IF NOT EXISTS `company_staff` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `real_name` VARCHAR(20) NOT NULL,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password` VARCHAR(100) NOT NULL,
    `company_id` INT NOT NULL,
    `dept_id` INT NOT NULL,
    CONSTRAINT `fk_company__company_1d311259` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_company__company__75c0ecec` FOREIGN KEY (`dept_id`) REFERENCES `company_department` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='企业员工';
        CREATE TABLE IF NOT EXISTS `coupon` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `amount` DECIMAL(10,2) NOT NULL DEFAULT 0,
    `discount` DECIMAL(3,2) NOT NULL DEFAULT 1,
    `start_time` DATETIME(6) NOT NULL,
    `end_time` DATETIME(6) NOT NULL
) CHARACTER SET utf8mb4 COMMENT='优惠券';
        CREATE TABLE IF NOT EXISTS `hot_search` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `keyword` VARCHAR(50) NOT NULL UNIQUE COMMENT '搜索关键词',
    `sort` INT NOT NULL COMMENT '排序权重' DEFAULT 0,
    `is_enabled` INT NOT NULL COMMENT '是否启用' DEFAULT 1,
    `search_count` INT NOT NULL COMMENT '累计搜索次数' DEFAULT 0
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `industry` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL UNIQUE,
    `icon` VARCHAR(255),
    `total_jobs` INT NOT NULL DEFAULT 0,
    `is_recommend` INT NOT NULL DEFAULT 0
) CHARACTER SET utf8mb4 COMMENT='行业表';
        CREATE TABLE IF NOT EXISTS `job` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `job_name` VARCHAR(100) NOT NULL,
    `salary_range` VARCHAR(50),
    `education` VARCHAR(20),
    `work_year` VARCHAR(20),
    `job_desc` LONGTEXT NOT NULL,
    `is_recommend` INT NOT NULL DEFAULT 0,
    `create_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `is_urgent` INT NOT NULL COMMENT '是否急招：1-是 0-否' DEFAULT 0,
    `is_home_recommend` INT NOT NULL COMMENT '是否首页推荐职位' DEFAULT 0,
    `salary_base` INT COMMENT '基础月薪（K）',
    `salary_top` INT COMMENT '最高月薪（K）',
    `salary_times` INT NOT NULL COMMENT '薪资倍数（如14薪）' DEFAULT 12,
    `city_id` INT NOT NULL,
    `company_id` INT NOT NULL,
    `industry_id` INT NOT NULL,
    `publisher_id` INT NOT NULL,
    CONSTRAINT `fk_job_city_cf8f74ca` FOREIGN KEY (`city_id`) REFERENCES `city` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_job_company_f2c22f58` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_job_industry_29b7ffd2` FOREIGN KEY (`industry_id`) REFERENCES `industry` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_job_company__d5cd4e31` FOREIGN KEY (`publisher_id`) REFERENCES `company_staff` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `phone` VARCHAR(20) NOT NULL UNIQUE COMMENT '手机号',
    `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(100) NOT NULL COMMENT '密码（加密）',
    `total_amount` DECIMAL(10,2) NOT NULL COMMENT '总金额' DEFAULT 0,
    `status` INT NOT NULL COMMENT '状态 1正常 0禁用' DEFAULT 1,
    `avatar` VARCHAR(255) COMMENT '头像',
    `resume_score` INT NOT NULL COMMENT '简历得分' DEFAULT 0,
    `total_deliver` INT NOT NULL COMMENT '总投递数' DEFAULT 0,
    `create_time` DATETIME(6) NOT NULL COMMENT '添加时间' DEFAULT CURRENT_TIMESTAMP(6),
    `email` VARCHAR(100) UNIQUE COMMENT '邮箱',
    `real_name` VARCHAR(20) COMMENT '姓名',
    `gender` INT COMMENT '1男 2女 0未知',
    `age` INT COMMENT '年龄',
    `intention_position` VARCHAR(100) COMMENT '意向职位',
    `expected_salary_min` INT COMMENT '期望最低薪资（K/月）',
    `expected_salary_max` INT COMMENT '期望最高薪资（K/月）',
    `expected_salary_type` VARCHAR(20) NOT NULL COMMENT '薪资类型：month-月薪 year-年薪' DEFAULT 'month',
    `intention_city_id` INT COMMENT '期望城市',
    CONSTRAINT `fk_user_city_f3951b78` FOREIGN KEY (`intention_city_id`) REFERENCES `city` (`id`) ON DELETE SET NULL
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `job_collect` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `job_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    UNIQUE KEY `uid_job_collect_user_id_a03c59` (`user_id`, `job_id`),
    CONSTRAINT `fk_job_coll_job_ae81a0b8` FOREIGN KEY (`job_id`) REFERENCES `job` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_job_coll_user_e4e6e85c` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `job_deliver` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `job_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    UNIQUE KEY `uid_job_deliver_user_id_316a40` (`user_id`, `job_id`),
    CONSTRAINT `fk_job_deli_job_18610a8f` FOREIGN KEY (`job_id`) REFERENCES `job` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_job_deli_user_93fbb84a` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `job_interview` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `interview_time` DATETIME(6) NOT NULL,
    `status` INT NOT NULL DEFAULT 0,
    `is_pass` INT,
    `remark` VARCHAR(255),
    `job_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_job_inte_job_a2c81d2e` FOREIGN KEY (`job_id`) REFERENCES `job` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_job_inte_user_abe0e221` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `skill_tag` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL UNIQUE COMMENT '标签名',
    `is_enabled` INT NOT NULL COMMENT '1可用 0禁用' DEFAULT 1
) CHARACTER SET utf8mb4 COMMENT='技能标签';
        CREATE TABLE IF NOT EXISTS `job_tag` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `job_id` INT NOT NULL,
    `tag_id` INT NOT NULL,
    UNIQUE KEY `uid_job_tag_job_id_ae1f85` (`job_id`, `tag_id`),
    CONSTRAINT `fk_job_tag_job_b61f7f34` FOREIGN KEY (`job_id`) REFERENCES `job` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_job_tag_skill_ta_b407a8c2` FOREIGN KEY (`tag_id`) REFERENCES `skill_tag` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `resume` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `resume_url` VARCHAR(255) NOT NULL COMMENT '简历地址',
    `sort` INT NOT NULL COMMENT '排序' DEFAULT 0,
    `user_id` INT NOT NULL COMMENT '用户ID',
    CONSTRAINT `fk_resume_user_1131c79b` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='简历表';
        CREATE TABLE IF NOT EXISTS `resume_basic` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `education` VARCHAR(20) COMMENT '学历',
    `job_intention` VARCHAR(100) COMMENT '求职意向',
    `salary_min` INT COMMENT '最低期望',
    `salary_max` INT COMMENT '最高期望',
    `resume_id` INT NOT NULL COMMENT '简历ID',
    CONSTRAINT `fk_resume_b_resume_6d559740` FOREIGN KEY (`resume_id`) REFERENCES `resume` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='简历基本信息';
        CREATE TABLE IF NOT EXISTS `resume_education` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `school_name` VARCHAR(100) NOT NULL COMMENT '学校',
    `major` VARCHAR(50) COMMENT '专业',
    `start_time` DATE NOT NULL,
    `end_time` DATE,
    `type` VARCHAR(20) COMMENT '本科/大专',
    `user_id` INT NOT NULL COMMENT '用户ID',
    CONSTRAINT `fk_resume_e_user_a42414ce` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='学历信息';
        CREATE TABLE IF NOT EXISTS `resume_work` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `company_name` VARCHAR(100) NOT NULL COMMENT '公司名',
    `industry` VARCHAR(50) COMMENT '行业',
    `position` VARCHAR(50) COMMENT '职位',
    `start_time` DATE NOT NULL COMMENT '开始时间',
    `end_time` DATE COMMENT '结束时间',
    `work_desc` LONGTEXT COMMENT '工作描述',
    `work_result` LONGTEXT COMMENT '工作业绩',
    `tags` VARCHAR(255) COMMENT '标签逗号分隔',
    `user_id` INT NOT NULL COMMENT '用户ID',
    CONSTRAINT `fk_resume_w_user_94c071af` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='工作经历';
        CREATE TABLE IF NOT EXISTS `resume_project` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `project_name` VARCHAR(100) NOT NULL COMMENT '项目名',
    `position` VARCHAR(50) COMMENT '职位',
    `start_time` DATE NOT NULL,
    `end_time` DATE,
    `task_desc` LONGTEXT COMMENT '任务描述',
    `result_desc` LONGTEXT COMMENT '业绩描述',
    `work_id` INT NOT NULL COMMENT '工作经历ID',
    CONSTRAINT `fk_resume_p_resume_w_b25a1ee0` FOREIGN KEY (`work_id`) REFERENCES `resume_work` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='项目经历';
        CREATE TABLE IF NOT EXISTS `user_auth` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `auth_type` VARCHAR(20) NOT NULL COMMENT 'wechat/dingtalk',
    `openid` VARCHAR(100) NOT NULL UNIQUE COMMENT '三方用户ID',
    `token` VARCHAR(255) COMMENT '令牌',
    `retoken` VARCHAR(255) COMMENT '刷新令牌',
    `user_id` INT NOT NULL COMMENT '用户ID',
    CONSTRAINT `fk_user_aut_user_3cb6ff0a` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='三方登录表';
        CREATE TABLE IF NOT EXISTS `user_auth_real` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `real_name` VARCHAR(20) NOT NULL COMMENT '姓名',
    `id_card` VARCHAR(18) NOT NULL UNIQUE COMMENT '身份证号',
    `front_img` VARCHAR(255) NOT NULL COMMENT '正面照片',
    `back_img` VARCHAR(255) NOT NULL COMMENT '反面照片',
    `status` INT NOT NULL COMMENT '0待审核 1通过 2拒绝' DEFAULT 0,
    `user_id` INT NOT NULL COMMENT '用户ID',
    CONSTRAINT `fk_user_aut_user_61e1f7df` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='实名认证表';
        CREATE TABLE IF NOT EXISTS `user_consume` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `amount` DECIMAL(10,2) NOT NULL,
    `remark` VARCHAR(255) NOT NULL,
    `create_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_user_con_user_c0ef503a` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='消费记录';
        CREATE TABLE IF NOT EXISTS `user_coupon` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `amount` DECIMAL(10,2) NOT NULL,
    `discount` DECIMAL(3,2) NOT NULL,
    `start_time` DATETIME(6) NOT NULL,
    `end_time` DATETIME(6) NOT NULL,
    `is_used` INT NOT NULL DEFAULT 0,
    `coupon_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_user_cou_coupon_794a3957` FOREIGN KEY (`coupon_id`) REFERENCES `coupon` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_cou_user_4f036706` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用户优惠券';
        CREATE TABLE IF NOT EXISTS `user_follow` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `create_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `staff_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    UNIQUE KEY `uid_user_follow_user_id_3b0ad2` (`user_id`, `staff_id`),
    CONSTRAINT `fk_user_fol_company__f0c8a7d4` FOREIGN KEY (`staff_id`) REFERENCES `company_staff` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_fol_user_87452b3b` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `user_recharge` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `pay_type` VARCHAR(20) NOT NULL,
    `serial_no` VARCHAR(100) NOT NULL UNIQUE,
    `amount` DECIMAL(10,2) NOT NULL,
    `recharge_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `status` INT NOT NULL COMMENT '0待支付 1成功 2失败' DEFAULT 0,
    `pay_time` DATETIME(6),
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_user_rec_user_a2f872d0` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='充值记录';
        CREATE TABLE IF NOT EXISTS `user_search_history` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `keyword` VARCHAR(100) NOT NULL,
    `search_type` VARCHAR(20) NOT NULL DEFAULT 'job',
    `create_time` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_user_sea_user_1caf2a13` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `user_skill` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `tag_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    UNIQUE KEY `uid_user_skill_user_id_642ac4` (`user_id`, `tag_id`),
    CONSTRAINT `fk_user_ski_skill_ta_eaa4c5d9` FOREIGN KEY (`tag_id`) REFERENCES `skill_tag` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_user_ski_user_19d138c5` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用户技能关联';
        DROP TABLE IF EXISTS `buser`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `resume_basic`;
        DROP TABLE IF EXISTS `user_recharge`;
        DROP TABLE IF EXISTS `user_coupon`;
        DROP TABLE IF EXISTS `user_consume`;
        DROP TABLE IF EXISTS `user_auth`;
        DROP TABLE IF EXISTS `hot_search`;
        DROP TABLE IF EXISTS `job`;
        DROP TABLE IF EXISTS `user`;
        DROP TABLE IF EXISTS `city`;
        DROP TABLE IF EXISTS `company_department`;
        DROP TABLE IF EXISTS `coupon`;
        DROP TABLE IF EXISTS `resume_project`;
        DROP TABLE IF EXISTS `user_search_history`;
        DROP TABLE IF EXISTS `company`;
        DROP TABLE IF EXISTS `skill_tag`;
        DROP TABLE IF EXISTS `job_tag`;
        DROP TABLE IF EXISTS `resume_work`;
        DROP TABLE IF EXISTS `user_skill`;
        DROP TABLE IF EXISTS `resume`;
        DROP TABLE IF EXISTS `job_collect`;
        DROP TABLE IF EXISTS `company_staff`;
        DROP TABLE IF EXISTS `resume_education`;
        DROP TABLE IF EXISTS `user_auth_real`;
        DROP TABLE IF EXISTS `user_follow`;
        DROP TABLE IF EXISTS `job_interview`;
        DROP TABLE IF EXISTS `industry`;
        DROP TABLE IF EXISTS `job_deliver`;"""


MODELS_STATE = (
    "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"
)
