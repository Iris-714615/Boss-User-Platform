<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { CompanyStatus } from 'shared-types'

const router = useRouter()

const query = reactive({
  keyword: '',
  status: '',
  page: 1,
  pageSize: 10,
})

// 使用统一的公司数据结构
const tableData = ref([
  { 
    id: 'company_001', 
    name: '示例科技有限公司', 
    industry: '互联网/软件', 
    city: '上海', 
    district: '浦东新区',
    status: CompanyStatus.ACTIVE, 
    createdAt: 1711900800000,
    updatedAt: 1711900800000
  },
  { 
    id: 'company_002', 
    name: '某某信息咨询', 
    industry: '企业服务', 
    city: '北京', 
    district: '朝阳区',
    status: CompanyStatus.PENDING, 
    createdAt: 1711641600000,
    updatedAt: 1711641600000
  },
  { 
    id: 'company_003', 
    name: '演示企业', 
    industry: '教育培训', 
    city: '深圳', 
    district: '南山区',
    status: CompanyStatus.BANNED, 
    createdAt: 1710950400000,
    updatedAt: 1710950400000
  },
  { 
    id: 'company_004', 
    name: '科技创新公司', 
    industry: '人工智能', 
    city: '杭州', 
    district: '西湖区',
    status: CompanyStatus.ACTIVE, 
    createdAt: 1711728000000,
    updatedAt: 1711728000000
  },
  { 
    id: 'company_005', 
    name: '网络科技公司', 
    industry: '互联网/软件', 
    city: '广州', 
    district: '天河区',
    status: CompanyStatus.PENDING, 
    createdAt: 1712160000000,
    updatedAt: 1712160000000
  },
])

// 分页数据
const pagination = reactive({
  total: 45,
  currentPage: 1,
  pageSize: 10,
  pageSizes: [10, 20, 50, 100],
})

// 获取状态类型（用于样式）
const getStatusType = (status: CompanyStatus) => {
  switch (status) {
    case CompanyStatus.ACTIVE:
      return 'success'
    case CompanyStatus.PENDING:
      return 'warning'
    case CompanyStatus.BANNED:
      return 'danger'
    default:
      return 'info'
  }
}

// 格式化时间显示
const formatTime = (timestamp: number) => {
  return new Date(timestamp).toLocaleDateString('zh-CN')
}

const onSearch = () => {
  // TODO: 接接口
  console.log('search', query)
  ElMessage.success('查询成功')
}

const onViewDetail = (row: any) => {
  router.push(`/admin/companies/${row.id}`)
}

const onAudit = (row: any) => {
  // 跳转到企业认证审核页
  router.push(`/admin/certification-audit/${row.id}`)
}

const handleBan = async (row: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要封禁企业"${row.name}"吗？`,
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

const handleUnban = async (row: any) => {
  try {
    await ElMessageBox.confirm(
      `确定要解封企业"${row.name}"吗？`,
      '解封确认',
      {
        confirmButtonText: '确认解封',
        cancelButtonText: '取消',
        type: 'success',
      }
    )
    ElMessage.success('企业已解封')
  } catch {
    // 取消操作
  }
}

const handleSizeChange = (val: number) => {
  pagination.pageSize = val
  console.log(`每页 ${val} 条`)
}

const handleCurrentChange = (val: number) => {
  pagination.currentPage = val
  console.log(`当前页：${val}`)
}
</script>

<template>
  <el-card>
    <template #header>
      <div style="display: flex; align-items: center; justify-content: space-between">
        <div style="font-weight: 600">企业管理</div>
        <div style="color: #909399; font-size: 12px">占位页：后续接入企业审核/处置接口</div>
      </div>
    </template>

    <el-form :inline="true" :model="query" style="margin-bottom: 12px">
      <el-form-item label="关键字">
        <el-input v-model="query.keyword" placeholder="企业名称/ID" style="width: 240px" />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="query.status" placeholder="全部" style="width: 160px">
          <el-option label="全部" value="" />
          <el-option label="正常" value="正常" />
          <el-option label="待审核" value="待审核" />
          <el-option label="封禁" value="封禁" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">查询</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="120" />
      <el-table-column prop="name" label="企业名称" min-width="200" />
      <el-table-column prop="industry" label="行业" min-width="160" />
      <el-table-column prop="city" label="城市" width="120" />
      <el-table-column prop="status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)" size="small">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createdAt" label="创建时间" width="160">
        <template #default="{ row }">
          {{ formatTime(row.createdAt) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="280" fixed="right">
        <template #default="{ row }">
          <el-button text type="primary" @click="onViewDetail(row)">详情</el-button>
          <el-button 
            v-if="row.status === '待审核'" 
            text 
            type="success" 
            @click="onAudit(row)"
          >
            审核
          </el-button>
          <el-button 
            v-if="row.status === '正常'" 
            text 
            type="danger" 
            @click="handleBan(row)"
          >
            封禁
          </el-button>
          <el-button 
            v-if="row.status === '封禁'" 
            text 
            type="success" 
            @click="handleUnban(row)"
          >
            解封
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
</template>

