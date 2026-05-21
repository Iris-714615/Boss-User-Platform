<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Upload, Paperclip, Picture, Phone, VideoCamera, User } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const messageInput = ref('')
const messages = ref([
  { id: 1, type: 'received', content: '您好，我对这个职位很感兴趣', time: '10:30' },
  { id: 2, type: 'sent', content: '您好！很高兴收到您的消息。请问您对这个岗位有什么想了解的吗？', time: '10:32' },
  { id: 3, type: 'received', content: '想了解一下具体的工作内容和技术栈', time: '10:35' },
])

const candidate = ref({
  name: '张三',
  position: '高级前端工程师',
  status: 'online'
})

const goBack = () => {
  router.back()
}

const sendMessage = () => {
  if (!messageInput.value.trim()) return
  
  messages.value.push({
    id: messages.value.length + 1,
    type: 'sent',
    content: messageInput.value,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  })
  
  messageInput.value = ''
}

const onKeyPress = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}
</script>

<template>
  <div class="chat-window-container">
    <!-- 头部 -->
    <el-card shadow="never" class="header-card">
      <div class="header-content">
        <div class="header-left">
          <el-button text @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
          </el-button>
          <el-avatar :size="40" class="avatar">
            <el-icon><User /></el-icon>
          </el-avatar>
          <div class="candidate-info">
            <div class="name">{{ candidate.name }}</div>
            <div class="position">{{ candidate.position }}</div>
          </div>
          <div class="status-dot" :class="candidate.status"></div>
        </div>
        <div class="header-right">
          <el-button circle text>
            <el-icon><Phone /></el-icon>
          </el-button>
          <el-button circle text>
            <el-icon><VideoCamera /></el-icon>
          </el-button>
        </div>
      </div>
    </el-card>
    
    <!-- 聊天区域 -->
    <el-card shadow="never" class="chat-card">
      <div class="messages-container">
        <div 
          v-for="message in messages" 
          :key="message.id"
          class="message-item"
          :class="message.type"
        >
          <div class="message-content">
            <div class="message-text">{{ message.content }}</div>
            <div class="message-time">{{ message.time }}</div>
          </div>
        </div>
      </div>
      
      <!-- 输入区域 -->
      <div class="input-area">
        <div class="input-tools">
          <el-button text circle size="small">
            <el-icon><Paperclip /></el-icon>
          </el-button>
          <el-button text circle size="small">
            <el-icon><Picture /></el-icon>
          </el-button>
        </div>
        <el-input
          v-model="messageInput"
          type="textarea"
          :rows="3"
          placeholder="输入消息... (Enter 发送，Shift+Enter 换行)"
          resize="none"
          @keypress="onKeyPress"
        >
          <template #append>
            <el-button type="primary" @click="sendMessage">
              <el-icon><Upload /></el-icon>
              发送
            </el-button>
          </template>
        </el-input>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.chat-window-container {
  padding: 0;
  height: calc(100vh - 100px);
  display: flex;
  flex-direction: column;
}

.header-card {
  margin-bottom: 16px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.candidate-info {
  flex: 1;
}

.name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.position {
  font-size: 13px;
  color: #909399;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid #fff;
}

.status-dot.online {
  background: #67C23A;
}

.status-dot.offline {
  background: #DCDFE6;
}

.header-right {
  display: flex;
  gap: 8px;
}

.chat-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f5f7fa;
}

.message-item {
  display: flex;
  margin-bottom: 16px;
}

.message-item.sent {
  justify-content: flex-end;
}

.message-item.received {
  justify-content: flex-start;
}

.message-content {
  max-width: 60%;
}

.message-text {
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
}

.message-item.sent .message-text {
  background: #0084ff;
  color: white;
}

.message-item.received .message-text {
  background: white;
  color: #303133;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
  text-align: right;
}

.input-area {
  border-top: 1px solid #e4e7ed;
  padding: 16px;
  background: white;
}

.input-tools {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
</style>
