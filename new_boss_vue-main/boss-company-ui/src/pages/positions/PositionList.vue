<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete, DocumentCopy, ChatDotRound } from '@element-plus/icons-vue'
import { PositionStatus, formatSalary } from 'shared-types'

const router = useRouter()

const query = reactive({
  keyword: '',
  status: '',
  city: '',
  page: 1,
  pageSize: 10
})

// 使用统一的职位数据结构
const tableData = ref([
  { 
    id: 'position_001', 
    title: '高级前端工程师', 
    department: '技术部', 
    city: '上海', 
    salaryMin: 25,           // ✅ 分字段存储
    salaryMax: 35,
    salaryMonth: 14,
    experience: '3-5 年', 
    education: '本科',
    status: PositionStatus.ACTIVE,  // ✅ 使用枚举
    views: 1256,
    communicates: 89,
    resumes: 34,
    publishDate: 1710460800000  // ✅ 时间戳
  },
  { 
    id: 'position_002', 
    title: '产品经理', 
    department: '产品部', 
    city: '北京', 
    salaryMin: 20,
    salaryMax: 30,
    salaryMonth: 14,
    experience: '3-5 年', 
    education: '本科',
    status: PositionStatus.ACTIVE,
    views: 982,
    communicates: 67,
    resumes: 28,
    publishDate: 1710720000000
  },
  { 
    id: 'position_003', 
    title: 'Java 开发工程师', 
    department: '技术部', 
    city: '深圳', 
    salaryMin: 18,
    salaryMax: 28,
    salaryMonth: 14,
    experience: '1-3 年', 
    education: '本科',
    status: PositionStatus.ACTIVE,
    views: 856,
    communicates: 52,
    resumes: 19,
    publishDate: 1710892800000
  },
  { 
    id: 'position_004', 
    title: 'UI 设计师', 
    department: '设计部', 
    city: '杭州', 
    salaryMin: 15,
    salaryMax: 22,
    salaryMonth: 13,
    experience: '1-3 年', 
    education: '大专',
    status: PositionStatus.CLOSED,  // ✅ 已关闭
    views: 634,
    communicates: 38,
    resumes: 15,
    publishDate: 1710028800000
  },
  { 
    id: 'position_005', 
    title: '测试工程师', 
    department: '技术部', 
    city: '广州', 
    salaryMin: 12,
    salaryMax: 18,
    salaryMonth: 13,
    experience: '1-3 年', 
    education: '本科',
    status: PositionStatus.CLOSED,
    views: 423,
    communicates: 25,
    resumes: 12,
    publishDate: 1709251200000
  }
])

const pagination = reactive({
  total: 45,
  currentPage: 1,
  pageSize: 10,
  pageSizes: [10, 20, 50, 100]
})

const onSearch = () => {
  ElMessage.success('查询成功')
  console.log('search', query)
}

const onViewDetail = (row) => {
  router.push(`/company/positions/${row.id}`)
}

const onEdit = (row) => {
  router.push(`/company/positions/edit/${row.id}`)
}

const onChat = (row) => {
  router.push('/company/chat')
}

const onResume = (row) => {
  router.push('/company/resumes')
}

