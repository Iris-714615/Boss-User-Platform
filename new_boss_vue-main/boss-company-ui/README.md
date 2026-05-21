# Boss直聘企业端 - 招聘管理系统

## 项目简介

这是一个仿 Boss直聘企业端的招聘管理系统，采用 Vue 3 + Vite + Element Plus 技术栈开发。系统提供了完整的招聘管理功能，包括职位管理、简历筛选、在线沟通等核心模块。

## 技术栈

- **前端框架**: Vue 3.5.22
- **构建工具**: Vite 4.5.14
- **UI 组件库**: Element Plus 2.10.2
- **路由管理**: Vue Router 4.6.3
- **状态管理**: Pinia 2.3.0
- **HTTP 请求**: Axios 1.10.0
- **图标库**: @element-plus/icons-vue

## 功能模块

### 1. 登录模块 (`/login`)
- 账号密码登录
- 记住账号功能
- 登录状态持久化
- 路由守卫保护

### 2. 招聘管理首页 (`/company/dashboard`)
- 今日概览数据卡片（在招职位、沟通数、新收简历、待面试）
- 职位效果数据表格
- 今日待办事项时间轴
- 快捷入口

### 3. 职位管理 (`/company/positions`)
- 职位列表展示
- 多条件筛选（关键字、状态、城市）
- 职位详情查看
- 发布新职位
- 编辑职位
- 关闭/删除职位
- 批量导入功能

### 4. 简历中心 (`/company/resumes`)
- 简历列表展示
- 智能匹配度评分
- 多维度筛选（职位、学历、经验、状态）
- 简历详情查看
- 在线沟通
- 简历下载

### 5. 消息沟通 (`/company/chat`)
- 聊天列表
- 实时消息对话
- 未读消息提醒
- 在线状态显示
- 电话/视频面试邀请

### 6. 公司主页 (`/company/company-profile`)
- 公司信息展示
- 公司介绍编辑
- 公司标签管理

### 7. 数据看板 (`/company/data`)
- 核心指标卡片
- 数据趋势图表
- 职位效果排行榜

## 项目结构

```
boss-company-ui/
├── src/
│   ├── layouts/              # 布局组件
│   │   └── CompanyLayout.vue
│   ├── pages/                # 页面组件
│   │   ├── Login.vue
│   │   ├── dashboard/
│   │   │   └── Dashboard.vue
│   │   ├── positions/
│   │   │   ├── PositionList.vue
│   │   │   ├── PositionDetail.vue
│   │   │   └── PublishPosition.vue
│   │   ├── candidates/
│   │   │   ├── ResumeList.vue
│   │   │   └── ResumeDetail.vue
│   │   ├── communications/
│   │   │   ├── ChatList.vue
│   │   │   └── ChatWindow.vue
│   │   ├── company/
│   │   │   └── CompanyProfile.vue
│   │   └── data/
│   │       └── DataDashboard.vue
│   ├── router/               # 路由配置
│   │   └── index.js
│   ├── stores/               # Pinia 状态管理
│   │   └── user.js
│   ├── utils/                # 工具函数
│   │   └── request.js
│   ├── App.vue
│   ├── main.js
│   └── style.css
├── .env.development          # 开发环境配置
├── .env.production           # 生产环境配置
├── vite.config.js            # Vite 配置
├── package.json
└── index.html
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:3001

### 构建生产版本

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 默认登录信息

- **账号**: 任意手机号/邮箱
- **密码**: 任意 6 位以上密码

当前为演示版本，使用本地模拟登录，无需真实后端。

## 主要特性

### UI 设计
- 采用 Boss直聘品牌蓝色 (#0084ff) 作为主色调
- 响应式布局，适配不同屏幕尺寸
- 统一的卡片式设计风格
- 平滑的过渡动画效果

### 功能亮点
- ✅ 完整的招聘流程管理
- ✅ 智能人岗匹配评分
- ✅ 实时消息通知
- ✅ 数据可视化展示
- ✅ 多级路由权限控制
- ✅ Token 自动管理和刷新

### 待完善功能
- ⏳ 后端 API 对接
- ⏳ ECharts 数据图表集成
- ⏳ 文件上传功能
- ⏳ 视频面试功能
- ⏳ 批量操作功能

## 开发规范

### 代码风格
- 使用 Composition API (`<script setup>`)
- 统一使用中文注释
- 遵循 Vue 3 官方风格指南

### 命名规范
- 组件文件：PascalCase (如 `PositionList.vue`)
- 变量和函数：camelCase (如 `positionData`)
- 常量：UPPER_SNAKE_CASE (如 `API_BASE_URL`)

## 浏览器支持

- Chrome >= 90
- Firefox >= 88
- Safari >= 14
- Edge >= 90

## License

MIT

---

**注意**: 本项目仅用于学习和交流，请勿用于商业用途。
