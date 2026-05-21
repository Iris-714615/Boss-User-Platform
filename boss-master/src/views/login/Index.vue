<template>
  <div class="login-page">
    <!-- 背景层 -->
    <div class="background-layer">
      <!-- 城市轮廓装饰 -->
      <div class="city-silhouette"></div>

      <!-- 底部左侧聊天气泡 -->
      <div class="chat-bubble">
        <div class="chat-icon">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
        <span>说点什么...</span>
      </div>

      <!-- 顶部右侧客服信息 -->
      <div class="service-hotline">客户服务热线: 400 065 5799</div>
    </div>

    <!-- 主容器卡片 -->
    <div class="main-card">
      <!-- 左侧功能展示区 -->
      <div class="left-panel">
        <!-- 第一个功能模块：海量优质人才 -->
        <div class="feature-item feature-main">
          <div class="feature-badge">BOSS 直聘</div>
          <h2 class="feature-main-title">海量优质人才,在线约面</h2>
          <p class="feature-main-desc">找工作,上BOSS直聘直接谈</p>
          <div class="feature-illustration">
            <div class="illustration-content">
              <!-- 人物1 -->
              <div class="person person-1">
                <div class="person-head"></div>
                <div class="person-body yellow-shirt"></div>
                <div class="person-legs white-pants"></div>
              </div>
              <!-- 浏览器窗口 -->
              <div class="browser-window">
                <div class="browser-header">
                  <div class="browser-dot"></div>
                  <div class="browser-dot"></div>
                  <div class="browser-dot"></div>
                </div>
                <div class="browser-content">
                  <div class="profile-grid">
                    <div class="profile-item" v-for="i in 6" :key="i"></div>
                  </div>
                </div>
              </div>
              <!-- 人物2 -->
              <div class="person person-2">
                <div class="person-head"></div>
                <div class="person-body dark-top"></div>
                <div class="person-legs dark-pants"></div>
                <div class="laptop"></div>
              </div>
              <!-- 纸飞机路径 -->
              <div class="paper-plane-path">
                <div class="paper-plane">✈</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 第二、三个功能模块：沟通和任性选 -->
        <div class="feature-row">
          <!-- 第二个功能模块：沟通 -->
          <div class="feature-item">
            <div class="feature-icon-wrapper">
              <div class="feature-icon communication-icon">
                <svg
                  width="32"
                  height="32"
                  viewBox="0 0 32 32"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M8 6C5.79086 6 4 7.79086 4 10V18C4 20.2091 5.79086 22 8 22H12L16 26L12 22H8C5.79086 22 4 20.2091 4 18V10C4 7.79086 5.79086 6 8 6Z"
                    stroke="#333"
                    stroke-width="1.5"
                    fill="none"
                  />
                  <circle cx="11" cy="14" r="1" fill="#333" />
                  <circle cx="16" cy="14" r="1" fill="#333" />
                  <circle cx="21" cy="14" r="1" fill="#333" />
                </svg>
              </div>
            </div>
            <h3 class="feature-title">沟通</h3>
            <p class="feature-desc">在线职位及时沟通</p>
          </div>

          <!-- 第三个功能模块：任性选 -->
          <div class="feature-item">
            <div class="feature-icon-wrapper">
              <div class="feature-icon briefcase-icon">
                <svg
                  width="32"
                  height="32"
                  viewBox="0 0 32 32"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M6 11C6 9.89543 6.89543 9 8 9H24C25.1046 9 26 9.89543 26 11V25C26 26.1046 25.1046 27 24 27H8C6.89543 27 6 26.1046 6 25V11Z"
                    fill="#8B4513"
                    stroke="#8B4513"
                    stroke-width="0.5"
                  />
                  <path
                    d="M11 9V7C11 5.89543 11.8954 5 13 5H19C20.1046 5 21 5.89543 21 7V9"
                    stroke="#8B4513"
                    stroke-width="1.5"
                    fill="none"
                  />
                  <path
                    d="M12 16H20"
                    stroke="white"
                    stroke-width="1.5"
                    stroke-linecap="round"
                  />
                </svg>
              </div>
            </div>
            <h3 class="feature-title">任性选</h3>
            <p class="feature-desc">各大行业职位任你选</p>
          </div>
        </div>
      </div>

      <!-- 右侧登录表单区 -->
      <div class="right-panel">
        <!-- 微信快速注册 -->
        <div class="wechat-quick-register">
          <div class="qr-code-box">
            <svg
              width="16"
              height="16"
              viewBox="0 0 16 16"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <rect
                x="2"
                y="2"
                width="5"
                height="5"
                stroke="#999"
                stroke-width="1"
                fill="none"
              />
              <rect
                x="9"
                y="2"
                width="5"
                height="5"
                stroke="#999"
                stroke-width="1"
                fill="none"
              />
              <rect
                x="2"
                y="9"
                width="5"
                height="5"
                stroke="#999"
                stroke-width="1"
                fill="none"
              />
              <rect
                x="9"
                y="9"
                width="5"
                height="5"
                stroke="#999"
                stroke-width="1"
                fill="none"
              />
              <rect x="3.5" y="3.5" width="2" height="2" fill="#999" />
              <rect x="10.5" y="3.5" width="2" height="2" fill="#999" />
              <rect x="3.5" y="10.5" width="2" height="2" fill="#999" />
            </svg>
          </div>
          <span>微信快速注册在这里</span>
        </div>

        <!-- 主标题 -->
        <h2 class="main-title">登录BOSS直聘</h2>

        <!-- 副标题 -->
        <p class="sub-title">请输入您的用户名和密码进行登录</p>

        <!-- 用户类型选择 -->
        <div class="user-type-selector">
          <button
            :class="['type-btn', { active: userType === 'jobseeker' }]"
            @click="userType = 'jobseeker'"
          >
            我要找工作
          </button>
          <button
            :class="['type-btn', { active: userType === 'recruiter' }]"
            @click="userType = 'recruiter'"
          >
            我要招聘
          </button>
        </div>

        <!-- 用户名输入 -->
        <div class="input-group">
          <input
            v-model="formData.username"
            type="text"
            placeholder="用户名"
            class="form-input"
          />
        </div>

        <!-- 密码输入 -->
        <div class="input-group">
          <input
            v-model="formData.password"
            type="password"
            placeholder="密码"
            class="form-input"
            @keyup.enter="handleLogin"
          />
        </div>

        <!-- 登录按钮 -->
        <button class="login-btn" @click="handleLogin" :disabled="loading">
          {{ loading ? "登录中..." : "登录" }}
        </button>

        <!-- 用户协议 -->
        <div class="terms-checkbox">
          <input
            type="checkbox"
            id="agreeTerms"
            v-model="agreeTerms"
            class="checkbox-input"
          />
          <label for="agreeTerms" class="terms-label">
            已阅读并同意BOSS直聘
            <a href="#" class="terms-link">《用户协议》</a>
            <a href="#" class="terms-link">《隐私政策》</a>
            ,允许BOSS直聘统一管理本人账号信息
          </label>
        </div>

        <!-- 微信登录 -->
        <div class="wechat-login">
          <span class="wechat-icon">
            <svg
              width="18"
              height="18"
              viewBox="0 0 18 18"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M9 2C4.58172 2 1 5.58172 1 10C1 12.5 2.2 14.7 4 16.2L3 19L5.8 18C7.3 18.7 8.9 19 9 19C13.4183 19 17 15.4183 17 11C17 6.58172 13.4183 3 9 3V2Z"
                fill="#07C160"
              />
              <circle cx="6.5" cy="9" r="0.8" fill="white" />
              <circle cx="11.5" cy="9" r="0.8" fill="white" />
            </svg>
          </span>
          <span>微信登录/注册</span>
        </div>

        <!-- 底部信息 -->
        <div class="footer-info">
          <p class="service-info">客服电话 400-065-5799 工作时间: 8:00-22:00</p>
          <p class="legal-info">
            人力资源服务许可证|营业执照|朝阳区人社局监督电话
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { http } from "../../utils/request.js";
import { ElMessage } from "element-plus";

