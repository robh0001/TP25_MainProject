<template>
  <div
    class="kids-dashboard-page"
    :class="{ 'kids-dashboard-dark-mode': isDarkMode, 'kids-dashboard-page--lite': motionLite }"
    aria-label="Kids dashboard with games, meal tracking, and hydration tracker"
  >
    <div id="confetti-layer" ref="confettiLayer"></div>

    <div class="kids-dashboard-kids-sky" aria-hidden="true">
      <div class="kids-dashboard-sky-gradient"></div>
      <div class="kids-dashboard-sky-aurora"></div>

      <div class="kids-dashboard-celestial kids-dashboard-sun-body">
        <div class="kids-dashboard-sun-core"></div>
        <div class="kids-dashboard-sun-halo"></div>
        <div class="kids-dashboard-sun-ring"></div>
      </div>

      <div class="kids-dashboard-celestial kids-dashboard-moon-body">
        <div class="kids-dashboard-moon-core">
          <span class="kids-dashboard-crater kids-dashboard-crater-1"></span>
          <span class="kids-dashboard-crater kids-dashboard-crater-2"></span>
          <span class="kids-dashboard-crater kids-dashboard-crater-3"></span>
        </div>
        <div class="kids-dashboard-moon-halo"></div>
      </div>

      <div class="kids-dashboard-sky-stars">
        <span
          v-for="star in skyStars"
          :key="`sky-star-${star.id}`"
          class="kids-dashboard-sky-star"
          :style="{
            left: `${star.left}%`,
            top: `${star.top}%`,
            width: `${star.size}px`,
            height: `${star.size}px`,
            animationDelay: `${star.delay}s`,
            animationDuration: `${star.duration}s`,
          }"
        ></span>
        <span
          v-for="shoot in shootingStars"
          :key="`sky-shoot-${shoot.id}`"
          class="kids-dashboard-sky-shoot"
          :style="{ left: `${shoot.left}%`, top: `${shoot.top}%`, animationDelay: `${shoot.delay}s` }"
        ></span>
      </div>

      <div class="kids-dashboard-sky-clouds">
        <span class="kids-dashboard-sky-cloud kids-dashboard-sky-cloud-1"></span>
        <span class="kids-dashboard-sky-cloud kids-dashboard-sky-cloud-2"></span>
        <span class="kids-dashboard-sky-cloud kids-dashboard-sky-cloud-3"></span>
        <span class="kids-dashboard-sky-cloud kids-dashboard-sky-cloud-4"></span>
      </div>

      <svg class="kids-dashboard-sky-hills" viewBox="0 0 1440 220" preserveAspectRatio="none">
        <path class="kids-dashboard-hill-back" d="M0,170 L160,120 L320,160 L520,90 L720,150 L920,100 L1140,160 L1300,120 L1440,150 L1440,220 L0,220 Z"/>
        <path class="kids-dashboard-hill-front" d="M0,220 L120,170 L300,210 L480,170 L660,205 L840,170 L1020,210 L1220,175 L1440,205 L1440,220 L0,220 Z"/>
      </svg>
    </div>

    <div class="kids-dashboard-dash-blobs" aria-hidden="true">
      <span class="kids-dashboard-blob kids-dashboard-blob-a"></span>
      <span class="kids-dashboard-blob kids-dashboard-blob-b"></span>
      <span class="kids-dashboard-blob kids-dashboard-blob-c"></span>
      <span class="kids-dashboard-blob kids-dashboard-blob-d"></span>
    </div>

    <div class="kids-dashboard-dash-sparkles" aria-hidden="true">
      <span class="kids-dashboard-spark kids-dashboard-spark-a">✨</span>
      <span class="kids-dashboard-spark kids-dashboard-spark-b">⭐</span>
      <span class="kids-dashboard-spark kids-dashboard-spark-c">💫</span>
      <span class="kids-dashboard-spark kids-dashboard-spark-d">✨</span>
    </div>

    <div class="kids-dashboard-water-fall-layer">
      <span
        v-for="drop in fallingDrops"
        :key="drop.id"
        class="kids-dashboard-fall-drop"
        :style="{
          left: `${drop.left}%`,
          animationDelay: `${drop.delay}ms`,
          animationDuration: `${drop.duration}ms`,
          '--drop-size': `${drop.size}px`,
          '--drop-drift': `${drop.drift}px`,
        }"
      ></span>
    </div>

    <div class="kids-dashboard-dash">
      <header class="kids-dashboard-header">
        <div class="kids-dashboard-avatar-zone">
          <div class="kids-dashboard-avatar">
            <span class="kids-dashboard-svg-holder kids-dashboard-avatar-svg" v-html="icons.avatar"></span>
          </div>
          <div class="kids-dashboard-orbit-ring"><div class="kids-dashboard-orbit-dot"></div></div>
        </div>

        <div class="kids-dashboard-header-text">
          <h1 data-hover-read-text aria-label="Hey there! Ready to play?">Hey there! Ready to play?</h1>
          <div class="kids-dashboard-header-sub" data-hover-read-text aria-label="Pick a game, collect healthy wins and keep your streak!">Pick a game, collect healthy wins &amp; keep your streak!</div>
        </div>

        <div class="kids-dashboard-header-right">
          <RouterLink to="/parent-dashboard" class="kids-dashboard-main-site-link">
            <span class="kids-dashboard-svg-holder kids-dashboard-mini-svg" v-html="icons.home"></span>
            Parents dashboard
          </RouterLink>
          <div class="kids-dashboard-date-tag">
            <span class="kids-dashboard-svg-holder kids-dashboard-mini-svg" v-html="icons.calendar"></span>
            {{ todayLabel }}
          </div>
          <div class="kids-dashboard-time-tag">
            <span class="kids-dashboard-svg-holder kids-dashboard-mini-svg" v-html="icons.clock"></span>
            {{ liveTime }}
          </div>
          <button type="button" class="kids-dashboard-streak-tag" aria-label="Celebrate your streak" data-hover-read-text @click="celebrateStreak">
            <span class="kids-dashboard-svg-holder kids-dashboard-mini-svg kids-dashboard-flame-icon" v-html="icons.flame"></span>
          </button>
        </div>
      </header>

      <section class="kids-dashboard-meal-day-panel" aria-labelledby="kids-dashboard-meal-day-title">
        <header class="kids-dashboard-meal-day-head">
          <div class="kids-dashboard-meal-day-heading">
            <span class="kids-dashboard-svg-holder kids-dashboard-meal-day-svg" aria-hidden="true" v-html="icons.sun"></span>
            <div>
              <h2 id="kids-dashboard-meal-day-title" class="kids-dashboard-meal-day-title" data-hover-read-text aria-label="Today's meals">Today's meals</h2>
              <p class="kids-dashboard-meal-day-sub" data-hover-read-text aria-label="Tap when you eat. We save it for today.">Tap when you eat — we save it for today</p>
            </div>
          </div>
        </header>

        <div class="kids-dashboard-boost-strip" role="group" aria-label="Breakfast, lunch, and dinner">
          <article
            v-for="check in mealChecks"
            :key="check.label"
            class="kids-dashboard-boost-pill"
            :class="[check.tone, { 'kids-dashboard-boost-pill--done': check.done }]"
            :aria-label="`${check.label}. ${check.helper}. ${check.actionLabel}`"
            data-hover-read-text
            @click="toggleMealCheck(check.label, $event)"
          >
            <div class="kids-dashboard-boost-icon">
              <span class="kids-dashboard-meal-check-emoji" aria-hidden="true">{{ check.emoji }}</span>
            </div>
            <div class="kids-dashboard-boost-copy">
              <div class="kids-dashboard-boost-label">{{ check.label }}</div>
              <div class="kids-dashboard-boost-sub">{{ check.helper }}</div>
            </div>
            <span class="kids-dashboard-boost-action">{{ check.actionLabel }}</span>
          </article>
        </div>
      </section>

      <div class="kids-dashboard-main-grid">
        <section class="kids-dashboard-games-tiles" aria-label="Pick a game">
          <div class="kids-dashboard-section-label">
            <span class="kids-dashboard-svg-holder kids-dashboard-section-svg" v-html="icons.target"></span>
            Games
          </div>

          <div class="kids-dashboard-game-tile-grid">
            <button
              v-for="tile in gameTiles"
              :key="tile.id"
              type="button"
              class="kids-dashboard-game-tile"
              :class="tile.tone"
              :aria-label="`${tile.title}. ${tile.short}`"
              data-hover-read-text
              @click="launchTile(tile.launchKey)"
            >
              <span class="kids-dashboard-game-tile-emoji" aria-hidden="true">{{ tile.emoji }}</span>
              <div class="kids-dashboard-game-tile-copy">
                <strong>{{ tile.title }}</strong>
                <span>{{ tile.short }}</span>
              </div>
              <span class="kids-dashboard-game-tile-arrow" aria-hidden="true">→</span>
            </button>
          </div>
        </section>

        <div ref="hydrationCard" class="kids-dashboard-hydration-card">
          <div class="kids-dashboard-hyd-ring"></div>
          <div class="kids-dashboard-hyd-ring"></div>

          <div class="kids-dashboard-hyd-header">
            <div class="kids-dashboard-section-label kids-dashboard-section-green">
              <span class="kids-dashboard-svg-holder kids-dashboard-section-svg" v-html="icons.drop"></span>
              Hydration Tracker
            </div>
            <div class="kids-dashboard-sip-counter" aria-live="polite" :title="`Glasses logged today`">
              <span class="kids-dashboard-sip-counter-emoji" aria-hidden="true">🥛</span>
              <span class="kids-dashboard-sip-counter-num">{{ glassCount }}</span>
            </div>
          </div>
          <div class="kids-dashboard-hydration-title" data-hover-read-text aria-label="Stay super hydrated!">Stay super hydrated!</div>
          <div class="kids-dashboard-hydration-sub" data-hover-read-text aria-label="Tap a drop to log your glass">Tap a drop to log your glass</div>

          <div class="kids-dashboard-drop-grid">
            <button
              v-for="(filled, index) in hydrationDrops"
              :key="`drop-${index}`"
              type="button"
              class="kids-dashboard-drop-btn"
              :class="{ 'kids-dashboard-filled': filled }"
              :title="`Sip ${index + 1}`"
              :aria-pressed="filled"
              :aria-label="filled ? `Water glass ${index + 1} logged` : `Log water glass ${index + 1}`"
              data-hover-read-text
              @click.stop="toggleDrop(index, $event)"
            >
              <span v-if="filled" class="kids-dashboard-drop-emoji" aria-hidden="true">💧</span>
              <span v-else class="kids-dashboard-svg-holder kids-dashboard-drop-svg" v-html="icons.drop"></span>
            </button>
          </div>

          <div class="kids-dashboard-hyd-actions">
            <button type="button" class="kids-dashboard-log-sip-btn" aria-label="Log another glass of water" data-hover-read-text @click.stop="logGlass">
              <span class="kids-dashboard-svg-holder kids-dashboard-button-svg" v-html="icons.plusCircle"></span>
              Log another glass
            </button>
            <button
              type="button"
              class="kids-dashboard-reset-glass-btn"
              aria-label="Reset water glasses"
              data-hover-read-text
              :disabled="glassCount === 0"
              @click.stop="resetGlasses"
            >
              Reset
            </button>
          </div>
        </div>
      </div>
    </div>

    <transition name="kids-dashboard-meal-toast">
      <div v-if="mealToast" class="kids-dashboard-meal-toast" role="status" aria-live="polite">
        {{ mealToast }}
      </div>
    </transition>

    <transition name="kids-dashboard-launch-screen">
      <div
        v-if="launching"
        class="kids-dashboard-launch-screen"
        :class="launchToneClass"
        role="status"
        aria-live="polite"
      >
        <div class="kids-dashboard-launch-card">
          <div class="kids-dashboard-launch-icon-wrap" aria-hidden="true">
            <span class="kids-dashboard-launch-emoji">{{ launchEmoji }}</span>
          </div>
          <div class="kids-dashboard-launch-title">{{ launchTitle }}</div>
          <div class="kids-dashboard-launch-sub">{{ launchSub }}</div>
          <div class="kids-dashboard-launch-loader" aria-hidden="true">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>
    </transition>

    <KidsBottomNav />

    <KidsThemeFloater :is-dark-mode="isDarkMode" @toggle-theme="toggleDarkMode" />
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue"
import { RouterLink } from "vue-router"
import KidsBottomNav from "./kids/KidsBottomNav.vue"
import KidsThemeFloater from "./kids/KidsThemeFloater.vue"
import { useKidsTheme } from "../composables/useKidsTheme.js"
import { useKidsProgressStore } from "../stores/kidsProgressStore.js"
import { useGameLaunch } from "../composables/useGameLaunch.js"
import { useKidsPerf } from "../composables/useKidsPerf.js"

