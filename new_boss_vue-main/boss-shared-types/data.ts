/**
 * BOSS 直聘三端共享静态数据
 * 确保三端使用相同的模拟数据，保持业务流程配套
 */

import { 
  Company, Position, ChatMessage, UserType, MessageType, MessageStatus,
  CompanyStatus, PositionStatus, DeliveryStatus 
} from './index';

// ==================== 企业数据 ====================
export const companies: Company[] = [
  {
    id: 'company_001',
    name: '示例科技有限公司',
    industry: '互联网/软件',
    scale: '100-500 人',
    stage: 'B 轮',
    city: '上海',
    district: '浦东新区',
    address: '张江高科技园区',
    description: '示例科技是一家专注于企业服务的科技公司，致力于为企业提供高效的数字化解决方案。',
    status: CompanyStatus.ACTIVE,
    createdAt: 1711900800000, // 2024-04-01
    updatedAt: 1711900800000
  },
  {
    id: 'company_002',
    name: '某某信息科技公司',
    industry: '互联网/电商',
    scale: '500-1000 人',
    stage: 'C 轮',
    city: '北京',
    district: '朝阳区',
    address: '中关村科技园',
    description: '某某信息科技是一家领先的电商服务公司。',
    status: CompanyStatus.ACTIVE,
    createdAt: 1711814400000,
    updatedAt: 1711814400000
  },
  {
    id: 'company_003',
    name: '科技创新公司',
    industry: '人工智能',
    scale: '50-100 人',
    stage: 'A 轮',
    city: '深圳',
    district: '南山区',
    address: '深圳湾科技园',
    description: '专注于人工智能技术研发。',
    status: CompanyStatus.PENDING,
    createdAt: 1711728000000,
    updatedAt: 1711728000000
  }
];

// ==================== 职位数据 ====================
export const positions: Position[] = [
  {
    id: 'position_001',
    companyId: 'company_001',
    companyName: '示例科技有限公司',
    title: '高级前端工程师',
    department: '技术部',
    city: '上海',
    district: '浦东新区',
    salaryMin: 25,
    salaryMax: 35,
    salaryMonth: 14,
    experience: '3-5 年',
    education: '本科',
    number: 5,
    tags: ['五险一金', '带薪年假', '弹性工作', '周末双休'],
    description: `岗位职责：
1. 负责公司核心产品的前端架构设计和开发
2. 主导前端性能优化，提升用户体验
3. 搭建组件库，提高团队开发效率
4. 指导初级工程师，组织技术分享`,
    requirements: `任职要求：
1. 计算机相关专业本科及以上学历
2. 3-5 年前端开发经验
3. 精通 Vue.js/React 等主流框架
4. 熟悉 TypeScript、Webpack 等工具
5. 具备良好的团队协作和沟通能力`,
    welfare: ['五险一金', '带薪年假', '弹性工作', '周末双休', '年终奖', '股票期权'],
    status: PositionStatus.ACTIVE,
    views: 1256,
    communicates: 89,
    resumes: 34,
    publishedAt: 1711900800000,
    createdAt: 1711900800000,
    updatedAt: 1711900800000
  },
  {
    id: 'position_002',
    companyId: 'company_002',
    companyName: '某某信息科技公司',
    title: '产品经理',
    department: '产品部',
    city: '北京',
    district: '朝阳区',
    salaryMin: 20,
    salaryMax: 30,
    salaryMonth: 14,
    experience: '3-5 年',
    education: '本科',
    number: 3,
    tags: ['年终奖', '定期体检', '股票期权'],
    description: '负责产品规划和设计。',
    requirements: '要求有 3 年以上产品经验。',
    welfare: ['年终奖', '定期体检', '股票期权'],
    status: PositionStatus.ACTIVE,
    views: 982,
    communicates: 67,
    resumes: 28,
    publishedAt: 1711814400000,
    createdAt: 1711814400000,
    updatedAt: 1711814400000
  },
  {
    id: 'position_003',
    companyId: 'company_001',
    companyName: '示例科技有限公司',
    title: 'Java 开发工程师',
    department: '技术部',
    city: '上海',
    district: '浦东新区',
    salaryMin: 18,
    salaryMax: 28,
    salaryMonth: 13,
    experience: '1-3 年',
    education: '本科',
    number: 10,
    tags: ['周末双休', '加班补助', '包住'],
    description: '负责后端开发。',
    requirements: '熟悉 Java、Spring Boot。',
    welfare: ['周末双休', '加班补助', '包住'],
    status: PositionStatus.ACTIVE,
    views: 856,
    communicates: 52,
    resumes: 19,
    publishedAt: 1711728000000,
    createdAt: 1711728000000,
    updatedAt: 1711728000000
  }
];

