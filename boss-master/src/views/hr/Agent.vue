<template>
  <div class="agent-container">
    <!-- 助手头部 -->
    <div class="agent-header">
      <div class="agent-info">
        <div class="agent-avatar">
          <el-icon :size="32">
            <ChatDotRound />
          </el-icon>
        </div>
        <div class="agent-title">
          <h2>Boss智能招聘助手</h2>
          <div class="status-indicator">
            <span class="status-dot"></span>
            <span>在线</span>
          </div>
        </div>
      </div>
      <div class="header-actions">
        <el-button
          @click="showTools = !showTools"
          :type="showTools ? 'primary' : ''"
        >
          <el-icon>
            <Tools />
          </el-icon>
          工具
        </el-button>
        <el-button @click="clearChat">
          <el-icon>
            <Delete />
          </el-icon>
          清空
        </el-button>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="agent-content">
      <!-- 聊天消息区域 -->
      <div class="chat-messages" ref="messagesContainer">
        <!-- 欢迎消息 -->
        <div v-if="messages.length === 0" class="welcome-section">
          <div class="welcome-emoji">👋</div>
          <h2 class="welcome-title">欢迎使用Boss智能招聘助手</h2>
          <p class="welcome-desc">
            我可以帮助您进行招聘相关的工作,请选择或输入您的问题
          </p>
          <!-- 建议问题 -->
          <div class="suggestions">
            <el-button
              v-for="suggestion in suggestions"
              :key="suggestion"
              class="suggestion-btn"
              @click="sendMessage(suggestion)"
            >
              {{ suggestion }}
            </el-button>
          </div>
        </div>

        <!-- 消息列表 -->
        <div
          v-for="message in messages"
          :key="message.id"
          class="message-item"
          :class="{
            'user-message': message.type === 'user',
            'ai-message': message.type === 'ai',
          }"
        >
          <div class="message-avatar">
            <div v-if="message.type === 'user'" class="user-avatar">
              <el-icon>
                <User />
              </el-icon>
            </div>
            <div v-else class="ai-avatar">
              <el-icon>
                <ChatDotRound />
              </el-icon>
            </div>
          </div>
          <div class="message-content">
            <div
              class="message-text"
              v-html="formatMessage(message.content)"
            ></div>
            <div class="message-time">{{ formatTime(message.time) }}</div>
          </div>
        </div>

        <!-- 正在输入指示器 -->
        <div v-if="isTyping" class="message-item ai-message">
          <div class="message-avatar">
            <div class="ai-avatar">
              <el-icon>
                <ChatDotRound />
              </el-icon>
            </div>
          </div>
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="chat-input-area">
      <!-- 简历上传区域 -->
      <div v-if="uploadedFile" class="upload-file-info">
        <el-tag
          closable
          @close="removeFile"
          type="success"
          size="large"
          class="file-tag"
        >
          <el-icon class="file-icon">
            <Document />
          </el-icon>
          <span class="file-name">{{ uploadedFile.name }}</span>
          <span class="file-size"
            >({{ formatFileSize(uploadedFile.size) }})</span
          >
        </el-tag>
      </div>

      <div v-else class="upload-area">
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :limit="1"
          :on-change="handleFileChange"
          :before-upload="beforeUpload"
          accept=".pdf,.doc,.docx,.txt"
          class="resume-upload"
        >
          <template #trigger>
            <el-button type="info" plain size="small" class="upload-btn">
              <el-icon>
                <Upload />
              </el-icon>
              上传简历
            </el-button>
          </template>
        </el-upload>
      </div>
      <div class="input-container">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="1"
          placeholder="输入您的问题..."
          class="message-input"
          @keydown.enter.exact.prevent="handleSend"
          @keydown.shift.enter.exact="handleNewLine"
          :autosize="{ minRows: 1, maxRows: 4 }"
          resize="none"
        />
        <el-button
          type="primary"
          :loading="isTyping"
          @click="handleSend"
          class="send-btn"
        >
          发送
          <el-icon>
            <Right />
          </el-icon>
        </el-button>
      </div>
      <div class="input-tip">
        提示:您可以问我关于招聘的任何问题。按 Enter 发送, Shift + Enter 换行
      </div>
    </div>

    <!-- 工具弹窗 -->
    <el-dialog
      v-model="showTools"
      title="可用工具"
      width="80%"
      :close-on-click-modal="true"
      :close-on-press-escape="true"
      class="tools-dialog"
    >
      <template #header>
        <div class="dialog-header">
          <el-icon class="header-icon">
            <Tools />
          </el-icon>
          <span>可用工具 ({{ tools.length }})</span>
        </div>
      </template>
      <div class="tools-grid">
        <div
          v-for="tool in tools"
          :key="tool.id"
          class="tool-card"
          @click="handleToolClick(tool)"
        >
          <el-icon class="tool-icon">
            <Setting />
          </el-icon>
          <div class="tool-content">
            <h4 class="tool-name">{{ tool.name }}</h4>
            <p class="tool-desc">{{ tool.description }}</p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from "vue";