const { isDarkMode, toggleDarkMode } = useKidsTheme()
const kp = useKidsProgressStore()
const { motionLite, syncKidsPerf, fx } = useKidsPerf()
const {
  launching,
  launchTitle,
  launchSub,
  launchEmoji,
  launchTone,
  startGameLaunch,
} = useGameLaunch()

const launchToneClass = computed(() => (launchTone.value ? `kids-dashboard-${launchTone.value}` : ""))

const confettiLayer = ref(null)
const hydrationCard = ref(null)
const fallingDrops = ref([])
const mealToast = ref("")
const liveTime = ref("")

const skyStars = ref([])
const shootingStars = ref([])

let nextFallingDropId = 1
const activeRibbons = []

let ribbonFrameId = 0
let mealToastTimer = 0
let liveTimeTimer = 0
let motionMediaListener = null
let visibilityListener = null

function buildAmbientStars(count) {
  return Array.from({ length: count }, (_, id) => ({
    id,
    left: Math.random() * 100,
    top: Math.random() * 70,
    size: 1 + Math.random() * 2.4,
    delay: Math.random() * 4,
    duration: 1.8 + Math.random() * 3.4,
  }))
}

function buildShootingStars(count) {
  return Array.from({ length: count }, (_, id) => ({
    id,
    left: 12 + Math.random() * 70,
    top: 8 + Math.random() * 40,
    delay: id * 6 + Math.random() * 4,
  }))
}

