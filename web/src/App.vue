<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { watch } from 'vue'

// 使用 ref 来存储路由名称
const routeName = ref<string>('/')
// 获取当前路由信息
const route = useRoute()
// 监听路由名称的变化，并更新 routeName
watch(
  () => route.name,
  (newName) => {
    if (newName) {
      routeName.value = newName as string // 确保类型为 string
    }
  },
)
const sidelCollapse = ref(false)
const sideWidth = ref('220px')
const clacMenuWidth = () => {
  if (window.innerWidth < 800) {
    sideWidth.value = '80px'
    sidelCollapse.value = true
  } else {
    sideWidth.value = '220px'
    sidelCollapse.value = false
  }
}

onMounted(() => {
  window.addEventListener('resize', clacMenuWidth, false)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', clacMenuWidth, false)
})
</script>

<template>
  <div class="app-wrapper">
    <BaseHeader class="header" />
    <div class="flex">
      <el-scrollbar class="menu" :style="{ width: sideWidth }">
        <BaseSide :sidelCollapse="sidelCollapse" />
      </el-scrollbar>
      <div class="content" v-if="routeName == '/'">
        <RouterView />
      </div>
      <el-scrollbar class="content" v-else>
        <RouterView />
      </el-scrollbar>

      <!-- 常驻前台的消息提示框 -->
      <status-badge />
    </div>
  </div>
</template>

<style>
.app-wrapper {
  width: 100%;
  height: 100%;
}

.header {
  height: 76px;
  padding: 0px;
  border-bottom: 1px solid #e5e7eb;
}

.menu {
  height: calc(100vh - 76px);
}

.content {
  position: relative;
  width: 100%;
  height: calc(100vh - 76px);
}
</style>
