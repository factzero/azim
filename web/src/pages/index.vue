<template>
  <div class="album" ref="albumEl">
    <el-timeline>
      <div
        class="month"
        v-for="(items, index) in convertFn(groupedPhotos)"
        :data-year="extractYear(items[0].timestamp)"
        :data-year-month="extractYearMonth(items[0].timestamp)"
        :key="index"
      >
        <el-timeline-item
          v-for="(group, index) in items"
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
      </div>
    </el-timeline>
    <div class="timeline-box">
      <div
        ref="timelineEl"
        class="timeline"
        @mousemove="onMousemove"
        @mouseleave="onMouseleave"
        @mousedown="onMousedown"
        @mouseup="onMouseup"
      >
        <div
          class="item"
          v-for="(item, index) in timeline"
          :data-year-month="item.yearMonth"
          :style="{ top: `${item.positionPercentage}%`, height: `${item.heightPercentage}%` }"
          :key="index"
        >
          <div class="dot"></div>
          <text class="txt" v-if="item.year">{{ item.year }}</text>
        </div>
        <div
          class="tips move"
          :style="{ bottom: 'auto', top: `${(posY < 0 ? 0 : posY) - 30}px` }"
          v-if="currentAttr"
        >
          {{ currentAttr }}
        </div>
        <div
          class="tips"
          :class="{ noClick: !tipsShow }"
          :style="{
            bottom: 'auto',
            top: `${tipsShow ? (tipsY < 0 ? 0 : tipsY) - 30 : tipsY - 2}px`,
          }"
        >
          {{ tipsValue }}
        </div>
      </div>
    </div>
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
import { reactive, ref, onMounted, onUnmounted, nextTick } from 'vue'
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
groupedPhotos.push({ timestamp: '2018-6-1', photos: [] })
groupedPhotos.push({ timestamp: '2017-6-5', photos: [] })
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
for (let i = 0; i < 10; i++) {
  GlobalID++
  groupedPhotos[3].photos.push({
    id: GlobalID,
    name: '31.jpg',
    url: 'https://fuss10.elemecdn.com/9/bb/e27858e973f5d7d3904835f46abbdjpeg.jpeg',
    selected: false,
  })
}

