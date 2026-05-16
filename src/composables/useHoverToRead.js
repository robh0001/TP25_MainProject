import { computed, ref, watch } from 'vue'

const STORAGE_KEY = 'hk-hover-to-read-enabled'

const hoverToReadEnabled = ref(false)

if (typeof window !== 'undefined') {
  const savedValue = localStorage.getItem(STORAGE_KEY)

  if (savedValue === 'true') {
    hoverToReadEnabled.value = true
  }

  watch(
    hoverToReadEnabled,
    (isEnabled) => {
      if (typeof document !== 'undefined') {
        document.body.classList.toggle('hk-hover-to-read-active', isEnabled)
      }

      localStorage.setItem(STORAGE_KEY, String(isEnabled))
    },
    { immediate: true }
  )
}

export function useHoverToRead() {
  const isHoverToReadEnabled = computed(() => hoverToReadEnabled.value)

  function enableHoverToRead() {
    hoverToReadEnabled.value = true
  }

  function disableHoverToRead() {
    hoverToReadEnabled.value = false
  }

  function toggleHoverToRead() {
    hoverToReadEnabled.value = !hoverToReadEnabled.value
  }

  return {
    isHoverToReadEnabled,
    enableHoverToRead,
    disableHoverToRead,
    toggleHoverToRead,
  }
}