<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Check, Warning, Clock, Upload, Camera } from '@element-plus/icons-vue'
import request from '@/utils/request'

const authInfo = ref({})
const loading = ref(false)
const submitting = ref(false)

// 表单数据
const form = ref({
  realName: '',
  idCardNumber: '',
  // idCardFront: null,
  // idCardBack: null,
  // selfie: null,
  imgurl: null
})

// 摄像头相关
const showCameraDialog = ref(false)
const videoRef = ref(null)
const canvasRef = ref(null)
const stream = ref(null)
const capturedImage = ref(null)

// 表单验证规则
const rules = {
  realName: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 10, message: '姓名长度为 2-10 个字符', trigger: 'blur' }
  ],
  idCardNumber: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/, message: '请输入正确的身份证号', trigger: 'blur' }
  ]
}
const token = ref('')
const imageUrl = ref('')
const getToken = ()=>{
  request.get('auth/qntoken').then(res=>{
    token.value = res.token
  })
}
onMounted(()=>{
  getToken()
})
const ws = ref(null)
const initwebsocket = ()=>{
  ws.value = new WebSocket('ws://localhost:8000/ws/1')
  ws.value.onopen = ()=>{
    console.log('连接成功')
  }
  ws.value.onmessage = (event)=>{
    console.log('收到消息', event.data)
    var idcard = JSON.parse(event.data)
    form.value.realName = idcard.realName
    form.value.idCardNumber = idcard.idCardNumber
  }
  ws.value.onclose = ()=>{
    console.log('连接关闭')
  }
}
const icard_ocr = (imgurl)=>{
  request.post('auth/idcard_ocr', {imgurl}).then(res=>{
    // form.value.idCardNumber = res.idCardNumber
    // form.value.realName = res.realName
    if(res.code == 200){
      initwebsocket()
      // request.post('auth/idcardocrmes', {imgurl}).then(res=>{
      //   if(res.code == 200){
      //     var t = setInterval(()=>{
      //       request.post('auth/idcardocrmes', {imgurl}).then(res1=>{
      //         if(res1.code == 200){
      //           form.value.realName = res1.realName
      //           form.value.idCardNumber = res1.idCardNumber
      //           clearInterval(t)
        //       }
        //     })
        // },1000)
    }
  })
}
const fileupload = (file) => {
  const formData = new FormData()
  alert(file.raw)
  formData.append('file', file.raw)
  formData.append('token', token.value)
  
  // 前端直接上传到七牛云
  request.post('https://up-z1.qiniup.com', formData).then(res => {
      imageUrl.value = "http://tfxnqdgub.hb-bkt.clouddn.com/" + res.key      
      form.value.imgurl = imageUrl.value
      icard_ocr(imageUrl.value)
      ElMessage.success('上传成功')
    }).catch(error => {
    console.error('上传失败', error)
    ElMessage.error('上传失败，请重试')
  })
}

// 上传前验证
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB！')
    return false
  }
  // fileupload(file)
  return true
}

// 获取认证状态
const fetchAuthStatus = async () => {
  try {
    loading.value = true
    const res = await request.get('auth/realname/status')
    authInfo.value = res.data
  } catch (error) {
    console.error('获取认证状态失败', error)
  } finally {
    loading.value = false
  }
}

// 提交认证
const submitAuth = async () => {
  if (!form.value.realName || !form.value.idCardNumber) {
    ElMessage.warning('请填写真实姓名和身份证号')
    return
  }
  request.post('auth/idcard_upload', form.value).then(res=>{
    ElMessage.success(res.data.msg || '认证成功')
    // await fetchAuthStatus()
    
    // 清空表单
    form.value = {
      realName: '',
      idCardNumber: '',
      // idCardFront: null,
      // idCardBack: null,
      // selfie: null
    }
  })
}

// 处理文件选择
const handleFrontSuccess = (response, file) => {
  form.value.idCardFront = file.raw
  ElMessage.success('身份证正面上传成功')
}

const handleBackSuccess = (response, file) => {
  form.value.idCardBack = file.raw
  ElMessage.success('身份证反面上传成功')
}

const handleSelfieSuccess = (response, file) => {
  form.value.selfie = file.raw
  ElMessage.success('自拍照上传成功')
}

// 打开摄像头
const openCamera = async () => {
  try {
    showCameraDialog.value = true
    await nextTick()
    
    // 获取摄像头权限
    stream.value = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user', width: 640, height: 480 }
    })
    
    if (videoRef.value) {
      videoRef.value.srcObject = stream.value
      videoRef.value.play()
    }
  } catch (error) {
    console.error('无法访问摄像头:', error)
    ElMessage.error('无法访问摄像头，请检查权限设置')
    showCameraDialog.value = false
  }
}

