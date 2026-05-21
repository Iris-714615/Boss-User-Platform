<template>
  <div class="login-container">
    <div class="login-bg">
      <div class="login-pattern"></div>
    </div>
    
    <div class="login-box">
      <div class="login-card">
        <div class="login-header">
          <div class="logo">
            <span class="logo-text">BOSS 直聘</span>
            <span class="logo-sub">企业版</span>
          </div>
          <div class="login-title">企业招聘管理系统</div>
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
        
        <el-form
          ref="loginFormRef"
          :model="form"
          :rules="rules"
          label-width="80px"
          class="login-form"
        >
          <!-- 密码登录 -->
          <template v-if="loginType === 'password'">
            <el-form-item label="账号" prop="username">
              <el-input
                v-model="form.username"
                placeholder="请输入手机号/邮箱"
                size="large"
                autocomplete="username"
              >
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            
            <el-form-item label="密码" prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="请输入密码"
                size="large"
                show-password
                autocomplete="current-password"
                @keyup.enter="onSubmit"
              >
                <template #prefix>
                  <el-icon><Lock /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </template>
          
          <!-- 验证码登录 -->
          <template v-else>
            <el-form-item label="手机号" prop="phone">
              <el-input
                v-model="form.phone"
                placeholder="请输入手机号"
                size="large"
                maxlength="11"
              >
                <template #prefix>
                  <el-icon><Message /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            
            <el-form-item label="验证码" prop="code">
              <div style="display: flex; gap: 12px; width: 100%">
                <el-input
                  v-model="form.code"
                  placeholder="请输入验证码"
                  size="large"
                  maxlength="6"
                  style="flex: 1"
                  @keyup.enter="onSubmit"
                >
                  <template #prefix>
                    <el-icon><Message /></el-icon>
                  </template>
                </el-input>
                <el-button
                  size="large"
                  :disabled="countdown > 0"
                  @click="sendCode"
                  style="min-width: 120px"
                >
                  {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
                </el-button>
              </div>
            </el-form-item>
          </template>
          
          <el-form-item>
            <div class="login-options">
              <el-checkbox v-model="form.remember">记住账号</el-checkbox>
              <el-link type="primary" :underline="false">忘记密码</el-link>
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
          
          <div class="login-tips">
            <el-divider>其他登录方式</el-divider>
            <div class="other-login">
              <el-button circle size="small">
                <el-icon><Connection /></el-icon>
              </el-button>
              <el-button circle size="small">
                <el-icon><VideoPlay /></el-icon>
              </el-button>
            </div>
            <p class="tip-text">
              还没有账号？
              <el-link type="primary" :underline="false" @click="goToRegister">立即注册</el-link>
            </p>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Lock, Connection, VideoPlay, Message } from '@element-plus/icons-vue'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)
const loginType = ref('password') // 'password' 或 'code'
const countdown = ref(0)

const form = reactive({
  username: '',
  password: '',
  phone: '',
  code: '',
  remember: false
})

const rules = {
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
    { min: 5, max: 50, message: '账号长度在 5-50 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为 6 位数字', trigger: 'blur' }
  ]
}

// 发送验证码
const sendCode = () => {
  if (!form.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }
  
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(form.phone)) {
    ElMessage.error('请输入正确的手机号')
    return
  }
  
  if (countdown.value > 0) return
  
  // TODO: 调用发送验证码接口
  ElMessage.success(`验证码已发送到 ${form.phone}`)
  countdown.value = 60
  
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

const onSubmit = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // TODO: 对接真实登录接口
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // 模拟登录成功
        const token = 'mock_company_token_' + Date.now()
        localStorage.setItem('companyToken', token)
        localStorage.setItem('companyUserInfo', JSON.stringify({
          username: form.username,
          realName: '张经理',
          company: '示例科技有限公司',
          role: 'HR 经理',
          avatar: ''
        }))
        
        ElMessage.success('登录成功')
        router.replace('/company/dashboard')
      } catch (error) {
        ElMessage.error('登录失败，请检查账号密码')
      } finally {
        loading.value = false
      }
    }
  })
}

const goToRegister = () => {
  router.push('/company/certification')
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  position: relative;
  overflow: hidden;
}

.login-bg {
  position: absolute;
  left: 0;
  top: 0;
  width: 50%;
  height: 100%;
  background: linear-gradient(135deg, #0084ff 0%, #00c6fb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-pattern {
  width: 400px;
  height: 400px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.login-box {
  position: absolute;
  right: 0;
  top: 0;
  width: 50%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
}

.login-card {
  width: 420px;
  padding: 40px;
}

.login-tabs {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
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

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  display: inline-flex;
  align-items: center;
  margin-bottom: 24px;
}

.logo-text {
  font-size: 28px;
  font-weight: 700;
  color: #0084ff;
  letter-spacing: 2px;
}

.logo-sub {
  font-size: 14px;
  color: #909399;
  margin-left: 12px;
}

.login-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.login-form {
  margin-top: 32px;
}

.login-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.login-tips {
  margin-top: 24px;
  text-align: center;
}

.other-login {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin: 16px 0;
}

.tip-text {
  font-size: 14px;
  color: #909399;
  margin-top: 16px;
}
</style>
