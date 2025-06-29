<template>
  <div class="status-badge" v-if="imageStore.showStatusBadge">
    <el-container>
      <el-header>
        <el-row :gutter="24">
          <el-col :span="16">
            <div class="text-sm">
              剩余{{ imageStore.imgUploadInfo.remain }} - 已处理
              {{ imageStore.imgUploadInfo.processed }}/{{ imageStore.imgUploadInfo.total }}
            </div>
            <div class="text-xs">
              已上传
              <span :style="{ color: '#67C23A' }">{{ imageStore.imgUploadInfo.success }}</span>
              - 错误
              <span :style="{ color: '#F56C6C' }">{{ imageStore.imgUploadInfo.error }}</span>
              - 重复
              <span :style="{ color: '#E6A23C' }">{{ imageStore.imgUploadInfo.duplicates }}</span>
            </div>
          </el-col>
          <el-col :span="8" class="text-right">
            <el-button circle size="small" class="icon-button">
              <el-icon :size="20"><Setting /></el-icon>
            </el-button>
            <el-button circle size="small" class="icon-button">
              <el-icon :size="20"><Minus /></el-icon>
            </el-button>
          </el-col>
        </el-row>
        <el-row :gutter="24">
          <el-col :span="8" :offset="16" class="text-right">
            <el-button circle size="small" class="icon-button">
              <el-icon :size="20"><Remove /></el-icon>
            </el-button>
          </el-col>
        </el-row>
      </el-header>
      <el-main>
        <el-row
          class="flex items-center py-1"
          v-for="(item, index) in imageStore.imgList"
          :key="index"
        >
          <el-col :span="2">
            <div class="flex items-center">
              <el-icon color="#E6A23C" :size="18"><Warning /></el-icon>
            </div>
          </el-col>
          <el-col :span="14">
            <div>{{ item.imageName.slice(-24) }}</div>
          </el-col>
          <el-col :span="8" class="text-right">
            <el-button circle size="small" class="icon-button">
              <el-icon :size="20" v-if="item.status === 'error'"><RefreshLeft /></el-icon>
              <el-icon :size="20" v-else><Link /></el-icon>
            </el-button>
            <el-button
              circle
              size="small"
              class="icon-button"
              @click="imageStore.removeImage(index)"
            >
              <el-icon :size="20"><Close /></el-icon>
            </el-button>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { Setting, Minus, Remove, Warning, Close, Link, RefreshLeft } from '@element-plus/icons-vue'
import { useImageStore } from '@/stores/useImageStore'

const imageStore = useImageStore()
</script>

<style lang="scss" scoped>
.status-badge {
  position: fixed;
  width: 300px;
  display: flex;
  align-items: center;
  background-color: #ebedf0;
  color: #303133;
  border-radius: 10px;
  padding: 12px 2px 2px 2px;
  font-size: 14px;
}

.icon-button {
  background-color: #ebedf0 !important; /* 背景 */
  border-color: #ebedf0 !important; /* 匹配按钮边框颜色 */
  color: #000; /* 文本颜色 */
}

.icon-button:hover {
  background-color: #cdd0d6 !important; /* 背景 */
  border-color: #cdd0d6 !important; /* 匹配按钮边框颜色 */
}
</style>
