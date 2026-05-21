<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Document,
  OfficeBuilding,
  User,
  Calendar,
  Money,
  Location,
  ZoomIn,
  Check,
  Close,
  Warning
} from '@element-plus/icons-vue'

const loading = ref(false)
const dialogVisible = ref(true)

// 企业基本信息
const companyInfo = reactive({
  id: '10002',
  name: '某某信息科技有限公司',
  status: '待审核',
  applyTime: '2026-03-31 09:30:00',
})

// 认证信息
const certificationInfo = reactive({
  type: '企业认证',
  legalPerson: '李四',
  registeredCapital: '500 万人民币',
  establishmentDate: '2019-08-15',
  registrationStatus: '存续',
  unifiedSocialCreditCode: '91310000MA1K3YJXX6',
  organizationCode: 'MA1K3YJX6',
  industry: '互联网/软件',
  companySize: '50-99 人',
  headquarters: '北京市海淀区中关村大街 1 号',
  businessScope: '技术开发、技术咨询、技术服务、软件开发',
  
  // 认证状态
  auditStatus: '待审核',
  submitTime: '2026-03-31 09:30:00',
  previousAuditResult: '通过',
  previousAuditTime: '2025-03-15 14:20:00',
})

// 资质材料
const documents = ref([
  {
    id: 1,
    type: '营业执照',
    image: '/api/images/business-license.jpg',
    uploadTime: '2026-03-31 09:28:00',
    status: '待审核',
  },
  {
    id: 2,
    type: '法人身份证（正面）',
    image: '/api/images/id-card-front.jpg',
    uploadTime: '2026-03-31 09:28:30',
    status: '待审核',
  },
  {
    id: 3,
    type: '法人身份证（反面）',
    image: '/api/images/id-card-back.jpg',
    uploadTime: '2026-03-31 09:29:00',
    status: '待审核',
  },
  {
    id: 4,
    type: '组织机构代码证',
    image: '/api/images/organization-code.jpg',
    uploadTime: '2026-03-31 09:29:30',
    status: '待审核',
  },
])

// 工商信息核验
const businessCheck = reactive({
  creditCodeValid: true,
  companyNameMatch: true,
  legalPersonMatch: true,
  registrationStatusNormal: true,
  noAbnormalOperation: true,
  noIllegalRecord: false,
  riskWarning: '发现 1 条历史行政处罚记录',
})

// 审核表单
const auditForm = reactive({
  result: '',
  remark: '',
  rejectReason: '',
})

const currentImage = ref('')
const imageViewerVisible = ref(false)

const viewImage = (imageUrl: string) => {
  currentImage.value = imageUrl
  imageViewerVisible.value = true
}

const handleApprove = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要通过企业"${companyInfo.name}"的认证申请吗？`,
      '审核通过确认',
      {
        confirmButtonText: '确认通过',
        cancelButtonText: '取消',
        type: 'success',
      }
    )
    
    auditForm.result = 'approve'
    ElMessage.success('审核通过')
    dialogVisible.value = false
  } catch {
    // 取消操作
  }
}

const handleReject = async () => {
  if (!auditForm.rejectReason) {
    ElMessage.warning('请填写拒绝原因')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要拒绝企业"${companyInfo.name}"的认证申请吗？`,
      '审核拒绝确认',
      {
        confirmButtonText: '确认拒绝',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    auditForm.result = 'reject'
    ElMessage.success('已拒绝申请')
    dialogVisible.value = false
  } catch {
    // 取消操作
  }
}

const handleClose = () => {
  dialogVisible.value = false
}

const quickRejectReasons = ref([
  '营业执照模糊不清，无法辨认',
  '证件信息与填写信息不符',
  '证件已过期',
  '疑似伪造证件',
  '企业被列入经营异常名录',
])

