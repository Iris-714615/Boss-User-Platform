<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Briefcase,
  Money,
  Location,
  User,
  TrendCharts,
  Document,
  Timer,
  Warning,
  CircleCheck,
  OfficeBuilding,
  Notebook,
  Calendar
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const dialogVisible = ref(true)

// 职位详细信息
const positionDetail = reactive({
  id: '30001',
  title: '高级前端工程师',
  company: {
    id: 10001,
    name: '示例科技有限公司',
    scale: '100-499 人',
    industry: '互联网/软件',
    financing: 'B 轮',
  },
  
  // 薪资福利
  salary: '25-35K',
  salaryDetail: {
    min: 25,
    max: 35,
    unit: 'K·15 薪',
    yearSalary: '37.5-52.5 万',
  },
  benefits: ['五险一金', '补充商业保险', '年终奖', '股票期权', '带薪年假', '定期体检', '节日福利', '团建活动'],
  
  // 职位要求
  experience: '3-5 年',
  education: '本科',
  age: '25-35 岁',
  skillTags: ['Vue', 'React', 'TypeScript', 'JavaScript', 'HTML5', 'CSS3', 'Node.js', 'Webpack'],
  
  // 工作地点
  city: '上海',
  district: '浦东新区',
  address: '张江高科技园区科苑路 88 号',
  longitude: 121.604,
  latitude: 31.202,
  
  // 招聘详情
  recruitmentCount: 5,
  positionType: '全职',
  department: '技术部 - 前端组',
  reportTo: '前端技术总监',
  workType: '朝九晚六，周末双休',
  
  // 职位描述
  description: `【岗位职责】
1. 负责公司核心产品的前端架构设计与开发
2. 参与产品需求分析，优化用户体验
3. 指导初级工程师，进行代码 review
4. 持续优化前端性能，提升页面加载速度

【任职要求】
1. 计算机相关专业本科及以上学历，3-5 年前端开发经验
2. 精通 Vue/React 框架，深入理解其原理
3. 熟练掌握 TypeScript，有良好的代码规范
4. 熟悉前端工程化，有 Webpack/Vite 实战经验
5. 具备良好的沟通能力和团队协作精神

【加分项】
1. 有大型项目架构经验
2. 开源项目贡献者
3. 技术博客作者`,
  
  // 状态信息
  status: '招聘中',
  auditStatus: '已通过',
  auditTime: '2026-03-01 10:30',
  auditor: '系统自动审核',
  
  // 统计数据
  viewCount: 15623,
  deliveryCount: 356,
  chatCount: 128,
  interviewCount: 45,
  offerCount: 12,
  favoriteCount: 892,
  
  // 时间信息
  publishTime: '2026-03-01 09:00:00',
  updateTime: '2026-03-30 16:20:00',
  deadline: '2026-06-01 23:59:59',
  createTime: '2026-02-28 14:30:00',
  
  // 风险标识
  riskLevel: '低风险',
  complaintCount: 0,
  blacklistReason: '',
})

// 投递记录
const deliveryRecords = ref([
  { id: 1, candidate: '张先生', resume: '5 年前端经验 | 硕士', deliveryTime: '2026-03-31 09:15', status: '待处理', matchRate: 92 },
  { id: 2, candidate: '李女士', resume: '3 年前端经验 | 本科', deliveryTime: '2026-03-30 16:40', status: '已查看', matchRate: 88 },
  { id: 3, candidate: '王先生', resume: '4 年前端经验 | 本科', deliveryTime: '2026-03-30 14:20', status: '已沟通', matchRate: 85 },
  { id: 4, candidate: '赵女士', resume: '6 年前端经验 | 硕士', deliveryTime: '2026-03-29 11:30', status: '面试中', matchRate: 95 },
])

// 沟通记录摘要
const chatSummary = ref([
  { id: 1, candidate: '张先生', lastMessage: '您好，我对这个职位很感兴趣', time: '2026-03-31 10:25', unread: 2 },
  { id: 2, candidate: '李女士', lastMessage: '请问上班时间是怎么安排的？', time: '2026-03-31 09:50', unread: 0 },
  { id: 3, candidate: '王先生', lastMessage: '可以远程面试吗？', time: '2026-03-30 15:30', unread: 1 },
])

const handleClose = () => {
  dialogVisible.value = false
  router.back()
}

const handleEdit = () => {
  ElMessage.info('编辑职位功能待开发')
}

const handleOffline = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要下架职位"${positionDetail.title}"吗？下架后将不再展示给求职者。`,
      '下架确认',
      {
        confirmButtonText: '确认下架',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    ElMessage.success('职位已下架')
  } catch {
    // 取消操作
  }
}

const handleBan = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要封禁职位"${positionDetail.title}"吗？此操作不可恢复。`,
      '封禁警告',
      {
        confirmButtonText: '确认封禁',
        cancelButtonText: '取消',
        type: 'error',
      }
    )
    ElMessage.success('职位已封禁')
  } catch {
    // 取消操作
  }
}

