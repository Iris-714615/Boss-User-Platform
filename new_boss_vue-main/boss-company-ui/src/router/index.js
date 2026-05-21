import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import CompanyLayout from '../layouts/CompanyLayout.vue'
import Dashboard from '../pages/dashboard/Dashboard.vue'
import PositionList from '../pages/positions/PositionList.vue'
import PositionDetail from '../pages/positions/PositionDetail.vue'
import PublishPosition from '../pages/positions/PublishPosition.vue'
import ResumeList from '../pages/candidates/ResumeList.vue'
import ResumeDetail from '../pages/candidates/ResumeDetail.vue'
import ChatList from '../pages/communications/ChatList.vue'
import ChatWindow from '../pages/communications/ChatWindow.vue'
import CompanyProfile from '../pages/company/CompanyProfile.vue'
import Certification from '../pages/company/Certification.vue'
import DataDashboard from '../pages/data/DataDashboard.vue'
import TeamMembers from '../pages/team/TeamMembers.vue'
import AccountSettings from '../pages/account/AccountSettings.vue'

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
    path: '/company/certification',
    name: 'Certification',
    component: Certification
  },
  {
    path: '/company',
    component: CompanyLayout,
    redirect: '/company/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'positions',
        name: 'PositionList',
        component: PositionList
      },
      {
        path: 'positions/:id',
        name: 'PositionDetail',
        component: PositionDetail
      },
      {
        path: 'positions/publish',
        name: 'PublishPosition',
        component: PublishPosition
      },
      {
        path: 'resumes',
        name: 'ResumeList',
        component: ResumeList
      },
      {
        path: 'resumes/:id',
        name: 'ResumeDetail',
        component: ResumeDetail
      },
      {
        path: 'chat',
        name: 'ChatList',
        component: ChatList
      },
      {
        path: 'chat/:userId',
        name: 'ChatWindow',
        component: ChatWindow
      },
      {
        path: 'company-profile',
        name: 'CompanyProfile',
        component: CompanyProfile
      },
      {
        path: 'data',
        name: 'DataDashboard',
        component: DataDashboard
      },
      {
        path: 'team',
        name: 'TeamMembers',
        component: TeamMembers
      },
      {
        path: 'account-settings',
        name: 'AccountSettings',
        component: AccountSettings
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('companyToken')
  
  // 白名单：无需登录即可访问的页面
  const whiteList = ['/login', '/company/certification']
  
  if (whiteList.includes(to.path)) {
    // 白名单页面直接放行
    if (to.path === '/login' && token) {
      // 已登录用户访问登录页，跳转到首页
      next('/company/dashboard')
    } else {
      next()
    }
  } else if (!token) {
    // 非白名单页面且未登录，跳转到登录页
    next('/login')
  } else {
    // 已登录用户正常访问
    next()
  }
})

export default router
