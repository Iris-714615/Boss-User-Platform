<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Briefcase, Location, Money, Clock, ChatDotRound, Check, Close } from '@element-plus/icons-vue'
import { DeliveryStatus, formatTime, formatSalary } from 'shared-types'

const router = useRouter()

// 使用统一的投递记录数据结构
const deliveryList = ref([
  {
    id: 'delivery_001',
    jobId: 'position_001',
    companyId: 'company_001',
    positionTitle: '高级前端工程师',
    companyName: '示例科技有限公司',
    industry: '互联网/软件',
    scale: '100-500 人',
    city: '上海',
    district: '浦东新区',
    salaryMin: 25,
    salaryMax: 35,
    salaryMonth: 14,
    status: DeliveryStatus.VIEWED,
    deliverTime: 1711900800000,
    feedback: ''
  },
  {
    id: 'delivery_002',
    jobId: 'position_002',
    companyId: 'company_002',
    positionTitle: '前端开发工程师',
    companyName: '某某信息科技公司',
    industry: '互联网/电商',
    scale: '500-1000 人',
    city: '北京',
    district: '朝阳区',
    salaryMin: 18,
    salaryMax: 25,
    salaryMonth: 12,
    status: DeliveryStatus.INTERESTED,
    deliverTime: 1711814400000,
    feedback: '简历与岗位匹配度较高，安排面试'
  },
  {
    id: 'delivery_003',
    jobId: 'position_003',
    companyId: 'company_003',
    positionTitle: 'Web 开发工程师',
    companyName: '演示企业',
    industry: '企业服务',
    scale: '50-100 人',
    city: '深圳',
    district: '南山区',
    salaryMin: 15,
    salaryMax: 20,
    salaryMonth: 12,
    status: DeliveryStatus.NOT_INTERESTED,
    deliverTime: 1711720800000,
    feedback: '暂不匹配，感谢关注'
  }
])

const getStatusText = (status) => {
  const statusMap = {
    [DeliveryStatus.APPLIED]: '已投递',
    [DeliveryStatus.VIEWED]: '已被查看',
    [DeliveryStatus.INTERESTED]: '感兴趣',
    [DeliveryStatus.NOT_INTERESTED]: '不合适',
    [DeliveryStatus.INTERVIEW]: '待面试',
    [DeliveryStatus.OFFER]: '已发 Offer',
    [DeliveryStatus.ACCEPTED]: '已接受'
  }
  return statusMap[status] || status
}

const getStatusType = (status) => {
  const typeMap = {
    [DeliveryStatus.APPLIED]: 'info',
    [DeliveryStatus.VIEWED]: 'primary',
    [DeliveryStatus.INTERESTED]: 'success',
    [DeliveryStatus.NOT_INTERESTED]: 'danger',
    [DeliveryStatus.INTERVIEW]: 'warning',
    [DeliveryStatus.OFFER]: 'success',
    [DeliveryStatus.ACCEPTED]: 'success'
  }
  return typeMap[status] || 'info'
}

const onChat = (item) => {
  router.push(`/chat/window?hrId=hr001&jobId=${item.jobId}`)
}

const onViewDetail = (item) => {
  router.push(`/jobs/detail/${item.jobId}`)
}
</script>

<template>
  <div class="delivery-record-container">
    <el-card shadow="never" class="header-card">
      <h3>投递记录</h3>
      <p>查看您投递的所有职位及处理状态</p>
    </el-card>

    <div class="delivery-list">
      <el-card
        v-for="item in deliveryList"
        :key="item.id"
        shadow="hover"
        class="delivery-item"
      >
        <div class="item-header">
          <div class="position-info">
            <el-icon :size="20" color="#0084ff"><Briefcase /></el-icon>
            <span class="position-title">{{ item.positionTitle }}</span>
          </div>
          <el-tag :type="getStatusType(item.status)" size="small">
            {{ getStatusText(item.status) }}
          </el-tag>
        </div>

        <div class="item-content">
          <div class="company-row">
            <span class="label">公司名称：</span>
            <span class="value">{{ item.companyName }}</span>
          </div>
          <div class="row">
            <span class="label">行业规模：</span>
            <span class="value">{{ item.industry }} · {{ item.scale }}</span>
          </div>
          <div class="row">
            <span class="label">工作地点：</span>
            <span class="value">{{ item.city }}{{ item.district ? '·' + item.district : '' }}</span>
          </div>
          <div class="row">
            <span class="label">薪资范围：</span>
            <span class="value salary">{{ formatSalary(item.salaryMin, item.salaryMax, item.salaryMonth) }}</span>
          </div>
          <div class="row">
            <span class="label">投递时间：</span>
            <span class="value">{{ formatTime(item.deliverTime) }}</span>
          </div>
          <div v-if="item.feedback" class="feedback-row">
            <span class="label">企业反馈：</span>
            <span class="value feedback">{{ item.feedback }}</span>
          </div>
        </div>

        <div class="item-actions">
          <el-button text size="small" @click="onViewDetail(item)">
            <el-icon><Briefcase /></el-icon>
            查看职位
          </el-button>
          <el-button 
            v-if="item.status !== DeliveryStatus.NOT_INTERESTED" 
            text 
            size="small" 
            type="primary" 
            @click="onChat(item)"
          >
            <el-icon><ChatDotRound /></el-icon>
            立即沟通
          </el-button>
        </div>
      </el-card>
    </div>

    <el-empty v-if="deliveryList.length === 0" description="暂无投递记录" />
  </div>
</template>

<style scoped>
.delivery-record-container {
  padding-bottom: 20px;
}

.header-card {
  margin-bottom: 16px;
  border-radius: 12px;
}

.header-card h3 {
  font-size: 18px;
  color: #303133;
  margin: 0 0 4px 0;
}

.header-card p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.delivery-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.delivery-item {
  border-radius: 12px;
  transition: all 0.3s;
}

.delivery-item:hover {
  transform: translateY(-2px);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.position-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.position-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.item-content {
  background: #f5f7fa;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
}

.company-row {
  margin-bottom: 8px;
}

.row {
  display: flex;
  align-items: flex-start;
  margin-bottom: 6px;
  font-size: 14px;
  color: #606266;
}

.row:last-child {
  margin-bottom: 0;
}

.label {
  color: #909399;
  min-width: 80px;
  flex-shrink: 0;
}

.value {
  color: #606266;
}

.salary {
  color: #F56C6C;
  font-weight: 600;
}

.feedback {
  color: #E6A23C;
}

.feedback-row {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed #dcdfe6;
}

.item-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>