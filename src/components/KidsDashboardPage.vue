<!--
  KidsDashboardPage.vue

  Creates the HelthyKidz kids dashboard page. Children can open games, log meals,
  track water, switch between day and night themes, and see playful animations.

  Store and composable requirements:
  - Uses useKidsTheme for light and dark mode.
  - Uses useKidsProgressStore for saved kids progress, meals, and hydration.
  - Uses useGameLaunch for the animated game launch screen.
  - Uses useKidsPerf to reduce animation effects when needed.

  Accessibility:
  - Uses aria-hidden for decorative sky, blobs, sparkles, and icon-only visuals.
  - Uses aria-live for meal toast, launch screen, hydration count, and live status updates.
  - Uses buttons and RouterLink elements for keyboard-friendly interaction.
-->

<template>
  <div
    class="kids-html-dashboard"
    :class="{ 'dark-mode': isDarkMode, 'kids-html-dashboard--lite': motionLite }"
  >
    <!-- Confetti layer used for celebration effects -->
    <div id="confetti-layer" ref="confettiLayer"></div>

    <!-- Decorative animated sky background -->
    <div class="kids-sky" aria-hidden="true">
      <div class="sky-gradient"></div>
      <div class="sky-aurora"></div>

      <div class="celestial sun-body">
        <div class="sun-core"></div>
        <div class="sun-halo"></div>
        <div class="sun-ring"></div>
      </div>

      <div class="celestial moon-body">
        <div class="moon-core">
          <span class="crater crater-1"></span>
          <span class="crater crater-2"></span>
          <span class="crater crater-3"></span>
        </div>
        <div class="moon-halo"></div>
      </div>

      <!-- Night mode stars and shooting stars -->
      <div class="sky-stars">
        <span
          v-for="star in skyStars"
          :key="`sky-star-${star.id}`"
          class="sky-star"
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
          class="sky-shoot"
          :style="{ left: `${shoot.left}%`, top: `${shoot.top}%`, animationDelay: `${shoot.delay}s` }"
        ></span>
      </div>

      <!-- Day mode drifting cloud layer -->
      <div class="sky-clouds">
        <span class="sky-cloud sky-cloud-1"></span>
        <span class="sky-cloud sky-cloud-2"></span>
        <span class="sky-cloud sky-cloud-3"></span>
        <span class="sky-cloud sky-cloud-4"></span>
      </div>

      <svg class="sky-hills" viewBox="0 0 1440 220" preserveAspectRatio="none">
        <path class="hill-back" d="M0,170 L160,120 L320,160 L520,90 L720,150 L920,100 L1140,160 L1300,120 L1440,150 L1440,220 L0,220 Z"/>
        <path class="hill-front" d="M0,220 L120,170 L300,210 L480,170 L660,205 L840,170 L1020,210 L1220,175 L1440,205 L1440,220 L0,220 Z"/>
      </svg>
    </div>

    <!-- Decorative blurred colour blobs -->
    <div class="dash-blobs" aria-hidden="true">
      <span class="blob blob-a"></span>
      <span class="blob blob-b"></span>
      <span class="blob blob-c"></span>
      <span class="blob blob-d"></span>
    </div>

    <!-- Decorative sparkle layer -->
    <div class="dash-sparkles" aria-hidden="true">
      <span class="spark spark-a">✨</span>
      <span class="spark spark-b">⭐</span>
      <span class="spark spark-c">💫</span>
      <span class="spark spark-d">✨</span>
    </div>

    <!-- Animated falling water drops after hydration actions -->
    <div class="water-fall-layer">
      <span
        v-for="drop in fallingDrops"
        :key="drop.id"
        class="fall-drop"
        :style="{
          left: `${drop.left}%`,
          animationDelay: `${drop.delay}ms`,
          animationDuration: `${drop.duration}ms`,
          '--drop-size': `${drop.size}px`,
          '--drop-drift': `${drop.drift}px`,
        }"
      ></span>
    </div>

    <!-- Main dashboard content -->
    <div class="dash">
      <!-- Top dashboard header with avatar, date, time, parent link, and streak button -->
      <header class="header">
        <!-- Avatar illustration and orbit decoration -->
        <div class="avatar-zone">
          <div class="avatar">
            <span class="svg-holder avatar-svg" v-html="icons.avatar"></span>
          </div>
          <div class="orbit-ring"><div class="orbit-dot"></div></div>
        </div>

        <div class="header-text">
          <h1>Hey there! Ready to play?</h1>
          <div class="header-sub">Pick a game, collect healthy wins &amp; keep your streak!</div>
        </div>

        <!-- Header quick actions and live date/time information -->
        <div class="header-right">
          <RouterLink to="/parent-dashboard" class="main-site-link">
            <span class="svg-holder mini-svg" v-html="icons.home"></span>
            Parents dashboard
          </RouterLink>
          <div class="date-tag">
            <span class="svg-holder mini-svg" v-html="icons.calendar"></span>
            {{ todayLabel }}
          </div>
          <div class="time-tag">
            <span class="svg-holder mini-svg" v-html="icons.clock"></span>
            {{ liveTime }}
          </div>
          <button type="button" class="streak-tag" @click="celebrateStreak">
            <span class="svg-holder mini-svg flame-icon" v-html="icons.flame"></span>
          </button>
        </div>
      </header>

      <!-- Daily meal check-in panel -->
      <section class="meal-day-panel" aria-labelledby="meal-day-title">
        <header class="meal-day-head">
          <div class="meal-day-heading">
            <span class="svg-holder meal-day-svg" aria-hidden="true" v-html="icons.sun"></span>
            <div>
              <h2 id="meal-day-title" class="meal-day-title">Today's meals</h2>
              <p class="meal-day-sub">Tap when you eat — we save it for today</p>
            </div>
          </div>
        </header>

        <!-- Breakfast, lunch, and dinner quick check buttons -->
        <div class="boost-strip" role="group" aria-label="Breakfast, lunch, and dinner">
          <article
            v-for="check in mealChecks"
            :key="check.label"
            class="boost-pill"
            :class="[check.tone, { 'boost-pill--done': check.done }]"
            @click="toggleMealCheck(check.label, $event)"
          >
            <div class="boost-icon">
              <span class="meal-check-emoji" aria-hidden="true">{{ check.emoji }}</span>
            </div>
            <div class="boost-copy">
              <div class="boost-label">{{ check.label }}</div>
              <div class="boost-sub">{{ check.helper }}</div>
            </div>
            <span class="boost-action">{{ check.actionLabel }}</span>
          </article>
        </div>
      </section>

      <!-- Main game shortcuts and hydration tracker grid -->
      <div class="main-grid">
        <!-- Game shortcut tiles -->
        <section class="games-tiles" aria-label="Pick a game">
          <div class="section-label">
            <span class="svg-holder section-svg" v-html="icons.target"></span>
            Games
          </div>

          <div class="game-tile-grid">
            <button
              v-for="tile in gameTiles"
              :key="tile.id"
              type="button"
              class="game-tile"
              :class="tile.tone"
              @click="launchTile(tile.launchKey)"
            >
              <span class="game-tile-emoji" aria-hidden="true">{{ tile.emoji }}</span>
              <div class="game-tile-copy">
                <strong>{{ tile.title }}</strong>
                <span>{{ tile.short }}</span>
              </div>
              <span class="game-tile-arrow" aria-hidden="true">→</span>
            </button>
          </div>
        </section>

        <!-- Hydration tracker card -->
        <div ref="hydrationCard" class="hydration-card">
          <div class="hyd-ring"></div>
          <div class="hyd-ring"></div>

          <div class="hyd-header">
            <div class="section-label section-green">
              <span class="svg-holder section-svg" v-html="icons.drop"></span>
              Hydration Tracker
            </div>
            <div class="sip-counter" aria-live="polite" :title="`Glasses logged today`">
              <span class="sip-counter-emoji" aria-hidden="true">🥛</span>
              <span class="sip-counter-num">{{ glassCount }}</span>
            </div>
          </div>
          <div class="hydration-title">Stay super hydrated!</div>
          <div class="hydration-sub">Tap a drop to log your glass</div>

          <!-- Water drop buttons for daily glasses -->
          <div class="drop-grid">
            <button
              v-for="(filled, index) in hydrationDrops"
              :key="`drop-${index}`"
              type="button"
              class="drop-btn"
              :class="{ filled }"
              :title="`Sip ${index + 1}`"
              :aria-pressed="filled"
              @click.stop="toggleDrop(index, $event)"
            >
              <span v-if="filled" class="drop-emoji" aria-hidden="true">💧</span>
              <span v-else class="svg-holder drop-svg" v-html="icons.drop"></span>
            </button>
          </div>

          <!-- Hydration action buttons -->
          <div class="hyd-actions">
            <button type="button" class="log-sip-btn" @click.stop="logGlass">
              <span class="svg-holder button-svg" v-html="icons.plusCircle"></span>
              Log another glass
            </button>
            <button
              type="button"
              class="reset-glass-btn"
              :disabled="glassCount === 0"
              @click.stop="resetGlasses"
            >
              Reset
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Temporary toast shown after meal and hydration actions -->
    <transition name="meal-toast">
      <div v-if="mealToast" class="meal-toast" role="status" aria-live="polite">
        {{ mealToast }}
      </div>
    </transition>

    <!-- Full-screen launch overlay shown before a game opens -->
    <transition name="launch-screen">
      <div
        v-if="launching"
        class="launch-screen"
        :class="launchTone"
        role="status"
        aria-live="polite"
      >
        <div class="launch-card">
          <div class="launch-icon-wrap" aria-hidden="true">
            <span class="launch-emoji">{{ launchEmoji }}</span>
          </div>
          <div class="launch-title">{{ launchTitle }}</div>
          <div class="launch-sub">{{ launchSub }}</div>
          <div class="launch-loader" aria-hidden="true">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>
    </transition>

    <!-- Bottom navigation for kids pages -->
    <KidsBottomNav />

    <!-- Floating light/dark mode control -->
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

// Theme, progress, performance, and game-launch composables.
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

// Template refs and reactive UI state.
const confettiLayer = ref(null)
const hydrationCard = ref(null)
const fallingDrops = ref([])
const mealToast = ref("")
const liveTime = ref("")

const skyStars = ref([])
const shootingStars = ref([])

// Internal timers, animation IDs, and cleanup handles.
let nextFallingDropId = 1
const activeRibbons = []

let ribbonFrameId = 0
let mealToastTimer = 0
let liveTimeTimer = 0
let motionMediaListener = null
let visibilityListener = null

// Builds random star positions for the animated night sky.
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

// Builds shooting star animation data.
function buildShootingStars(count) {
  return Array.from({ length: count }, (_, id) => ({
    id,
    left: 12 + Math.random() * 70,
    top: 8 + Math.random() * 40,
    delay: id * 6 + Math.random() * 4,
  }))
}

