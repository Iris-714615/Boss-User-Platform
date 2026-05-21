<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  DataAnalysis, 
  Document, 
  UserFilled, 
  ChatDotRound, 
  OfficeBuilding, 
  TrendCharts,
  User,
  ArrowDown,
  Bell,
  Setting,
  Menu,
  HomeFilled
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const route = useRoute()

const activeMenu = computed(() => route.path)
const unreadCount = ref(3)

const userInfo = ref({
  realName: '张经理',
  avatar: '',
  company: '示例科技有限公司',
  role: 'HR 经理'
})

const handleCommand = async (command) => {
  if (command === 'logout') {
    try {
      await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      
      localStorage.removeItem('companyToken')
      localStorage.removeItem('companyUserInfo')
      ElMessage.success('已退出登录')
      router.replace('/login')
    } catch {
      // 取消操作
    }
  } else if (command === 'profile') {
    router.push('/company/account-settings')
  } else if (command === 'company') {
    router.push('/company/manage-company')
  }
}
</script>

<template>
  <el-container class="layout-container">
    <!-- 左侧边栏 -->
    <el-aside width="240px" class="layout-aside">
      <div class="logo-section">
        <div class="logo" @click="router.push('/company/dashboard')">
          <el-icon :size="28" color="#0084ff"><HomeFilled /></el-icon>
          <span class="logo-text">BOSS 直聘</span>
        </div>
        <div class="logo-sub">企业版</div>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        router
        class="side-menu"
        background-color="#001529"
        text-color="#bfc7d8"
        active-text-color="#ffd04b"
      >
        <el-menu-item index="/company/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <span>招聘管理</span>
        </el-menu-item>
        
        <el-menu-item index="/company/positions">
          <el-icon><Document /></el-icon>
          <span>职位管理</span>
        </el-menu-item>
        
        <el-menu-item index="/company/resumes">
          <el-icon><UserFilled /></el-icon>
          <span>简历中心</span>
        </el-menu-item>
        
        <el-menu-item index="/company/chat">
          <el-icon><ChatDotRound /></el-icon>
          <span>消息</span>
          <el-badge v-if="unreadCount > 0" :value="unreadCount" style="margin-left: auto" />
        </el-menu-item>
        
        <el-menu-item index="/company/company-profile">
          <el-icon><OfficeBuilding /></el-icon>
          <span>公司主页</span>
        </el-menu-item>
        
        <el-menu-item index="/company/data">
          <el-icon><TrendCharts /></el-icon>
          <span>数据看板</span>
        </el-menu-item>
        
        <el-menu-item index="/company/team">
          <el-icon><UserFilled /></el-icon>
          <span>团队管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <!-- 右侧主体内容 -->
    <el-container class="main-container">
      <!-- 顶部导航 -->
      <el-header class="layout-header">
        <div class="header-content">
          <div class="header-left">
            <el-button text size="large">
              <el-icon :size="20"><Menu /></el-icon>
            </el-button>
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/company/dashboard' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item v-if="$route.name !== 'Dashboard'">{{ $route.meta.title || $route.name }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          
          <div class="header-right">
            <el-button circle text size="small" class="notification-btn">
              <el-icon><Bell /></el-icon>
              <el-badge :value="2" size="small" />
            </el-button>
            
            <el-dropdown @command="handleCommand" class="user-dropdown">
              <div class="user-info">
                <el-avatar :size="32" :src="userInfo.avatar || ''">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <span class="user-name">{{ userInfo.realName }}</span>
                <el-icon><ArrowDown /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">账号设置</el-dropdown-item>
                  <el-dropdown-item command="company">企业管理</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      
      <!-- 主内容区 -->
      <el-main class="layout-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.layout-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.layout-aside {
  background: #001529;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.logo-section {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #002140;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 1px;
}

.logo-sub {
  position: absolute;
  bottom: 8px;
  right: 20px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.6);
}

.side-menu {
  border-right: none;
  padding-top: 8px;
}

.side-menu .el-menu-item {
  height: 56px;
  line-height: 56px;
  margin: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
}

.side-menu .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.08);
}

.side-menu .el-menu-item.is-active {
  background-color: rgba(0, 132, 255, 0.15);
  color: #0084ff !important;
}

.side-menu .el-icon {
  font-size: 18px;
  margin-right: 12px;
}

.main-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.layout-header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 20px;
  height: 60px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-btn {
  position: relative;
}

.user-dropdown {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.user-name {
  font-size: 14px;
  color: #606266;
}

.layout-main {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

/* 滚动条美化 */
.layout-main::-webkit-scrollbar {
  width: 6px;
}

.layout-main::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.layout-main::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.layout-main::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
