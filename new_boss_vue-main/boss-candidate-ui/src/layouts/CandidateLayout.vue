<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  HomeFilled,
  Briefcase,
  ChatDotRound,
  Document,
  User,
  Star,
  Clock,
  Setting,
  Bell,
  Search
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
const router = useRouter()
const route = useRoute()

const activeMenu = computed(() => route.name)

const userInfo = ref({
  name: '',
  avatar: '',
  resumeStatus: '完善中'
})
const getuserInfo = ()=>{
   request.get('user_info').then(res=>{
    userInfo.value = res.data
  })
}
onMounted(()=>{
  userInfo.value.name = localStorage.getItem('candidateInfo').name || ''

  getuserInfo()
})

const menus = [
  { name: 'Home', label: '首页', icon: HomeFilled, path: '/candidate/home' },
  { name: 'JobList', label: '职位', icon: Search, path: '/candidate/jobs' },
  { name: 'Chat', label: '消息', icon: ChatDotRound, path: '/candidate/chat', badge: 3 },
  { name: 'Resume', label: '简历', icon: Document, path: '/candidate/resume' },
  { name: 'Profile', label: '我的', icon: User, path: '/candidate/profile' }
]

const handleCommand = (command) => {
  if (command === 'resume') {
    router.push('/candidate/resume')
  } else if (command === 'profile') {
    router.push('/candidate/profile')
  } else if (command === 'logout') {
    logout()
  }
}

const logout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    localStorage.removeItem('candidateToken')
    localStorage.removeItem('candidateInfo')
    ElMessage.success('已退出登录')
    router.replace('/login')
  } catch {
    // 取消操作
  }
}
</script>

<template>
  <div class="candidate-layout">
    <!-- 底部导航栏 -->
    <div class="bottom-nav">
      <div
        v-for="menu in menus"
        :key="menu.name"
        class="nav-item"
        :class="{ active: activeMenu === menu.name }"
        @click="router.push(menu.path)"
      >
        <div class="nav-content">
          <el-badge :value="menu.badge" :hidden="!menu.badge" class="badge">
            <el-icon :size="24"><component :is="menu.icon" /></el-icon>
          </el-badge>
          <span class="nav-label">{{ menu.label }}</span>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-container">
      <!-- 顶部栏 -->
      <div class="header">
        <div class="header-left">
          <span class="page-title">{{ route.meta.title || '' }}</span>
        </div>
        <div class="header-right">
          <el-badge :value="5" class="bell">
            <el-icon :size="20"><Bell /></el-icon>
          </el-badge>
          <el-dropdown @command="handleCommand">
            <div class="user-info">
              <el-avatar :size="32" :src="userInfo.avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <span class="user-name">{{ userInfo.name }}</span>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="resume">我的简历</el-dropdown-item>
                <el-dropdown-item command="profile">账号设置</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <!-- 内容区 -->
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<style scoped>
.candidate-layout {
  min-height: 100vh;
  background: #f5f7fa;
}

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: white;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.08);
  z-index: 1000;
  padding-bottom: env(safe-area-inset-bottom);
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  padding: 4px 0;
  min-width: 60px;
}

.nav-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.nav-item:hover {
  background: transparent;
}

.nav-item.active {
  color: #0084ff;
}

.nav-item.active .nav-icon {
  transform: scale(1.1);
}

.nav-label {
  font-size: 11px;
  margin-top: 2px;
  letter-spacing: 0.5px;
}

.badge {
  display: flex;
  align-items: center;
  margin-bottom: 2px;
}

.main-container {
  padding-bottom: 60px;
  min-height: 100vh;
}

.header {
  position: sticky;
  top: 0;
  background: white;
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  z-index: 100;
}

.header-left {
  flex: 1;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.bell {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.user-name {
  font-size: 14px;
  color: #606266;
}

.content {
  padding: 16px;
}
</style>
