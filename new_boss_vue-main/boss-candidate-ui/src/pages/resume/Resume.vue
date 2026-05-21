<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Edit, Upload, Plus, Document, User, Briefcase, Reading, Medal } from '@element-plus/icons-vue'

const resumeData = ref({
  name: '张先生',
  age: 28,
  phone: '138****8888',
  email: 'zhang***@example.com',
  workExperience: '5 年',
  education: '本科',
  expectedPosition: '前端工程师',
  expectedCity: '上海',
  expectedSalary: '20-30K',
  completeRate: 65
})

const sections = [
  { 
    title: '基本信息', 
    icon: User, 
    items: ['姓名', '年龄', '联系方式'], 
    complete: true 
  },
  { 
    title: '工作经历', 
    icon: Briefcase, 
    items: ['最近一份工作未填写'], 
    complete: false 
  },
  { 
    title: '教育经历', 
    icon: Reading, 
    items: ['本科 - 计算机科学与技术'], 
    complete: true 
  },
  { 
    title: '项目经验', 
    icon: Document, 
    items: ['暂无项目经验'], 
    complete: false 
  },
  { 
    title: '技能特长', 
    icon: Medal, 
    items: ['Vue.js', 'React', 'TypeScript'], 
    complete: true 
  }
]

const handleEdit = (section) => {
  ElMessageBox.confirm(`确定要编辑${section}吗？`, '提示', {
    confirmButtonText: '编辑',
    cancelButtonText: '取消',
    type: 'info'
  }).then(() => {
    ElMessage.info(`${section}编辑功能开发中`)
  }).catch(() => {
    // 取消操作
  })
}

const uploadResume = () => {
  ElMessageBox.confirm(
    '<p>支持 PDF、Word 格式，文件大小不超过 10MB</p><p style="color: #909399; font-size: 12px; margin-top: 8px;">上传后系统将自动解析简历内容</p>',
    '上传附件简历',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '选择文件',
      cancelButtonText: '取消',
      type: 'info'
    }
  ).then(() => {
    // 模拟文件选择
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = '.pdf,.doc,.docx'
    input.onchange = (e) => {
      const target = e.target
      const file = target.files?.[0]
      if (file) {
        ElMessage.success(`已选择文件：${file.name}`)
      }
    }
    input.click()
  }).catch(() => {
    // 取消操作
  })
}
</script>

<template>
  <div class="resume-container">
    <!-- 简历完成度卡片 -->
    <el-card shadow="never" class="resume-header">
      <div class="header-content">
        <div class="avatar-section">
          <el-avatar :size="64" :src="''">
            <el-icon :size="32"><User /></el-icon>
          </el-avatar>
          <el-badge is-dot class="camera-badge">
            <el-button circle text size="small" @click="ElMessage.info('更换头像')">
              <el-icon><Camera /></el-icon>
            </el-button>
          </el-badge>
        </div>
        
        <div class="info-section">
          <h2 class="name">{{ resumeData.name }}</h2>
          <p class="summary">
            {{ resumeData.workExperience }} · {{ resumeData.education }} · {{ resumeData.expectedPosition }}
          </p>
          <div class="expectation-tags">
            <el-tag size="small" effect="plain">{{ resumeData.expectedCity }}</el-tag>
            <el-tag size="small" effect="plain">{{ resumeData.expectedSalary }}</el-tag>
          </div>
        </div>
      </div>
      
      <!-- 完成度进度条 -->
      <div class="progress-section">
        <div class="progress-header">
          <span class="progress-label">简历完善度</span>
          <span class="progress-value">{{ resumeData.completeRate }}%</span>
        </div>
        <el-progress 
          :percentage="resumeData.completeRate" 
          :stroke-width="6"
          :show-text="false"
          status="success"
        />
        <p class="progress-tip">简历完整度越高，越容易获得面试机会哦！</p>
      </div>
    </el-card>

    <!-- 简历模块 -->
    <div class="sections-list" style="margin-top: 16px">
      <el-card
        v-for="(section, index) in sections"
        :key="index"
        shadow="hover"
        class="section-card"
      >
        <div class="section-header">
          <div class="section-title">
            <el-icon :size="20" color="#0084ff"><component :is="section.icon" /></el-icon>
            <span>{{ section.title }}</span>
          </div>
          <el-button text size="small" @click="handleEdit(section.title)">
            <el-icon><Edit /></el-icon>
            编辑
          </el-button>
        </div>
        
        <div class="section-content">
          <div
            v-for="(item, idx) in section.items"
            :key="idx"
            class="content-item"
            :class="{ incomplete: !section.complete }"
          >
            {{ item }}
          </div>
          <div v-if="section.items.length === 0" class="empty-tip">
            <el-empty description="暂无内容" :image-size="60" />
          </div>
        </div>
      </el-card>
    </div>

    <!-- 底部操作按钮 -->
    <div class="bottom-actions" style="margin-top: 24px">
      <el-button plain style="width: 100%" @click="uploadResume">
        <el-icon><Upload /></el-icon>
        上传附件简历
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.resume-container {
  padding-bottom: 20px;
}

.resume-header {
  border-radius: 12px;
}

.header-content {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}

.avatar-section {
  position: relative;
  flex-shrink: 0;
}

.camera-badge {
  position: absolute;
  bottom: 0;
  right: 0;
}

.info-section {
  flex: 1;
}

.name {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
}

.summary {
  font-size: 14px;
  color: #909399;
  margin: 0 0 12px 0;
}

.expectation-tags {
  display: flex;
  gap: 8px;
}

.progress-section {
  background: #f5f7fa;
  padding: 16px;
  border-radius: 8px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-label {
  font-size: 14px;
  color: #606266;
}

.progress-value {
  font-size: 18px;
  font-weight: 600;
  color: #67C23A;
}

.progress-tip {
  font-size: 12px;
  color: #909399;
  margin: 8px 0 0 0;
}

.sections-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-card {
  border-radius: 12px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.section-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.content-item {
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
  font-size: 14px;
  color: #606266;
}

.content-item.incomplete {
  color: #F56C6C;
  background: #fef0f0;
}

.empty-tip {
  padding: 8px 0;
}

.bottom-actions {
  padding: 0 16px;
}
</style>
