<template>
  <div class="hr-layout">
    <!-- 顶部栏 -->
    <header class="header">
      <div class="logo">
        <span class="logo-icon">HR</span>
        <span class="logo-text">智能招聘后台</span>
      </div>
      <div class="header-actions">
        <span class="badge">版本 Beta</span>
        <router-link to="/hr/post" class="primary-btn" style="text-decoration: none; color: inherit;">
          新建职位
        </router-link>
        <button class="ghost-btn logout-btn" @click="handleLogout">退出</button>
        <div class="user-label">{{ displayName }}</div>
        <div class="avatar">😊</div>
      </div>
    </header>

    <div class="body">
      <!-- 侧边菜单 -->
      <aside class="sidebar">
        <div class="menu-title">功能菜单</div>
        <ul class="menu-list">
          <router-link
            to="/hr/home"
            class="menu-item menu-link"
            :class="{ active: $route.path === '/hr/home' }"
          >
            <span class="icon">🏠</span>
            <span>工作台</span>
            <span class="tag">首页</span>
          </router-link>
          <router-link
            to="/hr/post"
            class="menu-item menu-link"
            :class="{ active: $route.path === '/hr/post' }"
          >
            <span class="icon">📢</span>
            <span>职位发布</span>
            <span class="tag">招聘</span>
          </router-link>
          <router-link
            to="/hr/candidates"
            class="menu-item menu-link"
            :class="{ active: $route.path === '/hr/candidates' }"
          >
            <span class="icon">👥</span>
            <span>候选人管理</span>
            <span class="tag blue">人才库</span>
          </router-link>
          <router-link
            to="/hr/agent"
            class="menu-item menu-link"
            :class="{ active: $route.path === '/hr/agent' }"
          >
            <span class="icon">🤖</span>
            <span>智能招聘助手</span>
            <span class="tag green">AI</span>
          </router-link>
          <router-link
            to="/hr/degree"
            class="menu-item menu-link"
            :class="{ active: $route.path === '/hr/degree' }"
          >
            <span class="icon">🎓</span>
            <span>学历验证</span>
            <span class="tag purple">校验</span>
          </router-link>
          <router-link
            to="/hr/assistant"
            class="menu-item menu-link"
            :class="{ active: $route.path === '/hr/assistant' }"
          >
            <span class="icon">🧾</span>
            <span>人事助手</span>
            <span class="tag orange">HR</span>
          </router-link>
        </ul>

        <div class="quick-actions">
          <div class="qa-title">快捷入口</div>
          <button class="ghost-btn">导入候选人</button>
          <button class="ghost-btn">批量邀约</button>
          <button class="ghost-btn">下载简历模板</button>
        </div>
      </aside>

      <!-- 主体内容 -->
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { ref } from "vue";

const router = useRouter();
const displayName = ref("HR");

const loadDisplayName = () => {
  const username = localStorage.getItem("username") || "HR";
  displayName.value = `HR-${username}`;
};

loadDisplayName();

const handleLogout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("refresh");
  localStorage.removeItem("username");
  localStorage.removeItem("userid");
  localStorage.removeItem("role");
  ElMessage.success("已退出登录");
  router.push("/login");
};
</script>

<style scoped>
:root {
  color-scheme: light;
}

.hr-layout {
  height: 100vh;
  overflow: hidden;
  background: #f5f7fb;
  display: flex;
  flex-direction: column;
}

.header {
  height: 64px;
  padding: 0 20px;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  color: #111827;
}

