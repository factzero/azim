import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useMenuStore = defineStore('menu', () => {
  const activeIndex = ref('/')
  function setActiveIndex(index: string) {
    activeIndex.value = index
    localStorage.setItem('activeMenuIndex', index)
  }
  const loadActiveIndex = computed(() => {
    const storedIndex = localStorage.getItem('activeMenuIndex')
    if (storedIndex) {
      activeIndex.value = storedIndex
    }
    return activeIndex.value
  })
  return { setActiveIndex, loadActiveIndex }
})
