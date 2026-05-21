<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const query = reactive({
  keyword: '',
  riskLevel: '',
})

const tableData = ref([
  { id: 1, sessionId: 'S20260331001', company: '示例科技', candidate: '张三', riskLevel: '高', createdAt: '2026-03-31 10:21' },
  { id: 2, sessionId: 'S20260331002', company: '某某信息', candidate: '李四', riskLevel: '中', createdAt: '2026-03-31 11:05' },
])

const onSearch = () => {
  // TODO: 接会话质检列表接口
  console.log('search chat reviews', query)
}

const onViewDetail = (row: any) => {
  router.push(`/admin/session-detail/${row.sessionId}`)
}
</script>

<template>
  <el-card>
    <template #header>
      <div style="display: flex; align-items: center; justify-content: space-between">
        <div style="font-weight: 600">会话审核</div>
        <div style="color: #909399; font-size: 12px">占位页：后续接入高风险会话质检任务</div>
      </div>
    </template>

    <el-form :inline="true" :model="query" style="margin-bottom: 12px">
      <el-form-item label="关键字">
        <el-input v-model="query.keyword" placeholder="企业/求职者/会话ID" style="width: 260px" />
      </el-form-item>
      <el-form-item label="风险等级">
        <el-select v-model="query.riskLevel" placeholder="全部" style="width: 160px">
          <el-option label="全部" value="" />
          <el-option label="高" value="高" />
          <el-option label="中" value="中" />
          <el-option label="低" value="低" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">查询</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="#" width="60" />
      <el-table-column prop="sessionId" label="会话ID" min-width="160" />
      <el-table-column prop="company" label="企业" min-width="160" />
      <el-table-column prop="candidate" label="求职者" width="120" />
      <el-table-column prop="riskLevel" label="风险等级" width="120" />
      <el-table-column prop="createdAt" label="命中时间" width="180" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button text type="primary" @click="onViewDetail(row)">查看详情</el-button>
          <el-button text type="success">标记无风险</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