const router = useRouter();

// 1.用户类型选择
const userType = ref("jobseeker"); // jobseeker: 我要找工作, recruiter: 我要招聘

// 2.表单数据
const formData = ref({
  username: "",
  password: "",
});

// 3.是否同意协议
const agreeTerms = ref(false);

// 4.登录按钮加载状态
const loading = ref(false);

// 5.登录
const handleLogin = async () => {
  // 验证表单
  if (!formData.value.username || !formData.value.password) {
    ElMessage.warning("请输入用户名和密码");
    return;
  }

  if (!agreeTerms.value) {
    ElMessage.warning("请先同意用户协议和隐私政策");
    return;
  }

  loading.value = true;

  try {
    // 调用登录接口
    const response = await http.post("/login/", formData.value);

    // 登录成功，保存 token 和用户信息
    if (response.token) {
      localStorage.setItem("token", response.token);
      localStorage.setItem("refresh", response.refresh);
      localStorage.setItem("username", response.username);
      localStorage.setItem("userid", response.userid);
      localStorage.setItem("role", response.role);

      ElMessage.success("登录成功");

      // 根据角色跳转到对应首页
      if (response.role === "hr") {
        router.push("/hr");
      } else {
        router.push("/");
      }
    }
  } catch (error) {
    console.error("登录失败:", error);
    const errorMessage =
      error.response?.data?.message ||
      error.message ||
      "登录失败，请检查用户名和密码";
    ElMessage.error(errorMessage);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  width: 100%;
  height: 100vh;
  background: #00c2c2;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 背景层 */
.background-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

/* 城市轮廓装饰 */
.city-silhouette {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 50%;
  background-image: url("data:image/svg+xml,%3Csvg width='800' height='400' xmlns='http://www.w3.org/2000/svg'%3E%3Cg opacity='0.15'%3E%3Cpath d='M50 350 L80 280 L120 300 L160 250 L200 280 L240 220 L280 240 L320 200 L360 220 L400 180 L440 200 L480 160 L520 180 L560 140 L600 160 L640 120 L680 140 L720 100 L760 120 L800 80 L800 400 L50 400 Z' fill='%23ffffff'/%3E%3Cpath d='M200 280 L220 240 L240 260 L260 220 L280 240 L300 200 L320 220 L340 180 L360 200 L380 160 L400 180 L420 140 L440 160 L460 120 L480 140 L500 100 L520 120 L540 80 L560 100 L580 60 L600 80 L620 40 L640 60 L660 20 L680 40 L700 0 L720 20 L740 0 L760 20 L780 0 L800 20 L800 400 L200 400 Z' fill='%23ffffff'/%3E%3Ccircle cx='400' cy='180' r='15' fill='%23ffffff'/%3E%3Ccircle cx='420' cy='160' r='10' fill='%23ffffff'/%3E%3Ccircle cx='380' cy='160' r='10' fill='%23ffffff'/%3E%3C/g%3E%3C/svg%3E");
  background-size: cover;
  background-repeat: no-repeat;
  background-position: bottom left;
  pointer-events: none;
  opacity: 0.3;
}

/* 底部左侧聊天气泡 */
.chat-bubble {
  position: absolute;
  bottom: 30px;
  left: 30px;
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 2;
}

.chat-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
}

.chat-icon .dot {
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
}

.chat-bubble span:last-child {
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
}

/* 顶部右侧客服信息 */
.service-hotline {
  position: absolute;
  top: 30px;
  right: 30px;
  color: white;
  font-size: 14px;
  z-index: 2;
}

/* 主容器卡片 */
.main-card {
  width: 1100px;
  height: 580px;
  background: white;
  border-radius: 30px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  display: flex;
  overflow: hidden;
  position: relative;
  z-index: 10;
}

/* 左侧功能展示区 */
.left-panel {
  width: 40%;
  background: #f5f5f5;
  padding: 50px 40px 40px 40px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 80px;
}

.feature-item {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feature-row {
  display: flex;
  gap: 16px;
  margin-top: 40px;
}

.feature-row .feature-item {
  flex: 1;
  gap: 8px;
}

.feature-main {
  gap: 12px;
}

.feature-badge {
  display: inline-block;
  background: #00c2c2;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  width: fit-content;
  font-weight: 500;
}

.feature-main-title {
  font-size: 26px;
  font-weight: bold;
  color: white;
  margin: 0;
  line-height: 1.3;
}

.feature-main-desc {
  font-size: 13px;
  color: white;
  margin: 0;
  line-height: 1.4;
}

.feature-illustration {
  margin-top: 10px;
  height: 100px;
  position: relative;
}

.illustration-content {
  width: 100%;
  height: 100%;
  position: relative;
}

.person {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.person-1 {
  left: 15px;
  bottom: 15px;
}

.person-2 {
  right: 15px;
  bottom: 15px;
}

.person-head {
  width: 16px;
  height: 16px;
  background: #ffdbac;
  border-radius: 50%;
  margin-bottom: 2px;
}

.person-body {
  width: 24px;
  height: 28px;
  border-radius: 4px 4px 0 0;
}

.yellow-shirt {
  background: #ffd700;
}

.dark-top {
  background: #333;
}

.person-legs {
  width: 24px;
  height: 20px;
  border-radius: 0 0 4px 4px;
}

.white-pants {
  background: white;
}

.dark-pants {
  background: #333;
}

.laptop {
  position: absolute;
  top: 40px;
  left: -8px;
  width: 40px;
  height: 24px;
  background: #666;
  border-radius: 2px;
  border: 2px solid #333;
}

.laptop::after {
  content: "";
  position: absolute;
  top: -6px;
  left: 50%;
  transform: translateX(-50%);
  width: 32px;
  height: 3px;
  background: #666;
  border-radius: 2px 2px 0 0;
}

.browser-window {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 130px;
  height: 95px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.browser-header {
  height: 20px;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 0 6px;
}

.browser-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ccc;
}

.browser-content {
  padding: 8px;
  height: calc(100% - 20px);
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}

.profile-item {
  width: 100%;
  aspect-ratio: 1;
  background: #e0e0e0;
  border-radius: 4px;
}

.paper-plane-path {
  position: absolute;
  left: 50%;
  top: 25%;
  width: 80px;
  height: 50px;
  transform: translateX(-50%);
}

.paper-plane {
  position: absolute;
  right: 0;
  top: 0;
  font-size: 16px;
  animation: fly 2s ease-in-out infinite;
}

@keyframes fly {
  0% {
    transform: translate(0, 0) rotate(0deg);
  }
  50% {
    transform: translate(-25px, 15px) rotate(-15deg);
  }
  100% {
    transform: translate(-50px, 30px) rotate(-30deg);
  }
}

.feature-icon-wrapper {
  width: 64px;
  height: 64px;
  background: #e8e8e8;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.feature-row .feature-icon-wrapper {
  width: 48px;
  height: 48px;
  margin-bottom: 6px;
}

.feature-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-row .feature-icon {
  width: 24px;
  height: 24px;
}

.feature-row .feature-icon svg {
  width: 24px;
  height: 24px;
}

.feature-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0;
  line-height: 1.2;
}

.feature-row .feature-title {
  font-size: 18px;
}

.feature-desc {
  font-size: 14px;
  color: #666;
  margin: 0;
  line-height: 1.4;
}

.feature-row .feature-desc {
  font-size: 12px;
}

/* 右侧登录表单区 */
.right-panel {
  width: 60%;
  padding: 40px 60px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: relative;
}

.wechat-quick-register {
  position: absolute;
  top: 30px;
  right: 30px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1890ff;
  font-size: 14px;
  cursor: pointer;
}

.qr-code-box {
  width: 24px;
  height: 24px;
  background: #f5f5f5;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin: 0;
  margin-top: 8px;
}

.sub-title {
  font-size: 13px;
  color: #999;
  margin: 0;
  margin-bottom: 6px;
}

/* 用户类型选择 */
.user-type-selector {
  display: flex;
  gap: 12px;
  margin: 12px 0;
}

.type-btn {
  flex: 1;
  padding: 12px 24px;
  border: 1px solid #e0e0e0;
  background: white;
  border-radius: 4px;
  font-size: 15px;
  color: #333;
  cursor: pointer;
  transition: all 0.3s;
}

.type-btn.active {
  background: #e6f7ff;
  border-color: #1890ff;
  color: #1890ff;
}

.type-btn:hover {
  border-color: #1890ff;
}

/* 输入组 */
.input-group {
  margin: 8px 0;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 15px;
  outline: none;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #1890ff;
}

.form-input::placeholder {
  color: #999;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  padding: 14px;
  background: #00c2c2;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 17px;
  font-weight: bold;
  cursor: pointer;
  margin: 16px 0 8px 0;
  transition: all 0.3s;
}

.login-btn:hover:not(:disabled) {
  background: #00a8a8;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 194, 194, 0.3);
}

.login-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

/* 用户协议 */
.terms-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin: 12px 0;
}

.checkbox-input {
  margin-top: 3px;
  cursor: pointer;
}

.terms-label {
  font-size: 12px;
  color: #666;
  line-height: 1.6;
  cursor: pointer;
}

.terms-link {
  color: #1890ff;
  text-decoration: none;
}

.terms-link:hover {
  text-decoration: underline;
}

/* 微信登录 */
.wechat-login {
  text-align: center;
  color: #666;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: auto;
  padding-top: 12px;
}

.wechat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 底部信息 */
.footer-info {
  margin-top: 20px;
  padding-top: 20px;
}

.service-info {
  font-size: 12px;
  color: #999;
  text-align: center;
  margin: 5px 0;
}

.legal-info {
  font-size: 11px;
  color: #ccc;
  text-align: center;
  margin: 5px 0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-card {
    width: 95%;
    max-width: 1100px;
  }
}

@media (max-width: 768px) {
  .main-card {
    flex-direction: column;
    height: auto;
    max-height: 90vh;
    overflow-y: auto;
  }

  .left-panel {
    width: 100%;
    padding: 40px 30px;
    gap: 30px;
  }

  .right-panel {
    width: 100%;
    padding: 40px 30px;
  }
}
</style>
