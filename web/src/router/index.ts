import { createRouter, createWebHistory } from 'vue-router'
import { routes } from 'vue-router/auto-routes'
import { useMenuStore } from '@/stores/menu'

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const menuStore = useMenuStore()
  // 将当前路由保存到 pinia
  menuStore.setActiveIndex(to.path)
  next()
})

export default router
