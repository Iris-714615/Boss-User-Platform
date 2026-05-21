<template>
  <div class="post-job-page">
    <header class="page-header">
      <div>
        <h2>职位发布</h2>
        <p class="sub">发布新的招聘职位，吸引优秀人才</p>
      </div>
    </header>

    <section class="card">
      <el-form
        :model="form"
        :rules="rules"
        ref="formRef"
        label-width="120px"
        class="job-form"
      >
        <el-form-item label="职位名称" prop="title">
          <el-input
            v-model="form.title"
            placeholder="请输入职位名称，如：前端开发工程师"
            clearable
          />
        </el-form-item>

        <el-form-item label="工作城市" prop="city">
          <el-select
            v-model="form.city"
            placeholder="请选择工作城市"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="city in cities"
              :key="city"
              :label="city"
              :value="city"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="工作经验" prop="experience">
          <el-select
            v-model="form.experience"
            placeholder="请选择工作经验要求"
            clearable
            style="width: 100%"
          >
            <el-option label="不限" value="不限" />
            <el-option label="1年以下" value="1年以下" />
            <el-option label="1-3年" value="1-3年" />
            <el-option label="3-5年" value="3-5年" />
            <el-option label="5-10年" value="5-10年" />
            <el-option label="10年以上" value="10年以上" />
          </el-select>
        </el-form-item>

        <el-form-item label="学历要求" prop="education">
          <el-select
            v-model="form.education"
            placeholder="请选择学历要求"
            clearable
            style="width: 100%"
          >
            <el-option label="不限" value="不限" />
            <el-option label="高中" value="高中" />
            <el-option label="大专" value="大专" />
            <el-option label="本科" value="本科" />
            <el-option label="硕士" value="硕士" />
            <el-option label="博士" value="博士" />
          </el-select>
        </el-form-item>

        <el-form-item label="薪资范围" prop="salary">
          <el-input
            v-model="form.salary"
            placeholder="如：10-20K、面议"
            clearable
          />
        </el-form-item>

        <el-form-item label="职位类型" prop="jobType">
          <el-radio-group v-model="form.jobType">
            <el-radio label="全职">全职</el-radio>
            <el-radio label="兼职">兼职</el-radio>
            <el-radio label="实习">实习</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="工作地点" prop="address">
          <el-input
            v-model="form.address"
            placeholder="请输入详细工作地址"
            clearable
          />
        </el-form-item>

        <el-form-item label="职位描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="6"
            placeholder="请输入职位描述，包括工作内容、职责等"
            clearable
          />
        </el-form-item>

        <el-form-item label="职位要求" prop="requirements">
          <el-input
            v-model="form.requirements"
            type="textarea"
            :rows="6"
            placeholder="请输入职位要求，包括技能、经验等"
            clearable
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            发布职位
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { ElMessage } from "element-plus";
import { http } from "@/utils/request";

const formRef = ref(null);
const loading = ref(false);

const form = reactive({
  title: "",
  city: "",
  experience: "",
  education: "",
  salary: "",
  jobType: "全职",
  address: "",
  description: "",
  requirements: "",
});

const rules = {
  title: [{ required: true, message: "请输入职位名称", trigger: "blur" }],
  city: [{ required: true, message: "请选择工作城市", trigger: "change" }],
  salary: [{ required: true, message: "请输入薪资范围", trigger: "blur" }],
};

const cities = [
  "北京",
  "上海",
  "广州",
  "深圳",
  "杭州",
  "南京",
  "成都",
  "武汉",
  "西安",
  "重庆",
  "其他",
];

const handleSubmit = async () => {
  if (!formRef.value) return;

  try {
    await formRef.value.validate();
    loading.value = true;

    // TODO: 调用发布职位接口
    // const response = await http.post("/hr/jobs/create/", form);
    
    // 模拟API调用
    await new Promise((resolve) => setTimeout(resolve, 1000));
    
    ElMessage.success("职位发布成功！");
    
    // 重置表单
    handleReset();
  } catch (error) {
    console.error("表单验证失败:", error);
  } finally {
    loading.value = false;
  }
};

const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields();
  }
  Object.assign(form, {
    title: "",
    city: "",
    experience: "",
    education: "",
    salary: "",
    jobType: "全职",
    address: "",
    description: "",
    requirements: "",
  });
};
</script>

<style scoped>
.post-job-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.page-header {
  background: #fff;
  border-radius: 12px;
  padding: 20px 24px;
  border: 1px solid #eef0f4;
}

.page-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.page-header .sub {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  border: 1px solid #eef0f4;
}

.job-form {
  max-width: 800px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
}

:deep(.el-textarea__inner) {
  border-radius: 8px;
}
</style>


