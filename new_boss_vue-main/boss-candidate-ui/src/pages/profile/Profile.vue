<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User,
  Document,
  Clock,
  Star,
  Setting,
  Phone,
  Bell,
  Lock,
  Service,
  QuestionFilled,
  Monitor,
  Wallet,
  Ticket,
  VideoCamera,
  Reading,
  Camera,
  Briefcase,
  ArrowRight
} from '@element-plus/icons-vue'

const router = useRouter()

const userInfo = ref({
  name: '张先生',
  phone: '138****8888',
  avatar: '',
  resumeStatus: '完善中',
  resumeComplete: 65,
  expectedPosition: '前端工程师',
  expectedCity: '上海',
  expectedSalary: '20-30K'
})

const menuGroups = [
  {
    title: '求职相关',
    items: [
      { icon: Document, label: '我的简历', path: '/candidate/resume', badge: '' },
      { icon: Clock, label: '投递记录', path: '/candidate/delivery', badge: '3' },
      { icon: Star, label: '我的收藏', path: '/candidate/favorites', badge: '' },
      { icon: VideoCamera, label: '面试邀请', path: '', badge: '1' }
    ]
  },
  {
    title: '沟通与联系',
    items: [
      { icon: Phone, label: '谁看过我', path: '', badge: '' },
      { icon: Reading, label: '沟通过', path: '/candidate/chat', badge: '' },
      { icon: Bell, label: '消息通知', path: '', badge: '5' }
    ]
  },
  {
    title: '账户与安全',
    items: [
      { icon: Setting, label: '账号设置', path: '', badge: '' },
      { icon: User, label: '实名认证', path: '/candidate/realname-auth', badge: '' },
      { icon: Lock, label: '隐私设置', path: '', badge: '' },
      { icon: Wallet, label: '钱包余额', path: '', badge: '¥0.00' }
    ]
  },
  {
    title: '其他服务',
    items: [
      { icon: Ticket, label: '优惠券', path: '', badge: '2' },
      { icon: Monitor, label: '在线竞争力', path: '', badge: '' },
      { icon: QuestionFilled, label: '帮助中心', path: '', badge: '' },
      { icon: Service, label: '联系客服', path: '', badge: '' }
    ]
  }
]

const handleCommand = (command) => {
  console.log('处理命令:', command)
  if (command === 'logout') {
    logout()
  } else if (command === 'resume') {
    router.push('/candidate/resume')
  } else if (command === 'profile') {
    ElMessage.info('账号设置功能开发中')
  }
}

const logout = async () => {
  try {
    await ElMessageBox.confirm(
      '<p>确定要退出登录吗？</p><p style="color: #909399; font-size: 12px; margin-top: 8px;">退出后需要重新登录才能使用全部功能</p>',
      '提示',
      {
        dangerouslyUseHTMLString: true,
        confirmButtonText: '确定退出',
        cancelButtonText: '取消',
        type: 'warning',
        showClose: true,
        closeOnClickModal: false
      }
    )
    
    // 模拟退出请求
    await new Promise(resolve => setTimeout(resolve, 500))
    
    localStorage.removeItem('candidateToken')
    localStorage.removeItem('candidateInfo')
    
    ElMessage({
      message: '已安全退出登录',
      type: 'success',
      duration: 2000
    })
    
    // 延迟跳转到登录页
    setTimeout(() => {
      router.replace('/login')
    }, 500)
  } catch {
    ElMessage.info('已取消退出')
  }
}
</script>

<template>
  <div class="profile-container">
    <!-- 个人信息卡片 -->
    <el-card shadow="never" class="user-card">
      <div class="user-header">
        <div class="avatar-section">
          <el-avatar :size="72" :src="userInfo.avatar">
            <el-icon :size="36"><User /></el-icon>
          </el-avatar>
          <el-badge is-dot class="edit-badge">
            <el-button circle text size="small" class="edit-avatar-btn">
              <el-icon><Camera /></el-icon>
            </el-button>
          </el-badge>
        </div>
        
        <div class="user-info">
          <h2 class="user-name">{{ userInfo.name }}</h2>
          <p class="user-phone">{{ userInfo.phone }}</p>
          <div class="resume-status">
            <span class="status-text">简历完善度 {{ userInfo.resumeComplete }}%</span>
            <el-progress 
              :percentage="userInfo.resumeComplete" 
              :stroke-width="4"
              :show-text="false"
              status="success"
            />
          </div>
        </div>
      </div>
      
      <!-- 求职期望 -->
      <div class="expectation-section">
        <div class="section-title">
          <el-icon><Briefcase /></el-icon>
          <span>求职期望</span>
          <el-button text size="small" style="margin-left: auto" @click="ElMessage.info('编辑期望')">
            编辑
          </el-button>
        </div>
        <div class="expectation-tags">
          <el-tag size="small" effect="plain">{{ userInfo.expectedPosition }}</el-tag>
          <el-tag size="small" effect="plain">{{ userInfo.expectedCity }}</el-tag>
          <el-tag size="small" effect="plain">{{ userInfo.expectedSalary }}</el-tag>
        </div>
      </div>
    </el-card>

    <!-- 功能菜单 -->
    <div class="menu-section" style="margin-top: 16px">
      <div v-for="group in menuGroups" :key="group.title" class="menu-group">
        <div class="group-title">{{ group.title }}</div>
        <el-card shadow="never" class="menu-card">
          <div
            v-for="item in group.items"
            :key="item.label"
            class="menu-item"
            @click="item.path ? router.push(item.path) : ElMessage.info(item.label + '开发中')"
          >
            <div class="menu-left">
              <div class="menu-icon">
                <el-icon :size="20"><component :is="item.icon" /></el-icon>
              </div>
              <span class="menu-label">{{ item.label }}</span>
            </div>
            <div class="menu-right">
              <el-tag v-if="item.badge" size="small" effect="dark" type="danger">
                {{ item.badge }}
              </el-tag>
              <el-icon class="arrow-icon"><ArrowRight /></el-icon>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 退出登录按钮 -->
    <div class="logout-section" style="margin-top: 24px; margin-bottom: 40px">
      <el-button plain style="width: 100%" @click="handleCommand('logout')">
        退出登录
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  padding-bottom: 20px;
}

.user-card {
  border-radius: 12px;
}

.user-header {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.avatar-section {
  position: relative;
  flex-shrink: 0;
}

.edit-badge {
  position: absolute;
  bottom: 0;
  right: 0;
}

.edit-avatar-btn {
  background: rgba(255, 255, 255, 0.9);
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 4px 0;
}

.user-phone {
  font-size: 14px;
  color: #909399;
  margin: 0 0 12px 0;
}

.resume-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-text {
  font-size: 12px;
  color: #606266;
  min-width: 80px;
}

.expectation-section {
  border-top: 1px solid #f0f0f0;
  padding-top: 16px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
}

.expectation-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.menu-section {
  padding-bottom: 20px;
}

.menu-group {
  margin-bottom: 16px;
}

.group-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
  padding-left: 4px;
}

.menu-card {
  border-radius: 12px;
  overflow: hidden;
}

.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  cursor: pointer;
  transition: all 0.3s;
  border-bottom: 1px solid #f5f7fa;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item:hover {
  background: #f5f7fa;
}

.menu-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.menu-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e6f2ff;
  border-radius: 8px;
  color: #0084ff;
}

.menu-label {
  font-size: 14px;
  color: #303133;
}

.menu-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.arrow-icon {
  color: #c0c4cc;
}

.logout-section {
  padding: 0 16px;
}
</style>
