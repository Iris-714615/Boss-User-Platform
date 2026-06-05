/**
 * Axios 请求封装
 * 用于统一管理 API 请求、响应拦截和错误处理
 */

import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 创建 axios 实例
const service = axios.create({
  baseURL: 'http://localhost:8000' , // API 基础路径
  timeout: 15000, // 请求超时时间
})

// 请求拦截器
// service.interceptors.request.use(
//   (config) => {
//     // 从 localStorage 获取 token
//     const token = localStorage.getItem('companyToken')
//     if (token) {
//       config.headers['Authorization'] = `Bearer ${token}`
//     }
//     return config
//   },
//   (error) => {
//     console.error('Request error:', error)
//     return Promise.reject(error)
//   }
// )

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    const res = response.data
    
    // 如果返回的状态码不是 200，说明接口有错误
    // if (res.code !== 200) {
    //   // 401: 未授权，需要重新登录
    //   if (res.code === 401) {
    //     ElMessage.error('登录已过期，请重新登录')
    //     localStorage.removeItem('companyToken')
    //     localStorage.removeItem('companyUserInfo')
    //     router.replace('/login')
    //   } else {
    //     ElMessage.error(res.message || '请求失败')
    //   }
    //   return Promise.reject(new Error(res.message || 'Error'))
    // }
    
    return res
  },
  (error) => {
    console.error('Response error:', error)
    
    let message = '网络错误，请稍后重试'
    if (error.response) {
      switch (error.response.status) {
        case 400:
          message = '请求参数错误'
          break
        case 401:
          message = '未授权，请重新登录'
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = '请求地址不存在'
          break
        case 500:
          message = '服务器内部错误'
          break
        case 502:
          message = '网关错误'
          break
        case 503:
          message = '服务不可用'
          break
        case 504:
          message = '网关超时'
          break
        default:
          message = `连接错误${error.response.status}`
      }
    } else if (error.message.includes('timeout')) {
      message = '请求超时'
    }
    
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export default service
