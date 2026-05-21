<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { PositionStatus } from 'shared-types'
import { positions } from 'shared-types'

const router = useRouter()

const query = reactive({
  keyword: '',
  city: '',
  status: '',
})

// 使用统一的职位数据
const tableData = ref(positions.map(pos => ({
  id: pos.id,
  title: pos.title,
  companyId: pos.companyId,
  companyName: pos.companyName,
  city: pos.city,
  salaryMin: pos.salaryMin,
  salaryMax: pos.salaryMax,
  salaryMonth: pos.salaryMonth,
  status: pos.status,
  views: pos.views,
  communicates: pos.communicates,
  resumes: pos.resumes,
  publishedAt: pos.publishedAt
})))

// 获取状态显示文本
const getStatusText = (status: PositionStatus) => {
  return status
}

// 获取状态类型
const getStatusType = (status: PositionStatus) => {
  switch (status) {
    case PositionStatus.ACTIVE:
      return 'success'
    case PositionStatus.PENDING:
      return 'warning'
    case PositionStatus.CLOSED:
      return 'info'
    case PositionStatus.BANNED:
      return 'danger'
    default:
      return 'info'
  }
}

// 格式化薪资显示
const formatSalary = (min: number, max: number, month: number) => {
  return `${min}-${max}K·${month}薪`
}

const onSearch = () => {
  // TODO: 接职位列表接口
  console.log('search positions', query)
}

const onViewDetail = (row: any) => {
  router.push(`/admin/positions/${row.id}`)
}
</script>

<template>
  <el-card>
    <template #header>
      <div style="display: flex; align-items: center; justify-content: space-between">
        <div style="font-weight: 600">职位管理</div>
        <div style="color: #909399; font-size: 12px">占位页：后续接入职位审核/下架等操作</div>
      </div>
    </template>

    <el-form :inline="true" :model="query" style="margin-bottom: 12px">
      <el-form-item label="职位/企业">
        <el-input v-model="query.keyword" placeholder="职位名称/企业名称" style="width: 240px" />
      </el-form-item>
      <el-form-item label="城市">
        <el-input v-model="query.city" placeholder="城市" style="width: 160px" />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="query.status" placeholder="全部" style="width: 160px">
          <el-option label="全部" value="" />
          <el-option label="已发布" :value="PositionStatus.ACTIVE" />
          <el-option label="待审核" :value="PositionStatus.PENDING" />
          <el-option label="已关闭" :value="PositionStatus.CLOSED" />
          <el-option label="封禁" :value="PositionStatus.BANNED" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">查询</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="120" />
      <el-table-column prop="title" label="职位名称" min-width="180" />
      <el-table-column prop="companyName" label="企业" min-width="160" />
      <el-table-column prop="city" label="城市" width="120" />
      <el-table-column label="薪资" width="140">
        <template #default="{ row }">
          {{ formatSalary(row.salaryMin, row.salaryMax, row.salaryMonth) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)" size="small">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220">
        <template #default="{ row }">
          <el-button text type="primary" @click="onViewDetail(row)">详情</el-button>
          <el-button text type="warning">下架</el-button>
          <el-button text type="danger">封禁</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

