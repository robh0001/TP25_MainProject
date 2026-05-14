import { computed, ref } from 'vue'

const STORAGE_KEY = 'hk-text-zoom-level'

const MIN_ZOOM_LEVEL = -2
const MAX_ZOOM_LEVEL = 5
const DEFAULT_ZOOM_LEVEL = 0

const zoomLevel = ref(DEFAULT_ZOOM_LEVEL)
let hasLoadedInitialZoom = false

function clampZoomLevel(value) {
  return Math.min(MAX_ZOOM_LEVEL, Math.max(MIN_ZOOM_LEVEL, value))
}

function getScaleFromZoomLevel(value) {
  return 1 + value * 0.1
}

function applyZoomLevel(value, options = {}) {
  const safeValue = clampZoomLevel(value)

  zoomLevel.value = safeValue

  const scale = getScaleFromZoomLevel(safeValue)

  if (typeof document !== 'undefined') {
    document.documentElement.style.setProperty('--hk-font-scale', String(scale))
  }

  if (typeof sessionStorage !== 'undefined') {
    if (options.clearStorage) {
      sessionStorage.removeItem(STORAGE_KEY)
    } else {
      sessionStorage.setItem(STORAGE_KEY, String(safeValue))
    }
  }
}

function loadStoredZoomLevel() {
  if (hasLoadedInitialZoom) return

  hasLoadedInitialZoom = true

  if (typeof sessionStorage === 'undefined') {
    applyZoomLevel(DEFAULT_ZOOM_LEVEL)
    return
  }

  const storedValue = sessionStorage.getItem(STORAGE_KEY)

  if (storedValue === null) {
    applyZoomLevel(DEFAULT_ZOOM_LEVEL, { clearStorage: true })
    return
  }

  const parsedValue = Number(storedValue)

  if (Number.isNaN(parsedValue)) {
    applyZoomLevel(DEFAULT_ZOOM_LEVEL, { clearStorage: true })
    return
  }

  applyZoomLevel(parsedValue)
}

loadStoredZoomLevel()

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
    applyZoomLevel(DEFAULT_ZOOM_LEVEL, { clearStorage: true })
  }

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