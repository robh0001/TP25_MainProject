import { ref } from "vue"

/**
 * Kids-area performance hints: honor reduced motion & Save-Data,
 * and scale decorative FX counts without touching functional UI.
 */
export function useKidsPerf() {
  const motionLite = ref(false)

  function syncKidsPerf() {
    if (typeof window === "undefined") return
    motionLite.value =
      window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
      Boolean(navigator.connection?.saveData)
  }


  function fx(count) {
    if (motionLite.value || count <= 0) return 0
    return Math.round(count)
  }

  return { motionLite, syncKidsPerf, fx }
}
