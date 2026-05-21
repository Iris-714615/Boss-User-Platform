<template>
  <div class="resume-generator">
    <div class="resume-header">
      <h1>智能简历生成</h1>
      <p>AI驱动的简历优化工具，让你的简历脱颖而出</p>
    </div>

    <div class="resume-steps">
      <div 
        v-for="(step, index) in steps" 
        :key="step.id"
        class="step-item"
        :class="{ active: currentStep === step.id, completed: completedSteps.includes(step.id) }"
      >
        <div class="step-number">{{ index + 1 }}</div>
        <div class="step-title">{{ step.title }}</div>
      </div>
    </div>

    <div class="resume-content">
      <!-- 基础信息 -->
      <div v-if="currentStep === 1" class="step-content">
        <h2>个人基础信息</h2>
        <form class="info-form">
          <div class="form-row">
            <div class="form-group">
              <label>姓名</label>
              <input v-model="basicInfo.name" type="text" placeholder="请输入姓名">
            </div>
            <div class="form-group">
              <label>性别</label>
              <select v-model="basicInfo.gender">
                <option value="">请选择</option>
                <option value="男">男</option>
                <option value="女">女</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>手机号码</label>
              <input v-model="basicInfo.phone" type="tel" placeholder="请输入手机号码">
            </div>
            <div class="form-group">
              <label>邮箱</label>
              <input v-model="basicInfo.email" type="email" placeholder="请输入邮箱">
            </div>
          </div>
          <div class="form-group">
            <label>个人简介</label>
            <textarea v-model="basicInfo.summary" placeholder="请简要介绍自己"></textarea>
          </div>
        </form>
      </div>

      <!-- 教育经历 -->
      <div v-if="currentStep === 2" class="step-content">
        <h2>教育经历</h2>
        <div v-for="(edu, index) in education" :key="index" class="edu-item">
          <div class="form-row">
            <div class="form-group">
              <label>学校名称</label>
              <input v-model="edu.school" type="text" placeholder="请输入学校名称">
            </div>
            <div class="form-group">
              <label>学历</label>
              <select v-model="edu.degree">
                <option value="">请选择</option>
                <option value="高中">高中</option>
                <option value="大专">大专</option>
                <option value="本科">本科</option>
                <option value="硕士">硕士</option>
                <option value="博士">博士</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>专业</label>
              <input v-model="edu.major" type="text" placeholder="请输入专业">
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>开始时间</label>
                <input v-model="edu.startDate" type="date">
              </div>
              <div class="form-group">
                <label>结束时间</label>
                <input v-model="edu.endDate" type="date">
              </div>
            </div>
          </div>
          <button class="remove-btn" @click="removeEducation(index)">删除</button>
        </div>
        <button class="add-btn" @click="addEducation">添加教育经历</button>
      </div>

      <!-- 工作/项目经历 -->
      <div v-if="currentStep === 3" class="step-content">
        <h2>工作/项目经历</h2>
        <div v-for="(exp, index) in experience" :key="index" class="exp-item">
          <div class="form-row">
            <div class="form-group">
              <label>公司/项目名称</label>
              <input v-model="exp.company" type="text" placeholder="请输入公司或项目名称">
            </div>
            <div class="form-group">
              <label>职位</label>
              <input v-model="exp.position" type="text" placeholder="请输入职位">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>开始时间</label>
              <input v-model="exp.startDate" type="date">
            </div>
            <div class="form-group">
              <label>结束时间</label>
              <input v-model="exp.endDate" type="date">
            </div>
          </div>
          <div class="form-group">
            <label>工作描述</label>
            <textarea v-model="exp.description" placeholder="请描述你的工作内容和成果"></textarea>
          </div>
          <button class="remove-btn" @click="removeExperience(index)">删除</button>
        </div>
        <button class="add-btn" @click="addExperience">添加经历</button>
      </div>

      <!-- 技能特长 -->
      <div v-if="currentStep === 4" class="step-content">
        <h2>技能特长</h2>
        <div class="skills-container">
          <div v-for="(skill, index) in skills" :key="index" class="skill-item">
            <input v-model="skill.name" type="text" placeholder="技能名称">
            <input v-model="skill.level" type="number" min="1" max="5" placeholder="熟练度 1-5">
            <button class="remove-btn" @click="removeSkill(index)">删除</button>
          </div>
        </div>
        <button class="add-btn" @click="addSkill">添加技能</button>
        <div class="form-group">
          <label>证书</label>
          <textarea v-model="certificates" placeholder="请列出你的证书"></textarea>
        </div>
      </div>

      <!-- 求职期望 -->
      <div v-if="currentStep === 5" class="step-content">
        <h2>求职期望</h2>
        <div class="form-row">
          <div class="form-group">
            <label>目标职位</label>
            <input v-model="expectation.position" type="text" placeholder="请输入目标职位">
          </div>
          <div class="form-group">
            <label>期望薪资</label>
            <input v-model="expectation.salary" type="text" placeholder="请输入期望薪资">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>期望城市</label>
            <input v-model="expectation.city" type="text" placeholder="请输入期望城市">
          </div>
          <div class="form-group">
            <label>工作性质</label>
            <select v-model="expectation.type">
              <option value="">请选择</option>
              <option value="全职">全职</option>
              <option value="兼职">兼职</option>
              <option value="实习">实习</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label>职业规划</label>
          <textarea v-model="expectation.plan" placeholder="请描述你的职业规划"></textarea>
        </div>
      </div>

      <!-- 简历生成 -->
      <div v-if="currentStep === 6" class="step-content">
        <h2>简历生成</h2>
        <div class="template-selection">
          <h3>选择模板</h3>
          <div class="template-grid">
            <div 
              v-for="template in templates" 
              :key="template.id"
              class="template-item"
              :class="{ selected: selectedTemplate === template.id }"
              @click="selectedTemplate = template.id"
            >
              <div class="template-preview">{{ template.preview }}</div>
              <div class="template-name">{{ template.name }}</div>
              <div class="template-tag">{{ template.tag }}</div>
            </div>
          </div>
        </div>
        <div class="generate-options">
          <div class="form-group">
            <label>目标岗位类型</label>
            <select v-model="generateOptions.positionType">
              <option value="">请选择</option>
              <option value="前端开发">前端开发</option>
              <option value="后端开发">后端开发</option>
              <option value="产品经理">产品经理</option>
              <option value="UI设计">UI设计</option>
              <option value="销售">销售</option>
            </select>
          </div>
          <div class="form-group">
            <label>人群类型</label>
            <select v-model="generateOptions.userType">
              <option value="">请选择</option>
              <option value="应届生">应届生</option>
              <option value="社招">社招</option>
              <option value="转行">转行</option>
            </select>
          </div>
        </div>
        <button class="generate-btn" @click="generateResume">生成简历</button>
      </div>

      <!-- 简历预览 -->
      <div v-if="currentStep === 7" class="step-content">
        <h2>简历预览</h2>
        <div class="resume-preview">
          <div v-if="generatedResume" class="resume-content">
            <h3>{{ generatedResume.name }}</h3>
            <p>{{ generatedResume.phone }} | {{ generatedResume.email }}</p>
            <h4>个人简介</h4>
            <p>{{ generatedResume.summary }}</p>
            <h4>教育经历</h4>
            <div v-for="(edu, index) in generatedResume.education" :key="index">
              <p>{{ edu.school }} - {{ edu.major }} ({{ edu.degree }})</p>
              <p>{{ edu.startDate }} - {{ edu.endDate }}</p>
            </div>
            <h4>工作经历</h4>
            <div v-for="(exp, index) in generatedResume.experience" :key="index">
              <p>{{ exp.company }} - {{ exp.position }}</p>
              <p>{{ exp.startDate }} - {{ exp.endDate }}</p>
              <p>{{ exp.description }}</p>
            </div>
            <h4>技能</h4>
            <p>{{ generatedResume.skills.map(s => s.name).join(', ') }}</p>
            <h4>求职期望</h4>
            <p>目标职位：{{ generatedResume.expectation.position }}</p>
            <p>期望薪资：{{ generatedResume.expectation.salary }}</p>
          </div>
          <div v-else class="loading">生成中...</div>
        </div>
        <div class="preview-actions">
          <button class="btn" @click="downloadResume">下载简历</button>
          <button class="btn" @click="editResume">重新编辑</button>
          <button class="btn" @click="changeTemplate">更换模板</button>
        </div>
      </div>
    </div>

    <div class="resume-actions">
      <button 
        class="action-btn prev" 
        @click="prevStep"
        :disabled="currentStep === 1"
      >
        上一步
      </button>
      <button 
        class="action-btn next" 
        @click="nextStep"
        :disabled="currentStep === 7"
      >
        {{ currentStep === 6 ? '生成简历' : '下一步' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { http } from "../../utils/request.js";

const currentStep = ref(1);
const completedSteps = ref([]);

const steps = [
  { id: 1, title: '个人基础信息' },
  { id: 2, title: '教育经历' },
  { id: 3, title: '工作/项目经历' },
  { id: 4, title: '技能特长' },
  { id: 5, title: '求职期望' },
  { id: 6, title: '简历生成' },
  { id: 7, title: '简历预览' }
];

// 基础信息
const basicInfo = ref({
  name: '',
  gender: '',
  phone: '',
  email: '',
  summary: ''
});

// 教育经历
const education = ref([{
  school: '',
  degree: '',
  major: '',
  startDate: '',
  endDate: ''
}]);

// 工作经历
const experience = ref([{
  company: '',
  position: '',
  startDate: '',
  endDate: '',
  description: ''
}]);

// 技能
const skills = ref([{
  name: '',
  level: 3
}]);

const certificates = ref('');

// 求职期望
const expectation = ref({
  position: '',
  salary: '',
  city: '',
  type: '',
  plan: ''
});

// 模板
const templates = [
  { id: 1, name: '简约商务', tag: 'ATS友好', preview: '📄' },
  { id: 2, name: '专业技术', tag: '技术岗', preview: '💻' },
  { id: 3, name: '创意美观', tag: '设计岗', preview: '🎨' },
  { id: 4, name: '销售精英', tag: '销售岗', preview: '💼' }
];

const selectedTemplate = ref(1);

// 生成选项
const generateOptions = ref({
  positionType: '',
  userType: ''
});

const generatedResume = ref(null);

// 方法
const addEducation = () => {
  education.value.push({
    school: '',
    degree: '',
    major: '',
    startDate: '',
    endDate: ''
  });
};

const removeEducation = (index) => {
  education.value.splice(index, 1);
  if (education.value.length === 0) {
    addEducation();
  }
};

const addExperience = () => {
  experience.value.push({
    company: '',
    position: '',
    startDate: '',
    endDate: '',
    description: ''
  });
};

const removeExperience = (index) => {
  experience.value.splice(index, 1);
  if (experience.value.length === 0) {
    addExperience();
  }
};

const addSkill = () => {
  skills.value.push({
    name: '',
    level: 3
  });
};

const removeSkill = (index) => {
  skills.value.splice(index, 1);
  if (skills.value.length === 0) {
    addSkill();
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
};

const nextStep = async () => {
  if (currentStep.value < 6) {
    // 保存当前步骤
    completedSteps.value.push(currentStep.value);
    currentStep.value++;
  } else if (currentStep.value === 6) {
    // 生成简历
    await generateResume();
  }
};

const generateResume = async () => {
  try {
    const response = await http({
      url: '/api/resume/generate/',
      method: 'post',
      data: {
        basicInfo: basicInfo.value,
        education: education.value,
        experience: experience.value,
        skills: skills.value,
        certificates: certificates.value,
        expectation: expectation.value,
        templateId: selectedTemplate.value,
        options: generateOptions.value
      }
    });
    generatedResume.value = response.data.resume;
    currentStep.value = 7;
  } catch (error) {
    console.error('生成简历失败:', error);
  }
};

const downloadResume = () => {
  // 下载简历逻辑
  console.log('下载简历');
};

const editResume = () => {
  currentStep.value = 1;
};

const changeTemplate = () => {
  currentStep.value = 6;
};
</script>

<style scoped>
.resume-generator {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.resume-header {
  text-align: center;
  margin-bottom: 40px;
}

.resume-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 10px;
}

.resume-header p {
  font-size: 16px;
  color: #666;
}

.resume-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 40px;
  padding: 0 20px;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex: 1;
}

.step-number {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 8px;
  transition: all 0.3s;
}

.step-title {
  font-size: 14px;
  color: #6b7280;
  text-align: center;
  transition: all 0.3s;
}

.step-item.active .step-number {
  background: #3b82f6;
  color: white;
}

.step-item.active .step-title {
  color: #3b82f6;
  font-weight: 500;
}

.step-item.completed .step-number {
  background: #10b981;
  color: white;
}

.step-item.completed .step-title {
  color: #10b981;
}

.step-content {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  margin-bottom: 30px;
}

.step-content h2 {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #1a1a1a;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.edu-item,
.exp-item {
  background: #f9fafb;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  position: relative;
}

.remove-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
}

.add-btn {
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s;
}

.add-btn:hover {
  background: #2563eb;
}

.skills-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.skill-item {
  display: flex;
  gap: 10px;
  align-items: center;
}

.skill-item input:first-child {
  flex: 2;
}

.skill-item input:last-child {
  width: 80px;
}

.template-selection {
  margin-bottom: 30px;
}

.template-selection h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.template-item {
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.template-item:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.1);
}

.template-item.selected {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.05);
}

