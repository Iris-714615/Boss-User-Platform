<script setup>
import { ref } from 'vue'
import { TrendCharts, User, Document, Calendar } from '@element-plus/icons-vue'

const dateRange = ref('近 7 天')

// 核心数据
const metrics = ref([
  { label: '职位曝光量', value: '125,678', trend: '+12.5%', icon: Document },
  { label: '主动沟通数', value: '2,456', trend: '+8.3%', icon: User },
  { label: '收到简历数', value: '856', trend: '+15.2%', icon: Document },
  { label: '安排面试数', value: '123', trend: '+5.6%', icon: Calendar }
])

// 趋势数据
const trendData = ref([
  { date: '03-25', views: 15600, communicates: 320, resumes: 98 },
  { date: '03-26', views: 16800, communicates: 356, resumes: 112 },
  { date: '03-27', views: 14200, communicates: 298, resumes: 87 },
  { date: '03-28', views: 18900, communicates: 412, resumes: 135 },
  { date: '03-29', views: 12300, communicates: 256, resumes: 76 },
  { date: '03-30', views: 19800, communicates: 445, resumes: 148 },
  { date: '03-31', views: 17600, communicates: 369, resumes: 120 }
])

// 职位效果排行
const positionRanking = ref([
  { rank: 1, name: '高级前端工程师', views: 1256, resumes: 34, rate: '2.7%' },
  { rank: 2, name: '产品经理', views: 982, resumes: 28, rate: '2.8%' },
  { rank: 3, name: 'Java 开发工程师', views: 856, resumes: 19, rate: '2.2%' },
  { rank: 4, name: 'UI 设计师', views: 634, resumes: 15, rate: '2.4%' },
  { rank: 5, name: '测试工程师', views: 423, resumes: 12, rate: '2.8%' }
])
</script>

<template>
  <div class="data-container">
    <!-- 核心指标 -->
    <el-row :gutter="20" class="metrics-row">
      <el-col :span="6" v-for="(metric, index) in metrics" :key="index">
        <el-card shadow="hover" class="metric-card">
          <div class="metric-content">
            <div class="metric-icon" :style="{ background: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)` }">
              <el-icon :size="24"><component :is="metric.icon" /></el-icon>
            </div>
            <div class="metric-info">
              <div class="metric-label">{{ metric.label }}</div>
              <div class="metric-value">{{ metric.value }}</div>
              <div class="metric-trend">{{ metric.trend }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 趋势图表 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>📈 数据趋势</span>
              <el-radio-group v-model="dateRange" size="small">
                <el-radio-button label="近 7 天" />
                <el-radio-button label="近 30 天" />
              </el-radio-group>
            </div>
          </template>
          
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; background: #f5f7fa; border-radius: 8px">
            <div style="text-align: center; color: #909399">
              <el-icon :size="48" style="margin-bottom: 16px"><TrendCharts /></el-icon>
              <div>ECharts 图表区域（待接入）</div>
              <div style="font-size: 12px; margin-top: 8px">展示曝光、沟通、简历的趋势变化</div>
            </div>
          </div>
          
          <!-- 简易表格 -->
          <el-table :data="trendData" style="margin-top: 16px" size="small">
            <el-table-column prop="date" label="日期" width="100" />
            <el-table-column prop="views" label="曝光量" />
            <el-table-column prop="communicates" label="沟通数" />
            <el-table-column prop="resumes" label="简历数" />
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="never">
          <template #header>
            <span>🏆 职位效果榜</span>
          </template>
          
          <el-table :data="positionRanking" style="width: 100%" size="small">
            <el-table-column type="index" label="排名" width="60">
              <template #default="{ $index }">
                <el-tag 
                  v-if="$index < 3"
                  :type="$index === 0 ? '' : $index === 1 ? '' : ''"
                  style="background: linear-gradient(45deg, #FFD700, #FFA500); color: white; border: none"
                >
                  {{ $index + 1 }}
                </el-tag>
                <span v-else>{{ $index + 1 }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="职位名称" min-width="120" />
            <el-table-column prop="views" label="查看" width="80" />
            <el-table-column prop="resumes" label="简历" width="80" />
            <el-table-column prop="rate" label="转化率" width="80">
              <template #default="{ row }">
                <span style="color: #67C23A">{{ row.rate }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.data-container {
  padding: 0;
}

.metrics-row {
  margin-bottom: 20px;
}

.metric-card {
  border-radius: 8px;
  overflow: hidden;
}

.metric-content {
  display: flex;
  align-items: center;
}

.metric-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 16px;
}

.metric-info {
  flex: 1;
}

.metric-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.metric-value {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
  line-height: 1;
}

.metric-trend {
  font-size: 12px;
  color: #67C23A;
  margin-top: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
