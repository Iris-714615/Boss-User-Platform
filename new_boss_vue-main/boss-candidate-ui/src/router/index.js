import { createRouter, createWebHistory } from 'vue-router'

// 布局组件
import CandidateLayout from '@/layouts/CandidateLayout.vue'

// 页面组件
import Login from '@/pages/Login.vue'
import Register from '@/pages/Register.vue'
import BindPhone from '@/pages/BindPhone.vue'
import DingLoginSuccess from '@/pages/DingLoginSuccess.vue'
import Home from '@/pages/Home.vue'
import JobList from '@/pages/jobs/JobList.vue'
import JobDetail from '@/pages/jobs/JobDetail.vue'
import Chat from '@/pages/chat/Chat.vue'
import ChatWindow from '@/pages/chat/ChatWindow.vue'
import QaChat from '@/pages/chat/QaChat.vue'
import TestChat from '@/pages/chat/TestChat.vue'
import Resume from '@/pages/resume/Resume.vue'
import DeliveryRecord from '@/pages/delivery/DeliveryRecord.vue'
import Favorites from '@/pages/favorites/Favorites.vue'
import Profile from '@/pages/profile/Profile.vue'
import RealNameAuth from '@/pages/profile/RealNameAuth.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/bind-phone',
    name: 'BindPhone',
    component: BindPhone
  },
  {
    path: '/dinglogin-success',
    name: 'DingLoginSuccess',
    component: DingLoginSuccess
  },
  {
    path: '/test-chat',
    name: 'TestChat',
    component: TestChat
  },
  {
    path: '/candidate',
    component: CandidateLayout,
    redirect: '/candidate/home',
    children: [
      {
        path: 'home',
        name: 'Home',
        component: Home
      },
      {
        path: 'jobs',
        name: 'JobList',
        component: JobList
      },
      {
        path: 'jobs/:id',
        name: 'JobDetail',
        component: JobDetail
      },
      {
        path: 'chat',
        name: 'Chat',
        component: Chat
      },
      {
        path: 'chat/:hrId',
        name: 'ChatWindow',
        component: ChatWindow
      },
      {
        path: 'qa',
        name: 'QaChat',
        component: QaChat
      },
      {
        path: 'resume',
        name: 'Resume',
        component: Resume
      },
      {
        path: 'delivery',
        name: 'DeliveryRecord',
        component: DeliveryRecord
      },
      {
        path: 'favorites',
        name: 'Favorites',
        component: Favorites
      },
      {
        path: 'profile',
        name: 'Profile',
        component: Profile
      },
      {
        path: 'realname-auth',
        name: 'RealNameAuth',
        component: RealNameAuth
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('candidateToken')
  
  // 允许直接访问登录页、注册页、绑定手机号页和钉钉登录成功页
  if (to.path === '/login' || to.path === '/register' || to.path === '/bind-phone' || to.path === '/dinglogin-success') {
    if (token && to.path !== '/bind-phone' && to.path !== '/dinglogin-success') {
      // 已登录则跳转到首页（绑定页和钉钉登录成功页除外）
      next('/candidate/home')
    } else {
      next()
    }
    return
  }
  
  // 其他页面需要登录
  if (!token) {
    next('/login')
  } else {
    next()
  }
})

export default router
