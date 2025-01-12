<script setup lang="ts">
import { RouterView } from 'vue-router'
import { ref, onMounted, onBeforeUnmount } from 'vue'

// const sideWidth = ref("220")
// const clacMenuWidth = () => {
//   if (window.innerWidth < 800) {
//     sideWidth.value = "64"
//   } else {
//     sideWidth.value = "220"
//   }

//   console.log(sideWidth.value)
// }

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
      <!-- <el-scrollbar class="menu" :style="{width:sideWidth+'px'}"> -->
      <el-scrollbar class="menu" :style="{width:sideWidth}">
      <!-- <el-scrollbar class="menu"> -->
        <BaseSide :sidelCollapse="sidelCollapse"/>
      </el-scrollbar>
      <el-scrollbar class="content">
        <RouterView />
      </el-scrollbar>
    </div>
  </div>
</template>

<!-- <template>
  <div class="app-wrapper">
    <BaseHeader class="header" />
    <div class="flex">
      <div class="menu" :style="{width:sideWidth+'px'}">
        <el-scrollbar>
          <BaseSide />
        </el-scrollbar>
      </div>
      <el-scrollbar class="content">
        <RouterView />
      </el-scrollbar>
    </div>
  </div>
</template> -->

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
