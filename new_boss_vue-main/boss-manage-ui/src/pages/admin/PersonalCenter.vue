<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import {
  User,
  Phone,
  Email,
  Lock,
  Calendar,
  Camera,
  Edit
} from '@element-plus/icons-vue'

const activeTab = ref('profile')

// 管理员信息
const adminInfo = reactive({
  id: 'admin001',
  username: 'zhangsan',
  realName: '张三',
  avatar: '',
  role: '超级管理员',
  email: 'zhangsan@boss.com',
  phone: '138****0001',
  department: '技术部',
  position: '系统管理员',
  gender: '男',
  birthday: '1990-01-01',
  createTime: '2025-01-01 00:00:00',
  lastLoginTime: '2026-03-31 09:00:00',
  loginCount: 1256,
})

// 编辑表单
const profileForm = reactive({
  realName: adminInfo.realName,
  email: adminInfo.email,
  phone: adminInfo.phone,
  gender: adminInfo.gender,
  department: adminInfo.department,
  position: adminInfo.position,
})

// 修改密码表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: '',
})

// 账号安全设置
const securitySettings = reactive({
  twoFactorAuth: false,
  emailVerified: true,
  phoneVerified: true,
  passwordStrength: '强',
  lastPasswordChange: '2026-01-15',
})

const handleAvatarUpload = (file: any) => {
  ElMessage.success(`头像 "${file.name}" 上传成功`)
}

const saveProfile = () => {
  Object.assign(adminInfo, profileForm)
  ElMessage.success('个人信息保存成功')
}

const validatePassword = () => {
  if (!passwordForm.oldPassword) {
    ElMessage.warning('请输入当前密码')
    return false
  }
  if (passwordForm.newPassword.length < 6) {
    ElMessage.warning('新密码长度不能少于 6 位')
    return false
  }
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    ElMessage.error('两次输入的新密码不一致')
    return false
  }
  return true
}

const changePassword = () => {
  if (!validatePassword()) return
  
  ElMessage.success('密码修改成功，请重新登录')
  // 清空表单
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
}

const bindPhone = () => {
  ElMessage.info('绑定手机功能待开发')
}

const bindEmail = () => {
  ElMessage.info('绑定邮箱功能待开发')
}

const toggleTwoFactor = () => {
  securitySettings.twoFactorAuth = !securitySettings.twoFactorAuth
  ElMessage.success(securitySettings.twoFactorAuth ? '已开启双因素认证' : '已关闭双因素认证')
}
</script>

