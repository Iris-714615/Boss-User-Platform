<template>
  <div class="recommend-job-container">
    <div class="page-header">
      <h1 class="page-title">智能岗位推荐</h1>
      <p class="page-desc">上传您的简历，AI将为您智能匹配最适合的岗位</p>
    </div>

    <!-- 文件上传区域 -->
    <div class="upload-section">
      <el-card class="upload-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Upload /></el-icon>
            <span>上传简历文件</span>
          </div>
        </template>
        <div class="upload-content">
          <el-upload
            ref="uploadRef"
            class="upload-dragger"
            drag
            :before-upload="beforeUpload"
            :on-change="handleFileChange"
            :limit="1"
            :auto-upload="false"
            accept=".pdf,.doc,.docx,.txt"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 PDF、DOC、DOCX、TXT 格式，文件大小不超过 10MB
              </div>
            </template>
          </el-upload>
          <div class="upload-actions" v-if="currentFile">
            <el-button
              type="primary"
              :loading="uploading"
              @click="submitUpload"
              size="large"
            >
              <el-icon v-if="!uploading"><Search /></el-icon>
              {{ uploading ? "分析中..." : "开始智能匹配" }}
            </el-button>
            <el-button @click="clearFiles" size="large">清除文件</el-button>
          </div>
          <div v-if="uploading" class="upload-progress">
            <el-progress
              :percentage="uploadProgress"
              :status="uploadProgress === 100 ? 'success' : null"
            />
          </div>
        </div>
      </el-card>
    </div>

    <!-- 结果展示区域 -->
    <div class="results-section" v-if="jobList.length > 0">
      <el-card class="results-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Briefcase /></el-icon>
            <span>推荐岗位 ({{ jobList.length }})</span>
            <el-tag type="success" class="success-tag">
              {{ resultMessage }}
            </el-tag>
          </div>
        </template>
        <div class="job-list">
          <div
            v-for="(job, index) in jobList"
            :key="job.id"
            class="job-card"
            :class="{ 'job-card-highlight': index === 0 }"
          >
            <div class="job-header">
              <div class="job-title-row">
                <h3 class="job-title">{{ job.title }}</h3>
                <el-tag
                  v-if="index === 0"
                  type="warning"
                  effect="dark"
                  class="top-tag"
                >
                  最匹配
                </el-tag>
              </div>
              <div class="job-meta">
                <span class="company-name">
                  <el-icon><OfficeBuilding /></el-icon>
                  {{ job.company }}
                </span>
                <span class="city-name">
                  <el-icon><Location /></el-icon>
                  {{ job.city }}
                </span>
                <el-tag v-if="job.tags" type="info" size="small">{{
                  job.tags
                }}</el-tag>
              </div>
            </div>
            <!-- 职责和技术要求 -->
            <div class="job-requirements" v-if="job.searchable_text">
              <div class="requirements-title">
                <el-icon><List /></el-icon>
                <span>岗位要求</span>
              </div>
              <div class="requirements-content">
                <div
                  class="requirements-text"
                  v-html="formatRequirements(job.searchable_text)"
                ></div>
              </div>
            </div>
            <div class="job-reason">
              <div class="reason-title">
                <el-icon><Star /></el-icon>
                <span>推荐理由</span>
              </div>
              <div
                class="reason-content"
                v-html="formatReason(job.reason)"
              ></div>
            </div>
            <div class="job-footer">
              <div class="job-score" v-if="getJobScore(job) !== null">
                <span class="score-label">匹配度：</span>
                <el-progress
                  :percentage="calculateScore(job)"
                  :color="getScoreColor(job)"
                  :stroke-width="8"
                  :show-text="false"
                />
                <span class="score-value">{{ formatScoreValue(job) }}</span>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 空状态 -->
    <div
      class="empty-state"
      v-if="!uploading && jobList.length === 0 && !hasUploaded"
    >
      <el-empty description="请上传简历文件开始智能匹配">
        <el-icon class="empty-icon"><Document /></el-icon>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { ElMessage } from "element-plus";
