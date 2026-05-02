import { provide, inject, ref, watch } from "vue"

export const KIDS_THEME_KEY = Symbol("kidsTheme")
const STORAGE_KEY = "kids-dashboard-theme"

/** Shared across all kid-facing pages — matches KidsDashboardPage storage key. */
let hydratedOnce = false
const isDarkMode = ref(false)

function hydrate() {
  if (typeof window === "undefined") return
  const saved = window.localStorage.getItem(STORAGE_KEY)
  if (saved === "dark" || saved === "light") {
    isDarkMode.value = saved === "dark"
    hydratedOnce = true
    return
  }
  isDarkMode.value = window.matchMedia("(prefers-color-scheme: dark)").matches
  hydratedOnce = true
}

watch(isDarkMode, value => {
  if (typeof window === "undefined") return
  window.localStorage.setItem(STORAGE_KEY, value ? "dark" : "light")
})

export function useKidsTheme() {
  if (typeof window !== "undefined" && !hydratedOnce) {
    hydrate()
  }

  function toggleDarkMode() {
    isDarkMode.value = !isDarkMode.value
  }

  return {
    isDarkMode,
    toggleDarkMode,
  }
}

/** Call from shell layout so children can inject the same refs. */
export function provideKidsTheme() {
  const theme = useKidsTheme()
  provide(KIDS_THEME_KEY, theme)
  return theme
}

export function injectKidsTheme() {
  const injected = inject(KIDS_THEME_KEY, null)
  if (injected) return injected
  return useKidsTheme()
}