<template>
  <div class="personal-center">
    <el-card shadow="never">
      <template #header>
        <span style="font-weight: 600">👤 个人中心</span>
      </template>
      
      <div style="display: flex; gap: 40px">
        <!-- 左侧：个人信息概览 -->
        <div style="width: 300px; text-align: center">
          <div style="position: relative; display: inline-block">
            <el-avatar :size="120" :src="adminInfo.avatar" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
              <el-icon :size="60"><User /></el-icon>
            </el-avatar>
            <el-button 
              type="primary" 
              size="small" 
              circle 
              style="position: absolute; bottom: 0; right: 0"
              @click="$refs.uploadInput?.click()"
            >
              <el-icon><Camera /></el-icon>
            </el-button>
            <input
              ref="uploadInput"
              type="file"
              accept="image/*"
              style="display: none"
              @change="handleAvatarUpload"
            />
          </div>
          
          <div style="margin-top: 16px">
            <div style="font-size: 20px; font-weight: 700">{{ adminInfo.realName }}</div>
            <div style="color: #909399; margin-top: 4px">{{ adminInfo.role }}</div>
            <div style="color: #606266; font-size: 14px; margin-top: 8px">
              {{ adminInfo.department }} · {{ adminInfo.position }}
            </div>
          </div>
          
          <el-divider />
          
          <div style="text-align: left; padding: 0 20px">
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px">
              <span style="color: #909399">账号</span>
              <span>{{ adminInfo.username }}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 12px">
              <span style="color: #909399">最后登录</span>
              <span>{{ adminInfo.lastLoginTime }}</span>
            </div>
            <div style="display: flex; justify-content: space-between">
              <span style="color: #909399">登录次数</span>
              <span>{{ adminInfo.loginCount }}次</span>
            </div>
          </div>
        </div>

        <!-- 右侧：选项卡内容 -->
        <div style="flex: 1">
          <el-tabs v-model="activeTab" type="border-card">
            <!-- 基本资料 -->
            <el-tab-pane label="基本资料" name="profile">
              <el-form :model="profileForm" label-width="100px" style="max-width: 500px">
                <el-form-item label="用户名">
                  <el-input :value="adminInfo.username" disabled />
                </el-form-item>
                
                <el-form-item label="真实姓名">
                  <el-input v-model="profileForm.realName" placeholder="请输入真实姓名" />
                </el-form-item>
                
                <el-form-item label="性别">
                  <el-radio-group v-model="profileForm.gender">
                    <el-radio label="男">男</el-radio>
                    <el-radio label="女">女</el-radio>
                  </el-radio-group>
                </el-form-item>
                
                <el-form-item label="出生日期">
                  <el-date-picker
                    v-model="profileForm.birthday"
                    type="date"
                    placeholder="选择出生日期"
                    style="width: 100%"
                    value-format="YYYY-MM-DD"
                  />
                </el-form-item>
                
                <el-form-item label="手机号码">
                  <el-input v-model="profileForm.phone" placeholder="请输入手机号码" />
                </el-form-item>
                
                <el-form-item label="电子邮箱">
                  <el-input v-model="profileForm.email" placeholder="请输入电子邮箱" />
                </el-form-item>
                
                <el-form-item label="所属部门">
                  <el-input v-model="profileForm.department" placeholder="请输入所属部门" />
                </el-form-item>
                
                <el-form-item label="职位">
                  <el-input v-model="profileForm.position" placeholder="请输入职位" />
                </el-form-item>
                
                <el-form-item>
                  <el-button type="primary" @click="saveProfile">保存修改</el-button>
                  <el-button @click="ElMessage.info('已取消')">取消</el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>

            <!-- 账号安全 -->
            <el-tab-pane label="账号安全" name="security">
              <el-card shadow="never" style="margin-bottom: 16px">
                <template #header>
                  <div style="display: flex; justify-content: space-between; align-items: center">
                    <span>登录密码</span>
                    <el-button type="primary" size="small" @click="$refs.passwordDialog?.show()">修改</el-button>
                  </div>
                </template>
                <div style="display: flex; justify-content: space-between">
                  <div>
                    <div style="font-weight: 600">当前密码强度：<span style="color: #67C23A">强</span></div>
                    <div style="color: #909399; font-size: 13px; margin-top: 4px">
                      上次修改时间：{{ securitySettings.lastPasswordChange }}
                    </div>
                  </div>
                </div>
              </el-card>

              <el-card shadow="never" style="margin-bottom: 16px">
                <template #header>
                  <div style="display: flex; justify-content: space-between; align-items: center">
                    <span>手机号码</span>
                    <el-button type="primary" size="small" @click="bindPhone">
                      {{ securitySettings.phoneVerified ? '更换' : '绑定' }}
                    </el-button>
                  </div>
                </template>
                <div>
                  <div style="font-weight: 600">{{ adminInfo.phone }}</div>
                  <div style="color: #909399; font-size: 13px; margin-top: 4px">
                    <el-tag type="success" size="small">已验证</el-tag>
                  </div>
                </div>
              </el-card>

              <el-card shadow="never" style="margin-bottom: 16px">
                <template #header>
                  <div style="display: flex; justify-content: space-between; align-items: center">
                    <span>电子邮箱</span>
                    <el-button type="primary" size="small" @click="bindEmail">
                      {{ securitySettings.emailVerified ? '更换' : '绑定' }}
                    </el-button>
                  </div>
                </template>
                <div>
                  <div style="font-weight: 600">{{ adminInfo.email }}</div>
                  <div style="color: #909399; font-size: 13px; margin-top: 4px">
                    <el-tag type="success" size="small">已验证</el-tag>
                  </div>
                </div>
              </el-card>

              <el-card shadow="never">
                <template #header>
                  <div style="display: flex; justify-content: space-between; align-items: center">
                    <span>双因素认证</span>
                    <el-switch
                      v-model="securitySettings.twoFactorAuth"
                      @change="toggleTwoFactor"
                    />
                  </div>
                </template>
                <div style="color: #909399; font-size: 13px">
                  开启后，登录时需要提供短信验证码或身份验证器验证码
                </div>
              </el-card>
            </el-tab-pane>

            <!-- 操作日志 -->
            <el-tab-pane label="操作日志" name="logs">
              <el-table :data="[]" style="width: 100%">
                <el-table-column prop="time" label="操作时间" width="180" />
                <el-table-column prop="action" label="操作行为" min-width="200" />
                <el-table-column prop="ip" label="IP 地址" width="160" />
                <el-table-column prop="location" label="登录地点" min-width="180" />
              </el-table>
              
              <div style="text-align: center; color: #909399; padding: 40px 0">
                暂无数据
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
    </el-card>

    <!-- 修改密码对话框 -->
    <el-dialog
      ref="passwordDialog"
      title="修改登录密码"
      width="400px"
      :close-on-click-modal="false"
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
            placeholder="请输入新密码"
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
        <el-button @click="$refs.passwordDialog?.close()">取消</el-button>
        <el-button type="primary" @click="changePassword">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.personal-center {
  padding: 20px;
}

:deep(.el-tabs__content) {
  padding: 20px;
}
</style>
