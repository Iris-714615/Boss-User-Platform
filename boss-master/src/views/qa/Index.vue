<template>
  <div class="smart-qa-container">
    <!-- 左侧历史记录 -->
    <div class="history-sidebar">
      <div class="history-header">
        <h3>历史对话</h3>
        <button class="new-chat-btn" @click="startNewChat">
          <i class="plus-icon"></i>
          新对话
        </button>
      </div>
      <div class="history-list">
        <div
          v-for="chat in chatHistory"
          :key="chat.id"
          class="history-item"
          :class="{ active: currentChatId === chat.id }"
          @click="selectChat(chat.id)"
        >
          <div class="chat-title">{{ chat.title }}</div>
          <div class="chat-time">{{ formatTime(chat.lastTime) }}</div>
        </div>
        <div v-if="chatHistory.length === 0" class="empty-history">
          暂无历史对话
        </div>
      </div>
    </div>
    <!-- 右侧对话区域 -->
    <div class="chat-area">
      <div class="chat-header">
        <h2>智能问答助手</h2>
        <p class="chat-subtitle">
          我是您的职场智能助手，可以为您解答求职、面试、职业规划等问题
        </p>
      </div>
      <div class="chat-messages" ref="messagesContainer">
        <div v-if="currentMessages.length === 0" class="welcome-message">
          <div class="welcome-content">
            <div class="welcome-icon">🤖</div>
            <h3>欢迎使用智能问答</h3>
            <p>您可以问我关于以下内容的问题：</p>
            <div class="suggestion-tags">
              <span class="tag" @click="askSuggestion('帮我生成简历？')"
                >生成简历</span
              >
              <span class="tag" @click="askSuggestion('帮我验证学历？')"
                >学历验证</span
              >
              <span class="tag" @click="askSuggestion('面试时需要注意什么？')"
                >面试技巧</span
              >
              <span class="tag" @click="askSuggestion('如何进行职业规划？')"
                >职业规划</span
              >
              <span class="tag" @click="askSuggestion('如何提升职场竞争力？')"
                >能力提升</span
              >
            </div>
          </div>
        </div>
        <!-- 用户消息列表区域 -->
        <div
          v-for="message in currentMessages"
          :key="message.id"
          class="message-item"
          :class="{
            'user-message': message.type === 'user',
            'ai-message': message.type === 'ai',
          }"
        >
          <div class="message-avatar">
            <div v-if="message.type === 'user'" class="user-avatar">👤</div>
            <div v-else class="ai-avatar">🤖</div>
          </div>
          <!-- ai正在输入动画效果 -->
          <div
            class="message-content"
            v-if="isTyping && message.type == 'ai' && message.content == ''"
          >
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
          <!-- 用户消息列表区域 -->
          <div v-else class="message-content">
            <div
              class="message-text"
              v-html="formatMessageContent(message.content)"
            ></div>
            <!-- <div class="message-text">{{ message.content }}</div> -->
            <div class="message-time">{{ formatTime(message.time) }}</div>
          </div>
        </div>
        <!-- ai正在输入 -->
        <!-- <div v-if="isTyping" class="message-item ai-message typing">
          <div class="message-avatar">
            <div class="ai-avatar">🤖</div>
          </div>
         
        </div> -->
      </div>
      <div class="chat-input-area">
        <div class="input-container">
          <textarea
            v-model="inputMessage"
            ref="messageInput"
            placeholder="请输入您的问题..."
            class="message-input"
            rows="1"
            @keydown.enter.prevent="handleEnter"
            @input="adjustTextareaHeight"
          ></textarea>
          <button
            class="send-btn"
            :disabled="!inputMessage.trim() || isTyping"
            @click="sendMessage"
          >
            <i class="send-icon"></i>
          </button>
        </div>
        <div class="input-tips">按 Enter 发送，Shift + Enter 换行</div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, reactive, onMounted, nextTick } from "vue";
import { http } from "../../utils/request";

