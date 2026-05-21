<template>
  <div class="hr-assistant-page">
    <header class="assistant-header">
      <div>
        <h2>人事助手 · RAG 问答</h2>
        <p class="sub">HR 可就入转调离、合同、考勤、福利等问题直接提问</p>
      </div>
      <div class="status">
        <span class="dot"></span> 知识库在线
      </div>
    </header>

    <div class="chat-box" ref="chatBox">
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="message"
        :class="msg.role === 'user' ? 'user' : 'ai'"
      >
        <div class="avatar">{{ msg.role === 'user' ? '我' : '助理' }}</div>
        <div class="bubble">
          <div class="text" v-html="msg.content"></div>
          <div class="time">{{ formatTime(msg.time) }}</div>
        </div>
      </div>
      <div v-if="loading" class="typing">
        <div class="avatar">AI</div>
        <div class="bubble typing-bubble">
          <span></span><span></span><span></span>
        </div>
      </div>
    </div>

    <div class="input-area">
      <textarea
        v-model="input"
        class="input"
        rows="2"
        placeholder="例如：帮我生成入职流程清单 / 试用期到期提醒怎么配置？"
        @keydown.enter.prevent="handleEnter"
      ></textarea>
      <button class="send-btn" :disabled="!input.trim() || loading" @click="send">
        {{ loading ? "思考中..." : "发送" }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";
import { ElMessage } from "element-plus";
import { http } from "@/utils/request";

const messages = ref([
  {
    id: 1,
    role: "ai",
    content:
      "您好，我是人事助手。可以咨询入职、转正、合同、请假、社保、公积金等问题。",
    time: new Date(),
  },
]);
const input = ref("");
const loading = ref(false);
const chatBox = ref(null);

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight;
  });
};

const formatTime = (time) =>
  new Intl.DateTimeFormat("zh-CN", {
    hour: "2-digit",
    minute: "2-digit",
  }).format(time);

const send = async () => {
  if (!input.value.trim() || loading.value) return;
  const question = input.value.trim();

  messages.value.push({
    id: Date.now(),
    role: "user",
    content: question,
    time: new Date(),
  });
  input.value = "";
  loading.value = true;
  scrollToBottom();

  try {
    const res = await http.post("/rag/hr_query/", { question });
    const answer = res?.data || res?.message || "";

    messages.value.push({
      id: Date.now() + 1,
      role: "ai",
      content: (answer || "抱歉，暂无回答").replace(/\n/g, "<br>"),
      time: new Date(),
    });
  } catch (error) {
    console.error(error);
    ElMessage.error("接口调用失败，请稍后重试");
    messages.value.push({
      id: Date.now() + 1,
      role: "ai",
      content: "抱歉，接口调用失败，请稍后重试。",
      time: new Date(),
    });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};

const handleEnter = (e) => {
  if (!e.shiftKey) {
    send();
  } else {
    input.value += "\n";
  }
};
</script>

<style scoped>
.hr-assistant-page {
  height: 100vh;
  background: #f5f7fb;
  display: flex;
  flex-direction: column;
  padding: 18px 18px 12px;
  box-sizing: border-box;
}

.assistant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.assistant-header h2 {
  margin: 0;
  font-size: 20px;
  color: #0f172a;
}

.sub {
  margin: 4px 0 0 0;
  color: #6b7280;
  font-size: 13px;
}

.status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #10b981;
  background: #ecfdf3;
  padding: 6px 10px;
  border-radius: 10px;
  border: 1px solid #d1fae5;
}

.dot {
  width: 8px;
  height: 8px;
  background: #10b981;
  border-radius: 50%;
  display: inline-block;
}

.chat-box {
  flex: 1;
  background: #fff;
  border-radius: 12px;
  padding: 14px;
  overflow-y: auto;
  border: 1px solid #e5e7eb;
}

.message {
  display: flex;
  margin-bottom: 12px;
  gap: 10px;
}

.message.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e5e7eb;
  display: grid;
  place-items: center;
  font-size: 13px;
  color: #111827;
  flex-shrink: 0;
}

.bubble {
  max-width: 70%;
  background: #f3f4f6;
  border-radius: 12px;
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
}

.message.user .bubble {
  background: #00bebd;
  color: #fff;
  border: none;
}

.text {
  font-size: 14px;
  line-height: 1.6;
  color: inherit;
  white-space: pre-wrap;
}

.time {
  margin-top: 4px;
  font-size: 12px;
  color: #6b7280;
}

.message.user .time {
  color: #e0f7f7;
}

.typing {
  display: flex;
  gap: 10px;
  align-items: center;
}

.typing-bubble {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 8px 12px;
}

.typing-bubble span {
  width: 8px;
  height: 8px;
  background: #9ca3af;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-bubble span:nth-child(2) {
  animation-delay: -0.2s;
}
.typing-bubble span:nth-child(3) {
  animation-delay: -0.4s;
}

@keyframes typing {
  0%,
  80%,
  100% {
    transform: scale(0.8);
    opacity: 0.4;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.input-area {
  margin-top: 12px;
  display: flex;
  gap: 10px;
}

.input {
  flex: 1;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  padding: 10px 12px;
  font-size: 14px;
  min-height: 44px;
  resize: vertical;
  box-sizing: border-box;
  outline: none;
}

.input:focus {
  border-color: #00a6d6;
  box-shadow: 0 0 0 2px rgba(0, 166, 214, 0.1);
}

.send-btn {
  width: 110px;
  border: none;
  border-radius: 10px;
  background: #00bebd;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.send-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

.send-btn:not(:disabled):hover {
  background: #00a6d6;
}
</style>