function initAmbientLayers() {
  syncKidsPerf()
  if (motionLite.value) {
    skyStars.value = []
    shootingStars.value = []
    return
  }

  const coarsePointer =
    typeof window !== "undefined" && window.matchMedia("(pointer: coarse)").matches
  const starCount = coarsePointer ? 18 : 30
  skyStars.value = buildAmbientStars(starCount)
  shootingStars.value = buildShootingStars(2)
}

function startLiveClock() {
  if (liveTimeTimer || typeof window === "undefined") return
  liveTimeTimer = window.setInterval(updateLiveTime, 1000)
}

function stopLiveClock() {
  if (!liveTimeTimer) return
  window.clearInterval(liveTimeTimer)
  liveTimeTimer = 0
}

function onVisibilityChange() {
  if (typeof document === "undefined") return
  if (document.hidden) {
    stopLiveClock()
    return
  }
  updateLiveTime()
  startLiveClock()
}

onMounted(() => {
  syncKidsPerf()
  initAmbientLayers()

  if (typeof window !== "undefined") {
    motionMediaListener = () => {
      syncKidsPerf()
      initAmbientLayers()
    }
    window.matchMedia("(prefers-reduced-motion: reduce)").addEventListener("change", motionMediaListener)
    navigator.connection?.addEventListener?.("change", motionMediaListener)

    visibilityListener = onVisibilityChange
    document.addEventListener("visibilitychange", visibilityListener)
  }

  kp.hydrate()
  updateLiveTime()
  startLiveClock()
})

