<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { User } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const activePath = computed(() => route.path)

const handleCommand = (command: string) => {
  if (command === 'profile') {
    router.push('/admin/personal-center')
  } else if (command === 'logout') {
    onLogout()
  }
}

const onLogout = () => {
  // 清理 token 和用户信息
  localStorage.removeItem('token')
  localStorage.removeItem('userInfo')
  
  // 跳转到登录页
  router.replace('/login')
}
</script>

<template>
  <el-container style="height: 100vh; background: #f5f7fa">
    <el-aside width="240px" style="background: #001529">
      <div style="height: 64px; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 700">
        Boss 管理端
      </div>

      <el-menu
        :default-active="activePath"
        router
        background-color="#001529"
        text-color="#bfc7d8"
        active-text-color="#ffd04b"
        style="border-right: none"
      >
        <el-menu-item index="/admin/dashboard">数据概览</el-menu-item>

        <el-sub-menu index="base">
          <template #title>供给侧</template>
          <el-menu-item index="/admin/companies">企业管理</el-menu-item>
          <el-menu-item index="/admin/certification-list">
            企业认证审核
            <el-badge :value="3" style="margin-left: 8px" />
          </el-menu-item>
          <el-menu-item index="/admin/positions">职位管理</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="user">
          <template #title>需求侧</template>
          <el-menu-item index="/admin/candidates">求职者管理</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="quality">
          <template #title>沟通质检</template>
          <el-menu-item index="/admin/chat-reviews">会话审核</el-menu-item>
          <el-menu-item index="/admin/report-tasks">举报工单</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="content">
          <template #title>内容运营</template>
          <el-menu-item index="/admin/content-articles">内容文章</el-menu-item>
          <el-menu-item index="/admin/activities">运营活动</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="system">
          <template #title>系统设置</template>
          <el-menu-item index="/admin/roles">角色权限</el-menu-item>
          <el-menu-item index="/admin/operation-logs">操作日志</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header
        style="background: #ffffff; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; border-bottom: 1px solid #eef0f3"
      >
        <div style="font-weight: 600; color: #303133">平台管理端</div>
        <div style="display: flex; align-items: center; gap: 16px">
          <el-dropdown @command="handleCommand">
            <span style="display: flex; align-items: center; gap: 8px; cursor: pointer">
              <el-avatar :size="32" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
                <el-icon><User /></el-icon>
              </el-avatar>
              <span style="font-size: 14px">管理员</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main style="padding: 20px; height: calc(100vh - 60px)">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped></style>

