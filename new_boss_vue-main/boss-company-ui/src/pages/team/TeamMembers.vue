<script setup>
import { reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Edit, Delete, User } from '@element-plus/icons-vue'

const query = reactive({
  keyword: '',
  role: '',
  status: ''
})

const teamMembers = ref([
  { 
    id: 1, 
    name: '张经理', 
    avatar: '', 
    phone: '138****0001', 
    email: 'zhang***@example.com',
    role: '超级管理员', 
    department: '人事部',
    status: '正常',
    joinDate: '2025-01-15',
    lastLogin: '2026-03-31 09:30',
    positions: 12,
    communicates: 156
  },
  { 
    id: 2, 
    name: '李 HR', 
    avatar: '', 
    phone: '139****0002', 
    email: 'li***@example.com',
    role: 'HR 经理', 
    department: '人事部',
    status: '正常',
    joinDate: '2025-03-20',
    lastLogin: '2026-03-31 08:45',
    positions: 8,
    communicates: 89
  },
  { 
    id: 3, 
    name: '王招聘', 
    avatar: '', 
    phone: '137****0003', 
    email: 'wang***@example.com',
    role: '招聘专员', 
    department: '人事部',
    status: '正常',
    joinDate: '2025-06-10',
    lastLogin: '2026-03-30 17:20',
    positions: 5,
    communicates: 45
  },
  { 
    id: 4, 
    name: '赵实习', 
    avatar: '', 
    phone: '136****0004', 
    email: 'zhao***@example.com',
    role: '实习 HR', 
    department: '人事部',
    status: '已禁用',
    joinDate: '2025-09-01',
    lastLogin: '2026-03-25 10:15',
    positions: 2,
    communicates: 12
  }
])

const roles = [
  { label: '超级管理员', value: '超级管理员', desc: '拥有所有权限，可管理团队和账号' },
  { label: 'HR 经理', value: 'HR 经理', desc: '可发布职位、查看简历、安排面试' },
  { label: '招聘专员', value: '招聘专员', desc: '可发布职位、沟通候选人' },
  { label: '实习 HR', value: '实习 HR', desc: '仅可查看简历和沟通' }
]

const showInviteDialog = ref(false)
const inviteForm = reactive({
  name: '',
  phone: '',
  email: '',
  role: '',
  department: ''
})

const onSearch = () => {
  ElMessage.success('查询成功')
}

const onInvite = () => {
  showInviteDialog.value = true
}

const onSubmitInvite = async () => {
  // TODO: 对接邀请接口
  ElMessage.success('邀请已发送')
  showInviteDialog.value = false
}

const onEdit = (member) => {
  ElMessage.success('编辑成员：' + member.name)
}

const onDisable = async (member) => {
  try {
    await ElMessageBox.confirm(
      `确定要${member.status === '正常' ? '禁用' : '启用'}该账号吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    member.status = member.status === '正常' ? '已禁用' : '正常'
    ElMessage.success('操作成功')
  } catch {
    // 取消操作
  }
}

const onDelete = async (member) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除成员"${member.name}"吗？此操作不可恢复。`,
      '删除成员',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error'
      }
    )
    const index = teamMembers.value.findIndex(item => item.id === member.id)
    if (index !== -1) {
      teamMembers.value.splice(index, 1)
    }
    ElMessage.success('成员已删除')
  } catch {
    // 取消操作
  }
}

const getStatusType = (status) => {
  return status === '正常' ? 'success' : 'danger'
}
</script>

