<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Filter, Download, User } from '@element-plus/icons-vue'
import { DeliveryStatus, formatTime } from 'shared-types'

const router = useRouter()

const query = reactive({
  keyword: '',
  position: '',
  education: '',
  experience: '',
  status: '',
  dateRange: ''
})

// 使用统一的简历数据结构
const tableData = ref([
  { 
    id: 'candidate_001', 
    userId: 'user_001',
    name: '张三', 
    avatar: '',
    age: 28, 
    education: '本科', 
    experience: '4 年', 
    expectedPosition: '高级前端工程师', 
    expectedCity: '上海',
    expectedSalaryMin: 25,  // ✅ 分字段存储
    expectedSalaryMax: 35,
    currentCompany: '某互联网公司',
    status: DeliveryStatus.APPLIED,
    deliveryTime: 1711900800000,
    matchRate: 95
  },
  { 
    id: 'candidate_002', 
    userId: 'user_002',
    name: '李四', 
    avatar: '',
    age: 26, 
    education: '本科', 
    experience: '3 年', 
    expectedPosition: '前端开发工程师', 
    expectedCity: '北京',
    expectedSalaryMin: 18,
    expectedSalaryMax: 25,
    currentCompany: '某科技公司',
    status: DeliveryStatus.VIEWED,
    deliveryTime: 1711897200000,
    matchRate: 92
  },
  { 
    id: 'candidate_003', 
    userId: 'user_003',
    name: '王五', 
    avatar: '',
    age: 30, 
    education: '硕士', 
    experience: '5 年', 
    expectedPosition: '技术专家', 
    expectedCity: '深圳',
    expectedSalaryMin: 35,
    expectedSalaryMax: 45,
    currentCompany: '某网络公司',
    status: DeliveryStatus.INTERESTED,
    deliveryTime: 1711814400000,
    matchRate: 88
  },
  { 
    id: 'candidate_004', 
    userId: 'user_004',
    name: '赵六', 
    avatar: '',
    age: 25, 
    education: '大专', 
    experience: '2 年', 
    expectedPosition: 'Web 开发工程师', 
    expectedCity: '杭州',
    expectedSalaryMin: 15,
    expectedSalaryMax: 20,
    currentCompany: '某创业公司',
    status: DeliveryStatus.INTERVIEW,
    deliveryTime: 1711807200000,
    matchRate: 85
  },
  { 
    id: 'candidate_005', 
    userId: 'user_005',
    name: '钱七', 
    avatar: '',
    age: 29, 
    education: '本科', 
    experience: '4 年', 
    expectedPosition: '前端架构师', 
    expectedCity: '广州',
    expectedSalaryMin: 30,
    expectedSalaryMax: 40,
    currentCompany: '某大型企业',
    status: DeliveryStatus.NOT_INTERESTED,
    deliveryTime: 1711720800000,
    matchRate: 78
  }
])

const pagination = reactive({
  total: 156,
  currentPage: 1,
  pageSize: 10,
  pageSizes: [10, 20, 50, 100]
})

const onSearch = () => {
  ElMessage.success('查询成功')
}

const onViewDetail = (row) => {
  router.push(`/company/resumes/${row.id}`)
}

const onChat = (row) => {
  router.push(`/company/chat?userId=${row.id}`)
}

const onDownload = (row) => {
  ElMessage.success('简历下载功能开发中')
}

const getStatusType = (status) => {
  const typeMap = {
    [DeliveryStatus.APPLIED]: 'success',
    [DeliveryStatus.VIEWED]: 'primary',
    [DeliveryStatus.INTERESTED]: 'warning',
    [DeliveryStatus.INTERVIEW]: '',
    [DeliveryStatus.NOT_INTERESTED]: 'info'
  }
  return typeMap[status] || 'info'
}

const handleSizeChange = (val) => {
  pagination.pageSize = val
}

const handleCurrentChange = (val) => {
  pagination.currentPage = val
}
</script>