// 拍照
const takePhoto = () => {
  if (!videoRef.value || !canvasRef.value) return
  
  const video = videoRef.value
  const canvas = canvasRef.value
  const context = canvas.getContext('2d')
  
  // 设置画布尺寸与视频一致
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  
  // 绘制视频帧到画布
  context.drawImage(video, 0, 0, canvas.width, canvas.height)
  
  // 转换为图片
  canvas.toBlob((blob) => {
    if (blob) {
      capturedImage.value = URL.createObjectURL(blob)
      form.value.selfie = new File([blob], 'selfie.jpg', { type: 'image/jpeg' })
      ElMessage.success('拍照成功')
    }
  }, 'image/jpeg', 0.9)
}

// 重新拍照
const retakePhoto = () => {
  capturedImage.value = null
  form.value.selfie = null
}

// 确认使用照片
const confirmPhoto = () => {
  showCameraDialog.value = false
  stopCamera()
}

// 关闭摄像头
const stopCamera = () => {
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
    stream.value = null
  }
  if (videoRef.value) {
    videoRef.value.srcObject = null
  }
}

// 对话框关闭时清理
const handleDialogClose = () => {
  stopCamera()
  capturedImage.value = null
}

// onMounted(() => {
//   // fetchAuthStatus()
// })
</script>

