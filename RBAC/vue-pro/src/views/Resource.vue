<template>
  <div class="resource-container">
    <div class="header">
      <h3>资源管理</h3>
      <el-button type="primary" @click="openAddModal">添加资源</el-button>
    </div>
    
    <el-table :data="resourceList" border style="width: 100%">
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="name" label="资源名称"></el-table-column>
      <el-table-column prop="code" label="资源标识"></el-table-column>
      <el-table-column prop="parentName" label="父资源">
        <template #default="scope">
          {{ scope.row.parentName || '无' }}
        </template>
      </el-table-column>
      <el-table-column prop="type" label="类型">
        <template #default="scope">
          <el-tag :type="scope.row.type === 'menu' ? 'primary' : 'success'">
            {{ scope.row.type === 'menu' ? '菜单' : '按钮' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="path" label="路径"></el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="openEditModal(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteResource(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑资源弹窗 -->
    <el-dialog :title="isEdit ? '编辑资源' : '添加资源'" v-model="showModal">
      <el-form ref="resourceForm" :model="form" label-width="100px">
        <el-form-item label="资源名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入资源名称"></el-input>
        </el-form-item>
        <el-form-item label="资源标识" prop="code">
          <el-input v-model="form.code" placeholder="请输入资源标识（英文）"></el-input>
        </el-form-item>
        <el-form-item label="父资源" prop="parentId">
          <el-select v-model="form.parentId" placeholder="请选择父资源">
            <el-option :value="null" label="无（顶级资源）"></el-option>
            <el-option v-for="res in parentOptions" :key="res.id" :label="res.name" :value="res.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择类型">
            <el-option value="menu" label="菜单"></el-option>
            <el-option value="button" label="按钮"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="路径" prop="path">
          <el-input v-model="form.path" placeholder="请输入资源路径（如 /user/list）"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showModal = false">取消</el-button>
        <el-button type="primary" @click="saveResource">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

// 资源列表
const resourceList = ref([
  { id: 1, name: '用户管理', code: 'user_manage', parentId: null, type: 'menu', path: '/user', parentName: '' },
  { id: 11, name: '查看用户', code: 'user_view', parentId: 1, type: 'button', path: '/user/list', parentName: '用户管理' },
  { id: 12, name: '添加用户', code: 'user_add', parentId: 1, type: 'button', path: '/user/add', parentName: '用户管理' },
  { id: 13, name: '编辑用户', code: 'user_edit', parentId: 1, type: 'button', path: '/user/edit', parentName: '用户管理' },
  { id: 2, name: '角色管理', code: 'role_manage', parentId: null, type: 'menu', path: '/role', parentName: '' },
  { id: 21, name: '查看角色', code: 'role_view', parentId: 2, type: 'button', path: '/role/list', parentName: '角色管理' },
  { id: 22, name: '添加角色', code: 'role_add', parentId: 2, type: 'button', path: '/role/add', parentName: '角色管理' },
  { id: 3, name: '资源管理', code: 'resource_manage', parentId: null, type: 'menu', path: '/resource', parentName: '' },
  { id: 31, name: '查看资源', code: 'resource_view', parentId: 3, type: 'button', path: '/resource/list', parentName: '资源管理' },
  { id: 4, name: '内容管理', code: 'content_manage', parentId: null, type: 'menu', path: '/content', parentName: '' },
  { id: 41, name: '发布内容', code: 'content_add', parentId: 4, type: 'button', path: '/content/add', parentName: '内容管理' },
  { id: 42, name: '审核内容', code: 'content_audit', parentId: 4, type: 'button', path: '/content/audit', parentName: '内容管理' }
])

const showModal = ref(false)
const isEdit = ref(false)
const form = ref({
  id: null,
  name: '',
  code: '',
  parentId: null,
  type: 'menu',
  path: ''
})

// 父资源选项（仅显示菜单类型）
const parentOptions = computed(() => {
  return resourceList.value.filter(r => r.type === 'menu')
})

const openAddModal = () => {
  isEdit.value = false
  form.value = { id: null, name: '', code: '', parentId: null, type: 'menu', path: '' }
  showModal.value = true
}

const openEditModal = (row) => {
  isEdit.value = true
  form.value = {
    id: row.id,
    name: row.name,
    code: row.code,
    parentId: row.parentId,
    type: row.type,
    path: row.path
  }
  showModal.value = true
}

const saveResource = () => {
  if (!form.value.name) {
    ElMessage.error('请输入资源名称')
    return
  }
  if (!form.value.code) {
    ElMessage.error('请输入资源标识')
    return
  }

  // 获取父资源名称
  const parent = resourceList.value.find(r => r.id === form.value.parentId)
  const parentName = parent ? parent.name : ''

  if (isEdit.value) {
    const index = resourceList.value.findIndex(r => r.id === form.value.id)
    if (index > -1) {
      resourceList.value[index] = { ...form.value, parentName }
      // 更新子资源的parentName
      resourceList.value.forEach(r => {
        if (r.parentId === form.value.id) {
          r.parentName = form.value.name
        }
      })
      ElMessage.success('编辑成功')
    }
  } else {
    resourceList.value.push({
      id: Date.now(),
      ...form.value,
      parentName
    })
    ElMessage.success('添加成功')
  }
  showModal.value = false
}

const deleteResource = (id) => {
  // 检查是否有子资源
  const hasChildren = resourceList.value.some(r => r.parentId === id)
  if (hasChildren) {
    ElMessage.error('请先删除子资源')
    return
  }
  resourceList.value = resourceList.value.filter(r => r.id !== id)
  ElMessage.success('删除成功')
}
</script>

<style scoped>
.resource-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
