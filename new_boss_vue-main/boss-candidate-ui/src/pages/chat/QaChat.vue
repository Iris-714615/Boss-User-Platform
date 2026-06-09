<template>
  <div class="qa-chat-container">
    <!-- 左侧边栏 -->
    <div class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <!-- 侧边栏头部 -->
      <div class="sidebar-header">
        <div class="logo" v-if="!sidebarCollapsed">
          <span class="logo-icon">🤖</span>
          <span class="logo-text">智能助手</span>
        </div>
        <span class="logo-icon collapsed-logo" v-else>🤖</span>
      </div>

      <!-- 功能按钮 -->
      <div class="sidebar-actions">
        <button class="action-btn new-chat" @click="newChat">
          <span class="btn-icon">+</span>
          <span class="btn-text" v-if="!sidebarCollapsed">新对话</span>
        </button>
        <button class="action-btn" @click="alert('AI创作功能开发中')">
          <span class="btn-icon">✨</span>
          <span class="btn-text" v-if="!sidebarCollapsed">AI 创作</span>
        </button>
        <button class="action-btn" @click="alert('云盘功能开发中')">
          <span class="btn-icon">☁️</span>
          <span class="btn-text" v-if="!sidebarCollapsed">云盘</span>
        </button>
        <button class="action-btn" @click="alert('更多功能开发中')">
          <span class="btn-icon">⋮</span>
          <span class="btn-text" v-if="!sidebarCollapsed">更多</span>
        </button>
      </div>

      <!-- 分隔线 -->
      <div class="divider" v-if="!sidebarCollapsed"></div>

      <!-- 历史对话标题 -->
      <div class="history-header" v-if="!sidebarCollapsed">
        <span class="history-title">历史对话</span>
        <span class="history-count">{{ historyList.length }}</span>
      </div>

      <!-- 历史对话列表 -->
      <div class="history-list">
        <div
          v-for="item in historyList"
          :key="item.id"
          class="history-item"
          :class="{ active: item.active }"
          @click="selectHistory(item)"
        >
          <span class="history-icon">💬</span>
          <span class="history-title-text" v-if="!sidebarCollapsed">{{ item.title }}</span>
          <span class="history-time" v-if="!sidebarCollapsed">{{ item.time }}</span>
        </div>
      </div>

      <!-- 用户信息 -->
      <div class="user-info" v-if="!sidebarCollapsed">
        <span class="user-icon">👤</span>
        <span class="user-name">用户</span>
      </div>
    </div>

    <!-- 侧边栏折叠按钮 -->
    <button class="sidebar-toggle" @click="toggleSidebar">
      {{ sidebarCollapsed ? '›' : '‹' }}
    </button>

    <!-- 右侧聊天区域 -->
    <div class="chat-area">
      <!-- 头部 -->
      <div class="chat-header">
        <div class="header-left">
          <div class="bot-avatar">🤖</div>
          <div class="header-info">
            <div class="bot-name">智能助手</div>
            <div class="bot-status">在线</div>
          </div>
        </div>
        <div class="header-actions">
          <button class="help-btn">帮助</button>
        </div>
      </div>

      <!-- 快捷问题 -->
      <div class="quick-questions">
        <button class="quick-btn" @click="inputMessage='简历优化建议'; sendMessage()">简历优化建议</button>
        <button class="quick-btn" @click="inputMessage='面试技巧'; sendMessage()">面试技巧</button>
        <button class="quick-btn" @click="inputMessage='职业规划'; sendMessage()">职业规划</button>
        <button class="quick-btn" @click="inputMessage='薪资谈判'; sendMessage()">薪资谈判</button>
      </div>

      <!-- 聊天内容区 -->
      <div ref="chatContainer" class="chat-content">
        <div 
          v-for="msg in messageList" 
          :key="msg.id" 
          class="message-item"
          :class="msg.type"
        >
          <!-- 用户消息 -->
          <div v-if="msg.type === 'user'" class="user-message">
            <div class="message-avatar user-avatar">👤</div>
            <div class="message-content">
              <div class="message-bubble user-bubble">
                {{ msg.content }}
              </div>
            </div>
          </div>

          <!-- 机器人消息 -->
          <div v-else-if="msg.type === 'bot'" class="bot-message">
            <div class="message-content">
              <div class="message-bubble bot-bubble">
                {{ msg.content }}
              </div>
            </div>
          </div>

          <!-- 系统消息 -->
          <div v-else class="system-message">
            {{ msg.content }}
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="chat-input">
        <div class="input-tools">
          <button class="tool-btn" @click="alert('表情功能开发中')">😊</button>
          <button class="tool-btn" @click="alert('文件功能开发中')">📎</button>
          <button class="tool-btn" @click="alert('图片功能开发中')">🖼️</button>
        </div>
        <div class="input-wrapper">
          <textarea
            v-model="inputMessage"
            placeholder="输入您的问题..."
            class="message-input"
            @keydown="handleKeydown"
          ></textarea>
        </div>
        <div class="send-btn-wrapper">
          <button 
            class="send-btn" 
            @click="sendMessage"
            :disabled="!inputMessage.trim() || isStreaming"
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import request from '@/utils/request'

