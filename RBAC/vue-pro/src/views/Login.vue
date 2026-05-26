<template>
  <div class="login-container">
    <div class="login-box">
      <h2>RBAC 权限管理系统</h2>
      <el-form ref="loginForm" :model="form" label-width="80px">
        <el-form-item label="用户名" prop="name">
          <el-input v-model="form.name" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="form.password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" style="width: 100%">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
const router = useRouter()
const form = ref({
  name: '',
  password: ''
})

const handleLogin = () => {
  if (form.value.name && form.value.password) {
   request.post('/user/login', form.value).then(res => {
    console.log('登录响应:', res)
    if (res && res.code === 200) {
      ElMessage.success('登录成功')
      localStorage.setItem('token', res.token)
      localStorage.setItem('name', res.name)
      localStorage.setItem('userid', res.userid)
      localStorage.setItem('menulist', JSON.stringify(res.menulist))
      router.push('/home')
    } else {
      ElMessage.error(res?.msg || '登录失败')
    }
   }).catch(err => {
    console.error('登录请求失败:', err)
    ElMessage.error('登录失败，请检查网络连接')
   })
  } else {
    ElMessage.error('请输入用户名和密码')
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.login-box h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}
</style>