.logo-icon {
  background: linear-gradient(135deg, #00bebd, #00a6d6);
  color: #fff;
  padding: 8px 10px;
  border-radius: 10px;
  font-size: 14px;
}

.logo-text {
  font-size: 16px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-label {
  font-size: 14px;
  color: #374151;
  font-weight: 600;
}

.badge {
  background: #e0f7f7;
  color: #008c8c;
  padding: 6px 10px;
  border-radius: 12px;
  font-size: 12px;
}

.primary-btn {
  background: #00bebd;
  color: #fff;
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s;
}

.link-btn {
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.primary-btn:hover {
  background: #00a6a5;
}

.logout-btn {
  border: 1px solid #e5e7eb;
  background: #fff;
  color: #374151;
}

.logout-btn:hover {
  border-color: #00a6d6;
  color: #00a6d6;
  background: #f0f9ff;
}

.text-btn {
  background: transparent;
  border: none;
  color: #00a6d6;
  cursor: pointer;
  font-weight: 600;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #eef2f7;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.body {
  display: flex;
  flex: 1;
  min-height: 0;
}

.sidebar {
  width: 240px;
  background: #fff;
  border-right: 1px solid #e5e7eb;
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: calc(100vh - 64px);
  overflow-y: auto;
  box-sizing: border-box;
}

.menu-title {
  font-weight: 700;
  color: #111827;
  margin-bottom: 6px;
}

.menu-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  cursor: pointer;
  color: #374151;
  transition: all 0.2s;
  border: 1px solid transparent;
}

.menu-item .icon {
  font-size: 16px;
}

.menu-item .tag {
  margin-left: auto;
  font-size: 12px;
  background: #eef2f7;
  color: #4b5563;
  padding: 2px 8px;
  border-radius: 999px;
}

.menu-item .tag.blue {
  background: #e6f4ff;
  color: #1d4ed8;
}

.menu-item .tag.green {
  background: #e6fbf3;
  color: #0f9d58;
}

.menu-item .tag.purple {
  background: #f3e8ff;
  color: #7c3aed;
}

.menu-item .tag.orange {
  background: #fff2e6;
  color: #d97706;
}

.menu-link {
  text-decoration: none;
}

.menu-item:hover {
  background: #f5f7fb;
  border-color: #dbeafe;
}

.menu-item.active {
  background: linear-gradient(135deg, #e0f7f7, #f5f7fb);
  border-color: #00bebd;
  color: #0f172a;
  box-shadow: 0 6px 12px rgba(0, 190, 189, 0.08);
}

.quick-actions {
  border-top: 1px solid #e5e7eb;
  padding-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.qa-title {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 6px;
}

.ghost-btn {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  color: #374151;
  padding: 8px 10px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
  text-align: left;
  transition: all 0.2s;
}

.ghost-btn:hover {
  border-color: #00a6d6;
  color: #00a6d6;
  background: #f0f9ff;
}

.content {
  flex: 1;
  padding: 20px 24px 28px;
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  gap: 18px;
  height: calc(100vh - 64px);
  box-sizing: border-box;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 14px;
  border: 1px solid #eef0f4;
  box-shadow: 0 4px 8px rgba(17, 24, 39, 0.03);
}

.stat-title {
  color: #6b7280;
  font-size: 13px;
}

.stat-value {
  font-size: 26px;
  font-weight: 700;
  color: #0f172a;
  margin: 6px 0;
}

.stat-desc {
  font-size: 12px;
  color: #6b7280;
}

.stat-desc.up {
  color: #0ea5e9;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 14px;
}

.feature-card {
  background: #fff;
  border-radius: 14px;
  padding: 16px;
  border: 1px solid #eef0f4;
  box-shadow: 0 8px 16px rgba(17, 24, 39, 0.04);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-head {
  display: flex;
  gap: 12px;
  align-items: center;
}

.icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: #f0f9ff;
  display: grid;
  place-items: center;
  font-size: 18px;
}

.card-title {
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
}

.card-sub {
  font-size: 13px;
  color: #6b7280;
}

.card-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #374151;
  font-size: 13px;
}

.card-actions {
  display: flex;
  gap: 10px;
}

@media (max-width: 960px) {
  .sidebar {
    width: 200px;
  }
}

@media (max-width: 768px) {
  .body {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 10px;
  }

  .menu-list {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .menu-item {
    flex: 1 1 45%;
  }
}
</style>