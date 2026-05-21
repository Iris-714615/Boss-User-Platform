/**
 * BOSS 直聘三端共享类型定义
 * 确保管理端、企业端、求职者端使用统一的数据模型
 */

// ==================== 状态枚举 ====================

/** 企业状态 */
export enum CompanyStatus {
  PENDING = '待审核',
  ACTIVE = '正常',
  BANNED = '封禁'
}

/** 职位状态 */
export enum PositionStatus {
  DRAFT = '草稿',
  PENDING = '待审核',
  ACTIVE = '已发布',
  CLOSED = '已关闭',
  BANNED = '封禁'
}

/** 投递状态 */
export enum DeliveryStatus {
  APPLIED = '已投递',
  VIEWED = '已查看',
  INTERESTED = '感兴趣',
  NOT_INTERESTED = '不合适',
  INTERVIEW = '待面试',
  OFFER = '已发 Offer',
  ACCEPTED = '已接受'
}

/** 消息类型 */
export enum MessageType {
  TEXT = 'text',
  IMAGE = 'image',
  FILE = 'file',
  SYSTEM = 'system',
  INTERVIEW_INVITE = 'interview_invite'
}

/** 消息状态 */
export enum MessageStatus {
  SENT = 'sent',
  DELIVERED = 'delivered',
  READ = 'read'
}

/** 用户类型 */
export enum UserType {
  ADMIN = 'admin',
  HR = 'hr',
  CANDIDATE = 'candidate'
}

// ==================== 核心业务实体 ====================

/** 企业 */
export interface Company {
  id: string              // 企业 ID（全局唯一）
  name: string            // 企业名称
  industry: string        // 行业
  scale: string           // 规模（如"100-500 人"）
  stage?: string          // 融资阶段（如"B 轮"）
  city: string            // 城市
  district?: string       // 区县
  address?: string        // 详细地址
  description?: string    // 企业简介
  logo?: string           // 企业 logo URL
  status: CompanyStatus   // 企业状态
  createdAt: number       // 创建时间戳
  updatedAt: number       // 更新时间戳
}

/** 职位 */
export interface Position {
  // 基本信息
  id: string              // 职位 ID
  companyId: string       // 所属企业 ID
  companyName: string     // 企业名称（冗余字段，方便显示）
  title: string           // 职位名称
  department: string      // 所属部门
  
  // 工作地点
  city: string            // 工作城市
  district?: string       // 工作区县
  address?: string        // 详细地址
  
  // 薪资（存储用 K 为单位）
  salaryMin: number       // 最低薪资 (K)
  salaryMax: number       // 最高薪资 (K)
  salaryMonth: number     // 月薪数
  
  // 要求
  experience: string      // 经验要求
  education: string       // 学历要求
  gender?: string         // 性别要求
  
  // 其他
  number: number          // 招聘人数
  tags: string[]          // 职位标签
  description: string     // 职位描述
  requirements: string    // 任职要求
  welfare: string[]       // 福利待遇
  
  // 状态与统计
  status: PositionStatus  // 职位状态
  publishedAt?: number    // 发布时间戳
  views: number           // 查看次数
  communicates: number    // 主动沟通数
  resumes: number         // 收到简历数
  
  // 时间戳
  createdAt: number       // 创建时间戳
  updatedAt: number       // 更新时间戳
}

/** HR 用户（企业端） */
export interface HRUser {
  id: string
  username: string
  phone: string
  realName: string
  companyId: string
  companyName: string
  role: '超级管理员' | 'HR 经理' | '普通 HR'
  avatar?: string
  createdAt: number
}

/** 求职者用户（求职者端） */
export interface CandidateUser {
  id: string
  phone: string
  name: string
  avatar?: string
  resumeStatus: '未完善' | '完善中' | '已完成'
  createdAt: number
}

/** 管理员用户（管理端） */
export interface AdminUser {
  id: string
  username: string
  realName: string
  role: '超级管理员' | '普通管理员'
  createdAt: number
}

