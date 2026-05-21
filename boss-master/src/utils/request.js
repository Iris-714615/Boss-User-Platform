// 1.引入axios模块
import axios from "axios";
import { ElMessage } from "element-plus";
// 2.创建axios实例
const request = axios.create({
  baseURL: "http://localhost:8000/", // 请求的后端访服务地址
  timeout: 500000, // 请求超时时间
});

// 3.请求拦截器(当前发起请求的时候，此时请求还没有出去)
request.interceptors.request.use(
  (config) => {
    // 追加token
    if (localStorage.getItem("token")) {
      config.headers.Authorization = "Bearer " + localStorage.getItem("token");
    }
    // 注意此处一定要返回
    return config;
  },
  (error) => {
    console.log("请求拦截器失败");
    // 返回失败状态
    return Promise.reject(error);
  },
);

// 4.响应拦截器(当前请求已经返回了，此时结果还没有达到视图组件)
request.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.log("响应拦截器失败", error.response.data);
    ElMessage.error(error.response.data.message);
    // 响应失败
    return Promise.reject(error);
  },
);

// 5.基于request封装restful风格api接口
const http = {
  // get请求:查询操作
  get(url, params) {
    return request.get(url, { params });
  },
  // post请求:创建操作
  post(url, data) {
    return request.post(url, data);
  },
  // put请求:更新操作（全部）
  put(url, data) {
    return request.put(url, data);
  },
  // patch请求:更新操作（局部字段）
  patch(url, data) {
    return request.patch(url, data);
  },
  // delete请求:删除操作
  delete(url, params) {
    return request.delete(url, { params });
  },
  // post带上传文件
  postupload(url, formData) {
    return request.post(url, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  // put带上传文件
  puttupload(url, formData) {
    return request.put(url, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  /**
   * 适配后端send_message接口的SSE请求方法
   * @param {string} url - 请求地址（示例：/chat/send_message/）
   * @param {Object} data - POST请求体数据（session_id + content）
   * @param {Object} callbacks - 回调函数集合
   * @param {Function} callbacks.onMessage - 接收单条消息回调 (data: {type, content, finished, code?, message?})
   * @param {Function} [callbacks.onError] - 错误回调
   * @param {Function} [callbacks.onComplete] - 流结束回调
   * @param {Function} [callbacks.onOpen] - 连接打开回调
   * @returns {Object} - 包含关闭连接的方法
   */
  sseChat(url, data, callbacks) {
    const { onMessage, onError, onComplete, onOpen } = callbacks;

    // 创建AbortController用于取消请求
    const abortController = new AbortController();
    let isCompleted = false;

    // 构建完整请求URL（拼接baseURL）
    const fullUrl = new URL(url, request.defaults.baseURL).href;

    // 发起POST SSE请求
    fetch(fullUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(localStorage.getItem("token")
          ? { Authorization: "Bearer " + localStorage.getItem("token") }
          : {}),
      },
      body: JSON.stringify(data),
      signal: abortController.signal,
      credentials: "include", // 携带cookie（如果需要）
    })
      .then(async (response) => {
        if (!response.ok) {
          // 处理HTTP错误状态
          const errorText = await response.text();
          throw new Error(
            `请求失败 [${response.status}]: ${errorText || response.statusText}`,
          );
        }

        if (!response.body) {
          throw new Error("响应流为空");
        }

        onOpen?.(); // 触发连接打开回调

        // 创建流读取器
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let buffer = "";

        // 循环读取流数据
        const readStream = async () => {
          try {
            const { done, value } = await reader.read();

            // 流结束
            if (done) {
              if (!isCompleted) {
                onComplete?.();
              }
              return;
            }

            // 解码并处理数据
            buffer += decoder.decode(value, { stream: true });
            // 按SSE格式分割（data: xxx\n\n）
            const lines = buffer.split(/\n\n/);
            buffer = lines.pop() || ""; // 保留未完成的最后一行

            // 处理每一条SSE消息
            for (const line of lines) {
              if (!line.trim()) continue;

              // 提取data字段内容（去掉data: 前缀）
              const dataStr = line.replace(/^data:\s*/, "");
              if (!dataStr) continue;

              try {
                // 解析后端返回的JSON数据
                const parsedData = JSON.parse(dataStr);

                // 触发消息回调
                onMessage?.(parsedData);

                // 判断是否是最后一条消息（finished: true）
                if (parsedData.finished === true) {
                  isCompleted = true;
                  onComplete?.();
                }

                // 处理后端返回的错误码
                if (parsedData.code === 400) {
                  onError?.(new Error(parsedData.message || "请求参数错误"));
                  abortController.abort(); // 关闭连接
                  return;
                }
              } catch (parseError) {
                onError?.(
                  new Error(
                    `解析消息失败: ${parseError.message}, 原始数据: ${dataStr}`,
                  ),
                );
              }
            }

            // 继续读取下一块数据
            await readStream();
          } catch (streamError) {
            // 排除主动取消的错误
            if (streamError.name !== "AbortError") {
              onError?.(streamError);
            }
          }
        };

        await readStream();
      })
      .catch((error) => {
        // 排除主动取消的错误
        if (error.name !== "AbortError") {
          onError?.(error);
          ElMessage.error("SSE连接失败: " + error.message);
        }
      });

    // 返回关闭连接的方法
    return {
      close: () => {
        isCompleted = true;
        abortController.abort();
        onComplete?.(); // 触发结束回调
      },
      isAborted: () => abortController.signal.aborted,
    };
  },
};

// 6.按需导出http，一个js文件可以按需导出多个模块
export { http };
