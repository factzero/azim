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
            <div class="photo-card" :class="{ 'bg-fuchsia-50': photo.selected }">
              <el-image
                style="width: auto; height: 9rem"
                :src="photo.url"
                fit="contain"
                :class="{ 'selected-photo': photo.selected }"
              />
              <div class="hover-effect">
                <el-button
                  :icon="Delete"
                  class="delete-button"
                  circle
                  @click="selectRemovePhoto(photo)"
                ></el-button>
              </div>
            </div>
          </div>
        </div>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { Delete } from '@element-plus/icons-vue'

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
  transition: transform 0.5s ease; /* 添加过渡效果 */

  &:hover {
    /* 鼠标悬停样式 */
    border-color: #409eff;

    .hover-effect {
      width: 100%;
      opacity: 1;
    }
  }
}

.hover-effect {
  /* 鼠标悬停效果样式 */
  position: absolute;
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100%;
  cursor: pointer;
  opacity: 0;
  transition: var(--transition);
}

.selected-photo {
  transform: scale(0.8); /* 缩小图片 */
  border-radius: 8px;
}

.delete-button {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}
</style>
