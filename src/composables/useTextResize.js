import { computed, onMounted, ref } from 'vue'

const STORAGE_KEY = 'hk-text-zoom-level'

const MIN_ZOOM_LEVEL = -2
const MAX_ZOOM_LEVEL = 5
const DEFAULT_ZOOM_LEVEL = 0

const zoomLevel = ref(DEFAULT_ZOOM_LEVEL)

function clampZoomLevel(value) {
  return Math.min(MAX_ZOOM_LEVEL, Math.max(MIN_ZOOM_LEVEL, value))
}

function applyZoomLevel(value) {
  const safeValue = clampZoomLevel(value)
  zoomLevel.value = safeValue

  const scale = 1 + safeValue * 0.1
  document.documentElement.style.setProperty('--hk-font-scale', String(scale))
  sessionStorage.setItem(STORAGE_KEY, String(safeValue))
}

function loadZoomLevel() {
  const savedValue = Number(sessionStorage.getItem(STORAGE_KEY))

  if (Number.isNaN(savedValue)) {
    applyZoomLevel(DEFAULT_ZOOM_LEVEL)
    return
  }

  applyZoomLevel(savedValue)
}

export function useTextResize() {
  const zoomPercent = computed(() => 100 + zoomLevel.value * 10)

  const canZoomIn = computed(() => zoomLevel.value < MAX_ZOOM_LEVEL)
  const canZoomOut = computed(() => zoomLevel.value > MIN_ZOOM_LEVEL)

  function zoomIn() {
    applyZoomLevel(zoomLevel.value + 1)
  }

  function zoomOut() {
    applyZoomLevel(zoomLevel.value - 1)
  }

  function resetZoom() {
    applyZoomLevel(DEFAULT_ZOOM_LEVEL)
    sessionStorage.removeItem(STORAGE_KEY)
  }

  onMounted(() => {
    loadZoomLevel()
  })

  return {
    zoomLevel,
    zoomPercent,
    canZoomIn,
    canZoomOut,
    zoomIn,
    zoomOut,
    resetZoom,
  }
}