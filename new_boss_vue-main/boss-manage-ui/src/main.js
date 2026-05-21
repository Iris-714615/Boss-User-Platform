import {createApp} from 'vue'
import './style.css'
import App from './App.vue'
// 导入路由配置
import router from './router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 创建 Vue 应用实例，并使用路由配置
const app = createApp(App)


// 使用路由
app.use(router).use(ElementPlus)

// 挂载应用到页面的 #app 元素
app.mount('#app')