// 响应式数据
const currentChatId = ref(null); // 当前聊天的ID
const messagesContainer = ref(null); // 聊天区域的容器
const messageInput = ref(null); // 输入框

// ==========================1.获取聊天历史==========================
const chatHistory = ref([]);
const getChatHistory = async () => {
  let { data } = await http.get("/chat/session_list/");
  // 循环处理数据格式
  chatHistory.value = data.map((item) => {
    return {
      id: item.session_id,
      title: item.last_message ? item.last_message : "新对话",
      lastTime: new Date(item.create_time),
    };
  });
};
// ===========================2.切换会话方法=========================
const selectChat = (chatId) => {
  // 切换当前会话ID
  currentChatId.value = chatId;
  // 根据会话id获取会话聊天记录
  getChatMessages(chatId);
};
// ===========================3.获取会话聊天记录方法=========================
// 当前对话消息列表
const currentMessages = ref([]);
const getChatMessages = async (chatId) => {
  let { data } = await http.get(`/chat/message_list/`, { session_id: chatId });
  // 循环数据组装格式
  currentMessages.value = data.map((item) => {
    return {
      id: Date.now(),
      content: item.content,
      type: item.role == "user" ? "user" : "ai",
      time: new Date(item.create_time),
    };
  });
};

// 方法
const formatTime = (date) => {
  const now = new Date();
  const diff = now - date;

  if (diff < 1000 * 60) return "刚刚";
  if (diff < 1000 * 60 * 60) return `${Math.floor(diff / (1000 * 60))}分钟前`;
  if (diff < 1000 * 60 * 60 * 24)
    return `${Math.floor(diff / (1000 * 60 * 60))}小时前`;
  return date.toLocaleDateString();
};

// 将消息内容中的 data:image base64 转换为二维码图片展示，避免长串挤占版面
const formatMessageContent = (content = "") => {
  if (!content) return "";

  // 1) 处理 data:image/base64 字符串为图片，并提供下载、预览能力
  // 改进正则表达式，匹配更完整的base64字符串（包括可能跨行的）
  // 先找到所有 data:image 开头的位置，然后尽可能匹配完整的base64字符串
  let transformed = content;
  
  // 使用更精确的匹配方式：找到 data:image 开头，然后匹配到下一个非base64字符或文本内容
  const dataImagePattern = /data:image\/[^;]+;base64,[A-Za-z0-9+/=\s\r\n]+/gi;
  
  transformed = transformed.replace(dataImagePattern, (match) => {
    // 去掉base64数据中的所有空白字符（换行、空格、制表符等），确保base64字符串完整
    const cleanSrc = match.replace(/[\s\r\n\t]+/g, "");
    
    // 提取base64部分
    const base64Match = cleanSrc.match(/;base64,([A-Za-z0-9+/=]+)/);
    if (!base64Match || base64Match[1].length < 100) {
      // 如果base64数据太短，可能不完整，返回原文本
      console.warn("Base64数据可能不完整，长度:", base64Match ? base64Match[1].length : 0);
      return match;
    }
    
    // 验证格式是否正确
    if (!cleanSrc.match(/^data:image\/[^;]+;base64,[A-Za-z0-9+/]+={0,2}$/)) {
      console.warn("Base64图片格式验证失败，但尝试显示");
    }
    
    return `
      <div class="qr-block">
        <div class="qr-title">电子备案二维码</div>
        <div class="qr-image-wrapper">
          <img src="${cleanSrc}" alt="二维码" class="qr-image" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';" />
          <div class="qr-error" style="display:none; color:#f56c6c; font-size:12px; padding:10px;">
            二维码加载失败，请尝试下载查看
          </div>
        </div>
        <div class="qr-actions">
          <a href="${cleanSrc}" download="qrcode.png" class="qr-download">下载二维码</a>
          <a href="${cleanSrc}" target="_blank" class="qr-preview">新窗口预览</a>
        </div>
      </div>
    `;
  });

  // 2) 将超长纯文本折叠，防止挤占版面
  transformed = transformed
    .split("\n")
    .map((line) => {
      const plainLine = line.trim();
      if (plainLine.length > 300 && !plainLine.startsWith("<")) {
        return `
          <details class="long-text">
            <summary>展开长内容（${plainLine.length} 字符）</summary>
            <div class="long-text-body">${plainLine}</div>
          </details>
        `;
      }
      return line;
    })
    .join("\n");

  // 3) 将换行转换为 <br>，保持原有格式
  return transformed.replace(/\n/g, "<br>");
};