// ==================== 聊天消息数据 ====================
export const messages: ChatMessage[] = [
  {
    id: 'msg_001',
    sessionId: 'hr_hr001_candidate_cand001',
    senderId: 'hr001',
    senderType: UserType.HR,
    receiverId: 'cand001',
    receiverType: UserType.CANDIDATE,
    type: MessageType.TEXT,
    content: '您好，看到您投递了我们的职位',
    timestamp: 1711900800000,
    status: MessageStatus.READ,
    relatedPositionId: 'position_001'
  },
  {
    id: 'msg_002',
    sessionId: 'hr_hr001_candidate_cand001',
    senderId: 'cand001',
    senderType: UserType.CANDIDATE,
    receiverId: 'hr001',
    receiverType: UserType.HR,
    type: MessageType.TEXT,
    content: '您好，我对这个职位很感兴趣',
    timestamp: 1711901100000,
    status: MessageStatus.READ,
    relatedPositionId: 'position_001'
  },
  {
    id: 'msg_003',
    sessionId: 'hr_hr001_candidate_cand001',
    senderId: 'hr001',
    senderType: UserType.HR,
    receiverId: 'cand001',
    receiverType: UserType.CANDIDATE,
    type: MessageType.TEXT,
    content: '您的简历我们已经收到了，觉得比较匹配。请问您什么时候方便面试？',
    timestamp: 1711901400000,
    status: MessageStatus.READ,
    relatedPositionId: 'position_001'
  },
  {
    id: 'msg_004',
    sessionId: 'hr_hr001_candidate_cand001',
    senderId: 'hr001',
    senderType: UserType.HR,
    receiverId: 'cand001',
    receiverType: UserType.CANDIDATE,
    type: MessageType.SYSTEM,
    content: '交换了电话',
    timestamp: 1711901700000,
    status: MessageStatus.READ
  },
  {
    id: 'msg_005',
    sessionId: 'hr_hr001_candidate_cand001',
    senderId: 'cand001',
    senderType: UserType.CANDIDATE,
    receiverId: 'hr001',
    receiverType: UserType.HR,
    type: MessageType.TEXT,
    content: '我这周三或周四下午都可以',
    timestamp: 1711902000000,
    status: MessageStatus.DELIVERED,
    relatedPositionId: 'position_001'
  }
];

// ==================== HR 用户数据 ====================
export const hrUsers = [
  {
    id: 'hr001',
    username: 'zhangsan',
    phone: '13800138000',
    realName: '张经理',
    companyId: 'company_001',
    companyName: '示例科技有限公司',
    role: 'HR 经理' as const,
    avatar: '',
    createdAt: 1711900800000
  }
];

// ==================== 求职者用户数据 ====================
export const candidateUsers = [
  {
    id: 'cand001',
    phone: '13900139000',
    name: '李先生',
    avatar: '',
    resumeStatus: '完善中' as const,
    createdAt: 1711814400000
  }
];

// ==================== 管理员用户数据 ====================
export const adminUsers = [
  {
    id: 'admin001',
    username: 'admin',
    realName: '超级管理员',
    role: '超级管理员' as const,
    createdAt: 1711900800000
  }
];
