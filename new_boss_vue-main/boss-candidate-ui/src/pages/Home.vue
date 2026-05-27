<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  Search,
  Location,
  Briefcase,
  Money,
  Clock,
  Star,
  TrendCharts,
  UserFilled,
  OfficeBuilding,
  Medal,
  VideoCamera
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { formatSalary, positions, companies } from 'shared-types'
import request from '@/utils/request'

const router = useRouter()

const searchKeyword = ref('')

// 搜索历史
const searchHistory = ref([])

// 热门城市
const hotCities = ref([])

const getHotCities = () => {
  request.get('hot_city').then(res => {
    if (res.code === 200) {
      hotCities.value = res.data
    }
  })
}

// 推荐职位 - 使用统一的职位数据
const recommendedJobs = ref([])
const getRecommendedJobs = () => {
  request.get('hot_job').then(res => {
    if (res.code === 200) {
      recommendedJobs.value = res.data
    }
  })
}


// 分类导航
const categories = ref([])
const getCategories = () => {
  request.get('hot_industry').then(res => {
    if (res.code === 200) {
      categories.value = res.data
    }
  })
}
// 求职期望
const jobExpectation = ref({
  position: '',
  city: '',
  salary: ''
})
const getJobExpectation = () => {
   var token = localStorage.getItem('token')
   token = "2323"
   if (token) {
    request.get('user_info').then(res=>{
      jobExpectation.value.position = res.data.position
      jobExpectation.value.city = res.data.city
      jobExpectation.value.salary = res.data.salary
    })
       }
     }

const gethotsearch = () => {
  request.get('hot_search').then(res => {
    if (res.code === 200) {
      searchHistory.value = res.data
    }
  })
}
const showSuggestion = ref(false)

const userSearchHistory = ref([])
const getuserHistory = () => {
  request.get('search_history').then(res => {
    if (res.code === 200) {
      userSearchHistory.value = res.data
    }
  })
}

onMounted(() => {
  getJobExpectation()
  gethotsearch()
  getuserHistory()
  getCategories()
  getRecommendedJobs()
  getHotCities()
})

const onSearch = () => {
  var keyword = searchKeyword.value.trim()
  if (keyword) {
    request.post('search', { keyword: keyword }).then(res => {
      if (res.code === 200) {
        router.push({ path: '/candidate/jobs', query: { keyword: keyword } })

      } else {
        ElMessage.error(res.msg)
           }
    })
  } else {
    ElMessage.warning('请输入搜索关键词')
  }
}

const goToJobDetail = (id) => {
  router.push(`/candidate/jobs/${id}`)
}

const clearHistory = () => {
  ElMessageBox.confirm('确定要清除搜索历史吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    searchHistory.value = []
    ElMessage.success('已清除搜索历史')
  }).catch(() => {
    // 取消操作
  })
}


// 点击输入框显示联想
const onInputFocus = () => {
  if (searchHistory.value.length > 0) {
    getuserHistory()  
    showSuggestion.value = true
  }
}

// 选择历史记录
const selectHistory = (item) => {
  searchKeyword.value = item
  showSuggestion.value = false
  onSearch()
}

// 点击外部关闭联想弹窗
const closeSuggestion = () => {
  showSuggestion.value = false
}
</script>