.template-preview {
  font-size: 48px;
  margin-bottom: 12px;
}

.template-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.template-tag {
  font-size: 12px;
  color: #6b7280;
  background: #f3f4f6;
  padding: 2px 8px;
  border-radius: 12px;
  display: inline-block;
}

.generate-options {
  margin-bottom: 30px;
}

.generate-btn {
  background: #10b981;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 32px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.generate-btn:hover {
  background: #059669;
}

.resume-preview {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 40px;
  margin-bottom: 30px;
  min-height: 400px;
}

.loading {
  text-align: center;
  padding: 100px;
  color: #6b7280;
}

.preview-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn {
  padding: 10px 24px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.resume-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 40px;
}

.action-btn {
  padding: 12px 32px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn.prev {
  background: white;
  color: #374151;
  border: 1px solid #d1d5db;
}

.action-btn.prev:hover:not(:disabled) {
  border-color: #3b82f6;
  color: #3b82f6;
}

.action-btn.next {
  background: #3b82f6;
  color: white;
  border: none;
}

.action-btn.next:hover:not(:disabled) {
  background: #2563eb;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .resume-steps {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .form-row {
    flex-direction: column;
  }
  
  .resume-actions {
    flex-direction: column;
    gap: 12px;
  }
  
  .action-btn {
    width: 100%;
  }
}
</style>