/** 聊天消息 */
export interface ChatMessage {
  id: string              // 消息 ID
  sessionId: string       // 会话 ID（格式："hr_{hrId}_candidate_{candidateId}"）
  senderId: string        // 发送者 ID
  senderType: UserType.HR | UserType.CANDIDATE  // 发送者类型
  receiverId: string      // 接收者 ID
  receiverType: UserType.HR | UserType.CANDIDATE  // 接收者类型
  type: MessageType       // 消息类型
  content: string         // 消息内容
  timestamp: number       // 时间戳
  status: MessageStatus   // 消息状态
  relatedPositionId?: string  // 关联职位 ID
}

/** 工作经历 */
export interface WorkExperience {
  companyId: string
  companyName: string
  position: string
  startDate: number
  endDate?: number
  description?: string
}

/** 项目经历 */
export interface Project {
  name: string
  role: string
  startDate: number
  endDate?: number
  description?: string
  technologies?: string[]
}

/** 简历 */
export interface Resume {
  // 基本信息
  id: string
  candidateId: string
  name: string
  phone: string
  email?: string
  avatar?: string
  age?: number
  gender?: '男' | '女'
  city: string
  
  // 教育信息
  education: string
  graduationYear?: number
  major?: string
  
  // 工作信息
  experience: string
  workExperiences?: WorkExperience[]
  projects?: Project[]
  skills?: string[]
  
  // 求职意向
  expectedPosition?: string
  expectedCity?: string
  expectedSalary?: string
  
  // 其他
  selfIntroduce?: string
  status: '保密' | '公开'
  
  // 时间戳
  updatedAt: number
}

/** 投递记录 */
export interface Delivery {
  id: string
  candidateId: string
  positionId: string
  companyId: string
  resumeId: string
  
  // 冗余字段（方便显示）
  candidateName: string
  positionTitle: string
  companyName: string
  
  status: DeliveryStatus
  deliveredAt: number
  viewedAt?: number
  feedback?: string
  
  createdAt: number
  updatedAt: number
}

// ==================== 工具函数 ====================

/** 格式化薪资显示 */
export function formatSalary(min: number, max: number, month: number): string {
  return `${min}-${max}K·${month}薪`;
}

