//import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
// import vueDevTools from 'vite-plugin-vue-devtools'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import VueRouter from 'unplugin-vue-router/vite'
import path from 'path';


// https://vite.dev/config/
export default defineConfig(({ mode }) =>{
  // 加载当前模式下的环境变量，前缀为 VITE_
  const env = loadEnv(mode, process.cwd(), 'VITE_')

  console.log('Proxy Target:', env.VITE_PROXY_TARGET)
  
  return {
    plugins: [
      VueRouter({}),
      vue(),
      // vueDevTools(),
      AutoImport({
        resolvers: [ElementPlusResolver()],
      }),
      Components({
        resolvers: [ElementPlusResolver()],
      }),
    ],
    resolve: {
      alias: {
        //'@': fileURLToPath(new URL('./src', import.meta.url))
        '@': path.resolve(__dirname, 'src'), // 设置 @ 别名指向 src 目录
      },
    },
    // 配置前端服务地址和端口
    server: {
      host: '0.0.0.0',
      port: 9963,
      // 设置反向代理，跨域
      proxy: {
        '/api': {
          // 后台地址
          target: env.VITE_PROXY_TARGET,
          changeOrigin: true,
          rewrite: path => path.replace(/^\/api/, '')
        },
      }
    },
  }
})

