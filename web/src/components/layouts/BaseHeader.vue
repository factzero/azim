<template>
  <el-menu class="el-menu-demo" mode="horizontal" :ellipsis="false" router>
    <el-menu-item index="/" style="width: 200px">
      <div class="flex items-center justify-center">
        <div class="text-xl" i-ep-element-plus />
        <span>Element Plus</span>
      </div>
    </el-menu-item>

    <el-menu-item>
      <el-input clearable style="width: 900px; height: 50px" placeholder="搜索您的照片">
        <template #prefix>
          <el-button :icon="Search" circle class="borderless-button" />
        </template>
        <template #suffix>
          <el-button :icon="Menu" circle class="borderless-button" />
        </template>
      </el-input>
    </el-menu-item>

    <el-menu-item>
      <el-switch
        v-model="isDark"
        :active-action-icon="Moon"
        :inactive-action-icon="Sunny"
        inline-prompt
        @change="toggleDark"
      />
    </el-menu-item>

    <el-menu-item>
      <el-button :icon="QuestionFilled" circle class="borderless-button" />
    </el-menu-item>

    <el-menu-item>
      <el-avatar :size="50" :src="circleUrl" />
    </el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup>
import { reactive, toRefs } from 'vue'
import { Search, Menu, Sunny, Moon, QuestionFilled } from '@element-plus/icons-vue'
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark()
const toggleDark = useToggle(isDark)

const state = reactive({
  circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
  squareUrl: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
  sizeList: ['small', '', 'large'] as const,
})

const { circleUrl } = toRefs(state)
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
