// 1.引入构建路由的模块（路由模式：hash（#）、history）
import { createRouter, createWebHistory } from "vue-router";

// 2.引入需要配置路由规则的vue页面文件
import Home from "../views/home/Index.vue";
import Login from "../views/login/Index.vue";
import Layout from "../views/layout/Index.vue";
import Qa from "../views/qa/Index.vue";
import Job from "../views/job/List.vue";
import Company from "../views/company/List.vue";
import JobMap from "../views/jobmap/Index.vue";
import HrLayout from "../views/hr/Layout.vue";
import HrHome from "../views/hr/Home.vue";
import HrPostJob from "../views/hr/PostJob.vue";
import HrCandidateList from "../views/hr/CandidateList.vue";
import HrAssistant from "../views/hr/Assistant.vue";
import HrAgent from "../views/hr/Agent.vue";
import HrDegreeVerify from "../views/hr/DegreeVerify.vue";
import ResumeJob from  "../views/recommendJob/Index.vue";
import Resume from "../views/resume/Index.vue";

// 3.创建路由规则,每一项路由规则都是对象格式
const routes = [
  // 登录页
  {
    path: "/",
    component: Layout, //布局页面组件
    // redirect 移除，改为在路由守卫中根据角色动态处理
    children: [
      {
        path: "home",
        component: Home, //首页页面组件
      },
      {
        path: "job",
        component: Job,
      },
      {
        path: "company",
        component: Company,
      },
      {
        path: "qa",
        component: Qa,
      },
      {
        path: "jobmap",
        component: JobMap,
      },
      {
        path: "resumeJob",
        component: ResumeJob,
      },
      {
        path: "resume",
        component: Resume,
      },
    ],
  },
  {
    path: "/login",
    component: Login, //登录页面组件
  },
  {
    path: "/hr",
    component: HrLayout,
    redirect: "/hr/home", // HR 登录后默认跳转到工作台
    meta: { requiresAuth: true, role: "hr" },
    children: [
      {
        path: "home",
        component: HrHome,
        meta: { requiresAuth: true, role: "hr" },
      },
      {
        path: "post",
        component: HrPostJob,
        meta: { requiresAuth: true, role: "hr" },
      },
      {
        path: "candidates",
        component: HrCandidateList,
        meta: { requiresAuth: true, role: "hr" },
      },
      {
        path: "assistant",
        component: HrAssistant,
        meta: { requiresAuth: true, role: "hr" },
      },
      {
        path: "agent",
        component: HrAgent,
        meta: { requiresAuth: true, role: "hr" },
      },
      {
        path: "degree",
        component: HrDegreeVerify,
        meta: { requiresAuth: true, role: "hr" },
      },
    ],
  },
];

// 4.创建路由实例对象
const router = createRouter({
  routes, //路由规则
  history: createWebHistory(), //路由模式(历史模式)
});

// 登录后根据角色进入对应首页
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  // 访问根路径时，根据角色跳转
  if (to.path === "/") {
    if (token && role === "hr") {
      // HR用户访问根路径，跳转到HR后台
      return next("/hr");
    }
    // 非HR用户或未登录，跳转到求职者首页
    return next("/home");
  }

  // 未登录访问需要登录的页面，跳转登录
  if (to.meta.requiresAuth && !token) {
    return next("/login");
  }

  // 登录页：如已登录则按角色跳转
  if (to.path === "/login" && token) {
    if (role === "hr") return next("/hr");
    return next("/");
  }

  // HR 页面角色校验
  if (to.meta.role === "hr" && role !== "hr") {
    return next("/");
  }

  next();
});

// 5.暴露路由实例对象
export default router;
