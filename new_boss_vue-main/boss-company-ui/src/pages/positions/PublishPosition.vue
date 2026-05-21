<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, UploadFilled } from '@element-plus/icons-vue'
import { formatSalary } from 'shared-types'

const router = useRouter()

const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  title: '',
  department: '',
  city: '上海',
  district: '',
  salaryMin: '',          // ✅ 使用统一的字段名
  salaryMax: '',          // ✅ 使用统一的字段名
  salaryMonth: 12,        // ✅ 使用统一的字段名
  experience: '',
  education: '',
  gender: '',
  number: 1,
  tags: [],
  description: '',
  requirements: ''
})

const rules = {
  title: [{ required: true, message: '请输入职位名称', trigger: 'blur' }],
  department: [{ required: true, message: '请输入所属部门', trigger: 'blur' }],
  city: [{ required: true, message: '请选择工作城市', trigger: 'change' }],
  salaryMin: [{ required: true, message: '请输入最低薪资', trigger: 'blur' }],
  salaryMax: [{ required: true, message: '请输入最高薪资', trigger: 'blur' }],
  experience: [{ required: true, message: '请选择工作经验要求', trigger: 'change' }],
  education: [{ required: true, message: '请选择学历要求', trigger: 'change' }]
}

const departments = [
  '技术部', '产品部', '设计部', '运营部', '市场部', '销售部', '人事部', '财务部', '行政部'
]

const cities = ['北京', '上海', '深圳', '杭州', '广州']

const districts = {
  '北京': ['朝阳区', '海淀区', '西城区', '东城区', '丰台区'],
  '上海': ['浦东新区', '黄浦区', '徐汇区', '长宁区', '静安区'],
  '深圳': ['南山区', '福田区', '罗湖区', '宝安区', '龙岗区'],
  '杭州': ['西湖区', '上城区', '拱墅区', '滨江区', '余杭区'],
  '广州': ['天河区', '越秀区', '海珠区', '荔湾区', '白云区']
}

const experiences = ['应届生', '1 年以下', '1-3 年', '3-5 年', '5-10 年', '10 年以上']

const educations = ['不限', '高中', '中专', '大专', '本科', '硕士', '博士']

const genders = ['不限', '男', '女']

const tagOptions = [
  '五险一金', '带薪年假', '弹性工作', '定期体检', '年终奖', 
  '绩效奖金', '岗位晋升', '技能培训', '节日福利', '餐补',
  '交通补助', '通讯补贴', '住房补贴', '周末双休', '加班补助'
]

const goBack = () => {
  router.back()
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // TODO: 对接发布职位接口
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // 打印提交的薪资数据（用于验证格式）
        console.log('提交职位:', {
          ...form,
          salaryDisplay: formatSalary(Number(form.salaryMin), Number(form.salaryMax), form.salaryMonth)
        })
        
        ElMessage.success('职位发布成功')
        router.push('/company/positions')
      } catch (error) {
        ElMessage.error('发布失败，请重试')
      } finally {
        loading.value = false
      }
    }
  })
}

const handleCityChange = () => {
  form.district = ''
}
</script>

<template>
  <div class="publish-container">
    <!-- 头部导航 -->
    <el-card shadow="never" class="nav-card">
      <div class="nav-content">
        <div class="nav-left">
          <el-button text @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
          <el-divider direction="vertical" />
          <span class="page-title">发布职位</span>
        </div>
      </div>
    </el-card>
    
    <!-- 表单区域 -->
    <el-card shadow="never" class="form-card" style="margin-top: 20px">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="position-form"
      >
        <el-form-item label="职位名称" prop="title">
          <el-input v-model="form.title" placeholder="例如：高级前端工程师" maxlength="50" show-word-limit />
        </el-form-item>
        
        <el-form-item label="所属部门" prop="department">
          <el-select v-model="form.department" placeholder="请选择部门" style="width: 100%" filterable allow-create>
            <el-option v-for="dept in departments" :key="dept" :label="dept" :value="dept" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="工作地点" required>
          <el-row :gutter="16">
            <el-col :span="12">
              <el-form-item prop="city">
                <el-select v-model="form.city" placeholder="选择城市" style="width: 100%" @change="handleCityChange">
                  <el-option v-for="city in cities" :key="city" :label="city" :value="city" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item prop="district">
                <el-select v-model="form.district" placeholder="选择区县" style="width: 100%">
                  <el-option 
                    v-for="district in districts[form.city]" 
                    :key="district" 
                    :label="district" 
                    :value="district" 
                  />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form-item>
        
        <el-form-item label="薪资范围" required>
          <el-row :gutter="16">
            <el-col :span="8">
              <el-form-item prop="salaryMin">
                <el-input-number v-model="form.salaryMin" :min="1" :max="1000" placeholder="最低" 
                  style="width: 100%" controls-position="right" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item prop="salaryMax">
                <el-input-number v-model="form.salaryMax" :min="1" :max="1000" placeholder="最高" 
                  style="width: 100%" controls-position="right" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item prop="salaryMonth">
                <el-input-number v-model="form.salaryMonth" :min="12" :max="16" placeholder="月薪数" 
                  style="width: 100%" controls-position="right" />
              </el-form-item>
            </el-col>
          </el-row>
        </el-form-item>
        
        <el-form-item label="经验学历" required>
          <el-row :gutter="16">
            <el-col :span="8">
              <el-form-item prop="experience">
                <el-select v-model="form.experience" placeholder="工作经验" style="width: 100%">
                  <el-option v-for="exp in experiences" :key="exp" :label="exp" :value="exp" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item prop="education">
                <el-select v-model="form.education" placeholder="学历要求" style="width: 100%">
                  <el-option v-for="edu in educations" :key="edu" :label="edu" :value="edu" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item prop="gender">
                <el-select v-model="form.gender" placeholder="性别要求" style="width: 100%">
                  <el-option v-for="gender in genders" :key="gender" :label="gender" :value="gender" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form-item>
        
        <el-form-item label="招聘人数">
          <el-input-number v-model="form.number" :min="1" :max="100" controls-position="right" />
        </el-form-item>
        
        <el-form-item label="职位标签">
          <el-checkbox-group v-model="form.tags">
            <el-checkbox 
              v-for="tag in tagOptions" 
              :key="tag" 
              :label="tag"
              border
              style="margin-right: 12px; margin-bottom: 12px"
            >
              {{ tag }}
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        
        <el-form-item label="职位描述" required>
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="8"
            placeholder="请输入岗位职责，让求职者更好地了解这个职位..."
            maxlength="2000"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="任职要求" required>
          <el-input
            v-model="form.requirements"
            type="textarea"
            :rows="8"
            placeholder="请输入任职要求，包括技能、经验、能力等..."
            maxlength="2000"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="附件简历模板">
          <el-upload
            class="upload-demo"
            drag
            action="#"
            multiple
            :limit="1"
            :auto-upload="false"
          >
            <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 pdf/doc/docx/xls/xlsx 格式，文件大小不超过 10MB
              </div>
            </template>
          </el-upload>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit" style="padding: 12px 40px">
            立即发布
          </el-button>
          <el-button @click="goBack">暂存草稿</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.publish-container {
  padding: 0;
}

.nav-card {
  margin-bottom: 16px;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-left {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.page-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.form-card {
  max-width: 900px;
}

.position-form {
  max-width: 800px;
  margin: 0 auto;
}

.upload-demo {
  width: 100%;
}
</style>
