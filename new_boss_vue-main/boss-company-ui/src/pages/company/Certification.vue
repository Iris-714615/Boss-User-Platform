<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  OfficeBuilding,
  User,
  Document,
  Upload,
  Check,
  Clock,
  Warning,
  InfoFilled
} from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)
const submitting = ref(false)
const activeStep = ref(0)

// 认证状态
const authStatus = ref({
  status: 'not_submitted', // not_submitted, pending, approved, rejected
  submitTime: '',
  approveTime: '',
  rejectReason: ''
})

// 表单数据
const form = reactive({
  // 基本信息
  companyName: '',
  unifiedSocialCreditCode: '',
  legalPerson: '',
  registeredCapital: '',
  establishmentDate: '',
  registrationStatus: '存续', // 登记状态
  industry: '',
  companySize: '',
  financingStage: '',
  headquarters: '',
  businessScope: '',
  website: '',
  
  // 联系信息
  contactName: '',
  contactPhone: '',
  contactEmail: '',
  
  // 文件
  businessLicense: null,
  idCardFront: null,
  idCardBack: null,
  organizationCode: null
})

// 表单验证规则
const rules = {
  companyName: [
    { required: true, message: '请输入企业名称', trigger: 'blur' }
  ],
  unifiedSocialCreditCode: [
    { required: true, message: '请输入统一社会信用代码', trigger: 'blur' },
    { pattern: /^[0-9A-HJ-NPQRTUWXY]{18}$/, message: '统一社会信用代码格式不正确', trigger: 'blur' }
  ],
  legalPerson: [
    { required: true, message: '请输入法人代表姓名', trigger: 'blur' }
  ],
  registeredCapital: [
    { required: true, message: '请输入注册资本', trigger: 'blur' }
  ],
  establishmentDate: [
    { required: true, message: '请选择成立日期', trigger: 'change' }
  ],
  industry: [
    { required: true, message: '请选择行业', trigger: 'change' }
  ],
  companySize: [
    { required: true, message: '请选择公司规模', trigger: 'change' }
  ],
  headquarters: [
    { required: true, message: '请输入总部地址', trigger: 'blur' }
  ],
  businessScope: [
    { required: true, message: '请输入经营范围', trigger: 'blur' }
  ],
  contactName: [
    { required: true, message: '请输入联系人姓名', trigger: 'blur' }
  ],
  contactPhone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  contactEmail: [
    { required: true, message: '请输入联系邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ]
}

const formRef = ref(null)

// 获取认证状态
const fetchAuthStatus = async () => {
  try {
    loading.value = true
    const res = await axios.get('/api/v1/company/certification/status')
    authStatus.value = res.data
    
    // 如果已提交，跳转到状态页
    if (authStatus.value.status !== 'not_submitted') {
      activeStep.value = 2
    }
  } catch (error) {
    console.error('获取认证状态失败', error)
  } finally {
    loading.value = false
  }
}

// 上传前验证
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/') || file.type.includes('pdf')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传图片或 PDF 文件！')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB！')
    return false
  }
  return true
}

// 处理文件选择
const handleFileChange = (file, field) => {
  form[field] = file.raw
  ElMessage.success(`${file.name} 上传成功`)
}

// 下一步
const nextStep = async () => {
  if (activeStep.value === 0) {
    // 验证第一步表单
    try {
      await formRef.value.validateField([
        'companyName',
        'unifiedSocialCreditCode',
        'legalPerson',
        'registeredCapital',
        'establishmentDate',
        'industry',
        'companySize',
        'headquarters',
        'businessScope'
      ])
      activeStep.value++
    } catch (error) {
      ElMessage.warning('请填写完整的企业信息')
    }
  } else if (activeStep.value === 1) {
    // 验证第二步表单
    try {
      await formRef.value.validateField([
        'contactName',
        'contactPhone',
        'contactEmail'
      ])
      
      // 验证文件上传
      if (!form.businessLicense) {
        ElMessage.warning('请上传营业执照')
        return
      }
      if (!form.idCardFront || !form.idCardBack) {
        ElMessage.warning('请上传法人身份证正反面')
        return
      }
      
      activeStep.value++
    } catch (error) {
      ElMessage.warning('请填写完整的联系信息并上传所有必需文件')
    }
  }
}

// 上一步
const prevStep = () => {
  if (activeStep.value > 0) {
    activeStep.value--
  }
}

