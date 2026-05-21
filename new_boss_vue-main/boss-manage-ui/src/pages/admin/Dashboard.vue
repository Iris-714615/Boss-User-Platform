<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const quickStats = ref([
  { label: '新增企业', value: '128' },
  { label: '新增职位', value: '356' },
  { label: '新增求职者', value: '812' },
  { label: '待处理举报', value: '23' },
])

const goToDataDashboard = () => {
  router.push('/admin/data-dashboard')
}
</script>

<template>
  <el-card>
    <template #header>
      <div style="font-weight: 600">数据概览</div>
    </template>

    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px">
      <div v-for="item in quickStats" :key="item.label" style="background: #ffffff; border: 1px solid #ebeef5; border-radius: 10px; padding: 16px">
        <div style="color: #909399; font-size: 13px">{{ item.label }}</div>
        <div style="font-size: 22px; font-weight: 700; margin-top: 8px">{{ item.value }}</div>
      </div>
    </div>

    <div style="margin-top: 16px; display: flex; gap: 12px">
      <el-button type="primary" @click="goToDataDashboard">
        📊 查看完整数据大屏
      </el-button>
      <el-button>
        📈 转化分析
      </el-button>
      <el-button>
        ⚠️ 风险预警
      </el-button>
    </div>

    <div style="margin-top: 16px">
      <el-card shadow="never" style="border: 1px solid #ebeef5">
        <template #header>
          <div style="font-weight: 600">运营预警（占位）</div>
        </template>
        <div style="color: #909399; font-size: 13px">
          后续可接入：异常注册/发职位、举报/质检高风险会话、转化漏斗异常等。
        </div>
      </el-card>
    </div>
  </el-card>
</template>

