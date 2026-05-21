<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  ArrowLeft, 
  Edit, 
  DocumentCopy, 
  ChatDotRound, 
  Share, 
  MoreFilled,
  Location,
  User,
  School,
  Briefcase,
  Money
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { PositionStatus, formatSalary, formatTime } from 'shared-types'

const route = useRoute()
const router = useRouter()

// 使用统一的职位数据结构
const position = ref({
  id: route.params.id,
  title: '高级前端工程师',
  department: '技术部',
  city: '上海',
  district: '浦东新区',
  salaryMin: 25,           // ✅ 分字段存储
  salaryMax: 35,
  salaryMonth: 14,
  experience: '3-5 年',
  education: '本科',
  status: PositionStatus.ACTIVE,  // ✅ 使用枚举
  publishDate: 1710460800000,     // ✅ 时间戳
  updateDate: 1711900800000,
  views: 1256,
  communicates: 89,
  resumes: 34,
  favorites: 156,
  description: `岗位职责：
1. 负责公司 Web 产品的前端开发和维护
2. 参与产品需求分析，技术方案设计
3. 优化前端性能和用户体验
4. 配合后端工程师完成接口联调

任职要求：
1. 计算机相关专业本科及以上学历
2. 3-5 年前端开发经验
3. 精通 Vue/React 等主流框架
4. 熟悉 TypeScript、Webpack 等工具
5. 具备良好的沟通能力和团队协作精神`,
  tags: ['五险一金', '带薪年假', '弹性工作', '定期体检', '年终奖']
})

const stats = ref([
  { label: '查看次数', value: 1256, trend: '+12%' },
  { label: '主动沟通', value: 89, trend: '+5%' },
  { label: '收到简历', value: 34, trend: '+8' },
  { label: '收藏人数', value: 156, trend: '+23' }
])

const relatedCandidates = ref([
  { 
    id: 1, 
    name: '张三', 
    avatar: '', 
    currentCompany: '某互联网公司', 
    position: '前端工程师', 
    experience: '4 年', 
    education: '本科',
    status: '在职 - 看看机会',
    matchRate: 95
  },
  { 
    id: 2, 
    name: '李四', 
    avatar: '', 
    currentCompany: '某科技公司', 
    position: '高级前端开发', 
    experience: '5 年', 
    education: '本科',
    status: '离职 - 随时到岗',
    matchRate: 92
  },
  { 
    id: 3, 
    name: '王五', 
    avatar: '', 
    currentCompany: '某网络公司', 
    position: 'Web 开发工程师', 
    experience: '3 年', 
    education: '本科',
    status: '在职 - 月内到岗',
    matchRate: 88
  }
])

const goBack = () => {
  router.back()
}

const onEdit = () => {
  router.push(`/company/positions/edit/${position.value.id}`)
}

const onResume = () => {
  router.push('/company/resumes')
}

const onChat = () => {
  router.push('/company/chat')
}

const onShare = () => {
  ElMessage.success('分享功能开发中')
}

const getStatusType = (status) => {
  if (status === PositionStatus.ACTIVE) return 'success'
  if (status === PositionStatus.PENDING) return 'warning'
  if (status === PositionStatus.CLOSED) return 'info'
  return 'info'
}
</script>

