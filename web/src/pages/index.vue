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
                @click="selectEditPhoto(photo)"
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
    <EditPhoto v-model="showEdit" :all-photos="allPhotosList" :initial-index="selectedPhotoIndex" />
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { Select, CloseBold } from '@element-plus/icons-vue'
import { getAllImgsInfo } from '@/api/ImgApi'

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

const groupedPhotos = reactive<PhotoList[]>([])

// 计算展平后的所有照片列表
const allPhotosList = computed<Photo[]>(() => {
  const photos: Photo[] = []
  groupedPhotos.forEach((group) => {
    group.photos.forEach((photo) => {
      photos.push(photo)
    })
  })
  return photos
})

// 当前选中的照片索引
const selectedPhotoIndex = ref(0)

const getImgs = async () => {
  try {
    const res = await getAllImgsInfo()

    // 假设返回的数据在 res.data.images 数组中
    const rawPhotos = res.data.images

    // 构建 Map<year-month, Photo[]>
    const groupedMap = new Map<string, Photo[]>()

    for (const item of rawPhotos) {
      const yearMonthDate = item.time

      const photo: Photo = {
        id: item.id,
        name: item.name,
        url: item.url,
        selected: false,
      }

      if (!groupedMap.has(yearMonthDate)) {
        groupedMap.set(yearMonthDate, [])
      }

      groupedMap.get(yearMonthDate)?.push(photo)
    }

    // 构造新的 groupedPhotos 数据
    const newGroupedPhotos: PhotoList[] = []

    for (const [yearMonthDate, photos] of groupedMap.entries()) {
      newGroupedPhotos.push({
        timestamp: yearMonthDate,
        photos,
      })
    }

    // 清空并更新 reactive 数据
    groupedPhotos.splice(0, groupedPhotos.length, ...newGroupedPhotos)
  } catch (error) {
    console.error('Failed to fetch image info:', error)
  }
}

function selectRemovePhoto(photo: Photo) {
  photo.selected = !photo.selected
}

const showEdit = ref(false)

// 修改 selectEditPhoto 方法以接受照片参数
const selectEditPhoto = (photo: Photo) => {
  // 找到选中照片在所有照片中的索引
  const index = allPhotosList.value.findIndex((p) => p.id === photo.id)
  if (index !== -1) {
    selectedPhotoIndex.value = index
  }
  showEdit.value = true
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
let Fntimer: ReturnType<typeof setTimeout> | null = null

/** 以下是右边日期进度条 */
const initTimeline = () => {
  // 获取左边图片区域高度
  const elTimelineHtml = document.querySelector('.el-timeline') as HTMLElement
  if (!elTimelineHtml) return

  const elTimelineHeight = elTimelineHtml.scrollHeight

  // 获取左边图片每个月的区块
  const months = document.querySelectorAll('.month') as NodeListOf<HTMLElement>
  const arrTemp: TimelineItem[] = []
  const displayedYears = new Set<string>() // 记录已处理过的年份

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

    const year = extractYear(month.getAttribute('data-year-month')!)
    const yearMonth = extractYearMonth(month.getAttribute('data-year-month')!)
    let shouldShowYearText = false
    // 判断是否已经显示过该年
    if (year && !displayedYears.has(year)) {
      shouldShowYearText = true
      displayedYears.add(year)
    }

    // 打印每个元素的位置和占比
    arrTemp.push({
      year: shouldShowYearText ? year : null,
      yearMonth: yearMonth,
      positionPercentage: Number(percentage.toFixed(2)),
      heightPercentage: Number(heightPercentage.toFixed(2)),
    })
  })

  timeline.value = arrTemp

  nextTick(() => {
    // 使用以下代码，必须需要.album作为滚动区域，别的区域不行
    // 监听 .album 滚动事件
    const albumElement = document.querySelector('.album') as HTMLElement
    if (albumElement) {
      albumElement.addEventListener('scroll', onAlbumScroll)
    }
  })
}

onMounted(async () => {
  await getImgs()
  await nextTick() // 确保 DOM 更新后再操作 DOM
  initTimeline()
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
const extractYear = (dateStr: string): string | null => {
  const parts = dateStr.split('-')
  return parts.length > 0 && parts[0] ? parts[0] : null
}
// 将年月日提取为年月
const extractYearMonth = (dateStr: string): string | null => {
  const parts = dateStr.split('-')
  return `${parts[0]}-${parts[1]}`
}
</script>

<style lang="scss" scoped>
:deep(.el-timeline-item__timestamp.is-top) {
  position: -webkit-sticky; /* Safari */
  position: sticky;
  top: 0;
  z-index: 1;
  padding: 10px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  background-color: var(--el-bg-color);
}

/* 统一 el-timeline-item 的背景色 */
:deep(.el-timeline-item) {
  background-color: var(--el-bg-color);
}

.album {
  padding: 0 5px 5px 5px;
  height: 100%;
  overflow: hidden;
  overflow-y: scroll;
  background-color: var(--el-bg-color-page);

  &::-webkit-scrollbar {
    display: none;
    /* 隐藏滚动条 */
  }
}

.photo-card {
  position: relative;
  cursor: pointer;
  transition: transform 0.3s ease;
  background-color: var(--el-bg-color);
  border: none;
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
  transform: scale(0.8);
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
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.timeline-box {
  padding: 37.5px 0;
  top: 0;
  right: 0;
  width: 70px;
  height: 100%;
  position: absolute;
  z-index: 800;

  .timeline {
    position: relative;
    width: 100%;
    height: 100%;
    color: var(--custom-timeline-color);
    cursor: row-resize;
    user-select: none;
    /* 修改这里，统一背景色 */
    background-color: var(--el-bg-color);
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
        background: var(--custom-timeline-dot);
      }

      .txt {
        position: absolute;
        width: 100%;
        bottom: 100%;
        text-indent: 10px;
        /* 第一行文本向左缩进，效果像右往左 */
        line-height: 1;
        transform: translateY(calc(50% - 2.5px));
        color: var(--custom-timeline-color);
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
      background: var(--custom-tips-bg);
      pointer-events: none;
      border-bottom: 2px solid var(--custom-tips-border);
      border-top-left-radius: 6px;
      box-shadow: -1px -1px 5px var(--el-box-shadow-light);
      color: var(--el-text-color-primary);

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
        background: var(--custom-tips-border);
      }
    }
  }
}
</style>
