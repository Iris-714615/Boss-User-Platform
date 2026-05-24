<template>
  <div class="user-container">
    <div class="header">
      <h3>用户管理</h3>
      <el-button type="primary" @click="openAddModal">添加用户</el-button>
    </div>
    
    <el-table :data="userList" border style="width: 100%">
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="username" label="用户名"></el-table-column>
      <el-table-column prop="role_name" label="角色"></el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="openEditModal(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteUser(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑用户弹窗 -->
    <el-dialog :title="isEdit ? '编辑用户' : '添加用户'" v-model="showModal">
      <el-form ref="userForm" :model="form" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="form.password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色">
            <el-option v-for="role in roleList" :key="role.id" :label="role.name" :value="role.id"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showModal = false">取消</el-button>
        <el-button type="primary" @click="saveUser">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

// 用户列表
const userList = ref([])

// 角色列表（用于选择）
const roleList = ref([])

// 获取用户列表
const getUserList = () => {
  request({
    url: '/user/users',
    method: 'get'
  }).then(res => {
    console.log('用户列表:', res)
    if (res && res.code === 200) {
      userList.value = res.data
    }
  }).catch(err => {
    ElMessage.error('获取用户列表失败')
  })
}

// 获取角色列表
const getRoleList = () => {
  request({
    url: '/user/roles',
    method: 'get'
  }).then(res => {
    console.log('角色列表:', res)
    if (res && res.code === 200) {
      roleList.value = res.data
    }
  }).catch(err => {
    ElMessage.error('获取角色列表失败')
  })
}

// 弹窗状态
const showModal = ref(false)
const isEdit = ref(false)
const form = ref({
  id: null,
  username: '',
  password: '',
  role: null
})

// 初始化
onMounted(() => {
  getUserList()
  getRoleList()
})

// 打开添加弹窗
const openAddModal = () => {
  isEdit.value = false
  form.value = { id: null, username: '', password: '', role: null }
  showModal.value = true
}

// 打开编辑弹窗
const openEditModal = (row) => {
  isEdit.value = true
  form.value = {
    id: row.id,
    username: row.username,
    password: '',
    role: row.role
  }
  showModal.value = true
}

const saveUser = () => {
  if (!form.value.username) {
    ElMessage.error('请输入用户名')
    return
  }
  
  if (!isEdit.value && !form.value.password) {
    ElMessage.error('请输入密码')
    return
  }

  if (!form.value.role) {
    ElMessage.error('请选择角色')
    return
  }

  if (isEdit.value) {
    // 编辑用户
    const editData = {
      username: form.value.username,
      role: form.value.role
    }
    if (form.value.password) {
      editData.password = form.value.password
    }
    
    request({
      url: `/user/users/${form.value.id}`,
      method: 'put',
      data: editData
    }).then(res => {
      if (res && res.code === 200) {
        ElMessage.success('编辑成功')
        getUserList()
      } else {
        ElMessage.error(res?.msg || '编辑失败')
      }
    }).catch(err => {
      ElMessage.error('编辑失败，请稍后重试')
    })
  } else {
    // 添加用户
    request({
      url: '/user/users',
      method: 'post',
      data: {
        username: form.value.username,
        password: form.value.password,
        role: form.value.role
      }
    }).then(res => {
      if (res && res.code === 200) {
        ElMessage.success('添加成功')
        // 前端直接更新列表
        const newUser = {
          id: res.id || Date.now(),
          username: form.value.username,
          role: form.value.role,
          role_name: roleList.value.find(r => r.id === form.value.role)?.name || '未知'
        }
        userList.value.unshift(newUser)
      } else {
        ElMessage.error(res?.msg || '添加失败')
      }
    }).catch(err => {
      ElMessage.error('添加失败，请稍后重试')
    })
  }
  showModal.value = false
}

// 删除用户
const deleteUser = (row) => {
  request({
    url: `/user/users/${row.id}`,
    method: 'delete'
  }).then(res => {
    if (res && res.code === 200) {
      userList.value = userList.value.filter(u => u.id !== row.id)
      ElMessage.success('删除成功')
    } else {
      ElMessage.error(res?.msg || '删除失败')
    }
  }).catch(err => {
    ElMessage.error('删除失败，请稍后重试')
  })
}
</script>

<style scoped>
.user-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.role-tag {
  background: #e6f7ff;
  color: #1890ff;
  padding: 2px 8px;
  border-radius: 4px;
  margin-right: 4px;
  font-size: 12px;
}
</style>
