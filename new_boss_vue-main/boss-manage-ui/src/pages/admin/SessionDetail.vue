<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  ChatDotRound, 
  Warning, 
  CircleCheck, 
  Clock, 
  User, 
  OfficeBuilding,
  Picture,
  Document,
  Link
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const dialogVisible = ref(true)
const loading = ref(false)

// 会话基本信息
const sessionInfo = reactive({
  sessionId: 'S20260331001',
  company: {
    id: 10001,
    name: '示例科技有限公司',
    hrName: '张经理',
    hrAvatar: '',
    position: '招聘经理',
  },
  candidate: {
    id: 20001,
    name: '张三',
    avatar: '',
    resume: '高级前端工程师 | 3 年经验 | 本科',
    phone: '138****0001',
  },
  position: {
    id: 30001,
    title: '高级前端工程师',
    salary: '25-35K',
    city: '上海',
  },
  startTime: '2026-03-31 10:20:00',
  lastTime: '2026-03-31 10:45:23',
  messageCount: 28,
  duration: '25 分 23 秒',
  
  // 风险评估
  riskLevel: '高',
  riskScore: 85,
  riskTags: ['疑似虚假承诺', '夸大薪资待遇', '引导线下交易'],
  riskDetails: [
    { type: '敏感词触发', count: 3, time: '10:25:15' },
    { type: '异常行为', count: 1, time: '10:35:42' },
  ],
})

// 聊天记录
const messages = ref([
  {
    id: 1,
    sender: 'hr',
    content: '您好，看到您对我们的前端工程师职位很感兴趣，方便聊聊吗？',
    time: '10:20:15',
    status: '已读',
  },
  {
    id: 2,
    sender: 'candidate',
    content: '您好，我确实在看机会。请问这个岗位的具体工作内容是什么？',
    time: '10:21:30',
    status: '已读',
  },
  {
    id: 3,
    sender: 'hr',
    content: '主要负责公司核心产品的前端开发，使用 Vue 和 React 技术栈。',
    time: '10:22:45',
    status: '已读',
  },
  {
    id: 4,
    sender: 'hr',
    content: '我们公司提供非常有竞争力的薪资，年薪可以达到 50-80 万，还有期权激励。',
    time: '10:23:20',
    status: '已读',
    flagged: true,
    flagReason: '疑似夸大薪资',
  },
  {
    id: 5,
    sender: 'candidate',
    content: '听起来不错。请问团队规模怎么样？',
    time: '10:25:10',
    status: '已读',
  },
  {
    id: 6,
    sender: 'hr',
    content: '前端团队目前有 20 多人，都是来自大厂的优秀工程师。',
    time: '10:26:00',
    status: '已读',
  },
  {
    id: 7,
    sender: 'hr',
    content: '不过这个职位需要先到我们合作的培训机构学习 3 个月，费用是 2 万元。',
    time: '10:28:30',
    status: '已读',
    flagged: true,
    flagReason: '疑似培训贷骗局',
  },
  {
    id: 8,
    sender: 'candidate',
    content: '什么？还要先交钱学习？这不太对吧...',
    time: '10:30:15',
    status: '已读',
  },
  {
    id: 9,
    sender: 'hr',
    content: '您放心，这个费用可以从以后的工资里扣除，而且我们保证学完就能入职。',
    time: '10:32:00',
    status: '已读',
    flagged: true,
    flagReason: '诱导性承诺',
  },
  {
    id: 10,
    sender: 'candidate',
    content: '我觉得不太靠谱，算了吧。',
    time: '10:35:20',
    status: '已读',
  },
  {
    id: 11,
    sender: 'hr',
    content: '别急着拒绝啊，我们可以安排面试，直接和部门领导聊。',
    time: '10:38:00',
    status: '已读',
  },
  {
    id: 12,
    sender: 'hr',
    content: '这样吧，您留个微信，我把详细资料发给您看看。',
    time: '10:40:15',
    status: '已读',
    flagged: true,
    flagReason: '引导私下联系',
  },
  {
    id: 13,
    sender: 'candidate',
    content: '不用了，谢谢。',
    time: '10:42:30',
    status: '已读',
  },
])

// 审核操作
const auditForm = reactive({
  result: '',
  remark: '',
})

const handleClose = () => {
  dialogVisible.value = false
  router.back()
}

const handleMarkSafe = () => {
  ElMessage.success('已标记为无风险')
}

const handleReport = () => {
  ElMessage.info('举报功能待开发')
}

const handleBanHR = async () => {
  ElMessage.warning('封禁 HR 账号功能待开发')
}

const viewCompanyDetail = () => {
  router.push(`/admin/companies/${sessionInfo.company.id}`)
}

