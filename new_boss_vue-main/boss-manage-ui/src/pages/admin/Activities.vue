<script setup lang="ts">
import { reactive, ref } from 'vue'

const query = reactive({
  keyword: '',
  status: '',
})

const tableData = ref([
  { id: 1, name: '春招拉新活动', type: '拉新补贴', status: '进行中', timeRange: '2026-03-01 ~ 2026-04-30' },
  { id: 2, name: '重点行业促招聘', type: '曝光加权', status: '已结束', timeRange: '2025-11-01 ~ 2025-12-31' },
])

const onSearch = () => {
  // TODO: 接活动列表接口
  console.log('search activities', query)
}
</script>

<template>
  <el-card>
    <template #header>
      <div style="display: flex; align-items: center; justify-content: space-between">
        <div style="font-weight: 600">运营活动</div>
        <div style="color: #909399; font-size: 12px">占位页：后续接入活动配置与效果数据</div>
      </div>
    </template>

    <el-form :inline="true" :model="query" style="margin-bottom: 12px">
      <el-form-item label="关键字">
        <el-input v-model="query.keyword" placeholder="活动名称" style="width: 260px" />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="query.status" placeholder="全部" style="width: 160px">
          <el-option label="全部" value="" />
          <el-option label="草稿" value="草稿" />
          <el-option label="未开始" value="未开始" />
          <el-option label="进行中" value="进行中" />
          <el-option label="已结束" value="已结束" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">查询</el-button>
        <el-button type="success">新建活动</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="活动名称" min-width="220" />
      <el-table-column prop="type" label="活动类型" width="160" />
      <el-table-column prop="status" label="状态" width="120" />
      <el-table-column prop="timeRange" label="活动时间" min-width="220" />
      <el-table-column label="操作" width="220">
        <template #default>
          <el-button text type="primary">编辑</el-button>
          <el-button text>效果数据</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