import { ElMessage } from "element-plus";
import {
  ChatDotRound,
  User,
  Tools,
  Delete,
  Setting,
  Right,
  Upload,
  Document,
} from "@element-plus/icons-vue";
import { http } from "@/utils/request.js";

// 状态管理
const showTools = ref(true);
const inputMessage = ref("");
const messages = ref([]);
const isTyping = ref(false);
const messagesContainer = ref(null);
const session_id = ref("");
const uploadRef = ref(null);
const uploadedFile = ref(null);

// 建议问题
const suggestions = ref([
  "帮我查询Python工程师职位",
  "推荐适合的候选人",
  "公司有什么福利?",
  "分析本月招聘数据",
]);

// 可用工具列表
const tools = ref([]);

// 发送建议问题
const sendMessage = (text) => {
  inputMessage.value = text;
  handleSend();
};

// 发送消息
const handleSend = async () => {
  if (!inputMessage.value.trim()) {
    ElMessage.warning("请输入您的问题");
    return;
  }

  // 添加用户消息
  const userMessage = {
    id: Date.now(),
    type: "user",
    content: inputMessage.value,
    time: new Date(),
  };
  messages.value.push(userMessage);

  let user_message = inputMessage.value;
  inputMessage.value = "";

  // 滚动到底部
  await nextTick();
  scrollToBottom();

  //开启ai回复输入加载动画
  isTyping.value = true;

  try {
    // 更新AI消息内容
    let sendMessage = {
      session_id: session_id.value,
      message: user_message,
    };
    if (uploadedFile.value) {
      sendMessage.resume = uploadedFile.value.raw;
    }
    let { data } = await http.postupload("/agent_app/hr_agent/", sendMessage);
    console.log("ai回复消息", data);

    // 先关闭正在输入指示器
    isTyping.value = false;

    if (data.output) {
      // 检测session_id是否有值，没有就缓存到本地
      if (!session_id.value && data.session_id) {
        localStorage.setItem("session_id", data.session_id);
        session_id.value = data.session_id;
      }

      // 添加AI消息占位符（在关闭isTyping之后）
      const aiMessageId = Date.now() + 1;
      const aiMessage = {
        id: aiMessageId,
        type: "ai",
        content: "",
        time: new Date(),
      };
      messages.value.push(aiMessage);

      // 等待DOM更新，确保正在输入指示器已隐藏
      await nextTick();

      // 流式输出效果（打字机效果）
      await streamTextOutput(data.output, aiMessageId);
    } else {
      // 如果没有输出，也创建一条错误消息
      const aiMessageId = Date.now() + 1;
      const aiMessage = {
        id: aiMessageId,
        type: "ai",
        content: "抱歉，我暂时无法回答这个问题。",
        time: new Date(),
      };
      messages.value.push(aiMessage);
    }
  } catch (error) {
    console.error("Chat error:", error);
    isTyping.value = false;
    // 创建错误消息
    const aiMessageId = Date.now() + 1;
    const aiMessage = {
      id: aiMessageId,
      type: "ai",
      content: "抱歉，发生了错误，请稍后重试。",
      time: new Date(),
    };
    messages.value.push(aiMessage);
    ElMessage.error("发送失败，请稍后重试");
  }

  // 滚动到底部
  await nextTick();
  scrollToBottom();

  console.log("聊天完成");
  uploadedFile.value = null;
};

// 换行处理
const handleNewLine = () => {
  // Shift + Enter 换行，不做任何处理
};

// 清空聊天
const clearChat = () => {
  messages.value = [];
  inputMessage.value = "";
  localStorage.removeItem("session_id");
  ElMessage.success("聊天记录已清空");
};

// 工具点击
const handleToolClick = (tool) => {
  ElMessage.info(`点击了工具: ${tool.name}`);
  // 可以根据工具类型执行相应操作
  // 点击后可以选择关闭弹窗
  // showTools.value = false;
};

// 文件上传前验证
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
  if (file.raw) {
    uploadedFile.value = {
      name: file.name,
      size: file.size,
      raw: file.raw,
    };
  }
};

