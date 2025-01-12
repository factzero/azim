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
import { ref, onMounted, onBeforeUnmount } from 'vue'

defineProps(['sidelCollapse'])

const serverStatus = ref('online')
const centerDialogVisible = ref(false)
const isCollapse = ref(false)
const sideWidth = ref('100%')

const calcWinColl = () => {
  if (window.innerWidth < 800) {
    isCollapse.value = true
    sideWidth.value = '100%'
  } else {
    isCollapse.value = false
    sideWidth.value = '220px'
  }
}

onMounted(() => {
  window.addEventListener('resize', calcWinColl, false)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', calcWinColl, false)
})
</script>

<template>
  <el-menu router :collapse="sidelCollapse">
    <el-menu-item index="/showImgs">
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

    <div v-if="isCollapse" class="flex justify-center align-middle">
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

    <div v-show="isCollapse != true"  class="px-4 py-2">
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

    <!-- <div v-if="isCollapse != true">
        <div class="text-left text-xs">
          <div v-if="serverStatus == 'online'" @click="centerDialogVisible = true">
            服务器在线 <el-badge :is-dot="true" type="success" class="pr-2" /> v0.0.1
          </div>
          <div v-else :style="{ color: '#F56C6C' }">服务器离线 <el-badge :is-dot="true" /></div>
        </div>

        <el-dialog v-model="centerDialogVisible" title="关于" width="500" align-center>
          <span>Open the dialog from the center from the screen</span>
        </el-dialog> 
    </div> -->

    <!-- <el-card shadow="Never" v-if="isCollapse != true">
      <div class="text-left">存储空间</div>
      <div class="text-slate-400 py-2 text-xs">已用 : 3.5GB / 16GB</div>
      <el-progress :show-text="false" :stroke-width="12" :percentage="60" />

      <template #footer>
        <div class="text-left text-xs">
          <div v-if="serverStatus == 'online'" @click="centerDialogVisible = true">
            服务器在线 <el-badge :is-dot="true" type="success" class="pr-2" /> v0.0.1
          </div>
          <div v-else :style="{ color: '#F56C6C' }">服务器离线 <el-badge :is-dot="true" /></div>
        </div>

        <el-dialog v-model="centerDialogVisible" title="关于" width="500" align-center>
          <span>Open the dialog from the center from the screen</span>
        </el-dialog>
      </template>
    </el-card> -->
  </el-menu>
</template>

<style lang="scss" scoped>
.el-menu {
	border-right:0!important;
}

.custom-divider {
  width: 50%; /* 设置为父元素的 50% 宽度 */
}

.custom-progress .el-progress--line {
  margin-bottom: 10px;
  max-width: 120px;
}
</style>
