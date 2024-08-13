# vue2基础用法和下载安装

## 作用：绑定数据和DOM元素，实现数据驱动的视图更新，当数据发生变化时，视图自动更新

## 支持前后端分离和前后端不分离

- ### 前后端不分离

  1. 导入vue2.js文件

     ```html
     <script src="https://cdn.jsdelivr.net/npm/vue@2.7.16/dist/vue.js"></script>
     ```

  2. 建立vue数据模型

     ```vue
     //el绑定div id值为app
     <script>
             new Vue({
                 el: "#app",
                 data: {
                     users: [{
                         name: "longersking",
                         age:20,
                         gender: 1,
                         score:90
                     },{
                         name: "admin",
                         age:22,
                         gender: 2,
                         score:93
                     },{
                         name: "guest",
                         age:20,
                         gender: 1,
                         score:66
                     },{
                         name: "dyc",
                         age:19,
                         gender: 2,
                         score:100
                     },{
                         name: "make",
                         age:25,
                         gender: 1,
                         score:55
                     }
                     
                 ]
                 }
             })
         </script>
     ```

  3. 利用表达式和指令对数据模型中的一些数据操作

     ```vue
     {{ 数据模型中的数据，上述代码中的users }}
     ```

     v指令简化一些操作 例如v-for遍历 

     ```vue
      v-for="(user,index) in users"
     ```

- ### 前后端分离

  1. 创建vue项目

     ```shell
     npm install -g @vue/cli #安装vue脚手架，便于安装
     mkdir vue_project #创建目录
     cd vue_project #进入此目录
     cmd =》 vue ui #启动图形化交互界面创建项目
     # 点击创建，创建vue2项目名称
     # 设置包管理工具，正常情况可以设置npm,nodejs环境下默认的包管理工具
     # 功能在默认基础上添加路由功能Router勾选
     # 设置vue版本为2.x,语法检测规范选择第一个，创建项目
     # 可以保存预设也可以不保存，等待下载和创建
     ```

  2. 说明创建的vue项目一些文件夹作用

     ```shell
     # node_modules 整个项目的依赖包
     # public 存放项目的静态文件
     # src 存放项目的源代码
     # package.json 模块基本信息，项目开发所需模块，版本信息
     # vue.config.js 保存vue配置的文件，如：端口，代理配置
     # src 子目录 asset 静态资源
     # src 子目录 components 可重用的组件
     # src 子目录 router 路由配置
     # src 子目录 views 视图组件（页面）
     # src 子文件 App.vue 入口页面（根组件）
     # src 子文件 main.js 入口js文件
     ```

  3. 运行前端项目

     ```shell
     # ide 中的插件或者图形化启动工具
     # 命令行 npm run serve
     # 修改项目启动端口 在vue.config.js文件中 写入
     devServer: {
       port: 7000,
     }
     # 这一段代码写在defineConfig中
     ```

  4. 介绍vue项目的相关标签

     ```vue
     # main.js
     new Vue({
       router,
       render: h => h(App)
     }).$mount('#app')
     #.$mount('#app')挂载到id为app的div标签
     # vue文件
     <template></template> #模板部分用来生成html代码
     # 控制模板的数据来源和行为
     <script>
         export default {
            # 数据模型 这里为message
            data () {
                return {
                   message: "hello world"
                }
            },
            # 方法定义
            methods: {
              
            }
         }
         # export 将默认方法和数据导出，在main.js文件中导入
     </script>
     
     <style></style> #css样式，美化界面
     
     
     ```

  5. 为了快速入门可以直接使用一些现成的组件库，这里推荐Element

     ```shell
     # 安装ElementUI
     npm install element-ui@2.15.3
     # 引入ElementUI组件库
     import ElementUI from 'element-ui';
     import 'element-ui/lib/theme-chalk/index.css';
     
     Vue.use(ElementUI);
     ```

     

