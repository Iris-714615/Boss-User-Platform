<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Document, 
  UserFilled, 
  DocumentCopy, 
  Calendar,
  Top,
  ArrowRight,
  Plus,
  Edit,
  DataAnalysis
} from '@element-plus/icons-vue'
import { PositionStatus, formatTime } from 'shared-types'
import { positions } from 'shared-types'

const router = useRouter()

const dateRange = ref('近 7 天')

// 使用统一的职位数据
const positionStats = computed(() => {
  return positions.map(pos => ({
    id: pos.id,
    name: pos.title,
    views: pos.views,
    communicates: pos.communicates,
    resumes: pos.resumes,
    status: pos.status === PositionStatus.ACTIVE ? '招聘中' : '暂停招聘'
  }))
})

// 今日待办
const todoList = ref([
  { id: 1, type: 'interview', title: '面试 - 高级前端工程师', candidate: '张三', time: '09:30', detail: '10:00-10:45 · 视频面试' },
  { id: 2, type: 'interview', title: '面试 - 产品经理', candidate: '李四', time: '11:00', detail: '11:30-12:00 · 现场面试' },
  { id: 3, type: 'resume', title: '待处理简历', candidate: '王五', time: '待处理', detail: '期望职位：Java 开发' },
  { id: 4, type: 'chat', title: '未读消息', candidate: '赵六', time: '15 分钟前', detail: '询问岗位详情' }
])

// 快捷入口
const quickActions = ref([
  { icon: Plus, label: '发布职位', path: '/company/positions/publish' },
  { icon: Edit, label: '优化职位', path: '/company/positions' },
  { icon: DocumentCopy, label: '筛选简历', path: '/company/resumes' },
  { icon: DataAnalysis, label: '数据报告', path: '/company/data' }
])

const getStatusType = (status) => {
  return status === '招聘中' ? 'success' : 'info'
}

const handleTodo = (item) => {
  if (item.type === 'interview') {
    // TODO: 跳转到面试管理
    console.log('跳转到面试管理')
  } else if (item.type === 'resume') {
    router.push('/company/resumes')
  } else if (item.type === 'chat') {
    router.push('/company/chat')
  }
}

const goToPositionDetail = (id) => {
  router.push(`/company/positions/${id}`)
}
</script>

<template>
  <div class="dashboard-container">
    <!-- 顶部欢迎区 -->
    <el-card shadow="never" class="welcome-card">
      <div class="welcome-content">
        <div class="welcome-text">
          <h2>早上好，张经理！</h2>
          <p>示例科技有限公司 · HR 经理</p>
        </div>
        <div class="welcome-actions">
          <el-button type="primary" @click="router.push('/company/positions/publish')">
            <el-icon><Plus /></el-icon>
            发布新职位
          </el-button>
          <el-button @click="router.push('/company/resumes')">
            <el-icon><DocumentCopy /></el-icon>
            查看新简历
          </el-button>
        </div>
      </div>
    </el-card>
    
    <!-- 今日概览 -->
    <el-row :gutter="20" class="overview-row">
      <el-col :span="6" v-for="(item, index) in overviewData" :key="index">
        <el-card shadow="hover" class="overview-card">
          <div class="card-content">
            <div class="card-icon" :style="{ background: `linear-gradient(135deg, ${index * 60}deg, #667eea 0%, #764ba2 100%)` }">
              <el-icon :size="28"><component :is="item.icon" /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-label">{{ item.label }}</div>
              <div class="card-value">{{ item.value }}</div>
              <div class="card-trend" :class="item.trendType">
                <el-icon v-if="item.trendType === 'up'"><Top /></el-icon>
                <span>{{ item.trend }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 快捷操作 & 待办事项 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>📊 职位效果数据</span>
              <el-radio-group v-model="dateRange" size="small">
                <el-radio-button label="近 7 天" />
                <el-radio-button label="近 30 天" />
                <el-radio-button label="全部" />
              </el-radio-group>
            </div>
          </template>
          
          <el-table :data="positionStats" style="width: 100%" size="default">
            <el-table-column prop="name" label="职位名称" min-width="180" />
            <el-table-column prop="views" label="查看次数" width="100">
              <template #default="{ row }">
                <span style="color: #409EFF">{{ row.views }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="communicates" label="主动沟通" width="100">
              <template #default="{ row }">
                <span style="color: #67C23A">{{ row.communicates }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="resumes" label="收到简历" width="100">
              <template #default="{ row }">
                <span style="color: #E6A23C">{{ row.resumes }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button text type="primary" size="small" @click="goToPositionDetail(row.id)">详情</el-button>
                <el-button text type="primary" size="small">优化</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>⏰ 今日待办</span>
              <el-button type="primary" link size="small">查看全部</el-button>
            </div>
          </template>
          
          <el-timeline>
            <el-timeline-item 
              v-for="item in todoList" 
              :key="item.id"
              :timestamp="item.time" 
              placement="top" 
              :type="item.type === 'interview' ? 'primary' : item.type === 'resume' ? 'success' : 'warning'"
            >
              <el-card shadow="hover" class="todo-item" @click="handleTodo(item)">
                <h4>{{ item.title }}</h4>
                <p>{{ item.candidate }} · {{ item.detail }}</p>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 快捷入口 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card shadow="never">
          <template #header>
            <span>⚡ 快捷入口</span>
          </template>
          
          <div class="quick-actions">
            <div 
              v-for="(action, index) in quickActions" 
              :key="index"
              class="quick-action"
              @click="router.push(action.path)"
            >
              <div class="action-icon">
                <el-icon :size="24"><component :is="action.icon" /></el-icon>
              </div>
              <span class="action-label">{{ action.label }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.dashboard-container {
  padding: 0;
}

.welcome-card {
  margin-bottom: 20px;
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome-text h2 {
  font-size: 24px;
  color: #303133;
  margin: 0 0 8px 0;
}

.welcome-text p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.welcome-actions {
  display: flex;
  gap: 12px;
}

.overview-row {
  margin-bottom: 20px;
}

.overview-card {
  border-radius: 8px;
}

.card-content {
  display: flex;
  align-items: center;
}

.card-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 16px;
}

.card-info {
  flex: 1;
}

.card-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.card-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  line-height: 1;
}

.card-trend {
  display: flex;
  align-items: center;
  margin-top: 8px;
  font-size: 12px;
  color: #67C23A;
}

.card-trend.normal {
  color: #909399;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.todo-item {
  cursor: pointer;
  transition: all 0.3s;
}

.todo-item:hover {
  transform: translateX(4px);
}

.todo-item h4 {
  font-size: 14px;
  color: #303133;
  margin: 0 0 4px 0;
}

.todo-item p {
  font-size: 12px;
  color: #909399;
  margin: 0;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  padding: 20px 0;
}

.quick-action {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #e4e7ed;
}

.quick-action:hover {
  background-color: #f5f7fa;
  border-color: #0084ff;
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 132, 255, 0.15);
}

.action-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-bottom: 12px;
}

.action-label {
  font-size: 14px;
  color: #606266;
}
</style>
