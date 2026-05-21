# BOSS 直聘三端共享类型和数据

这个包包含了 BOSS 直聘三端（管理端、企业端、求职者端）共享的类型定义和静态数据，确保三端的字段和模型完全配套。

## 📦 目录结构

```
boss-shared-types/
├── index.ts          # 类型定义和工具函数
├── data.ts           # 共享的静态数据
├── package.json      # 包配置
└── README.md         # 使用说明
```

## 🚀 使用方法

### 1. 导入类型定义

```typescript
// 在 Vue 组件中
import { 
  Company, Position, ChatMessage, 
  CompanyStatus, PositionStatus, UserType,
  formatSalary, formatTime 
} from './shared-types'

// 使用类型定义
const company: Company = {
  id: 'company_001',
  name: '示例科技有限公司',
  industry: '互联网/软件',
  scale: '100-500 人',
  status: CompanyStatus.ACTIVE,
  createdAt: 1711900800000,
  updatedAt: 1711900800000
}

// 使用工具函数
const salaryDisplay = formatSalary(25, 35, 14)  // "25-35K·14 薪"
const timeDisplay = formatTime(1711900800000)   // "刚刚" 或具体日期
```

### 2. 导入静态数据

```typescript
import { companies, positions, messages } from './shared-types/data'

// 直接使用统一的静态数据
const companyList = companies
const positionList = positions
const messageList = messages
```

## 📋 核心类型

### 状态枚举

- `CompanyStatus` - 企业状态（待审核、正常、封禁）
- `PositionStatus` - 职位状态（草稿、待审核、已发布等）
- `DeliveryStatus` - 投递状态（已投递、已查看等）
- `MessageType` - 消息类型（文本、图片、系统等）
- `MessageStatus` - 消息状态（已发送、已送达、已读）
- `UserType` - 用户类型（管理员、HR、求职者）

### 数据接口

- `Company` - 企业
- `Position` - 职位
- `HRUser` - HR 用户
- `CandidateUser` - 求职者用户
- `AdminUser` - 管理员用户
- `ChatMessage` - 聊天消息
- `Resume` - 简历
- `Delivery` - 投递记录

### 工具函数

- `formatSalary(min, max, month)` - 格式化薪资显示
- `formatTime(timestamp)` - 格式化时间显示
- `generateSessionId(hrId, candidateId)` - 生成会话 ID

## ✅ 修复清单

已完成的修复：

### 求职者端 (boss-candidate-ui)
- ✅ JobDetail.vue - 使用统一的职位数据结构
  - 添加 `companyId` 和 `companyName`
  - 薪资分三个字段存储 (`salaryMin`, `salaryMax`, `salaryMonth`)
  - 使用 `city` 替代 `location`
  - 使用时间戳而非相对时间
  - 添加计算属性显示薪资和时间

- ✅ ChatWindow.vue - 使用统一的消息结构
  - 使用 `senderType` 替代 `isSelf`
  - 使用时间戳替代字符串时间
  - 添加 `sessionId` 和 `relatedPositionId`
  - 使用枚举值 `UserType` 和 `MessageType`

### 企业端 (boss-company-ui)
- ✅ PublishPosition.vue - 保持统一的字段命名
  - 薪资字段已经是三个独立字段 ✅
  - 添加格式化工具函数引用

### 管理端 (boss-manage-ui)
- ✅ Companies.vue - 使用统一的数据结构和枚举
  - 使用 `CompanyStatus` 枚举
  - ID 改为字符串格式
  - 时间改为时间戳
  - 添加 `district` 字段
  - 使用统一的格式化函数

## 🎯 关键改进点

### 1. 字段命名统一
```typescript
// ❌ 修改前
{
  company: '示例科技有限公司',  // 直接是字符串
  salary: '25-35K·14 薪',       // 组合字符串
  location: '上海'              // 不统一
}

// ✅ 修改后
{
  companyId: 'company_001',     // 统一用 ID
  companyName: '示例科技有限公司',
  salaryMin: 25,                // 分字段存储
  salaryMax: 35,
  salaryMonth: 14,
  city: '上海'                  // 统一用 city
}
```

### 2. 时间格式统一
```typescript
// ❌ 修改前
createdAt: '2026-03-01'    // 字符串
publishTime: '2 小时前'     // 相对时间

// ✅ 修改后
createdAt: 1711900800000   // 毫秒时间戳
publishedAt: 1711900800000

// 显示时用工具函数格式化
formatTime(1711900800000)  // "刚刚" 或 "2 小时前" 或 "2024-04-01"
```

### 3. 状态枚举统一
```typescript
// ❌ 修改前
status: '正常'    // 字符串，可能不一致

// ✅ 修改后
status: CompanyStatus.ACTIVE  // 使用枚举
```

### 4. 聊天消息结构统一
```typescript
// ❌ 修改前
{
  type: 'sent',     // 含义不明
  time: '10:20',    // 字符串时间
  isSelf: false     // 无法区分 HR/候选人
}

// ✅ 修改后
{
  senderType: UserType.HR,    // 明确的发送者类型
  timestamp: 1711900800000,   // 统一时间戳
  sessionId: 'hr_001_cand_001' // 会话 ID
}
```

## 📝 下一步

建议继续修复：

1. **企业端 Dashboard** - 使用统一的 Position 和 Company 数据
2. **求职者端首页** - 使用统一的 Position 列表
3. **管理端职位列表** - 使用统一的 PositionStatus
4. **所有聊天相关页面** - 使用统一的 ChatMessage 结构

## 🔗 相关链接

- [三端统一数据模型规范](../三端统一数据模型规范.md)
- [三端字段映射对照表](../三端字段映射对照表.md)
- [BOSS 直聘三端原型检查最终结论](../BOSS 直聘三端原型检查最终结论.md)
