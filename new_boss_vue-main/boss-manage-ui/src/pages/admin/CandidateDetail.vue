<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User,
  Phone,
  Message,
  Location,
  Calendar,
  Briefcase,
  GraduationCap,
  Trophy,
  Warning,
  CircleCheck,
  Document,
  TrendCharts
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const dialogVisible = ref(true)

// 求职者详细信息
const candidateDetail = reactive({
  id: '20001',
  name: '张三',
  phone: '138****0001',
  email: 'zhangsan@email.com',
  avatar: '',
  
  // 基本信息
  gender: '男',
  age: 28,
  birthday: '1998-05-20',
  nationality: '中国',
  city: '上海',
  district: '浦东新区',
  address: '上海市浦东新区张江高科技园区',
  maritalStatus: '未婚',
  politicalStatus: '群众',
  
  // 求职意向
  expectPosition: '高级前端工程师',
  expectSalary: '25-35K',
  expectCity: ['上海', '杭州'],
  workType: '全职',
  status: '离职，随时到岗',
  industry: '互联网/软件',
  
  // 教育经历
  education: '本科',
  degree: '学士',
  university: '上海交通大学',
  major: '计算机科学与技术',
  graduationYear: 2020,
  educationDetail: [
    {
      school: '上海交通大学',
      degree: '本科',
      major: '计算机科学与技术',
      startDate: '2016-09',
      endDate: '2020-06',
    },
  ],
  
  // 工作经历
  workExperience: '5 年',
  workDetail: [
    {
      company: '某知名互联网公司',
      position: '前端开发工程师',
      startDate: '2022-03',
      endDate: '至今',
      description: '负责公司核心产品的前端开发，主导技术架构升级',
    },
    {
      company: '某创业公司',
      position: '前端开发',
      startDate: '2020-07',
      endDate: '2022-02',
      description: '参与多个项目的前端开发，熟悉 Vue/React 技术栈',
    },
  ],
  
  // 项目经历
  projectCount: 8,
  projectDetail: [
    {
      name: '电商平台重构',
      role: '前端负责人',
      startDate: '2023-01',
      endDate: '2023-06',
      description: '主导电商平台从 0 到 1 的重构，使用 Vue3 + TypeScript 技术栈',
    },
    {
      name: '数据可视化系统',
      role: '核心开发',
      startDate: '2022-06',
      endDate: '2022-12',
      description: '负责数据大屏的开发，使用 ECharts 进行数据展示',
    },
  ],
  
  // 技能清单
  skillTags: ['Vue', 'React', 'TypeScript', 'JavaScript', 'HTML5', 'CSS3', 'Node.js', 'Webpack', 'Git'],
  languageSkills: [
    { language: '普通话', level: '母语' },
    { language: '英语', level: 'CET-6' },
  ],
  
  // 证书与荣誉
  certificates: ['软件工程师中级职称', '阿里云 ACA 认证'],
  awards: ['公司年度优秀员工 2023', '黑客马拉松三等奖'],
  
  // 作品集
  portfolioLinks: [
    { title: 'GitHub', url: 'github.com/zhangsan' },
    { title: '技术博客', url: 'blog.zhangsan.com' },
  ],
  
  // 账号状态
  accountStatus: '正常',
  verificationStatus: '已实名认证',
  resumeStatus: '完善',
  resumeCompleteRate: 95,
  
  // 风险标识
  riskLevel: '低风险',
  blacklistStatus: '未封禁',
  complaintCount: 0,
  abnormalBehavior: [],
  
  // 统计数据
  viewCount: 2356,
  deliveryCount: 156,
  interviewCount: 45,
  offerCount: 12,
  favoriteCount: 89,
  
  // 活跃度
  lastActiveTime: '2026-03-31 10:30:00',
  loginFrequency: '每天',
  avgResponseTime: '2 小时',
  
  // 时间信息
  registerTime: '2025-01-15 14:30:00',
  resumeUpdateTime: '2026-03-28 16:20:00',
  createTime: '2025-01-15 14:30:00',
})

// 投递记录
const deliveryRecords = ref([
  { id: 1, company: '示例科技有限公司', position: '高级前端工程师', salary: '25-35K', deliveryTime: '2026-03-31 09:15', status: '待处理', matchRate: 92 },
  { id: 2, company: '某某信息科技', position: '前端专家', salary: '30-40K', deliveryTime: '2026-03-30 14:20', status: '已查看', matchRate: 88 },
  { id: 3, company: '演示企业', position: '技术主管', salary: '35-45K', deliveryTime: '2026-03-29 11:30', status: '面试中', matchRate: 95 },
])

// 面试记录
const interviewRecords = ref([
  { id: 1, company: '示例科技有限公司', position: '高级前端工程师', time: '2026-04-02 14:00', type: '现场面试', result: '待面试' },
  { id: 2, company: '某某信息科技', position: '前端专家', time: '2026-03-28 10:00', type: '视频面试', result: '通过' },
])

