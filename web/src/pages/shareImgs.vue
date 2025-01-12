<template>
  <div>share images</div>

  <el-menu class="custom-menu">
    <el-menu-item>
      <el-input clearable style="width: 300px; height: 50px">
        <template #prefix>
          <el-button :icon="Search" circle class="borderless-button" />
        </template>
        <template #suffix>
          <el-button :icon="Menu" circle class="borderless-button" />
        </template>
      </el-input>
    </el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup>
import { Search, Menu } from '@element-plus/icons-vue'
</script>

<style lang="scss" scoped>
:deep(.el-input__wrapper),
:deep(.el-textarea__inner),
:deep(.el-select__wrapper) {
  border-radius: 120px;
}

.borderless-button {
  border: none !important;
  box-shadow: none !important; /* 可选，移除按钮的阴影 */
}

.custom-menu .el-menu-item:hover {
  background-color: var(--el-menu-bg-color); /* 鼠标悬浮背景色 */
}
</style>
