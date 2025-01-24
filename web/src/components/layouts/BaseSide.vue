<script lang="ts" setup>
import {
  Picture,
  PictureFilled,
  Search,
  MapLocation,
  Share,
  Star,
  Suitcase,
  Folder,
  Delete,
} from '@element-plus/icons-vue'
import { ref } from 'vue'
import { useMenuStore } from '@/stores/menu'

defineProps(['sidelCollapse'])

const serverStatus = ref('online')
const centerDialogVisible = ref(false)
const menuStore = useMenuStore()
const activeIndex = ref(menuStore.loadActiveIndex)
</script>

<template>
  <el-menu :default-active="activeIndex" router :collapse="sidelCollapse" class="sidebar-menu">
    <el-menu-item index="/">
      <el-icon>
        <Picture />
      </el-icon>
      <template #title> 图片 </template>
    </el-menu-item>
    <el-menu-item index="/exploreImgs">
      <el-icon>
        <Search />
      </el-icon>
      <template #title> 探索 </template>
    </el-menu-item>
    <el-menu-item index="/mapLocation">
      <el-icon>
        <MapLocation />
      </el-icon>
      <template #title> 地图 </template>
    </el-menu-item>
    <el-menu-item index="/shareImgs">
      <el-icon>
        <Share />
      </el-icon>
      <template #title> 共享 </template>
    </el-menu-item>

    <div v-if="sidelCollapse" class="flex justify-center align-middle">
      <el-divider class="custom-divider" />
    </div>
    <div v-else class="p-4 h-12 text-left text-sm">图库</div>

    <el-menu-item index="/exploreImgs">
      <el-icon>
        <Star />
      </el-icon>
      <template #title> 收藏夹 </template>
    </el-menu-item>
    <el-menu-item index="/exploreImgs">
      <el-icon>
        <PictureFilled />
      </el-icon>
      <template #title> 相册 </template>
    </el-menu-item>
    <el-menu-item index="/exploreImgs">
      <el-icon>
        <Suitcase />
      </el-icon>
      <template #title> 实用工具 </template>
    </el-menu-item>
    <el-menu-item index="/exploreImgs">
      <el-icon>
        <Folder />
      </el-icon>
      <template #title> 归档 </template>
    </el-menu-item>
    <el-menu-item index="/exploreImgs">
      <el-icon>
        <Delete />
      </el-icon>
      <template #title> 回收站 </template>
    </el-menu-item>

    <div v-show="sidelCollapse != true" class="px-4 py-2">
      <div class="bg-slate-50 px-2 py-2" style="width: 140px">
        <div class="text-left">存储空间</div>
        <div class="text-slate-500 py-2 text-sm">已用 : 3.5GB / 16GB</div>
        <div class="custom-progress">
          <el-progress :show-text="false" :stroke-width="10" :percentage="60" />
        </div>
      </div>

      <div class="text-left text-sm py-4">
        <div v-if="serverStatus == 'online'" @click="centerDialogVisible = true">
          服务器在线 <el-badge :is-dot="true" type="success" class="pr-2" /> v0.0.1
        </div>
        <div v-else :style="{ color: '#F56C6C' }">服务器离线 <el-badge :is-dot="true" /></div>
      </div>

      <el-dialog v-model="centerDialogVisible" title="关于" width="500" align-center>
        <span>Open the dialog from the center from the screen</span>
      </el-dialog>
    </div>
  </el-menu>
</template>

<style lang="scss" scoped>
/* 自定义选中项的样式 */
.sidebar-menu .el-menu-item.is-active {
  background-color: #ecf5ff !important; /* 设置选中项的背景色 */
  color: #409eff !important; /* 设置选中项的文字颜色 */
  border-radius: 0 32px 32px 0;
}

/* 可选：为所有菜单项设置统一的高度 */
.sidebar-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
}

/* 确保整个菜单项（包括图标和文本）都能被点击 */
.sidebar-menu .el-menu-item {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding-left: 20px !important; /* 调整内边距以适应布局 */
  border-radius: 0 32px 32px 0;
}

/* 鼠标悬停时的样式 */
.sidebar-menu .el-menu-item:hover {
  background-color: #f5f7fa !important; /* 悬停时的背景色 */
  border-radius: 0 32px 32px 0;
}

.el-menu {
  border-right: 0 !important;
}

.custom-divider {
  width: 50%; /* 设置为父元素的 50% 宽度 */
}

.custom-progress .el-progress--line {
  margin-bottom: 10px;
  max-width: 120px;
}
</style>
