# BOSS 直聘求职者端 - 项目说明

## 📱 项目简介

BOSS 直聘求职者端是一个仿 BOSS 直聘平台的求职者应用，采用 Vue 3 + Vite + Element Plus 技术栈开发。系统提供了完整的求职功能，包括职位搜索、简历管理、在线沟通等核心模块。

## 🛠️ 技术栈

- **前端框架**: Vue 3.5.22
- **构建工具**: Vite 4.5.14
- **UI 组件库**: Element Plus 2.10.2
- **路由管理**: Vue Router 4.6.3
- **HTTP 请求**: Axios 1.10.0
- **图标库**: @element-plus/icons-vue

## 🚀 快速开始

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:3002

### 构建生产版本

```bash
npm run build
```

## 📁 项目结构

```
boss-candidate-ui/
├── src/
│   ├── layouts/              # 布局组件
│   │   └── CandidateLayout.vue
│   ├── pages/                # 页面组件
│   │   ├── Login.vue         # 登录页
│   │   ├── Home.vue          # 首页
│   │   ├── jobs/             # 职位相关
│   │   │   ├── JobList.vue
│   │   │   └── JobDetail.vue
│   │   ├── chat/             # 聊天相关
│   │   │   ├── Chat.vue
│   │   │   └── ChatWindow.vue
│   │   ├── resume/           # 简历
│   │   ├── delivery/         # 投递记录
│   │   ├── favorites/        # 收藏
│   │   └── profile/          # 个人中心
│   ├── router/               # 路由配置
│   ├── utils/                # 工具函数
│   ├── App.vue
│   ├── main.js
│   └── style.css
├── .env.development
├── .env.production
├── vite.config.js
└── package.json
```

## 🎯 核心功能

### 1. 用户登录
- 手机号密码登录
- 记住账号功能
- 登录状态持久化

### 2. 首页
- 智能职位推荐
- 热门搜索标签
- 热门城市选择

### 3. 职位模块
- 职位列表展示
- 多维度筛选（城市、薪资、经验）
- 职位详情查看
- 一键投递简历

### 4. 在线沟通
- 与 HR 实时聊天
- 消息列表展示
- 未读消息提醒

### 5. 简历管理
- 在线简历创建
- 简历完善度提示

### 6. 投递记录
- 查看投递状态
- 面试邀请管理

### 7. 收藏功能
- 收藏职位和职位

### 8. 个人中心
- 个人信息管理
- 账号设置

## 🔐 默认登录信息

当前为演示版本，使用本地模拟登录：
- **手机号**: 任意 11 位手机号
- **密码**: 6 位以上任意密码

## 📊 端口配置

- 开发环境：http://localhost:3002
- API 代理：/api → http://localhost:8080

## 🎨 UI 设计

### 主色调
- Boss 直聘蓝：#0084ff

### 底部导航
采用移动端经典的底部 Tab 导航设计：
- 首页
- 职位
- 消息
- 简历
- 我的

## 📝 开发规范

### 代码风格
- 使用 Composition API (`<script setup>`)
- 统一使用中文注释
- 遵循 Vue 3 官方风格指南

### 命名规范
- 组件文件：PascalCase
- 变量和函数：camelCase
- 常量：UPPER_SNAKE_CASE

## ⏳ 待完善功能

以下功能已规划但尚未完全实现：
- 验证码登录
- 简历完整编辑功能
- 投递记录详细展示
- 收藏列表
- 视频面试
- 实名认证

## 🌐 浏览器支持

- Chrome >= 90
- Firefox >= 88
- Safari >= 14
- Edge >= 90

## 📄 License

MIT

---

**注意**: 本项目仅用于学习和交流，请勿用于商业用途。
