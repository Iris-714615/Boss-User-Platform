<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User,
  OfficeBuilding,
  Location,
  Money,
  TrendCharts,
  Document,
  Timer,
  Phone,
  Notebook,
  Warning,
  CircleCheck
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const dialogVisible = ref(true)

// 企业详细信息
const companyDetail = reactive({
  id: '10001',
  name: '示例科技有限公司',
  legalPerson: '张三',
  registeredCapital: '1000 万人民币',
  establishmentDate: '2018-05-20',
  registrationStatus: '存续',
  unifiedSocialCreditCode: '91310000MA1K3YJXX5',
  organizationCode: 'MA1K3YJXX',
  industry: '互联网/软件',
  companySize: '100-499 人',
  financingStage: 'B 轮',
  headquarters: '上海市浦东新区张江高科技园区',
  businessScope: '从事网络科技、计算机科技领域内的技术开发、技术咨询、技术转让、技术服务',
  website: 'www.example.com',
  email: 'hr@example.com',
  phone: '021-12345678',
  
  // 认证信息
  certificationStatus: '已认证',
  certificationTime: '2026-03-01 10:30',
  certificationType: '企业认证 + 营业执照认证',
  
  // 账号状态
  accountStatus: '正常',
  riskLevel: '低风险',
  blacklistStatus: '未封禁',
  
  // 统计数据
  totalPositions: 28,
  activePositions: 15,
  totalCandidates: 1256,
  todayActive: 45,
  totalChatCount: 3580,
  complaintCount: 2,
  
  // 最近操作
  lastLoginTime: '2026-03-31 09:15:23',
  lastPublishTime: '2026-03-30 16:20:00',
  createTime: '2026-01-15 14:30:00',
  updateTime: '2026-03-31 10:00:00',
  
  // 标签
  tags: ['高新技术企业', '瞪羚企业', '周末双休', '五险一金'],
  
  // 地址详情
  address: '上海市浦东新区张江高科技园区科苑路 88 号',
  longitude: 121.604,
  latitude: 31.202,
  
  // 团队成员
  teamMembers: [
    { id: 1, name: '张经理', phone: '138****0001', email: 'zhang***@example.com', role: '超级管理员', department: '人事部', status: '正常', joinDate: '2025-01-15', lastLogin: '2026-03-31 09:30' },
    { id: 2, name: '李 HR', phone: '139****0002', email: 'li***@example.com', role: 'HR 经理', department: '人事部', status: '正常', joinDate: '2025-03-20', lastLogin: '2026-03-31 08:45' },
    { id: 3, name: '王招聘', phone: '137****0003', email: 'wang***@example.com', role: '招聘专员', department: '人事部', status: '正常', joinDate: '2025-06-10', lastLogin: '2026-03-30 17:20' },
  ]
})

// 在招职位列表
const positionsList = ref([
  { id: 1, title: '高级前端工程师', salary: '25-35K', experience: '3-5 年', education: '本科', city: '上海', status: '招聘中', deliveryCount: 156 },
  { id: 2, title: 'Java 开发工程师', salary: '20-30K', experience: '1-3 年', education: '本科', city: '上海', status: '招聘中', deliveryCount: 203 },
  { id: 3, title: '产品经理', salary: '18-25K', experience: '3-5 年', education: '本科', city: '上海', status: '招聘中', deliveryCount: 89 },
])

// 沟通记录
const chatRecords = ref([
  { id: 1, candidate: '张先生', position: '高级前端工程师', lastMessage: '您好，我对这个职位很感兴趣', time: '2026-03-31 10:25', unread: 2 },
  { id: 2, candidate: '李女士', position: 'Java 开发工程师', lastMessage: '请问上班时间是怎么安排的？', time: '2026-03-31 09:50', unread: 0 },
])

const handleClose = () => {
  dialogVisible.value = false
  router.back()
}

const handleEdit = () => {
  ElMessage.info('编辑企业信息功能待开发')
}

