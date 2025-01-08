<template>
  <el-container class="layout-cont h-full">
    <el-header class="header-cont">
      <div>Header</div>
    </el-header>
    <el-divider class="el-divider_top" />
    <el-container>
      <el-aside class="aside-cont"><BaseSide /></el-aside>
      <el-divider direction="vertical" />
      <el-main>Main</el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup></script>

<style lang="scss" scoped>
.el-container.layout-cont {
  .header-cont {
    @apply px-4 h-16 bg-white;
  }

  .aside-cont {
    @apply w-48 h-full bg-white;
  }
}

.el-divider_top {
  margin: 0 0 0 0;
  border-color: gray;
}

.el-divider--vertical {
  display: inline-block;
  height: 100%;
  margin: 0 0;
  vertical-align: middle;
  position: relative;
  border-color: gray;
}
</style>
