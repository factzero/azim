<template>
  <div class="bg-black w-full h-full">
    <el-container>
      <el-header class="flex items-center h-12 w-full">
        <el-row class="flex justify-start items-center w-full">
          <el-col :span="1" class="h-full flex items-center justify-start">
            <el-tooltip effect="dark" content="返回" placement="bottom">
              <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                <el-icon :size="24" class="custom-icon-color"><Back /></el-icon>
              </el-button>
            </el-tooltip>
          </el-col>
          <el-col :offset="17" :span="6" class="h-full flex items-center justify-end">
            <div class="h-full flex items-center justify-end">
              <el-tooltip effect="dark" content="共享" placement="bottom">
                <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                  <el-icon :size="24" class="custom-icon-color"><Share /></el-icon>
                </el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="缩放" placement="bottom">
                <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                  <el-icon :size="24" class="custom-icon-color"><ZoomIn /></el-icon>
                </el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="复制" placement="bottom">
                <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                  <el-icon :size="24" class="custom-icon-color"><CopyDocument /></el-icon>
                </el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="信息" placement="bottom">
                <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                  <el-icon :size="24" class="custom-icon-color"><InfoFilled /></el-icon>
                </el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="收藏" placement="bottom">
                <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                  <el-icon :size="24" class="custom-icon-color"><Star /></el-icon>
                </el-button>
              </el-tooltip>
              <el-tooltip effect="dark" content="删除" placement="bottom">
                <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                  <el-icon :size="24" class="custom-icon-color"><Delete /></el-icon>
                </el-button>
              </el-tooltip>

              <el-dropdown placement="bottom">
                <el-button size="large" circle class="black-to-gray">
                  <el-icon :size="24" class="custom-icon-color" style="transform: rotate(90deg)">
                    <MoreFilled />
                  </el-icon>
                </el-button>

                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :icon="DataBoard">幻灯片放映</el-dropdown-item>
                    <el-dropdown-item :icon="Download">下载</el-dropdown-item>
                    <el-dropdown-item :icon="DocumentAdd">添加到相册</el-dropdown-item>
                    <el-dropdown-item :icon="Share">添加到共享相册</el-dropdown-item>
                    <el-dropdown-item :icon="User">设为个人资料图片</el-dropdown-item>
                    <el-dropdown-item :icon="MoreFilled">归档</el-dropdown-item>
                    <el-dropdown-item :icon="Upload">上传以替换</el-dropdown-item>
                    <el-dropdown-item :icon="MoreFilled">在时间轴查看</el-dropdown-item>
                    <el-dropdown-item :icon="MoreFilled">刷新人脸</el-dropdown-item>
                    <el-dropdown-item :icon="MoreFilled">刷新元数据</el-dropdown-item>
                    <el-dropdown-item :icon="MoreFilled">刷新缩略图</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </el-col>
        </el-row>
      </el-header>
      <el-main class="w-full p-0" style="height: calc(100vh - 48px)">
        <el-row class="flex justify-between items-center h-full w-full">
          <el-col :span="1" class="h-full flex items-center justify-start">
            <!-- 上一张按钮 -->
            <div class="h-full flex items-center justify-start">
              <el-button
                circle
                size="large"
                class="black-to-gray"
                :disabled="currentPhotoIndex <= 0"
                @click="prevPhoto"
              >
                <el-icon :size="32" class="custom-icon-color"><ArrowLeft /></el-icon>
              </el-button>
            </div>
          </el-col>

          <el-col :span="22" class="photo-area">
            <!-- 照片显示区域，添加过渡效果 -->
            <transition name="fade" mode="out-in">
              <el-image
                class="photo-display"
                :key="currentPhotoIndex"
                :src="currentPhoto.url"
                fit="cover"
              >
                <template #placeholder>
                  <div class="image-placeholder">
                    <el-icon :size="50"><Picture /></el-icon>
                  </div>
                </template>
                <template #error>
                  <div class="image-error">
                    <el-icon :size="50"><Picture /></el-icon>
                  </div>
                </template>
              </el-image>
            </transition>
          </el-col>

          <el-col :span="1" class="h-full flex items-end justify-end">
            <!-- 下一张按钮 -->
            <div class="h-full flex items-center justify-end">
              <el-button
                circle
                size="large"
                class="black-to-gray"
                :disabled="currentPhotoIndex >= allPhotos.length - 1"
                @click="nextPhoto"
              >
                <el-icon :size="32" class="custom-icon-color"><ArrowRight /></el-icon>
              </el-button>
            </div>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import {
  Back,
  Share,
  ZoomIn,
  CopyDocument,
  InfoFilled,
  Star,
  Delete,
  MoreFilled,
  DataBoard,
  Download,
  DocumentAdd,
  User,
  Upload,
  ArrowLeft,
  ArrowRight,
  Picture,
} from '@element-plus/icons-vue'
import { computed, ref, watch } from 'vue'

// 定义照片接口
interface Photo {
  id: number
  name: string
  url: string
  selected: boolean
}

// 定义组件属性
const props = defineProps<{
  allPhotos: Photo[]
  initialIndex: number
}>()

const modelValue = defineModel()

// 当前照片索引
const currentPhotoIndex = ref(props.initialIndex)

// 计算当前显示的照片
const currentPhoto = computed(() => {
  return props.allPhotos[currentPhotoIndex.value]
})

// 切换到上一张照片
const prevPhoto = () => {
  if (currentPhotoIndex.value > 0) {
    currentPhotoIndex.value--
  }
}

// 切换到下一张照片
const nextPhoto = () => {
  if (currentPhotoIndex.value < props.allPhotos.length - 1) {
    currentPhotoIndex.value++
  }
}

const closeEdit = () => {
  modelValue.value = false
}

// 监听初始索引变化
watch(
  () => props.initialIndex,
  (newIndex) => {
    currentPhotoIndex.value = newIndex
  },
)
</script>

<style lang="scss" scoped>
.black-to-gray {
  background-color: #000 !important;
  border-color: #000 !important;
  color: #fff;
}

.black-to-gray:hover {
  background-color: #888 !important;
  border-color: #888 !important;
}

/* 禁用状态样式 */
:deep(.el-button.is-disabled) {
  opacity: 0.5;
  cursor: not-allowed;
}

.photo-area {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}

.photo-display {
  width: 100% !important;
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;

  :deep(.el-image__inner) {
    object-fit: contain !important;
    width: 100% !important;
    height: 100% !important;
    max-width: none !important;
    max-height: none !important;
  }

  :deep(.el-image__placeholder),
  :deep(.el-image__error) {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    background-color: #000;
  }
}

/* 添加淡入淡出过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.image-placeholder,
.image-error {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: #000;
  color: #666;
}
</style>
