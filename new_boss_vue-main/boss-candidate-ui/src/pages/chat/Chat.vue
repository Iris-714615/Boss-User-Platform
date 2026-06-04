<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Phone, VideoCamera, User } from '@element-plus/icons-vue'
import { formatTime } from 'shared-types'

const router = useRouter()

const searchKeyword = ref('')

// 使用统一的会话数据结构
const messages = ref([
  {
    id: 'chat_001',
    hrId: 'hr001',
    hrName: '张经理',
    hrAvatar: '',
    companyId: 'company_001',
    company: '示例科技有限公司',
    position: '招聘经理',
    lastMessage: '您好，请问您对这个职位感兴趣吗？我们可以详细聊聊',
    time: 1711900800000,
    unread: 2,
    online: true,
    jobId: 'position_001',
    jobTitle: '高级前端工程师'
  },
  {
    id: 'chat_002',
    hrId: 'hr002',
    hrName: '李女士',
    hrAvatar: '',
    companyId: 'company_002',
    company: '某某信息科技公司',
    position: 'HRBP',
    lastMessage: '您的简历我们已经收到了，觉得比较匹配',
    time: 1711814400000,
    unread: 0,
    online: false,
    jobId: 'position_002',
    jobTitle: '产品经理'
  },
  {
    id: 'chat_003',
    hrId: 'hr003',
    hrName: '王先生',
    hrAvatar: '',
    companyId: 'company_003',
    company: '科技创新公司',
    position: '技术总监',
    lastMessage: '什么时候可以来面试？',
    time: 1711555200000,
    unread: 5,
    online: true,
    jobId: 'position_003',
    jobTitle: 'Java 开发工程师'
  }
])

const goToChat = (hrId) => {
  router.push(`/candidate/chat/${hrId}`)
}

const handleCall = (e, item) => {
  e.stopPropagation()
  ElMessageBox.confirm(
    `<p>拨打给 ${item.hrName}？</p><p style="color: #909399; font-size: 12px; margin-top: 8px;">${item.company} · ${item.position}</p>`,
    '电话沟通',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '拨打',
      cancelButtonText: '取消',
      type: 'info'
    }
  ).then(() => {
    ElMessage.success('正在呼叫...')
  }).catch(() => {
    // 取消操作
  })
}

const handleVideo = (e, item) => {
  e.stopPropagation()
  ElMessageBox.confirm(
    `发起与 ${item.hrName} 的视频面试？`,
    '视频面试',
    {
      confirmButtonText: '发起',
      cancelButtonText: '取消',
      type: 'success'
    }
  ).then(() => {
    ElMessage.info('等待对方接听...')
  }).catch(() => {
    // 取消操作
  })
}
</script>

<template>
  <div class="chat-container">
    <!-- 顶部搜索 -->
    <el-card shadow="never" class="search-card">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索聊天消息"
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </el-card>

    <!-- 会话列表 -->
    <div class="message-list" style="margin-top: 16px">
      <el-card
        v-for="msg in messages"
        :key="msg.id"
        shadow="hover"
        class="message-item"
        @click="goToChat(msg.id)"
      >
        <div class="message-content">
          <!-- 头像 -->
          <div class="avatar-wrapper">
            <el-avatar :size="48" :src="msg.hrAvatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <span v-if="msg.online" class="online-status"></span>
          </div>
          
          <!-- 信息区 -->
          <div class="info-wrapper">
            <!-- 第一行：姓名 + 时间 -->
            <div class="top-row">
              <div class="name-section">
                <span class="hr-name">{{ msg.hrName }}</span>
                <span class="hr-position">{{ msg.position }}</span>
              </div>
              <div class="time-section">
                <span class="time">{{ formatTime(msg.time) }}</span>
                <el-badge :value="msg.unread" :hidden="msg.unread === 0" class="badge" />
              </div>
            </div>
            
            <!-- 第二行：公司 + 职位 -->
            <div class="middle-row">
              <span class="company">{{ msg.company }}</span>
              <span class="divider">·</span>
              <span class="job-title">{{ msg.jobTitle }}</span>
            </div>
            
            <!-- 第三行：最后消息 -->
            <div class="bottom-row">
              <span class="last-message">{{ msg.lastMessage }}</span>
            </div>
          </div>
        
          <!-- 操作按钮 -->
          <div class="action-buttons">
            <el-button circle text size="small" @click="handleCall($event, msg)">
              <el-icon><Phone /></el-icon>
            </el-button>
            <el-button circle text size="small" @click="handleVideo($event, msg)">
              <el-icon><VideoCamera /></el-icon>
            </el-button>
          </div>
        </div>
      </el-card>
      
      <!-- 空状态 -->
      <el-empty v-if="messages.length === 0" description="暂无消息" />
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  padding-bottom: 20px;
}

.search-card {
  border-radius: 12px;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-item {
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.message-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.message-content {
  display: flex;
  gap: 12px;
  padding: 12px 0;
}

.avatar-wrapper {
  position: relative;
  flex-shrink: 0;
}

.online-status {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  background: #67C23A;
  border: 2px solid white;
  border-radius: 50%;
}

.info-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
  overflow: hidden;
}

.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.name-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hr-name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.hr-position {
  font-size: 12px;
  color: #909399;
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 4px;
}

.time-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.time {
  font-size: 12px;
  color: #c0c4cc;
}

.badge {
  display: flex;
}

.middle-row {
  font-size: 13px;
  color: #606266;
}

.company {
  font-weight: 500;
}

.divider {
  margin: 0 6px;
  color: #c0c4cc;
}

.job-title {
  color: #909399;
}

.bottom-row {
  font-size: 13px;
  color: #909399;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s;
}

.message-item:hover .action-buttons {
  opacity: 1;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .action-buttons {
    display: none;
  }
  
  .info-wrapper {
    gap: 4px;
  }
  
  .hr-name {
    font-size: 14px;
  }
  
  .last-message {
    max-width: 100%;
  }
}
</style>