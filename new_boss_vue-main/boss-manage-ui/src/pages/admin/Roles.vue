<script setup lang="ts">
import { reactive, ref } from 'vue'

const query = reactive({
  keyword: '',
})

const tableData = ref([
  { id: 1, name: '超级管理员', description: '拥有全部权限', userCount: 3 },
  { id: 2, name: '运营', description: '负责内容与活动配置', userCount: 8 },
  { id: 3, name: '风控', description: '负责会话质检与举报处理', userCount: 5 },
])

const onSearch = () => {
  // TODO: 接角色列表接口
  console.log('search roles', query)
}
</script>

<template>
  <el-card>
    <template #header>
      <div style="display: flex; align-items: center; justify-content: space-between">
        <div style="font-weight: 600">角色权限</div>
        <div style="color: #909399; font-size: 12px">占位页：后续接入角色-菜单-接口权限配置</div>
      </div>
    </template>

    <el-form :inline="true" :model="query" style="margin-bottom: 12px">
      <el-form-item label="角色名称">
        <el-input v-model="query.keyword" placeholder="角色名称" style="width: 260px" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSearch">查询</el-button>
        <el-button type="success">新建角色</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="角色名称" min-width="160" />
      <el-table-column prop="description" label="描述" min-width="260" />
      <el-table-column prop="userCount" label="关联账号数" width="140" />
      <el-table-column label="操作" width="220">
        <template #default>
          <el-button text type="primary">编辑权限</el-button>
          <el-button text>关联账号</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

