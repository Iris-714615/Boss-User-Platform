<script setup>
import { ref, nextTick, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Picture, Folder, Odometer, Phone, VideoCamera, MoreFilled } from '@element-plus/icons-vue'
import { UserType, MessageType, formatTime } from 'shared-types'

const route = useRoute()
const router = useRouter()

const messageInput = ref('')
const inputRef = ref(null)

// 使用统一的数据结构
const chatInfo = ref({
  hrId: 'hr001',              // ✅ HR ID
  hrName: '张经理',
  hrAvatar: '',
  companyId: 'company_001',   // ✅ 企业 ID
  company: '示例科技有限公司',
  position: '招聘经理',
  online: true,
  jobId: 'position_001',      // ✅ 职位 ID
  jobTitle: '高级前端工程师',
  salaryMin: 25,              // ✅ 分字段存储
  salaryMax: 35,
  salaryMonth: 14
})

// 计算属性：薪资显示
const salaryDisplay = computed(() => {
  return `${chatInfo.value.salaryMin}-${chatInfo.value.salaryMax}K·${chatInfo.value.salaryMonth}薪`
})

// 消息列表 - 使用统一的 ChatMessage 结构
const messages = ref([
  {
    id: 'msg_001',
    sessionId: 'hr_hr001_candidate_cand001',
    senderId: 'hr001',
    senderType: UserType.HR,      // ✅ 使用枚举值
    receiverId: 'cand001',
    receiverType: UserType.CANDIDATE,
    type: MessageType.TEXT,
    content: '您好，看到您投递了我们的职位',
    timestamp: Date.now() - 3600000 * 2,  // ✅ 使用时间戳
    status: 'read',
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
    timestamp: Date.now() - 3600000 * 1.9,
    status: 'read',
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
    timestamp: Date.now() - 3600000 * 1.8,
    status: 'read',
    relatedPositionId: 'position_001'
  },
  {
    id: 'msg_004',
    sessionId: 'hr_hr001_candidate_cand001',
    senderId: 'system',
    senderType: UserType.HR,
    receiverId: 'cand001',
    receiverType: UserType.CANDIDATE,
    type: MessageType.SYSTEM,
    content: '交换了电话',
    timestamp: Date.now() - 3600000 * 1.7,
    status: 'read'
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
    timestamp: Date.now() - 3600000 * 1.6,
    status: 'delivered',
    relatedPositionId: 'position_001'
  }
])

const sendMessage = () => {
  if (!messageInput.value.trim()) {
    ElMessage.warning('请输入消息内容')
    return
  }
  
  // 使用统一的消息结构
  messages.value.push({
    id: `msg_${Date.now()}`,
    sessionId: 'hr_hr001_candidate_cand001',
    senderId: 'cand001',
    senderType: UserType.CANDIDATE,
    receiverId: 'hr001',
    receiverType: UserType.HR,
    type: MessageType.TEXT,
    content: messageInput.value,
    timestamp: Date.now(),
    status: 'sent',
    relatedPositionId: 'position_001'
  })
  
  messageInput.value = ''
  scrollToBottom()
  
  // 模拟对方回复
  setTimeout(() => {
    messages.value.push({
      id: `msg_${Date.now() + 1}`,
      sessionId: 'hr_hr001_candidate_cand001',
      senderId: 'hr001',
      senderType: UserType.HR,
      receiverId: 'cand001',
      receiverType: UserType.CANDIDATE,
      type: MessageType.TEXT,
      content: '收到您的消息，我们会尽快处理',
      timestamp: Date.now(),
      status: 'sent',
      relatedPositionId: 'position_001'
    })
    scrollToBottom()
  }, 2000)
}

const onKeyPress = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    const container = document.querySelector('.message-container')
    if (container) {
      container.scrollTop = container.scrollHeight
    }
  })
}

const handleSendImage = () => {
  ElMessage.info('图片发送功能开发中')
}

const handleSendFile = () => {
  ElMessage.info('文件发送功能开发中')
}

