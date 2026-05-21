<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  ArrowLeft, 
  Download, 
  ChatDotRound, 
  Phone, 
  VideoCamera, 
  Calendar,
  User,
  School,
  Briefcase,
  Location,
  Money,
  Document
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()

const resume = ref({
  id: route.params.id,
  name: '张三',
  avatar: '',
  age: 28,
  gender: '男',
  phone: '138****0000',
  email: 'zhang***@example.com',
  currentCity: '上海',
  expectedCity: '上海',
  expectedPosition: '高级前端工程师',
  expectedSalary: '25-35K',
  education: '本科',
  experience: '4 年',
  workStatus: '在职 - 看看机会',
 到岗时间: '月内到岗',
  matchRate: 95,
  
  educationHistory: [
    {
      school: '上海交通大学',
      major: '计算机科学与技术',
      degree: '本科',
      startDate: '2014-09',
      endDate: '2018-06'
    }
  ],
  
  workExperience: [
    {
      company: '某知名互联网公司',
      position: '前端开发工程师',
      startDate: '2020-03',
      endDate: '至今',
      description: `1. 负责公司核心产品的前端架构设计和开发
2. 主导前端性能优化，页面加载速度提升 50%
3. 搭建组件库，提高团队开发效率
4. 指导初级工程师，组织技术分享`
    },
    {
      company: '某科技公司',
      position: 'Web 开发工程师',
      startDate: '2018-07',
      endDate: '2020-02',
      description: `1. 参与公司电商平台的前端开发
2. 使用 Vue.js 重构旧项目
3. 配合后端完成接口联调`
    }
  ],
  
  skills: [
    'HTML5/CSS3/JavaScript',
    'Vue.js/React',
    'TypeScript',
    'Node.js',
    'Webpack/Vite',
    'Git'
  ],
  
  selfEvaluation: `4 年前端开发经验，对前端技术有浓厚兴趣。熟练掌握 Vue.js 和 React 框架，有丰富的项目实战经验。具备良好的团队协作能力和沟通能力，能够快速适应新环境。工作认真负责，有较强的抗压能力。`,
  
  deliveryTime: '2026-03-31 10:30',
  deliveryPosition: '高级前端工程师'
})

const goBack = () => {
  router.back()
}

const onChat = () => {
  router.push(`/company/chat?userId=${resume.value.id}`)
}

const onPhone = () => {
  ElMessage.success('拨打电话功能开发中')
}

const onVideo = () => {
  ElMessage.success('视频面试功能开发中')
}

const onInterview = () => {
  ElMessage.success('安排面试功能开发中')
}

const onDownload = () => {
  ElMessage.success('简历下载功能开发中')
}

