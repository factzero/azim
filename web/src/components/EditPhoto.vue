<template>
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
} from '@element-plus/icons-vue'

const modelValue = defineModel()

const closeEdit = () => {
  modelValue.value = false
}
</script>

<style lang="scss" scoped>
.black-to-gray {
  background-color: #000 !important; /* 黑色背景 */
  border-color: #000 !important; /* 匹配按钮边框颜色 */
  color: #fff; /* 白色文本颜色 */
}

.black-to-gray:hover {
  background-color: #888 !important; /* 灰色背景 */
  border-color: #888 !important; /* 匹配按钮边框颜色 */
}
</style>