// 沟通记录
const chatRecords = ref([
  { id: 1, company: '示例科技有限公司', hr: '张经理', lastMessage: '您好，方便聊聊吗？', time: '2026-03-31 10:25', unread: 2 },
  { id: 2, company: '某某信息科技', hr: '李女士', lastMessage: '您的简历很优秀', time: '2026-03-30 15:30', unread: 0 },
])

// 投诉记录
const complaintRecords = ref([])

const handleClose = () => {
  dialogVisible.value = false
  router.back()
}

const handleEdit = () => {
  ElMessage.info('编辑功能待开发')
}

const handleFreeze = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要冻结用户"${candidateDetail.name}"的账号吗？冻结后将无法登录和投递简历。`,
      '冻结警告',
      {
        confirmButtonText: '确认冻结',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    ElMessage.success('账号已冻结')
  } catch {
    // 取消操作
  }
}

const handleBan = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要永久封禁用户"${candidateDetail.name}"吗？此操作不可恢复。`,
      '封禁警告',
      {
        confirmButtonText: '确认封禁',
        cancelButtonText: '取消',
        type: 'error',
      }
    )
    ElMessage.success('账号已封禁')
  } catch {
    // 取消操作
  }
}

const viewResume = () => {
  ElMessage.info('查看完整简历功能待开发')
}

const exportResume = () => {
  ElMessage.info('导出简历功能待开发')
}