// 移除文件
const removeFile = () => {
  uploadedFile.value = null;
  if (uploadRef.value) {
    uploadRef.value.clearFiles();
  }
};

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
};

// 流式输出文本（打字机效果）
const streamTextOutput = async (text, messageId) => {
  const msg = messages.value.find((m) => m.id === messageId);
  if (!msg) return;

  // 智能分词：将文本分割成合理的显示单元
  const tokens = [];
  let currentToken = "";

  for (let i = 0; i < text.length; i++) {
    const char = text[i];

    if (char === "\n") {
      // 换行符单独处理
      if (currentToken) {
        tokens.push(currentToken);
        currentToken = "";
      }
      tokens.push("\n");
    } else if (/[\u4e00-\u9fa5]/.test(char)) {
      // 中文字符，每个字符作为一个单元
      if (currentToken) {
        tokens.push(currentToken);
        currentToken = "";
      }
      tokens.push(char);
    } else if (/\s/.test(char)) {
      // 空格，如果当前有token则结束，空格本身也作为一个单元
      if (currentToken) {
        tokens.push(currentToken);
        currentToken = "";
      }
      tokens.push(char);
    } else {
      // 英文、数字、标点等，累积到当前token
      currentToken += char;
    }
  }

  // 处理最后一个token
  if (currentToken) {
    tokens.push(currentToken);
  }

  // 逐单元显示
  let currentIndex = 0;
  const speed = 30; // 每个单元的延迟时间（毫秒），可以根据需要调整

  const typeNextToken = () => {
    if (currentIndex < tokens.length) {
      msg.content += tokens[currentIndex];
      currentIndex++;

      // 滚动到底部（每5个token滚动一次，提高性能）
      if (currentIndex % 5 === 0 || currentIndex === tokens.length) {
        nextTick(() => {
          scrollToBottom();
        });
      }

      // 继续下一个单元
      setTimeout(typeNextToken, speed);
    } else {
      // 完成时确保滚动到底部
      nextTick(() => {
        scrollToBottom();
      });
    }
  };

  // 开始打字效果
  typeNextToken();
};

// 格式化消息内容
const formatMessage = (content) => {
  if (!content) return "";

  let formatted = content;

  // 处理表格格式（Markdown表格格式）
  const tableRegex = /(\|.+\|[\r\n]+(?:\|[-: ]+\|[\r\n]+)?(?:\|.+\|[\r\n]+)+)/g;
  formatted = formatted.replace(tableRegex, (match) => {
    const lines = match
      .trim()
      .split("\n")
      .filter((line) => line.trim());
    if (lines.length < 2) return match;

    let html = '<table class="message-table">';
    lines.forEach((line, index) => {
      if (index === 1) return; // 跳过分隔行
      const cells = line.split("|").filter((cell) => cell.trim());
      if (cells.length > 0) {
        html += "<tr>";
        cells.forEach((cell, cellIndex) => {
          const tag = index === 0 ? "th" : "td";
          html += `<${tag}>${cell.trim()}</${tag}>`;
        });
        html += "</tr>";
      }
    });
    html += "</table>";
    return html;
  });

  // 处理列表格式
  formatted = formatted.replace(
    /^(\d+)[\.、]\s+(.+)$/gm,
    '<div class="list-item"><span class="list-number">$1.</span> $2</div>',
  );
  formatted = formatted.replace(
    /^[•·]\s+(.+)$/gm,
    '<div class="list-item"><span class="list-bullet">•</span> $1</div>',
  );

  // 将剩余的换行符转换为 <br>
  formatted = formatted.replace(/\n/g, "<br>");

  // 处理加粗文本
  formatted = formatted.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");

  return formatted;
};

// 格式化时间
const formatTime = (time) => {
  if (!time) return "";
  const date = new Date(time);
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  return `${hours}:${minutes}`;
};

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// 定义获取全部工具的方法
const getTools = async () => {
  let { data } = await http.get("/agent_app/get_tools/");
  tools.value = data.tools;
};
onMounted(() => {
  scrollToBottom();
  getTools();
  session_id.value = localStorage.getItem("session_id") || "";
});
</script>

<style scoped>
.agent-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 60px);
  background: #f5f7fa;
}

.agent-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.agent-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.agent-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.agent-title h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
  font-size: 14px;
  color: #67c23a;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #67c23a;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.5;
  }
}

.header-actions {
  display: flex;
  gap: 12px;
}

.agent-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.tools-dialog :deep(.el-dialog__header) {
  padding: 20px 24px;
  border-bottom: 1px solid #e4e7ed;
}