<template>
  <div class="position-detail-container">
    <!-- 头部导航 -->
    <el-card shadow="never" class="nav-card">
      <div class="nav-content">
        <div class="nav-left">
          <el-button text @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
          <el-divider direction="vertical" />
          <span class="page-title">职位详情</span>
        </div>
        <div class="nav-right">
          <el-button type="primary" @click="onEdit">
            <el-icon><Edit /></el-icon>
            编辑职位
          </el-button>
          <el-button @click="onResume">
            <el-icon><DocumentCopy /></el-icon>
            查看简历
          </el-button>
          <el-button @click="onChat">
            <el-icon><ChatDotRound /></el-icon>
            沟通知情人
          </el-button>
          <el-button text @click="onShare">
            <el-icon><Share /></el-icon>
          </el-button>
          <el-button text>
            <el-icon><MoreFilled /></el-icon>
          </el-button>
        </div>
      </div>
    </el-card>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <!-- 左侧主要内容 -->
      <el-col :span="16">
        <!-- 职位基本信息 -->
        <el-card shadow="never" class="info-card">
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
              <el-tag :type="getStatusType(position.status)" size="small">
                {{ position.status }}
              </el-tag>
            </div>
          </template>
          
          <div class="position-header">
            <h1 class="position-title">{{ position.title }}</h1>
            <div class="position-meta">
              <span><el-icon><Location /></el-icon> {{ position.city }} · {{ position.district }}</span>
              <span><el-icon><Money /></el-icon> {{ position.salary }}</span>
              <span><el-icon><Briefcase /></el-icon> {{ position.experience }}</span>
              <span><el-icon><School /></el-icon> {{ position.education }}</span>
            </div>
          </div>
          
          <el-divider />
          
          <div class="tags-section">
            <div class="section-label">职位标签：</div>
            <el-tag v-for="(tag, index) in position.tags" :key="index" size="small" style="margin-right: 8px">
              {{ tag }}
            </el-tag>
          </div>
          
          <el-divider />
          
          <div class="publish-info">
            <span>发布时间：{{ position.publishDate }}</span>
            <span>更新时间：{{ position.updateDate }}</span>
            <span>职位 ID: {{ position.id }}</span>
          </div>
        </el-card>
        
        <!-- 职位描述 -->
        <el-card shadow="never" class="desc-card" style="margin-top: 20px">
          <template #header>
            <span>职位描述</span>
          </template>
          
          <div class="position-description">
            <pre>{{ position.description }}</pre>
          </div>
        </el-card>
      </el-col>
      
      <!-- 右侧数据和推荐 -->
      <el-col :span="8">
        <!-- 效果数据 -->
        <el-card shadow="never" class="stats-card">
          <template #header>
            <span>📊 效果数据（近 7 日）</span>
          </template>
          
          <div class="stats-grid">
            <div v-for="(stat, index) in stats" :key="index" class="stat-item">
              <div class="stat-label">{{ stat.label }}</div>
              <div class="stat-value">
                {{ stat.value }}
                <span class="stat-trend">{{ stat.trend }}</span>
              </div>
            </div>
          </div>
        </el-card>
        
        <!-- 推荐候选人 -->
        <el-card shadow="never" class="candidates-card" style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <span>🎯 推荐候选人</span>
              <el-button type="primary" link size="small">查看全部</el-button>
            </div>
          </template>
          
          <div class="candidate-list">
            <div 
              v-for="candidate in relatedCandidates" 
              :key="candidate.id"
              class="candidate-item"
              @click="router.push(`/company/resumes/${candidate.id}`)"
            >
              <div class="candidate-header">
                <el-avatar :size="40" :src="candidate.avatar">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <div class="match-rate">{{ candidate.matchRate }}% 匹配</div>
              </div>
              
              <div class="candidate-info">
                <div class="candidate-name">{{ candidate.name }}</div>
                <div class="candidate-position">{{ candidate.position }}</div>
                <div class="candidate-company">{{ candidate.currentCompany }}</div>
              </div>
              
              <div class="candidate-tags">
                <el-tag size="small" type="info">{{ candidate.experience }}</el-tag>
                <el-tag size="small" type="info">{{ candidate.education }}</el-tag>
              </div>
              
              <div class="candidate-status">{{ candidate.status }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.position-detail-container {
  padding: 0;
}

.nav-card {
  margin-bottom: 16px;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-left {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.page-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.nav-right {
  display: flex;
  gap: 12px;
}

.info-card, .desc-card, .stats-card, .candidates-card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.position-header {
  margin-bottom: 20px;
}

.position-title {
  font-size: 24px;
  color: #303133;
  margin: 0 0 16px 0;
}

.position-meta {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #606266;
}

.position-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.tags-section {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
}

.section-label {
  font-size: 14px;
  color: #909399;
  margin-right: 12px;
  line-height: 32px;
}

.publish-info {
  display: flex;
  gap: 24px;
  font-size: 13px;
  color: #909399;
}

.position-description pre {
  font-family: inherit;
  white-space: pre-wrap;
  line-height: 1.8;
  color: #606266;
  font-size: 14px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.stat-trend {
  font-size: 12px;
  color: #67C23A;
}

.candidate-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.candidate-item {
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.candidate-item:hover {
  border-color: #0084ff;
  box-shadow: 0 2px 12px rgba(0, 132, 255, 0.1);
  transform: translateY(-2px);
}

.candidate-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.match-rate {
  font-size: 12px;
  color: #67C23A;
  font-weight: 600;
}

.candidate-info {
  margin-bottom: 8px;
}

.candidate-name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.candidate-position {
  font-size: 13px;
  color: #606266;
  margin-bottom: 4px;
}

.candidate-company {
  font-size: 13px;
  color: #909399;
}

.candidate-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.candidate-status {
  font-size: 12px;
  color: #909399;
}
</style>
