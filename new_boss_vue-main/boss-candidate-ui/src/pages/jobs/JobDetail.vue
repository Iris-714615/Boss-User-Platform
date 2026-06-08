<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Location, Money, Briefcase, Share, Star, Clock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { formatSalary, formatTime } from 'shared-types'
import request from '@/utils/request'

const route = useRoute()
const router = useRouter()

// 使用统一的职位数据结构
// 初始化 定义一下  -避免懒加载
const job = ref({'company':{},'publisher':{}})
const getJobDetail = () => {
  request.get('jobdetail/'+route.params.id).then(res => {
    if (res.code === 200) {
      job.value = res.data
    }
  })
}
onMounted(() => {
  getJobDetail()
  fetchReviews()
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

// 评价数据
const reviewDialogVisible = ref(false)
const reviewForm = ref({
  rating: 5,
  content: ''
})

// 当前职位对应的 HR id（从 job 中取 publisher.id，没有则默认 1）
const hrId = computed(() => job.value?.publisher?.id || 1)

// 评价列表（从后端拉取）
const reviews = ref([])
const reviewLoading = ref(false)

// 分页
const reviewPage = ref(1)
const reviewPageSize = ref(3)
const reviewTotal = ref(0)
const pagedReviews = computed(() => reviews.value)

// 拉取评价列表
const fetchReviews = async () => {
  reviewLoading.value = true
  try {
    const res = await request.get('/hrcomment', {
      params: {
        hrid: hrId.value,
        page: reviewPage.value,
        page_size: reviewPageSize.value
      }
    })
    if (res.code === 200) {
      reviews.value = res.data || []
      reviewTotal.value = res.total || 0
    }
  } catch (err) {
    console.error('拉取评价失败:', err)
    ElMessage.error('拉取评价失败')
  } finally {
    reviewLoading.value = false
  }
}

// 翻页
const onReviewPageChange = (page) => {
  reviewPage.value = page
  fetchReviews()
}

// 打开评价弹窗
const onOpenReview = () => {
  reviewForm.value = { rating: 5, content: '' }
  reviewDialogVisible.value = true
}

// 提交评价
const onSubmitReview = async () => {
  if (!reviewForm.value.content.trim()) {
    ElMessage.warning('请输入评价内容')
    return
  }
  try {
    const res = await request.post('/hrcomment', {
      hrid: hrId.value,
      rating: reviewForm.value.rating,
      content: reviewForm.value.content
    })
    if (res.code === 200) {
      ElMessage.success('评价成功，感谢您的反馈！')
      reviewDialogVisible.value = false
      reviewPage.value = 1
      await fetchReviews()
    } else {
      ElMessage.error(res.msg || '评价失败')
    }
  } catch (err) {
    console.error('提交评价失败:', err)
    ElMessage.error('提交评价失败')
  }
}

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
          <h1 class="job-title">{{ job.job_name }}</h1>
          <div class="job-salary">{{ job.salary_range }}</div>
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
        <el-tag size="large">{{ job.work_year }}</el-tag>
        <el-tag size="large">{{ job.education }}</el-tag>
      </div>
      <div class="publish-info">
        <span class="time-label"><Clock /> 发布于 {{ publishTimeDisplay.value }}</span>
      </div>
    </el-card>

    <!-- 职位描述 -->
    <el-card shadow="never" class="desc-card" style="margin-top: 16px">
      <template #header>
        <div class="card-header">
          <span>📋 职位描述</span>
        </div>
      </template>
      <div class="desc-content" style="white-space: pre-wrap">{{ job.job_desc }}</div>
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
      <div class="company-name">{{ job.company.name }}</div>
      <div class="company-tags">
        <el-tag size="small" effect="plain">{{ job.company.intro }}</el-tag>
        <el-tag size="small" effect="plain">{{ job.company.scale }}</el-tag>
        <!-- <el-tag size="small" effect="plain">{{ job.publisher.dept }}</el-tag> -->
      </div>
      <div class="company-desc" style="margin-top: 12px; font-size: 14px; color: #606266">
        {{ job.publisher.name }}
      </div>
    </el-card>

    <!-- HR 评价 -->
    <el-card shadow="never" class="review-card" style="margin-top: 16px">
      <template #header>
        <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
          <span>💬 HR 评价</span>
          <el-button type="primary" size="small" @click="onOpenReview">
            评价 HR
          </el-button>
        </div>
      </template>

      <div v-loading="reviewLoading" class="review-list" v-if="pagedReviews.length">
        <div v-for="item in pagedReviews" :key="item._id || item.id" class="review-item">
          <div class="review-header">
            <span class="reviewer">{{ item.username || '匿名' }}</span>
            <el-rate
              :model-value="item.rating || 5"
              disabled
              show-score
              :score-template="`${item.rating || 5} 分`"
              size="small"
            />
            <span class="review-time">{{ (item.time || '').slice(0, 10) }}</span>
          </div>
          <div class="review-content">{{ item.content }}</div>
        </div>
      </div>
      <el-empty v-else description="暂无评价，来抢沙发吧～" />

      <div class="review-pagination" v-if="reviewTotal > reviewPageSize">
        <el-pagination
          v-model:current-page="reviewPage"
          :total="reviewTotal"
          :page-size="reviewPageSize"
          layout="total, prev, pager, next, jumper"
          background
          @current-change="onReviewPageChange"
        />
      </div>
    </el-card>

    <!-- 工作地点 -->
    <el-card shadow="never" class="address-card" style="margin-top: 16px">
      <template #header>
        <span>📍 工作地点</span>
      </template>
      <div class="work-address">
        <el-icon><Location /></el-icon>
        {{ job.company.address }}
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

    <!-- 评价弹窗 -->
    <el-dialog
      v-model="reviewDialogVisible"
      title="评价 HR"
      width="480px"
      :close-on-click-modal="false"
    >
      <div class="review-dialog">
        <div class="form-row">
          <span class="form-label">评分：</span>
          <el-rate v-model="reviewForm.rating" show-text />
        </div>
        <div class="form-row" style="margin-top: 16px;">
          <span class="form-label">评价内容：</span>
          <el-input
            v-model="reviewForm.content"
            type="textarea"
            :rows="4"
            maxlength="200"
            show-word-limit
            placeholder="请输入您对 HR 的评价..."
          />
        </div>
      </div>
      <template #footer>
        <el-button @click="reviewDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="onSubmitReview">提交评价</el-button>
      </template>
    </el-dialog>
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

/* 评价列表 */
.review-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.review-item {
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
}

.review-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.reviewer {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.review-time {
  font-size: 12px;
  color: #909399;
  margin-left: auto;
}

.review-content {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
}

.review-pagination {
  margin-top: 16px;
  display: flex;
  justify-content: center;
}

.review-dialog .form-row {
  display: flex;
  align-items: flex-start;
}

.review-dialog .form-label {
  width: 80px;
  font-size: 14px;
  color: #303133;
  line-height: 32px;
}
</style>
