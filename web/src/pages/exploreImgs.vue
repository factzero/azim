<template>
  <div>explore images</div>

  <el-input clearable style="width: 300px; height: 50px">
    <template #prefix>
      <el-button :icon="Search" circle class="borderless-button" />
    </template>
    <template #suffix>
      <el-button :icon="Menu" circle class="borderless-button" />
    </template>
  </el-input>

  <el-input class="custom-input" placeholder="请输入内容"> </el-input>

  <el-switch
    v-model="isDark"
    :active-action-icon="Moon"
    :inactive-action-icon="Sunny"
    inline-prompt
    @change="toggleDark"
  />
</template>

<script lang="ts" setup>
import { Search, Menu, Sunny, Moon } from '@element-plus/icons-vue'
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark()
const toggleDark = useToggle(isDark)
</script>

<style scoped>
:deep(.el-input__wrapper),
:deep(.el-textarea__inner),
:deep(.el-select__wrapper) {
  border-radius: 120px;
}

.borderless-button {
  border: none !important;
  box-shadow: none !important; /* 可选，移除按钮的阴影 */
}

.custom-input {
  position: relative;
  overflow: hidden;
  padding: 0;
}

.custom-input::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #fff; /* 输入框的背景颜色 */
  border-radius: 50%; /* 设置为50%以实现圆形输入框 */
}

.custom-input input {
  border: none;
  outline: none;
  background-color: transparent;
  padding: 10px; /* 根据需要调整 */
}
</style>