// 提交认证
const submitCertification = async () => {
  try {
    await ElMessageBox.confirm(
      '请确保填写的信息真实有效，虚假信息将承担法律责任。提交后将在 1-2 个工作日内完成审核。',
      '确认提交',
      {
        confirmButtonText: '确认提交',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    submitting.value = true

    const formData = new FormData()
    
    // 添加基本信息
    Object.keys(form).forEach(key => {
      if (key !== 'businessLicense' && key !== 'idCardFront' && 
          key !== 'idCardBack' && key !== 'organizationCode') {
        formData.append(key, form[key])
      }
    })
    
    // 添加文件
    if (form.businessLicense) {
      formData.append('business_license', form.businessLicense)
    }
    if (form.idCardFront) {
      formData.append('id_card_front', form.idCardFront)
    }
    if (form.idCardBack) {
      formData.append('id_card_back', form.idCardBack)
    }
    if (form.organizationCode) {
      formData.append('organization_code', form.organizationCode)
    }

    const res = await axios.post('/api/v1/company/certification/apply', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    ElMessage.success(res.data.message || '提交成功，等待审核')
    await fetchAuthStatus()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '提交失败，请重试')
    }
  } finally {
    submitting.value = false
  }
}

// 重新申请
const retryApplication = () => {
  authStatus.value = {
    status: 'not_submitted',
    submitTime: '',
    approveTime: '',
    rejectReason: ''
  }
  activeStep.value = 0
  
  // 清空表单
  Object.keys(form).forEach(key => {
    form[key] = key === 'businessLicense' || key === 'idCardFront' || 
                key === 'idCardBack' || key === 'organizationCode' ? null : ''
  })
}

onMounted(() => {
  fetchAuthStatus()
})
</script>

<template>
  <div class="certification-page" v-loading="loading">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span style="font-size: 18px; font-weight: 600">企业认证</span>
          <el-tag v-if="authStatus.status === 'approved'" type="success" size="large">
            <el-icon><Check /></el-icon>
            已认证
          </el-tag>
        </div>
      </template>

      <!-- 未提交状态 -->
      <div v-if="authStatus.status === 'not_submitted'">
        <el-alert
          title="完成企业认证，开启招聘之旅"
          description="认证后您可以发布职位、查看简历、与求职者沟通。我们将严格保护您的企业信息安全。"
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 24px"
        />

        <!-- 步骤条 -->
        <el-steps :active="activeStep" finish-status="success" style="margin-bottom: 32px">
          <el-step title="企业信息" description="填写基本工商信息" />
          <el-step title="资质材料" description="上传营业执照和身份证" />
          <el-step title="确认提交" description="核对信息并提交" />
        </el-steps>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="140px"
          style="max-width: 800px"
        >
          <!-- 第一步：企业信息 -->
          <div v-show="activeStep === 0">
            <el-divider content-position="left">
              <el-icon><OfficeBuilding /></el-icon>
              企业基本信息
            </el-divider>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="企业名称" prop="companyName" required>
                  <el-input v-model="form.companyName" placeholder="请输入营业执照上的企业全称" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="统一社会信用代码" prop="unifiedSocialCreditCode" required>
                  <el-input v-model="form.unifiedSocialCreditCode" placeholder="18 位信用代码" maxlength="18" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="法人代表" prop="legalPerson" required>
                  <el-input v-model="form.legalPerson" placeholder="请输入法人姓名" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="注册资本" prop="registeredCapital" required>
                  <el-input v-model="form.registeredCapital" placeholder="例如：500 万人民币" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="成立日期" prop="establishmentDate" required>
                  <el-date-picker
                    v-model="form.establishmentDate"
                    type="date"
                    placeholder="选择成立日期"
                    style="width: 100%"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="登记状态" prop="registrationStatus" required>
                  <el-select v-model="form.registrationStatus" placeholder="请选择登记状态" style="width: 100%">
                    <el-option label="存续" value="存续" />
                    <el-option label="在业" value="在业" />
                    <el-option label="开业" value="开业" />
                    <el-option label="停业" value="停业" />
                    <el-option label="清算" value="清算" />
                    <el-option label="吊销" value="吊销" />
                    <el-option label="注销" value="注销" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="所属行业" prop="industry" required>
                  <el-select v-model="form.industry" placeholder="请选择行业" style="width: 100%">
                    <el-option label="互联网/软件" value="互联网/软件" />
                    <el-option label="人工智能" value="人工智能" />
                    <el-option label="电子商务" value="电子商务" />
                    <el-option label="金融" value="金融" />
                    <el-option label="教育" value="教育" />
                    <el-option label="医疗" value="医疗" />
                    <el-option label="其他" value="其他" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="公司规模" prop="companySize" required>
                  <el-select v-model="form.companySize" placeholder="请选择规模" style="width: 100%">
                    <el-option label="0-20 人" value="0-20 人" />
                    <el-option label="20-99 人" value="20-99 人" />
                    <el-option label="100-499 人" value="100-499 人" />
                    <el-option label="500-999 人" value="500-999 人" />
                    <el-option label="1000-9999 人" value="1000-9999 人" />
                    <el-option label="10000 人以上" value="10000 人以上" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="融资阶段">
              <el-select v-model="form.financingStage" placeholder="请选择（可选）" style="width: 100%; max-width: 400px">
                <el-option label="天使轮" value="天使轮" />
                <el-option label="A 轮" value="A 轮" />
                <el-option label="B 轮" value="B 轮" />
                <el-option label="C 轮" value="C 轮" />
                <el-option label="D 轮及以上" value="D 轮及以上" />
                <el-option label="已上市" value="已上市" />
                <el-option label="不需要融资" value="不需要融资" />
              </el-select>
            </el-form-item>

            <el-form-item label="总部地址" prop="headquarters" required>
              <el-input v-model="form.headquarters" placeholder="请输入企业总部详细地址" />
            </el-form-item>

            <el-form-item label="经营范围" prop="businessScope" required>
              <el-input
                v-model="form.businessScope"
                type="textarea"
                :rows="3"
                placeholder="请输入营业执照上的经营范围"
              />
            </el-form-item>
          </div>

          <!-- 第二步：资质材料 -->
          <div v-show="activeStep === 1">
            <el-divider content-position="left">
              <el-icon><Document /></el-icon>
              联系信息
            </el-divider>

            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="联系人姓名" prop="contactName" required>
                  <el-input v-model="form.contactName" placeholder="请输入联系人姓名" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="联系电话" prop="contactPhone" required>
                  <el-input v-model="form.contactPhone" placeholder="请输入手机号" maxlength="11" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="联系邮箱" prop="contactEmail" required>
                  <el-input v-model="form.contactEmail" placeholder="请输入邮箱" />
                </el-form-item>
              </el-col>
            </el-row>

            <el-divider content-position="left">
              <el-icon><Upload /></el-icon>
              资质材料上传
            </el-divider>

            <el-alert
              title="上传要求"
              description="• 支持 JPG、PNG、PDF 格式<br/>• 单个文件不超过 10MB<br/>• 请确保图片清晰、完整<br/>• 证件需在有效期内"
              type="warning"
              :closable="false"
              show-icon
              style="margin-bottom: 20px"
            />

            <el-form-item label="营业执照" required>
              <el-upload
                action="#"
                :auto-upload="false"
                :before-upload="beforeUpload"
                :on-change="(file) => handleFileChange(file, 'businessLicense')"
                :show-file-list="true"
                accept="image/*,.pdf"
                :limit="1"
              >
                <el-button type="primary" :icon="Upload">
                  上传营业执照
                </el-button>
                <template #tip>
                  <div class="upload-tip">
                    请上传清晰的营业执照扫描件或照片
                  </div>
                </template>
              </el-upload>
            </el-form-item>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="法人身份证（正面）" required>
                  <el-upload
                    action="#"
                    :auto-upload="false"
                    :before-upload="beforeUpload"
                    :on-change="(file) => handleFileChange(file, 'idCardFront')"
                    :show-file-list="true"
                    accept="image/*"
                    :limit="1"
                  >
                    <el-button type="primary" :icon="Upload">
                      上传正面
                    </el-button>
                  </el-upload>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="法人身份证（反面）" required>
                  <el-upload
                    action="#"
                    :auto-upload="false"
                    :before-upload="beforeUpload"
                    :on-change="(file) => handleFileChange(file, 'idCardBack')"
                    :show-file-list="true"
                    accept="image/*"
                    :limit="1"
                  >
                    <el-button type="primary" :icon="Upload">
                      上传反面
                    </el-button>
                  </el-upload>
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="组织机构代码证">
              <el-upload
                action="#"
                :auto-upload="false"
                :before-upload="beforeUpload"
                :on-change="(file) => handleFileChange(file, 'organizationCode')"
                :show-file-list="true"
                accept="image/*,.pdf"
                :limit="1"
              >
                <el-button :icon="Upload">
                  上传组织机构代码证（可选）
                </el-button>
                <template #tip>
                  <div class="upload-tip">
                    如已三证合一，可不上传此项
                  </div>
                </template>
              </el-upload>
            </el-form-item>
          </div>

          <!-- 第三步：确认提交 -->
          <div v-show="activeStep === 2">
            <el-alert
              title="请仔细核对以下信息"
              description="提交后将无法修改，请确保所有信息准确无误"
              type="warning"
              :closable="false"
              show-icon
              style="margin-bottom: 24px"
            />

            <el-descriptions :column="2" border>
              <el-descriptions-item label="企业名称">{{ form.companyName }}</el-descriptions-item>
              <el-descriptions-item label="统一社会信用代码">{{ form.unifiedSocialCreditCode }}</el-descriptions-item>
              <el-descriptions-item label="法人代表">{{ form.legalPerson }}</el-descriptions-item>
              <el-descriptions-item label="注册资本">{{ form.registeredCapital }}</el-descriptions-item>
              <el-descriptions-item label="成立日期">{{ form.establishmentDate }}</el-descriptions-item>
              <el-descriptions-item label="登记状态">{{ form.registrationStatus }}</el-descriptions-item>
              <el-descriptions-item label="所属行业">{{ form.industry }}</el-descriptions-item>
              <el-descriptions-item label="公司规模">{{ form.companySize }}</el-descriptions-item>
              <el-descriptions-item label="融资阶段">{{ form.financingStage || '未填写' }}</el-descriptions-item>
              <el-descriptions-item label="总部地址" :span="2">{{ form.headquarters }}</el-descriptions-item>
              <el-descriptions-item label="联系人">{{ form.contactName }}</el-descriptions-item>
              <el-descriptions-item label="联系电话">{{ form.contactPhone }}</el-descriptions-item>
              <el-descriptions-item label="联系邮箱" :span="2">{{ form.contactEmail }}</el-descriptions-item>
            </el-descriptions>

            <el-divider />

            <el-alert
              title="隐私保护承诺"
              description="我们承诺：您的企业信息仅用于身份认证，不会泄露给任何第三方。所有资料均采用加密存储，严格遵守《网络安全法》和《个人信息保护法》。"
              type="success"
              :closable="false"
              show-icon
            />
          </div>

          <!-- 操作按钮 -->
          <el-form-item style="margin-top: 32px">
            <el-button v-if="activeStep > 0" @click="prevStep">
              上一步
            </el-button>
            <el-button 
              v-if="activeStep < 2" 
              type="primary" 
              @click="nextStep"
            >
              下一步
            </el-button>
            <el-button 
              v-if="activeStep === 2" 
              type="primary" 
              size="large"
              @click="submitCertification"
              :loading="submitting"
            >
              {{ submitting ? '提交中...' : '确认提交' }}
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 审核中状态 -->
      <div v-else-if="authStatus.status === 'pending'">
        <el-result icon="info" title="审核中">
          <template #sub-title>
            <p style="font-size: 16px; color: #606266">
              <el-icon style="vertical-align: middle"><Clock /></el-icon>
              您的企业认证申请正在审核中
            </p>
            <p style="color: #909399; margin-top: 8px">
              提交时间：{{ authStatus.submitTime }}
            </p>
            <p style="color: #909399">
              预计 1-2 个工作日内完成审核
            </p>
          </template>
          <template #extra>
            <el-alert
              title="温馨提示"
              description="审核期间您可以先完善公司信息，审核通过后将立即获得发布职位的权限"
              type="info"
              :closable="false"
              show-icon
              style="margin-top: 20px"
            />
          </template>
        </el-result>
      </div>

      <!-- 已通过状态 -->
      <div v-else-if="authStatus.status === 'approved'">
        <el-result icon="success" title="企业认证已通过">
          <template #sub-title>
            <el-descriptions :column="2" border style="margin-top: 20px; max-width: 600px; margin-left: auto; margin-right: auto">
              <el-descriptions-item label="企业名称">{{ form.companyName }}</el-descriptions-item>
              <el-descriptions-item label="统一社会信用代码">{{ form.unifiedSocialCreditCode }}</el-descriptions-item>
              <el-descriptions-item label="认证时间">{{ authStatus.approveTime }}</el-descriptions-item>
            </el-descriptions>
          </template>
          <template #extra>
            <el-alert
              title="认证成功"
              description="✓ 可以发布职位 ✓ 查看完整简历 ✓ 与求职者沟通 ✓ 获得更多曝光"
              type="success"
              :closable="false"
              show-icon
              style="margin-top: 20px"
            />
            <el-button type="primary" @click="router.push('/company/dashboard')" style="margin-top: 20px">
              前往工作台
            </el-button>
          </template>
        </el-result>
      </div>

      <!-- 被拒绝状态 -->
      <div v-else-if="authStatus.status === 'rejected'">
        <el-result icon="error" title="认证被拒绝">
          <template #sub-title>
            <el-alert
              :title="'拒绝原因：' + (authStatus.rejectReason || '资料不符合要求')"
              type="error"
              :closable="false"
              show-icon
              style="margin-top: 16px"
            />
          </template>
          <template #extra>
            <el-button type="primary" @click="retryApplication" size="large">
              重新申请
            </el-button>
          </template>
        </el-result>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.certification-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
  line-height: 1.5;
}

:deep(.el-descriptions__label) {
  width: 140px;
  font-weight: 600;
}

:deep(.el-divider__text) {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #303133;
}
</style>