// Initialises or disables ambient effects based on performance settings.
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

// Starts the live time updater.
function startLiveClock() {
  if (liveTimeTimer || typeof window === "undefined") return
  liveTimeTimer = window.setInterval(updateLiveTime, 1000)
}

// Stops the live time updater.
function stopLiveClock() {
  if (!liveTimeTimer) return
  window.clearInterval(liveTimeTimer)
  liveTimeTimer = 0
}

// Pauses or resumes the live clock when the browser tab visibility changes.
function onVisibilityChange() {
  if (typeof document === "undefined") return
  if (document.hidden) {
    stopLiveClock()
    return
  }
  updateLiveTime()
  startLiveClock()
}

// Sets up ambient effects, saved progress, live time, and listeners when the page loads.
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

// Formatted date shown in the dashboard header.
const todayLabel = new Intl.DateTimeFormat("en-AU", {
  weekday: "short",
  day: "numeric",
  month: "short",
}).format(new Date())

// Updates the live time shown in the dashboard header.
function updateLiveTime() {
  liveTime.value = new Intl.DateTimeFormat("en-AU", {
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit",
  }).format(new Date())
}

// Inline SVG icons used across the dashboard.
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

// Game shortcut tile data.
const gameTiles = [
  {
    id: "bubble",
    launchKey: "bubble",
    title: "Bubble Game",
    short: "Pop healthy words fast",
    emoji: "🫧",
    tone: "tile-bubble",
  },
  {
    id: "explorer",
    launchKey: "explorer",
    title: "Explorer Game",
    short: "Match bright healthy pairs",
    emoji: "🧭",
    tone: "tile-explorer",
  },
  {
    id: "humit",
    launchKey: "humit",
    title: "Hum It!",
    short: "Your hum powers your creature",
    emoji: "🎵",
    tone: "tile-humit",
  },
  {
    id: "smash",
    launchKey: "smash",
    title: "Routine Rumble",
    short: "Smash healthy routines",
    emoji: "🎈",
    tone: "tile-smash",
  },
]

// Meal check cards derived from saved daily progress.
const mealChecks = computed(() => [
  {
    label: "Breakfast",
    helper: kp.daily.meals.Breakfast ? "Saved for today" : "Not logged yet",
    actionLabel: kp.daily.meals.Breakfast ? "Undo" : "Add",
    emoji: "🍳",
    tone: "boost-coral",
    done: Boolean(kp.daily.meals.Breakfast),
  },
  {
    label: "Lunch",
    helper: kp.daily.meals.Lunch ? "Saved for today" : "Not logged yet",
    actionLabel: kp.daily.meals.Lunch ? "Undo" : "Add",
    emoji: "🥪",
    tone: "boost-sky",
    done: Boolean(kp.daily.meals.Lunch),
  },
  {
    label: "Dinner",
    helper: kp.daily.meals.Dinner ? "Saved for today" : "Not logged yet",
    actionLabel: kp.daily.meals.Dinner ? "Undo" : "Add",
    emoji: "🍽️",
    tone: "boost-violet",
    done: Boolean(kp.daily.meals.Dinner),
  },
])

// Hydration goal and safety cap.
const GLASS_GOAL = 8
const GLASS_MAX = 50

// Builds the visible water drop state from the current glass count.
const hydrationDrops = computed(() =>
  Array.from({ length: GLASS_GOAL }, (_, index) => index < Math.min(GLASS_GOAL, kp.daily.waterGlasses)),
)

// Clamps the displayed glass count within the allowed range.
const glassCount = computed(() => Math.max(0, Math.min(GLASS_MAX, kp.daily.waterGlasses)))

// Creates a short ripple animation on tapped controls.
function ripple(event) {
  const el = event.currentTarget
  if (!(el instanceof HTMLElement)) return
  const rippleEl = document.createElement("div")
  rippleEl.className = "rip"
  const rect = el.getBoundingClientRect()
  const size = Math.max(rect.width, rect.height)
  rippleEl.style.width = `${size}px`
  rippleEl.style.height = `${size}px`
  rippleEl.style.left = `${event.clientX - rect.left - size / 2}px`
  rippleEl.style.top = `${event.clientY - rect.top - size / 2}px`
  el.appendChild(rippleEl)
  window.setTimeout(() => rippleEl.remove(), 700)
}

// Spawns lightweight confetti pieces for celebrations.
function spawnConfetti(count, originRect) {
  const n = fx(count)
  if (n < 1) return
  const layer = confettiLayer.value
  if (!layer) return

  const colors = ["#FF6058", "#3B9EFF", "#2CC97A", "#FFB020", "#9B72FF", "#FF7EB3", "#1EC8C8", "#FFDD57"]

  for (let index = 0; index < n; index += 1) {
    const piece = document.createElement("div")
    piece.className = "conf-piece"
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

// Returns a random number between two values.
function randomBetween(min, max) {
  return min + Math.random() * (max - min)
}

// Runs the ribbon physics animation loop.
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

// Creates falling ribbon celebration pieces.
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
    ribbon.className = "cele-ribbon"

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

// Combines confetti and ribbon rain into a bigger celebration.
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

// Fires a small full-page confetti burst.
function fireConfetti() {
  spawnConfetti(26)
}

// Plays the streak celebration when the flame button is tapped.
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

// Plays a small local confetti effect near one element.
function miniConfetti(element) {
  if (!(element instanceof HTMLElement)) return
  spawnConfetti(12, element.getBoundingClientRect())
}

// Creates animated water drops after hydration logging.
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

// Toggles a meal check and shows celebration or undo feedback.
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

// Shows a temporary toast message.
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

// Updates hydration count when a specific drop button is tapped.
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

// Adds one glass of water and shows feedback.
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

// Resets the daily glass count back to zero.
function resetGlasses() {
  const current = kp.daily.waterGlasses
  if (current <= 0) return
  kp.addWater(-current)
  showMealToast("Glasses reset")
}

// Starts a selected game with a launch animation.
function launchTile(launchKey) {
  fireConfetti()
  startGameLaunch(launchKey)
}

// Cleans up timers, listeners, animation frames, and active ribbons before leaving the page.
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

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap");

/* Local reset for this dashboard component */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* Main dashboard wrapper and light mode design tokens */
.kids-html-dashboard {
  --coral: #FF6058;
  --sky: #3B9EFF;
  --mint: #2CC97A;
  --amber: #FFB020;
  --violet: #9B72FF;
  --rose: #FF7EB3;
  --teal: #1EC8C8;
  --ink: #18192B;
  --ink2: #444562;
  --muted: #9395A8;
  --border: #EEEEF5;
  --white: #FFFFFF;
  --bg: #F4F5FB;
  --card-shadow: 0 2px 16px rgba(24, 25, 43, 0.07);
  --card-shadow-hover: 0 12px 40px rgba(24, 25, 43, 0.13);
  --surface: rgba(255, 255, 255, 0.9);
  --surface-strong: #FFFFFF;
  --surface-soft: rgba(255, 255, 255, 0.7);
  --nav-bg: #18192B;
  --nav-text: rgba(255, 255, 255, 0.25);
  --hero-glow-1: rgba(255, 176, 32, 0.26);
  --hero-glow-2: rgba(59, 158, 255, 0.18);
  --hero-glow-3: rgba(155, 114, 255, 0.2);
  font-family: "DM Sans", sans-serif;
  background: var(--bg);
  color: var(--ink);
  overflow-x: hidden;
  min-height: 100vh;
  padding-bottom: 78px;
  position: relative;
}

/* Dark mode design tokens */
.kids-html-dashboard.dark-mode {
  --ink: #F7F8FF;
  --ink2: #C3C7EA;
  --muted: #98A0D0;
  --border: rgba(143, 154, 227, 0.18);
  --white: #12162B;
  --bg: #090E1F;
  --card-shadow: 0 10px 30px rgba(3, 7, 23, 0.42);
  --card-shadow-hover: 0 18px 46px rgba(3, 7, 23, 0.5);
  --surface: rgba(18, 22, 43, 0.92);
  --surface-strong: #171C35;
  --surface-soft: rgba(26, 32, 59, 0.8);
  --nav-bg: rgba(7, 10, 24, 0.92);
  --nav-text: rgba(233, 237, 255, 0.44);
  --hero-glow-1: rgba(255, 126, 179, 0.24);
  --hero-glow-2: rgba(59, 158, 255, 0.22);
  --hero-glow-3: rgba(155, 114, 255, 0.24);
}

/* Fixed ambient background glow */
.kids-html-dashboard::before {
  content: "";
  position: fixed;
  inset: 0;
  background-image:
    radial-gradient(circle at 20% 20%, rgba(59, 158, 255, 0.07) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(155, 114, 255, 0.07) 0%, transparent 50%),
    radial-gradient(circle at 50% 95%, rgba(44, 201, 122, 0.06) 0%, transparent 45%);
  pointer-events: none;
  z-index: 0;
  animation: bgShift 12s ease-in-out infinite alternate;
}

@keyframes bgShift {
  from { background-position: 0% 0%, 100% 100%, 50% 100%; }
  to { background-position: 5% 5%, 95% 95%, 55% 98%; }
}

/* === KIDS SKY (day / night) === */
.kids-sky {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
  contain: layout paint;
}

.sky-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, #ffe6c2 0%, #ffd1b5 22%, #c8e6ff 60%, #e8f4ff 100%);
  transition: background 1.1s ease, opacity 1.1s ease;
}

.dark-mode .sky-gradient {
  background: linear-gradient(180deg, #05071c 0%, #0e1037 32%, #1a1855 62%, #2a1a6b 100%);
}

.sky-aurora {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 18% 16%, rgba(255, 209, 102, 0.5), transparent 42%),
    radial-gradient(ellipse at 78% 14%, rgba(255, 150, 100, 0.32), transparent 38%),
    radial-gradient(ellipse at 50% 78%, rgba(108, 217, 255, 0.28), transparent 45%);
  transition: background 1s ease;
}

.dark-mode .sky-aurora {
  background:
    radial-gradient(ellipse at 22% 14%, rgba(108, 75, 255, 0.5), transparent 45%),
    radial-gradient(ellipse at 80% 22%, rgba(58, 200, 255, 0.3), transparent 42%),
    radial-gradient(ellipse at 50% 80%, rgba(255, 95, 162, 0.18), transparent 48%);
}

.celestial {
  position: absolute;
  width: clamp(150px, 18vw, 240px);
  height: clamp(150px, 18vw, 240px);
  right: 6%;
  transition: top 1.4s cubic-bezier(0.34, 1.1, 0.64, 1), opacity 0.9s ease;
}

.sun-body {
  top: -180px;
  opacity: 0;
}

.kids-html-dashboard:not(.dark-mode) .sun-body {
  top: 6%;
  opacity: 1;
}

.sun-core,
.moon-core {
  position: absolute;
  inset: 22%;
  border-radius: 50%;
  z-index: 2;
}

.sun-core {
  background: radial-gradient(circle at 35% 35%, #fffae3, #ffd166 50%, #ff9a3e 100%);
  box-shadow: 0 0 80px rgba(255, 209, 102, 0.55), inset 0 0 18px rgba(255, 255, 255, 0.5);
  animation: kidsSunPulse 4.5s ease-in-out infinite alternate;
}

.sun-halo {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 209, 102, 0.45) 30%, transparent 70%);
  filter: blur(18px);
  animation: kidsSunSpin 24s linear infinite;
}