const handleBan = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要封禁企业"${companyDetail.name}"吗？封禁后将无法发布职位和查看简历。`,
      '封禁警告',
      {
        confirmButtonText: '确认封禁',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    ElMessage.success('企业已封禁')
  } catch {
    // 取消操作
  }
}

const handleUnban = () => {
  ElMessage.info('解封功能待开发')
}

const viewCertification = () => {
  ElMessage.info('查看资质功能待开发')
}

const viewRiskDetail = () => {
  ElMessage.info('风险详情功能待开发')
}
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="`企业详情 - ${companyDetail.name}`"
    width="90%"
    top="5vh"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-loading="loading" class="company-detail">
      <!-- 基本信息卡片 -->
      <el-card shadow="never" class="info-card">
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center">
            <span style="font-weight: 600">基本信息</span>
            <el-button type="primary" size="small" @click="handleEdit">编辑</el-button>
          </div>
        </template>
        
        <el-descriptions :column="3" border>
          <el-descriptions-item label="企业名称">{{ companyDetail.name }}</el-descriptions-item>
          <el-descriptions-item label="法人代表">{{ companyDetail.legalPerson }}</el-descriptions-item>
          <el-descriptions-item label="注册资本">{{ companyDetail.registeredCapital }}</el-descriptions-item>
          <el-descriptions-item label="成立日期">{{ companyDetail.establishmentDate }}</el-descriptions-item>
          <el-descriptions-item label="登记状态">{{ companyDetail.registrationStatus }}</el-descriptions-item>
          <el-descriptions-item label="行业">{{ companyDetail.industry }}</el-descriptions-item>
          <el-descriptions-item label="公司规模">{{ companyDetail.companySize }}</el-descriptions-item>
          <el-descriptions-item label="融资阶段">{{ companyDetail.financingStage }}</el-descriptions-item>
          <el-descriptions-item label="总部地点">{{ companyDetail.headquarters }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 认证与资质 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center">
            <span style="font-weight: 600">认证与资质</span>
            <el-button type="primary" size="small" @click="viewCertification">查看资质</el-button>
          </div>
        </template>
        
        <el-descriptions :column="3" border>
          <el-descriptions-item label="认证状态">
            <el-tag type="success" size="small">{{ companyDetail.certificationStatus }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="认证时间">{{ companyDetail.certificationTime }}</el-descriptions-item>
          <el-descriptions-item label="认证类型">{{ companyDetail.certificationType }}</el-descriptions-item>
          <el-descriptions-item label="统一社会信用代码" :span="3">{{ companyDetail.unifiedSocialCreditCode }}</el-descriptions-item>
          <el-descriptions-item label="组织机构代码">{{ companyDetail.organizationCode }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 账号状态 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center">
            <span style="font-weight: 600">账号状态</span>
            <div>
              <el-button 
                v-if="companyDetail.accountStatus === '正常'" 
                type="danger" 
                size="small" 
                @click="handleBan"
              >
                封禁
              </el-button>
              <el-button v-else type="success" size="small" @click="handleUnban">解封</el-button>
            </div>
          </div>
        </template>
        
        <el-descriptions :column="3" border>
          <el-descriptions-item label="账号状态">
            <el-tag :type="companyDetail.accountStatus === '正常' ? 'success' : 'danger'" size="small">
              {{ companyDetail.accountStatus }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="风险等级">
            <el-tag 
              :type="companyDetail.riskLevel === '低风险' ? 'success' : companyDetail.riskLevel === '中风险' ? 'warning' : 'danger'" 
              size="small"
              @click="viewRiskDetail"
              style="cursor: pointer"
            >
              {{ companyDetail.riskLevel }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="黑名单状态">
            <el-tag :type="companyDetail.blacklistStatus === '未封禁' ? 'success' : 'danger'" size="small">
              {{ companyDetail.blacklistStatus }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="投诉次数">{{ companyDetail.complaintCount }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 统计数据 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <span style="font-weight: 600">运营数据</span>
        </template>
        
        <el-row :gutter="16">
          <el-col :span="6">
            <el-statistic title="在招职位" :value="companyDetail.totalPositions">
              <template #suffix>个</template>
            </el-statistic>
          </el-col>
          <el-col :span="6">
            <el-statistic title="活跃职位" :value="companyDetail.activePositions">
              <template #suffix>个</template>
            </el-statistic>
          </el-col>
          <el-col :span="6">
            <el-statistic title="累计收到简历" :value="companyDetail.totalCandidates">
              <template #suffix>份</template>
            </el-statistic>
          </el-col>
          <el-col :span="6">
            <el-statistic title="今日活跃" :value="companyDetail.todayActive">
              <template #suffix>次</template>
            </el-statistic>
          </el-col>
        </el-row>
        
        <el-divider />
        
        <el-row :gutter="16">
          <el-col :span="8">
            <el-statistic title="总沟通数" :value="companyDetail.totalChatCount">
              <template #suffix>次</template>
            </el-statistic>
          </el-col>
          <el-col :span="8">
            <el-statistic title="最近登录" :value="companyDetail.lastLoginTime" />
          </el-col>
          <el-col :span="8">
            <el-statistic title="最近发布" :value="companyDetail.lastPublishTime" />
          </el-col>
        </el-row>
      </el-card>

      <!-- 联系方式 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <span style="font-weight: 600">联系方式</span>
        </template>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="联系电话">{{ companyDetail.phone }}</el-descriptions-item>
          <el-descriptions-item label="电子邮箱">{{ companyDetail.email }}</el-descriptions-item>
          <el-descriptions-item label="公司网站">{{ companyDetail.website }}</el-descriptions-item>
          <el-descriptions-item label="办公地址" :span="2">{{ companyDetail.address }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 在招职位 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <span style="font-weight: 600">在招职位（{{ positionsList.length }}）</span>
        </template>
        
        <el-table :data="positionsList" style="width: 100%">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="title" label="职位名称" min-width="180" />
          <el-table-column prop="salary" label="薪资" width="120" />
          <el-table-column prop="experience" label="经验" width="100" />
          <el-table-column prop="education" label="学历" width="100" />
          <el-table-column prop="city" label="城市" width="100" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag type="success" size="small">{{ row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="deliveryCount" label="投递数" width="100" />
          <el-table-column label="操作" width="120">
            <template #default>
              <el-button text type="primary" size="small">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 最近沟通 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <span style="font-weight: 600">最近沟通（{{ chatRecords.length }}）</span>
        </template>
        
        <el-table :data="chatRecords" style="width: 100%">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="candidate" label="求职者" width="120" />
          <el-table-column prop="position" label="职位" min-width="160" />
          <el-table-column prop="lastMessage" label="最近消息" min-width="200" show-overflow-tooltip />
          <el-table-column prop="time" label="时间" width="160" />
          <el-table-column prop="unread" label="未读" width="80">
            <template #default="{ row }">
              <el-tag v-if="row.unread > 0" type="danger" size="small">{{ row.unread }}</el-tag>
              <span v-else>-</span>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
      
      <!-- 团队成员 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <span style="font-weight: 600">👥 团队成员（{{ companyDetail.teamMembers.length }}）</span>
        </template>
        
        <el-table :data="companyDetail.teamMembers" style="width: 100%">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="name" label="姓名" width="100" />
          <el-table-column prop="role" label="角色" width="120">
            <template #default="{ row }">
              <el-tag :type="row.role === '超级管理员' ? 'danger' : row.role === 'HR 经理' ? 'warning' : ''" size="small">
                {{ row.role }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="department" label="部门" width="120" />
          <el-table-column prop="phone" label="手机号" width="140" />
          <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === '正常' ? 'success' : 'danger'" size="small">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="joinDate" label="加入日期" width="120" />
          <el-table-column prop="lastLogin" label="最后登录" width="160" />
        </el-table>
      </el-card>
    </div>

    <template #footer>
      <el-button @click="handleClose">关闭</el-button>
      <el-button type="primary" @click="handleEdit">编辑信息</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.company-detail {
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 10px;
}

.info-card {
  margin-bottom: 16px;
}

:deep(.el-descriptions__label) {
  width: 140px;
  font-weight: 500;
}
</style>