<template>
  <div class="resume-list-container">
    <!-- 头部 -->
    <el-card shadow="never" class="header-card">
      <div class="header-content">
        <div class="header-left">
          <h3>简历中心</h3>
          <p class="header-desc">管理收到的所有简历</p>
        </div>
        <div class="header-right">
          <el-button @click="ElMessage.success('批量下载功能开发中')">
            <el-icon><Download /></el-icon>
            批量下载
          </el-button>
          <el-button @click="ElMessage.success('人才库功能开发中')">
            <el-icon><User /></el-icon>
            人才库
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
            placeholder="姓名/职位/公司" 
            style="width: 240px"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="期望职位">
          <el-select v-model="query.position" placeholder="全部" style="width: 180px" clearable>
            <el-option label="前端工程师" value="前端工程师" />
            <el-option label="产品经理" value="产品经理" />
            <el-option label="Java 开发" value="Java 开发" />
          </el-select>
        </el-form-item>
        <el-form-item label="学历">
          <el-select v-model="query.education" placeholder="全部" style="width: 140px" clearable>
            <el-option label="大专" value="大专" />
            <el-option label="本科" value="本科" />
            <el-option label="硕士" value="硕士" />
            <el-option label="博士" value="博士" />
          </el-select>
        </el-form-item>
        <el-form-item label="经验">
          <el-select v-model="query.experience" placeholder="全部" style="width: 140px" clearable>
            <el-option label="应届生" value="应届生" />
            <el-option label="1-3 年" value="1-3 年" />
            <el-option label="3-5 年" value="3-5 年" />
            <el-option label="5 年以上" value="5 年以上" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="query.status" placeholder="全部" style="width: 140px" clearable>
            <el-option :label="DeliveryStatus.APPLIED" :value="DeliveryStatus.APPLIED" />
            <el-option :label="DeliveryStatus.VIEWED" :value="DeliveryStatus.VIEWED" />
            <el-option :label="DeliveryStatus.INTERESTED" :value="DeliveryStatus.INTERESTED" />
            <el-option :label="DeliveryStatus.INTERVIEW" :value="DeliveryStatus.INTERVIEW" />
            <el-option :label="DeliveryStatus.NOT_INTERESTED" :value="DeliveryStatus.NOT_INTERESTED" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSearch">查询</el-button>
          <el-button @click="query = { keyword: '', position: '', education: '', experience: '', status: '', dateRange: '' }">
            <el-icon><Filter /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 简历列表 -->
    <el-card shadow="never" class="table-card">
      <el-table :data="tableData" style="width: 100%" v-loading="false">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column label="候选人" min-width="180">
          <template #default="{ row }">
            <div class="candidate-info" @click="onViewDetail(row)">
              <el-avatar :size="40" :src="row.avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="info-detail">
                <div class="name">{{ row.name }}</div>
                <div class="basic">{{ row.age }}岁 · {{ row.education }} · {{ row.experience }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="expectedPosition" label="期望职位" min-width="160" />
        <el-table-column prop="expectedCity" label="期望城市" width="120" />
        <el-table-column label="期望薪资" width="120">
          <template #default="{ row }">
            {{ row.expectedSalaryMin }}-{{ row.expectedSalaryMax }}K
          </template>
        </el-table-column>
        <el-table-column prop="currentCompany" label="当前公司" min-width="160" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="投递时间" width="160">
          <template #default="{ row }">
            {{ formatTime(row.deliveryTime) }}
          </template>
        </el-table-column>
        <el-table-column label="匹配度" width="100">
          <template #default="{ row }">
            <el-progress 
              :percentage="row.matchRate" 
              :color="row.matchRate >= 90 ? '#67C23A' : row.matchRate >= 80 ? '#E6A23C' : '#F56C6C'"
              :stroke-width="16"
              :show-text="false"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button text type="primary" size="small" @click="onViewDetail(row)">详情</el-button>
            <el-button text type="primary" size="small" @click="onChat(row)">沟通</el-button>
            <el-button text type="primary" size="small" @click="onDownload(row)">下载</el-button>
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
.resume-list-container {
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

.table-card {
  margin-bottom: 16px;
}

.candidate-info {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.candidate-info:hover {
  opacity: 0.8;
}

.info-detail {
  flex: 1;
}

.name {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.basic {
  font-size: 12px;
  color: #909399;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