const viewCandidateDetail = () => {
  ElMessage.info('求职者详情功能待开发')
}

const copyContent = (text: string) => {
  navigator.clipboard.writeText(text)
  ElMessage.success('内容已复制')
}

const filterFlagged = ref(false)

const filteredMessages = computed(() => {
  if (filterFlagged.value) {
    return messages.value.filter(m => m.flagged)
  }
  return messages.value
})
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="`会话详情 - ${sessionInfo.sessionId}`"
    width="90%"
    top="2vh"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-loading="loading" class="session-detail">
      <el-row :gutter="20">
        <!-- 左侧：聊天信息和记录 -->
        <el-col :span="16">
          <!-- 会话头部信息 -->
          <el-card shadow="never" class="session-header">
            <div style="display: flex; justify-content: space-between; align-items: center">
              <div style="display: flex; gap: 20px">
                <div>
                  <div style="font-size: 12px; color: #909399; margin-bottom: 4px">企业方</div>
                  <div style="display: flex; align-items: center; gap: 8px">
                    <el-avatar :size="40" style="background: #409EFF">
                      <el-icon><OfficeBuilding /></el-icon>
                    </el-avatar>
                    <div>
                      <div style="font-weight: 600">{{ sessionInfo.company.name }}</div>
                      <div style="font-size: 12px; color: #909399">{{ sessionInfo.company.hrName }} · {{ sessionInfo.company.position }}</div>
                    </div>
                  </div>
                </div>
                
                <el-icon :size="24" style="color: #909399"><ChatDotRound /></el-icon>
                
                <div>
                  <div style="font-size: 12px; color: #909399; margin-bottom: 4px">求职者</div>
                  <div style="display: flex; align-items: center; gap: 8px">
                    <el-avatar :size="40" style="background: #67C23A">
                      <el-icon><User /></el-icon>
                    </el-avatar>
                    <div>
                      <div style="font-weight: 600">{{ sessionInfo.candidate.name }}</div>
                      <div style="font-size: 12px; color: #909399">{{ sessionInfo.candidate.resume }}</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div style="text-align: right">
                <div style="font-size: 12px; color: #909399">沟通时长</div>
                <div style="font-weight: 600; font-size: 16px">{{ sessionInfo.duration }}</div>
              </div>
            </div>
          </el-card>

          <!-- 风险提示卡片 -->
          <el-alert
            v-if="sessionInfo.riskLevel === '高'"
            title="高风险会话"
            type="error"
            :closable="false"
            style="margin: 16px 0"
            show-icon
          >
            <template #default>
              <div style="margin-top: 8px">
                <el-tag type="danger" size="small" style="margin-right: 8px">风险评分：{{ sessionInfo.riskScore }}</el-tag>
                <el-tag 
                  v-for="(tag, index) in sessionInfo.riskTags" 
                  :key="index"
                  type="danger"
                  size="small"
                  style="margin-right: 8px"
                >
                  {{ tag }}
                </el-tag>
              </div>
            </template>
          </el-alert>

          <!-- 聊天记录区域 -->
          <el-card shadow="never" class="chat-card">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center">
                <span style="font-weight: 600">💬 聊天记录（{{ messages.length }}条）</span>
                <div>
                  <el-checkbox v-model="filterFlagged" label="仅看风险消息" />
                  <el-button size="small" @click="copyContent(JSON.stringify(messages))">导出记录</el-button>
                </div>
              </div>
            </template>
            
            <div class="chat-container">
              <div
                v-for="message in filteredMessages"
                :key="message.id"
                :class="['message-item', message.sender]"
              >
                <div class="message-avatar">
                  <el-avatar 
                    :size="40" 
                    :style="{ background: message.sender === 'hr' ? '#409EFF' : '#67C23A' }"
                  >
                    <el-icon>
                      <component :is="message.sender === 'hr' ? OfficeBuilding : User" />
                    </el-icon>
                  </el-avatar>
                </div>
                
                <div class="message-content">
                  <div class="message-info">
                    <span class="message-sender">
                      {{ message.sender === 'hr' ? sessionInfo.company.hrName : sessionInfo.candidate.name }}
                    </span>
                    <span class="message-time">{{ message.time }}</span>
                  </div>
                  
                  <div 
                    :class="['message-bubble', message.sender]"
                    @dblclick="copyContent(message.content)"
                  >
                    {{ message.content }}
                  </div>
                  
                  <div v-if="message.flagged" class="message-flag">
                    <el-tag type="warning" size="small">
                      <el-icon><Warning /></el-icon>
                      {{ message.flagReason }}
                    </el-tag>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 右侧：职位信息和审核操作 -->
        <el-col :span="8">
          <!-- 职位信息 -->
          <el-card shadow="never" class="info-card">
            <template #header>
              <span style="font-weight: 600">📋 沟通职位</span>
            </template>
            
            <el-descriptions :column="1" border size="small">
              <el-descriptions-item label="职位名称">{{ sessionInfo.position.title }}</el-descriptions-item>
              <el-descriptions-item label="薪资范围">{{ sessionInfo.position.salary }}</el-descriptions-item>
              <el-descriptions-item label="工作地点">{{ sessionInfo.position.city }}</el-descriptions-item>
            </el-descriptions>
            
            <el-button text type="primary" style="margin-top: 12px; width: 100%">
              查看职位详情
            </el-button>
          </el-card>

          <!-- 会话元数据 -->
          <el-card shadow="never" class="info-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">ℹ️ 会话信息</span>
            </template>
            
            <el-descriptions :column="1" border size="small">
              <el-descriptions-item label="会话 ID">{{ sessionInfo.sessionId }}</el-descriptions-item>
              <el-descriptions-item label="开始时间">{{ sessionInfo.startTime }}</el-descriptions-item>
              <el-descriptions-item label="最后活跃">{{ sessionInfo.lastTime }}</el-descriptions-item>
              <el-descriptions-item label="消息数量">{{ sessionInfo.messageCount }}条</el-descriptions-item>
            </el-descriptions>
          </el-card>

          <!-- 风险详情 -->
          <el-card shadow="never" class="info-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">⚠️ 风险详情</span>
            </template>
            
            <el-timeline>
              <el-timeline-item 
                v-for="(detail, index) in sessionInfo.riskDetails" 
                :key="index"
                type="warning"
                :timestamp="detail.time"
              >
                {{ detail.type }}（{{ detail.count }}次）
              </el-timeline-item>
            </el-timeline>
          </el-card>

          <!-- 审核操作面板 -->
          <el-card shadow="never" class="audit-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">✅ 审核操作</span>
            </template>
            
            <el-form :model="auditForm" label-width="70px" size="small">
              <el-form-item label="审核结果">
                <el-radio-group v-model="auditForm.result">
                  <el-radio label="safe">无风险</el-radio>
                  <el-radio label="risk">有风险</el-radio>
                </el-radio-group>
              </el-form-item>
              
              <el-form-item label="备注说明">
                <el-input 
                  v-model="auditForm.remark" 
                  type="textarea" 
                  :rows="3"
                  placeholder="请输入审核意见"
                />
              </el-form-item>
              
              <el-button type="primary" style="width: 100%" @click="ElMessage.success('审核完成')">提交审核</el-button>
            </el-form>
            
            <el-divider />
            
            <el-button type="success" plain style="width: 100%; margin-bottom: 8px" @click="handleMarkSafe">
              <el-icon><CircleCheck /></el-icon>
              标记无风险
            </el-button>
            
            <el-button type="warning" plain style="width: 100%; margin-bottom: 8px" @click="handleReport">
              <el-icon><Warning /></el-icon>
              提交举报
            </el-button>
            
            <el-button type="danger" plain style="width: 100%" @click="handleBanHR">
              <el-icon><Warning /></el-icon>
              封禁 HR 账号
            </el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <template #footer>
      <el-button @click="handleClose">关闭</el-button>
      <el-button type="primary" @click="viewCompanyDetail">查看企业详情</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.session-detail {
  max-height: 75vh;
  overflow-y: auto;
  padding-right: 10px;
}

.session-header {
  margin-bottom: 16px;
}

.chat-card {
  min-height: 500px;
}

.chat-container {
  max-height: 500px;
  overflow-y: auto;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 8px;
}

.message-item {
  display: flex;
  margin-bottom: 16px;
  gap: 12px;
}

.message-item.hr {
  flex-direction: row;
}

.message-item.candidate {
  flex-direction: row-reverse;
}

.message-content {
  flex: 1;
  max-width: 70%;
}

.message-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  font-size: 12px;
  color: #909399;
}

.message-sender {
  font-weight: 600;
}

.message-bubble {
  padding: 12px 16px;
  border-radius: 8px;
  word-wrap: break-word;
  cursor: pointer;
}

.message-bubble.hr {
  background: white;
  border: 1px solid #e4e7ed;
}

.message-bubble.candidate {
  background: #f0f9ff;
  border: 1px solid #c6e2ff;
}

.message-flag {
  margin-top: 8px;
}

.info-card {
  margin-bottom: 16px;
}

.audit-card {
  background: #fef0f0;
}
</style>