// ==========================4.开始新会话========================================
const startNewChat = async () => {
  // 重置数据: 会话ID、消息列表、输入框内容赋空
  currentChatId.value = null;
  currentMessages.value = [];
  inputMessage.value = "";
  // 发起新会话请求
  let { data } = await http.post("/chat/create_session/");
  // 将新生成的对话记录追加到左侧栏中进行显示
  chatHistory.value.unshift({
    id: data.session_id,
    title: "新对话",
    lastTime: new Date(),
  });
  // 激活当前会话
  currentChatId.value = data.session_id;
};

// ==========================5.发送消息========================================
/**
 * 实现思路：
 * 1. 获取用户输入的内容
 * 2. 验证用户输入的内容
 * 3. 组装用户消息并展示
 * 4. 开启ai回复加载动画
 * 5. 请求接口获取ai回复内容
 * 6. 关闭加载动画，渲染ai回复消息
 * */
const inputMessage = ref(""); // 用户输入的文本
const isTyping = ref(false); // 是否正在输入
const sendMessage = async () => {
  // 1. 获取用户输入的内容并验证内容
  if (!inputMessage.value.trim() || isTyping.value) return;
  // 2. 组装用户消息并展示
  const userMessage = {
    id: Date.now(),
    type: "user",
    content: inputMessage.value.trim(),
    time: new Date(),
  };
  // 3. 添加用户消息到消息列表中
  currentMessages.value.push(userMessage);
  // 4.显示输入状态
  isTyping.value = true;
  // 5. 滚动到底部
  nextTick(() => {
    adjustTextareaHeight();
    scrollToBottom();
  });

  // 6.初始化ai回复消息内容
  let aiMessage = {
    id: Date.now(),
    type: "ai",
    content: "",
    time: new Date(),
  };
  currentMessages.value.push(aiMessage);
  // 获取ai消息索引下标
  let len = currentMessages.value.length - 1;

  // 6. 发送请求获取ai回复内容
  let connectSse = http.sseChat(
    "http://localhost:8000/api/v1/chat/send_message/",
    {
      session_id: currentChatId.value,
      content: inputMessage.value,
    },
    {
      onOpen: () => {
        console.log("sse连接成功");
      },
      onMessage: (data) => {
        // 关闭哎输入状态
        isTyping.value = false;
        console.log("流式数据：", data.content);
        // 通过ai消息索引下标追加内容
        currentMessages.value[len].content += data.content;
        // 滚动到底部
        nextTick(() => {
          adjustTextareaHeight();
          scrollToBottom();
        });
      },
      onError: (error) => {
        console.log("sse连接错误：", error);
      },
      onComplete: () => {
        console.log("ai回复完成");
        inputMessage.value = ""; // 清空输入框
        connectSse = null; //断开连接
      },
    }
  );
};
// 获取AI回复
const getAIResponse = (question) => {
  const responses = {
    简历: "关于简历优化，我建议您：\n\n1. **突出重点**：将最相关的经验和技能放在显眼位置\n2. **量化成果**：用数字和百分比展示您的成就\n3. **关键词优化**：包含招聘信息中的关键技能词汇\n4. **格式清晰**：使用清晰的标题和条理化的布局\n\n需要我帮您分析具体的简历内容吗？",

    面试: "面试成功的关键在于充分准备：\n\n**技术准备**\n• 复习与岗位相关的专业知识\n• 准备项目经验的详细介绍\n• 了解公司的业务和文化\n\n**心理准备**\n• 保持自信和积极的心态\n• 准备应对压力面试的策略\n• 练习清晰表达自己的想法\n\n您想了解哪种类型面试的具体技巧？",

    职业规划:
      "制定职业规划需要考虑以下几个方面：\n\n1. **自我评估**：了解自己的兴趣、能力和价值观\n2. **市场分析**：研究行业发展趋势和机会\n3. **目标设定**：制定短期、中期和长期职业目标\n4. **技能发展**：识别需要提升的核心技能\n5. **行动计划**：制定具体的实施步骤和时间表\n\n您目前处于职业发展的哪个阶段？",

    薪资: "关于薪资谈判的建议：\n\n**准备阶段**\n• 调研行业薪资水平和市场行情\n• 评估自己的价值和贡献\n• 准备具体的成就案例\n\n**谈判技巧**\n• 以数据和事实为基础\n• 展示您能为公司创造的价值\n• 考虑整体薪酬包，不只是基本工资\n\n您想了解如何在面试中合适地提及薪资期望吗？",
  };

  // 简单的关键词匹配
  for (const [keyword, response] of Object.entries(responses)) {
    if (question.includes(keyword)) {
      return response;
    }
  }

  // 默认回复
  return '感谢您的提问！作为您的职场智能助手，我可以帮您解答关于求职、面试、职业规划、技能提升等方面的问题。\n\n请告诉我您具体想了解什么，我会为您提供详细的建议和指导。\n\n您也可以尝试问我：\n• "如何准备技术面试？"\n• "怎样提升领导力？"\n• "如何转行到新的行业？"\n• "远程工作有什么技巧？"';
};

