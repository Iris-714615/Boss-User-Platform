<template>
  <div v-if="processing" style="text-align: center; padding: 50px;">
    <h2>正在处理登录...</h2>
  </div>
  <div v-else style="text-align: center; padding: 50px;">
    <h2>{{ message }}</h2>
    <p v-if="error">正在跳转到登录页...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const processing = ref(true)
const message = ref('')
const error = ref(false)

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search)
  const token = urlParams.get('token')
  const userid = urlParams.get('userid')
  const username = urlParams.get('username')
  const phone = urlParams.get('phone')
  const name = urlParams.get('name')

  if (token && userid) {
    // 存储登录信息
    localStorage.setItem('candidateToken', token)
    localStorage.setItem('candidateInfo', JSON.stringify({
      phone: phone || '',
      name: username || name || '钉钉用户',
      avatar: '',
      resumeStatus: '完善中'
    }))

    message.value = '登录成功！正在跳转...'
    ElMessage.success('登录成功')
    
    // 清理URL参数并跳转
    window.history.replaceState({}, document.title, window.location.pathname)
    setTimeout(() => {
      router.replace('/candidate/home')
    }, 100)
  } else {
    processing.value = false
    error.value = true
    message.value = '登录信息无效'
    ElMessage.error('登录信息无效')
    setTimeout(() => {
      router.replace('/login')
    }, 2000)
  }
})
</script>