import {
  Upload,
  UploadFilled,
  Search,
  Briefcase,
  OfficeBuilding,
  Location,
  Star,
  Document,
  List,
} from "@element-plus/icons-vue";
import { http } from "@/utils/request.js";

// 上传相关
const uploadRef = ref(null);
const fileList = ref([]);
const uploading = ref(false);
const hasUploaded = ref(false);
const uploadProgress = ref(0);
const currentFile = ref(null);

// 结果相关
const jobList = ref([]);
const resultMessage = ref("");

// 上传前验证
const beforeUpload = (file) => {
  const isValidType =
    file.type === "application/pdf" ||
    file.type ===
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ||
    file.type === "application/msword" ||
    file.type === "text/plain";
  const isLt10M = file.size / 1024 / 1024 < 10;

  if (!isValidType) {
    ElMessage.error("只能上传 PDF、DOC、DOCX、TXT 格式的文件!");
    return false;
  }
  if (!isLt10M) {
    ElMessage.error("文件大小不能超过 10MB!");
    return false;
  }
  return true;
};

// 文件选择变化
const handleFileChange = (file, fileList) => {
  currentFile.value = file.raw;
};

// 提交上传
const submitUpload = async () => {
  if (!currentFile.value) {
    ElMessage.warning("请先选择文件");
    return;
  }

  uploading.value = true;
  uploadProgress.value = 0;

  try {
    // 模拟上传进度
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 10;
      }
    }, 200);

    // 创建 FormData 对象
    const formData = new FormData();
    formData.append("resume", currentFile.value);

    // 调用简历推荐接口
    const response = await http.postupload("/job/recommend/", formData);

    clearInterval(progressInterval);
    uploadProgress.value = 100;

    // 处理响应
    if (response.code === 200) {
      resultMessage.value = response.message || "岗位推荐成功";
      // 处理返回的职位数据，并按 _fused_score 倒序排列
      jobList.value = (response.data || [])
        .map((job) => ({
          id: job.id || job.job_id,
          title: job.title || "",
          company: job.company || "",
          city: job.city || "",
          tags: job.tags || "",
          money: job.money || "",
          education: job.education || "",
          job_type: job.job_type || "",
          working_years: job.working_years || "",
          jobcate: job.jobcate || "",
          searchable_text: job.searchable_text || "",
          description: job.description || "",
          reason: job.reason || "",
          _es_score: job._es_score,
          _vec_score: job._vec_score,
          _fused_score: job._fused_score,
        }))
        .sort((a, b) => {
          // 按 _fused_score 倒序排列（从高到低）
          const scoreA = a._fused_score || 0;
          const scoreB = b._fused_score || 0;
          return scoreB - scoreA;
        });
      hasUploaded.value = true;
      ElMessage.success(resultMessage.value);
    } else {
      ElMessage.error(response.message || "推荐失败，请重试");
      jobList.value = [];
    }
  } catch (error) {
    console.error("Upload error:", error);
    ElMessage.error(
      error.response?.data?.message ||
        error.message ||
        "上传失败，请检查网络连接或稍后重试"
    );
    jobList.value = [];
  } finally {
    uploading.value = false;
    setTimeout(() => {
      uploadProgress.value = 0;
    }, 1000);
  }
};

// 清除文件
const clearFiles = () => {
  uploadRef.value.clearFiles();
  fileList.value = [];
  currentFile.value = null;
  jobList.value = [];
  hasUploaded.value = false;
  resultMessage.value = "";
  uploadProgress.value = 0;
};

