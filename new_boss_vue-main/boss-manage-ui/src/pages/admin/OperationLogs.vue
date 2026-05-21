<script setup lang="ts">
import { reactive, ref } from 'vue'

const query = reactive({
  operator: '',
  target: '',
})

const tableData = ref([
  { id: 1, operator: 'admin01', action: '封禁企业', target: '示例科技有限公司', createdAt: '2026-03-31 10:30' },
  { id: 2, operator: 'risk02', action: '处理举报', target: '举报 R20260331002', createdAt: '2026-03-31 11:05' },
])

const onSearch = () => {
  // TODO: 接操作日志列表接口
  console.log('search operation logs', query)
}
</script>

<template>
  <el-card>
    <template #header>
      <div style="display: flex; align-items: center; justify-content: space-between">
        <div style="font-weight: 600">操作日志</div>
        <div style="color: #909399; font-size: 12px">占位页：后续接入完整的审计与检索能力</div>
      </div>
    </template>

    <el-form :inline="true" :model="query" style="margin-bottom: 12px">
      <el-form-item label="操作人">
        <el-input v-model="query.operator" placeholder="账号" style="width: 200px" />
      </el-form-item>
      <el-form-item label="对象">
        <el-input v-model="query.target" placeholder="企业/职位/举报ID等" style="width: 260px" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">查询</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="operator" label="操作人" width="140" />
      <el-table-column prop="action" label="操作行为" min-width="180" />
      <el-table-column prop="target" label="对象" min-width="240" />
      <el-table-column prop="createdAt" label="时间" width="200" />
    </el-table>
  </el-card>
</template>