const downloadAttachment = () => {
  ElMessage.info('下载附件功能待开发')
}
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="`求职者详情 - ${candidateDetail.name}`"
    width="90%"
    top="2vh"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-loading="loading" class="candidate-detail">
      <el-row :gutter="20">
        <!-- 左侧：主要信息 -->
        <el-col :span="16">
          <!-- 个人名片 -->
          <el-card shadow="never" class="profile-card">
            <div style="display: flex; gap: 20px">
              <el-avatar :size="80" style="background: #409EFF">
                <el-icon :size="40"><User /></el-icon>
              </el-avatar>
              
              <div style="flex: 1">
                <div style="display: flex; justify-content: space-between; align-items: center">
                  <div>
                    <div style="font-size: 24px; font-weight: 700; margin-bottom: 8px">
                      {{ candidateDetail.name }}
                      <el-tag type="success" size="small" style="margin-left: 8px">已实名</el-tag>
                    </div>
                    <div style="color: #909399; margin-bottom: 8px">
                      {{ candidateDetail.expectPosition }} | {{ candidateDetail.workExperience }} | {{ candidateDetail.education }} | {{ candidateDetail.city }}
                    </div>
                    <div style="display: flex; gap: 16px; font-size: 13px; color: #606266">
                      <span><el-icon><Phone /></el-icon> {{ candidateDetail.phone }}</span>
                      <span><el-icon><Message /></el-icon> {{ candidateDetail.email }}</span>
                    </div>
                  </div>
                  
                  <div style="text-align: right">
                    <el-button type="primary" size="small" @click="viewResume">查看简历</el-button>
                    <el-button type="success" size="small" @click="exportResume">导出简历</el-button>
                  </div>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 基本信息 -->
          <el-card shadow="never" class="info-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">👤 基本信息</span>
            </template>
            
            <el-descriptions :column="3" border>
              <el-descriptions-item label="性别">{{ candidateDetail.gender }}</el-descriptions-item>
              <el-descriptions-item label="年龄">{{ candidateDetail.age }}岁</el-descriptions-item>
              <el-descriptions-item label="生日">{{ candidateDetail.birthday }}</el-descriptions-item>
              <el-descriptions-item label="民族">{{ candidateDetail.nationality }}</el-descriptions-item>
              <el-descriptions-item label="现居地">{{ candidateDetail.city }} {{ candidateDetail.district }}</el-descriptions-item>
              <el-descriptions-item label="婚姻状况">{{ candidateDetail.maritalStatus }}</el-descriptions-item>
              <el-descriptions-item label="政治面貌">{{ candidateDetail.politicalStatus }}</el-descriptions-item>
            </el-descriptions>
          </el-card>

          <!-- 求职意向 -->
          <el-card shadow="never" class="info-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">💼 求职意向</span>
            </template>
            
            <el-descriptions :column="3" border>
              <el-descriptions-item label="期望职位">{{ candidateDetail.expectPosition }}</el-descriptions-item>
              <el-descriptions-item label="期望薪资">{{ candidateDetail.expectSalary }}</el-descriptions-item>
              <el-descriptions-item label="工作性质">{{ candidateDetail.workType }}</el-descriptions-item>
              <el-descriptions-item label="期望城市" :span="2">{{ candidateDetail.expectCity.join('、') }}</el-descriptions-item>
              <el-descriptions-item label="求职状态">{{ candidateDetail.status }}</el-descriptions-item>
              <el-descriptions-item label="期望行业">{{ candidateDetail.industry }}</el-descriptions-item>
            </el-descriptions>
          </el-card>

          <!-- 教育经历 -->
          <el-card shadow="never" class="info-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">🎓 教育经历</span>
            </template>
            
            <div v-for="(edu, index) in candidateDetail.educationDetail" :key="index" style="margin-bottom: 16px">
              <div style="display: flex; justify-content: space-between; margin-bottom: 8px">
                <div style="font-weight: 600">{{ edu.school }}</div>
                <div style="color: #909399">{{ edu.startDate }} - {{ edu.endDate }}</div>
              </div>
              <div style="color: #606266; font-size: 14px">
                {{ edu.major }} | {{ edu.degree }}
              </div>
            </div>
          </el-card>

          <!-- 工作经历 -->
          <el-card shadow="never" class="info-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">💻 工作经历</span>
            </template>
            
            <div v-for="(work, index) in candidateDetail.workDetail" :key="index" style="margin-bottom: 16px">
              <div style="display: flex; justify-content: space-between; margin-bottom: 8px">
                <div style="font-weight: 600">{{ work.company }}</div>
                <div style="color: #909399">{{ work.startDate }} - {{ work.endDate }}</div>
              </div>
              <div style="color: #606266; font-size: 14px; margin-bottom: 4px">{{ work.position }}</div>
              <div style="color: #909399; font-size: 13px">{{ work.description }}</div>
            </div>
          </el-card>

          <!-- 项目经历 -->
          <el-card shadow="never" class="info-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">🏆 项目经历（{{ candidateDetail.projectCount }}个）</span>
            </template>
            
            <div v-for="(proj, index) in candidateDetail.projectDetail" :key="index" style="margin-bottom: 16px">
              <div style="display: flex; justify-content: space-between; margin-bottom: 8px">
                <div style="font-weight: 600">{{ proj.name }}</div>
                <div style="color: #909399">{{ proj.startDate }} - {{ proj.endDate }}</div>
              </div>
              <div style="color: #606266; font-size: 14px; margin-bottom: 4px">{{ proj.role }}</div>
              <div style="color: #909399; font-size: 13px">{{ proj.description }}</div>
            </div>
          </el-card>

          <!-- 技能与证书 -->
          <el-card shadow="never" class="info-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">🛠️ 技能与证书</span>
            </template>
            
            <div style="margin-bottom: 16px">
              <div style="font-size: 13px; color: #909399; margin-bottom: 8px">专业技能</div>
              <el-tag
                v-for="(tag, index) in candidateDetail.skillTags"
                :key="index"
                type="info"
                size="small"
                style="margin-right: 8px; margin-bottom: 8px"
              >
                {{ tag }}
              </el-tag>
            </div>
            
            <div style="margin-bottom: 16px">
              <div style="font-size: 13px; color: #909399; margin-bottom: 8px">语言能力</div>
              <div v-for="(lang, index) in candidateDetail.languageSkills" :key="index" style="margin-bottom: 8px">
                <el-tag size="small">{{ lang.language }}: {{ lang.level }}</el-tag>
              </div>
            </div>
            
            <div>
              <div style="font-size: 13px; color: #909399; margin-bottom: 8px">证书与荣誉</div>
              <el-tag
                v-for="(cert, index) in candidateDetail.certificates"
                :key="index"
                type="success"
                size="small"
                style="margin-right: 8px; margin-bottom: 8px"
              >
                {{ cert }}
              </el-tag>
              <el-tag
                v-for="(award, index) in candidateDetail.awards"
                :key="index"
                type="warning"
                size="small"
                style="margin-right: 8px; margin-bottom: 8px"
              >
                {{ award }}
              </el-tag>
            </div>
          </el-card>

          <!-- 投递记录 -->
          <el-card shadow="never" class="info-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">📨 最近投递（{{ deliveryRecords.length }}）</span>
            </template>
            
            <el-table :data="deliveryRecords" style="width: 100%">
              <el-table-column prop="id" label="ID" width="60" />
              <el-table-column prop="company" label="企业" min-width="180" />
              <el-table-column prop="position" label="职位" min-width="160" />
              <el-table-column prop="salary" label="薪资" width="120" />
              <el-table-column prop="deliveryTime" label="投递时间" width="160" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="{ row }">
                  <el-tag 
                    :type="row.status === '待处理' ? 'warning' : row.status === '已查看' ? 'info' : 'success'" 
                    size="small"
                  >
                    {{ row.status }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>

        <!-- 右侧：状态与统计 -->
        <el-col :span="8">
          <!-- 账号状态 -->
          <el-card shadow="never" class="status-card">
            <template #header>
              <span style="font-weight: 600">🔐 账号状态</span>
            </template>
            
            <el-descriptions :column="1" border size="small">
              <el-descriptions-item label="当前状态">
                <el-tag type="success" size="small">{{ candidateDetail.accountStatus }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="实名认证">
                <el-tag type="success" size="small">{{ candidateDetail.verificationStatus }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="简历状态">{{ candidateDetail.resumeStatus }}</el-descriptions-item>
              <el-descriptions-item label="完整度">
                <el-progress :percentage="candidateDetail.resumeCompleteRate" :stroke-width="12" />
              </el-descriptions-item>
              <el-descriptions-item label="风险等级">
                <el-tag type="success" size="small">{{ candidateDetail.riskLevel }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="黑名单">
                <el-tag type="success" size="small">{{ candidateDetail.blacklistStatus }}</el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="投诉次数">{{ candidateDetail.complaintCount }}</el-descriptions-item>
            </el-descriptions>
            
            <el-divider />
            
            <el-button type="warning" plain style="width: 100%; margin-bottom: 8px" @click="handleFreeze">
              冻结账号
            </el-button>
            <el-button type="danger" plain style="width: 100%" @click="handleBan">
              永久封禁
            </el-button>
          </el-card>

          <!-- 统计数据 -->
          <el-card shadow="never" class="status-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">📊 活跃数据</span>
            </template>
            
            <el-row :gutter="12">
              <el-col :span="12">
                <el-statistic title="被查看" :value="candidateDetail.viewCount">
                  <template #suffix>次</template>
                </el-statistic>
              </el-col>
              <el-col :span="12">
                <el-statistic title="投递数" :value="candidateDetail.deliveryCount">
                  <template #suffix>份</template>
                </el-statistic>
              </el-col>
              <el-col :span="12">
                <el-statistic title="面试数" :value="candidateDetail.interviewCount">
                  <template #suffix>次</template>
                </el-statistic>
              </el-col>
              <el-col :span="12">
                <el-statistic title="Offer 数" :value="candidateDetail.offerCount">
                  <template #suffix>个</template>
                </el-statistic>
              </el-col>
              <el-col :span="12">
                <el-statistic title="被收藏" :value="candidateDetail.favoriteCount">
                  <template #suffix>次</template>
                </el-statistic>
              </el-col>
              <el-col :span="12">
                <el-statistic title="登录频率" :value="每天" />
              </el-col>
            </el-row>
            
            <el-divider />
            
            <div style="font-size: 13px; color: #909399; margin-bottom: 8px">
              平均响应时间：<el-tag type="success" size="small">{{ candidateDetail.avgResponseTime }}</el-tag>
            </div>
            <div style="font-size: 13px; color: #909399; margin-bottom: 8px">
              最后活跃：<div>{{ candidateDetail.lastActiveTime }}</div>
            </div>
          </el-card>

          <!-- 时间线 -->
          <el-card shadow="never" class="status-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">⏰ 关键时间点</span>
            </template>
            
            <el-timeline>
              <el-timeline-item timestamp="2026-03-28" placement="top">
                更新简历
              </el-timeline-item>
              <el-timeline-item timestamp="2026-03-31" placement="top">
                最近活跃
              </el-timeline-item>
              <el-timeline-item timestamp="2025-01-15" placement="top">
                注册账号
              </el-timeline-item>
            </el-timeline>
          </el-card>

          <!-- 沟通记录 -->
          <el-card shadow="never" class="status-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">💬 沟通记录（{{ chatRecords.length }}）</span>
            </template>
            
            <el-timeline>
              <el-timeline-item 
                v-for="(chat, index) in chatRecords" 
                :key="index"
                :timestamp="chat.time"
                placement="top"
              >
                <div style="font-weight: 600">{{ chat.company }} · {{ chat.hr }}</div>
                <div style="font-size: 12px; color: #909399; margin-top: 4px">{{ chat.lastMessage }}</div>
                <el-tag v-if="chat.unread > 0" type="danger" size="small" style="margin-top: 4px">未读 {{ chat.unread }}</el-tag>
              </el-timeline-item>
            </el-timeline>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <template #footer>
      <el-button @click="handleClose">关闭</el-button>
      <el-button type="primary" @click="handleEdit">编辑信息</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.candidate-detail {
  max-height: 80vh;
  overflow-y: auto;
  padding-right: 10px;
}

.profile-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.profile-card :deep(.el-icon) {
  color: white;
}

.info-card, .status-card {
  margin-bottom: 16px;
}

:deep(.el-descriptions__label) {
  width: 120px;
  font-weight: 500;
}

:deep(.el-statistic__content) {
  font-size: 20px;
  font-weight: 600;
}
</style>
