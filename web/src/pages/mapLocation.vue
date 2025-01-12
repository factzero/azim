<template>
  <el-input v-model="searchInput" placeholder="Type something" clearable>
    <template #suffix>
      <Search class="icon-search" style="width: 1em; height: 1em; margin-right: 6px" color="" />
    </template>
  </el-input>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const searchInput = ref('')
</script>

<style scoped>
.el-input {
  width: 600px;
  height: 44px;
  align-self: center;
  display: flex;
}

:deep(.el-input__wrapper) {
  margin-left: 5px;
  font-size: 15px;
  background-color: rgba(255, 255, 255, 0); /*覆盖原背景颜色，设置成透明 */
  border-radius: 120px;
  box-shadow: 2 2 2 2px;
}

:deep(.el-input__inner) {
  margin-left: 10px;
}

.icon-search:hover {
  color: #409efc; /* 改变颜色 */
  cursor: pointer; /* 将指针样式改为小手 */
}
</style>