<template>
  <div class="team-container">
    <!-- 头部 -->
    <el-card shadow="never" class="header-card">
      <div class="header-content">
        <div class="header-left">
          <h3>团队管理</h3>
          <p class="header-desc">管理企业招聘团队成员和权限</p>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="onInvite">
            <el-icon><Plus /></el-icon>
            邀请成员
          </el-button>
        </div>
      </div>
    </el-card>
    
    <!-- 筛选区 -->
    <el-card shadow="never" class="filter-card">
      <el-form :inline="true" :model="query" class="filter-form">
        <el-form-item label="关键字">
          <el-input 
            v-model="query.keyword" 
            placeholder="姓名/手机号/邮箱" 
            style="width: 240px"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="query.role" placeholder="全部" style="width: 160px" clearable>
            <el-option v-for="role in roles" :key="role.value" :label="role.label" :value="role.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="query.status" placeholder="全部" style="width: 140px" clearable>
            <el-option label="正常" value="正常" />
            <el-option label="已禁用" value="已禁用" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSearch">查询</el-button>
          <el-button @click="query = { keyword: '', role: '', status: '' }">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 成员列表 -->
    <el-card shadow="never" class="table-card">
      <div class="card-header">
        <span>团队成员</span>
        <div class="stats">
          <el-tag size="small" type="info">总人数：{{ teamMembers.length }}</el-tag>
          <el-tag size="small" type="success" style="margin-left: 8px">正常：{{ teamMembers.filter(m => m.status === '正常').length }}</el-tag>
          <el-tag size="small" type="danger" style="margin-left: 8px">已禁用：{{ teamMembers.filter(m => m.status === '已禁用').length }}</el-tag>
        </div>
      </div>
      
      <el-table :data="teamMembers" style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column label="成员信息" min-width="200">
          <template #default="{ row }">
            <div class="member-info">
              <el-avatar :size="40" :src="row.avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="info-detail">
                <div class="name">{{ row.name }}</div>
                <div class="contact">{{ row.phone }} · {{ row.email }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="role" label="角色" min-width="140">
          <template #default="{ row }">
            <div class="role-info">
              <div class="role-name">{{ row.role }}</div>
              <div class="role-dept">{{ row.department }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="工作数据" width="200">
          <template #default="{ row }">
            <div class="work-stats">
              <span class="stat-item">在招 {{ row.positions }} 个</span>
              <span class="stat-item">沟通 {{ row.communicates }} 次</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="lastLogin" label="最后登录" width="160" />
        <el-table-column label="操作" width="260" fixed="right">
          <template #default="{ row }">
            <el-button text type="primary" size="small" @click="onEdit(row)">编辑</el-button>
            <el-button 
              text 
              :type="row.status === '正常' ? 'warning' : 'success'" 
              size="small" 
              @click="onDisable(row)"
            >
              {{ row.status === '正常' ? '禁用' : '启用' }}
            </el-button>
            <el-button 
              v-if="row.role !== '超级管理员'" 
              text 
              type="danger" 
              size="small" 
              @click="onDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 邀请成员对话框 -->
    <el-dialog
      v-model="showInviteDialog"
      title="邀请成员加入团队"
      width="500px"
    >
      <el-form :model="inviteForm" label-width="80px">
        <el-form-item label="姓名" required>
          <el-input v-model="inviteForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="手机号" required>
          <el-input v-model="inviteForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="邮箱" required>
          <el-input v-model="inviteForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="角色" required>
          <el-select v-model="inviteForm.role" placeholder="请选择角色" style="width: 100%">
            <el-option v-for="role in roles" :key="role.value" :label="role.label" :value="role.value">
              <div class="role-option">
                <div>{{ role.label }}</div>
                <div class="option-desc">{{ role.desc }}</div>
              </div>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="部门">
          <el-input v-model="inviteForm.department" placeholder="请输入部门" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showInviteDialog = false">取消</el-button>
        <el-button type="primary" @click="onSubmitInvite">发送邀请</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.team-container {
  padding: 0;
}

.header-card {
  margin-bottom: 16px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left h3 {
  font-size: 20px;
  color: #303133;
  margin: 0 0 4px 0;
}

.header-desc {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.filter-card {
  margin-bottom: 16px;
}

.table-card {
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.stats {
  display: flex;
  gap: 8px;
}

.member-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.info-detail {
  flex: 1;
}

.name {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.contact {
  font-size: 12px;
  color: #909399;
}

.role-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.role-name {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.role-dept {
  font-size: 12px;
  color: #909399;
}

.work-stats {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  color: #606266;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.role-option {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.option-desc {
  font-size: 12px;
  color: #909399;
}
</style>