<template>
  <div class="realname-auth">
    <el-card v-loading="loading">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center">
          <span style="font-size: 18px; font-weight: 600">实名认证</span>
          <el-tag v-if="authInfo.status === 'approved'" type="success" size="large">
            <el-icon><Check /></el-icon>
            已认证
          </el-tag>
        </div>
      </template>

      <!-- 未认证状态 -->
      <div v-if="!authInfo.status || authInfo.status === 'not_submitted'">
        <el-alert
          title="完成实名认证，获得更多机会"
          description="实名认证后，您的简历将获得认证标识，更容易获得 HR 的信任和关注"
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 24px"
        />

        <el-steps :active="0" finish-status="success" style="margin-bottom: 32px">
          <el-step title="上传身份证" description="正反面清晰照片" />
          <el-step title="拍摄自拍照" description="本人实时照片" />
          <el-step title="等待审核" description="自动审核，即时生效" />
        </el-steps>

        <el-form ref="authFormRef" :model="form" :rules="rules" label-width="120px" style="max-width: 600px">
          <el-form-item label="真实姓名" prop="realName" required>
            <el-input
              v-model="form.realName"
              placeholder="请输入身份证上的真实姓名"
              maxlength="10"
            />
          </el-form-item>

          <el-form-item label="身份证号" prop="idCardNumber" required>
            <el-input
              v-model="form.idCardNumber"
              placeholder="请输入18位身份证号码"
              maxlength="18"
            />
          </el-form-item>

          <el-form-item label="身份证正面" required>
            <el-upload
              action="#"
              :auto-upload="false"
              :before-upload="beforeUpload"
              :on-change="fileupload"
              :show-file-list="true"
              accept="image/*"
            >
              <el-button type="primary" :icon="Upload">
                上传身份证正面
              </el-button>
              <template #tip>
                <div class="el-upload__tip">
                  请上传清晰的身份证正面照片，支持 JPG/PNG 格式，不超过 10MB
                </div>
              </template>
            </el-upload>
          </el-form-item>

          <el-form-item label="身份证反面" required>
            <el-upload
              action="#"
              :auto-upload="false"
              :before-upload="beforeUpload"
              :on-change="(file) => { form.idCardBack = file.raw }"
              :show-file-list="true"
              accept="image/*"
            >
              <el-button type="primary" :icon="Upload">
                上传身份证反面
              </el-button>
              <template #tip>
                <div class="el-upload__tip">
                  请上传清晰的身份证反面照片，支持 JPG/PNG 格式，不超过 10MB
                </div>
              </template>
            </el-upload>
          </el-form-item>

          <el-form-item label="自拍照" required>
            <div style="display: flex; align-items: center; gap: 16px">
              <!-- 已拍照预览 -->
              <div v-if="form.selfie" style="position: relative">
                <el-image
                  :src="capturedImage || URL.createObjectURL(form.selfie)"
                  fit="cover"
                  style="width: 120px; height: 120px; border-radius: 8px"
                />
                <el-button
                  size="small"
                  type="danger"
                  circle
                  @click="retakePhoto"
                  style="position: absolute; top: -8px; right: -8px"
                >
                  ×
                </el-button>
              </div>
              
              <!-- 拍照按钮 -->
              <el-button 
                v-else
                type="primary" 
                :icon="Camera"
                @click="openCamera"
                size="large"
              >
                打开摄像头拍照
              </el-button>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                请点击按钮打开摄像头，拍摄本人正面免冠照片，用于人脸比对
              </div>
            </template>
          </el-form-item>

          <!-- 摄像头拍照对话框 -->
          <el-dialog
            v-model="showCameraDialog"
            title="拍摄自拍照"
            width="700px"
            :close-on-click-modal="false"
            @close="handleDialogClose"
          >
            <div style="text-align: center">
              <!-- 视频预览区 -->
              <div v-if="!capturedImage" style="position: relative; background: #000; border-radius: 8px; overflow: hidden">
                <video
                  ref="videoRef"
                  autoplay
                  playsinline
                  style="width: 100%; max-height: 480px; display: block"
                ></video>
                <canvas ref="canvasRef" style="display: none"></canvas>
              </div>
              
              <!-- 拍照预览区 -->
              <div v-else style="position: relative; background: #000; border-radius: 8px; overflow: hidden">
                <img
                  :src="capturedImage"
                  alt="拍摄的照片"
                  style="width: 100%; max-height: 480px; display: block"
                />
              </div>
              
              <!-- 操作按钮 -->
              <div style="margin-top: 24px; display: flex; justify-content: center; gap: 16px">
                <el-button v-if="!capturedImage" type="primary" size="large" @click="takePhoto">
                  <el-icon><Camera /></el-icon>
                  拍照
                </el-button>
                <el-button v-else size="large" @click="retakePhoto">
                  重新拍摄
                </el-button>
                <el-button v-if="capturedImage" type="success" size="large" @click="confirmPhoto">
                  确认使用
                </el-button>
              </div>
              
              <p style="margin-top: 16px; color: #909399; font-size: 14px">
                请保持光线充足，正对摄像头，确保面部清晰可见
              </p>
            </div>
          </el-dialog>

          <el-form-item>
            <el-alert
              title="隐私保护说明"
              description="您的身份信息仅用于实名认证，我们将严格保护您的隐私安全，不会泄露给第三方"
              type="success"
              :closable="false"
              show-icon
              style="margin-bottom: 16px"
            />
            
            <el-button 
              type="primary" 
              size="large" 
              @click="submitAuth" 
              :loading="submitting"
              style="width: 200px"
            >
              {{ submitting ? '提交中...' : '提交认证' }}
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 已认证状态 -->
      <div v-else-if="authInfo.status === 'approved'">
        <el-result icon="success" title="实名认证已通过">
          <template #sub-title>
            <el-descriptions :column="1" border style="margin-top: 20px; max-width: 500px; margin-left: auto; margin-right: auto">
              <el-descriptions-item label="姓名">{{ authInfo.real_name }}</el-descriptions-item>
              <el-descriptions-item label="身份证号">{{ authInfo.id_card_number }}</el-descriptions-item>
              <el-descriptions-item label="认证时间">{{ authInfo.authenticated_at }}</el-descriptions-item>
            </el-descriptions>
          </template>
          <template #extra>
            <el-alert
              title="认证优势"
              description="✓ 简历获得认证标识 ✓ 优先推荐给 HR ✓ 提升信任度"
              type="success"
              :closable="false"
              show-icon
              style="margin-top: 20px"
            />
          </template>
        </el-result>
      </div>

      <!-- 审核中状态 -->
      <div v-else-if="authInfo.status === 'pending'">
        <el-result icon="info" title="审核中">
          <template #sub-title>
            <p style="font-size: 16px; color: #606266">
              <el-icon style="vertical-align: middle"><Clock /></el-icon>
              您的认证申请正在审核中，请耐心等待
            </p>
            <p style="color: #909399; margin-top: 8px">
              通常会在 1-2 小时内完成审核
            </p>
          </template>
          <template #extra>
            <el-alert
              title="温馨提示"
              description="审核期间您可以继续浏览职位和投递简历，审核通过后将获得认证标识"
              type="info"
              :closable="false"
              show-icon
              style="margin-top: 20px"
            />
          </template>
        </el-result>
      </div>

      <!-- 被拒绝状态 -->
      <div v-else-if="authInfo.status === 'rejected'">
        <el-result icon="error" title="认证被拒绝">
          <template #sub-title>
            <el-alert
              :title="'拒绝原因：' + (authInfo.reject_reason || '照片不清晰或信息不符')"
              type="error"
              :closable="false"
              show-icon
              style="margin-top: 16px"
            />
          </template>
          <template #extra>
            <el-button type="primary" @click="retryAuth" size="large">
              重新认证
            </el-button>
          </template>
        </el-result>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.realname-auth {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.el-upload__tip {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
  line-height: 1.5;
}

:deep(.el-descriptions__label) {
  width: 120px;
  font-weight: 600;
}
</style>
