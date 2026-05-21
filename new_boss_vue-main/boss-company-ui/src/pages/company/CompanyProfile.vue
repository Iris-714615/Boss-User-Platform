<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const form = ref({
  companyName: '示例科技有限公司',
  industry: '互联网/软件',
  scale: '100-500 人',
  location: '上海市浦东新区',
  description: '',
  tags: ['五险一金', '带薪年假', '弹性工作']
})

const onSave = () => {
  ElMessage.success('公司信息保存成功')
}
</script>

<template>
  <div class="company-profile-container">
    <el-card shadow="never">
      <template #header>
        <span>公司主页</span>
      </template>
      
      <el-form :model="form" label-width="120px">
        <el-form-item label="公司名称">
          <el-input v-model="form.companyName" disabled />
        </el-form-item>
        
        <el-form-item label="行业">
          <el-input v-model="form.industry" disabled />
        </el-form-item>
        
        <el-form-item label="规模">
          <el-input v-model="form.scale" disabled />
        </el-form-item>
        
        <el-form-item label="位置">
          <el-input v-model="form.location" disabled />
        </el-form-item>
        
        <el-form-item label="公司介绍">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="6"
            placeholder="请输入公司介绍"
          />
        </el-form-item>
        
        <el-form-item label="公司标签">
          <el-tag v-for="tag in form.tags" :key="tag" style="margin-right: 8px">{{ tag }}</el-tag>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="onSave">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.company-profile-container {
  padding: 0;
}
</style>