.sun-ring {
  position: absolute;
  inset: 9%;
  border-radius: 50%;
  border: 2px dashed rgba(255, 209, 102, 0.35);
  animation: kidsSunSpin 40s linear infinite reverse;
}

@keyframes kidsSunPulse {
  from { transform: scale(1); filter: brightness(1); }
  to   { transform: scale(1.04); filter: brightness(1.1); }
}

@keyframes kidsSunSpin {
  to { transform: rotate(360deg); }
}

.moon-body {
  top: -200px;
  opacity: 0;
}

.dark-mode .moon-body {
  top: 6%;
  opacity: 1;
}

.moon-core {
  background: radial-gradient(circle at 30% 28%, #fdfdff, #c8cbf8 65%, #6c4bff 100%);
  box-shadow: 0 0 90px rgba(155, 134, 255, 0.55), inset 0 0 14px rgba(255, 255, 255, 0.35);
  animation: kidsMoonGlow 5s ease-in-out infinite alternate;
}

.moon-halo {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(155, 134, 255, 0.42) 30%, transparent 70%);
  filter: blur(22px);
}

.crater {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, rgba(108, 75, 255, 0.55), rgba(50, 30, 110, 0.85));
  box-shadow: inset -1px -1px 2px rgba(0, 0, 0, 0.25);
}

.crater-1 { width: 18%; height: 18%; top: 25%; left: 30%; }
.crater-2 { width: 12%; height: 12%; top: 55%; left: 55%; }
.crater-3 { width: 9%;  height: 9%;  top: 38%; left: 60%; }

@keyframes kidsMoonGlow {
  from { transform: scale(1); filter: brightness(1); }
  to   { transform: scale(1.03); filter: brightness(1.12); }
}

.sky-stars {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 1.1s ease;
}

.dark-mode .sky-stars { opacity: 1; }

.sky-star {
  position: absolute;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 0 6px rgba(255, 255, 255, 0.85);
  animation: kidsStarTwinkle 2.6s ease-in-out infinite alternate;
}

@keyframes kidsStarTwinkle {
  from { opacity: 0.25; transform: scale(0.8); }
  to   { opacity: 1;    transform: scale(1.3); }
}

.sky-shoot {
  position: absolute;
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0) 0%, #fff 60%, #fff 80%, rgba(255, 255, 255, 0));
  border-radius: 999px;
  opacity: 0;
  transform: rotate(-22deg);
  animation: kidsShoot 9s linear infinite;
}

@keyframes kidsShoot {
  0%   { opacity: 0; transform: translate(-20px, 0) rotate(-22deg); }
  6%   { opacity: 1; }
  12%  { opacity: 0; transform: translate(240px, 90px) rotate(-22deg); }
  100% { opacity: 0; transform: translate(240px, 90px) rotate(-22deg); }
}

.sky-clouds {
  position: absolute;
  inset: 0;
  transition: opacity 1s ease, filter 1s ease;
}

.dark-mode .sky-clouds { opacity: 0.18; filter: blur(1.5px); }

.sky-cloud {
  position: absolute;
  background: rgba(255, 255, 255, 0.92);
  border-radius: 999px;
  filter: blur(0.4px);
  box-shadow:
    20px -8px 0 0 rgba(255, 255, 255, 0.9),
    40px 5px 0 -3px rgba(255, 255, 255, 0.85),
    -18px 6px 0 -4px rgba(255, 255, 255, 0.8);
}

.sky-cloud-1 { width: 120px; height: 30px; top: 14%; left: 6%;  animation: kidsCloudDrift 42s linear infinite; }
.sky-cloud-2 { width: 86px;  height: 22px; top: 24%; left: 28%; animation: kidsCloudDrift 56s linear infinite reverse; animation-delay: -8s; }
.sky-cloud-3 { width: 110px; height: 28px; top: 10%; left: 52%; animation: kidsCloudDrift 48s linear infinite; animation-delay: -16s; }
.sky-cloud-4 { width: 76px;  height: 20px; top: 36%; left: 12%; animation: kidsCloudDrift 64s linear infinite reverse; animation-delay: -22s; }

@keyframes kidsCloudDrift {
  from { transform: translateX(-12vw); }
  to   { transform: translateX(115vw); }
}

.sky-hills {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 22vh;
  min-height: 140px;
  opacity: 0.85;
  transition: opacity 0.8s ease;
}

.hill-back  { fill: rgba(180, 200, 230, 0.7); transition: fill 0.8s ease; }
.hill-front { fill: rgba(125, 155, 210, 0.85); transition: fill 0.8s ease; }

.dark-mode .hill-back  { fill: rgba(36, 36, 88, 0.85); }
.dark-mode .hill-front { fill: rgba(14, 14, 42, 0.96); }

.dash-blobs {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
  contain: layout paint;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.35;
  mix-blend-mode: screen;
}

.blob-a {
  width: 320px; height: 320px;
  left: -80px; top: 12%;
  background: radial-gradient(circle, rgba(59, 158, 255, 0.45), rgba(59, 158, 255, 0) 70%);
  animation: blobDriftA 18s ease-in-out infinite alternate;
}

.blob-b {
  width: 380px; height: 380px;
  right: -110px; top: 35%;
  background: radial-gradient(circle, rgba(155, 114, 255, 0.4), rgba(155, 114, 255, 0) 70%);
  animation: blobDriftB 22s ease-in-out infinite alternate;
}

.blob-c {
  width: 260px; height: 260px;
  left: 30%; bottom: -100px;
  background: radial-gradient(circle, rgba(44, 201, 122, 0.4), rgba(44, 201, 122, 0) 70%);
  animation: blobDriftC 20s ease-in-out infinite alternate;
}

.blob-d {
  width: 240px; height: 240px;
  right: 18%; top: 4%;
  background: radial-gradient(circle, rgba(255, 176, 32, 0.36), rgba(255, 176, 32, 0) 70%);
  animation: blobDriftD 24s ease-in-out infinite alternate;
}

.dark-mode .blob { opacity: 0.45; }

@keyframes blobDriftA {
  from { transform: translate3d(0, 0, 0) scale(1); }
  to { transform: translate3d(40px, 30px, 0) scale(1.08); }
}

@keyframes blobDriftB {
  from { transform: translate3d(0, 0, 0) scale(1); }
  to { transform: translate3d(-50px, -40px, 0) scale(1.1); }
}

@keyframes blobDriftC {
  from { transform: translate3d(0, 0, 0) scale(1); }
  to { transform: translate3d(60px, -50px, 0) scale(1.12); }
}

@keyframes blobDriftD {
  from { transform: translate3d(0, 0, 0) scale(1); }
  to { transform: translate3d(-30px, 50px, 0) scale(1.06); }
}

.dash-sparkles {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.spark {
  position: absolute;
  font-size: 16px;
  opacity: 0.35;
  filter: drop-shadow(0 2px 4px rgba(255, 255, 255, 0.18));
}

.spark-a { left: 8%;  top: 22%; animation: sparkDrift 9s ease-in-out infinite; }
.spark-b { right: 12%; top: 40%; animation: sparkDrift 11s ease-in-out 1.4s infinite; }
.spark-c { left: 42%; bottom: 16%; animation: sparkDrift 12s ease-in-out 0.7s infinite; }
.spark-d { right: 30%; bottom: 28%; animation: sparkDrift 10.5s ease-in-out 2s infinite; }

@keyframes sparkDrift {
  0%, 100% { transform: translateY(0) rotate(0); opacity: 0.18; }
  50% { transform: translateY(-14px) rotate(15deg); opacity: 0.6; }
}

.dash {
  position: relative;
  z-index: 1;
  max-width: min(900px, 100%);
  margin: 0 auto;
  padding: clamp(14px, 3vw, 16px) clamp(12px, 3.5vw, 14px) clamp(28px, 5vw, 34px);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--surface);
  border-radius: 22px;
  padding: 15px 18px;
  margin-bottom: 14px;
  box-shadow: var(--card-shadow);
  border: 1.5px solid var(--border);
  animation: headerDrop 0.7s cubic-bezier(0.22, 1, 0.36, 1) both;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(16px);
}

@keyframes headerDrop {
  from { transform: translateY(-40px) scale(0.97); opacity: 0; }
  to { transform: translateY(0) scale(1); opacity: 1; }
}

.header::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 12% 18%, var(--hero-glow-1) 0%, transparent 24%),
    radial-gradient(circle at 84% 16%, var(--hero-glow-2) 0%, transparent 30%),
    radial-gradient(circle at 52% 112%, var(--hero-glow-3) 0%, transparent 34%);
  pointer-events: none;
}

.header::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--coral), var(--amber), var(--mint), var(--sky), var(--violet), var(--rose));
  background-size: 400% 100%;
  animation: gradientWave 4s linear infinite;
}

@keyframes gradientWave { 0% { background-position: 0%; } 100% { background-position: 400%; } }

.header > * {
  position: relative;
  z-index: 1;
}

.avatar-zone {
  position: relative;
  cursor: pointer;
  flex-shrink: 0;
  animation: avatarBreathe 4.6s ease-in-out infinite;
}

.avatar {
  width: 52px;
  height: 52px;
  background: linear-gradient(145deg, #FFE4C8, #FFCBA4);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 18px rgba(255, 176, 32, 0.3);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.avatar:hover { transform: rotate(-8deg) scale(1.1); }

@keyframes avatarBreathe {
  0%, 100% { transform: translateY(0) rotate(0); }
  50% { transform: translateY(-3px) rotate(1.2deg); }
}

.orbit-ring {
  position: absolute;
  inset: -7px;
  border-radius: 22px;
  border: 2px dashed rgba(255, 176, 32, 0.35);
  animation: orbitSpin 6s linear infinite;
}

@keyframes orbitSpin { from { transform: rotate(0); } to { transform: rotate(360deg); } }

.orbit-dot {
  position: absolute;
  top: -4px;
  left: 50%;
  width: 8px;
  height: 8px;
  background: var(--amber);
  border-radius: 50%;
  transform: translateX(-50%);
  box-shadow: 0 0 6px var(--amber);
}

.header-text { flex: 1; margin-left: 11px; }

.greeting-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #F0FFF8;
  border: 1.5px solid #C2F0D8;
  border-radius: 20px;
  padding: 3px 10px;
  font-size: 11px;
  font-weight: 700;
  color: var(--mint);
  margin-bottom: 5px;
  animation: chipFadeIn 0.5s ease 0.4s both;
}

@keyframes chipFadeIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }

.chip-dot {
  width: 6px;
  height: 6px;
  background: var(--mint);
  border-radius: 50%;
  animation: dotBlink 1.4s ease-in-out infinite;
}

@keyframes dotBlink {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.3; transform: scale(0.5); }
}

.header-text h1 {
  font-family: "Baloo 2", cursive;
  font-size: clamp(18px, 2.8vw, 21px);
  font-weight: 800;
  color: var(--ink);
  line-height: 1.1;
  animation: textReveal 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.2s both;
}

@keyframes textReveal { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0% 0 0); } }

.header-text h1 em { font-style: normal; color: var(--coral); }
.header-sub { font-size: 12px; color: var(--muted); font-weight: 500; margin-top: 2px; }

.header-right {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  max-width: 460px;
}

.main-site-link {
  background: linear-gradient(135deg, rgba(44, 201, 122, 0.16), rgba(30, 200, 200, 0.14));
  border: 1.5px solid rgba(44, 201, 122, 0.22);
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 11px;
  font-weight: 700;
  color: var(--ink);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  box-shadow: 0 6px 18px rgba(44, 201, 122, 0.14);
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s, filter 0.25s;
}

.main-site-link:hover {
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 10px 22px rgba(44, 201, 122, 0.2);
  filter: brightness(1.02);
}

.theme-toggle {
  background: linear-gradient(135deg, rgba(59, 158, 255, 0.15), rgba(155, 114, 255, 0.18));
  border: 1.5px solid rgba(115, 131, 255, 0.2);
  border-radius: 999px;
  padding: 7px 12px;
  font-size: 12px;
  font-weight: 700;
  color: var(--ink);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s, background 0.25s;
  box-shadow: 0 6px 18px rgba(76, 104, 255, 0.14);
}

.theme-toggle:hover {
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 10px 22px rgba(76, 104, 255, 0.22);
}

.theme-toggle[aria-pressed="true"] {
  background: linear-gradient(135deg, rgba(19, 27, 66, 0.96), rgba(62, 37, 112, 0.96));
  color: #F8FAFF;
}

.date-tag,
.time-tag {
  background: var(--bg);
  border: 1.5px solid var(--border);
  border-radius: 20px;
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 600;
  color: var(--ink2);
  display: flex;
  align-items: center;
  gap: 5px;
}

.streak-tag {
  background: linear-gradient(135deg, #FFF8E8, #FFEEC8);
  border: 1.5px solid #FFD980;
  border-radius: 15px;
  width: 38px;
  height: 38px;
  color: #A06800;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  cursor: pointer;
  transition: box-shadow 0.2s ease, filter 0.2s ease;
  border-style: solid;
}

.streak-tag:hover { box-shadow: 0 4px 14px rgba(255, 176, 32, 0.3); filter: brightness(1.03); }
.flame-icon { animation: flameDance 0.35s ease-in-out infinite alternate; }
@keyframes flameDance { from { transform: scaleY(1) rotate(-4deg); } to { transform: scaleY(1.15) rotate(4deg); } }

.meal-day-panel {
  margin-bottom: 12px;
  padding: 11px 12px 10px;
  border-radius: 18px;
  border: 1.5px solid rgba(255, 176, 32, 0.26);
  background:
    linear-gradient(165deg, rgba(255, 253, 248, 0.98) 0%, rgba(255, 251, 242, 0.96) 38%, rgba(242, 246, 255, 0.55) 100%);
  box-shadow:
    0 10px 32px rgba(255, 149, 92, 0.09),
    0 1px 0 rgba(255, 255, 255, 0.9) inset;
}

.meal-day-head {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(24, 25, 43, 0.07);
}

.meal-day-heading {
  display: flex;
  align-items: center;
  gap: 10px;
}

.meal-day-svg :deep(svg) {
  width: 20px;
  height: 20px;
  color: #e89400;
  flex-shrink: 0;
}

.meal-day-title {
  font-family: "Baloo 2", cursive;
  font-size: clamp(14px, 3.6vw, 15px);
  font-weight: 800;
  color: var(--ink);
  line-height: 1.15;
  margin: 0;
}

.meal-day-sub {
  font-size: 10px;
  font-weight: 600;
  color: var(--muted);
  margin: 3px 0 0;
  line-height: 1.35;
}

.boost-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
}

.boost-pill {
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 5px;
  padding: 8px 10px;
  border-radius: 14px;
  border: 1.5px solid var(--border);
  background: var(--surface);
  box-shadow: 0 4px 14px rgba(24, 25, 43, 0.06);
  cursor: pointer;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  animation: floatIn 0.65s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.boost-pill::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.65) 0%, transparent 48%);
  opacity: 0.75;
  pointer-events: none;
  z-index: 0;
}

.boost-pill:active {
  transform: none;
}

.boost-strip .boost-pill:nth-child(2) { animation-delay: 0.08s; }
.boost-strip .boost-pill:nth-child(3) { animation-delay: 0.16s; }

@keyframes floatIn {
  from { opacity: 0; transform: translateY(20px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.boost-icon,
.boost-copy,
.boost-action {
  position: relative;
  z-index: 1;
}

.boost-icon {
  width: 30px;
  height: 30px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.94);
  box-shadow:
    0 2px 8px rgba(24, 25, 43, 0.07),
    inset 0 1px 0 rgba(255, 255, 255, 1);
  backdrop-filter: blur(8px);
}

.boost-copy {
  width: 100%;
  min-width: 0;
}

.boost-label {
  font-family: "Baloo 2", cursive;
  font-size: 13px;
  font-weight: 800;
  line-height: 1;
  text-align: center;
}

.boost-sub {
  font-size: 9px;
  color: rgba(24, 25, 43, 0.62);
  font-weight: 600;
  margin-top: 2px;
  text-align: center;
  line-height: 1.3;
}

.boost-action {
  margin-top: 1px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 3px 9px;
  border-radius: 999px;
  font-size: 8px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(24, 25, 43, 0.1);
  color: rgba(24, 25, 43, 0.72);
}

.boost-pill--done {
  border-color: rgba(44, 201, 122, 0.42);
  box-shadow:
    0 4px 18px rgba(44, 201, 122, 0.14),
    inset 0 0 0 1px rgba(44, 201, 122, 0.06);
}

.boost-pill--done .boost-action {
  background: rgba(44, 201, 122, 0.2);
  border-color: rgba(44, 201, 122, 0.38);
  color: #065c34;
}

.boost-pill--done .boost-sub {
  color: rgba(6, 92, 52, 0.78);
  font-weight: 700;
}

.meal-toast {
  position: fixed;
  top: 22px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 120;
  min-width: min(320px, calc(100vw - 32px));
  text-align: center;
  padding: 14px 18px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(44, 201, 122, 0.96), rgba(118, 233, 171, 0.96));
  border: 1.5px solid rgba(255, 255, 255, 0.42);
  box-shadow: 0 18px 34px rgba(44, 201, 122, 0.28);
  font-family: "Baloo 2", cursive;
  font-size: 18px;
  font-weight: 800;
  color: #08361b;
  pointer-events: none;
}

.meal-toast-enter-active,
.meal-toast-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.meal-toast-enter-from,
.meal-toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-10px) scale(0.98);
}

.meal-check-emoji {
  font-size: 15px;
  line-height: 1;
}

