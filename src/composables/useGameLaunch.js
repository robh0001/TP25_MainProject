import { ref } from "vue"
import { useRouter } from "vue-router"

const launching = ref(false)
const launchTitle = ref("Opening...")
const launchSub = ref("Get ready to play")
const launchEmoji = ref("🎮")
const launchTone = ref("default")

let launchTimer = 0

const DEFAULT_LAUNCH_DURATION_MS = 1600
const GAMES_TAB_LAUNCH_DURATION_MS = 2000

const presets = {
  bubble: {
    title: "Opening Bubble Game...",
    sub: "Get ready to pop those healthy words!",
    emoji: "🫧",
    tone: "tone-bubble",
    path: "/kids-game-zone",
    query: { game: "bubble" },
    durationMs: DEFAULT_LAUNCH_DURATION_MS,
  },
  explorer: {
    title: "Opening Explorer Game...",
    sub: "Match those healthy combos!",
    emoji: "🧭",
    tone: "tone-explorer",
    path: "/kids-game-zone",
    query: { game: "explorer" },
    durationMs: DEFAULT_LAUNCH_DURATION_MS,
  },
  smash: {
    title: "Opening Routine Game...",
    sub: "Time to smash some healthy habits!",
    emoji: "🎈",
    tone: "tone-smash",
    path: "/kids-game-zone",
    query: { game: "smash" },
    durationMs: DEFAULT_LAUNCH_DURATION_MS,
  },
  humit: {
    title: "Hum It! loading…",
    sub: "Warm up your humming voice!",
    emoji: "🎵",
    tone: "tone-humit",
    path: "/kids-game-zone",
    query: { game: "humit" },
    durationMs: DEFAULT_LAUNCH_DURATION_MS,
  },
  games: {
    title: "Opening Games...",
    sub: "Are you excited?!",
    emoji: "🎮",
    tone: "tone-games",
    path: "/kids-game-zone",
    query: {},
    durationMs: GAMES_TAB_LAUNCH_DURATION_MS,
  },
}

export function useGameLaunch() {
  const router = useRouter()

  function startGameLaunch(key = "games", overrides = {}) {
    if (launching.value) return

    const preset = presets[key] || presets.games

    launchTitle.value = overrides.title ?? preset.title
    launchSub.value = overrides.sub ?? preset.sub
    launchEmoji.value = overrides.emoji ?? preset.emoji
    launchTone.value = overrides.tone ?? preset.tone

    const targetPath = overrides.path ?? preset.path
    const targetQuery = overrides.query ?? preset.query
    const durationMs = overrides.durationMs ?? preset.durationMs ?? DEFAULT_LAUNCH_DURATION_MS

    launching.value = true
    if (launchTimer) {
      window.clearTimeout(launchTimer)
    }
    launchTimer = window.setTimeout(() => {
      launching.value = false
      launchTimer = 0
      router.push({ path: targetPath, query: targetQuery })
    }, durationMs)
  }

  function cancelGameLaunch() {
    if (launchTimer) {
      window.clearTimeout(launchTimer)
      launchTimer = 0
    }
    launching.value = false
  }

  return {
    launching,
    launchTitle,
    launchSub,
    launchEmoji,
    launchTone,
    startGameLaunch,
    cancelGameLaunch,
    DEFAULT_LAUNCH_DURATION_MS,
    GAMES_TAB_LAUNCH_DURATION_MS,
  }
}
