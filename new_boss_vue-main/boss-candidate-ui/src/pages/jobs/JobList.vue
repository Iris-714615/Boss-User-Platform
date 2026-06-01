<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search, Location, Money, Briefcase } from '@element-plus/icons-vue'
import { positions, formatSalary } from 'shared-types'
import request from '@/utils/request'
const route = useRoute()
const router = useRouter()

const query = reactive({
  name: route.query.name || '',
  city: route.query.city || '',
  salary: '',
  experience: ''
})

// 使用统一的职位数据
// const jobList = computed(() => {
//   return positions.map(pos => ({
//     id: pos.id,
//     title: pos.title,
//     companyId: pos.companyId,
//     companyName: pos.companyName,
//     salaryDisplay: formatSalary(pos.salaryMin, pos.salaryMax, pos.salaryMonth),
//     city: pos.city,
//     district: pos.district,
//     experience: pos.experience,
//     education: pos.education,
//     tags: pos.tags || pos.welfare,
//     hot: pos.status === '已发布',
//     industry: pos.industry,
//     scale: pos.scale
//   }))
// })
const jobList = ref([])
const search = ()=>{
  request.get('search?name='+query.name+'&city='+query.city).then(res=>{
    jobList.value = res.data
  })
}
const onSearch = () => {
  // router.push({ path: '/candidate/jobs', query })
  search()
}
onMounted(()=>{
  query.name = route.query.name || ''
  query.city = route.query.city || ''
  search()
})
</script>

<template>
  <div class="job-list-container">
    <!-- 筛选区 -->
    <el-card shadow="never" class="filter-card">
      <el-form :inline="true" :model="query">
        <el-form-item>
          <el-input v-model="query.name" placeholder="职位/公司" style="width: 200px" />
        </el-form-item>
        <el-form-item>
          <el-select v-model="query.city" placeholder="城市" style="width: 120px" clearable>
            <el-option label="北京" value="北京" />
            <el-option label="上海" value="上海" />
            <el-option label="广州" value="广州" />
            <el-option label="深圳" value="深圳" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSearch">搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 职位列表 -->
    <el-card shadow="never" class="job-card" style="margin-top: 16px">
      <div class="job-item" v-for="job in jobList" :key="job.id" @click="router.push(`/candidate/jobs/${job.id}`)">
        <div class="job-header">
          <span class="job-title">{{ job.job_name }}</span>
          <el-tag v-if="job.hot" type="danger" size="small">热</el-tag>
        </div>
        <div class="job-company">{{ job.companyName }}</div>
        <div class="job-info">
          <span><Money /> {{ job.salaryDisplay }}</span>
          <span><Location /> {{ job.city }}{{ job.district ? '·' + job.district : '' }}</span>
          <span><Briefcase /> {{ job.experience }} · {{ job.education }}</span>
        </div>
        <div class="job-tags" v-if="job.tags && job.tags.length > 0">
          <el-tag v-for="(tag, index) in job.tags" :key="index" size="small" effect="plain" style="margin-right: 6px; margin-top: 6px">
            {{ tag }}
          </el-tag>
        </div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.job-list-container {
  padding-bottom: 20px;
}

.filter-card {
  border-radius: 12px;
}

.job-card {
  border-radius: 12px;
}

.job-item {
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}

.job-item:last-child {
  border-bottom: none;
}

.job-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.job-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.job-company {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.job-info {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
}

.job-info span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.job-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
</style>
