<template>
  <div class="role-container">
    <div class="header">
      <h3>角色管理</h3>
      <el-button type="primary" @click="openAddModal">添加角色</el-button>
    </div>
    
    <el-table :data="roleList" border style="width: 100%">
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="name" label="角色名称"></el-table-column>
      
      <!-- <el-table-column prop="resources" label="资源数量">
        <template #default="scope">
          {{ scope.row.resources?.length || 0 }} 个
        </template>
      </el-table-column> -->
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="openEditModal(scope.row)">编辑</el-button>
          <el-button size="small" @click="openResourceModal(scope.row)">配置资源</el-button>
          <el-button size="small" type="danger" @click="deleteRole(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑角色弹窗 -->
    <el-dialog :title="isEdit ? '编辑角色' : '添加角色'" v-model="showModal">
      <el-form ref="roleForm" :model="form" label-width="80px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入角色名称"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="form.description" placeholder="请输入角色描述"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showModal = false">取消</el-button>
        <el-button type="primary" @click="saveRole">确定</el-button>
      </template>
    </el-dialog>

    <!-- 配置资源弹窗 -->
    <el-dialog title="配置资源" v-model="showResourceModal" width="600px">
      <div v-if="currentRole">
        <p>角色: {{ currentRole.name }}</p>
        <el-tree
          :data="resourceTree"
          show-checkbox
          node-key="id"
          :default-checked-keys="checkedResources"
          :props="treeProps"
          ref="resourceTreeRef"
        ></el-tree>
      </div>
      <template #footer>
        <el-button @click="showResourceModal = false">取消</el-button>
        <el-button type="primary" @click="saveResourceConfig">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref,onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

// 角色列表
const roleList = ref([])
// [
//   { id: 1, name: '超级管理员', description: '拥有所有权限', resources: [1, 2, 3, 4, 5] },
//   { id: 2, name: '普通用户', description: '基础操作权限', resources: [1, 2] },
//   { id: 3, name: '编辑', description: '内容编辑权限', resources: [1, 2, 3] },
//   { id: 4, name: '审核员', description: '审核权限', resources: [1, 4] }
// ])

const getrolelist = () => { 
  request.get('/users/roles').then(res => {
    roleList.value = res.data.rolelist
  })
}

onMounted(() => {
  getrolelist()
})

// 资源树
const resourceTree = ref([
  {
    id: 1,
    label: '用户管理',
   
  },
  {
    id: 2,
    label: '角色管理',
   
  },
  {
    id: 3,
    label: '资源管理',
   
  },
  {
    id: 4,
    label: '内容管理',
    
  }
])

const treeProps = {
  children: 'children',
  label: 'label'
}

const showModal = ref(false)
const showResourceModal = ref(false)
const isEdit = ref(false)
const currentRole = ref(null)
const checkedResources = ref([])
const resourceTreeRef = ref(null)

const form = ref({
  id: null,
  name: '',
  description: ''
})

const openAddModal = () => {
  isEdit.value = false
  form.value = { id: null, name: '', description: '' }
  showModal.value = true
}

const openEditModal = (row) => {
  isEdit.value = true
  form.value = { id: row.id, name: row.name, description: row.description }
  showModal.value = true
}

const saveRole = () => {
  if (!form.value.name) {
    ElMessage.error('请输入角色名称')
    return
  }

  if (isEdit.value) {
    const index = roleList.value.findIndex(r => r.id === form.value.id)
    if (index > -1) {
      roleList.value[index] = { ...roleList.value[index], ...form.value }
      ElMessage.success('编辑成功')
    }
  } else {
    request.post('/users/roles',form.value).then(res => {

       roleList.value.push({
      id: Date.now(),
      name: form.value.name,
      description: form.value.description,
      resources: []
    })
    ElMessage.success('添加成功')
      
    })
   
  }
  showModal.value = false
}

const openResourceModal = (row) => {
  currentRole.value = row
  checkedResources.value = [...(row.resources || [])]
  showResourceModal.value = true
}

const saveResourceConfig = () => {
  if (currentRole.value) {
    const checkedKeys = resourceTreeRef.value.getCheckedKeys()
    alert(checkedKeys)
    const roleIndex = roleList.value.findIndex(r => r.id === currentRole.value.id)
    if (roleIndex > -1) {
      roleList.value[roleIndex].resources = checkedKeys
      ElMessage.success('配置成功')
    }
  }
  showResourceModal.value = false
}

const deleteRole = (id) => {
  roleList.value = roleList.value.filter(r => r.id !== id)
  ElMessage.success('删除成功')
}
</script>

<style scoped>
.role-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
