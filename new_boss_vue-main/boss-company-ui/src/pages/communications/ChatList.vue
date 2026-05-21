<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Search, ChatDotRound, Phone, VideoCamera, User } from '@element-plus/icons-vue'
import { UserType, formatTime, messages, candidateUsers } from 'shared-types'

const router = useRouter()

const query = ref('')

// 使用统一的消息数据生成聊天列表
const chatList = ref(candidateUsers.map(candidate => {
  // 找到与该候选人的最新消息
  const candidateMessages = messages.filter(
    msg => msg.senderId === candidate.id || msg.receiverId === candidate.id
  )
  const lastMessage = candidateMessages[candidateMessages.length - 1]
  
  return {
    id: candidate.id,
    name: candidate.name,
    avatar: candidate.avatar || '',
    lastMessage: lastMessage ? lastMessage.content : '暂无消息',
    time: lastMessage ? formatTime(lastMessage.timestamp) : '',
    unread: Math.floor(Math.random() * 3), // TODO: 实际应该从后端获取
    position: '求职者',
    status: 'online'
  }
}))

const onSearch = () => {
  console.log('search:', query.value)
}

const onChat = (userId) => {
  router.push(`/company/chat/${userId}`)
}

const onPhone = () => {
  // TODO: 打电话功能
}

const onVideo = () => {
  // TODO: 视频面试功能
}
</script>

<template>
  <div class="chat-list-container">
    <!-- 头部 -->
    <el-card shadow="never" class="header-card">
      <div class="header-content">
        <div class="header-left">
          <h3>消息</h3>
          <p class="header-desc">与候选人实时沟通</p>
        </div>
        <div class="header-right">
          <el-input
            v-model="query"
            placeholder="搜索候选人"
            style="width: 240px"
            clearable
            @input="onSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </div>
    </el-card>
    
    <!-- 聊天列表 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="16">
        <el-card shadow="never" class="chat-card">
          <div class="chat-list">
            <div 
              v-for="chat in chatList" 
              :key="chat.id"
              class="chat-item"
              @click="onChat(chat.id)"
            >
              <div class="chat-left">
                <el-avatar :size="48" :src="chat.avatar" class="avatar">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <div class="status-dot" :class="chat.status"></div>
              </div>
              
              <div class="chat-center">
                <div class="chat-header">
                  <span class="name">{{ chat.name }}</span>
                  <span class="position">{{ chat.position }}</span>
                  <span class="time">{{ chat.time }}</span>
                </div>
                <div class="last-message">
                  <el-icon v-if="chat.unread === 0"><ChatDotRound /></el-icon>
                  {{ chat.lastMessage }}
                </div>
              </div>
              
              <div class="chat-right">
                <el-badge :value="chat.unread" :hidden="chat.unread === 0" type="primary" />
                <div class="actions">
                  <el-button circle text size="small" @click.stop="onPhone">
                    <el-icon><Phone /></el-icon>
                  </el-button>
                  <el-button circle text size="small" @click.stop="onVideo">
                    <el-icon><VideoCamera /></el-icon>
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="never" class="tips-card">
          <template #header>
            <span>💡 沟通技巧</span>
          </template>
          
          <div class="tips-list">
            <div class="tip-item">
              <div class="tip-title">及时回复</div>
              <div class="tip-desc">尽量在 1 小时内回复候选人消息</div>
            </div>
            <div class="tip-item">
              <div class="tip-title">主动沟通</div>
              <div class="tip-desc">对感兴趣的简历主动发起聊天</div>
            </div>
            <div class="tip-item">
              <div class="tip-title">专业礼貌</div>
              <div class="tip-desc">使用礼貌用语，展现企业专业形象</div>
            </div>
            <div class="tip-item">
              <div class="tip-title">明确信息</div>
              <div class="tip-desc">清晰说明岗位职责和薪资待遇</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.chat-list-container {
  padding: 0;
}

.header-card {
  margin-bottom: 16px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left h3 {
  font-size: 20px;
  color: #303133;
  margin: 0 0 4px 0;
}

.header-desc {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.chat-card {
  min-height: 600px;
}

.chat-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chat-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #e4e7ed;
}

.chat-item:hover {
  background-color: #f5f7fa;
  border-color: #0084ff;
  transform: translateX(4px);
}

.chat-left {
  position: relative;
  margin-right: 16px;
}

.status-dot {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid #fff;
}

.status-dot.online {
  background: #67C23A;
}

.status-dot.offline {
  background: #DCDFE6;
}

.chat-center {
  flex: 1;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
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

.time {
  font-size: 12px;
  color: #C0C4CC;
  margin-left: auto;
}

.last-message {
  font-size: 14px;
  color: #606266;
  display: flex;
  align-items: center;
  gap: 4px;
}

.chat-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
}

.actions {
  display: flex;
  gap: 8px;
}

.tips-card {
  min-height: 600px;
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tip-item {
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
}

.tip-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.tip-desc {
  font-size: 13px;
  color: #909399;
  line-height: 1.6;
}
</style>
