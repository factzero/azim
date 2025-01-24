<template>
  <div class="album">
    <el-timeline>
      <el-timeline-item
        v-for="(group, index) in groupedPhotos"
        :key="index"
        :timestamp="group.timestamp"
        placement="top"
      >
        <div class="flex flex-wrap gap-x-1 gap-y-0">
          <div v-for="photo in group.photos" :key="photo.id">
            <div
              class="photo-card"
              :class="{ 'bg-fuchsia-50': photo.selected }"
              @click="selectEditPhoto"
            >
              <el-image
                style="width: auto; height: 9rem"
                :src="photo.url"
                fit="contain"
                :class="{ 'selected-photo': photo.selected }"
              />
              <div class="overlay" :class="{ 'always-show': photo.selected }">
                <el-button
                  :icon="photo.selected ? Select : CloseBold"
                  :type="photo.selected ? 'primary' : 'info'"
                  class="delete-button"
                  circle
                  @click.stop="selectRemovePhoto(photo)"
                ></el-button>
              </div>
            </div>
          </div>
        </div>
      </el-timeline-item>
    </el-timeline>
  </div>
  <div v-if="showEdit" class="custom-dialog-overlay">
    <div class="bg-black w-full h-full">
      <el-container>
        <el-header class="flex justify-between items-center h-12 w-full">
          <div class="flex items-center">
            <el-tooltip effect="light" content="返回" placement="bottom">
              <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                <el-icon :size="24" class="custom-icon-color"><Back /></el-icon>
              </el-button>
            </el-tooltip>
          </div>
          <div class="flex items-center mx-2">
            <el-tooltip effect="light" content="共享" placement="bottom">
              <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                <el-icon :size="24" class="custom-icon-color"><Share /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip effect="light" content="缩放" placement="bottom">
              <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                <el-icon :size="24" class="custom-icon-color"><ZoomIn /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip effect="light" content="复制" placement="bottom">
              <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                <el-icon :size="24" class="custom-icon-color"><CopyDocument /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip effect="light" content="信息" placement="bottom">
              <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                <el-icon :size="24" class="custom-icon-color"><InfoFilled /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip effect="light" content="收藏" placement="bottom">
              <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                <el-icon :size="24" class="custom-icon-color"><Star /></el-icon>
              </el-button>
            </el-tooltip>
            <el-tooltip effect="light" content="删除" placement="bottom">
              <el-button size="large" circle class="black-to-gray" @click="closeEdit">
                <el-icon :size="24" class="custom-icon-color"><Delete /></el-icon>
              </el-button>
            </el-tooltip>

            <el-dropdown placement="bottom">
              <el-button size="large" circle class="black-to-gray">
                <el-icon :size="24" class="custom-icon-color" style="transform: rotate(90deg)"
                  ><MoreFilled
                /></el-icon>
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
        </el-header>
        <el-main class="h-full w-full">
          <div class="flex items-center justify-between">
            <el-button circle class="black-to-gray" :style="{ width: '48px', height: '48px' }">
              <el-icon :size="32" class="custom-icon-color"><ArrowLeft /></el-icon>
            </el-button>
            <el-image
              style="width: auto; height: 100%"
              src="https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"
              fit="contain"
            />
            <el-button circle class="black-to-gray" :style="{ width: '48px', height: '48px' }">
              <el-icon :size="32" class="custom-icon-color"><ArrowRight /></el-icon>
            </el-button>
          </div>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import {
  Select,
  CloseBold,
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
} from '@element-plus/icons-vue'

interface Photo {
  id: number
  name: string
  url: string
  selected: boolean
}

interface PhotoList {
  timestamp: string
  photos: Photo[]
}

let GlobalID = 0
const groupedPhotos = reactive<PhotoList[]>([])

groupedPhotos.push({ timestamp: '2020-1-19', photos: [] })
groupedPhotos.push({ timestamp: '2020-1-2', photos: [] })
groupedPhotos.push({ timestamp: '2020-1-1', photos: [] })
for (let i = 0; i < 10; i++) {
  GlobalID++
  groupedPhotos[0].photos.push({
    id: GlobalID,
    name: '31.jpg',
    url: 'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
    selected: false,
  })
}
for (let i = 0; i < 10; i++) {
  GlobalID++
  groupedPhotos[1].photos.push({
    id: GlobalID,
    name: '31.jpg',
    url: 'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
    selected: false,
  })
}
for (let i = 0; i < 20; i++) {
  GlobalID++
  groupedPhotos[2].photos.push({
    id: GlobalID,
    name: '31.jpg',
    url: 'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
    selected: false,
  })
}

function selectRemovePhoto(photo: Photo) {
  photo.selected = !photo.selected
}

const showEdit = ref(false)

const selectEditPhoto = () => {
  console.log('selectEditPhoto')
  showEdit.value = true
}

const closeEdit = () => {
  showEdit.value = false
}
</script>

<style lang="scss" scoped>
:deep(.el-timeline-item__timestamp.is-top) {
  position: -webkit-sticky; /* Safari */
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 1;
  padding: 10px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.album {
  padding: 5px;
}

.photo-card {
  position: relative;
  cursor: pointer;
  transition: transform 0.3s ease; /* 添加过渡效果 */
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.photo-card:hover .overlay:not(.always-show) {
  opacity: 1;
}

.always-show {
  opacity: 1 !important;
}

.selected-photo {
  transform: scale(0.8); /* 缩小图片 */
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.delete-button {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

.custom-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: black;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.black-to-gray {
  background-color: #000 !important; /* 黑色背景 */
  border-color: #000 !important; /* 匹配按钮边框颜色 */
  color: #fff; /* 白色文本颜色 */
}

.black-to-gray:hover {
  background-color: #888 !important; /* 灰色背景 */
  border-color: #888 !important; /* 匹配按钮边框颜色 */
}

.custom-icon-color {
  color: #ffffff; /* 针对字体图标 */
  fill: #ffffff; /* 针对SVG图标 */
}

:deep(.el-dropdown-menu__item) {
  padding-top: 12px;
  padding-bottom: 12px;
  font-size: 16px;
}

:deep(.el-dropdown-menu__item:hover) {
  background-color: #888;
  color: #000;
}
</style>