<template>
  <div class="home-container">
    <!-- 求职期望卡片 -->
    <el-card shadow="never" class="expectation-card">
      <div class="expectation-header">
        <h3>我的求职期望</h3>
        <el-link type="primary" @click="ElMessage.info('编辑求职期望')">编辑</el-link>
      </div>
      <div class="expectation-content">
        <div class="expectation-item">
          <el-icon><Briefcase /></el-icon>
          <span>意向职位：{{ jobExpectation.position || '未设置' }}</span>
        </div>
        <div class="expectation-item">
          <el-icon><Location /></el-icon>
          <span>期望城市：{{ jobExpectation.city || '未设置' }}</span>
        </div>
        <div class="expectation-item">
          <el-icon><Money /></el-icon>
          <span>期望薪资：{{ jobExpectation.salary || '未设置' }}</span>
        </div>
      </div>
    </el-card>

    <!-- 搜索区 -->
    <el-card shadow="never" class="search-card" style="margin-top: 16px">
      <div class="search-box" style="position: relative">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索职位、公司、行业"
          size="large"
          clearable
          @keyup.enter="onSearch"
          @focus="onInputFocus"
          @blur="closeSuggestion"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
          <template #append>
            <el-button type="primary" @click="onSearch">搜索</el-button>
          </template>
        </el-input>
      

      <!-- 搜索联想弹窗 -->
        <div v-if="showSuggestion" class="suggestion-panel" @click.stop>
          <div class="suggestion-header">
            <span class="suggestion-title">🔍 搜索历史</span>
            <el-button text size="small" @click="clearHistory">清除</el-button>
          </div>
          <div class="suggestion-list">
            <div
              v-for="(item, index) in userSearchHistory"
              :key="index"
              class="suggestion-item"
              @click="selectHistory(item)"
            >
              <el-icon><Clock /></el-icon>
              <span>{{ item }}</span>
            </div>
          </div>
        </div>
        </div>

      <!-- 搜索历史 -->
      <div class="search-history" v-if="searchHistory.length > 0">
        <div class="history-header">
          <span class="history-label">🔥 热门搜索</span>
          <el-button text size="small" @click="clearHistory">清除历史</el-button>
        </div>
        <div class="history-tags">
          <el-tag
            v-for="(item, index) in searchHistory"
            :key="index"
            size="default"
            effect="plain"
            style="margin-right: 8px; margin-bottom: 8px; cursor: pointer"
            @click="router.push({ path: '/candidate/jobs', query: { keyword: item } })"
          >
            {{ item }}
          </el-tag>
        </div>
      </div>
    </el-card>

      
    <!-- 分类导航 -->
    <el-card shadow="never" class="section-card" style="margin-top: 16px">
      <template #header>
        <div class="card-header">
          <span>📊 行业分类</span>
          <el-link type="primary" @click="router.push('/candidate/jobs')">查看全部</el-link>
        </div>
      </template>
      
      <div class="category-grid">
        <div
          v-for="cat in categories"
          :key="cat.name"
          class="category-item"
          @click="router.push({ path: '/candidate/jobs', query: { category: cat.name } })"
        >
          <div class="category-icon">
            <el-icon :size="28"><component :is="cat.icon" /></el-icon>
          </div>
          <div class="category-name">{{ cat.name }}</div>
          <div class="category-count">{{ cat.count }}职位</div>
        </div>
      </div>
    </el-card>

    <!-- 推荐职位 -->
    <el-card shadow="never" class="section-card" style="margin-top: 16px">
      <template #header>
        <div class="card-header">
          <span>🔥 推荐职位</span>
          <el-link type="primary" @click="router.push('/candidate/jobs')">查看更多</el-link>
        </div>
      </template>
      
      <div class="job-list">
        <div
          v-for="job in recommendedJobs"
          :key="job.id"
          class="job-item"
          @click="goToJobDetail(job.id)"
        >
          <div class="job-main">
            <div class="job-header">
              <span class="job-title">{{ job.job_name }}</span>
              <el-tag v-if="job.hot" type="danger" size="small" effect="dark" style="margin-left: 8px">
                急招
              </el-tag>
            </div>
            <div class="job-company">
              <el-icon><OfficeBuilding /></el-icon>
              {{ job.companyName }}
              <span class="company-info">{{ job.industry }} · {{ job.scale }}</span>
            </div>
          </div>
          <div class="job-details">
            <div class="salary">{{ job.salary_range }}</div>
            <div class="job-tags">
              <span class="tag-item"><Location /> {{ job.city }}</span>
              <span class="tag-item"><Clock /> {{ job.work_year }}</span>
              <span class="tag-item"><Briefcase /> {{ job.education }}</span>
            </div>
          </div>
          <div class="welfare-tags">
            <el-tag v-for="tag in job.tags" :key="tag" size="small" effect="plain" round style="margin-right: 4px">
              {{ tag }}
            </el-tag>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 热门城市 -->
    <el-card shadow="never" class="section-card" style="margin-top: 16px">
      <template #header>
        <span>📍 热门城市</span>
      </template>
      
      <div class="city-grid">
        <div
          v-for="city in hotCities"
          :key="city"
          class="city-item"
          @click="router.push({ path: '/candidate/jobs', query: { city } })"
        >
          {{ city }}
        </div>
      </div>
    </el-card>
  </div>
  
</template>

<style scoped>
.home-container {
  padding-bottom: 20px;
}

/* 求职期望卡片 */
.expectation-card {
  border-radius: 12px;
  background: linear-gradient(135deg, #66b1ff 0%, #0084ff 100%);
  color: white;
}

.expectation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.expectation-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.expectation-content {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.expectation-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 12px;
  border-radius: 8px;
}

.search-card {
  border-radius: 12px;
  overflow: visible !important;
}

.search-box {
  position: relative;
  margin-bottom: 16px;
}
/* 搜索联想弹窗 */
.suggestion-panel {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  margin-top: 4px;
  overflow: hidden;
}

.search-history {
  padding-top: 8px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.history-label {
  font-size: 14px;
  color: #909399;
  font-weight: 500;
}

.history-tags {
  display: flex;
  flex-wrap: wrap;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-card {
  border-radius: 12px;
}

/* 分类导航 */
.category-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.category-item:hover {
  background: #f5f7fa;
  transform: translateY(-2px);
}

.category-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e6f2ff 0%, #d0e8ff 100%);
  border-radius: 12px;
  margin-bottom: 8px;
  color: #0084ff;
}

.category-name {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
}

.category-count {
  font-size: 12px;
  color: #909399;
}

/* 职位列表 */
.job-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.job-item {
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.job-item:hover {
  border-color: #0084ff;
  box-shadow: 0 4px 12px rgba(0, 132, 255, 0.1);
  transform: translateY(-2px);
}

.job-main {
  margin-bottom: 12px;
}

.job-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.job-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.job-company {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #606266;
}

.company-info {
  color: #909399;
  font-size: 13px;
  margin-left: 8px;
}

.job-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.salary {
  font-size: 18px;
  color: #f56c6c;
  font-weight: 600;
}

.job-tags {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: #909399;
}

.tag-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.welfare-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* 热门城市 */
.city-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}

.city-item {
  text-align: center;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
  font-size: 14px;
  color: #606266;
  cursor: pointer;
  transition: all 0.3s;
}

.city-item:hover {
  background: #e6f2ff;
  color: #0084ff;
  transform: scale(1.05);
}

/* 响应式 */
@media (max-width: 768px) {
  .category-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .city-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
