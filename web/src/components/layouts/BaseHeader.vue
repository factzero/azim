<template>
  <div class="flex items-center justify-between">
    <div class="flex items-center px-12 h-full">
      <div class="cursor-pointer" @click="router.push({ path: '/' })">
        <img style="width: 50px" src="@/assets/logo.svg" />
      </div>
    </div>

    <div class="flex items-center p-2 h-full w-1/2">
      <el-input clearable class="h-full" placeholder="搜索您的照片">
        <template #prefix>
          <el-button :icon="Search" circle class="borderless-button" />
        </template>
        <template #suffix>
          <el-button :icon="Menu" circle class="borderless-button" />
        </template>
      </el-input>
    </div>

    <div class="flex items-center">
      <div class="px-4" v-show="showUpload">
        <el-button :icon="Upload" round class="white-to-gray flex items-center space-x-0.5"
          >上传</el-button
        >
      </div>
      <div class="px-4">
        <el-tooltip effect="light" content="切换主题" placement="bottom">
          <el-switch
            v-model="isDark"
            :active-action-icon="Moon"
            :inactive-action-icon="Sunny"
            inline-prompt
            @change="toggleDark"
          />
        </el-tooltip>
      </div>
      <div class="px-4">
        <el-tooltip effect="light" content="支持与反馈" placement="bottom">
          <el-button circle class="borderless-button white-to-gray">
            <el-icon :size="24"><QuestionFilled /></el-icon>
          </el-button>
        </el-tooltip>
      </div>
      <div class="m-4">
        <el-avatar :size="48" :src="circleUrl" />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, toRefs, watch } from 'vue'
import { Search, Menu, Sunny, Moon, QuestionFilled, Upload } from '@element-plus/icons-vue'
import { useDark, useToggle } from '@vueuse/core'
import { useRouter } from 'vue-router'

const isDark = useDark()
const toggleDark = useToggle(isDark)

const state = reactive({
  circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
  squareUrl: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
  sizeList: ['small', '', 'large'] as const,
})

const { circleUrl } = toRefs(state)

const showUpload = ref(true)
const router = useRouter()
watch(
  () => router.currentRoute,
  (newRoute) => {
    // 当路由发生变化时，这个函数会被调用
    if (newRoute.value.path == '/') {
      showUpload.value = true
    } else {
      showUpload.value = false
    }
  },
  {
    immediate: true, // 立即监听，不需要等待首次渲染
    deep: true, // 深度监听路由对象的变化
  },
)
</script>

<style lang="scss" scoped>
.el-menu-demo {
  &.el-menu--horizontal > .el-menu-item:nth-child(2) {
    margin-right: auto;
  }
}

.el-menu-demo .el-menu-item:hover {
  background-color: var(--el-menu-bg-color); /* 鼠标悬浮背景色 */
}

:deep(.el-input__wrapper),
:deep(.el-textarea__inner),
:deep(.el-select__wrapper) {
  border-radius: 120px;
}

.borderless-button {
  border: none !important;
  box-shadow: none !important; /* 可选，移除按钮的阴影 */
}

.white-to-gray {
  background-color: #fff !important; /* 背景 */
  border-color: #fff !important; /* 匹配按钮边框颜色 */
  color: #000; /* 文本颜色 */
}

.white-to-gray:hover {
  background-color: #cdd0d6 !important; /* 背景 */
  border-color: #cdd0d6 !important; /* 匹配按钮边框颜色 */
}
</style>