.dialog-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.header-icon {
  font-size: 20px;
  color: #409eff;
}

.tools-dialog :deep(.el-dialog__body) {
  padding: 24px;
  max-height: 60vh;
  overflow-y: auto;
}

.tools-dialog :deep(.el-dialog) {
  border-radius: 12px;
}

.tools-dialog :deep(.el-dialog__header) {
  margin: 0;
}

.tools-dialog :deep(.el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid #e4e7ed;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.tool-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.tool-card:hover {
  background: #f0f7ff;
  border-color: #409eff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.15);
}

.tool-icon {
  font-size: 24px;
  color: #409eff;
  flex-shrink: 0;
}

.tool-content {
  flex: 1;
}

.tool-name {
  margin: 0 0 6px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.tool-desc {
  margin: 0;
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #f5f7fa;
}

.welcome-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
}

.welcome-emoji {
  font-size: 80px;
  margin-bottom: 24px;
  animation: wave 2s ease-in-out infinite;
}

@keyframes wave {
  0%,
  100% {
    transform: rotate(0deg);
  }

  25% {
    transform: rotate(20deg);
  }

  75% {
    transform: rotate(-20deg);
  }
}

.welcome-title {
  margin: 0 0 12px 0;
  font-size: 28px;
  font-weight: 600;
  color: #303133;
}

.welcome-desc {
  margin: 0 0 32px 0;
  font-size: 16px;
  color: #606266;
}

.suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  max-width: 800px;
}

.suggestion-btn {
  padding: 12px 24px;
  font-size: 15px;
  border-radius: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s;
}

.suggestion-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.user-avatar,
.ai-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.user-avatar {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: #fff;
}

.ai-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.message-content {
  max-width: 70%;
  min-width: 200px;
}

.user-message .message-content {
  text-align: right;
}

.message-text {
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.6;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.user-message .message-text {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: #fff;
  border-bottom-right-radius: 4px;
}

.ai-message .message-text {
  background: #fff;
  color: #303133;
  border: 1px solid #e4e7ed;
  border-bottom-left-radius: 4px;
}

.message-time {
  margin-top: 6px;
  font-size: 12px;
  color: #909399;
}

.user-message .message-time {
  text-align: right;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  border-bottom-left-radius: 4px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #909399;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%,
  60%,
  100% {
    transform: translateY(0);
    opacity: 0.7;
  }

  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

.chat-input-area {
  padding: 16px 24px;
  background: #fff;
  border-top: 1px solid #e4e7ed;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
}

.upload-area {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.upload-file-info {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.file-tag {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  font-size: 14px;
}

.file-icon {
  font-size: 16px;
}

.file-name {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-size {
  color: #909399;
  font-size: 12px;
}

.upload-btn {
  border-radius: 20px;
}

.resume-upload {
  display: inline-block;
}

.input-container {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.message-input {
  flex: 1;
}

:deep(.message-input .el-textarea__inner) {
  border-radius: 20px;
  padding: 12px 16px;
  font-size: 15px;
  border: 1px solid #e4e7ed;
  resize: none;
}

:deep(.message-input .el-textarea__inner:focus) {
  border-color: #667eea;
}

.send-btn {
  padding: 12px 24px;
  border-radius: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  font-size: 15px;
  font-weight: 500;
}

.send-btn:hover {
  background: linear-gradient(135deg, #5568d3 0%, #653a8f 100%);
}

.input-tip {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
  text-align: center;
}

/* 表格样式 */
:deep(.message-table) {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

:deep(.message-table td),
:deep(.message-table th) {
  padding: 10px 12px;
  border: 1px solid #e4e7ed;
  text-align: left;
  font-size: 14px;
}

:deep(.message-table th) {
  background: #f5f7fa;
  font-weight: 600;
  color: #303133;
}

:deep(.message-table tr:hover) {
  background: #f8f9fa;
}

/* 列表样式 */
:deep(.list-item) {
  display: flex;
  align-items: flex-start;
  margin: 6px 0;
  padding: 4px 0;
  line-height: 1.6;
}

:deep(.list-number) {
  color: #409eff;
  font-weight: 600;
  margin-right: 8px;
  min-width: 20px;
}

:deep(.list-bullet) {
  color: #409eff;
  margin-right: 8px;
  font-weight: bold;
}

/* 加粗文本 */
:deep(strong) {
  color: #303133;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .tools-grid {
    grid-template-columns: 1fr;
  }

  .message-content {
    max-width: 85%;
  }

  .suggestions {
    flex-direction: column;
  }
}
</style>
