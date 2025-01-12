<template>
  <el-menu class="el-menu-demo" mode="horizontal" :ellipsis="false" router>
    <div class="grid grid-cols-12 gap-12 items-center justify-center">
      <div class="col-span-2">
        <el-menu-item index="/" class="flex items-center justify-center">
          <div class="flex items-center justify-center">
            <div class="text-xl" i-ep-element-plus />
            <span>Element Plus</span>
          </div>
        </el-menu-item>
      </div>

      <div class="col-span-6">
        <el-menu-item>
          <el-input clearable style="height: 50px" placeholder="搜索您的照片">
            <template #prefix>
              <el-button :icon="Search" circle class="borderless-button" />
            </template>
            <template #suffix>
              <el-button :icon="Menu" circle class="borderless-button" />
            </template>
          </el-input>
        </el-menu-item>
      </div>

      <div class="col-start-10">
        <div>
          <el-menu-item v-show="showUpload">
            <el-button :icon="QuestionFilled" circle class="borderless-button" />
          </el-menu-item>
        </div>
      </div>
      <div class="col-end-12">
        <div class="flex items-center justify-start">
          <div>
            <el-switch
              v-model="isDark"
              :active-action-icon="Moon"
              :inactive-action-icon="Sunny"
              inline-prompt
              @change="toggleDark"
            />
          </div>

          <div class="px-4">
            <el-button :icon="QuestionFilled" circle class="borderless-button" />
          </div>

          <div>
            <el-avatar :size="50" :src="circleUrl" />
          </div>
        </div>
      </div>
    </div>
  </el-menu>
</template>

<script lang="ts" setup>
import { reactive, ref, toRefs, watch } from 'vue'
import { Search, Menu, Sunny, Moon, QuestionFilled } from '@element-plus/icons-vue'
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
</style>
