<template>
  <div class="verify-page">
    <header class="page-header">
      <div>
        <h2>学历验证</h2>
        <p class="sub">输入学历验证码，获取验证结果</p>
      </div>
    </header>

    <section class="card">
      <div class="form">
        <label>验证码</label>
        <input
          v-model="code"
          type="text"
          placeholder="请输入学历验证码"
          @keydown.enter.prevent="handleVerify"
        />
        <div class="actions">
          <button
            class="primary-btn"
            :disabled="loading || !code.trim()"
            @click="handleVerify"
          >
            {{ loading ? "验证中..." : "验证" }}
          </button>
          <button class="ghost-btn" @click="reset" :disabled="loading">
            重置
          </button>
        </div>
      </div>
    </section>

    <section class="card result" v-if="result">
      <h3>验证结果</h3>
      <pre>{{ result }}</pre>
    </section>

    <section class="card empty" v-else>
      <p class="placeholder">提交验证码后，将显示验证结果</p>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";
import { http } from "@/utils/request";

const code = ref("");
const loading = ref(false);
const result = ref("");

const handleVerify = async () => {
  if (!code.value.trim()) {
    ElMessage.warning("请输入学历验证码");
    return;
  }
  loading.value = true;
  result.value = "";
  try {
    // TODO: 如后端接口路径不同，请替换为实际的验证接口
    const res = await http.post("/call/check_education/", {
      question: `帮我验证学历：${code.value.trim()}`,
    });
    // 后端返回可能是 { message, data } 或直接 data，做兼容处理
    result.value = res?.data || res?.message || JSON.stringify(res, null, 2);
    ElMessage.success("验证完成");
  } catch (err) {
    console.error(err);
    ElMessage.error("验证失败，请稍后重试");
  } finally {
    loading.value = false;
  }
};

const reset = () => {
  code.value = "";
  result.value = "";
};
</script>

<style scoped>
.verify-page {
  padding: 18px 18px 28px;
  background: #f5f7fb;
  min-height: 100vh;
  box-sizing: border-box;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  color: #0f172a;
}

.sub {
  margin: 4px 0 0 0;
  color: #6b7280;
  font-size: 13px;
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  margin-bottom: 12px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

label {
  font-size: 13px;
  color: #6b7280;
}

input {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 14px;
  outline: none;
  box-sizing: border-box;
}

input:focus {
  border-color: #00a6d6;
  box-shadow: 0 0 0 2px rgba(0, 166, 214, 0.1);
}

.actions {
  display: flex;
  gap: 10px;
}

.primary-btn {
  background: #00bebd;
  color: #fff;
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.primary-btn:hover {
  background: #00a6d6;
}

.primary-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

.ghost-btn {
  border: 1px solid #e5e7eb;
  background: #fff;
  color: #374151;
  padding: 10px 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.ghost-btn:hover {
  border-color: #00a6d6;
  color: #00a6d6;
  background: #f0f9ff;
}

.result pre {
  background: #f8fafc;
  border-radius: 10px;
  padding: 12px;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 14px;
  line-height: 1.6;
  border: 1px solid #e5e7eb;
}

.empty .placeholder {
  color: #9ca3af;
  margin: 0;
  text-align: center;
}
</style>
