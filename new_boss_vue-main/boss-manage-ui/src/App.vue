<script setup>

</script>

<template>
  <div>
    <!-- 路由出口，用于渲染匹配到的路由组件 -->
    <router-view></router-view>


  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>