// 当前对话消息
const messageList = ref([
  {
    id: 1,
    type: 'system',
    content: '您好！我是智能助手，请问有什么可以帮助您的？'
  }
])

// 历史对话记录
const historyList = ref([
  { id: 1, title: '工具调用问题修复', time: '刚刚', active: true },
  { id: 2, title: 'FastAPI与Vue3实战项目响应', time: '10分钟前' },
  { id: 3, title: 'MongoDB聊天系统消息整合与...', time: '30分钟前' },
  { id: 4, title: 'Python Web+AI项目名推荐', time: '1小时前' },
  { id: 5, title: '员工信息管理系统数据库设计...', time: '2小时前' },
  { id: 6, title: '员工信息管理系统介绍', time: '昨天' },
  { id: 7, title: 'APScheduler任务管理系统介绍', time: '昨天' },
  { id: 8, title: 'Python员工管理系统项目介绍...', time: '2天前' },
  { id: 9, title: '《人工智能基础与应用》课程介...', time: '3天前' },
  { id: 10, title: '员工添加功能需求分析', time: '1周前' },
  { id: 11, title: '员工档案新增系统流程', time: '1周前' },
  { id: 12, title: '项目—（人工智能新时代）文档...', time: '1周前' },
  { id: 13, title: '小升初数学快速提升方法', time: '2周前' }
])

const inputMessage = ref('')
const chatContainer = ref(null)
const sidebarCollapsed = ref(false)

// 👇 新增：当前正在流式输出的消息ID 和 状态
const currentStreamingId = ref(null)
const isStreaming = ref(false)

let eventSource = null

// 关闭连接
const closeSSE = () => {
  if (eventSource) {
    eventSource.close()
    eventSource = null
  }
  // 重置流式状态
  currentStreamingId.value = null
  isStreaming.value = false
}

