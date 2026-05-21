<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Clock, Warning } from '@element-plus/icons-vue'

const router = useRouter()

const query = reactive({
  keyword: '',
  submitTimeStart: '',
  submitTimeEnd: '',
})

// 待审核企业列表
const auditList = ref([
  { 
    id: 1, 
    name: '某某信息科技有限公司', 
    legalPerson: '李四',
    unifiedSocialCreditCode: '91310000MA1K3YJXX6',
    industry: '互联网/软件',
    city: '北京',
    submitTime: '2026-03-31 09:30:00',
    auditType: '新企业认证',
    priority: '高',
  },
  { 
    id: 2, 
    name: '科技创新公司', 
    legalPerson: '王五',
    unifiedSocialCreditCode: '91310000MA1K3YJXX7',
    industry: '人工智能',
    city: '杭州',
    submitTime: '2026-03-31 10:15:00',
    auditType: '资质更新',
    priority: '中',
  },
  { 
    id: 3, 
    name: '网络科技公司', 
    legalPerson: '赵六',
    unifiedSocialCreditCode: '91310000MA1K3YJXX8',
    industry: '互联网/软件',
    city: '广州',
    submitTime: '2026-03-31 11:20:00',
    auditType: '新企业认证',
    priority: '高',
  },
  { 
    id: 4, 
    name: '电子商务公司', 
    legalPerson: '孙七',
    unifiedSocialCreditCode: '91310000MA1K3YJXX9',
    industry: '电子商务',
    city: '上海',
    submitTime: '2026-03-30 16:40:00',
    auditType: '信息变更',
    priority: '低',
  },
])

// 分页数据
const pagination = reactive({
  total: 23,
  currentPage: 1,
  pageSize: 10,
  pageSizes: [10, 20, 50, 100],
})

// 统计信息
const auditStats = reactive({
  totalPending: 23,
  todayPending: 8,
  highPriority: 5,
  overdueRisk: 2,
})

const onSearch = () => {
  console.log('search audit list', query)
  ElMessage.success('查询成功')
}

const handleAudit = (row: any) => {
  router.push(`/admin/certification-audit/${row.id}`)
}

const handleBatchApprove = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要批量通过选中的 ${selectedRows.value.length} 家企业吗？`,
      '批量通过确认',
      {
        confirmButtonText: '确认通过',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    ElMessage.success(`已批量通过 ${selectedRows.value.length} 家企业`)
    selectedRows.value = []
  } catch {
    // 取消操作
  }
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
}

// 批量选择
const selectedRows = ref<any[]>([])

const handleSelectionChange = (selection: any[]) => {
  selectedRows.value = selection
}
</script>

<template>
  <div class="certification-list-page">
    <!-- 统计卡片 -->
    <el-row :gutter="16" style="margin-bottom: 20px">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div style="display: flex; align-items: center; gap: 12px">
            <div style="background: #409EFF; color: white; padding: 12px; border-radius: 8px">
              <el-icon :size="24"><Document /></el-icon>
            </div>
            <div>
              <div style="font-size: 13px; color: #909399">待审核总数</div>
              <div style="font-size: 24px; font-weight: 700">{{ auditStats.totalPending }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div style="display: flex; align-items: center; gap: 12px">
            <div style="background: #67C23A; color: white; padding: 12px; border-radius: 8px">
              <el-icon :size="24"><Clock /></el-icon>
            </div>
            <div>
              <div style="font-size: 13px; color: #909399">今日新增</div>
              <div style="font-size: 24px; font-weight: 700">{{ auditStats.todayPending }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div style="display: flex; align-items: center; gap: 12px">
            <div style="background: #E6A23C; color: white; padding: 12px; border-radius: 8px">
              <el-icon :size="24"><Warning /></el-icon>
            </div>
            <div>
              <div style="font-size: 13px; color: #909399">高优先级</div>
              <div style="font-size: 24px; font-weight: 700">{{ auditStats.highPriority }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div style="display: flex; align-items: center; gap: 12px">
            <div style="background: #F56C6C; color: white; padding: 12px; border-radius: 8px">
              <el-icon :size="24"><Warning /></el-icon>
            </div>
            <div>
              <div style="font-size: 13px; color: #909399">超时风险</div>
              <div style="font-size: 24px; font-weight: 700">{{ auditStats.overdueRisk }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 搜索栏 -->
    <el-card shadow="never" style="margin-bottom: 16px">
      <el-form :inline="true" :model="query" style="margin-bottom: 0">
        <el-form-item label="企业名称">
          <el-input 
            v-model="query.keyword" 
            placeholder="请输入企业名称" 
            clearable
            style="width: 240px" 
          />
        </el-form-item>
        <el-form-item label="提交时间">
          <el-date-picker
            v-model="query.submitTimeStart"
            type="date"
            placeholder="开始日期"
            style="width: 180px"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="至">
          <el-date-picker
            v-model="query.submitTimeEnd"
            type="date"
            placeholder="结束日期"
            style="width: 180px"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSearch">查询</el-button>
          <el-button @click="query.keyword = ''; query.submitTimeStart = ''; query.submitTimeEnd = ''">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 批量操作工具栏 -->
    <el-card shadow="never" style="margin-bottom: 16px">
      <div style="display: flex; justify-content: space-between; align-items: center">
        <div style="color: #606266">
          <span v-if="selectedRows.length > 0">
            已选择 <strong style="color: #409EFF">{{ selectedRows.length }}</strong> 家企业
          </span>
          <span v-else style="color: #909399">
            请勾选需要批量审核的企业
          </span>
        </div>
        <div>
          <el-button 
            type="success" 
            :disabled="selectedRows.length === 0"
            @click="handleBatchApprove"
          >
            批量通过
          </el-button>
          <el-button type="info">
            导出列表
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 审核列表表格 -->
    <el-card shadow="never">
      <el-table 
        :data="auditList" 
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="企业名称" min-width="220">
          <template #default="{ row }">
            <div style="display: flex; align-items: center; gap: 8px">
              <span>{{ row.name }}</span>
              <el-tag 
                v-if="row.priority === '高'" 
                type="danger" 
                size="small"
              >
                加急
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="legalPerson" label="法人" width="120" />
        <el-table-column prop="unifiedSocialCreditCode" label="统一社会信用代码" min-width="200" show-overflow-tooltip />
        <el-table-column prop="industry" label="行业" width="140" />
        <el-table-column prop="city" label="城市" width="100" />
        <el-table-column prop="auditType" label="审核类型" width="120">
          <template #default="{ row }">
            <el-tag 
              :type="row.auditType === '新企业认证' ? 'primary' : row.auditType === '资质更新' ? 'warning' : 'info'" 
              size="small"
            >
              {{ row.auditType }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="submitTime" label="提交时间" width="170" />
        <el-table-column label="操作" width="140" fixed="right">
          <template #default="{ row }">
            <el-button 
              text 
              type="primary" 
              @click="handleAudit(row)"
            >
              审核
            </el-button>
            <el-button text>
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div style="margin-top: 16px; display: flex; justify-content: flex-end">
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="pagination.pageSizes"
          :total="pagination.total"
          background
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.certification-list-page {
  padding: 20px;
}

.stat-card {
  margin-bottom: 16px;
}

.stat-card:hover {
  transform: translateY(-2px);
  transition: all 0.3s;
}
</style>