// 格式化岗位要求（解析 searchable_text）
const formatRequirements = (text) => {
  if (!text) return "";

  // 按换行符分割
  const lines = text.split("\n").filter((line) => line.trim());

  if (lines.length === 0) return "";

  // 第一行通常是岗位标题，跳过
  // 从第二行开始是要求列表
  const requirements = lines.slice(1);

  if (requirements.length === 0) {
    // 如果没有要求列表，直接显示整个文本
    return text.replace(/\n/g, "<br>");
  }

  // 格式化要求列表
  let formatted = "";
  requirements.forEach((req) => {
    // 跳过标签和学历等单行信息（通常是短文本且不包含数字编号）
    if (req.length < 20 && !req.match(/^\d+[\.、]/)) {
      // 可能是标签或学历，用特殊样式显示
      formatted += `<div class="requirement-tag">${req}</div>`;
    } else {
      // 检查是否是编号列表（如 "1.xxx" 或 "1、xxx"）
      const numberedMatch = req.match(/^(\d+)[\.、]\s*(.+)$/);
      if (numberedMatch) {
        formatted += `<div class="requirement-item"><span class="req-number">${numberedMatch[1]}.</span> <span class="req-text">${numberedMatch[2]}</span></div>`;
      } else {
        // 普通文本要求
        formatted += `<div class="requirement-item"><span class="req-text">${req}</span></div>`;
      }
    }
  });

  return formatted;
};

// 格式化推荐理由（将换行符转换为HTML）
const formatReason = (reason) => {
  if (!reason) return "";
  // 将换行符转换为 <br>，保留项目符号
  return reason
    .replace(/\n/g, "<br>")
    .replace(/•/g, "•")
    .replace(/<br>\s*•/g, "<br>•"); // 确保项目符号前有换行
};

// 获取岗位分数（优先使用 _fused_score）
const getJobScore = (job) => {
  if (job._fused_score !== undefined && job._fused_score !== null) {
    return { type: "fused", value: job._fused_score };
  }
  if (job._vec_score !== undefined && job._vec_score !== null) {
    return { type: "vec", value: job._vec_score };
  }
  if (job._es_score !== undefined && job._es_score !== null) {
    return { type: "es", value: job._es_score };
  }
  return null;
};

// 计算匹配度百分比
const calculateScore = (job) => {
  const scoreInfo = getJobScore(job);
  if (!scoreInfo) return 0;

  if (scoreInfo.type === "fused") {
    // _fused_score 通常是 0-1 之间的小数（如 0.79）
    // 直接乘以 100 转换为百分比
    const percentage = Math.round(scoreInfo.value * 100);
    return Math.min(Math.max(percentage, 0), 100);
  } else if (scoreInfo.type === "vec") {
    // _vec_score 通常是 0-2 之间的相似度分数
    // 将其转换为 0-100 的百分比
    const percentage = Math.min(Math.round((scoreInfo.value / 2) * 100), 100);
    return Math.max(percentage, 0);
  } else {
    // _es_score 可能是更大的数值（如 249.28）
    // 假设最大分数是 300，可以根据实际情况调整
    const maxScore = 300;
    return Math.min(Math.round((scoreInfo.value / maxScore) * 100), 100);
  }
};

// 格式化分数显示值
const formatScoreValue = (job) => {
  const scoreInfo = getJobScore(job);
  if (!scoreInfo) return "0%";

  if (scoreInfo.type === "fused") {
    // _fused_score 显示为百分比形式（如 0.79 -> 79%）
    const percentage = scoreInfo.value * 100;
    return `${percentage.toFixed(1)}%`;
  } else if (scoreInfo.type === "vec") {
    // _vec_score 显示为百分比形式
    const percentage = (scoreInfo.value / 2) * 100;
    return `${percentage.toFixed(1)}%`;
  } else {
    // _es_score 显示原始值
    return scoreInfo.value.toFixed(2);
  }
};

// 根据分数获取颜色
const getScoreColor = (job) => {
  const percentage = calculateScore(job);
  if (percentage >= 80) return "#67c23a";
  if (percentage >= 60) return "#e6a23c";
  return "#f56c6c";
};
</script>

