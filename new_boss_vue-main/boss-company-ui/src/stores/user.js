import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('companyToken') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('companyUserInfo') || '{}'))

  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('companyToken', newToken)
  }

  const setUserInfo = (info) => {
    userInfo.value = info
    localStorage.setItem('companyUserInfo', JSON.stringify(info))
  }

  const logout = () => {
    token.value = ''
    userInfo.value = {}
    localStorage.removeItem('companyToken')
    localStorage.removeItem('companyUserInfo')
  }

  return {
    token,
    userInfo,
    setToken,
    setUserInfo,
    logout
  }
})
