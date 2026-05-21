<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'
import {User, Message} from '@element-plus/icons-vue'

const router = useRouter()
const bindFormRef = ref(null)
const loading = ref(false)
const countdown = ref(0)

const form = ref({
  phone: '',
  code: ''
})

const rules = {
  phone: [
    {required: true, message: '请输入手机号', trigger: 'blur'},
    {pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur'}
  ],
  code: [
    {required: true, message: '请输入验证码', trigger: 'blur'},
    {len: 6, message: '验证码为 6 位数字', trigger: 'blur'}
  ]
}

const sendCode = () => {
  if (!form.value.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }

  // 验证手机号格式
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(form.value.phone)) {
    ElMessage.error('请输入正确的手机号')
    return
  }

  if (countdown.value > 0) return

  // TODO: 调用发送验证码接口
  ElMessage.success('验证码已发送到 ' + form.value.phone)
  countdown.value = 60

  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

const onSubmit = async () => {
  if (!bindFormRef.value) return

  await bindFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // TODO: 对接真实绑定接口
        await new Promise(resolve => setTimeout(resolve, 1000))

        // 获取用户信息并更新
        const userInfo = JSON.parse(localStorage.getItem('candidateInfo') || '{}')
        userInfo.phone = form.value.phone
        userInfo.isPhoneBound = true
        localStorage.setItem('candidateInfo', JSON.stringify(userInfo))

        ElMessage.success('绑定成功')

        // 返回上一页或跳转到首页
        const redirect = router.currentRoute.value.query.redirect || '/candidate/home'
        router.replace(redirect)
      } catch (error) {
        ElMessage.error('绑定失败，请稍后重试')
      } finally {
        loading.value = false
      }
    } else {
      ElMessage.warning('请填写完整的信息')
    }
  })
}

const goBack = () => {
  // 使用 replace 或 push 跳转到登录页
  router.replace('/login')   // 根据你的登录页实际路径调整
}
</script>

<template>
  <div class="bind-phone-container">
    <div class="bind-wrapper">
      <!-- 左侧品牌区 -->
      <div class="brand-section">
        <div class="brand-content">
          <div class="logo">
            <span class="logo-text">BOSS 直聘</span>
          </div>
          <h1 class="brand-title">绑定手机号</h1>
          <p class="brand-desc">
            绑定手机号后，您可以：<br/>
            • 接收面试通知和消息提醒<br/>
            • 快速登录账号<br/>
            • 保障账号安全
          </p>
        </div>
      </div>

      <!-- 右侧绑定表单 -->
      <div class="form-section">
        <div class="form-card">
          <div class="form-header">
            <h2 class="form-title">绑定手机号</h2>
            <p class="form-subtitle">请输入您的手机号完成绑定</p>
          </div>

          <el-form
              ref="bindFormRef"
              :model="form"
              :rules="rules"
              class="bind-form"
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
                {{ loading ? '绑定中...' : '确认绑定' }}
              </el-button>
            </el-form-item>
          </el-form>

          <div class="form-footer">
            <el-link type="primary" underline="never" @click="goBack">
              返回
            </el-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bind-phone-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0084ff 0%, #00c6fb 100%);
  padding: 40px 20px;
}

.bind-wrapper {
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
  margin: 0;
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

.bind-form {
  margin-bottom: 24px;
}

.form-footer {
  margin-top: 24px;
  text-align: center;
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
