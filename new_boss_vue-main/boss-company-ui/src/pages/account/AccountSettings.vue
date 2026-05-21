<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Phone, Message, Lock } from '@element-plus/icons-vue'

const userInfo = ref({
  name: '张经理',
  phone: '138****0001',
  email: 'zhang***@example.com',
  company: '示例科技有限公司',
  department: '人事部',
  position: 'HR 经理',
  avatar: ''
})

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const showPasswordDialog = ref(false)

const onSaveProfile = () => {
  ElMessage.success('个人信息保存成功')
}

const onChangePassword = () => {
  showPasswordDialog.value = true
}

const onSubmitPassword = () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  // TODO: 对接修改密码接口
  ElMessage.success('密码修改成功')
  showPasswordDialog.value = false
  passwordForm.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
}
</script>

<template>
  <div class="account-container">
    <el-row :gutter="20">
      <!-- 左侧个人信息卡片 -->
      <el-col :span="8">
        <el-card shadow="never" class="profile-card">
          <div class="profile-header">
            <el-avatar :size="80" :src="userInfo.avatar">
              <el-icon :size="40"><User /></el-icon>
            </el-avatar>
            <h3>{{ userInfo.name }}</h3>
            <p>{{ userInfo.position }}</p>
          </div>
          
          <el-divider />
          
          <div class="profile-info">
            <div class="info-item">
              <el-icon><User /></el-icon>
              <span>{{ userInfo.company }}</span>
            </div>
            <div class="info-item">
              <el-icon><User /></el-icon>
              <span>{{ userInfo.department }}</span>
            </div>
            <div class="info-item">
              <el-icon><Phone /></el-icon>
              <span>{{ userInfo.phone }}</span>
            </div>
            <div class="info-item">
              <el-icon><Message /></el-icon>
              <span>{{ userInfo.email }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 右侧表单 -->
      <el-col :span="16">
        <el-card shadow="never" class="form-card">
          <template #header>
            <div class="card-header">
              <span>个人信息</span>
              <el-button type="primary" size="small" @click="onSaveProfile">保存</el-button>
            </div>
          </template>
          
          <el-form :model="userInfo" label-width="100px">
            <el-form-item label="姓名">
              <el-input v-model="userInfo.name" placeholder="请输入姓名" />
            </el-form-item>
            
            <el-form-item label="手机号">
              <el-input v-model="userInfo.phone" placeholder="请输入手机号" disabled />
              <div class="form-tip">手机号已绑定，如需修改请联系管理员</div>
            </el-form-item>
            
            <el-form-item label="邮箱">
              <el-input v-model="userInfo.email" placeholder="请输入邮箱" />
            </el-form-item>
            
            <el-form-item label="公司">
              <el-input v-model="userInfo.company" disabled />
            </el-form-item>
            
            <el-form-item label="部门">
              <el-input v-model="userInfo.department" placeholder="请输入部门" />
            </el-form-item>
            
            <el-form-item label="职位">
              <el-input v-model="userInfo.position" placeholder="请输入职位" />
            </el-form-item>
          </el-form>
        </el-card>
        
        <el-card shadow="never" class="security-card" style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <span>账号安全</span>
              <el-button type="primary" size="small" @click="onChangePassword">
                <el-icon><Lock /></el-icon>
                修改密码
              </el-button>
            </div>
          </template>
          
          <div class="security-items">
            <div class="security-item">
              <div class="item-label">登录密码</div>
              <div class="item-value">••••••••</div>
              <el-button text type="primary" @click="onChangePassword">修改</el-button>
            </div>
            
            <div class="security-item">
              <div class="item-label">手机验证</div>
              <div class="item-value">{{ userInfo.phone }}</div>
              <el-tag size="small" type="success">已绑定</el-tag>
            </div>
            
            <div class="security-item">
              <div class="item-label">邮箱验证</div>
              <div class="item-value">{{ userInfo.email }}</div>
              <el-tag size="small" type="success">已绑定</el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="showPasswordDialog"
      title="修改登录密码"
      width="450px"
    >
      <el-form :model="passwordForm" label-width="100px">
        <el-form-item label="当前密码" required>
          <el-input 
            v-model="passwordForm.oldPassword" 
            type="password" 
            placeholder="请输入当前密码"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="新密码" required>
          <el-input 
            v-model="passwordForm.newPassword" 
            type="password" 
            placeholder="请输入新密码 (6-20 位)"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="确认密码" required>
          <el-input 
            v-model="passwordForm.confirmPassword" 
            type="password" 
            placeholder="请再次输入新密码"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" @click="onSubmitPassword">确认修改</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.account-container {
  padding: 0;
}

.profile-card {
  margin-bottom: 20px;
}

.profile-header {
  text-align: center;
  padding: 20px 0;
}

.profile-header h3 {
  font-size: 18px;
  color: #303133;
  margin: 16px 0 4px 0;
}

.profile-header p {
  font-size: 14px;
  color: #909399;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 8px 0;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: #606266;
}

.info-item .el-icon {
  width: 20px;
  color: #909399;
}

.form-card, .security-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.security-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.security-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
}

.item-label {
  width: 100px;
  font-size: 14px;
  color: #909399;
}

.item-value {
  flex: 1;
  font-size: 14px;
  color: #303133;
}
</style>
