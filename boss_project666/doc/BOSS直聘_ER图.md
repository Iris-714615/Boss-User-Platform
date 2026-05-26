# BOSS 直聘 — 实体关系图 (ER Diagram)

> **格式**: Mermaid (纯文本、可编辑、Markdown 原生渲染)  
> **版本**: V1.0 | **日期**: 2026-05-26  
> **适用项目**: boss-candidate-ui / boss-company-ui / boss-manage-ui

---

## 一、全局 ER 图

```mermaid
erDiagram
    CandidateUser ||--o| Resume : "拥有"
    CandidateUser ||--o{ Delivery : "投递"
    CandidateUser ||--o| RealNameAuth : "实名认证"
    CandidateUser ||--o{ ChatMessage : "发送/接收消息"

    Resume ||--o{ WorkExperience : "包含"
    Resume ||--o{ Project : "包含"

    Company ||--o{ Position : "发布"
    Company ||--o{ HRUser : "雇佣"
    Company ||--o{ Delivery : "被投递"

    Position ||--o{ Delivery : "被投递"
    Position ||--o{ ChatMessage : "关联消息"

    HRUser ||--o{ ChatMessage : "发送/接收消息"

    AdminUser {
        string id PK "管理员ID"
        string username "用户名"
        string realName "真实姓名"
        string role "角色: 超级管理员|普通管理员"
        number createdAt "创建时间"
    }

    CandidateUser {
        string id PK "求职者ID"
        string phone UK "手机号"
        string name "姓名"
        string avatar "头像URL"
        string resumeStatus "简历状态: 未完善|完善中|已完成"
        number createdAt "注册时间"
    }

    RealNameAuth {
        string id PK "认证记录ID"
        string candidateId FK "求职者ID"
        string realName "真实姓名"
        string idCardNumber "身份证号"
        string idCardFront "身份证正面照URL"
        string idCardBack "身份证反面照URL"
        string selfie "自拍照URL"
        string status "状态: not_submitted|pending|approved|rejected"
        string rejectReason "驳回原因"
        number submittedAt "提交时间"
        number reviewedAt "审核时间"
    }

    Resume {
        string id PK "简历ID"
        string candidateId FK "求职者ID"
        string name "姓名"
        string phone "手机号"
        string email "邮箱"
        string avatar "头像"
        number age "年龄"
        string gender "性别: 男|女"
        string city "所在城市"
        string education "学历"
        number graduationYear "毕业年份"
        string major "专业"
        string experience "工作经验"
        string expectedPosition "期望职位"
        string expectedCity "期望城市"
        string expectedSalary "期望薪资"
        string selfIntroduce "自我介绍"
        string status "状态: 保密|公开"
        number updatedAt "更新时间"
    }

    WorkExperience {
        string companyId "公司ID"
        string companyName "公司名称"
        string position "职位"
        number startDate "开始时间"
        number endDate "结束时间"
        string description "工作描述"
    }

    Project {
        string name "项目名称"
        string role "担任角色"
        number startDate "开始时间"
        number endDate "结束时间"
        string description "项目描述"
        string technologies "技术栈"
    }

    Company {
        string id PK "公司ID"
        string name "公司名称"
        string industry "行业"
        string scale "规模"
        string stage "融资阶段"
        string city "城市"
        string district "区域"
        string address "详细地址"
        string description "公司介绍"
        string logo "Logo URL"
        string status "状态: 待审核|正常|封禁"
        number createdAt "创建时间"
        number updatedAt "更新时间"
    }

    Position {
        string id PK "职位ID"
        string companyId FK "公司ID"
        string companyName "公司名称(冗余)"
        string title "职位标题"
        string department "部门"
        string city "工作城市"
        string district "工作区域"
        string address "工作地址"
        number salaryMin "最低薪资(K)"
        number salaryMax "最高薪资(K)"
        number salaryMonth "年薪月数"
        string experience "经验要求"
        string education "学历要求"
        string gender "性别要求"
        number number "招聘人数"
        string description "职位描述"
        string requirements "任职要求"
        string status "状态: 草稿|待审核|已发布|已关闭|封禁"
        number publishedAt "发布时间"
        number views "浏览次数"
        number communicates "沟通次数"
        number resumes "收到简历数"
        number createdAt "创建时间"
        number updatedAt "更新时间"
    }

    HRUser {
        string id PK "HR ID"
        string username "用户名"
        string phone "手机号"
        string realName "真实姓名"
        string companyId FK "所属公司ID"
        string companyName "公司名称(冗余)"
        string role "角色: 超级管理员|HR经理|普通HR"
        string avatar "头像URL"
        number createdAt "创建时间"
    }

    Delivery {
        string id PK "投递记录ID"
        string candidateId FK "求职者ID"
        string positionId FK "职位ID"
        string companyId FK "公司ID"
        string resumeId FK "简历ID"
        string candidateName "求职者姓名(冗余)"
        string positionTitle "职位名称(冗余)"
        string companyName "公司名称(冗余)"
        string status "状态: 已投递|已查看|感兴趣|不合适|待面试|已发Offer|已接受"
        number deliveredAt "投递时间"
        number viewedAt "查看时间"
        string feedback "HR反馈"
        number createdAt "创建时间"
        number updatedAt "更新时间"
    }

    ChatMessage {
        string id PK "消息ID"
        string sessionId "会话ID (hr_xxx_candidate_xxx)"
        string senderId FK "发送方ID"
        string senderType "发送方类型: hr|candidate"
        string receiverId FK "接收方ID"
        string receiverType "接收方类型: hr|candidate"
        string type "消息类型: text|image|file|system|interview_invite"
        string content "消息内容"
        number timestamp "消息时间戳"
        string status "消息状态: sent|delivered|read"
        string relatedPositionId FK "关联职位ID"
    }
```

