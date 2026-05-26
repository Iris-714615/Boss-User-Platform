<template>
  <div class="home-container">
    <!-- 左侧菜单 -->
    <aside class="sidebar">
      <div class="logo">
        <h2>RBAC 管理系统</h2>
      </div>
      <el-menu :default-active="activeMenu" class="el-menu-vertical-demo" @select="handleMenuSelect" :unique-opened="true">
        <template v-for="item in menulist" :key="item.id">
          <el-sub-menu v-if="item.son && item.son.length > 0" :index="String(item.id)">
            <template #title>
              <span>{{ item.name }}</span>
            </template>
            <el-menu-item v-for="son in item.son" :key="son.id" :index="son.url">
              {{ son.name }}
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item v-else :index="item.url">
            <span>{{ item.name }}</span>
          </el-menu-item>
        </template>
      </el-menu>

      <div class="logout" @click="handleLogout">
        <span>退出登录</span>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <header class="header">
        <span>欢迎, {{ name }}</span>
      </header>
      <div class="content-wrapper">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const activeMenu = ref('')
const name = ref('')
const menulist = ref([])

onMounted(() => {
  name.value = localStorage.getItem('name') || '管理员'
  activeMenu.value = route.path
  menulist.value = JSON.parse(localStorage.getItem('menulist') || '[]')
})

const handleMenuSelect = (index) => {
  activeMenu.value = index
  router.push(index)
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('name')
  ElMessage.success('退出成功')
  router.push('/login')
}
</script>

<style scoped>
.home-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 200px;
  background: #2a3f5f;
  color: #333;
  display: flex;
  flex-direction: column;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #1a2e4a;
}

.logo h2 {
  margin: 0;
  font-size: 16px;
  color: #fff;
}

.el-menu-vertical-demo {
  flex: 1;
  border-right: none;
  background: #2a3f5f;
}

/* 菜单项样式 */
.el-menu-vertical-demo .el-menu-item {
  color: #fff !important;
  background: #2a3f5f !important;
}

.el-menu-vertical-demo .el-menu-item:hover {
  background: #1a2e4a !important;
}

.el-menu-vertical-demo .el-menu-item.is-active {
  background: #1a2e4a !important;
}

/* 子菜单标题样式 */
.el-menu-vertical-demo .el-sub-menu__title {
  color: #fff !important;
  background: #2a3f5f !important;
}

.el-menu-vertical-demo .el-sub-menu__title:hover {
  background: #1a2e4a !important;
}

/* 子菜单选项样式 */
.el-menu-vertical-demo .el-sub-menu .el-menu-item {
  padding-left: 45px !important;
}

.logout {
  padding: 15px 20px;
  cursor: pointer;
  border-top: 1px solid #1a2e4a;
  color: #fff;
}

.logout:hover {
  background: #1a2e4a;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #f5f5f5;
}

.header {
  padding: 15px 20px;
  background: #fff;
  border-bottom: 1px solid #eee;
  text-align: right;
}

.header span {
  color: #666;
}

.content-wrapper {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

/* 确保路由视图中的内容有正确的颜色 */
.content-wrapper :deep(*) {
  color: #333;
}

.content-wrapper :deep(.el-table) {
  color: #333;
}

.content-wrapper :deep(.el-button) {
  color: #333;
}

.content-wrapper :deep(.el-input) {
  color: #333;
}

.content-wrapper :deep(.el-form-item__label) {
  color: #666;
}
</style>