for (let i = 0; i < 10; i++) {
  GlobalID++
  groupedPhotos[4].photos.push({
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

// 将groupedPhotos转换成可以按月分组
const convertFn = (groupedPhotos: PhotoList[]) => {
  const arrTemp: PhotoList[][] = []
  const yearMonthArr: string[] = []
  groupedPhotos.forEach((item) => {
    const yearMonth = item.timestamp.split('-').slice(0, 2).join('-')
    if (yearMonthArr.includes(yearMonth)) {
      const l = arrTemp.length
      arrTemp[l - 1].push(item)
    } else {
      yearMonthArr.push(yearMonth)
      arrTemp.push([item])
    }
  })
  return arrTemp
}

// 用来储存右边时间条的数据
interface TimelineItem {
  year: string | null
  yearMonth: string | null
  positionPercentage: number
  heightPercentage: number
}

const albumEl = ref<HTMLDivElement | null>(null)
const timelineEl = ref<HTMLDivElement | null>(null)
const timeline = ref<TimelineItem[]>([])
let Fntimer: number | null = null

/** 以下是右边日期进度条 */
onMounted(() => {
  // if (albumEl.value) {
  //   console.log('Album 高度:', albumEl.value.clientHeight);
  // }
  // 获取左边图片区域高度
  const elTimelineHtml = document.querySelector('.el-timeline') as HTMLElement
  const elTimelineHeight = elTimelineHtml.scrollHeight
  // 获取左边图片每个月的区块
  const months = document.querySelectorAll('.month') as NodeListOf<HTMLElement>
  const arrTemp: TimelineItem[] = []
  months.forEach((month) => {
    // 获取元素
    const rect = month.getBoundingClientRect()
    // 获取每个月区块的高度
    const monthHeight = rect.height

    // 计算元素顶部相对于 elTimeline 的位置
    const topPosition = rect.top - elTimelineHtml.getBoundingClientRect().top

    // 计算元素在 .el-timeline 中的位置百分比
    const percentage = (topPosition / elTimelineHeight) * 100
    // 计算元素高度所占 .el-timeline 高度的百分比
    const heightPercentage = (monthHeight / elTimelineHeight) * 100
    // 打印每个元素的位置和占比
    arrTemp.push({
      year: month.getAttribute('data-year'),
      yearMonth: month.getAttribute('data-year-month'),
      positionPercentage: Number(percentage.toFixed(2)),
      heightPercentage: Number(heightPercentage.toFixed(2)),
    })
    timeline.value = arrTemp
  })
  // 渲染节点完毕时，对滚动条进行监听
  nextTick(() => {
    // 使用以下代码，必须需要.album作为滚动区域，别的区域不行
    // 监听 .album 滚动事件
    const albumElement = document.querySelector('.album') as HTMLElement
    if (albumElement) {
      albumElement.addEventListener('scroll', onAlbumScroll)
    }
  })
})

const onAlbumScroll = (event: Event) => {
  const album = event.currentTarget as HTMLElement
  const timeline = document.querySelector('.timeline') as HTMLElement

  if (!album || !timeline) return
  // 获取 album 和 timeline 的滚动位置
  const albumScrollTop = album.scrollTop

  // 获取所有的 .item 元素
  const items = Array.from(timeline.querySelectorAll('.item')) as HTMLElement[]

  // 遍历所有的 .item 元素，找到当前应展示 tips 的位置
  let targetItem: HTMLElement | null = null
  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    const itemRect = item.getBoundingClientRect()

    // 判断滚动位置是否在当前 item 的显示范围内
    if (itemRect.top <= albumScrollTop && itemRect.bottom >= albumScrollTop) {
      targetItem = item
      break
    }
  }
  if (targetItem) {
    const attr = targetItem.getAttribute('data-year-month')
    if (attr) {
      const value = attr.split('-')
      tipsValue.value = `${value[0]}年${value[1]}月`
    }
  }
  // 显示出tips
  tipsShow.value = true
  // 获取 album 的总高度和当前滚动位置
  const albumHeight = album.scrollHeight - album.clientHeight
  // 计算 album 的滚动百分比
  const scrollPercentage = (albumScrollTop / albumHeight) * 100
  // 获取 .timeline 的固定高度
  const timelineHeight = timeline.clientHeight
  // 计算 timeline 对应位置的像素值
  const timelineScrollTop = (scrollPercentage / 100) * timelineHeight
  tipsY.value = timelineScrollTop
  // 清理定时器，避免重复运行
  if (Fntimer) {
    clearTimeout(Fntimer)
  }
  // 定时器
  Fntimer = setTimeout(() => {
    // 一段时间不操作时隐藏
    tipsShow.value = false
  }, 1000)
}

onUnmounted(() => {
  const album = document.querySelector('.album') as HTMLElement | null
  if (album) {
    album.removeEventListener('scroll', onAlbumScroll)
  }
})

// 用于存储鼠标在 timeline 内的相对坐标
const posX = ref(0)
const posY = ref(0)
// 用于存储当前鼠标位置下子元素的 data-year-month 属性
const currentAttr = ref<string>('')

/**
 * 鼠标移动事件处理函数：
 * - 计算鼠标在 timeline 内的相对坐标
 * - 根据鼠标所在位置获取 timeline 子元素的 data-year-month 属性
 */
const onMousemove = (event: MouseEvent) => {
  if (isDragging) {
    return
  }
  const timeline = event.currentTarget as HTMLElement
  // 获取 timeline 的边界信息
  const timelineRect = timeline.getBoundingClientRect()
  // 计算鼠标在 timeline 内的相对坐标
  posX.value = event.clientX - timelineRect.left
  posY.value = event.clientY - timelineRect.top
  const element = (event.target as HTMLElement).closest('.item') as HTMLElement
  const attr = element.getAttribute('data-year-month')
  if (attr) {
    const value = attr.split('-')
    currentAttr.value = `${value[0]}年${value[1]}月`
  }
}
/**
 * 鼠标移出事件处理函数：
 * 移除就清空currentAttr
 *
 */
const onMouseleave = () => {
  currentAttr.value = ''
}
/**
 * 鼠标点击事件处理函数：
 */
let isDragging: boolean = false
const onMousedown = (event: MouseEvent) => {
  isDragging = true
  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', onMouseUp)
  // 如果为true表示按住鼠标，false是松开鼠标
  // 计算当前点击的位置
  const currentTarget = event.currentTarget as HTMLElement
  const timelineRect = currentTarget.getBoundingClientRect()
  tipsY.value = event.clientY - timelineRect.top
  tipsValue.value = currentAttr.value
  tipsShow.value = true

  // 获取 .timeline 的固定高度
  const timelineHeight = timelineRect.height
  if (tipsY.value < 0) {
    tipsY.value = 0
  }
  // 获取进度条百分比
  const percentage = (tipsY.value / timelineHeight) * 100
  const albumElement = document.querySelector('.album') as HTMLElement
  const scrollHeight = albumElement.scrollHeight
  const albumHeight = albumElement.clientHeight
  // 根据百分比获取实际的像素
  const scrollPosition = (scrollHeight - albumHeight) * (percentage / 100)
  // 滚动区域跳转到对应位置
  albumElement.scrollTop = scrollPosition

  if (Fntimer) {
    clearTimeout(Fntimer)
  }
  // 定时器
  Fntimer = setTimeout(() => {
    tipsShow.value = false
  }, 1000)
}

// 全局的监听
const onMouseMove = (event: MouseEvent) => {
  if (isDragging) {
    const timelineEl = document.querySelector('.timeline') as HTMLElement
    const timelineRect = timelineEl.getBoundingClientRect()
    const top = timelineRect.top
    const height = timelineRect.height
    const value = event.clientY - top
    if (value < 0) {
      tipsY.value = 0
    } else if (value > height) {
      tipsY.value = height
    } else {
      tipsY.value = value
    }
    posY.value = tipsY.value
    // 获取 .timeline 的固定高度
    const timelineHeight = timelineEl!.clientHeight
    // 获取进度条百分比
    const percentage = (tipsY.value / timelineHeight) * 100
    const albumElement = document.querySelector('.album') as HTMLElement
    const scrollHeight = albumElement.scrollHeight
    const albumHeight = albumElement.clientHeight
    // 根据百分比获取实际的像素
    const scrollPosition = (scrollHeight - albumHeight) * (percentage / 100)
    // 滚动区域跳转到对应位置
    albumElement.scrollTop = scrollPosition
  }
}
// 全局的监听
const onMouseUp = () => {
  isDragging = false
  document.removeEventListener('mousemove', onMouseMove)
  document.removeEventListener('mouseup', onMouseUp)
}

/**
 * 鼠标松开事件处理函数：
 *
 */
const onMouseup = () => {}
// 用来判断点击时间条时，是否显示tips
const tipsShow = ref(false)
const tipsValue = ref('')
// 点击时间条后的当前位置
const tipsY = ref(0)
// 将年月日提取为年
const extractYear = (dateStr: string): string | undefined => {
  const parts = dateStr.split('-')
  return parts[0]
}
// 将年月日提取为年月
const extractYearMonth = (dateStr: string): string | undefined => {
  const parts = dateStr.split('-')
  return `${parts[0]}-${parts[1]}`
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
  padding: 0 5px 5px 5px;
  height: 100%;
  overflow: hidden;
  overflow-y: scroll;

  &::-webkit-scrollbar {
    display: none;
    /* 隐藏滚动条 */
  }
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

.timeline-box {
  padding: 37.5px 0;
  top: 0;
  right: 0;
  width: 70px;
  height: 100%;
  position: absolute;
  z-index: 998;

  .timeline {
    position: relative;
    width: 100%;
    height: 100%;
    color: #3a3a3a;
    cursor: row-resize;
    user-select: none;
    /* 标准属性 */
    -webkit-user-select: none;
    /* Chrome、Safari、Opera */
    -moz-user-select: none;
    /* Firefox */
    -ms-user-select: none;

    .item {
      width: 100%;
      position: absolute;

      .dot {
        position: absolute;
        right: 15px;
        bottom: 0;
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #d1d5db;
      }

      .txt {
        position: absolute;
        width: 100%;
        bottom: 100%;
        text-indent: 10px;
        /* 第一行文本向左缩进，效果像右往左 */
        line-height: 1;
        transform: translateY(calc(50% - 2.5px));
      }
    }

    .tips {
      position: absolute;
      bottom: 100%;
      right: 0;
      width: 80px;
      height: 30px;
      line-height: 30px;
      text-align: center;
      background: rgba($color: #fff, $alpha: 0.8);
      pointer-events: none;
      border-bottom: 2px solid #5764bb;
      border-top-left-radius: 6px;
      box-shadow: -1px -1px 5px #a3a3a3;

      &.noClick {
        width: 50%;
        height: 2px;
        overflow: hidden;
        border-bottom: 0;
        border-top-left-radius: 0;
        box-shadow: none;
      }

      &.noClick::after {
        position: absolute;
        bottom: -100%;
        left: 0;
        content: '';
        width: 100%;
        height: 10px;
        background: #5764bb;
      }
    }
  }
}
</style>