const viewCompanyDetail = () => {
  router.push(`/admin/companies/${positionDetail.company.id}`)
}

const viewDeliveryDetail = (row: any) => {
  ElMessage.info(`查看 ${row.candidate} 的投递详情`)
}

const exportData = () => {
  ElMessage.info('导出数据功能待开发')
}
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="`职位详情 - ${positionDetail.title}`"
    width="90%"
    top="5vh"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-loading="loading" class="position-detail">
      <!-- 基本信息卡片 -->
      <el-card shadow="never" class="info-card">
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center">
            <span style="font-weight: 600">基本信息</span>
            <div>
              <el-button type="primary" size="small" @click="handleEdit">编辑</el-button>
              <el-button 
                v-if="positionDetail.status === '招聘中'" 
                type="warning" 
                size="small" 
                @click="handleOffline"
              >
                下架
              </el-button>
              <el-button type="danger" size="small" @click="handleBan">封禁</el-button>
            </div>
          </div>
        </template>
        
        <el-descriptions :column="3" border>
          <el-descriptions-item label="职位名称" :span="2">{{ positionDetail.title }}</el-descriptions-item>
          <el-descriptions-item label="职位 ID">{{ positionDetail.id }}</el-descriptions-item>
          <el-descriptions-item label="所属企业">
            <el-button text type="primary" @click="viewCompanyDetail">{{ positionDetail.company.name }}</el-button>
          </el-descriptions-item>
          <el-descriptions-item label="企业规模">{{ positionDetail.company.scale }}</el-descriptions-item>
          <el-descriptions-item label="所属行业">{{ positionDetail.company.industry }}</el-descriptions-item>
          <el-descriptions-item label="融资阶段">{{ positionDetail.company.financing }}</el-descriptions-item>
          <el-descriptions-item label="工作性质">{{ positionDetail.positionType }}</el-descriptions-item>
          <el-descriptions-item label="所属部门">{{ positionDetail.department }}</el-descriptions-item>
          <el-descriptions-item label="汇报对象">{{ positionDetail.reportTo }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 薪资与福利 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <span style="font-weight: 600">💰 薪资福利</span>
        </template>
        
        <el-row :gutter="20">
          <el-col :span="8">
            <el-statistic title="月薪范围" :value="`${positionDetail.salaryDetail.min}-${positionDetail.salaryDetail.max}`">
              <template #suffix>K</template>
            </el-statistic>
          </el-col>
          <el-col :span="8">
            <el-statistic title="年薪范围" :value="positionDetail.salaryDetail.yearSalary">
              <template #suffix>万</template>
            </el-statistic>
          </el-col>
          <el-col :span="8">
            <el-statistic title="发放月数" :value="15">
              <template #suffix>薪</template>
            </el-statistic>
          </el-col>
        </el-row>
        
        <el-divider />
        
        <div style="margin-top: 12px">
          <div style="font-size: 13px; color: #909399; margin-bottom: 8px">福利待遇</div>
          <el-tag
            v-for="(benefit, index) in positionDetail.benefits"
            :key="index"
            type="success"
            size="small"
            style="margin-right: 8px; margin-bottom: 8px"
          >
            {{ benefit }}
          </el-tag>
        </div>
      </el-card>

      <!-- 职位要求 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <span style="font-weight: 600">📋 职位要求</span>
        </template>
        
        <el-descriptions :column="3" border>
          <el-descriptions-item label="工作经验">{{ positionDetail.experience }}</el-descriptions-item>
          <el-descriptions-item label="学历要求">{{ positionDetail.education }}</el-descriptions-item>
          <el-descriptions-item label="年龄范围">{{ positionDetail.age }}</el-descriptions-item>
          <el-descriptions-item label="技能标签" :span="3">
            <el-tag
              v-for="(tag, index) in positionDetail.skillTags"
              :key="index"
              type="info"
              size="small"
              style="margin-right: 8px; margin-bottom: 8px"
            >
              {{ tag }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 工作地点 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <span style="font-weight: 600">📍 工作地点</span>
        </template>
        
        <el-descriptions :column="2" border>
          <el-descriptions-item label="城市">{{ positionDetail.city }}</el-descriptions-item>
          <el-descriptions-item label="区县">{{ positionDetail.district }}</el-descriptions-item>
          <el-descriptions-item label="详细地址" :span="2">{{ positionDetail.address }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 审核与状态 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <span style="font-weight: 600">✅ 审核与状态</span>
        </template>
        
        <el-descriptions :column="3" border>
          <el-descriptions-item label="当前状态">
            <el-tag type="success" size="small">{{ positionDetail.status }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="审核状态">
            <el-tag type="success" size="small">{{ positionDetail.auditStatus }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="审核时间">{{ positionDetail.auditTime }}</el-descriptions-item>
          <el-descriptions-item label="审核人">{{ positionDetail.auditor }}</el-descriptions-item>
          <el-descriptions-item label="风险等级">
            <el-tag type="success" size="small">{{ positionDetail.riskLevel }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="投诉次数">{{ positionDetail.complaintCount }}</el-descriptions-item>
          <el-descriptions-item label="发布时间">{{ positionDetail.publishTime }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ positionDetail.updateTime }}</el-descriptions-item>
          <el-descriptions-item label="截止日期">{{ positionDetail.deadline }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- 统计数据 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <div style="display: flex; justify-content: space-between; align-items: center">
            <span style="font-weight: 600">📊 招聘效果数据</span>
            <el-button type="primary" size="small" @click="exportData">导出数据</el-button>
          </div>
        </template>
        
        <el-row :gutter="16">
          <el-col :span="4">
            <el-statistic title="被浏览" :value="positionDetail.viewCount">
              <template #suffix>次</template>
            </el-statistic>
          </el-col>
          <el-col :span="4">
            <el-statistic title="被投递" :value="positionDetail.deliveryCount">
              <template #suffix>份</template>
            </el-statistic>
          </el-col>
          <el-col :span="4">
            <el-statistic title="沟通数" :value="positionDetail.chatCount">
              <template #suffix>次</template>
            </el-statistic>
          </el-col>
          <el-col :span="4">
            <el-statistic title="面试数" :value="positionDetail.interviewCount">
              <template #suffix>人</template>
            </el-statistic>
          </el-col>
          <el-col :span="4">
            <el-statistic title="Offer 数" :value="positionDetail.offerCount">
              <template #suffix>个</template>
            </el-statistic>
          </el-col>
          <el-col :span="4">
            <el-statistic title="被收藏" :value="positionDetail.favoriteCount">
              <template #suffix>次</template>
            </el-statistic>
          </el-col>
        </el-row>
        
        <el-divider />
        
        <el-row :gutter="16">
          <el-col :span="8">
            <div style="font-size: 13px; color: #909399; margin-bottom: 8px">投递转化率</div>
            <el-progress 
              :percentage="Math.round((positionDetail.interviewCount / positionDetail.deliveryCount) * 100)" 
              :color="'#409EFF'"
            />
          </el-col>
          <el-col :span="8">
            <div style="font-size: 13px; color: #909399; margin-bottom: 8px">面试通过率</div>
            <el-progress 
              :percentage="Math.round((positionDetail.offerCount / positionDetail.interviewCount) * 100)" 
              :color="'#67C23A'"
            />
          </el-col>
          <el-col :span="8">
            <div style="font-size: 13px; color: #909399; margin-bottom: 8px">平均响应时间</div>
            <el-tag type="success" size="small">2.5 小时</el-tag>
          </el-col>
        </el-row>
      </el-card>

      <!-- 职位描述详情 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <span style="font-weight: 600">📝 职位描述详情</span>
        </template>
        
        <div class="description-content" v-html="positionDetail.description.replace(/\n/g, '<br>')"></div>
      </el-card>

      <!-- 投递记录 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <span style="font-weight: 600">📨 最近投递（{{ deliveryRecords.length }}）</span>
        </template>
        
        <el-table :data="deliveryRecords" style="width: 100%">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="candidate" label="求职者" width="120" />
          <el-table-column prop="resume" label="简历摘要" min-width="200" />
          <el-table-column prop="deliveryTime" label="投递时间" width="160" />
          <el-table-column prop="matchRate" label="匹配度" width="100">
            <template #default="{ row }">
              <el-tag 
                :type="row.matchRate >= 90 ? 'success' : row.matchRate >= 80 ? 'warning' : 'info'" 
                size="small"
              >
                {{ row.matchRate }}%
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag 
                :type="row.status === '待处理' ? 'warning' : row.status === '已查看' ? 'info' : row.status === '已沟通' ? 'primary' : 'success'" 
                size="small"
              >
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template #default="{ row }">
              <el-button text type="primary" size="small" @click="viewDeliveryDetail(row)">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <!-- 沟通记录 -->
      <el-card shadow="never" class="info-card" style="margin-top: 16px">
        <template #header>
          <span style="font-weight: 600">💬 最近沟通（{{ chatSummary.length }}）</span>
        </template>
        
        <el-table :data="chatSummary" style="width: 100%">
          <el-table-column prop="id" label="ID" width="60" />
          <el-table-column prop="candidate" label="求职者" width="120" />
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
    </div>

    <template #footer>
      <el-button @click="handleClose">关闭</el-button>
      <el-button type="primary" @click="handleEdit">编辑职位</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.position-detail {
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 10px;
}

.info-card {
  margin-bottom: 16px;
}

.description-content {
  line-height: 1.8;
  color: #303133;
  font-size: 14px;
  padding: 10px 0;
}

:deep(.el-descriptions__label) {
  width: 140px;
  font-weight: 500;
}

:deep(.el-statistic__content) {
  font-size: 24px;
  font-weight: 600;
}
</style>