/** 格式化时间显示 */
export function formatTime(timestamp: number): string {
  const now = Date.now();
  const diff = now - timestamp;
  
  if (diff < 60000) return '刚刚';
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`;
  if (diff < 2592000000) return `${Math.floor(diff / 86400000)}天前`;
  
  return new Date(timestamp).toLocaleDateString('zh-CN');
}

/** 生成会话 ID */
export function generateSessionId(hrId: string, candidateId: string): string {
  return `hr_${hrId}_candidate_${candidateId}`;
}

// ==================== 示例数据 ====================

/** 示例职位数据 */
export const positions: Position[] = [
  {
    id: 'position_001',
    companyId: 'company_001',
    companyName: '示例科技有限公司',
    title: '高级前端工程师',
    department: '技术部',
    city: '北京',
    district: '海淀区',
    salaryMin: 25,
    salaryMax: 35,
    salaryMonth: 14,
    experience: '3-5 年',
    education: '本科',
    number: 3,
    tags: ['前端', 'Vue', 'React'],
    description: '负责公司核心产品的前端开发',
    requirements: '精通 Vue/React 框架，有大型项目经验',
    welfare: ['五险一金', '弹性工作', '年终奖'],
    status: PositionStatus.ACTIVE,
    views: 1250,
    communicates: 89,
    resumes: 45,
    createdAt: 1710460800000,
    updatedAt: 1711900800000,
    publishedAt: 1710547200000
  },
  {
    id: 'position_002',
    companyId: 'company_002',
    companyName: '某某信息科技公司',
    title: '产品经理',
    department: '产品部',
    city: '上海',
    district: '浦东新区',
    salaryMin: 20,
    salaryMax: 30,
    salaryMonth: 13,
    experience: '3-5 年',
    education: '本科',
    number: 2,
    tags: ['产品', 'B 端', 'SaaS'],
    description: '负责 B 端 SaaS 产品的规划与设计',
    requirements: '有 3 年以上 B 端产品经验，逻辑清晰',
    welfare: ['五险一金', '带薪年假', '定期体检'],
    status: PositionStatus.ACTIVE,
    views: 980,
    communicates: 67,
    resumes: 38,
    createdAt: 1709856000000,
    updatedAt: 1711814400000,
    publishedAt: 1709942400000
  },
  {
    id: 'position_003',
    companyId: 'company_003',
    companyName: '科技创新公司',
    title: 'Java 开发工程师',
    department: '研发部',
    city: '广州',
    district: '天河区',
    salaryMin: 18,
    salaryMax: 28,
    salaryMonth: 14,
    experience: '1-3 年',
    education: '本科',
    number: 5,
    tags: ['后端', 'Java', 'Spring'],
    description: '参与后端服务的设计与开发',
    requirements: '熟悉 Java、Spring Boot、MySQL',
    welfare: ['六险一金', '餐补', '节日福利'],
    status: PositionStatus.ACTIVE,
    views: 1560,
    communicates: 120,
    resumes: 78,
    createdAt: 1708646400000,
    updatedAt: 1711555200000,
    publishedAt: 1708732800000
  }
];

/** 示例企业数据 */
export const companies: Company[] = [
  {
    id: 'company_001',
    name: '示例科技有限公司',
    industry: '互联网/移动互联网',
    scale: '100-500 人',
    stage: 'B 轮',
    city: '北京',
    district: '海淀区',
    address: '中关村科技园',
    description: '专注于人工智能技术研发',
    logo: '',
    status: CompanyStatus.ACTIVE,
    createdAt: 1704067200000,
    updatedAt: 1711900800000
  },
  {
    id: 'company_002',
    name: '某某信息科技公司',
    industry: '计算机软件',
    scale: '50-100 人',
    stage: 'A 轮',
    city: '上海',
    district: '浦东新区',
    address: '张江高科技园区',
    description: '企业级 SaaS 服务提供商',
    logo: '',
    status: CompanyStatus.ACTIVE,
    createdAt: 1701388800000,
    updatedAt: 1711814400000
  },
  {
    id: 'company_003',
    name: '科技创新公司',
    industry: '互联网/移动互联网',
    scale: '500-1000 人',
    stage: 'C 轮',
    city: '广州',
    district: '天河区',
    address: '珠江新城',
    description: '领先的互联网金融科技公司',
    logo: '',
    status: CompanyStatus.ACTIVE,
    createdAt: 1698796800000,
    updatedAt: 1711555200000
  }
];

/** 示例求职者用户数据 */
export const candidateUsers: CandidateUser[] = [
  {
    id: 'candidate_001',
    phone: '13800138001',
    name: '张三',
    avatar: '',
    resumeStatus: '已完成',
    createdAt: 1704067200000
  },
  {
    id: 'candidate_002',
    phone: '13800138002',
    name: '李四',
    avatar: '',
    resumeStatus: '完善中',
    createdAt: 1706745600000
  },
  {
    id: 'candidate_003',
    phone: '13800138003',
    name: '王五',
    avatar: '',
    resumeStatus: '已完成',
    createdAt: 1709251200000
  }
];

/** 示例消息数据 */
export const messages: ChatMessage[] = [
  {
    id: 'msg_001',
    sessionId: 'hr_hr001_candidate_candidate_001',
    senderId: 'candidate_001',
    senderType: UserType.CANDIDATE,
    receiverId: 'hr001',
    receiverType: UserType.HR,
    type: MessageType.TEXT,
    content: '您好，请问您对这个职位感兴趣吗？',
    timestamp: 1711900800000,
    status: MessageStatus.READ,
    relatedPositionId: 'position_001'
  },
  {
    id: 'msg_002',
    sessionId: 'hr_hr001_candidate_candidate_002',
    senderId: 'hr001',
    senderType: UserType.HR,
    receiverId: 'candidate_002',
    receiverType: UserType.CANDIDATE,
    type: MessageType.TEXT,
    content: '您的简历我们已经收到了',
    timestamp: 1711814400000,
    status: MessageStatus.DELIVERED,
    relatedPositionId: 'position_002'
  },
  {
    id: 'msg_003',
    sessionId: 'hr_hr001_candidate_candidate_003',
    senderId: 'candidate_003',
    senderType: UserType.CANDIDATE,
    receiverId: 'hr001',
    receiverType: UserType.HR,
    type: MessageType.TEXT,
    content: '什么时候可以来面试？',
    timestamp: 1711555200000,
    status: MessageStatus.READ,
    relatedPositionId: 'position_003'
  }
];