const handleStatusChange = async (row) => {
  try {
    const action = row.status === '招聘中' ? '暂停' : '开启'
    await ElMessageBox.confirm(
      `确定要${action}该职位的招聘吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    row.status = row.status === '招聘中' ? '暂停招聘' : '招聘中'
    ElMessage.success(`操作成功`)
  } catch {
    // 取消操作
  }
}

const handleClose = async (row) => {
  try {
    await ElMessageBox.confirm(
      '确定要关闭该职位吗？关闭后将无法继续接收简历。',
      '关闭职位',
      {
        confirmButtonText: '确定关闭',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    row.status = '已关闭'
    ElMessage.success('职位已关闭')
  } catch {
    // 取消操作
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该职位吗？此操作不可恢复。',
      '删除职位',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error'
      }
    )
    
    const index = tableData.value.findIndex(item => item.id === row.id)
    if (index !== -1) {
      tableData.value.splice(index, 1)
    }
    ElMessage.success('职位已删除')
  } catch {
    // 取消操作
  }
}

const handleSizeChange = (val) => {
  pagination.pageSize = val
}

const handleCurrentChange = (val) => {
  pagination.currentPage = val
}

const getStatusType = (status) => {
  if (status === PositionStatus.ACTIVE) return 'success'
  if (status === PositionStatus.PENDING) return 'warning'
  if (status === PositionStatus.CLOSED) return 'info'
  return 'info'
}
</script>

<template>
  <div class="position-list-container">
    <!-- 头部操作区 -->
    <el-card shadow="never" class="header-card">
      <div class="header-content">
        <div class="header-left">
          <h3>职位管理</h3>
          <p class="header-desc">管理和优化您的招聘职位</p>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="router.push('/company/positions/publish')">
            <el-icon><Plus /></el-icon>
            发布新职位
          </el-button>
          <el-button @click="router.push('/company/positions/batch-import')">
            <el-icon><DocumentCopy /></el-icon>
            批量导入
          </el-button>
        </div>
      </div>
    </el-card>
    
    <!-- 筛选区 -->
    <el-card shadow="never" class="filter-card">
      <el-form :inline="true" :model="query" class="filter-form">
        <el-form-item label="关键字">
          <el-input 
            v-model="query.keyword" 
            placeholder="职位名称/部门" 
            style="width: 240px"
            clearable
          />
        </el-form-item>
        <el-form-item label="招聘状态">
          <el-select v-model="query.status" placeholder="全部" style="width: 160px" clearable>
            <el-option label="招聘中" value="招聘中" />
            <el-option label="暂停招聘" value="暂停招聘" />
            <el-option label="已关闭" value="已关闭" />
          </el-select>
        </el-form-item>
        <el-form-item label="工作城市">
          <el-select v-model="query.city" placeholder="全部" style="width: 160px" clearable>
            <el-option label="北京" value="北京" />
            <el-option label="上海" value="上海" />
            <el-option label="深圳" value="深圳" />
            <el-option label="杭州" value="杭州" />
            <el-option label="广州" value="广州" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSearch">查询</el-button>
          <el-button @click="query = { keyword: '', status: '', city: '', page: 1, pageSize: 10 }">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 职位列表 -->
    <el-card shadow="never" class="table-card">
      <el-table :data="tableData" style="width: 100%" v-loading="false">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="title" label="职位名称" min-width="180">
          <template #default="{ row }">
            <div class="position-title" @click="onViewDetail(row)">
              {{ row.title }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="department" label="部门" width="120" />
        <el-table-column prop="city" label="城市" width="100" />
        <el-table-column label="薪资" width="160">
          <template #default="{ row }">
            {{ formatSalary(row.salaryMin, row.salaryMax, row.salaryMonth) }}
          </template>
        </el-table-column>
        <el-table-column prop="experience" label="经验" width="100" />
        <el-table-column prop="education" label="学历" width="100" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="效果" width="200">
          <template #default="{ row }">
            <div class="stats">
              <span class="stat-item">查看 {{ row.views }}</span>
              <span class="stat-item">沟通 {{ row.communicates }}</span>
              <span class="stat-item">简历 {{ row.resumes }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="320" fixed="right">
          <template #default="{ row }">
            <el-button text type="primary" size="small" @click="onViewDetail(row)">详情</el-button>
            <el-button text type="primary" size="small" @click="onEdit(row)">编辑</el-button>
            <el-button text type="success" size="small" @click="onResume(row)">简历</el-button>
            <el-button text type="primary" size="small" @click="onChat(row)">沟通</el-button>
            <el-dropdown trigger="click" size="small">
              <el-button text size="small">
                更多<el-icon class="el-icon--right"><arrow-down /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="handleStatusChange(row)">
                    {{ row.status === PositionStatus.ACTIVE ? '暂停招聘' : '开启招聘' }}
                  </el-dropdown-item>
                  <el-dropdown-item @click="handleClose(row)" divided>关闭职位</el-dropdown-item>
                  <el-dropdown-item @click="handleDelete(row)" divided>删除职位</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
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
.position-list-container {
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

.header-right {
  display: flex;
  gap: 12px;
}

.filter-card {
  margin-bottom: 16px;
}

.filter-form {
  margin-bottom: 0;
}

.table-card {
  margin-bottom: 16px;
}

.position-title {
  color: #0084ff;
  cursor: pointer;
  font-weight: 500;
}

.position-title:hover {
  text-decoration: underline;
}

.stats {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #606266;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
