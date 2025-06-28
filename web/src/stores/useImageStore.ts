// src/stores/useImageStore.ts
import { defineStore } from 'pinia'
import { ref, watchEffect } from 'vue'

interface ImageUpLoadInfo {
  total: number
  processed: number
  remain: number
  success: number
  duplicates: number
  error: number
}

interface ImageUpLoadState {
  status: string // 状态：error:失败, duplicates:相同照片, success:成功
  imageName: string // 图片名
  url: string // URL
}

export const useImageStore = defineStore('image', () => {
  const showStatusBadge = ref(true)

  const imgUploadInfo = ref<ImageUpLoadInfo>({
    total: 0,
    processed: 0,
    remain: 0,
    success: 0,
    duplicates: 0,
    error: 0,
  })

  const imgList = ref<ImageUpLoadState[]>([])

  function setTotal(n: number) {
    imgUploadInfo.value.total = n
  }

  function updateImageStatus(status: string, imageName: string, url: string = '') {
    imgUploadInfo.value.processed += 1
    imgUploadInfo.value.remain = imgUploadInfo.value.total - imgUploadInfo.value.processed

    if (status === 'success') {
      imgUploadInfo.value.success++
    } else if (status === 'error') {
      imgUploadInfo.value.error++
    } else if (status === 'duplicates') {
      imgUploadInfo.value.duplicates++
    }

    const img: ImageUpLoadState = {
      status,
      imageName: imageName,
      url: url || '',
    }
    imgList.value.push(img)
  }

  function setShowStatusBadge(value: boolean) {
    showStatusBadge.value = value
  }

  function removeImage(index: number) {
    imgList.value.splice(index, 1)
  }

  function clearImageList() {
    imgList.value = []
  }

  // 使用 watchEffect 自动响应依赖变化
  watchEffect(() => {
    showStatusBadge.value = imgList.value.length > 0
  })

  return {
    showStatusBadge,
    imgList,
    imgUploadInfo,
    setTotal,
    updateImageStatus,
    setShowStatusBadge,
    removeImage,
    clearImageList,
  }
})