const askSuggestion = (question) => {
  inputMessage.value = question;
  sendMessage();
};

// 监听用户点击回车发送消息事件
const handleEnter = (event) => {
  if (event.shiftKey) {
    return; // 允许换行
  }
  sendMessage();
};

const adjustTextareaHeight = () => {
  const textarea = messageInput.value;
  if (textarea) {
    textarea.style.height = "auto";
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + "px";
  }
};

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// 组件挂载时的初始化
onMounted(async () => {
  // 获取历史对话记录
  await getChatHistory();
  // 默认选择第一个对话进行展示;
  if (chatHistory.value.length > 0) {
    selectChat(chatHistory.value[0].id);
  }
});
</script>
<style scoped>
.smart-qa-container {
  display: flex;
  height: calc(100vh - 49px);
  margin-top: 49px;
  background: #f5f7fa;
}

/* 左侧历史记录 */
.history-sidebar {
  width: 280px;
  background: #fff;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}

.history-header {
  padding: 20px;
  border-bottom: 1px solid #e4e7ed;
}

.history-header h3 {
  margin: 0 0 15px 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
}

.new-chat-btn {
  width: 100%;
  padding: 10px;
  background: #00bebd;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  transition: background-color 0.3s;
}

.new-chat-btn:hover {
  background: #009a9a;
}

.plus-icon::before {
  content: "+";
  font-size: 16px;
  font-weight: bold;
}

.history-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.history-item {
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
  border: 1px solid transparent;
}

.history-item:hover {
  background: #f5f7fa;
}

.history-item.active {
  background: #e6f9f9;
  border-color: #00bebd;
}

.chat-title {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chat-time {
  font-size: 12px;
  color: #909399;
}

.empty-history {
  text-align: center;
  color: #909399;
  font-size: 14px;
  padding: 40px 20px;
}

/* 右侧对话区域 */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
}

.chat-header {
  padding: 20px 30px;
  border-bottom: 1px solid #e4e7ed;
  background: #fff;
}

.chat-header h2 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 20px;
  font-weight: 600;
}

.chat-subtitle {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px 30px;
  background: #fafbfc;
}

.welcome-message {
  text-align: center;
  padding: 60px 20px;
}

.welcome-content {
  max-width: 500px;
  margin: 0 auto;
}

.welcome-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.welcome-content h3 {
  color: #303133;
  font-size: 24px;
  margin-bottom: 10px;
}