---

## 二、关系说明

| 关系 | 类型 | 说明 |
|------|------|------|
| CandidateUser → Resume | **1:1** | 每个求职者拥有一份简历 |
| CandidateUser → Delivery | **1:N** | 一个求职者可投递多个职位 |
| CandidateUser → RealNameAuth | **1:1** | 每个求职者有一条实名认证记录 |
| Resume → WorkExperience | **1:N** | 简历包含多条工作经历（组合） |
| Resume → Project | **1:N** | 简历包含多条项目经历（组合） |
| Company → Position | **1:N** | 一个公司可发布多个职位 |
| Company → HRUser | **1:N** | 一个公司有多个 HR 账号 |
| Company → Delivery | **1:N** | 公司被多次投递 |
| Position → Delivery | **1:N** | 一个职位被多次投递 |
| Position → ChatMessage | **1:N** (可选) | 聊天消息可关联职位上下文 |
| CandidateUser → ChatMessage | **1:N** | 求职者参与多条聊天消息 |
| HRUser → ChatMessage | **1:N** | HR 参与多条聊天消息 |

> **注意**: ChatMessage 的 `senderId`/`receiverId` 是多态外键——根据 `senderType`/`receiverType` 分别指向 `CandidateUser` 或 `HRUser`。

---

## 三、枚举值速查

### 3.1 DeliveryStatus（投递状态流转）

```mermaid
stateDiagram-v2
    [*] --> APPLIED: 求职者投递
    APPLIED --> VIEWED: HR查看简历
    VIEWED --> INTERESTED: HR标记感兴趣
    VIEWED --> NOT_INTERESTED: HR标记不合适
    INTERESTED --> INTERVIEW: 预约面试
    INTERVIEW --> OFFER: HR发放Offer
    OFFER --> ACCEPTED: 求职者接受
    NOT_INTERESTED --> [*]
    ACCEPTED --> [*]
```

### 3.2 其他枚举

| 枚举 | 值 |
|------|-----|
| **CompanyStatus** | `待审核` → `正常` / `封禁` |
| **PositionStatus** | `草稿` → `待审核` → `已发布` → `已关闭` / `封禁` |
| **MessageType** | `text` / `image` / `file` / `system` / `interview_invite` |
| **MessageStatus** | `sent` → `delivered` → `read` |
| **UserType** | `admin` / `hr` / `candidate` |
| **RealNameAuthStatus** | `not_submitted` → `pending` → `approved` / `rejected` |

---

## 四、关键字段设计约定

| 约定 | 说明 |
|------|------|
| 主键 ID | 全部使用 `string` 类型（如 `candidate_001`, `company_001`） |
| 时间戳 | Unix 毫秒时间戳 (`number`)，如 `1711900800000` |
| 薪资 | 拆分为 `salaryMin`(K) + `salaryMax`(K) + `salaryMonth`(月数)，展示时通过 `formatSalary()` 拼接为 `"25-35K·14薪"` |
| 会话 ID | `generateSessionId(hrId, candidateId)` → `"hr_{hrId}_candidate_{candidateId}"` |
| 冗余字段 | Delivery、Position、HRUser 中保留冗余的 `companyName`、`candidateName`、`positionTitle` 等字段以减少 JOIN 查询 |

---

> **使用说明**: 本 Mermaid ER 图可在 GitHub、Notion、飞书文档、VS Code（安装 Mermaid 插件）等支持 Mermaid 渲染的工具中直接查看和编辑。纯文本格式，可直接复制修改。
