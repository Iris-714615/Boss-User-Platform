<script setup lang="ts">
import { reactive, ref } from 'vue'

const query = reactive({
  keyword: '',
  status: '',
})

const tableData = ref([
  { id: 1, reportId: 'R20260331001', type: '虚假职位', target: '职位：高级前端工程师', status: '待处理', createdAt: '2026-03-31 09:30' },
  { id: 2, reportId: 'R20260331002', type: '骚扰聊天', target: '企业：某某信息', status: '处理中', createdAt: '2026-03-31 10:02' },
])

const onSearch = () => {
  // TODO: 接举报工单列表接口
  console.log('search report tasks', query)
}
</script>

<template>
  <el-card>
    <template #header>
      <div style="display: flex; align-items: center; justify-content: space-between">
        <div style="font-weight: 600">举报工单</div>
        <div style="color: #909399; font-size: 12px">占位页：后续接入举报处理流程</div>
      </div>
    </template>

    <el-form :inline="true" :model="query" style="margin-bottom: 12px">
      <el-form-item label="关键字">
        <el-input v-model="query.keyword" placeholder="举报ID/对象" style="width: 260px" />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="query.status" placeholder="全部" style="width: 160px">
          <el-option label="全部" value="" />
          <el-option label="待处理" value="待处理" />
          <el-option label="处理中" value="处理中" />
          <el-option label="已处理" value="已处理" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">查询</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="#" width="60" />
      <el-table-column prop="reportId" label="举报ID" min-width="140" />
      <el-table-column prop="type" label="举报类型" min-width="140" />
      <el-table-column prop="target" label="举报对象" min-width="220" />
      <el-table-column prop="status" label="状态" width="120" />
      <el-table-column prop="createdAt" label="创建时间" width="180" />
      <el-table-column label="操作" width="200">
        <template #default>
          <el-button text type="primary">处理</el-button>
          <el-button text>详情</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

