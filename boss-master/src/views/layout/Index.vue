<template>
  <el-container>
    <!--1.顶部导航栏  -->
    <el-header>
      <div class="boss-header">
        <div class="header-container">
          <div class="logo">
            <router-link to="/home" @click="refreshHome"
              >BOSS直聘</router-link
            >
          </div>
          <!-- 新城市选择弹窗按钮 -->
          <div class="city-selector-btn" @click="showSelector = true">
            <i class="location-icon"></i>
            <span class="current-city">{{ currentCity }}</span>
            <span class="switch-text">[切换]</span>
          </div>
          <CitySelector v-model:visible="showSelector" @select="onSelectCity" />

          <nav class="main-nav">
            <ul>
              <li>
                <router-link to="/home" active-class="active" exact
                  >首页</router-link
                >
              </li>
              <li>
                <router-link to="/job" active-class="active">职位</router-link>
              </li>
              <li>
                <router-link to="/company" active-class="active"
                  >公司</router-link
                >
              </li>
              <li class="combo-item">
                <router-link to="/school" active-class="active"
                  >校园</router-link
                >
                <span class="divider">/</span>
                <router-link to="/overseas" active-class="active"
                  >海归</router-link
                >
              </li>
              <li>
                <router-link to="/app" active-class="active">APP</router-link>
              </li>
              <li>
                <router-link to="/discover" active-class="active"
                  >社区</router-link
                >
              </li>
              <li>
                <router-link to="/overseas" active-class="active"
                  >海外</router-link
                >
              </li>
              <li>
                <router-link to="/accessible" active-class="active"
                  >无障碍专区</router-link
                >
              </li>
              <li>
                <router-link to="/qa" active-class="active"
                  >问答系统</router-link
                >
              </li>
            </ul>
          </nav>
          <div class="user-area">
            <!-- 消息按钮 -->
            <div
              class="message-box"
              @mouseenter="showMessageTip = true"
              @mouseleave="showMessageTip = false"
            >
              <router-link to="/messages" class="message-btn">
                <i class="message-icon"></i>
                <span class="message-count" v-if="unreadCount > 0">{{
                  unreadCount
                }}</span>
              </router-link>
              <div class="message-tip" v-show="showMessageTip">
                <div class="tip-arrow"></div>
                <div class="tip-content">您有{{ unreadCount }}条未读消息</div>
              </div>
            </div>
            <!-- 简历按钮 -->
            <div
              class="resume-box"
              @mouseenter="showResumeMenu = true"
              @mouseleave="showResumeMenu = false"
            >
              <router-link to="/resume" class="resume-btn">简历</router-link>
              <div class="resume-menu" v-show="showResumeMenu">
                <router-link to="/resume/edit" class="menu-item">
                  <i class="resume-icon edit-icon"></i>
                  <span>在线编辑简历</span>
                </router-link>
                <router-link to="/resume/upload" class="menu-item">
                  <i class="resume-icon upload-icon"></i>
                  <span>简历分析</span>
                </router-link>
                <router-link to="/resume/template" class="menu-item">
                  <i class="resume-icon template-icon"></i>
                  <span>简历模板</span>
                </router-link>
                <router-link to="/resume/interviewSetup" class="menu-item">
                  <i class="resume-icon template-icon"></i>
                  <span>AI模拟面试</span>
                </router-link>
                <router-link to="/resumeJob" class="menu-item">
                  <i class="resume-icon edit-icon"></i>
                  <span>智能岗位推荐</span>
                </router-link>
                <router-link to="/qa" class="menu-item">
                  <i class="resume-icon qa-icon"></i>
                  <span>智能问答</span>
                </router-link>
              </div>
            </div>
            <!-- 个人中心 -->
            <div
              class="user-avatar"
              @mouseenter="showUserMenu = true"
              @mouseleave="onUserMenuLeave"
            >
              <span class="user-name">{{ displayName }}</span>
              <div
                class="user-menu"
                v-show="showUserMenu"
                @mouseenter="clearUserMenuTimer"
                @mouseleave="onUserMenuLeave"
              >
                <router-link to="/user/profile" class="menu-item">
                  <i class="user-icon profile-icon"></i>
                  <span>个人中心</span>
                </router-link>
                <router-link to="/verify-process" class="menu-item">
                  <i class="user-icon verify-icon"></i>
                  <span>认证流程</span>
                </router-link>
                <a href="javascript:;" class="menu-item" @click.prevent="handleLogout">
                  <i class="user-icon logout-icon"></i>
                  <span>退出登录</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-header>
    <!-- 2.中部内容区域 -->
    <el-main>
      <!-- 二级路由出口 要展示：首页、公司、职位....... -->
      <router-view></router-view>
    </el-main>
  </el-container>
