<script setup lang="ts">
import { ref, reactive } from 'vue'
import { 
  User, 
  OfficeBuilding, 
  Briefcase, 
  Warning,
  TrendCharts,
  ArrowUp,
  ArrowDown
} from '@element-plus/icons-vue'

// 核心指标卡片数据
const coreMetrics = ref([
  { 
    title: '累计企业数', 
    value: '128,456', 
    suffix: '家',
    trend: 'up',
    trendValue: '+12.5%',
    icon: OfficeBuilding,
    color: '#409EFF'
  },
  { 
    title: '累计求职者', 
    value: '2,356,789', 
    suffix: '人',
    trend: 'up',
    trendValue: '+8.3%',
    icon: User,
    color: '#67C23A'
  },
  { 
    title: '在招职位', 
    value: '456,123', 
    suffix: '个',
    trend: 'up',
    trendValue: '+15.2%',
    icon: Briefcase,
    color: '#E6A23C'
  },
  { 
    title: '待处理举报', 
    value: '23', 
    suffix: '件',
    trend: 'down',
    trendValue: '-5.8%',
    icon: Warning,
    color: '#F56C6C'
  },
])

// 今日实时数据
const todayData = reactive({
  newCompanies: 128,
  newPositions: 356,
  newCandidates: 812,
  chatCount: 15623,
  complaintCount: 23,
  activeUsers: 45678,
})

// 趋势图表数据（占位，后续接入 ECharts）
const trendData = ref([
  { date: '03-25', companies: 120, positions: 350, candidates: 800 },
  { date: '03-26', companies: 132, positions: 368, candidates: 856 },
  { date: '03-27', companies: 101, positions: 320, candidates: 720 },
  { date: '03-28', companies: 134, positions: 390, candidates: 900 },
  { date: '03-29', companies: 90, positions: 280, candidates: 650 },
  { date: '03-30', companies: 150, positions: 420, candidates: 980 },
  { date: '03-31', companies: 128, positions: 356, candidates: 812 },
])

// 地域分布 Top10
const regionRanking = ref([
  { rank: 1, city: '北京', companies: 25680, candidates: 458900, change: '+5.2%' },
  { rank: 2, city: '上海', companies: 23450, candidates: 425600, change: '+4.8%' },
  { rank: 3, city: '广州', companies: 18920, candidates: 356700, change: '+3.9%' },
  { rank: 4, city: '深圳', companies: 17650, candidates: 389200, change: '+6.1%' },
  { rank: 5, city: '杭州', companies: 15230, candidates: 298500, change: '+7.3%' },
  { rank: 6, city: '成都', companies: 12890, candidates: 256300, change: '+4.5%' },
  { rank: 7, city: '武汉', companies: 10560, candidates: 215600, change: '+3.2%' },
  { rank: 8, city: '南京', companies: 9870, candidates: 198700, change: '+2.8%' },
  { rank: 9, city: '西安', companies: 8560, candidates: 176500, change: '+4.1%' },
  { rank: 10, city: '重庆', companies: 7890, candidates: 165400, change: '+3.6%' },
])

// 行业分布
const industryDistribution = ref([
  { industry: '互联网/软件', percentage: 28.5, count: 36580 },
  { industry: '电子商务', percentage: 15.2, count: 19520 },
  { industry: '企业服务', percentage: 12.8, count: 16450 },
  { industry: '教育培训', percentage: 10.5, count: 13490 },
  { industry: '金融', percentage: 9.3, count: 11950 },
  { industry: '医疗健康', percentage: 7.6, count: 9760 },
  { industry: '其他', percentage: 16.1, count: 20696 },
])

// 预警信息
const warnings = ref([
  { type: '高风险', title: '异常注册行为检测', count: 15, time: '10 分钟前' },
  { type: '中风险', title: '虚假职位投诉激增', count: 8, time: '30 分钟前' },
  { type: '低风险', title: '会话敏感词触发', count: 23, time: '1 小时前' },
])

// 转化漏斗数据
const funnelData = ref([
  { stage: '注册用户', count: 2356789, rate: 100 },
  { stage: '完善简历', count: 1856234, rate: 78.8 },
  { stage: '主动投递', count: 1256789, rate: 53.3 },
  { stage: '获得面试', count: 456123, rate: 19.4 },
  { stage: '成功入职', count: 125678, rate: 5.3 },
])
</script>

