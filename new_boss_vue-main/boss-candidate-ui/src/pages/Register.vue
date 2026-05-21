<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, User, Lock, Message, Phone, InfoFilled, CircleCheck } from '@element-plus/icons-vue'

const router = useRouter()
const registerFormRef = ref(null)
const loading = ref(false)
const step = ref(1) // 1: 手机号验证，2: 设置密码，3: 注册成功
const countdown = ref(0)

const form = ref({
  phone: '',
  code: '',
  password: '',
  confirmPassword: '',
  agreeTerms: true
})

const rules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码为 6 位数字', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 16, message: '密码长度在 6-16 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== form.value.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const sendCode = async () => {
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
  
  // TODO: 调用发送验证码接口
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  ElMessage.success('验证码已发送')
  countdown.value = 60
  
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

const onNextStep = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid, fields) => {
    if (valid) {
      // TODO: 调用验证手机号接口
      await new Promise(resolve => setTimeout(resolve, 1000))
      step.value = 2
      ElMessage.success('手机号验证通过')
    } else {
      ElMessage.warning('请填写完整的信息')
    }
  })
}

const onRegister = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      if (!form.value.agreeTerms) {
        ElMessage.warning('请先同意用户协议和隐私政策')
        return
      }
      
      loading.value = true
      try {
        // TODO: 调用注册接口
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        // 注册成功
        ElMessageBox.alert(
          '<p style="font-size: 16px; font-weight: 600; margin-bottom: 8px;">🎉 注册成功</p><p style="color: #909399;">账号已创建，现在可以登录了</p>',
          '提示',
          {
            dangerouslyUseHTMLString: true,
            confirmButtonText: '立即登录',
            type: 'success'
          }
        ).then(() => {
          router.replace('/login')
        })
      } catch (error) {
        ElMessage.error('注册失败，请稍后重试')
      } finally {
        loading.value = false
      }
    } else {
      ElMessage.warning('请填写完整的信息')
    }
  })
}

const onBack = () => {
  if (step.value === 2) {
    step.value = 1
  } else {
    router.back()
  }
}
</script>

<template>
  <div class="register-container">
    <div class="register-box">
      <!-- 返回按钮 -->
      <div class="back-btn" @click="onBack">
        <el-icon><ArrowLeft /></el-icon>
      </div>
      
      <!-- 进度条 -->
      <div class="progress-bar">
        <div class="progress-step" :class="{ active: step >= 1 }">
          <div class="step-number">{{ step > 1 ? '✓' : '1' }}</div>
          <div class="step-label">验证手机</div>
        </div>
        <div class="step-line" :class="{ active: step >= 2 }"></div>
        <div class="progress-step" :class="{ active: step >= 2 }">
          <div class="step-number">{{ step > 2 ? '✓' : '2' }}</div>
          <div class="step-label">设置密码</div>
        </div>
      </div>
      
      <!-- 步骤 1：手机号验证 -->
      <div v-if="step === 1" class="step-content">
        <div class="step-header">
          <h2 class="step-title">注册 BOSS 直聘账号</h2>
          <p class="step-subtitle">使用手机号注册，开启职业旅程</p>
        </div>
        
        <el-form
          ref="registerFormRef"
          :model="form"
          :rules="rules"
          class="register-form"
          size="large"
        >
          <el-form-item prop="phone">
            <el-input
              v-model="form.phone"
              placeholder="请输入手机号"
              maxlength="11"
            >
              <template #prefix>
                <el-icon><Phone /></el-icon>
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
                <el-icon><Message /></el-icon>
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
            <el-checkbox v-model="form.agreeTerms">
              <span style="font-size: 13px; color: #606266">
                我已阅读并同意
                <el-link type="primary" underline="never" @click.prevent="ElMessage.info('查看用户协议')">《用户协议》</el-link>
                和
                <el-link type="primary" underline="never" @click.prevent="ElMessage.info('查看隐私政策')">《隐私政策》</el-link>
              </span>
            </el-checkbox>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              style="width: 100%"
              @click="onNextStep"
            >
              下一步
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="step-footer">
          <p class="tip-text">
            已有账号？
            <el-link type="primary" underline="never" @click="router.push('/login')">
              立即登录
            </el-link>
          </p>
        </div>
      </div>
      
      <!-- 步骤 2：设置密码 -->
      <div v-else-if="step === 2" class="step-content">
        <div class="step-header">
          <h2 class="step-title">设置登录密码</h2>
          <p class="step-subtitle">用于下次密码登录和账号保护</p>
        </div>
        
        <el-form
          ref="registerFormRef"
          :model="form"
          :rules="rules"
          class="register-form"
          size="large"
        >
          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码（6-16 位）"
              show-password
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              show-password
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item>
            <div class="password-tips">
              <el-icon><InfoFilled /></el-icon>
              <span>密码需包含数字和字母，不能使用纯数字</span>
            </div>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              style="width: 100%"
              @click="onRegister"
            >
              {{ loading ? '注册中...' : '完成注册' }}
            </el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 步骤 3：注册成功 -->
      <div v-else-if="step === 3" class="step-content">
        <div class="success-wrapper">
          <div class="success-icon">
            <el-icon :size="80" color="#67C23A"><CircleCheck /></el-icon>
          </div>
          <h2 class="success-title">注册成功</h2>
          <p class="success-desc">账号已创建，现在可以登录了</p>
          <el-button
            type="primary"
            size="large"
            style="width: 100%; margin-top: 24px"
            @click="router.push('/login')"
          >
            立即登录
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0084ff 0%, #00c6fb 100%);
  padding: 40px 20px;
}

.register-box {
  width: 100%;
  max-width: 420px;
  position: relative;
}

.back-btn {
  position: absolute;
  top: -60px;
  left: 0;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  color: white;
  font-size: 20px;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.progress-bar {
  display: flex;
  align-items: center;
  margin-bottom: 32px;
  padding: 0 20px;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e0e0e0;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  transition: all 0.3s;
}

.progress-step.active .step-number {
  background: #0084ff;
  color: white;
}

.step-label {
  font-size: 13px;
  color: #999;
}

.progress-step.active .step-label {
  color: #303133;
  font-weight: 600;
}

.step-line {
  flex: 1;
  height: 2px;
  background: #e0e0e0;
  margin: 0 20px;
  transition: all 0.3s;
}

.step-line.active {
  background: #0084ff;
}

.step-content {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.step-header {
  text-align: center;
  margin-bottom: 32px;
}

.step-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.step-subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.register-form {
  margin-bottom: 24px;
}

.password-tips {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #909399;
  background: #f5f7fa;
  padding: 8px 12px;
  border-radius: 6px;
}

.step-footer {
  text-align: center;
  margin-top: 16px;
}

.tip-text {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.success-wrapper {
  text-align: center;
  padding: 40px 20px;
}

.success-icon {
  margin-bottom: 24px;
}

.success-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.success-desc {
  font-size: 14px;
  color: #909399;
  margin: 0;
}
</style>
