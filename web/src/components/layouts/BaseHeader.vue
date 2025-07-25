<template>
  <div class="flex items-center justify-between">
    <div class="flex items-center px-12 h-full">
      <div class="cursor-pointer" @click="router.push({ path: '/' })">
        <img style="width: 50px" src="@/assets/logo.svg" />
      </div>
    </div>

    <div class="flex items-center p-2 h-full w-1/2">
      <el-input
        clearable
        class="h-full"
        v-model="searchText"
        placeholder="搜索您的照片"
        @keyup.enter="SearchImgs"
      >
        <template #prefix>
          <el-button :icon="Search" circle class="borderless-button" />
        </template>
        <template #suffix>
          <el-button :icon="Menu" circle class="borderless-button" />
        </template>
      </el-input>
    </div>

    <div class="flex items-center">
      <div class="px-4" v-show="showUpload">
        <el-upload
          v-model:file-list="fileList"
          :auto-upload="false"
          :on-change="handleChangeUploadImg"
          :show-file-list="false"
          multiple
          accept=".jpg,.jpeg,.bmp,.png"
        >
          <el-button :icon="Upload" round class="white-to-gray flex items-center space-x-0.5"
            >上传</el-button
          >
        </el-upload>
      </div>
      <div class="px-4">
        <el-tooltip effect="light" content="切换主题" placement="bottom">
          <el-switch
            v-model="isDark"
            :active-action-icon="Moon"
            :inactive-action-icon="Sunny"
            inline-prompt
            @change="toggleDark"
          />
        </el-tooltip>
      </div>
      <div class="px-4">
        <el-tooltip effect="light" content="支持与反馈" placement="bottom">
          <el-button circle class="borderless-button white-to-gray">
            <el-icon :size="24"><QuestionFilled /></el-icon>
          </el-button>
        </el-tooltip>
      </div>
      <div class="m-4">
        <el-avatar :size="48" :src="circleUrl" />
      </div>
    </div>
    <div class="search-dialog-overlay" v-if="showSearchPage">
      <div class="bg-white w-full h-full">
        <el-container>
          <el-header class="flex items-center h-12 w-full bg-gray-400 relative px-4">
            <el-row :gutter="20" class="w-full h-full">
              <el-col :span="4">
                <div class="flex justify-start items-center h-full">
                  <el-tooltip effect="light" content="返回" placement="bottom">
                    <el-button size="large" circle @click="closeSearchPage">
                      <el-icon :size="24"><Back /></el-icon>
                    </el-button>
                  </el-tooltip>
                </div>
              </el-col>
              <el-col :span="16">
                <div class="flex justify-center items-center p-2 h-full">
                  <el-input
                    clearable
                    class="h-full"
                    v-model="searchText"
                    placeholder="搜索您的照片"
                    @keyup.enter="SearchImgs"
                  >
                    <template #prefix>
                      <el-button :icon="Search" circle class="borderless-button" />
                    </template>
                    <template #suffix>
                      <el-button :icon="Menu" circle class="borderless-button" />
                    </template>
                  </el-input>
                </div>
              </el-col>
            </el-row>
          </el-header>
          <el-main class="h-full w-full">
            <div v-loading="loading" class="flex flex-wrap gap-x-1 gap-y-0">
              <div v-for="photo in photos" :key="photo.id">
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
          </el-main>
        </el-container>
      </div>
    </div>
    <div v-if="showEdit" class="edit-dialog-overlay">
      <EditPhoto v-model="showEdit" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, toRefs, watch } from 'vue'
import {
  Search,
  Menu,
  Sunny,
  Moon,
  QuestionFilled,
  Upload,
  Back,
  Select,
  CloseBold,
} from '@element-plus/icons-vue'
import { useDark, useToggle } from '@vueuse/core'
import { useRouter } from 'vue-router'
import { uploadImgs, searchImgs } from '@/api/ImgApi'
import type { UploadFile } from 'element-plus'
import { useImageStore } from '@/stores/useImageStore'

interface Photo {
  id: number
  name: string
  url: string
  selected: boolean
}

const showSearchPage = ref(false)
const searchText = ref('')
const photos = reactive<Photo[]>([])
const loading = ref(false)

const SearchImgs = () => {
  loading.value = true
  photos.splice(0, photos.length)
  showSearchPage.value = true
  searchImgs({
    txt: searchText.value,
  })
    .then((res) => {
      for (const item of res.data.images) {
        photos.push({
          id: item.id,
          name: item.name,
          url: item.url,
          selected: false,
        })
      }
    })
    .finally(() => {
      // 无论成功或失败都关闭加载状态
      loading.value = false
    })
}

const closeSearchPage = () => {
  showSearchPage.value = false
  // 关闭搜索页面时重置加载状态
  loading.value = false
}

photos.push(
  {
    id: 1,
    name: 'Sunset',
    url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
    selected: false,
  },
  {
    id: 2,
    name: 'Mountain',
    url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
    selected: true,
  },
)

const showEdit = ref(false)

const selectEditPhoto = () => {
  console.log('selectEditPhoto')
  showEdit.value = true
}

function selectRemovePhoto(photo: Photo) {
  photo.selected = !photo.selected
}

const imageStore = useImageStore()
const isDark = useDark()
const toggleDark = useToggle(isDark)

const state = reactive({
  circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
  squareUrl: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
  sizeList: ['small', '', 'large'] as const,
})

const { circleUrl } = toRefs(state)

const fileList = ref([])

const handleChangeUploadImg = async (file: UploadFile) => {
  const nativeFile = file.raw || file
  if (!(nativeFile instanceof File)) {
    console.warn('Invalid file object received')
    return
  }

  const formData = new FormData()
  formData.append('file', nativeFile)
  formData.append('mod_time', (nativeFile.lastModified / 1000.0).toString())
  uploadImgs(formData)
    .then((res) => {
      const respData = res.data
      imageStore.updateImageStatus(respData.status, respData.filename, respData.url)
    })
    .catch((err) => {
      console.log('Upload error:', err.response?.data || err.message)
      imageStore.updateImageStatus('error', file.name)
    })
}

const showUpload = ref(true)
const router = useRouter()
watch(
  () => router.currentRoute,
  (newRoute) => {
    // 当路由发生变化时，这个函数会被调用
    if (newRoute.value.path == '/') {
      showUpload.value = true
    } else {
      showUpload.value = false
    }
  },
  {
    immediate: true, // 立即监听，不需要等待首次渲染
    deep: true, // 深度监听路由对象的变化
  },
)

watch(
  () => fileList.value,
  (newFileList) => {
    imageStore.setTotal(newFileList.length)
  },
)
</script>

<style lang="scss" scoped>
.el-menu-demo {
  &.el-menu--horizontal > .el-menu-item:nth-child(2) {
    margin-right: auto;
  }
}

.el-menu-demo .el-menu-item:hover {
  background-color: var(--el-menu-bg-color); /* 鼠标悬浮背景色 */
}

:deep(.el-input__wrapper),
:deep(.el-textarea__inner),
:deep(.el-select__wrapper) {
  border-radius: 120px;
}

.borderless-button {
  border: none !important;
  box-shadow: none !important; /* 可选，移除按钮的阴影 */
}

.white-to-gray {
  background-color: #fff !important; /* 背景 */
  border-color: #fff !important; /* 匹配按钮边框颜色 */
  color: #000; /* 文本颜色 */
}

.white-to-gray:hover {
  background-color: #cdd0d6 !important; /* 背景 */
  border-color: #cdd0d6 !important; /* 匹配按钮边框颜色 */
}

.search-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: black;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 900;
}

.edit-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: black;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 910;
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
</style>
