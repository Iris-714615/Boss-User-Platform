// Vue 文件类型声明
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// JavaScript 文件类型声明
declare module '*.js' {
  const value: any
  export default value
}