const handleStatus = async (status) => {
  try {
    await ElMessageBox.confirm(
      `确定将该候选人标记为"${status}"吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    ElMessage.success('操作成功')
  } catch {
    // 取消操作
  }
}
</script>

<template>
  <div class="resume-detail-container">
    <!-- 头部导航 -->
    <el-card shadow="never" class="nav-card">
      <div class="nav-content">
        <div class="nav-left">
          <el-button text @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
          <el-divider direction="vertical" />
          <span class="page-title">简历详情</span>
        </div>
        <div class="nav-right">
          <el-button type="primary" @click="onChat">
            <el-icon><ChatDotRound /></el-icon>
            立即沟通
          </el-button>
          <el-button @click="onPhone">
            <el-icon><Phone /></el-icon>
            打电话
          </el-button>
          <el-button @click="onVideo">
            <el-icon><VideoCamera /></el-icon>
            视频面试
          </el-button>
          <el-button @click="onInterview">
            <el-icon><Calendar /></el-icon>
            安排面试
          </el-button>
          <el-dropdown>
            <el-button>
              更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleStatus('待沟通')">标记待沟通</el-dropdown-item>
                <el-dropdown-item @click="handleStatus('不合适')">标记不合适</el-dropdown-item>
                <el-dropdown-item divided @click="onDownload">下载简历</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </el-card>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <!-- 左侧简历内容 -->
      <el-col :span="18">
        <!-- 基本信息 -->
        <el-card shadow="never" class="info-card">
          <div class="resume-header">
            <div class="header-left">
              <el-avatar :size="80" :src="resume.avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="header-info">
                <h1 class="name">{{ resume.name }}</h1>
                <div class="meta">
                  <span>{{ resume.age }}岁 · {{ resume.gender }}</span>
                  <span>{{ resume.education }} · {{ resume.experience }}</span>
                  <span>{{ resume.currentCity }}</span>
                </div>
                <div class="contact">
                  <span><el-icon><Phone /></el-icon> {{ resume.phone }}</span>
                  <span><el-icon><Document /></el-icon> {{ resume.email }}</span>
                </div>
              </div>
            </div>
            <div class="header-right">
              <div class="match-badge">
                <div class="match-rate">{{ resume.matchRate }}%</div>
                <div class="match-label">岗位匹配度</div>
              </div>
            </div>
          </div>
          
          <el-divider />
          
          <div class="expect-section">
            <div class="section-title">求职期望</div>
            <div class="expect-grid">
              <div class="expect-item">
                <el-icon><Location /></el-icon>
                <span>{{ resume.expectedCity }}</span>
              </div>
              <div class="expect-item">
                <el-icon><Briefcase /></el-icon>
                <span>{{ resume.expectedPosition }}</span>
              </div>
              <div class="expect-item">
                <el-icon><Money /></el-icon>
                <span>{{ resume.expectedSalary }}</span>
              </div>
              <div class="expect-item">
                <el-icon><Calendar /></el-icon>
                <span>{{ resume.workStatus }} · {{ resume.到岗时间 }}</span>
              </div>
            </div>
          </div>
        </el-card>
        
        <!-- 教育经历 -->
        <el-card shadow="never" class="section-card" style="margin-top: 20px">
          <template #header>
            <div class="section-header">
              <el-icon><School /></el-icon>
              <span>教育经历</span>
            </div>
          </template>
          
          <div v-for="(edu, index) in resume.educationHistory" :key="index" class="experience-item">
            <div class="exp-header">
              <div class="exp-title">{{ edu.school }}</div>
              <div class="exp-meta">{{ edu.major }} · {{ edu.degree }}</div>
            </div>
            <div class="exp-time">{{ edu.startDate }} - {{ edu.endDate }}</div>
          </div>
        </el-card>
        
        <!-- 工作经历 -->
        <el-card shadow="never" class="section-card" style="margin-top: 20px">
          <template #header>
            <div class="section-header">
              <el-icon><Briefcase /></el-icon>
              <span>工作经历</span>
            </div>
          </template>
          
          <div v-for="(work, index) in resume.workExperience" :key="index" class="experience-item">
            <div class="exp-header">
              <div class="exp-title">{{ work.company }}</div>
              <div class="exp-meta">{{ work.position }}</div>
            </div>
            <div class="exp-time">{{ work.startDate }} - {{ work.endDate }}</div>
            <div class="exp-desc">{{ work.description }}</div>
          </div>
        </el-card>
        
        <!-- 专业技能 -->
        <el-card shadow="never" class="section-card" style="margin-top: 20px">
          <template #header>
            <div class="section-header">
              <span>专业技能</span>
            </div>
          </template>
          
          <div class="skills-list">
            <el-tag v-for="(skill, index) in resume.skills" :key="index" size="default" style="margin-right: 12px; margin-bottom: 12px">
              {{ skill }}
            </el-tag>
          </div>
        </el-card>
        
        <!-- 自我评价 -->
        <el-card shadow="never" class="section-card" style="margin-top: 20px">
          <template #header>
            <div class="section-header">
              <span>自我评价</span>
            </div>
          </template>
          
          <div class="self-eval">
            {{ resume.selfEvaluation }}
          </div>
        </el-card>
      </el-col>
      
      <!-- 右侧投递信息 -->
      <el-col :span="6">
        <el-card shadow="never" class="delivery-card">
          <template #header>
            <span>投递信息</span>
          </template>
          
          <div class="delivery-info">
            <div class="info-row">
              <span class="label">投递职位：</span>
              <span class="value">{{ resume.deliveryPosition }}</span>
            </div>
            <div class="info-row">
              <span class="label">投递时间：</span>
              <span class="value">{{ resume.deliveryTime }}</span>
            </div>
            <div class="info-row">
              <span class="label">来源：</span>
              <span class="value">BOSS 直聘</span>
            </div>
          </div>
        </el-card>
        
        <el-card shadow="never" class="actions-card" style="margin-top: 20px">
          <template #header>
            <span>快捷操作</span>
          </template>
          
          <div class="quick-actions">
            <el-button type="primary" plain style="width: 100%; margin-bottom: 12px" @click="onChat">
              发起聊天
            </el-button>
            <el-button plain style="width: 100%; margin-bottom: 12px" @click="onPhone">
              打电话
            </el-button>
            <el-button plain style="width: 100%" @click="onInterview">
              安排面试
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.resume-detail-container {
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

.info-card, .section-card, .delivery-card, .actions-card {
  margin-bottom: 16px;
}

.resume-header {
  display: flex;
  justify-content: space-between;
}

.header-left {
  display: flex;
  gap: 20px;
}

.header-info {
  flex: 1;
}

.name {
  font-size: 24px;
  color: #303133;
  margin: 0 0 12px 0;
}

.meta {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.contact {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #909399;
}

.contact span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.match-badge {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #67C23A 0%, #95D46E 100%);
  border-radius: 12px;
  color: white;
}

.match-rate {
  font-size: 36px;
  font-weight: 700;
}

.match-label {
  font-size: 14px;
  opacity: 0.9;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
}

.expect-section {
  margin-top: 20px;
}

.expect-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.expect-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.experience-item {
  padding: 16px 0;
  border-bottom: 1px solid #e4e7ed;
}

.experience-item:last-child {
  border-bottom: none;
}

.exp-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.exp-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.exp-meta {
  font-size: 14px;
  color: #909399;
}

.exp-time {
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
}

.exp-desc {
  font-size: 14px;
  color: #606266;
  line-height: 1.8;
  white-space: pre-wrap;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
}

.self-eval {
  font-size: 14px;
  color: #606266;
  line-height: 1.8;
}

.delivery-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.label {
  color: #909399;
}

.value {
  color: #606266;
}

.quick-actions {
  display: flex;
  flex-direction: column;
}
</style>