.welcome-content p {
  color: #606266;
  font-size: 16px;
  margin-bottom: 30px;
}

.suggestion-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.tag {
  padding: 8px 16px;
  background: #e6f9f9;
  color: #00bebd;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #00bebd;
}

.tag:hover {
  background: #00bebd;
  color: white;
}

.message-item {
  display: flex;
  margin-bottom: 20px;
  align-items: flex-start;
}

.user-message {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin: 0 15px;
  flex-shrink: 0;
}

.user-avatar {
  background: #00bebd;
  color: white;
}

.ai-avatar {
  background: #f0f2f5;
  color: #606266;
}

.message-content {
  max-width: 70%;
  min-width: 100px;
}

.user-message .message-content {
  text-align: right;
}

.message-text {
  background: #fff;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
  color: #303133;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  white-space: pre-wrap;
}

.user-message .message-text {
  background: #00bebd;
  color: white;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.user-message .message-time {
  text-align: right;
}

/* 二维码块样式 */
.qr-block {
  border: 1px dashed #e4e7ed;
  border-radius: 12px;
  padding: 12px;
  margin-top: 8px;
  background: #f8f9fb;
}

.qr-title {
  font-size: 13px;
  color: #606266;
  margin-bottom: 8px;
  font-weight: 600;
}

.qr-image-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}

.qr-image {
  display: block;
  max-width: 300px;
  max-height: 300px;
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  background: #fff;
  padding: 8px;
}

.qr-actions {
  display: flex;
  gap: 12px;
}

.qr-download,
.qr-preview {
  font-size: 12px;
  color: #00bebd;
  text-decoration: none;
}

.qr-download:hover,
.qr-preview:hover {
  text-decoration: underline;
}

/* 长文本折叠 */
.long-text {
  margin-top: 8px;
  background: #f8f9fb;
  border: 1px solid #e4e7ed;
  border-radius: 10px;
  padding: 10px 12px;
}

.long-text summary {
  cursor: pointer;
  color: #00bebd;
  font-size: 13px;
  outline: none;
}

.long-text-body {
  margin-top: 8px;
  color: #606266;
  word-break: break-all;
  font-size: 13px;
  line-height: 1.5;
}

.typing {
  opacity: 0.8;
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px 16px;
  background: #f0f2f5;
  border-radius: 12px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #909399;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%,
  80%,
  100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  40% {
    opacity: 1;
    transform: scale(1);
  }
}

/* 输入区域 */
.chat-input-area {
  padding: 20px 30px;
  border-top: 1px solid #e4e7ed;
  background: #fff;
}

.input-container {
  display: flex;
  align-items: flex-end;
  gap: 15px;
  margin-bottom: 8px;
}

.message-input {
  flex: 1;
  min-height: 44px;
  max-height: 120px;
  padding: 12px 16px;
  border: 1px solid #dcdfe6;
  border-radius: 22px;
  font-size: 14px;
  line-height: 1.4;
  resize: none;
  outline: none;
  font-family: inherit;
  transition: border-color 0.3s;
}

.message-input:focus {
  border-color: #00bebd;
}

.send-btn {
  width: 44px;
  height: 44px;
  background: #00bebd;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  background: #009a9a;
}

.send-btn:disabled {
  background: #c0c4cc;
  cursor: not-allowed;
}

.send-icon::before {
  content: "➤";
  font-size: 16px;
}

.input-tips {
  font-size: 12px;
  color: #909399;
  text-align: center;
}

/* 滚动条样式 */
.history-list::-webkit-scrollbar,
.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.history-list::-webkit-scrollbar-track,
.chat-messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.history-list::-webkit-scrollbar-thumb,
.chat-messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.history-list::-webkit-scrollbar-thumb:hover,
.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .smart-qa-container {
    flex-direction: column;
  }

  .history-sidebar {
    width: 100%;
    height: 200px;
  }

  .message-content {
    max-width: 85%;
  }

  .chat-messages {
    padding: 15px 20px;
  }

  .chat-input-area {
    padding: 15px 20px;
  }
}
</style>
