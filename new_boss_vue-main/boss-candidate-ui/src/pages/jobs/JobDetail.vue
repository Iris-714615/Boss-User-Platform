<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Location, Money, Briefcase, Share, Star, Clock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { formatSalary, formatTime } from 'shared-types'

const route = useRoute()
const router = useRouter()

// 使用统一的职位数据结构
const job = ref({
  id: route.params.id,
  title: '高级前端工程师',
  companyId: 'company_001',        // ✅ 添加企业 ID
  companyName: '示例科技有限公司',  // ✅ 添加企业名称
  salaryMin: 25,                   // ✅ 分字段存储
  salaryMax: 35,
  salaryMonth: 14,
  city: '上海',
  district: '浦东新区',
  address: '上海市浦东新区张江高科技园区',
  experience: '3-5 年',
  education: '本科',
  industry: '互联网/软件',
  scale: '100-500 人',
  stage: 'B 轮',
  description: `岗位职责：
1. 负责公司核心产品的前端架构设计和开发
2. 主导前端性能优化，提升用户体验
3. 搭建组件库，提高团队开发效率
4. 指导初级工程师，组织技术分享

任职要求：
1. 计算机相关专业本科及以上学历
2. 3-5 年前端开发经验
3. 精通 Vue.js/React 等主流框架
4. 熟悉 TypeScript、Webpack 等工具
5. 具备良好的团队协作和沟通能力`,
  welfare: ['五险一金', '带薪年假', '弹性工作', '周末双休', '年终奖', '股票期权', '定期体检', '零食下午茶'],
  tags: ['五险一金', '带薪年假', '弹性工作', '周末双休'],
  status: '已发布',
  publishedAt: Date.now() - 7200000, // 2 小时前
  views: 1256,
  communicates: 89,
  resumes: 34
})

// 计算属性：薪资显示
const salaryDisplay = computed(() => {
  return formatSalary(job.value.salaryMin, job.value.salaryMax, job.value.salaryMonth)
})

// 计算属性：发布时间
const publishTimeDisplay = computed(() => {
  return formatTime(job.value.publishedAt || Date.now())
})

const companyInfo = ref({
  id: 'company_001',           // ✅ 添加企业 ID
  name: '示例科技有限公司',
  industry: '互联网/软件',
  scale: '100-500 人',
  stage: 'B 轮',
  city: '上海',
  district: '浦东新区',
  address: '上海市浦东新区张江高科技园区',
  description: '示例科技是一家专注于企业服务的科技公司，致力于为企业提供高效的数字化解决方案。' 
})

const onApply = () => {
  ElMessageBox.confirm(
    '<p>确定要申请这个职位吗？</p><p style="color: #909399; font-size: 12px; margin-top: 8px;">申请后 HR 将看到您的简历和联系方式</p>',
    '申请职位',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '确认申请',
      cancelButtonText: '再想想',
      type: 'success'
    }
  ).then(() => {
    // 模拟投递请求
    setTimeout(() => {
      ElMessage.success('投递成功！HR 会尽快查看您的简历')
    }, 500)
  }).catch(() => {
    // 取消操作
  })
}

const onChat = () => {
  ElMessageBox.confirm(
    `<p>与 ${job.value.company} 的 HR 直接沟通？</p><p style="color: #909399; font-size: 12px; margin-top: 8px;">在线沟通可以让 HR 更了解您的意向</p>`,
    '立即沟通',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '开始聊天',
      cancelButtonText: '取消',
      type: 'info'
    }
  ).then(() => {
    router.push('/candidate/chat?hrId=1')
  }).catch(() => {
    // 取消操作
  })
}
</script>

<template>
  <div class="job-detail-container">
    <!-- 头部 -->
    <el-card shadow="never" class="header-card">
      <div class="header-content">
        <el-button text circle @click="router.back()">
          <el-icon><ArrowLeft /></el-icon>
        </el-button>
        <div class="header-info">
          <h1 class="job-title">{{ job.title }}</h1>
          <div class="job-salary">{{ salaryDisplay }}</div>
        </div>
        <div class="header-actions">
          <el-button circle text @click="ElMessage.info('分享功能开发中')">
            <el-icon><Share /></el-icon>
          </el-button>
          <el-button circle text @click="ElMessage.info('收藏成功')">
            <el-icon><Star /></el-icon>
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 职位基本信息 -->
    <el-card shadow="never" class="info-card" style="margin-top: 16px">
      <div class="tags-row">
        <el-tag size="large"><Location /> {{ job.city }}</el-tag>
        <el-tag size="large">{{ job.experience }}</el-tag>
        <el-tag size="large">{{ job.education }}</el-tag>
      </div>
      <div class="publish-info">
        <span class="time-label"><Clock /> 发布于 {{ publishTimeDisplay }}</span>
      </div>
    </el-card>

    <!-- 职位描述 -->
    <el-card shadow="never" class="desc-card" style="margin-top: 16px">
      <template #header>
        <div class="card-header">
          <span>📋 职位描述</span>
        </div>
      </template>
      <div class="desc-content" style="white-space: pre-wrap">{{ job.description }}</div>
    </el-card>

    <!-- 职位福利 -->
    <el-card shadow="never" class="welfare-card" style="margin-top: 16px">
      <template #header>
        <span>🎁 职位福利</span>
      </template>
      <div class="welfare-tags">
        <el-tag v-for="tag in job.welfare" :key="tag" size="large" effect="plain" round>
          {{ tag }}
        </el-tag>
      </div>
    </el-card>

    <!-- 公司信息 -->
    <el-card shadow="never" class="company-card" style="margin-top: 16px">
      <template #header>
        <span>🏢 公司信息</span>
      </template>
      <div class="company-name">{{ companyInfo.name }}</div>
      <div class="company-tags">
        <el-tag size="small" effect="plain">{{ companyInfo.industry }}</el-tag>
        <el-tag size="small" effect="plain">{{ companyInfo.scale }}</el-tag>
        <el-tag size="small" effect="plain">{{ companyInfo.stage }}</el-tag>
      </div>
      <div class="company-desc" style="margin-top: 12px; font-size: 14px; color: #606266">
        {{ companyInfo.description }}
      </div>
    </el-card>

    <!-- 工作地点 -->
    <el-card shadow="never" class="address-card" style="margin-top: 16px">
      <template #header>
        <span>📍 工作地点</span>
      </template>
      <div class="work-address">
        <el-icon><Location /></el-icon>
        {{ job.address }}
      </div>
    </el-card>

    <!-- 底部操作栏 -->
    <div class="bottom-bar">
      <el-button plain style="flex: 1" @click="onChat">
        立即沟通
      </el-button>
      <el-button type="primary" style="flex: 1" @click="onApply">
        立即申请
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.job-detail-container {
  padding-bottom: 80px;
}

.header-card {
  border-radius: 12px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-info {
  flex: 1;
}

.job-title {
  font-size: 18px;
  margin: 0 0 8px 0;
  color: #303133;
}

.job-salary {
  font-size: 22px;
  color: #f56c6c;
  font-weight: 600;
}

.tags-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.publish-info {
  font-size: 13px;
  color: #909399;
}

.time-label {
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-header {
  font-weight: 600;
}

.desc-content {
  font-size: 14px;
  line-height: 1.8;
  color: #606266;
}

.welfare-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.company-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #303133;
}

.company-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.company-desc {
  line-height: 1.6;
}

.work-address {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #606266;
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: white;
  display: flex;
  padding: 0 16px;
  gap: 12px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.08);
}
</style>
