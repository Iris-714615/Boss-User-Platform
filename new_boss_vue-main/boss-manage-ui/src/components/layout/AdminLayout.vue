<template>
  <el-container class="admin-layout">
    <el-aside width="220px" class="admin-sider">
      <div class="logo">Boss 管理后台</div>
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical-demo"
        router
        unique-opened
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>数据总览</span>
        </el-menu-item>
        <el-sub-menu index="/enterprise">
          <template #title>
            <el-icon><OfficeBuilding /></el-icon>
            <span>企业管理</span>
          </template>
          <el-menu-item index="/enterprise/list">企业列表</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="/job">
          <template #title>
            <el-icon><Briefcase /></el-icon>
            <span>职位管理</span>
          </template>
          <el-menu-item index="/job/list">职位列表</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="/user">
          <template #title>
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </template>
          <el-menu-item index="/user/list">用户列表</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="/im">
          <template #title>
            <el-icon><ChatSquare /></el-icon>
            <span>沟通质检</span>
          </template>
          <el-menu-item index="/im/risk">高风险会话</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="/risk">
          <template #title>
            <el-icon><WarningFilled /></el-icon>
            <span>风控举报</span>
          </template>
          <el-menu-item index="/risk/report">举报工单</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="admin-header">
        <div class="header-left">
          <span class="system-name">Boss 直聘平台管理端</span>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="el-dropdown-link">
              超级管理员
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人中心</el-dropdown-item>
                <el-dropdown-item divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="admin-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  HomeFilled,
  OfficeBuilding,
  Briefcase,
  User,
  ChatSquare,
  WarningFilled
} from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.admin-layout {
  height: 100vh;
}

.admin-sider {
  background-color: #001529;
  color: #fff;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #fff;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.system-name {
  font-size: 16px;
  font-weight: 500;
}

.admin-main {
  background-color: #f5f5f5;
  padding: 16px;
}
</style>
