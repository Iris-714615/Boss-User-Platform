<template>
  <div class="login-wrap">
    <div class="login-card">
      <div class="login-title">Boss 直聘 - 平台管理端</div>

      <el-form :model="form" label-width="80px" class="login-form" :rules="rules" ref="loginFormRef">
        <el-form-item label="账号" prop="username">
          <el-input v-model="form.username" placeholder="请输入账号" autocomplete="username" />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            placeholder="请输入密码"
            type="password"
            autocomplete="current-password"
            show-password
            @keyup.enter="onSubmit"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" style="width: 100%" :loading="loading" @click="onSubmit">
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="login-tip">温馨提示：请使用管理员账号登录系统。</div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
})

const rules = {
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' },
    { min: 3, max: 20, message: '账号长度在 3-20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' }
  ]
}

const onSubmit = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      loading.value = true
      try {
        // TODO: 对接真实登录接口
        // const response = await api.login(form)
        // localStorage.setItem('token', response.token)
        // localStorage.setItem('userInfo', JSON.stringify(response.userInfo))
        
        // 模拟登录成功 - 设置 token
        localStorage.setItem('token', 'mock_token_' + Date.now())
        localStorage.setItem('userInfo', JSON.stringify({
          username: form.username,
          realName: '管理员',
          role: '超级管理员'
        }))
        
        // 模拟登录延迟
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        ElMessage.success('登录成功')
        
        // 直接跳转到首页（数据概览页）
        router.replace('/admin/dashboard')
      } catch (error) {
        ElMessage.error('登录失败，请检查账号密码')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background-color: #f5f7fa;
}

.login-card {
  width: 420px;
  padding: 24px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.login-title {
  font-size: 18px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 18px;
}

.login-tip {
  margin-top: 12px;
  font-size: 12px;
  color: #909399;
  text-align: center;
}
</style>
