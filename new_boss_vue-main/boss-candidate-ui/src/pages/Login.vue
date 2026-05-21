<script setup>
import {ref, onUnmounted} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import {User, Lock, Message, ChatDotRound, Loading} from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)
const loginType = ref('password') // 'password' or 'code'
const countdown = ref(0)

// 钉钉登录相关
const dingTalkWindow = ref(null)
const dingTalkSuccess = ref(false)   // 新增：标记登录是否已完成

const form = ref({
  phone: '',
  password: '',
  code: '',
  remember: false
})

const rules = {
  phone: [
    {required: true, message: '请输入手机号', trigger: 'blur'},
    {pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur'}
  ],
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'},
    {min: 6, message: '密码长度不能少于 6 位', trigger: 'blur'}
  ],
  code: [
    {required: true, message: '请输入验证码', trigger: 'blur'},
    {len: 6, message: '验证码为 6 位数字', trigger: 'blur'}
  ]
}

const onSubmit = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // TODO: 对接真实登录接口
        await new Promise(resolve => setTimeout(resolve, 1000))

        const token = 'mock_candidate_token_' + Date.now()
        localStorage.setItem('candidateToken', token)
        localStorage.setItem('candidateInfo', JSON.stringify({
          phone: form.value.phone,
          name: '张先生',
          avatar: '',
          resumeStatus: '完善中'
        }))

        ElMessage.success('登录成功')
        router.replace('/candidate/home')
      } catch (error) {
        ElMessage.error('登录失败，请检查账号密码')
      } finally {
        loading.value = false
      }
    } else {
      ElMessage.warning('请填写完整的登录信息')
    }
  })
}

const sendCode = () => {
  if (!form.value.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }

  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(form.value.phone)) {
    ElMessage.error('请输入正确的手机号')
    return
  }

  if (countdown.value > 0) return

  ElMessage.success('验证码已发送到 ' + form.value.phone)
  countdown.value = 60

  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

const goToRegister = () => {
  console.log('准备跳转到注册页')
  router.push('/register')
}

// ================== 钉钉登录 ==================
const handleDingTalkLogin = () => {
  const clientId = 'dingmbiza7wx7lrsl05z'
  const redirectUri = 'http://127.0.0.1:8000/third_party/dingtalk/login/callback'
  const scope = 'openid corpid Contact.User.Read'

  const loginUrl = 'https://login.dingtalk.com/oauth2/auth' +
      '?response_type=code' +
      `&client_id=${encodeURIComponent(clientId)}` +
      `&redirect_uri=${encodeURIComponent(redirectUri)}` +
      `&scope=${encodeURIComponent(scope)}` +
      '&prompt=consent' +
      '&state=random_state'

  const width = 450
  const height = 600
  const left = (window.screen.width - width) / 2
  const top = (window.screen.height - height) / 2

  dingTalkWindow.value = window.open(
      loginUrl,
      '钉钉登录',
      `width=${width},height=${height},left=${left},top=${top},toolbar=no,menubar=no,scrollbars=no,resizable=yes,location=no,status=no`
  )

  // 监听子窗口关闭
  const checkClosed = setInterval(() => {
    if (dingTalkWindow.value && dingTalkWindow.value.closed) {
      clearInterval(checkClosed)
      console.log('钉钉登录窗口已关闭')
      // 只有未成功登录时才提示取消
      if (!dingTalkSuccess.value) {
        //ElMessage.info('已取消钉钉登录')
      }
    }
  }, 500)

  // 添加消息监听
  window.addEventListener('message', handleDingTalkCallback)
}

const handleDingTalkCallback = (event) => {
  console.log('收到钉钉回调:', event.data)

  if (event.data && event.data.type === 'dingtalk_callback') {
    dingTalkSuccess.value = true   // 标记登录已成功

    const {userInfo, is_bind} = event.data

    try {
      loading.value = true

      // const token = 'candidate_token_' + Date.now()
      // localStorage.setItem('candidateToken', token)
      // localStorage.setItem('candidateInfo', JSON.stringify(userInfo))

      if (is_bind) {
        ElMessage.success('登录成功')
        router.replace('/candidate/home')
      } else {
        ElMessage.warning('请先绑定手机号')
        router.replace('/bind-phone')
      }

      if (dingTalkWindow.value && !dingTalkWindow.value.closed) {
        dingTalkWindow.value.close()
      }
    } catch (error) {
      ElMessage.error('登录处理失败')
    } finally {
      loading.value = false
    }
  }
}

// 组件卸载时重置标记，并清理监听/窗口
onUnmounted(() => {
  dingTalkSuccess.value = false
  window.removeEventListener('message', handleDingTalkCallback)
  if (dingTalkWindow.value && !dingTalkWindow.value.closed) {
    dingTalkWindow.value.close()
  }
})
</script>