</template>
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import CitySelector from "../../components/CitySelector.vue";

const router = useRouter();
const currentCity = ref("北京");
const showSelector = ref(false);
const unreadCount = ref(3);
const showMessageTip = ref(false);
const showResumeMenu = ref(false);
const showUserMenu = ref(false);
let userMenuTimer = null;
const displayName = ref("用户");

const clearUserMenuTimer = () => {
  if (userMenuTimer) {
    clearTimeout(userMenuTimer);
    userMenuTimer = null;
  }
};

const onUserMenuLeave = () => {
  userMenuTimer = setTimeout(() => {
    showUserMenu.value = false;
  }, 200);
};

const onSelectCity = (city) => {
  currentCity.value = city;
};

const refreshHome = () => {
  if (window.location.pathname === "/home") {
    window.location.reload();
  }
};

const loadDisplayName = () => {
  const role = localStorage.getItem("role") || "user";
  const username = localStorage.getItem("username") || "用户";
  if (role === "hr") {
    displayName.value = `HR-${username}`;
  } else {
    displayName.value = `求职者-${username}`;
  }
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
.boss-header {
  background-color: #202329;
  color: white;
  height: 49px;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
  background-image: url("https://img.bosszhipin.com/static/zhipin/geek/982401352937125536.png.webp");
  background-size: 100% 49px;
  background-repeat: no-repeat;
  margin: 0;
  padding: 0;
  border: none;
  box-shadow: none;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.logo a {
  color: #00bebd;
  font-size: 22px;
  font-weight: bold;
  text-decoration: none;
  margin-right: 30px;
}

.city-selector-btn {
  position: relative;
  margin-right: 30px;
  cursor: pointer;
  padding: 0 10px;
  height: 100%;
  display: flex;
  align-items: center;
}

.city-selector-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.location-icon {
  display: inline-block;
  width: 14px;
  height: 14px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23FFFFFF"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>');
  background-repeat: no-repeat;
  margin-right: 5px;
}

.current-city {
  font-size: 14px;
  color: #ffffff;
}

.switch-text {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  margin-left: 4px;
}

.main-nav ul {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

.main-nav li {
  margin: 0 10px;
  position: relative;
}

.main-nav a {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 14px;
  padding: 15px 5px;
  display: inline-block;
  transition: all 0.3s;
}

.main-nav a:hover,
.main-nav a.active {
  color: #ffffff;
  font-weight: 500;
}

.combo-item {
  display: flex;
  align-items: center;
}

.divider {
  color: rgba(255, 255, 255, 0.3);
  margin: 0 2px;
}

.user-area {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 20px;
}

.message-box {
  position: relative;
}

.message-btn {
  display: flex;
  align-items: center;
  position: relative;
}

.message-icon {
  display: inline-block;
  width: 20px;
  height: 20px;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23FFFFFF"><path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/></svg>');
  background-repeat: no-repeat;
}

.message-count {
  background: #ff7d00;
  color: #fff;
  border-radius: 8px;
  font-size: 12px;
  padding: 2px 6px;
  margin-left: 4px;
  position: absolute;
  top: -8px;
  right: -8px;
}

.message-tip {
  position: absolute;
  top: 36px;
  left: 0;
  background: #fff;
  color: #333;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  padding: 8px 16px;
  z-index: 20;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.tip-arrow {
  width: 0;
  height: 0;
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-bottom: 8px solid #fff;
  position: absolute;
  top: -8px;
  left: 16px;
}

.tip-content {
  font-size: 13px;
  color: #333;
}

.resume-box {
  position: relative;
}

.resume-btn {
  color: #fff;
  background: none;
  border: none;
  font-size: 15px;
  cursor: pointer;
  padding: 0 10px;
  height: 100%;
  display: flex;
  align-items: center;
}

.resume-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: #fff;
  color: #333;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  min-width: 140px;
  padding: 8px 0;
  z-index: 10;
}

.resume-menu .menu-item {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  color: #333;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.2s;
}

.resume-menu .menu-item:hover {
  background: #f5f7fa;
  color: #00bebd;
}

.resume-icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 8px;
  background-repeat: no-repeat;
  background-size: contain;
}

.edit-icon {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23333"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>');
}

.upload-icon {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23333"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>');
}

.template-icon {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23333"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"/><path d="M7 12h2v5H7zm4-7h2v12h-2zm4 4h2v8h-2z"/></svg>');
}

.qa-icon {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23333"><path d="M21 6h-2v9H6v2c0 .55.45 1 1 1h11l4 4V7c0-.55-.45-1-1-1zm-4 6V3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v14l4-4h11c.55 0 1-.45 1-1z"/></svg>');
}

.user-avatar {
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0 10px;
  height: 100%;
}

.user-name {
  color: #fff;
  font-size: 14px;
}

.user-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: #fff;
  color: #333;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  min-width: 160px;
  padding: 8px 0;
  z-index: 10;
  display: flex;
  flex-direction: column;
}

.user-menu .menu-item {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  color: #333;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.2s;
}

.user-menu .menu-item:hover {
  background: #f5f7fa;
  color: #00bebd;
}

.user-icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-right: 8px;
  background-repeat: no-repeat;
  background-size: contain;
}

