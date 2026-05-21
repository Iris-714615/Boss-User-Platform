<script setup lang="ts">
import { reactive, ref } from 'vue'

const query = reactive({
  keyword: '',
  status: '',
})

const tableData = ref([
  { id: 1, title: '春招求职指南', channel: '求职攻略', status: '已发布', publishedAt: '2026-03-20' },
  { id: 2, title: '面试常见问题合集', channel: '面试技巧', status: '草稿', publishedAt: '-' },
  { id: 3, title: '如何写出高转化职位 JD', category: '求职指南', status: '已发布', updatedAt: '2026-03-30' },
  { id: 4, title: '面试中的常见坑', category: '面试技巧', status: '草稿', updatedAt: '2026-03-28' },
])

const onSearch = () => {
  // TODO: 接内容文章列表接口
  console.log('search content articles', query)
}
</script>

<template>
  <el-card>
    <template #header>
      <div style="display: flex; align-items: center; justify-content: space-between">
        <div style="font-weight: 600">内容文章</div>
        <div style="color: #909399; font-size: 12px">占位页：后续接入文章编辑、发布、下线</div>
      </div>
    </template>

    <el-form :inline="true" :model="query" style="margin-bottom: 12px">
      <el-form-item label="关键字">
        <el-input v-model="query.keyword" placeholder="标题/分类" style="width: 260px" />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="query.status" placeholder="全部" style="width: 160px">
          <el-option label="全部" value="" />
          <el-option label="草稿" value="草稿" />
          <el-option label="已发布" value="已发布" />
          <el-option label="已下线" value="已下线" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">查询</el-button>
        <el-button type="success">新建文章</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="title" label="标题" min-width="220" />
      <el-table-column prop="channel" label="频道/分类" min-width="160" />
      <el-table-column prop="status" label="状态" width="120" />
      <el-table-column prop="publishedAt" label="发布时间" width="180" />
      <el-table-column label="操作" width="220">
        <template #default>
          <el-button text type="primary">编辑</el-button>
          <el-button text type="warning">下线</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