const handleCall = () => {
  ElMessageBox.confirm(
    `<p>拨打给 ${chatInfo.value.hrName}？</p><p style="color: #909399; font-size: 12px; margin-top: 8px;">通话费用以运营商标准为准</p>`,
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

const handleVideo = () => {
  ElMessageBox.confirm(
    `发起与 ${chatInfo.value.hrName} 的视频面试？`,
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
  <div class="chat-window-container">
    <!-- 头部 -->
    <div class="chat-header">
      <div class="header-left">
        <el-button text circle @click="router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        <div class="hr-info">
          <div class="name-row">
            <span class="hr-name">{{ chatInfo.hrName }}</span>
            <span v-if="chatInfo.online" class="online-tag">在线</span>
          </div>
          <div class="company-row">
            {{ chatInfo.company }} · {{ chatInfo.position }}
          </div>
        </div>
      </div>
      <div class="header-right">
        <el-button circle text @click="handleCall">
          <el-icon><Phone /></el-icon>
        </el-button>
        <el-button circle text @click="handleVideo">
          <el-icon><VideoCamera /></el-icon>
        </el-button>
        <el-button circle text>
          <el-icon><MoreFilled /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- 职位卡片 -->
    <div class="job-card">
      <div class="job-info" @click="router.push(`/candidate/jobs/${chatInfo.jobId}`)">
        <div class="job-title">{{ chatInfo.jobTitle }}</div>
        <div class="job-salary">{{ salaryDisplay }}</div>
      </div>
      <el-button type="primary" size="small" round>
        查看职位
      </el-button>
    </div>

    <!-- 消息列表 -->
    <div class="message-container">
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="message-item"
        :class="{ 
          'self': msg.senderType === UserType.CANDIDATE, 
          'system': msg.type === MessageType.SYSTEM 
        }"
      >
        <template v-if="msg.type === MessageType.SYSTEM">
          <div class="system-message">{{ msg.content }}</div>
        </template>
        <template v-else>
          <div v-if="msg.senderType !== UserType.CANDIDATE" class="avatar">
            <el-avatar :size="40" :src="chatInfo.hrAvatar">
              <el-icon><User /></el-icon>
            </el-avatar>
          </div>
          <div class="message-content">
            <div class="message-bubble">
              {{ msg.content }}
            </div>
            <div class="message-time">{{ formatTime(msg.timestamp) }}</div>
          </div>
          <div v-if="msg.senderType === UserType.CANDIDATE" class="avatar">
            <el-avatar :size="40">
              <el-icon><User /></el-icon>
            </el-avatar>
          </div>
        </template>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-area">
      <div class="toolbar">
        <el-button text circle size="small" @click="handleSendImage">
          <el-icon><Picture /></el-icon>
        </el-button>
        <el-button text circle size="small" @click="handleSendFile">
          <el-icon><Folder /></el-icon>
        </el-button>
        <el-button text circle size="small">
          <el-icon><Odometer /></el-icon>
        </el-button>
      </div>
      <div class="input-wrapper">
        <el-input
          ref="inputRef"
          v-model="messageInput"
          type="textarea"
          :rows="3"
          placeholder="按 Enter 发送，Shift+Enter 换行"
          resize="none"
          @keydown="onKeyPress"
        />
        <el-button type="primary" @click="sendMessage">
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-window-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 60px);
  background: #f5f7fa;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.hr-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hr-name {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.online-tag {
  font-size: 12px;
  color: #67C23A;
  background: #f0f9eb;
  padding: 2px 6px;
  border-radius: 4px;
}

.company-row {
  font-size: 13px;
  color: #909399;
}

.header-right {
  display: flex;
  gap: 8px;
}

.job-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: white;
  margin: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
}

.job-info {
  flex: 1;
}

.job-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.job-salary {
  font-size: 13px;
  color: #f56c6c;
  font-weight: 500;
}

.message-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.message-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.message-item.self {
  flex-direction: row-reverse;
}

.message-item.system {
  justify-content: center;
}

.avatar {
  flex-shrink: 0;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-width: 60%;
}

.message-item.self .message-content {
  align-items: flex-end;
}

.message-bubble {
  background: white;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  word-break: break-word;
}

.message-item.self .message-bubble {
  background: #0084ff;
  color: white;
}

.message-time {
  font-size: 11px;
  color: #c0c4cc;
}

.system-message {
  background: rgba(0, 0, 0, 0.05);
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 12px;
  color: #909399;
}

.input-area {
  background: white;
  padding: 12px 16px;
  border-top: 1px solid #e4e7ed;
}

.toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.input-wrapper {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.input-wrapper :deep(.el-textarea__inner) {
  border: none;
  box-shadow: none;
  background: #f5f7fa;
  padding: 12px;
  font-size: 14px;
}

.input-wrapper .el-button {
  flex-shrink: 0;
  padding: 12px 24px;
}
</style>