<template>
  <div class="login-container">
    <div class="login-wrapper">
      <!-- 左侧品牌区 -->
      <div class="brand-section">
        <div class="brand-content">
          <div class="logo">
            <span class="logo-text">BOSS 直聘</span>
          </div>
          <h1 class="brand-title">找工作直接跟老板谈</h1>
          <p class="brand-desc">
            全国 300+ 城市，数千万求职者使用 BOSS 直聘<br/>
            与雇主直接沟通，快速找到理想工作
          </p>
          <div class="brand-stats">
            <div class="stat-item">
              <div class="stat-value">300+</div>
              <div class="stat-label">覆盖城市</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">5000 万+</div>
              <div class="stat-label">活跃用户</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">95%</div>
              <div class="stat-label">好评率</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧登录表单 -->
      <div class="form-section">
        <div class="form-card">
          <div class="form-header">
            <h2 class="form-title">欢迎回来</h2>
            <p class="form-subtitle">登录后开启精彩职业旅程</p>
          </div>

          <!-- 登录方式切换 -->
          <div class="login-tabs">
            <div
                class="tab-item"
                :class="{ active: loginType === 'password' }"
                @click="loginType = 'password'"
            >
              密码登录
            </div>
            <div
                class="tab-item"
                :class="{ active: loginType === 'code' }"
                @click="loginType = 'code'"
            >
              验证码登录
            </div>
          </div>

          <!-- 密码登录表单 -->
          <el-form
              v-if="loginType === 'password'"
              ref="loginFormRef"
              :model="form"
              :rules="rules"
              class="login-form"
              size="large"
          >
            <el-form-item prop="phone">
              <el-input
                  v-model="form.phone"
                  placeholder="请输入手机号"
                  maxlength="11"
              >
                <template #prefix>
                  <el-icon>
                    <User/>
                  </el-icon>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                  v-model="form.password"
                  type="password"
                  placeholder="请输入密码"
                  show-password
                  @keyup.enter="onSubmit"
              >
                <template #prefix>
                  <el-icon>
                    <Lock/>
                  </el-icon>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item>
              <div class="form-options">
                <el-checkbox v-model="form.remember">记住账号</el-checkbox>
                <el-link type="primary" underline="never" @click="ElMessage.info('请联系客服重置密码')">
                  忘记密码？
                </el-link>
              </div>
            </el-form-item>

            <el-form-item>
              <el-button
                  type="primary"
                  size="large"
                  :loading="loading"
                  style="width: 100%"
                  @click="onSubmit"
              >
                {{ loading ? '登录中...' : '登 录' }}
              </el-button>
            </el-form-item>
          </el-form>

          <!-- 验证码登录表单 -->
          <el-form
              v-else
              ref="loginFormRef"
              :model="form"
              :rules="rules"
              class="login-form"
              size="large"
          >
            <el-form-item prop="phone">
              <el-input
                  v-model="form.phone"
                  placeholder="请输入手机号"
                  maxlength="11"
              >
                <template #prefix>
                  <el-icon>
                    <User/>
                  </el-icon>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item prop="code">
              <el-input
                  v-model="form.code"
                  placeholder="请输入验证码"
                  maxlength="6"
              >
                <template #prefix>
                  <el-icon>
                    <Message/>
                  </el-icon>
                </template>
              </el-input>
              <el-button
                  type="primary"
                  plain
                  :disabled="countdown > 0"
                  @click="sendCode"
                  style="margin-left: 8px"
              >
                {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
              </el-button>
            </el-form-item>

            <el-form-item>
              <el-button
                  type="primary"
                  size="large"
                  :loading="loading"
                  style="width: 100%"
                  @click="onSubmit"
              >
                {{ loading ? '登录中...' : '登 录' }}
              </el-button>
            </el-form-item>
          </el-form>

          <!-- 其他登录方式 -->
          <div class="other-login">
            <el-divider content-position="center">其他登录方式</el-divider>
            <div class="login-methods">
              <el-button circle @click="handleDingTalkLogin" title="钉钉登录">
                <img src="/icons/dingtalk.svg" width="20" height="20" alt="钉钉"/>
              </el-button>
              <el-button circle @click="ElMessage.info('微信登录开发中')" title="微信登录">
                <el-icon size="20">
                  <ChatDotRound/>
                </el-icon>
              </el-button>
            </div>
          </div>


          <div class="form-footer">
            <p class="tip-text">
              还没有账号？
              <el-link type="primary" underline="never" @click="goToRegister">
                立即注册
              </el-link>
            </p>
            <p class="tip-text small">
              未注册的手机号验证通过后自动创建账号
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0084ff 0%, #00c6fb 100%);
  padding: 40px 20px;
}

.login-wrapper {
  display: flex;
  width: 100%;
  max-width: 1200px;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.brand-section {
  flex: 1;
  background: linear-gradient(135deg, #0084ff 0%, #00c6fb 100%);
  padding: 60px;
  color: white;
  display: flex;
  align-items: center;
}

.brand-content {
  max-width: 400px;
}

.logo {
  margin-bottom: 32px;
}

.logo-text {
  font-size: 42px;
  font-weight: 700;
  letter-spacing: 3px;
}

.brand-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 16px 0;
  line-height: 1.4;
}

.brand-desc {
  font-size: 16px;
  line-height: 1.8;
  opacity: 0.9;
  margin: 0 0 40px 0;
}

.brand-stats {
  display: flex;
  gap: 32px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
}

.form-section {
  flex: 1;
  padding: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
}

.form-card {
  width: 100%;
  max-width: 420px;
}

.form-header {
  margin-bottom: 32px;
}

.form-title {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.form-subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.login-tabs {
  display: flex;
  gap: 24px;
  margin-bottom: 32px;
  border-bottom: 2px solid #f0f0f0;
}

.tab-item {
  font-size: 16px;
  color: #606266;
  padding: 12px 0;
  cursor: pointer;
  position: relative;
  transition: all 0.3s;
}

.tab-item.active {
  color: #0084ff;
  font-weight: 600;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: #0084ff;
}

.login-form {
  margin-bottom: 24px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.other-login {
  margin-top: 32px;
}

.login-methods {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 16px;
}

.form-footer {
  margin-top: 24px;
  text-align: center;
}

.tip-text {
  font-size: 14px;
  color: #909399;
  margin: 0 0 8px 0;
}

.tip-text.small {
  font-size: 12px;
  color: #c0c4cc;
}

/* 响应式 */
@media (max-width: 968px) {
  .brand-section {
    display: none;
  }

  .form-section {
    padding: 40px 20px;
  }
}
</style>