const todayLabel = new Intl.DateTimeFormat("en-AU", {
  weekday: "short",
  day: "numeric",
  month: "short",
}).format(new Date())

function updateLiveTime() {
  liveTime.value = new Intl.DateTimeFormat("en-AU", {
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit",
  }).format(new Date())
}

const icons = {
  avatar: `<svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="32" cy="32" r="30" fill="#FFE8B8"/><path d="M19 25C19 17.8203 24.8203 12 32 12C39.1797 12 45 17.8203 45 25V28H19V25Z" fill="#D97A00"/><circle cx="32" cy="28" r="12" fill="#FFD7B3"/><path d="M25 27C26.3333 25.4 28.4 24.6 31.2 24.6C34 24.6 36.2667 25.4 38 27" stroke="#7A3E00" stroke-width="2.8" stroke-linecap="round"/><circle cx="27.5" cy="29.5" r="1.6" fill="#7A3E00"/><circle cx="36.5" cy="29.5" r="1.6" fill="#7A3E00"/><path d="M28 34.5C29.1 36.1667 30.4333 37 32 37C33.5667 37 34.9 36.1667 36 34.5" stroke="#7A3E00" stroke-width="2.6" stroke-linecap="round"/><path d="M18 52C18.8 44.5333 23.4667 40.8 32 40.8C40.5333 40.8 45.2 44.5333 46 52" fill="#5B7CFA"/><path d="M18 52C18.8 44.5333 23.4667 40.8 32 40.8C40.5333 40.8 45.2 44.5333 46 52" stroke="#3B56D9" stroke-width="2.4" stroke-linecap="round"/><path d="M32 41V52" stroke="#D8E4FF" stroke-width="2.4" stroke-linecap="round"/><circle cx="32" cy="46" r="2.1" fill="#D8E4FF"/></svg>`,
  calendar: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>`,
  flame: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c0 4-4 6-4 10a4 4 0 0 0 8 0c0-4-4-6-4-10z"/><path d="M12 12c0 2-2 3-2 5a2 2 0 0 0 4 0c0-2-2-3-2-5z"/></svg>`,
  target: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`,
  bubbleMission: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2"/></svg>`,
  play: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>`,
  arrowRight: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`,
  drop: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L5 12a7 7 0 1 0 14 0L12 2z"/></svg>`,
  plusCircle: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>`,
  clock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>`,
  home: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.8V21h14V9.8"/><path d="M9 21v-6h6v6"/></svg>`,
  moon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>`,
  sun: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2.2M12 19.8V22M4.9 4.9l1.5 1.5M17.6 17.6l1.5 1.5M2 12h2.2M19.8 12H22M4.9 19.1l1.5-1.5M17.6 6.4l1.5-1.5"/></svg>`,
  bolt: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
  message: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`,
}

const gameTiles = [
  {
    id: "bubble",
    launchKey: "bubble",
    title: "Bubble Game",
    short: "Pop healthy words fast",
    emoji: "🫧",
    tone: "kids-dashboard-tile-bubble",
  },
  {
    id: "explorer",
    launchKey: "explorer",
    title: "Explorer Game",
    short: "Match bright healthy pairs",
    emoji: "🧭",
    tone: "kids-dashboard-tile-explorer",
  },
  {
    id: "humit",
    launchKey: "humit",
    title: "Hum It!",
    short: "Your hum powers your creature",
    emoji: "🎵",
    tone: "kids-dashboard-tile-humit",
  },
  {
    id: "smash",
    launchKey: "smash",
    title: "Routine Rumble",
    short: "Smash healthy routines",
    emoji: "🎈",
    tone: "kids-dashboard-tile-smash",
  },
]

const mealChecks = computed(() => [
  {
    label: "Breakfast",
    helper: kp.daily.meals.Breakfast ? "Saved for today" : "Not logged yet",
    actionLabel: kp.daily.meals.Breakfast ? "Undo" : "Add",
    emoji: "🍳",
    tone: "kids-dashboard-boost-coral",
    done: Boolean(kp.daily.meals.Breakfast),
  },
  {
    label: "Lunch",
    helper: kp.daily.meals.Lunch ? "Saved for today" : "Not logged yet",
    actionLabel: kp.daily.meals.Lunch ? "Undo" : "Add",
    emoji: "🥪",
    tone: "kids-dashboard-boost-sky",
    done: Boolean(kp.daily.meals.Lunch),
  },
  {
    label: "Dinner",
    helper: kp.daily.meals.Dinner ? "Saved for today" : "Not logged yet",
    actionLabel: kp.daily.meals.Dinner ? "Undo" : "Add",
    emoji: "🍽️",
    tone: "kids-dashboard-boost-violet",
    done: Boolean(kp.daily.meals.Dinner),
  },
])

const GLASS_GOAL = 8
const GLASS_MAX = 50

const hydrationDrops = computed(() =>
  Array.from({ length: GLASS_GOAL }, (_, index) => index < Math.min(GLASS_GOAL, kp.daily.waterGlasses)),
)

const glassCount = computed(() => Math.max(0, Math.min(GLASS_MAX, kp.daily.waterGlasses)))

function ripple(event) {
  const el = event.currentTarget
  if (!(el instanceof HTMLElement)) return
  const rippleEl = document.createElement("div")
  rippleEl.className = "kids-dashboard-rip"
  const rect = el.getBoundingClientRect()
  const size = Math.max(rect.width, rect.height)
  rippleEl.style.width = `${size}px`
  rippleEl.style.height = `${size}px`
  rippleEl.style.left = `${event.clientX - rect.left - size / 2}px`
  rippleEl.style.top = `${event.clientY - rect.top - size / 2}px`
  el.appendChild(rippleEl)
  window.setTimeout(() => rippleEl.remove(), 700)
}

function spawnConfetti(count, originRect) {
  const n = fx(count)
  if (n < 1) return
  const layer = confettiLayer.value
  if (!layer) return

  const colors = ["#FF6058", "#3B9EFF", "#2CC97A", "#FFB020", "#9B72FF", "#FF7EB3", "#1EC8C8", "#FFDD57"]

  for (let index = 0; index < n; index += 1) {
    const piece = document.createElement("div")
    piece.className = "kids-dashboard-conf-piece"
    const duration = originRect ? 0.7 + Math.random() * 0.6 : 1.4 + Math.random() * 1.4
    const left = originRect
      ? ((originRect.left + originRect.width / 2) / window.innerWidth) * 100 + (-10 + Math.random() * 20)
      : Math.random() * 100
    const top = originRect ? (originRect.top / window.innerHeight) * 100 : 0

    piece.style.left = `${left}%`
    piece.style.top = `${top}%`
    piece.style.width = `${(originRect ? 5 : 6) + Math.random() * (originRect ? 5 : 8)}px`
    piece.style.height = `${(originRect ? 5 : 6) + Math.random() * (originRect ? 5 : 8)}px`
    piece.style.background = colors[Math.floor(Math.random() * colors.length)]
    piece.style.borderRadius = originRect || Math.random() > 0.5 ? "50%" : "2px"
    piece.style.animationDuration = `${duration}s`
    piece.style.animationDelay = originRect ? "0s" : `${Math.random() * 0.5}s`
    piece.style.position = "absolute"
    piece.style.pointerEvents = "none"

    layer.appendChild(piece)
    window.setTimeout(() => piece.remove(), (duration + 0.8) * 1000)
  }
}

function randomBetween(min, max) {
  return min + Math.random() * (max - min)
}

function startRibbonSimulation() {
  if (ribbonFrameId || !confettiLayer.value) return

  let lastTime = performance.now()

  const tick = now => {
    const deltaSeconds = Math.min((now - lastTime) / 1000, 0.032)
    lastTime = now

    for (let index = activeRibbons.length - 1; index >= 0; index -= 1) {
      const ribbon = activeRibbons[index]

      if (!ribbon.isActive) {
        if (now >= ribbon.startAt) {
          ribbon.isActive = true
          ribbon.element.style.opacity = "1"
        } else {
          continue
        }
      }

      ribbon.age += deltaSeconds
      ribbon.vy += ribbon.gravity * deltaSeconds
      ribbon.x += ribbon.vx * deltaSeconds
      ribbon.y += ribbon.vy * deltaSeconds
      ribbon.rotationZ += ribbon.spin * deltaSeconds

      const sway = Math.sin(ribbon.age * ribbon.swayFrequency + ribbon.phase) * ribbon.swayAmplitude
      const twistX = Math.sin(ribbon.age * ribbon.flutterSpeed + ribbon.phase) * ribbon.flutterX
      const twistY = Math.cos(ribbon.age * ribbon.flutterSpeed * 0.78 + ribbon.phase) * ribbon.flutterY
      const entry = Math.min(1, Math.max(0, (ribbon.y + ribbon.height) / 120))
      const fade = ribbon.y > ribbon.fadeStart
        ? Math.max(0, 1 - (ribbon.y - ribbon.fadeStart) / (ribbon.maxY - ribbon.fadeStart))
        : 1
      const opacity = entry * fade
      const stretch = 0.96 + Math.min(0.18, ribbon.vy / 1500)
      const depth = 0.9 + Math.sin(ribbon.age * 2.8 + ribbon.phase) * 0.08

      ribbon.element.style.opacity = `${opacity}`
      ribbon.element.style.transform = `translate3d(${ribbon.x + sway}px, ${ribbon.y}px, 0) scale(${depth}, ${stretch}) rotateX(${twistX}deg) rotateY(${twistY}deg) rotateZ(${ribbon.rotationZ}deg)`

      if (ribbon.y > ribbon.maxY || opacity <= 0) {
        ribbon.element.remove()
        activeRibbons.splice(index, 1)
      }
    }

    if (activeRibbons.length > 0) {
      ribbonFrameId = window.requestAnimationFrame(tick)
    } else {
      ribbonFrameId = 0
    }
  }

  ribbonFrameId = window.requestAnimationFrame(tick)
}

function spawnRibbonRain(count, options = {}) {
  const total = fx(count)
  if (total < 1) return

  const layer = confettiLayer.value
  if (!layer) return

  const width = window.innerWidth
  const height = window.innerHeight
  const now = performance.now()

  const centerX = width / 2
  const spread = Math.min(width * 0.55, 620)

  const palette = [
    ["#FF7A72", "#FFB96B"],
    ["#51B7FF", "#7CF1FF"],
    ["#8E7CFF", "#D4A8FF"],
    ["#54E69F", "#A8FFD4"],
    ["#FF8BC2", "#FFD36F"],
  ]

  for (let index = 0; index < total; index += 1) {
    const ribbon = document.createElement("div")
    ribbon.className = "kids-dashboard-cele-ribbon"

    const [colorStart, colorEnd] = palette[index % palette.length]
    const ribbonWidth = randomBetween(16, 26)
    const ribbonHeight = randomBetween(150, 260)

    const startX = Math.max(
      24,
      Math.min(width - 48, centerX - spread / 2 + Math.random() * spread)
    )

    ribbon.style.position = "absolute"
    ribbon.style.left = `${startX}px`
    ribbon.style.top = `${randomBetween(-height * 0.35, -ribbonHeight - 60)}px`
    ribbon.style.width = `${ribbonWidth}px`
    ribbon.style.height = `${ribbonHeight}px`
    ribbon.style.pointerEvents = "none"
    ribbon.style.setProperty("--ribbon-start", colorStart)
    ribbon.style.setProperty("--ribbon-end", colorEnd)
    ribbon.style.opacity = "0"

    layer.appendChild(ribbon)

    activeRibbons.push({
      element: ribbon,
      x: 0,
      y: 0,
      vx: randomBetween(-36, 36),
      vy: randomBetween(210, 300),
      gravity: randomBetween(330, 470),
      rotationZ: randomBetween(-30, 30),
      spin: randomBetween(-110, 110),
      swayAmplitude: randomBetween(18, 42),
      swayFrequency: randomBetween(1.8, 3.4),
      flutterX: randomBetween(32, 76),
      flutterY: randomBetween(48, 110),
      flutterSpeed: randomBetween(6.2, 9.4),
      phase: randomBetween(0, Math.PI * 2),
      fadeStart: height * randomBetween(0.82, 0.94),
      maxY: height + 260,
      height: ribbonHeight,
      age: 0,
      startAt: now + index * randomBetween(18, 38),
      isActive: false,
    })
  }

  startRibbonSimulation()
}

function launchRibbonCelebration(count) {
  if (fx(count) < 1) return

  const centerRect = {
    left: window.innerWidth / 2 - 40,
    top: window.innerHeight / 2 - 40,
    width: 80,
    height: 80,
  }

  spawnConfetti(Math.max(14, Math.round(count * 0.28)), centerRect)
  spawnRibbonRain(count, { originRect: centerRect })
}

function fireConfetti() {
  spawnConfetti(26)
}

function celebrateStreak(event) {
  ripple(event)

  const centerRect = {
    left: window.innerWidth / 2 - 40,
    top: window.innerHeight / 2 - 40,
    width: 80,
    height: 80,
  }

  spawnConfetti(44, centerRect)
  launchRibbonCelebration(28)
}

function miniConfetti(element) {
  if (!(element instanceof HTMLElement)) return
  spawnConfetti(12, element.getBoundingClientRect())
}

function spawnWaterDrops(sourceElement, count = 16) {
  const n = fx(count)
  if (n < 1) return

  const origin = sourceElement instanceof HTMLElement ? sourceElement : hydrationCard.value
  const rect = origin?.getBoundingClientRect?.()
  if (!rect) return

  const created = Array.from({ length: n }, (_, index) => ({
    id: nextFallingDropId++,
    left: ((rect.left + Math.random() * rect.width) / window.innerWidth) * 100,
    delay: index * 55 + Math.random() * 120,
    duration: 950 + Math.random() * 650,
    size: 10 + Math.random() * 14,
    drift: -26 + Math.random() * 52,
  }))

  fallingDrops.value.push(...created)

  const maxLifetime = Math.max(...created.map(drop => drop.delay + drop.duration)) + 200
  window.setTimeout(() => {
    const createdIds = new Set(created.map(drop => drop.id))
    fallingDrops.value = fallingDrops.value.filter(drop => !createdIds.has(drop.id))
  }, maxLifetime)
}

function toggleMealCheck(label, event) {
  const wasDone = Boolean(kp.daily.meals[label])
  kp.toggleMeal(label)
  if (!wasDone) {
    miniConfetti(event.currentTarget)
    showMealToast(`Great! ${label} added`)
    return
  }
  showMealToast(`${label} removed`)
}

function showMealToast(message) {
  mealToast.value = message
  if (mealToastTimer) {
    window.clearTimeout(mealToastTimer)
  }
  mealToastTimer = window.setTimeout(() => {
    mealToast.value = ""
    mealToastTimer = 0
  }, 1400)
}

function toggleDrop(index, event) {
  const currentCount = Math.min(GLASS_GOAL, kp.daily.waterGlasses)
  const nextCount = index < currentCount ? index : index + 1
  if (nextCount === currentCount) return
  kp.addWater(nextCount - currentCount)
  if (nextCount > currentCount) {
    spawnWaterDrops(hydrationCard.value, 12)
    miniConfetti(event.currentTarget)
  }
}

function logGlass(event) {
  if (kp.daily.waterGlasses >= GLASS_MAX) {
    showMealToast(`Max ${GLASS_MAX} glasses reached`)
    return
  }
  kp.addWater(1)
  spawnWaterDrops(hydrationCard.value, 15)
  miniConfetti(event.currentTarget)
  const next = Math.min(GLASS_MAX, kp.daily.waterGlasses)
  if (next > GLASS_GOAL) {
    showMealToast(`Bonus glass! ${next} logged`)
  } else {
    showMealToast(`Great! ${next} / ${GLASS_GOAL} glasses`)
  }
}

function resetGlasses() {
  const current = kp.daily.waterGlasses
  if (current <= 0) return
  kp.addWater(-current)
  showMealToast("Glasses reset")
}

function launchTile(launchKey) {
  fireConfetti()
  startGameLaunch(launchKey)
}

onBeforeUnmount(() => {
  stopLiveClock()

  if (typeof window !== "undefined" && motionMediaListener) {
    window.matchMedia("(prefers-reduced-motion: reduce)").removeEventListener("change", motionMediaListener)
    navigator.connection?.removeEventListener?.("change", motionMediaListener)
    motionMediaListener = null
  }

  if (typeof document !== "undefined" && visibilityListener) {
    document.removeEventListener("visibilitychange", visibilityListener)
    visibilityListener = null
  }

  if (ribbonFrameId) {
    window.cancelAnimationFrame(ribbonFrameId)
    ribbonFrameId = 0
  }

  if (mealToastTimer) {
    window.clearTimeout(mealToastTimer)
    mealToastTimer = 0
  }

  for (const ribbon of activeRibbons) {
    ribbon.element.remove()
  }

  activeRibbons.length = 0
})
</script>