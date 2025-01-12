<script setup lang="ts">
import { RouterView } from 'vue-router'
import { ref, onMounted, onBeforeUnmount } from 'vue'

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

  console.log(sideWidth.value)
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
      <el-scrollbar class="content">
        <RouterView />
      </el-scrollbar>
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
