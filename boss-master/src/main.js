//=================项目入口文件==============================
// 1.引入vue.js框架中的场景应用的方法
import { createApp } from "vue";
// 2.引入全局基础的样式文件
import "./style.css";
// 3.引入项目根组件App.vue，一个项目只能有一个根组件
import App from "./App.vue";
// 4.引入element-ui
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
// 5.引入路由实例对象
import router from "./router";
// 6.创建项目应用实例对象
const app = createApp(App);
// 7.注册element-ui到全局项目中
app.use(ElementPlus);
// 8.注册路由实例对象
app.use(router);
// 9.挂载到了根节点上
app.mount("#app");
