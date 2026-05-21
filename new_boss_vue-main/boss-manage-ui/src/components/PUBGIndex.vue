<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  // 默认进入平台管理端
  router.replace('/admin/dashboard')
})
</script>

<template>
  <div style="padding: 24px">正在进入平台管理端...</div>
</template>

<style scoped></style>