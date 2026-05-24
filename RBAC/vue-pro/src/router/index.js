import { createWebHistory, createRouter } from 'vue-router'

import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import User from '../views/User.vue'
import Role from '../views/Role.vue'
import Resource from '../views/Resource.vue'

const routes = [
    { path: '/login', component: Login },
    { path: '/', redirect: '/login' },
    { path: '/home', component: Home,
      children: [
        { path: '/user', component: User },
        { path: '/role', component: Role },
        { path: '/resource', component: Resource }
      ]
    },
    { path: '/user', component: Home,
      children: [
        { path: '', component: User }
      ]
    },
    { path: '/role', component: Home,
      children: [
        { path: '', component: Role }
      ]
    },
    { path: '/resource', component: Home,
      children: [
        { path: '', component: Resource }
      ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
    if (to.path === '/login') {
        next()
    } else {
        let token = localStorage.getItem('token')
        if (token === null || token === '') {
            next('/login')
        } else {
            next()
        }
    }
})

export default router