.boost-coral {
  background: linear-gradient(155deg, #fffbf7 0%, #fff0e8 36%, #ffd8ca 100%);
  border-color: rgba(255, 107, 84, 0.38);
}

.boost-sky {
  background: linear-gradient(155deg, #f7fbff 0%, #ebf5fc 38%, #dbeefa 100%);
  border-color: rgba(59, 158, 255, 0.4);
}

.boost-violet {
  background: linear-gradient(155deg, #fbfaff 0%, #f2ebff 40%, #e6dcf9 100%);
  border-color: rgba(139, 92, 246, 0.34);
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 18px;
}

.stat-card {
  background: var(--surface);
  border-radius: 22px;
  padding: 16px 14px;
  box-shadow: var(--card-shadow);
  border: 1.5px solid var(--border);
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.35s;
}

.stat-card:hover { transform: translateY(-7px) scale(1.03); box-shadow: var(--card-shadow-hover); }
.stat-card:nth-child(1) { animation: flipInLeft 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.05s both; }
.stat-card:nth-child(2) { animation: dropBounceIn 0.65s cubic-bezier(0.34, 1.56, 0.64, 1) 0.15s both; }
.stat-card:nth-child(3) { animation: scalePop 0.55s cubic-bezier(0.34, 1.56, 0.64, 1) 0.25s both; }
.stat-card:nth-child(4) { animation: flipInRight 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.35s both; }

@keyframes flipInLeft { from { transform: rotateY(-60deg) translateX(-20px); opacity: 0; } to { transform: rotateY(0) translateX(0); opacity: 1; } }
@keyframes dropBounceIn { from { transform: translateY(-40px) scale(0.8); opacity: 0; } to { transform: translateY(0) scale(1); opacity: 1; } }
@keyframes scalePop { from { transform: scale(0.5); opacity: 0; } to { transform: scale(1); opacity: 1; } }
@keyframes flipInRight { from { transform: rotateY(60deg) translateX(20px); opacity: 0; } to { transform: rotateY(0) translateX(0); opacity: 1; } }

.stat-icon {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 11px;
  transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.stat-card:hover .stat-icon { transform: rotate(12deg) scale(1.15); }
.stat-label { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: var(--muted); margin-bottom: 3px; }
.stat-value { font-family: "Baloo 2", cursive; font-size: 25px; font-weight: 800; line-height: 1; color: var(--ink); }
.stat-sub { font-size: 11px; font-weight: 600; margin-top: 3px; }

.prog-track { background: #F0F1F8; border-radius: 10px; height: 6px; margin-top: 10px; overflow: hidden; }

.prog-fill {
  height: 100%;
  border-radius: 10px;
  position: relative;
  animation: barGrow 1.3s cubic-bezier(0.34, 1.56, 0.64, 1) 0.7s both;
}

@keyframes barGrow { from { width: 0 !important; } }

.prog-fill::after {
  content: "";
  position: absolute;
  top: 0;
  left: -30%;
  width: 30%;
  height: 100%;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 10px;
  animation: travelShimmer 2.2s ease-in-out 1.5s infinite;
}

@keyframes travelShimmer {
  0% { left: -30%; opacity: 0; }
  30% { opacity: 1; }
  70% { opacity: 1; }
  100% { left: 110%; opacity: 0; }
}

.sc-steps { background: linear-gradient(160deg, rgba(255, 240, 238, 0.96), rgba(255, 255, 255, 0.92)); }
.sc-steps .stat-icon { background: #FFF0EE; }
.sc-steps .prog-fill { background: linear-gradient(90deg, #FFA8A4, var(--coral)); }
.sc-steps .stat-sub { color: var(--coral); }

.sc-water { background: linear-gradient(160deg, rgba(234, 243, 255, 0.96), rgba(255, 255, 255, 0.92)); }
.sc-water .stat-icon { background: #EAF3FF; }
.sc-water .prog-fill { background: linear-gradient(90deg, #82C4FF, var(--sky)); }
.sc-water .stat-sub { color: var(--sky); }

.sc-sleep { background: linear-gradient(160deg, rgba(242, 238, 255, 0.96), rgba(255, 255, 255, 0.92)); }
.sc-sleep .stat-icon { background: #F2EEFF; }
.sc-sleep .prog-fill { background: linear-gradient(90deg, #C3ACFF, var(--violet)); }
.sc-sleep .stat-sub { color: var(--violet); }

.sc-mood { background: linear-gradient(160deg, rgba(238, 255, 245, 0.96), rgba(255, 255, 255, 0.92)); }
.sc-mood .stat-icon { background: #EEFFF5; }
.sc-mood .prog-fill { background: linear-gradient(90deg, #7DE8A8, var(--mint)); }
.sc-mood .stat-sub { color: var(--mint); }

.stat-card::before {
  content: "";
  position: absolute;
  right: -18px;
  bottom: -18px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  opacity: 0.06;
  transition: transform 0.4s ease, opacity 0.4s;
}

.sc-steps::before { background: var(--coral); }
.sc-water::before { background: var(--sky); }
.sc-sleep::before { background: var(--violet); }
.sc-mood::before { background: var(--mint); }
.stat-card:hover::before { transform: scale(2.5); opacity: 0.09; }

.main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 11px; margin-bottom: 11px; }

.section-label {
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.3px;
  color: var(--muted);
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.games-tiles {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.94), rgba(248, 246, 255, 0.98));
  border-radius: 18px;
  padding: 13px 14px;
  border: 1.5px solid var(--border);
  box-shadow: var(--card-shadow);
  animation: floatIn 0.65s cubic-bezier(0.22, 1, 0.36, 1) 0.3s both;
}

.game-tile-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px;
  margin-top: 8px;
}

@media (min-width: 560px) {
  .game-tile-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

.game-tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  padding: 8px 10px;
  border-radius: 12px;
  border: 1.5px solid var(--border);
  background: var(--bg);
  cursor: pointer;
  text-align: center;
  font-family: "DM Sans", sans-serif;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s, border-color 0.25s, background 0.25s;
}

.game-tile:active {
  transform: none;
}

@media (hover: hover) and (pointer: fine) {
  .game-tile:hover {
    transform: translateY(-2px);
    border-color: rgba(115, 131, 255, 0.32);
    box-shadow: 0 8px 20px rgba(60, 80, 180, 0.12);
  }
}

.game-tile-emoji {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  font-size: 19px;
  background: linear-gradient(145deg, #FFFFFF, #F2F1FF);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7), 0 4px 10px rgba(70, 92, 200, 0.1);
  flex-shrink: 0;
}

.game-tile-copy {
  flex: 0 1 auto;
  display: grid;
  gap: 2px;
  justify-items: center;
  text-align: center;
}

.game-tile-copy strong {
  font-family: "Baloo 2", cursive;
  font-size: 13px;
  font-weight: 800;
  color: var(--ink);
}

.game-tile-copy span {
  font-size: 10px;
  font-weight: 600;
  color: var(--muted);
}

.game-tile-arrow {
  font-family: "Baloo 2", cursive;
  font-size: 16px;
  font-weight: 800;
  color: var(--muted);
  transition: transform 0.25s ease, color 0.25s ease;
  line-height: 1;
}

@media (hover: hover) and (pointer: fine) {
  .game-tile:hover .game-tile-arrow {
    transform: translateX(4px);
    color: var(--ink);
  }
}

.game-tile.tile-bubble {
  background: linear-gradient(145deg, rgba(59, 158, 255, 0.1), rgba(255, 255, 255, 0.95));
  border-color: rgba(59, 158, 255, 0.22);
}

.game-tile.tile-explorer {
  background: linear-gradient(145deg, rgba(44, 201, 122, 0.12), rgba(255, 255, 255, 0.95));
  border-color: rgba(44, 201, 122, 0.22);
}

.game-tile.tile-humit {
  background: linear-gradient(145deg, rgba(155, 114, 255, 0.14), rgba(79, 209, 255, 0.12));
  border-color: rgba(124, 92, 255, 0.28);
}

.game-tile.tile-smash {
  background: linear-gradient(145deg, rgba(255, 96, 88, 0.1), rgba(255, 248, 245, 0.95));
  border-color: rgba(255, 96, 88, 0.22);
}

.dark-mode .games-tiles {
  background: linear-gradient(145deg, rgba(20, 24, 50, 0.96), rgba(14, 18, 40, 0.96));
  backdrop-filter: blur(18px);
}

.dark-mode .game-tile {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(143, 154, 227, 0.22);
}

.dark-mode .game-tile.tile-bubble {
  background: linear-gradient(145deg, rgba(28, 56, 100, 0.7), rgba(16, 20, 44, 0.85));
}

.dark-mode .game-tile.tile-explorer {
  background: linear-gradient(145deg, rgba(20, 60, 44, 0.72), rgba(14, 22, 36, 0.88));
}

.dark-mode .game-tile.tile-humit {
  background: linear-gradient(145deg, rgba(90, 70, 160, 0.72), rgba(28, 90, 120, 0.82));
  border-color: rgba(160, 190, 255, 0.35);
}

.dark-mode .game-tile.tile-smash {
  background: linear-gradient(145deg, rgba(82, 26, 42, 0.7), rgba(20, 16, 36, 0.88));
}

.dark-mode .game-tile-emoji {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.04));
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.12), 0 6px 14px rgba(3, 7, 23, 0.45);
}

.launch-screen {
  position: fixed;
  inset: 0;
  z-index: 200;
  display: grid;
  place-items: center;
  padding: 24px;
  background:
    radial-gradient(circle at top, rgba(255, 176, 32, 0.18), transparent 32%),
    radial-gradient(circle at bottom, rgba(59, 158, 255, 0.22), transparent 40%),
    rgba(8, 12, 32, 0.5);
  backdrop-filter: blur(10px);
}

.launch-card {
  min-width: min(360px, calc(100vw - 32px));
  max-width: 420px;
  padding: 28px 32px;
  border-radius: 32px;
  border: 1.5px solid rgba(255, 255, 255, 0.2);
  background: linear-gradient(155deg, rgba(48, 36, 110, 0.96), rgba(22, 26, 64, 0.96));
  box-shadow: 0 30px 80px rgba(8, 10, 32, 0.45);
  display: grid;
  justify-items: center;
  gap: 12px;
  text-align: center;
}

.launch-screen.tone-bubble .launch-card {
  background: linear-gradient(155deg, rgba(50, 102, 200, 0.96), rgba(34, 56, 130, 0.96));
}
.launch-screen.tone-explorer .launch-card {
  background: linear-gradient(155deg, rgba(28, 130, 90, 0.96), rgba(22, 70, 56, 0.96));
}
.launch-screen.tone-smash .launch-card {
  background: linear-gradient(155deg, rgba(196, 60, 110, 0.96), rgba(110, 26, 78, 0.96));
}
.launch-screen.tone-humit .launch-card {
  background: linear-gradient(155deg, rgba(124, 92, 255, 0.96), rgba(40, 160, 210, 0.96));
}
.launch-screen.tone-games .launch-card {
  background: linear-gradient(155deg, rgba(225, 132, 56, 0.96), rgba(160, 48, 110, 0.96));
}

.launch-icon-wrap {
  width: 86px;
  height: 86px;
  border-radius: 28px;
  display: grid;
  place-items: center;
  background: linear-gradient(155deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.06));
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.25);
  animation: launchPulse 0.85s ease-in-out infinite alternate;
}

.launch-emoji {
  font-size: 44px;
  line-height: 1;
}

.launch-title {
  font-family: "Baloo 2", cursive;
  font-size: 26px;
  font-weight: 800;
  color: #FFFFFF;
}

.launch-sub {
  font-size: 14px;
  font-weight: 600;
  color: rgba(232, 237, 255, 0.86);
}

.launch-loader {
  margin-top: 6px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.launch-loader span {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.85);
  animation: launchDot 1.1s ease-in-out infinite;
}

.launch-loader span:nth-child(2) { animation-delay: 0.18s; }
.launch-loader span:nth-child(3) { animation-delay: 0.36s; }

@keyframes launchPulse {
  from { transform: scale(1); box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.25), 0 10px 26px rgba(59, 158, 255, 0.22); }
  to { transform: scale(1.06); box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.25), 0 18px 36px rgba(255, 176, 32, 0.28); }
}

@keyframes launchDot {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
  40% { transform: translateY(-6px); opacity: 1; }
}

.launch-screen-enter-active,
.launch-screen-leave-active {
  transition: opacity 0.55s ease, transform 0.55s ease;
}

.launch-screen-enter-from,
.launch-screen-leave-to {
  opacity: 0;
}

.launch-screen-enter-from .launch-card,
.launch-screen-leave-to .launch-card {
  transform: translateY(20px) scale(0.94);
}

.wins-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.94), rgba(245, 247, 255, 0.98));
  border-radius: 26px;
  padding: 22px;
  box-shadow: var(--card-shadow);
  border: 1.5px solid var(--border);
  animation: winsReveal 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.4s both;
}

@keyframes winsReveal {
  from { transform: translateX(30px) rotate(1.5deg); opacity: 0; }
  to { transform: translateX(0) rotate(0); opacity: 1; }
}

.win-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 13px;
  border-radius: 16px;
  margin-bottom: 7px;
  background: var(--surface-soft);
  border: 1.5px solid var(--border);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.win-item:nth-child(2):hover { transform: scale(1.03); background: #FFF4F3; border-color: #FFD0CC; }
.win-item:nth-child(3):hover { transform: scale(1.03); background: #F0F8FF; border-color: #BBDCFF; }
.win-item:nth-child(4):hover { transform: scale(1.03); background: #F0F7FF; border-color: #D4CAFF; }

.win-icon {
  width: 40px;
  height: 40px;
  border-radius: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.win-item:hover .win-icon { transform: rotate(-10deg) scale(1.18); }
.win-icon-1 { background: #FFF0EE; }
.win-icon-2 { background: #EAF3FF; }
.win-icon-3 { background: #F2EEFF; }

.win-title { font-size: 13px; font-weight: 700; color: var(--ink); }
.win-sub { font-size: 11px; color: var(--muted); font-weight: 500; }

.win-check {
  margin-left: auto;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--mint);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0) rotate(-90deg);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  flex-shrink: 0;
}

.win-item:hover .win-check { opacity: 1; transform: scale(1) rotate(0deg); }

.meal-banner {
  grid-column: 1 / -1;
  background: linear-gradient(130deg, #FFFBF0, #FFF4D6);
  border-radius: 26px;
  padding: 22px 26px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: var(--card-shadow);
  border: 1.5px solid #FFE8A0;
  animation: mealBannerIn 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.5s both;
  position: relative;
  overflow: hidden;
}

@keyframes mealBannerIn {
  from { transform: scaleX(0.85) translateY(15px); opacity: 0; transform-origin: left center; }
  to { transform: scaleX(1) translateY(0); opacity: 1; }
}

.meal-float {
  position: absolute;
  right: 180px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  gap: 10px;
  opacity: 0.18;
}

.meal-float .float-svg :deep(svg) {
  width: 28px;
  height: 28px;
  color: #D97A00;
  animation: floatBob 3s ease-in-out infinite;
}

.meal-float .float-svg:nth-child(2) :deep(svg) { animation-delay: 0.4s; }
.meal-float .float-svg:nth-child(3) :deep(svg) { animation-delay: 0.8s; }
.meal-float .float-svg:nth-child(4) :deep(svg) { animation-delay: 1.2s; }

@keyframes floatBob {
  0%, 100% { transform: translateY(0) rotate(0); }
  50% { transform: translateY(-8px) rotate(5deg); }
}

.meal-text .section-label { color: #B07800; }
.meal-title { font-family: "Baloo 2", cursive; font-size: 20px; font-weight: 800; color: #6B3A00; margin-bottom: 3px; }
.meal-sub { font-size: 13px; color: #A07020; font-weight: 500; }

.meal-btn {
  background: linear-gradient(135deg, var(--amber), #FFD060);
  color: #6B3A00;
  border: none;
  border-radius: 16px;
  padding: 13px 20px;
  font-family: "Baloo 2", cursive;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 5px 18px rgba(255, 176, 32, 0.35);
  white-space: nowrap;
  flex-shrink: 0;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s;
  position: relative;
  overflow: hidden;
}

.meal-btn:hover { transform: translateY(-4px) scale(1.04); box-shadow: 0 8px 24px rgba(255, 176, 32, 0.45); }
.meal-btn:hover .button-svg :deep(svg) { transform: rotate(360deg); }

.game-section {
  margin-bottom: 14px;
  animation: fadeLift 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.6s both;
}

@keyframes fadeLift { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.section-heading { font-family: "Baloo 2", cursive; font-size: 18px; font-weight: 800; color: var(--ink); }

.see-all {
  font-size: 12px;
  font-weight: 700;
  color: var(--sky);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 3px;
  text-decoration: none;
  transition: gap 0.25s;
  background: transparent;
  border: 0;
}

.see-all:hover { gap: 6px; }

.games-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }

.game-card {
  background: var(--surface);
  border-radius: 22px;
  padding: 18px 16px;
  cursor: pointer;
  border: 1.5px solid var(--border);
  box-shadow: var(--card-shadow);
  position: relative;
  overflow: hidden;
  transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.35s, border-color 0.3s;
  text-align: left;
}

.game-card:hover { transform: translateY(-8px) scale(1.02); box-shadow: var(--card-shadow-hover); }
.game-card:nth-child(1) { --gc: var(--coral); --gc-light: #FFF0EE; }
.game-card:nth-child(2) { --gc: var(--sky); --gc-light: #EAF3FF; }
.game-card:nth-child(3) { --gc: var(--violet); --gc-light: #F2EEFF; }
.game-card:hover { border-color: var(--gc); }

.game-card::before {
  content: "";
  position: absolute;
  inset: 0;
  background: var(--gc-light);
  border-radius: 22px;
  transform: scaleY(0);
  transform-origin: bottom;
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1);
  z-index: 0;
}

.game-card:hover::before { transform: scaleY(1); }
.game-card > * { position: relative; z-index: 1; }

.game-icon {
  width: 48px;
  height: 48px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: var(--gc-light);
}

.game-card:hover .game-icon { transform: scale(1.2) rotate(-10deg); }
.game-name { font-family: "Baloo 2", cursive; font-size: 14px; font-weight: 700; color: var(--ink); margin-bottom: 3px; }
.game-desc { font-size: 11px; color: var(--muted); font-weight: 500; line-height: 1.4; }

.active-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: var(--coral);
  color: white;
  font-size: 9px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 3px 8px;
  border-radius: 20px;
  animation: badgePulseScale 1.6s ease-in-out infinite;
}

@keyframes badgePulseScale { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }

.bottom-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  animation: fadeLift 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.75s both;
}

.challenge-card {
  background: linear-gradient(145deg, #EEF5FF, #E0EEFF);
  border-radius: 26px;
  padding: 22px;
  border: 1.5px solid rgba(59, 158, 255, 0.2);
  box-shadow: var(--card-shadow);
  position: relative;
  overflow: hidden;
}

.challenge-card::before {
  content: "";
  position: absolute;
  right: -30px;
  bottom: -30px;
  width: 120px;
  height: 120px;
  border: 16px solid rgba(59, 158, 255, 0.07);
  border-radius: 50%;
  animation: ringExpand 4s ease-out infinite;
}

.challenge-card::after {
  content: "";
  position: absolute;
  right: -50px;
  bottom: -50px;
  width: 160px;
  height: 160px;
  border: 10px solid rgba(59, 158, 255, 0.05);
  border-radius: 50%;
  animation: ringExpand 4s ease-out 0.8s infinite;
}

@keyframes ringExpand { 0% { transform: scale(0.6); opacity: 0.8; } 100% { transform: scale(1.4); opacity: 0; } }

.section-blue { color: var(--sky); }
.challenge-title { font-family: "Baloo 2", cursive; font-size: 18px; font-weight: 800; color: #1A3A6E; margin-bottom: 3px; }
.challenge-sub { font-size: 12px; color: #4A70A8; font-weight: 500; margin-bottom: 14px; }
.xp-row { display: flex; justify-content: space-between; font-size: 11px; font-weight: 700; color: #3060A0; margin-bottom: 5px; }
.xp-track { background: rgba(59, 158, 255, 0.15); border-radius: 10px; height: 10px; overflow: hidden; position: relative; }

.xp-bar {
  height: 100%;
  border-radius: 10px;
  background: linear-gradient(90deg, var(--sky), #74C4FF);
  width: 68%;
  animation: barGrow 1.5s cubic-bezier(0.34, 1.56, 0.64, 1) 1s both;
  position: relative;
  overflow: hidden;
}

.xp-bar::after {
  content: "";
  position: absolute;
  top: 0;
  left: -30%;
  width: 30%;
  height: 100%;
  background: rgba(255, 255, 255, 0.55);
  border-radius: 10px;
  animation: travelShimmer 2.5s ease-in-out 2s infinite;
}

.star-row { display: flex; gap: 5px; margin-top: 10px; }

.star-btn {
  width: 30px;
  height: 30px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.07);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.star-btn:hover { transform: scale(1.3) rotate(10deg); }
.star-btn.earned { background: linear-gradient(135deg, var(--amber), #FFD060); }
.star-btn.earned .star-svg :deep(svg) { color: #6B3A00; fill: currentColor; }
.star-btn:not(.earned) .star-svg :deep(svg) { color: #D0D2E0; fill: none; }

.hydration-card {
  background: linear-gradient(145deg, #EDFFF6, #D8FFED);
  border-radius: 20px;
  padding: 17px;
  border: 1.5px solid rgba(44, 201, 122, 0.2);
  box-shadow: var(--card-shadow);
  position: relative;
  overflow: hidden;
}

.hyd-ring {
  position: absolute;
  bottom: -20px;
  right: -20px;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 10px solid rgba(44, 201, 122, 0.1);
  animation: hydRipple 3s ease-out infinite;
}

.hyd-ring:nth-child(2) { width: 120px; height: 120px; animation: hydRipple 3s ease-out 0.7s infinite; }
@keyframes hydRipple { 0% { transform: scale(0.5); opacity: 1; } 100% { transform: scale(2); opacity: 0; } }

.section-green { color: var(--mint); }
.hydration-title { font-family: "Baloo 2", cursive; font-size: 16px; font-weight: 800; color: #0A4A28; margin-bottom: 3px; }
.hydration-sub { font-size: 11px; color: #3A8060; font-weight: 500; margin-bottom: 11px; }

.hyd-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  position: relative;
  z-index: 1;
  margin-bottom: 6px;
}

.sip-counter {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 9px;
  border-radius: 999px;
  background: linear-gradient(135deg, rgba(59, 158, 255, 0.16), rgba(44, 201, 122, 0.18));
  border: 1.5px solid rgba(44, 201, 122, 0.28);
  color: #0A4A28;
  font-family: "Baloo 2", cursive;
  font-weight: 800;
  font-size: 12px;
  box-shadow: 0 3px 10px rgba(44, 201, 122, 0.16);
}

.sip-counter-emoji { font-size: 12px; line-height: 1; }
.sip-counter-num { font-variant-numeric: tabular-nums; min-width: 14px; text-align: center; }

.drop-grid { display: flex; gap: 6px; flex-wrap: wrap; position: relative; z-index: 1; }
.drop-emoji {
  font-size: 16px;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  filter: drop-shadow(0 1px 2px rgba(11, 60, 36, 0.35));
}

.drop-btn {
  width: 30px;
  height: 30px;
  border-radius: 10px;
  border: 1.5px solid rgba(44, 201, 122, 0.2);
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.drop-btn:hover { transform: scale(1.3) translateY(-5px); box-shadow: 0 6px 16px rgba(44, 201, 122, 0.3); }
.drop-btn .drop-svg :deep(svg) { color: #B0E8CC; }
.drop-btn.filled { background: linear-gradient(135deg, #60EBAC, var(--mint)); border-color: transparent; }
.drop-btn.filled .drop-svg :deep(svg) { color: white; }

.hyd-actions {
  display: flex;
  align-items: stretch;
  gap: 7px;
  margin-top: 8px;
  position: relative;
  z-index: 1;
}

.log-sip-btn {
  flex: 1 1 auto;
  padding: 7px;
  background: white;
  border: 2px dashed rgba(44, 201, 122, 0.4);
  border-radius: 11px;
  font-family: "Baloo 2", cursive;
  font-size: 12px;
  font-weight: 700;
  color: var(--mint);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.log-sip-btn:hover {
  background: rgba(44, 201, 122, 0.1);
  border-style: solid;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(44, 201, 122, 0.2);
}

.log-sip-btn:hover .button-svg :deep(svg) { transform: scale(1.4) rotate(20deg); }

.reset-glass-btn {
  flex: 0 0 auto;
  padding: 7px 11px;
  border-radius: 11px;
  border: 1.5px solid rgba(255, 96, 88, 0.34);
  background: rgba(255, 96, 88, 0.08);
  color: #B7271F;
  font-family: "Baloo 2", cursive;
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s, background 0.25s, opacity 0.2s;
}

.reset-glass-btn:hover {
  background: rgba(255, 96, 88, 0.16);
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(255, 96, 88, 0.22);
}

.reset-glass-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.dark-mode .reset-glass-btn {
  background: rgba(255, 96, 88, 0.18);
  border-color: rgba(255, 126, 113, 0.42);
  color: #FFD7D2;
}

.nav-bar {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--nav-bg);
  border-radius: 30px;
  padding: 10px 16px;
  display: flex;
  gap: 4px;
  box-shadow: 0 12px 40px rgba(24, 25, 43, 0.25);
  z-index: 100;
  animation: navUp 0.7s cubic-bezier(0.22, 1, 0.36, 1) 1s both;
}

@keyframes navUp {
  from { transform: translateX(-50%) translateY(70px); opacity: 0; }
  to { transform: translateX(-50%) translateY(0); opacity: 1; }
}

.nav-item {
  width: 50px;
  height: 50px;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  gap: 2px;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  background: transparent;
  border: 0;
}

.nav-item span {
  font-size: 8px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--nav-text);
  transition: color 0.3s;
}

.nav-item:hover .nav-svg :deep(svg) { color: rgba(255, 255, 255, 0.7); transform: translateY(-3px) scale(1.15); }
.nav-item.active { background: rgba(255, 255, 255, 0.12); }
.nav-item.active .nav-svg :deep(svg) { color: white; transform: translateY(-2px); }
.nav-item.active span { color: rgba(255, 255, 255, 0.6); }

.nav-dot {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 6px;
  height: 6px;
  background: var(--coral);
  border-radius: 50%;
  border: 1.5px solid var(--ink);
  animation: dotBlink 1.5s ease-in-out infinite;
}

#confetti-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  overflow: hidden;
  perspective: 1200px;
  contain: layout paint;
}

.water-fall-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9500;
  overflow: hidden;
  contain: layout paint;
}

.fall-drop {
  --drop-size: 14px;
  --drop-drift: 0px;
  position: absolute;
  top: -40px;
  width: calc(var(--drop-size) * 0.72);
  height: calc(var(--drop-size) * 1.45);
  border-radius: 60% 60% 70% 70%;
  background: linear-gradient(180deg, rgba(225, 246, 255, 0.98) 0%, rgba(110, 201, 255, 0.95) 52%, rgba(40, 153, 255, 0.88) 100%);
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.4),
    0 10px 20px rgba(59, 158, 255, 0.22);
  transform-origin: center top;
  animation: fallDrop linear forwards;
}

.fall-drop::before {
  content: "";
  position: absolute;
  left: 50%;
  bottom: calc(100% - 1px);
  transform: translateX(-50%);
  width: calc(var(--drop-size) * 0.34);
  height: calc(var(--drop-size) * 0.5);
  border-radius: 100% 100% 0 0;
  background: linear-gradient(180deg, rgba(225, 246, 255, 0.95), rgba(110, 201, 255, 0.8));
}

@keyframes fallDrop {
  0% {
    transform: translate3d(0, -8vh, 0) scale(0.7) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.95;
  }
  72% {
    transform: translate3d(var(--drop-drift), 74vh, 0) scale(1) rotate(10deg);
    opacity: 0.96;
  }
  86% {
    transform: translate3d(calc(var(--drop-drift) * 0.8), 84vh, 0) scale(1.12, 0.84) rotate(-6deg);
    opacity: 0.92;
  }
  100% {
    transform: translate3d(calc(var(--drop-drift) * 0.7), 92vh, 0) scale(1.3, 0.44) rotate(0deg);
    opacity: 0;
  }
}

.conf-piece {
  position: absolute;
  border-radius: 2px;
  animation: confFall linear forwards;
  opacity: 0;
}

.cele-ribbon {
  --ribbon-start: #FF7A72;
  --ribbon-end: #FFB96B;
  position: absolute;
  top: 0;
  left: 0;
  border-radius: 999px 999px 20px 20px;
  transform-style: preserve-3d;
  will-change: transform, opacity;
  filter: drop-shadow(0 18px 22px rgba(16, 24, 40, 0.2));
}

.cele-ribbon::before {
  content: "";
  position: absolute;
  inset: 0 0 16px;
  border-radius: inherit;
  background:
    linear-gradient(135deg, var(--ribbon-start), var(--ribbon-end)),
    linear-gradient(180deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0));
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.4),
    inset 4px 0 9px rgba(255, 255, 255, 0.18),
    inset -5px 0 12px rgba(15, 23, 42, 0.16);
}

.cele-ribbon::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 52%;
  height: 22px;
  transform: translateX(-50%);
  background:
    linear-gradient(135deg, transparent 48%, rgba(255, 255, 255, 0.1) 49%, rgba(255, 255, 255, 0.1) 51%, transparent 52%),
    linear-gradient(135deg, var(--ribbon-start), var(--ribbon-end));
  clip-path: polygon(0 0, 100% 0, 70% 100%, 50% 68%, 30% 100%);
  filter: brightness(1.02);
}

.cele-ribbon > span {
  display: none;
}

@keyframes confFall {
  0% { transform: translateY(-10px) rotate(0); opacity: 1; }
  80% { opacity: 1; }
  100% { transform: translateY(100vh) rotate(800deg); opacity: 0; }
}

.rip {
  position: absolute;
  border-radius: 50%;
  transform: scale(0);
  animation: ripOut 0.6s ease-out forwards;
  background: rgba(255, 255, 255, 0.35);
  pointer-events: none;
}

@keyframes ripOut { to { transform: scale(4); opacity: 0; } }

.svg-holder { display: inline-flex; }
.avatar-svg :deep(svg) { width: 26px; height: 26px; color: #D97A00; }
.mini-svg :deep(svg) { width: 12px; height: 12px; }
.stat-svg :deep(svg) { width: 20px; height: 20px; }
.section-svg :deep(svg),
.tag-svg :deep(svg) { width: 10px; height: 10px; }
.mission-svg :deep(svg) { width: 24px; height: 24px; color: var(--coral); }
.button-svg :deep(svg) { width: 16px; height: 16px; transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.win-svg :deep(svg) { width: 19px; height: 19px; }
.check-svg :deep(svg) { width: 12px; height: 12px; color: white; }
.link-svg :deep(svg) { width: 12px; height: 12px; }
.game-svg :deep(svg) { width: 24px; height: 24px; color: var(--gc); }
.star-svg :deep(svg) { width: 14px; height: 14px; }
.drop-svg :deep(svg) { width: 14px; height: 14px; transition: color 0.3s; }
.nav-svg :deep(svg) {
  width: 20px;
  height: 20px;
  color: rgba(255, 255, 255, 0.38);
  transition: color 0.3s, transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.dark-mode .greeting-chip {
  background: rgba(44, 201, 122, 0.12);
  border-color: rgba(44, 201, 122, 0.26);
}

.dark-mode .header-sub,
.dark-mode .section-label,
.dark-mode .stat-label,
.dark-mode .stat-sub,
.dark-mode .mission-desc,
.dark-mode .game-desc,
.dark-mode .win-sub,
.dark-mode .meal-sub,
.dark-mode .challenge-sub,
.dark-mode .hydration-sub,
.dark-mode .boost-sub {
  color: var(--ink2);
}

.dark-mode .date-tag,
.dark-mode .time-tag {
  background: rgba(255, 255, 255, 0.04);
  color: var(--ink2);
}

.dark-mode .streak-tag {
  background: linear-gradient(135deg, rgba(255, 176, 32, 0.18), rgba(255, 126, 179, 0.18));
  border-color: rgba(255, 176, 32, 0.3);
  color: #FFD98E;
}

.dark-mode .meal-day-panel {
  border-color: rgba(255, 184, 108, 0.16);
  background: linear-gradient(165deg, rgba(26, 30, 52, 0.96) 0%, rgba(18, 22, 44, 0.94) 55%, rgba(22, 26, 56, 0.92) 100%);
  box-shadow:
    0 14px 42px rgba(0, 0, 0, 0.35),
    inset 0 1px 0 rgba(255, 255, 255, 0.06);
}

.dark-mode .meal-day-head {
  border-bottom-color: rgba(255, 255, 255, 0.09);
}

.dark-mode .meal-day-svg :deep(svg) {
  color: #ffd98e;
}

.dark-mode .meal-day-sub {
  color: var(--muted);
}

.dark-mode .boost-pill::before {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.12) 0%, transparent 50%);
  opacity: 1;
}

.dark-mode .boost-icon {
  background: rgba(255, 255, 255, 0.1);
  box-shadow:
    0 2px 10px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.12);
}

.dark-mode .boost-action {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.14);
  color: rgba(236, 240, 255, 0.88);
}

.dark-mode .boost-pill--done .boost-action {
  background: rgba(44, 201, 122, 0.22);
  border-color: rgba(96, 235, 172, 0.38);
  color: #b8ffd9;
}

.dark-mode .boost-pill--done .boost-sub {
  color: rgba(152, 242, 191, 0.92);
}

.dark-mode .boost-pill,
.dark-mode .stat-card,
.dark-mode .mission-card,
.dark-mode .wins-card,
.dark-mode .game-card {
  backdrop-filter: blur(18px);
}

.dark-mode .boost-coral {
  background: linear-gradient(145deg, rgba(53, 25, 38, 0.95), rgba(35, 29, 59, 0.92));
}

.dark-mode .boost-sky {
  background: linear-gradient(145deg, rgba(15, 41, 78, 0.95), rgba(13, 57, 74, 0.92));
}

.dark-mode .boost-violet {
  background: linear-gradient(145deg, rgba(52, 29, 90, 0.95), rgba(73, 32, 73, 0.92));
}

.dark-mode .meal-toast {
  background: linear-gradient(135deg, rgba(11, 87, 53, 0.98), rgba(28, 143, 91, 0.96));
  border-color: rgba(96, 235, 172, 0.22);
  color: #d7ffe8;
}

.dark-mode .main-site-link {
  background: linear-gradient(135deg, rgba(20, 94, 58, 0.9), rgba(16, 79, 79, 0.88));
  border-color: rgba(96, 235, 172, 0.22);
  color: #e7fff1;
}

.dark-mode .boost-label,
.dark-mode .meal-day-title,
.dark-mode .stat-value,
.dark-mode .mission-title,
.dark-mode .win-title,
.dark-mode .meal-title,
.dark-mode .game-name,
.dark-mode .section-heading,
.dark-mode .challenge-title,
.dark-mode .hydration-title {
  color: var(--ink);
}

.dark-mode .sc-steps {
  background: linear-gradient(145deg, rgba(65, 26, 34, 0.96), rgba(27, 22, 45, 0.96));
}

.dark-mode .sc-water {
  background: linear-gradient(145deg, rgba(15, 40, 72, 0.96), rgba(17, 25, 49, 0.96));
}

.dark-mode .sc-sleep {
  background: linear-gradient(145deg, rgba(45, 28, 82, 0.96), rgba(23, 24, 52, 0.96));
}

.dark-mode .sc-mood {
  background: linear-gradient(145deg, rgba(15, 60, 46, 0.96), rgba(16, 33, 46, 0.96));
}

.dark-mode .prog-track,
.dark-mode .xp-track {
  background: rgba(255, 255, 255, 0.08);
}

.dark-mode .tag,
.dark-mode .win-item {
  background: rgba(255, 255, 255, 0.04);
  color: var(--ink2);
}

.dark-mode .tag-svg :deep(svg),
.dark-mode .section-svg :deep(svg),
.dark-mode .mini-svg :deep(svg),
.dark-mode .win-svg :deep(svg),
.dark-mode .link-svg :deep(svg) {
  color: var(--ink);
}

.dark-mode .avatar-svg :deep(svg) {
  color: #FFD98E;
}

.dark-mode .stat-svg :deep(svg) {
  color: currentColor;
}

.dark-mode .sc-steps .stat-icon {
  background: rgba(255, 96, 88, 0.16);
  color: #FFB8B2;
}

.dark-mode .sc-water .stat-icon {
  background: rgba(59, 158, 255, 0.18);
  color: #9FD2FF;
}

.dark-mode .sc-sleep .stat-icon {
  background: rgba(155, 114, 255, 0.2);
  color: #D2B7FF;
}

.dark-mode .sc-mood .stat-icon {
  background: rgba(44, 201, 122, 0.18);
  color: #98F2BF;
}

.dark-mode .tag:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.2);
  color: #FFFFFF;
}

.dark-mode .mission-card {
  background: linear-gradient(145deg, rgba(41, 23, 34, 0.98), rgba(21, 26, 53, 0.96));
}

.dark-mode .wins-card {
  background: linear-gradient(145deg, rgba(22, 28, 53, 0.98), rgba(20, 22, 43, 0.96));
}

.dark-mode .meal-banner {
  background: linear-gradient(145deg, rgba(61, 40, 13, 0.94), rgba(40, 24, 8, 0.96));
  border-color: rgba(255, 208, 96, 0.24);
}

.dark-mode .meal-text .section-label,
.dark-mode .meal-title,
.dark-mode .meal-sub {
  color: #FFE0A1;
}

.dark-mode .meal-btn {
  color: #2F1800;
}

.dark-mode .challenge-card {
  background: linear-gradient(145deg, rgba(15, 39, 74, 0.98), rgba(19, 24, 54, 0.96));
  border-color: rgba(116, 196, 255, 0.2);
}

.dark-mode .challenge-title,
.dark-mode .challenge-sub,
.dark-mode .xp-row {
  color: #D8E8FF;
}

.dark-mode .button-svg :deep(svg),
.dark-mode .drop-svg :deep(svg),
.dark-mode .star-svg :deep(svg) {
  color: currentColor;
}

.dark-mode .hydration-card {
  background: linear-gradient(145deg, rgba(11, 66, 43, 0.96), rgba(10, 29, 36, 0.96));
  border-color: rgba(96, 235, 172, 0.24);
}

.dark-mode .hydration-title,
.dark-mode .hydration-sub {
  color: #D7FFE8;
}

.dark-mode .sip-counter {
  background: linear-gradient(135deg, rgba(59, 158, 255, 0.22), rgba(44, 201, 122, 0.24));
  border-color: rgba(96, 235, 172, 0.32);
  color: #E7FFF1;
  box-shadow: 0 6px 18px rgba(3, 24, 14, 0.32);
}

.dark-mode .drop-btn,
.dark-mode .star-btn,
.dark-mode .log-sip-btn {
  background: rgba(255, 255, 255, 0.06);
  color: var(--ink);
}

.dark-mode .drop-btn .drop-svg :deep(svg) {
  color: rgba(215, 255, 232, 0.68);
}

.dark-mode .drop-btn.filled {
  color: #08150F;
}

.dark-mode .drop-btn.filled .drop-svg :deep(svg) {
  color: #FFFFFF;
}

.dark-mode .star-btn.earned {
  color: #3A2300;
}

.dark-mode .star-btn:not(.earned) .star-svg :deep(svg) {
  color: rgba(220, 226, 255, 0.42);
}

.dark-mode .log-sip-btn {
  border-color: rgba(96, 235, 172, 0.32);
}

.dark-mode .active-badge {
  color: #FFFFFF;
}

.dark-mode .nav-svg :deep(svg) {
  color: rgba(255, 255, 255, 0.62);
}

.dark-mode .nav-item.active {
  background: rgba(255, 255, 255, 0.14);
}

/* Lite / reduced-motion & Save-Data: drop heavy decorations & blur cost */
.kids-html-dashboard--lite .dash-blobs,
.kids-html-dashboard--lite .dash-sparkles {
  display: none !important;
}

.kids-html-dashboard--lite .blob {
  animation: none !important;
}

.kids-html-dashboard--lite .sky-cloud {
  animation: none !important;
}

.kids-html-dashboard--lite .spark {
  animation: none !important;
}

.kids-html-dashboard--lite .avatar-zone {
  animation: none !important;
}

.kids-html-dashboard--lite .orbit-ring {
  animation: none !important;
}

.kids-html-dashboard--lite .sun-core,
.kids-html-dashboard--lite .sun-halo,
.kids-html-dashboard--lite .sun-ring,
.kids-html-dashboard--lite .moon-core,
.kids-html-dashboard--lite .moon-halo {
  animation: none !important;
}

.kids-html-dashboard--lite .sky-star {
  animation: none !important;
}

.kids-html-dashboard--lite .sky-shoot {
  animation: none !important;
}

.kids-html-dashboard--lite .fall-drop {
  animation: none !important;
  opacity: 0 !important;
}

.kids-html-dashboard--lite .header,
.kids-html-dashboard--lite .boost-pill,
.kids-html-dashboard--lite .games-tiles,
.kids-html-dashboard--lite .hydration-card {
  backdrop-filter: none !important;
}

@media (max-width: 740px) {
  .boost-strip { grid-template-columns: 1fr; }
  .stats-row { grid-template-columns: 1fr 1fr; }
  .main-grid, .bottom-row, .games-row { grid-template-columns: 1fr; gap: 10px; }
  .meal-float { display: none; }
  .meal-banner { flex-direction: column; gap: 14px; align-items: flex-start; }
  .nav-bar { width: calc(100% - 32px); justify-content: space-around; }
  .header { align-items: flex-start; flex-wrap: wrap; gap: 14px; }
  .header-right { width: 100%; max-width: none; justify-content: flex-start; }
}

:global(.conf-piece) {
  position: absolute;
  border-radius: 2px;
  animation: confFall linear forwards;
  opacity: 0;
  pointer-events: none;
}

:global(.cele-ribbon) {
  --ribbon-start: #FF7A72;
  --ribbon-end: #FFB96B;
  position: absolute;
  top: 0;
  left: 0;
  border-radius: 999px 999px 20px 20px;
  transform-style: preserve-3d;
  will-change: transform, opacity;
  filter: drop-shadow(0 18px 22px rgba(16, 24, 40, 0.2));
  pointer-events: none;
}

:global(.cele-ribbon::before) {
  content: "";
  position: absolute;
  inset: 0 0 16px;
  border-radius: inherit;
  background:
    linear-gradient(135deg, var(--ribbon-start), var(--ribbon-end)),
    linear-gradient(180deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0));
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.4),
    inset 4px 0 9px rgba(255, 255, 255, 0.18),
    inset -5px 0 12px rgba(15, 23, 42, 0.16);
}

:global(.cele-ribbon::after) {
  content: "";
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 52%;
  height: 22px;
  transform: translateX(-50%);
  background:
    linear-gradient(135deg, transparent 48%, rgba(255, 255, 255, 0.1) 49%, rgba(255, 255, 255, 0.1) 51%, transparent 52%),
    linear-gradient(135deg, var(--ribbon-start), var(--ribbon-end));
  clip-path: polygon(0 0, 100% 0, 70% 100%, 50% 68%, 30% 100%);
  filter: brightness(1.02);
}

:global(.cele-ribbon > span) {
  display: none;
}

:global(.rip) {
  position: absolute;
  border-radius: 50%;
  transform: scale(0);
  animation: ripOut 0.6s ease-out forwards;
  background: rgba(255, 255, 255, 0.35);
  pointer-events: none;
}
:global(#confetti-layer) {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  overflow: hidden;
  perspective: 1200px;
  contain: layout paint;
}
.kids-html-dashboard {
  --kids-font-scale: var(--hk-font-scale, 1);
}
.header-text h1 {
  font-size: calc(28px * var(--kids-font-scale));
}

.header-sub {
  font-size: calc(14px * var(--kids-font-scale));
}

.main-site-link,
.date-tag,
.time-tag,
.streak-tag {
  font-size: calc(13px * var(--kids-font-scale));
}

.meal-day-title {
  font-size: calc(24px * var(--kids-font-scale));
}

.meal-day-sub {
  font-size: calc(14px * var(--kids-font-scale));
}

.boost-label {
  font-size: calc(16px * var(--kids-font-scale));
}

.boost-sub {
  font-size: calc(13px * var(--kids-font-scale));
}

.boost-action {
  font-size: calc(13px * var(--kids-font-scale));
}

.section-label {
  font-size: calc(14px * var(--kids-font-scale));
}

.game-tile-copy strong {
  font-size: calc(17px * var(--kids-font-scale));
}

.game-tile-copy span {
  font-size: calc(13px * var(--kids-font-scale));
}

.hydration-title {
  font-size: calc(24px * var(--kids-font-scale));
}

.hydration-sub {
  font-size: calc(14px * var(--kids-font-scale));
}

.log-sip-btn,
.reset-glass-btn {
  font-size: calc(14px * var(--kids-font-scale));
}
</style>