<template>
  <div class="dashboard-container">
    <!-- 核心指标卡片 -->
    <el-row :gutter="20" class="metric-row">
      <el-col :span="6" v-for="(metric, index) in coreMetrics" :key="index">
        <el-card shadow="hover" class="metric-card">
          <div class="metric-content">
            <div class="metric-icon" :style="{ background: metric.color }">
              <el-icon :size="24"><component :is="metric.icon" /></el-icon>
            </div>
            <div class="metric-info">
              <div class="metric-title">{{ metric.title }}</div>
              <div class="metric-value">
                {{ metric.value }}
                <span class="metric-suffix">{{ metric.suffix }}</span>
              </div>
              <div class="metric-trend" :class="metric.trend">
                <el-icon><component :is="metric.trend === 'up' ? ArrowUp : ArrowDown" /></el-icon>
                <span>{{ metric.trendValue }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 今日实时数据 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card shadow="never">
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center">
              <span style="font-weight: 600">📊 今日实时数据（截至 {{ new Date().toLocaleTimeString() }}）</span>
              <el-button type="primary" size="small">刷新</el-button>
            </div>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="4">
              <el-statistic title="新增企业" :value="todayData.newCompanies">
                <template #suffix>家</template>
              </el-statistic>
            </el-col>
            <el-col :span="4">
              <el-statistic title="新增职位" :value="todayData.newPositions">
                <template #suffix>个</template>
              </el-statistic>
            </el-col>
            <el-col :span="4">
              <el-statistic title="新增求职者" :value="todayData.newCandidates">
                <template #suffix>人</template>
              </el-statistic>
            </el-col>
            <el-col :span="4">
              <el-statistic title="沟通次数" :value="todayData.chatCount">
                <template #suffix>次</template>
              </el-statistic>
            </el-col>
            <el-col :span="4">
              <el-statistic title="新增举报" :value="todayData.complaintCount">
                <template #suffix>件</template>
              </el-statistic>
            </el-col>
            <el-col :span="4">
              <el-statistic title="活跃用户" :value="todayData.activeUsers">
                <template #suffix>人</template>
              </el-statistic>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>

    <!-- 趋势图表与预警 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>
            <span style="font-weight: 600">📈 近 7 日趋势</span>
          </template>
          
          <div style="height: 300px; display: flex; align-items: center; justify-content: center; background: #f5f7fa; border-radius: 8px">
            <div style="text-align: center; color: #909399">
              <el-icon :size="48" style="margin-bottom: 16px"><TrendCharts /></el-icon>
              <div>ECharts 图表区域（待接入）</div>
              <div style="font-size: 12px; margin-top: 8px">展示企业、职位、求职者的增长趋势</div>
            </div>
          </div>
          
          <!-- 简易表格展示趋势 -->
          <el-table :data="trendData" style="margin-top: 16px" :show-header="true" size="small">
            <el-table-column prop="date" label="日期" width="100" />
            <el-table-column prop="companies" label="新增企业" />
            <el-table-column prop="positions" label="新增职位" />
            <el-table-column prop="candidates" label="新增求职者" />
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="never">
          <template #header>
            <span style="font-weight: 600">⚠️ 运营预警</span>
          </template>
          
          <el-timeline>
            <el-timeline-item 
              v-for="(warning, index) in warnings" 
              :key="index"
              :type="warning.type === '高风险' ? 'danger' : warning.type === '中风险' ? 'warning' : 'info'"
              :timestamp="warning.time"
            >
              <el-tag :type="warning.type === '高风险' ? 'danger' : warning.type === '中风险' ? 'warning' : 'info'" size="small">
                {{ warning.type }}
              </el-tag>
              <div style="margin-top: 8px">{{ warning.title }}（{{ warning.count }}件）</div>
            </el-timeline-item>
          </el-timeline>
        </el-card>
        
        <el-card shadow="never" style="margin-top: 20px">
          <template #header>
            <span style="font-weight: 600">🎯 转化漏斗</span>
          </template>
          
          <div style="padding: 10px 0">
            <div v-for="(item, index) in funnelData" :key="index" style="margin-bottom: 12px">
              <div style="display: flex; justify-content: space-between; margin-bottom: 4px">
                <span style="font-size: 13px">{{ item.stage }}</span>
                <span style="font-size: 13px; color: #909399">{{ item.count.toLocaleString() }} ({{ item.rate }}%)</span>
              </div>
              <el-progress 
                :percentage="item.rate" 
                :color="index === 0 ? '#409EFF' : index === 1 ? '#67C23A' : index === 2 ? '#E6A23C' : index === 3 ? '#F56C6C' : '#909399'"
                :stroke-width="16"
                :show-text="false"
              />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 地域排名与行业分布 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>
            <span style="font-weight: 600">🌍 城市活力榜 Top10</span>
          </template>
          
          <el-table :data="regionRanking" style="width: 100%" size="small">
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
            <el-table-column prop="city" label="城市" width="100" />
            <el-table-column prop="companies" label="企业数" />
            <el-table-column prop="candidates" label="求职者数" />
            <el-table-column prop="change" label="周增长" width="100">
              <template #default="{ row }">
                <span style="color: #67C23A">{{ row.change }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="never">
          <template #header>
            <span style="font-weight: 600">🏢 行业分布</span>
          </template>
          
          <div style="padding: 10px 0">
            <div v-for="(item, index) in industryDistribution" :key="index" style="margin-bottom: 12px">
              <div style="display: flex; justify-content: space-between; margin-bottom: 4px">
                <span style="font-size: 13px">{{ item.industry }}</span>
                <span style="font-size: 13px; color: #909399">{{ item.count.toLocaleString() }} ({{ item.percentage }}%)</span>
              </div>
              <el-progress 
                :percentage="item.percentage" 
                :color="index === 0 ? '#409EFF' : index === 1 ? '#67C23A' : '#E6A23C'"
                :stroke-width="16"
                :show-text="false"
              />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.metric-row {
  margin-bottom: 20px;
}

.metric-card {
  border-radius: 12px;
  overflow: hidden;
}

.metric-content {
  display: flex;
  align-items: center;
}

.metric-icon {
  width: 60px;
  height: 60px;
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

.metric-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.metric-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  line-height: 1;
}

.metric-suffix {
  font-size: 14px;
  color: #909399;
  margin-left: 4px;
}

.metric-trend {
  display: flex;
  align-items: center;
  margin-top: 8px;
  font-size: 12px;
}

.metric-trend.up {
  color: #67C23A;
}

.metric-trend.down {
  color: #F56C6C;
}

:deep(.el-statistic__content) {
  font-size: 24px;
  font-weight: 600;
}
</style>