const sendMessage = () => {
  if (!inputMessage.value.trim()) {
    alert('请输入内容')
    return
  }
  if (isStreaming.value) {
    alert('请等待当前回复完成')
    return
  }

  // 1. 添加用户消息
  const userMsgId = Date.now()
  messageList.value.push({
    id: userMsgId,
    type: 'user',
    content: inputMessage.value.trim()
  })

  // 2. 新增一个空的机器人消息，用于流式追加
  const botMsgId = Date.now() + 1
  messageList.value.push({
    id: botMsgId,
    type: 'bot',
    content: ''
  })
  currentStreamingId.value = botMsgId
  isStreaming.value = true

  // 清空输入框
  const text = inputMessage.value.trim()
  inputMessage.value = ''
  scrollToBottom()

  // 3. 连接 SSE
  const url = `http://127.0.0.1:8000/chatai/chat_stream?message=${encodeURIComponent(text)}`
  eventSource = new EventSource(url)

  // 监听消息
  eventSource.onmessage = (e) => {
    const data = e.data
    console.log('收到分片:', data)

    // 👇 关键：把分片追加到当前的 bot 消息里
    if (currentStreamingId.value) {
      const botMsg = messageList.value.find(m => m.id === currentStreamingId.value)
      if (botMsg) {
        // 去掉后端可能加的 \n\n，避免多余换行
        const cleanData = data.replace(/\n\n$/, '')
        // 如果是结束标记，直接跳过或处理
        if (cleanData === '[DONE]') {
          closeSSE()
          return
        }
        botMsg.content += cleanData
        scrollToBottom()
      }
    }
  }

  // 监听错误
  eventSource.onerror = (err) => {
    console.error('SSE 错误:', err)
    if (currentStreamingId.value) {
      const botMsg = messageList.value.find(m => m.id === currentStreamingId.value)
      if (botMsg) {
        botMsg.content += '\n\n（连接异常，输出中断）'
      }
    }
    closeSSE()
    scrollToBottom()
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

const newChat = () => {
  // 先关闭旧连接
  closeSSE()
  messageList.value = [{
    id: 1,
    type: 'system',
    content: '您好！我是智能助手，请问有什么可以帮助您的？'
  }]
  historyList.value.unshift({
    id: Date.now(),
    title: '新对话',
    time: '刚刚',
    active: true
  })
  historyList.value.forEach((item, index) => {
    item.active = index === 0
  })
}

const selectHistory = (item) => {
  closeSSE()
  historyList.value.forEach(h => h.active = false)
  item.active = true
  messageList.value = [{
    id: 1,
    type: 'system',
    content: '您好！我是智能助手，请问有什么可以帮助您的？'
  }, {
    id: 2,
    type: 'user',
    content: `关于"${item.title}"的问题`
  }, {
    id: 3,
    type: 'bot',
    content: '当然可以！我可以帮您解答相关问题。请问您具体想了解什么呢？'
  }]
  scrollToBottom()
}

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.qa-chat-container {
  height: calc(100vh - 60px);
  display: flex;
  background: #f5f7fa;
}

/* 左侧边栏 */
.sidebar {
  width: 260px;
  background: white;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #ebeef5;
  transition: width 0.3s;
}

.sidebar.collapsed {
  width: 56px;
}

.sidebar-header {
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 1px solid #ebeef5;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
}

.collapsed-logo {
  font-size: 24px;
}

.logo-text {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.sidebar-actions {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border: none;
  border-radius: 8px;
  background: transparent;
  cursor: pointer;
  transition: background 0.2s;
}

.action-btn:hover {
  background: #f5f7fa;
}

.action-btn.new-chat {
  background: #0084ff;
  color: white;
}

.action-btn.new-chat:hover {
  background: #0073e6;
}

.btn-icon {
  font-size: 16px;
}

.btn-text {
  font-size: 14px;
}

.divider {
  height: 1px;
  background: #ebeef5;
  margin: 0 12px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  font-size: 12px;
  color: #909399;
}

.history-title {
  font-weight: 500;
}

.history-count {
  background: #f5f7fa;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}

.history-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 8px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.history-item:hover {
  background: #f5f7fa;
}

.history-item.active {
  background: #e8f0fe;
}

.history-icon {
  font-size: 16px;
}

.history-title-text {
  flex: 1;
  font-size: 13px;
  color: #303133;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-time {
  font-size: 12px;
  color: #909399;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  border-top: 1px solid #ebeef5;
}

.user-icon {
  font-size: 20px;
}

.user-name {
  font-size: 14px;
  color: #606266;
}

/* 侧边栏折叠按钮 */
.sidebar-toggle {
  width: 20px;
  background: white;
  border: none;
  border-right: 1px solid #ebeef5;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #909399;
  transition: background 0.2s;
}

.sidebar-toggle:hover {
  background: #f5f7fa;
}

/* 右侧聊天区域 */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
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

.bot-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.header-info {
  display: flex;
  flex-direction: column;
}

.bot-name {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.bot-status {
  font-size: 12px;
  color: #67c23a;
}

.header-actions {
  color: #909399;
}

.help-btn {
  padding: 4px 12px;
  border: none;
  background: transparent;
  color: #909399;
  font-size: 14px;
  cursor: pointer;
}

.help-btn:hover {
  color: #606266;
}

/* 快捷问题 */
.quick-questions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px 16px;
  background: white;
  border-bottom: 1px solid #ebeef5;
}

.quick-btn {
  padding: 6px 14px;
  border: 1px solid #e4e7ed;
  border-radius: 20px;
  background: white;
  font-size: 13px;
  color: #606266;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-btn:hover {
  background: #f5f7fa;
  border-color: #c0c4cc;
}

/* 聊天内容区 */
.chat-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-item {
  display: flex;
}

.user-message {
  justify-content: flex-end;
}

.user-message .message-content {
  align-items: flex-end;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.user-bubble {
  background: #0084ff;
  color: white;
  border-radius: 18px 18px 4px 18px;
}

.bot-message {
  justify-content: flex-start;
}

.bot-message .message-content {
  align-items: flex-start;
}

.bot-bubble {
  background: white;
  color: #303133;
  border-radius: 18px 18px 18px 4px;
  border: 1px solid #ebeef5;
  /* 👇 让长文本自动换行 */
  white-space: pre-wrap;
  word-break: break-word;
}

.message-avatar {
  flex-shrink: 0;
}

.message-content {
  display: flex;
  max-width: 70%;
}

.message-bubble {
  padding: 12px 16px;
  font-size: 14px;
  line-height: 1.6;
}

.system-message {
  text-align: center;
  font-size: 12px;
  color: #909399;
  padding: 8px 0;
}

/* 输入区 */
.chat-input {
  display: flex;
  align-items: flex-end;
  padding: 12px 16px;
  background: white;
  border-top: 1px solid #ebeef5;
  gap: 12px;
}

.input-tools {
  display: flex;
  gap: 8px;
}

.tool-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: #f5f7fa;
  border-radius: 50%;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-btn:hover {
  background: #e4e7ed;
}

.input-wrapper {
  flex: 1;
}

.message-input {
  width: 100%;
  min-height: 40px;
  max-height: 120px;
  padding: 10px 12px;
  border: none;
  border-radius: 20px;
  background: #f5f7fa;
  font-size: 14px;
  resize: none;
  outline: none;
  box-sizing: border-box;
}

.message-input::placeholder {
  color: #c0c4cc;
}

.send-btn-wrapper {
  flex-shrink: 0;
}

.send-btn {
  width: 44px;
  height: 44px;
  border: none;
  border-radius: 50%;
  background: #0084ff;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.send-btn:hover:not(:disabled) {
  background: #0073e6;
}

.send-btn:disabled {
  background: #c0c4cc;
  cursor: not-allowed;
}
</style>