const selectRejectReason = (reason: string) => {
  auditForm.rejectReason = reason
}
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="`企业认证审核 - ${companyInfo.name}`"
    width="95%"
    top="2vh"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <div v-loading="loading" class="certification-audit">
      <el-row :gutter="20">
        <!-- 左侧：资质材料与工商信息 -->
        <el-col :span="16">
          <!-- 基本信息提示 -->
          <el-alert
            title="企业认证申请"
            type="info"
            :closable="false"
            style="margin-bottom: 16px"
          >
            <template #default>
              <div style="display: flex; justify-content: space-between; align-items: center">
                <div>
                  <span>申请企业：<strong>{{ companyInfo.name }}</strong></span>
                  <span style="margin-left: 20px">申请时间：{{ companyInfo.applyTime }}</span>
                </div>
                <el-tag type="warning" size="small">待审核</el-tag>
              </div>
            </template>
          </el-alert>

          <!-- 资质材料 -->
          <el-card shadow="never" class="doc-card">
            <template #header>
              <span style="font-weight: 600">📄 资质材料</span>
            </template>
            
            <el-table :data="documents" style="width: 100%">
              <el-table-column prop="id" label="序号" width="60" />
              <el-table-column prop="type" label="材料类型" min-width="200" />
              <el-table-column prop="uploadTime" label="上传时间" width="180" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="{ row }">
                  <el-tag type="warning" size="small">{{ row.status }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120">
                <template #default="{ row }">
                  <el-button 
                    text 
                    type="primary" 
                    size="small"
                    @click="viewImage(row.image)"
                  >
                    <el-icon><ZoomIn /></el-icon>
                    查看
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>

          <!-- 工商信息详情 -->
          <el-card shadow="never" class="info-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">🏢 工商信息详情</span>
            </template>
            
            <el-descriptions :column="2" border>
              <el-descriptions-item label="企业名称">{{ certificationInfo.name }}</el-descriptions-item>
              <el-descriptions-item label="法人代表">{{ certificationInfo.legalPerson }}</el-descriptions-item>
              <el-descriptions-item label="注册资本">{{ certificationInfo.registeredCapital }}</el-descriptions-item>
              <el-descriptions-item label="成立日期">{{ certificationInfo.establishmentDate }}</el-descriptions-item>
              <el-descriptions-item label="登记状态">{{ certificationInfo.registrationStatus }}</el-descriptions-item>
              <el-descriptions-item label="所属行业">{{ certificationInfo.industry }}</el-descriptions-item>
              <el-descriptions-item label="统一社会信用代码" :span="2">{{ certificationInfo.unifiedSocialCreditCode }}</el-descriptions-item>
              <el-descriptions-item label="组织机构代码">{{ certificationInfo.organizationCode }}</el-descriptions-item>
              <el-descriptions-item label="公司规模">{{ certificationInfo.companySize }}</el-descriptions-item>
              <el-descriptions-item label="总部地点">{{ certificationInfo.headquarters }}</el-descriptions-item>
              <el-descriptions-item label="经营范围" :span="2">{{ certificationInfo.businessScope }}</el-descriptions-item>
            </el-descriptions>
          </el-card>

          <!-- 工商核验结果 -->
          <el-card shadow="never" class="check-card" style="margin-top: 16px">
            <template #header>
              <div style="display: flex; justify-content: space-between; align-items: center">
                <span style="font-weight: 600">✅ 工商核验结果</span>
                <el-button type="primary" size="small">重新核验</el-button>
              </div>
            </template>
            
            <el-table :data="[businessCheck]" style="width: 100%" :show-header="false">
              <el-table-column>
                <template #default>
                  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px">
                    <div style="display: flex; align-items: center; gap: 8px">
                      <el-icon color="#67C23A" :size="20"><Check /></el-icon>
                      <span>统一社会信用代码有效</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px">
                      <el-icon color="#67C23A" :size="20"><Check /></el-icon>
                      <span>企业名称匹配</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px">
                      <el-icon color="#67C23A" :size="20"><Check /></el-icon>
                      <span>法人信息匹配</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px">
                      <el-icon color="#67C23A" :size="20"><Check /></el-icon>
                      <span>经营状态正常</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px">
                      <el-icon color="#67C23A" :size="20"><Check /></el-icon>
                      <span>无经营异常</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px">
                      <el-icon color="#F56C6C" :size="20"><Close /></el-icon>
                      <span style="color: #F56C6C">有违法记录</span>
                    </div>
                  </div>
                </template>
              </el-table-column>
            </el-table>
            
            <el-alert
              v-if="businessCheck.riskWarning"
              :title="businessCheck.riskWarning"
              type="warning"
              :closable="false"
              style="margin-top: 16px"
              show-icon
            />
          </el-card>

          <!-- 历史审核记录 -->
          <el-card shadow="never" class="history-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">⏰ 历史审核记录</span>
            </template>
            
            <el-timeline>
              <el-timeline-item timestamp="2025-03-15 14:20" placement="top" type="success">
                <el-tag type="success" size="small">审核通过</el-tag>
                <div style="margin-top: 8px; color: #606266">审核员：系统自动审核</div>
              </el-timeline-item>
              <el-timeline-item timestamp="2025-03-15 09:30" placement="top">
                提交认证申请
              </el-timeline-item>
            </el-timeline>
          </el-card>
        </el-col>

        <!-- 右侧：审核操作面板 -->
        <el-col :span="8">
          <!-- 审核表单 -->
          <el-card shadow="never" class="audit-card">
            <template #header>
              <span style="font-weight: 600">📝 审核操作</span>
            </template>
            
            <el-form :model="auditForm" label-width="80px">
              <el-form-item label="审核结果">
                <el-radio-group v-model="auditForm.result" style="display: flex; gap: 16px">
                  <el-radio label="approve">
                    <el-icon color="#67C23A"><Check /></el-icon>
                    通过
                  </el-radio>
                  <el-radio label="reject">
                    <el-icon color="#F56C6C"><Close /></el-icon>
                    拒绝
                  </el-radio>
                </el-radio-group>
              </el-form-item>
              
              <el-form-item 
                v-if="auditForm.result === 'reject'" 
                label="拒绝原因"
                required
              >
                <el-select
                  v-model="auditForm.rejectReason"
                  placeholder="请选择拒绝原因"
                  style="width: 100%"
                  allow-create
                  filterable
                >
                  <el-option
                    v-for="reason in quickRejectReasons"
                    :key="reason"
                    :label="reason"
                    :value="reason"
                  />
                </el-select>
                
                <div style="margin-top: 8px">
                  <el-tag
                    v-for="reason in quickRejectReasons"
                    :key="reason"
                    size="small"
                    style="margin-right: 8px; margin-bottom: 8px; cursor: pointer"
                    @click="selectRejectReason(reason)"
                  >
                    {{ reason }}
                  </el-tag>
                </div>
              </el-form-item>
              
              <el-form-item label="备注说明">
                <el-input
                  v-model="auditForm.remark"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入审核意见或补充说明"
                />
              </el-form-item>
              
              <el-divider />
              
              <el-button
                type="success"
                plain
                style="width: 100%; margin-bottom: 12px"
                :disabled="!auditForm.result || auditForm.result === 'reject'"
                @click="handleApprove"
              >
                <el-icon><Check /></el-icon>
                确认通过
              </el-button>
              
              <el-button
                type="danger"
                plain
                style="width: 100%"
                :disabled="!auditForm.result || auditForm.result === 'approve'"
                @click="handleReject"
              >
                <el-icon><Close /></el-icon>
                确认拒绝
              </el-button>
            </el-form>
          </el-card>

          <!-- 注意事项 -->
          <el-card shadow="never" class="tips-card" style="margin-top: 16px">
            <template #header>
              <span style="font-weight: 600">⚠️ 审核注意事项</span>
            </template>
            
            <el-timeline>
              <el-timeline-item type="warning" placement="top">
                检查营业执照是否清晰、完整
              </el-timeline-item>
              <el-timeline-item type="warning" placement="top">
                核对统一社会信用代码格式是否正确
              </el-timeline-item>
              <el-timeline-item type="warning" placement="top">
                确认企业名称与营业执照一致
              </el-timeline-item>
              <el-timeline-item type="warning" placement="top">
                核实法人身份证信息是否匹配
              </el-timeline-item>
              <el-timeline-item type="warning" placement="top">
                查询企业是否存在经营异常
              </el-timeline-item>
            </el-timeline>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 图片查看器 -->
    <el-image-viewer
      v-if="imageViewerVisible"
      :url-list="[currentImage]"
      @close="imageViewerVisible = false"
    />
  </el-dialog>
</template>

<style scoped>
.certification-audit {
  max-height: 80vh;
  overflow-y: auto;
  padding-right: 10px;
}

.doc-card, .info-card, .check-card, .history-card, .audit-card, .tips-card {
  margin-bottom: 16px;
}

:deep(.el-descriptions__label) {
  width: 140px;
  font-weight: 500;
}

.audit-card {
  background: #f5f7fa;
}
</style>