.profile-icon {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23333"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>');
}

.settings-icon {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23333"><path d="M19.43 12.98c.04-.32.07-.64.07-.98s-.03-.66-.07-.98l2.11-1.65c.19-.15.24-.42.12-.64l-2-3.46c-.12-.22-.39-.3-.61-.22l-2.49 1c-.52-.4-1.08-.73-1.69-.98l-.38-2.65C14.46 2.18 14.25 2 14 2h-4c-.25 0-.46.18-.49.42l-.38 2.65c-.61.25-1.17.59-1.69.98l-2.49-1c-.23-.09-.49 0-.61.22l-2 3.46c-.13.22-.07.49.12.64l2.11 1.65c-.04.32-.07.65-.07.98s.03.66.07.98l-2.11 1.65c-.19.15-.24.42-.12.64l2 3.46c.12.22.39.3.61.22l2.49-1c.52.4 1.08.73 1.69.98l.38 2.65c.03.24.24.42.49.42h4c.25 0 .46-.18.49-.42l.38-2.65c.61-.25 1.17-.59 1.69-.98l2.49 1c.23.09.49 0 .61-.22l2-3.46c.12-.22.07-.49-.12-.64l-2.11-1.65zM12 15.5c-1.93 0-3.5-1.57-3.5-3.5s1.57-3.5 3.5-3.5 3.5 1.57 3.5 3.5-1.57 3.5-3.5 3.5z"/></svg>');
}

.verify-icon {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23333"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/></svg>');
}

.logout-icon {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23333"><path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/></svg>');
}

.message-btn:hover,
.resume-btn:hover,
.user-avatar:hover {
  opacity: 0.8;
}

a {
  text-decoration: none;
}

.el-container {
  margin: 0 !important;
  padding: 0 !important;
}

.el-header {
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  height: 49px !important;
}

.el-main {
  padding: 0;
  margin: 0;
}
</style>
