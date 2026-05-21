<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

const query = reactive({
  keyword: '',
  status: '',
})

// 使用统一的求职者数据结构
const tableData = ref([
  { 
    id: 'user_001', 
    name: '张三', 
    phone: '138****0001', 
    city: '上海', 
    status: '正常', 
    createdAt: '2026-03-10',
    totalDeliveries: 15,
    activeJobs: 3
  },
  { 
    id: 'user_002', 
    name: '李四', 
    phone: '139****0002', 
    city: '北京', 
    status: '冻结', 
    createdAt: '2026-03-15',
    totalDeliveries: 8,
    activeJobs: 1
  },
])

const onSearch = () => {
  // TODO: 接求职者列表接口
  console.log('search candidates', query)
}

const onViewDetail = (row: any) => {
  router.push(`/admin/candidates/${row.id}`)
}

const onFreeze = (row: any) => {
  ElMessageBox.confirm(
    `确定要冻结用户「${row.name}」吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    ElMessage.success('已冻结该用户')
  }).catch(() => {})
}

const onBan = (row: any) => {
  ElMessageBox.confirm(
    `确定要封禁用户「${row.name}」吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'danger'
    }
  ).then(() => {
    ElMessage.success('已封禁该用户')
  }).catch(() => {})
}
</script>

<template>
  <el-card>
    <template #header>
      <div style="display: flex; align-items: center; justify-content: space-between">
        <div style="font-weight: 600">求职者管理</div>
        <div style="color: #909399; font-size: 12px">占位页：后续接入账号处置、行为记录等</div>
      </div>
    </template>

    <el-form :inline="true" :model="query" style="margin-bottom: 12px">
      <el-form-item label="关键字">
        <el-input v-model="query.keyword" placeholder="姓名/手机号/ID" style="width: 260px" />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="query.status" placeholder="全部" style="width: 160px">
          <el-option label="全部" value="" />
          <el-option label="正常" value="正常" />
          <el-option label="冻结" value="冻结" />
          <el-option label="封禁" value="封禁" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">查询</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="120" />
      <el-table-column prop="name" label="姓名" width="120" />
      <el-table-column prop="phone" label="手机号" width="160" />
      <el-table-column prop="city" label="城市" width="120" />
      <el-table-column label="投递数" width="100">
        <template #default="{ row }">
          {{ row.totalDeliveries }}
        </template>
      </el-table-column>
      <el-table-column label="在投职位" width="100">
        <template #default="{ row }">
          {{ row.activeJobs }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="120" />
      <el-table-column prop="createdAt" label="注册时间" width="160" />
      <el-table-column label="操作" width="280">
        <template #default="{ row }">
          <el-button text type="primary" @click="onViewDetail(row)">详情</el-button>
          <el-button 
            v-if="row.status === '正常'" 
            text 
            type="warning" 
            @click="onFreeze(row)"
          >
            冻结
          </el-button>
          <el-button 
            v-if="row.status !== '封禁'" 
            text 
            type="danger" 
            @click="onBan(row)"
          >
            封禁
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

