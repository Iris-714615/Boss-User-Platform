/**
 * Vue Router 配置文件
 * 用于定义应用程序的路由规则
 */

// 导入 Vue Router 创建函数
import {createRouter, createWebHistory} from 'vue-router'

// 导入页面组件
import PUBGIndex from './components/PUBGIndex.vue'
import Login from './components/Login.vue'
import AdminLayout from './layouts/AdminLayout.vue'
import Dashboard from './pages/admin/Dashboard.vue'
import DataDashboard from './pages/admin/DataDashboard.vue'
import Companies from './pages/admin/Companies.vue'
import CompanyDetail from './pages/admin/CompanyDetail.vue'
import CertificationAudit from './pages/admin/CertificationAudit.vue'
import CertificationList from './pages/admin/CertificationList.vue'
import Positions from './pages/admin/Positions.vue'
import PositionDetail from './pages/admin/PositionDetail.vue'
import Candidates from './pages/admin/Candidates.vue'
import CandidateDetail from './pages/admin/CandidateDetail.vue'
import ChatReviews from './pages/admin/ChatReviews.vue'
import SessionDetail from './pages/admin/SessionDetail.vue'
import ReportTasks from './pages/admin/ReportTasks.vue'
import ContentArticles from './pages/admin/ContentArticles.vue'
import Activities from './pages/admin/Activities.vue'
import Roles from './pages/admin/Roles.vue'
import OperationLogs from './pages/admin/OperationLogs.vue'
import PersonalCenter from './pages/admin/PersonalCenter.vue'


// 定义路由规则
const routes = [
  {
    // 根路径，指向占位首页（会自动跳转到后台）
    path: '/',
    name: 'PUBGIndex',
    component: PUBGIndex,
  },
  {
    // 登录页面路径
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/admin',
    component: AdminLayout,
    redirect: '/admin/dashboard', // 默认重定向到数据概览页
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: Dashboard,
      },
      {
        path: 'data-dashboard',
        name: 'AdminDataDashboard',
        component: DataDashboard,
      },
      {
        path: 'companies',
        name: 'AdminCompanies',
        component: Companies,
      },
      {
        path: 'certification-list',
        name: 'AdminCertificationList',
        component: CertificationList,
      },
      {
        path: 'companies/:id',
        name: 'AdminCompanyDetail',
        component: CompanyDetail,
      },
      {
        path: 'positions',
        name: 'AdminPositions',
        component: Positions,
      },
      {
        path: 'positions/:id',
        name: 'AdminPositionDetail',
        component: PositionDetail,
      },
      {
        path: 'candidates',
        name: 'AdminCandidates',
        component: Candidates,
      },
      {
        path: 'candidates/:id',
        name: 'AdminCandidateDetail',
        component: CandidateDetail,
      },
      {
        path: 'chat-reviews',
        name: 'AdminChatReviews',
        component: ChatReviews,
      },
      {
        path: 'session-detail/:id',
        name: 'AdminSessionDetail',
        component: SessionDetail,
      },
      {
        path: 'report-tasks',
        name: 'AdminReportTasks',
        component: ReportTasks,
      },
      {
        path: 'content-articles',
        name: 'AdminContentArticles',
        component: ContentArticles,
      },
      {
        path: 'activities',
        name: 'AdminActivities',
        component: Activities,
      },
      {
        path: 'roles',
        name: 'AdminRoles',
        component: Roles,
      },
      {
        path: 'operation-logs',
        name: 'AdminOperationLogs',
        component: OperationLogs,
      },
      {
        path: 'personal-center',
        name: 'AdminPersonalCenter',
        component: PersonalCenter,
      },
      {
        path: 'certification-audit/:id',
        name: 'AdminCertificationAudit',
        component: CertificationAudit,
      },
    ],
  },
]

// 创建路由器实例
const router = createRouter({
    // 使用 HTML5 History 模式
    history: createWebHistory(),
    // 路由规则
    routes
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  // 获取 token
  const token = localStorage.getItem('token')
  
  // 需要认证的路由
  const authRoutes = ['/admin', '/admin/dashboard', '/admin/companies', '/admin/positions', '/admin/candidates']
  const isAuthRoute = authRoutes.some(route => to.path.startsWith(route))
  
  if (isAuthRoute && !token) {
    // 未登录，跳转到登录页
    next('/login')
  } else if (to.path === '/login' && token) {
    // 已登录，访问登录页时重定向到首页
    next('/admin/dashboard')
  } else {
    next()
  }
})

// 导出路由器实例，以便在主应用中使用
export default router