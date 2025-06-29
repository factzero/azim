<template>
  <div class="album" ref="albumEl">
    <el-upload
      v-model:file-list="fileList"
      :auto-upload="false"
      :on-change="handleChange"
      :show-file-list="false"
      multiple
      accept=".jpg,.jpeg,.bmp,.png"
    >
      <el-button :icon="Upload" round class="white-to-gray flex items-center space-x-0.5"
        >上传</el-button
      >
    </el-upload>
    <el-dialog
      v-model="dialogVisible"
      title="上传结果"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :modal="false"
    >
      <div v-if="uploadResults.length > 0">
        <div v-for="(result, index) in uploadResults" :key="index" class="upload-result-item">
          <div class="file-name">{{ result.name }}</div>
          <div class="file-status" :class="{ error: !result.success }">
            <i :class="result.success ? 'el-icon-success' : 'el-icon-error'"></i>
            {{ result.success ? '上传成功' : '无法上传文件' }}
          </div>
        </div>
      </div>
      <div v-else>
        <p>暂无上传信息。</p>
      </div>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { Upload } from '@element-plus/icons-vue'
import { uploadImgs } from '@/api/ImgApi'
import type { UploadFile } from 'element-plus'

interface UploadResult {
  name: string
  success: boolean
}

const dialogVisible = ref(false)
const uploadResults = ref<UploadResult[]>([])

const fileList = ref([])

const handleChange = async (file: UploadFile) => {
  const nativeFile = file.raw instanceof File ? file.raw : file
  if (!(nativeFile instanceof File)) {
    console.warn('Invalid file object received')
    return
  }

  const formData = new FormData()
  formData.append('file', nativeFile)
  formData.append('mod_time', (nativeFile.lastModified / 1000.0).toString())

  try {
    await uploadImgs(formData)
    uploadResults.value.push({ name: nativeFile.name, success: true })
  } catch (err) {
    console.log('Upload error:', err)
    uploadResults.value.push({ name: nativeFile.name, success: false })
  }

  dialogVisible.value = true // 打开对话框
}
</script>

<style lang="scss" scoped>
.album {
  padding: 0 5px 5px 5px;
  height: 100%;
  overflow: hidden;
  overflow-y: scroll;

  &::-webkit-scrollbar {
    display: none;
    /* 隐藏滚动条 */
  }
}

.always-on-top-dialog {
  z-index: 9999 !important; // 强制置顶
  // pointer-events: auto !important; // 防止被遮罩阻挡交互
}

.upload-result-item {
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  display: flex;
  align-items: center;

  .file-name {
    font-weight: bold;
    flex: 1;
  }

  .file-status {
    color: #67c23a; // 默认绿色（成功）
    display: flex;
    align-items: center;

    i {
      margin-right: 5px;
      font-size: 16px;
    }
  }

  .file-status.error {
    color: #f56c6c; // 红色（失败）
  }
}
</style>