<style scoped>
.recommend-job-container {
  min-height: calc(100vh - 120px);
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 12px;
  background: linear-gradient(135deg, #00c2b3 0%, #00e0be 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-desc {
  font-size: 16px;
  color: #606266;
  margin: 0;
}

.upload-section {
  max-width: 800px;
  margin: 0 auto 40px;
}

.upload-card {
  border-radius: 16px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.card-header .el-icon {
  font-size: 20px;
  color: #00c2b3;
}

.upload-content {
  padding: 20px;
}

.upload-dragger {
  width: 100%;
}

:deep(.el-upload-dragger) {
  width: 100%;
  height: 200px;
  border: 2px dashed #d9d9d9;
  border-radius: 12px;
  background: #fafafa;
  transition: all 0.3s;
}

:deep(.el-upload-dragger:hover) {
  border-color: #00c2b3;
  background: #f0fdfc;
}

:deep(.el-icon--upload) {
  font-size: 48px;
  color: #00c2b3;
  margin-bottom: 16px;
}

:deep(.el-upload__text) {
  color: #606266;
  font-size: 16px;
}

:deep(.el-upload__text em) {
  color: #00c2b3;
  font-style: normal;
  font-weight: 600;
}

:deep(.el-upload__tip) {
  color: #909399;
  font-size: 14px;
  margin-top: 12px;
}

.upload-actions {
  margin-top: 24px;
  display: flex;
  justify-content: center;
  gap: 16px;
}

.upload-progress {
  margin-top: 20px;
  padding: 0 20px;
}

:deep(.upload-progress .el-progress) {
  width: 100%;
}

.results-section {
  max-width: 1200px;
  margin: 0 auto;
}

.results-card {
  border-radius: 16px;
  overflow: hidden;
}

.success-tag {
  margin-left: auto;
  font-size: 14px;
}

.job-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.job-card {
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  padding: 24px;
  transition: all 0.3s;
  cursor: pointer;
}

.job-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.job-card-highlight {
  border: 2px solid #00c2b3;
  background: linear-gradient(135deg, #ffffff 0%, #f0fdfc 100%);
  box-shadow: 0 4px 16px rgba(0, 194, 179, 0.15);
}

.job-header {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.job-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.job-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0;
  flex: 1;
}

.top-tag {
  font-size: 12px;
  padding: 4px 12px;
}

.job-meta {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}

.company-name,
.city-name {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #606266;
  font-size: 14px;
}

.company-name .el-icon,
.city-name .el-icon {
  font-size: 16px;
  color: #909399;
}

.job-requirements {
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.requirements-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
}

.requirements-title .el-icon {
  color: #409eff;
  font-size: 18px;
}

.requirements-content {
  color: #606266;
  font-size: 14px;
  line-height: 1.8;
}

.requirements-text {
  padding: 12px;
  background: #f0f7ff;
  border-radius: 8px;
  border-left: 3px solid #409eff;
}

.requirement-item {
  margin-bottom: 8px;
  padding-left: 4px;
  display: flex;
  align-items: flex-start;
}

.requirement-item:last-child {
  margin-bottom: 0;
}

.req-number {
  color: #409eff;
  font-weight: 600;
  margin-right: 8px;
  min-width: 20px;
  display: inline-block;
}

.req-text {
  flex: 1;
  word-break: break-word;
}

.requirement-tag {
  display: inline-block;
  padding: 4px 12px;
  margin: 4px 8px 4px 0;
  background: #e6f4ff;
  color: #409eff;
  border-radius: 12px;
  font-size: 13px;
  border: 1px solid #b3d8ff;
}

.job-reason {
  margin-bottom: 16px;
}

.reason-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
}

.reason-title .el-icon {
  color: #f39c12;
  font-size: 18px;
}

.reason-content {
  color: #606266;
  font-size: 15px;
  line-height: 1.8;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 3px solid #00c2b3;
}

.job-footer {
  display: flex;
  align-items: center;
  gap: 12px;
}

.job-score {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.score-label {
  font-size: 14px;
  color: #909399;
  white-space: nowrap;
}

.score-value {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  min-width: 60px;
  text-align: right;
}

:deep(.el-progress) {
  flex: 1;
}

.empty-state {
  max-width: 600px;
  margin: 60px auto;
  text-align: center;
}

.empty-icon {
  font-size: 80px;
  color: #d3d4d6;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .recommend-job-container {
    padding: 20px 12px;
  }

  .page-title {
    font-size: 24px;
  }

  .job-card {
    padding: 16px;
  }

  .job-title {
    font-size: 18px;
  }

  .job-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
