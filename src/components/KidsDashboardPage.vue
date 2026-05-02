<template>
  <div class="kids-html-dashboard" :class="{ 'dark-mode': isDarkMode }">
    <div id="confetti-layer" ref="confettiLayer"></div>
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

    <div class="dash">
      <header class="header">
        <div class="avatar-zone">
          <div class="avatar">
            <span class="svg-holder avatar-svg" v-html="icons.avatar"></span>
          </div>
          <div class="orbit-ring"><div class="orbit-dot"></div></div>
        </div>

        <div class="header-text">
          <div class="greeting-chip">
            <div class="chip-dot"></div>
            Healthy Kids Dashboard
          </div>
          <h1>Hey, <em>Alex!</em> Ready to play?</h1>
          <div class="header-sub">Pick a game, collect healthy wins &amp; keep your streak!</div>
        </div>

        <div class="header-right">
          <RouterLink
            to="/parent-dashboard"
            class="parent-dash-link"
            aria-label="Open parent dashboard home"
          >
            <span class="svg-holder mini-svg parent-door-svg" v-html="icons.parentDoor"></span>
            <span>Parents home</span>
          </RouterLink>
          <button
            type="button"
            class="theme-toggle"
            :aria-pressed="isDarkMode"
            @click="toggleDarkMode"
          >
            <span class="svg-holder mini-svg" v-html="isDarkMode ? icons.sun : icons.moon"></span>
            {{ isDarkMode ? "Light glow" : "Dark sky" }}
          </button>
          <div class="date-tag">
            <span class="svg-holder mini-svg" v-html="icons.calendar"></span>
            {{ todayLabel }}
          </div>
          <button type="button" class="streak-tag" @click="celebrateStreak">
            <span class="svg-holder mini-svg flame-icon" v-html="icons.flame"></span>
            5 day streak
          </button>
        </div>
      </header>

      <section class="boost-strip" aria-label="Daily power ups">
        <article
          v-for="boost in powerUps"
          :key="boost.label"
          class="boost-pill"
          :class="boost.tone"
          @click="handleBoostClick(boost, $event)"
        >
          <div class="boost-icon">
            <span class="svg-holder section-svg" v-html="boost.icon"></span>
          </div>
          <div>
            <div class="boost-label">{{ boost.label }}</div>
            <div class="boost-sub">{{ boost.helper }}</div>
          </div>
          <strong>{{ boost.value }}</strong>
        </article>
      </section>

      <section class="stats-row" aria-label="Health summary">
        <article
          v-for="stat in stats"
          :key="stat.label"
          class="stat-card"
          :class="stat.theme"
          @click="openStatsPage($event)"
        >
          <div class="stat-icon">
            <span class="svg-holder stat-svg" v-html="stat.icon"></span>
          </div>
          <div class="stat-label">{{ stat.label }}</div>
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-sub">{{ stat.helper }}</div>
          <div class="prog-track"><div class="prog-fill" :style="{ width: stat.progress }"></div></div>
        </article>
      </section>

      <div class="main-grid">
        <div class="mission-card" @click="openBubbleMission">
          <div class="section-label">
            <span class="svg-holder section-svg" v-html="icons.target"></span>
            Today's Mission
          </div>

          <div class="mission-header">
            <div class="mission-icon-wrap">
              <span class="svg-holder mission-svg" v-html="icons.bubbleMission"></span>
            </div>
            <div class="mission-title">Healthy Bubble Game</div>
          </div>

          <div class="mission-desc">
            Pop the target health words before they self-pop. Fast fingers win!
          </div>

          <div class="tag-row">
            <span v-for="tag in missionTags" :key="tag.label" class="tag">
              <span class="svg-holder tag-svg" v-html="tag.icon"></span>
              {{ tag.label }}
            </span>
          </div>

          <button type="button" class="play-btn" @click="playNow">
            <span class="svg-holder button-svg" v-html="icons.play"></span>
            Play Now
            <span class="svg-holder button-svg" v-html="icons.arrowRight"></span>
          </button>
        </div>

        <div class="wins-card" @click="openWinsPage">
          <div class="section-label">
            <span class="svg-holder section-svg" v-html="icons.trophy"></span>
            Healthy Wins
          </div>

          <div
            v-for="(win, index) in wins"
            :key="win.label"
            class="win-item"
          >
            <div class="win-icon" :class="`win-icon-${index + 1}`">
              <span class="svg-holder win-svg" v-html="win.icon"></span>
            </div>
            <div>
              <div class="win-title">{{ win.label }}</div>
              <div class="win-sub">{{ win.helper }}</div>
            </div>
            <div class="win-check">
              <span class="svg-holder check-svg" v-html="icons.check"></span>
            </div>
          </div>
        </div>

        <div class="meal-banner" @click="openMealsPage">
          <div class="meal-float">
            <span class="svg-holder float-svg" v-html="icons.meal1"></span>
            <span class="svg-holder float-svg" v-html="icons.meal2"></span>
            <span class="svg-holder float-svg" v-html="icons.meal3"></span>
            <span class="svg-holder float-svg" v-html="icons.meal4"></span>
          </div>

          <div class="meal-text">
            <div class="section-label">
              <span class="svg-holder section-svg" v-html="icons.meal1"></span>
              Meal Planner
            </div>
            <div class="meal-title">Build a bright food day!</div>
            <div class="meal-sub">
              Tap to see your playful breakfast, lunch, snack &amp; dinner plan.
            </div>
          </div>

          <button type="button" class="meal-btn" @click="handleMealPlannerClick">
            <span class="svg-holder button-svg" v-html="icons.grid"></span>
            Open meal planner
          </button>
        </div>
      </div>

      <section class="game-section">
        <div class="section-header">
          <div>
            <div class="section-label">
              <span class="svg-holder section-svg" v-html="icons.gamepad"></span>
              Game Corner
            </div>
            <div class="section-heading">Choose your adventure!</div>
          </div>

          <button type="button" class="see-all" @click="goToGameZone('bubble')">
            See all
            <span class="svg-holder link-svg" v-html="icons.arrowRight"></span>
          </button>
        </div>

        <div class="games-row">
          <button
            v-for="game in gameCards"
            :key="game.id"
            type="button"
            class="game-card"
            @click="goToGameZone(game.id, $event)"
          >
            <div v-if="game.playing" class="active-badge">Playing</div>
            <div class="game-icon">
              <span class="svg-holder game-svg" v-html="game.icon"></span>
            </div>
            <div class="game-name">{{ game.name }}</div>
            <div class="game-desc">{{ game.description }}</div>
          </button>
        </div>
      </section>

      <div class="bottom-row">
        <div class="challenge-card" @click="openWinsPage">
          <div class="section-label section-blue">
            <span class="svg-holder section-svg" v-html="icons.star"></span>
            Weekly Challenge
          </div>
          <div class="challenge-title">Veggie Champion</div>
          <div class="challenge-sub">Eat 5 different veggies this week!</div>
          <div class="xp-row"><span>XP Progress</span><span>340 / 500 XP</span></div>
          <div class="xp-track"><div class="xp-bar"></div></div>

          <div class="star-row">
            <button
              v-for="(earned, index) in stars"
              :key="`star-${index}`"
              type="button"
              class="star-btn"
              :class="{ earned }"
              @click.stop="toggleStar(index, $event)"
            >
              <span class="svg-holder star-svg" v-html="icons.star"></span>
            </button>
          </div>
        </div>

        <div ref="hydrationCard" class="hydration-card" @click="openStatsPage">
          <div class="hyd-ring"></div>
          <div class="hyd-ring"></div>

          <div class="section-label section-green">
            <span class="svg-holder section-svg" v-html="icons.drop"></span>
            Hydration Tracker
          </div>
          <div class="hydration-title">Stay super hydrated!</div>
          <div class="hydration-sub">Tap a drop to log your sip</div>

          <div class="drop-grid">
            <button
              v-for="(filled, index) in drops"
              :key="`drop-${index}`"
              type="button"
              class="drop-btn"
              :class="{ filled }"
              :title="`Sip ${index + 1}`"
              @click.stop="toggleDrop(index, $event)"
            >
              <span class="svg-holder drop-svg" v-html="icons.drop"></span>
            </button>
          </div>

          <button type="button" class="log-sip-btn" @click.stop="logSip">
            <span class="svg-holder button-svg" v-html="icons.plusCircle"></span>
            Log another sip
          </button>
        </div>
      </div>
    </div>

    <KidsBottomNav />
  </div>
</template>

<script setup>
import { onBeforeUnmount, ref } from "vue"
import { RouterLink, useRouter } from "vue-router"
import KidsBottomNav from "./kids/KidsBottomNav.vue"
import { useKidsTheme } from "../composables/useKidsTheme.js"

const router = useRouter()
const { isDarkMode, toggleDarkMode } = useKidsTheme()

const confettiLayer = ref(null)
const hydrationCard = ref(null)
const stars = ref([true, true, true, false, false])
const drops = ref([true, true, true, true, true, false, false, false])
const fallingDrops = ref([])

let nextFallingDropId = 1
const activeRibbons = []

let ribbonFrameId = 0

const todayLabel = new Intl.DateTimeFormat("en-AU", {
  weekday: "short",
  day: "numeric",
  month: "short",
}).format(new Date())

const icons = {
  avatar: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>`,
  parentDoor: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M13 21h8v-9h-8z"/><path d="M3 21V4a1 1 0 0 1 1-1h7l5 5v13"/><circle cx="16.5" cy="13.5" r="1" fill="currentColor"/></svg>`,
  calendar: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>`,
  flame: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2c0 4-4 6-4 10a4 4 0 0 0 8 0c0-4-4-6-4-10z"/><path d="M12 12c0 2-2 3-2 5a2 2 0 0 0 4 0c0-2-2-3-2-5z"/></svg>`,
  target: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`,
  bubbleMission: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2"/></svg>`,
  play: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>`,
  arrowRight: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`,
  trophy: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>`,
  check: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`,
  meal1: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>`,
  meal2: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 0 1 10 10"/><path d="M12 6v6l4 2"/><circle cx="12" cy="12" r="2"/></svg>`,
  meal3: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/></svg>`,
  meal4: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>`,
  grid: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>`,
  gamepad: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M12 12h.01"/><path d="M7 12h.01"/><path d="M17 12h.01"/></svg>`,
  bubbleCard: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1" fill="currentColor"/></svg>`,
  explorerCard: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>`,
  smashCard: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
  star: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`,
  drop: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L5 12a7 7 0 1 0 14 0L12 2z"/></svg>`,
  plusCircle: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>`,
  moon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>`,
  sun: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2.2M12 19.8V22M4.9 4.9l1.5 1.5M17.6 17.6l1.5 1.5M2 12h2.2M19.8 12H22M4.9 19.1l1.5-1.5M17.6 6.4l1.5-1.5"/></svg>`,
  steps: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 4v4l3 3-2 5-4-2-3 4H4"/><path d="M20 12v4l-2 4"/></svg>`,
  sleep: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`,
  smile: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>`,
  timer: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 0 1 10 10"/><path d="M12 6v6l4 2"/><circle cx="12" cy="12" r="2"/></svg>`,
  bolt: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
  message: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`,
}

const stats = [
  { label: "Steps", value: "7,240", helper: "Move goal 72%", progress: "72%", theme: "sc-steps", icon: icons.steps },
  { label: "Water", value: "5 / 8", helper: "Three more sips!", progress: "62%", theme: "sc-water", icon: icons.drop },
  { label: "Sleep", value: "8.5h", helper: "Great bedtime win", progress: "90%", theme: "sc-sleep", icon: icons.sleep },
  { label: "Mood", value: "Happy", helper: "Energy is high!", progress: "85%", theme: "sc-mood", icon: icons.smile },
]

const missionTags = [
  { label: "Color pop", icon: icons.target },
  { label: "Quick taps", icon: icons.bolt },
  { label: "Healthy words", icon: icons.message },
]

const wins = [
  { label: "3 healthy bites", helper: "Fruit and veggie streak", icon: icons.timer },
  { label: "Water power", helper: "Sipping through the day", icon: icons.drop },
  { label: "Sleep star", helper: "Strong bedtime routine", icon: icons.sleep },
]

const powerUps = [
  { label: "Rainbow bites", helper: "Fruit mission streak", value: "3 / 5", tone: "boost-coral", icon: icons.star },
  { label: "Power splash", helper: "Hydration glow-up", value: "+80 XP", tone: "boost-sky", icon: icons.drop },
  { label: "Dream spark", helper: "Lights out on time", value: "8.5h", tone: "boost-violet", icon: icons.sleep },
]

const gameCards = [
  {
    id: "bubble",
    name: "Bubble Game",
    description: "Pop target health words before they self-pop",
    icon: icons.bubbleCard,
    playing: true,
  },
  {
    id: "explorer",
    name: "Explorer Game",
    description: "Pick matching healthy habit pairs",
    icon: icons.explorerCard,
    playing: false,
  },
  {
    id: "smash",
    name: "Smash Game",
    description: "Drag and wiggle to build power",
    icon: icons.smashCard,
    playing: false,
  },
]

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

function safeRipple(event) {
  if (event && typeof event === "object" && "currentTarget" in event) {
    ripple(event)
  }
}

function spawnConfetti(count, originRect) {
  const layer = confettiLayer.value
  if (!layer) return

  const colors = ["#FF6058", "#3B9EFF", "#2CC97A", "#FFB020", "#9B72FF", "#FF7EB3", "#1EC8C8", "#FFDD57"]

  for (let index = 0; index < count; index += 1) {
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
  const layer = confettiLayer.value
  if (!layer) return

  const width = window.innerWidth
  const height = window.innerHeight
  const now = performance.now()
  const centerX = options.originRect
    ? options.originRect.left + options.originRect.width / 2
    : width / 2
  const spread = options.originRect
    ? Math.max(width * 0.42, options.originRect.width * 10)
    : width * 1.1
  const palette = [
    ["#FF7A72", "#FFB96B"],
    ["#51B7FF", "#7CF1FF"],
    ["#8E7CFF", "#D4A8FF"],
    ["#54E69F", "#A8FFD4"],
    ["#FF8BC2", "#FFD36F"],
  ]

  for (let index = 0; index < count; index += 1) {
    const ribbon = document.createElement("div")
    ribbon.className = "cele-ribbon"

    const [colorStart, colorEnd] = palette[index % palette.length]
    const ribbonWidth = randomBetween(16, 26)
    const ribbonHeight = randomBetween(180, 320)
    ribbon.style.width = `${ribbonWidth}px`
    ribbon.style.height = `${ribbonHeight}px`
    ribbon.style.setProperty("--ribbon-start", colorStart)
    ribbon.style.setProperty("--ribbon-end", colorEnd)
    ribbon.style.opacity = "0"

    layer.appendChild(ribbon)

    activeRibbons.push({
      element: ribbon,
      x: Math.max(-80, Math.min(width + 40, centerX - spread / 2 + Math.random() * spread)),
      y: randomBetween(-height * 0.7, -ribbonHeight - 80),
      vx: randomBetween(-55, 55),
      vy: randomBetween(210, 320),
      gravity: randomBetween(360, 540),
      rotationZ: randomBetween(-30, 30),
      spin: randomBetween(-120, 120),
      swayAmplitude: randomBetween(22, 56),
      swayFrequency: randomBetween(1.9, 3.6),
      flutterX: randomBetween(38, 84),
      flutterY: randomBetween(58, 132),
      flutterSpeed: randomBetween(6.5, 9.8),
      phase: randomBetween(0, Math.PI * 2),
      fadeStart: height * randomBetween(0.8, 0.92),
      maxY: height + 260,
      height: ribbonHeight,
      age: 0,
      startAt: now + index * randomBetween(22, 46),
      isActive: false,
    })
  }

  startRibbonSimulation()
}

function launchRibbonCelebration(count, originElement) {
  const originRect = originElement instanceof HTMLElement ? originElement.getBoundingClientRect() : null
  if (originRect) {
    spawnConfetti(Math.max(12, Math.round(count * 0.25)), originRect)
  }
  spawnRibbonRain(count, { originRect })
}

function fireConfetti() {
  spawnConfetti(70)
}

function celebrateStreak(event) {
  ripple(event)
  launchRibbonCelebration(34, event.currentTarget)
}

function miniConfetti(element) {
  if (!(element instanceof HTMLElement)) return
  spawnConfetti(18, element.getBoundingClientRect())
}

function spawnWaterDrops(sourceElement, count = 16) {
  const origin = sourceElement instanceof HTMLElement ? sourceElement : hydrationCard.value
  const rect = origin?.getBoundingClientRect?.()
  if (!rect) return

  const created = Array.from({ length: count }, (_, index) => ({
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

function toggleStar(index, event) {
  stars.value[index] = !stars.value[index]
  if (stars.value[index]) {
    miniConfetti(event.currentTarget)
    launchRibbonCelebration(22, event.currentTarget)
  }
}

function toggleDrop(index, event) {
  drops.value[index] = !drops.value[index]
  if (drops.value[index]) {
    spawnWaterDrops(hydrationCard.value, 14)
    miniConfetti(event.currentTarget)
  }
}

function logSip(event) {
  const nextIndex = drops.value.findIndex(filled => !filled)
  if (nextIndex !== -1) {
    drops.value[nextIndex] = true
    spawnWaterDrops(hydrationCard.value, 18)
    miniConfetti(event.currentTarget)
  }
}

function goToGameZone(gameId, event) {
  if (event) {
    ripple(event)
  }
  router.push({ path: "/kids-game-zone", query: gameId ? { game: gameId } : {} })
}

function openBubbleMission(event) {
  goToGameZone("bubble", event)
}

function openMealsPage(event) {
  safeRipple(event)
  router.push("/kids-meals")
}

function openStatsPage(event) {
  safeRipple(event)
  router.push("/kids-stats")
}

function openWinsPage(event) {
  safeRipple(event)
  router.push("/kids-wins")
}

function handleBoostClick(boost, event) {
  if (boost.tone === "boost-sky") {
    openStatsPage(event)
    return
  }

  if (boost.tone === "boost-coral") {
    openWinsPage(event)
    return
  }

  if (boost.tone === "boost-violet") {
    openStatsPage(event)
    return
  }

  safeRipple(event)
}

function playNow(event) {
  ripple(event)
  fireConfetti()
  router.push({ path: "/kids-game-zone", query: { game: "bubble" } })
}

function handleMealPlannerClick(event) {
  ripple(event)
  router.push("/kids-meals")
}

onBeforeUnmount(() => {
  if (ribbonFrameId) {
    window.cancelAnimationFrame(ribbonFrameId)
    ribbonFrameId = 0
  }

  for (const ribbon of activeRibbons) {
    ribbon.element.remove()
  }

  activeRibbons.length = 0
})
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap");

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

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
  padding-bottom: 88px;
  position: relative;
}

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

.dash {
  position: relative;
  z-index: 1;
  max-width: 980px;
  margin: 0 auto;
  padding: 20px 16px 40px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--surface);
  border-radius: 26px;
  padding: 18px 22px;
  margin-bottom: 18px;
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

.avatar-zone { position: relative; cursor: pointer; flex-shrink: 0; }

.avatar {
  width: 58px;
  height: 58px;
  background: linear-gradient(145deg, #FFE4C8, #FFCBA4);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 18px rgba(255, 176, 32, 0.3);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.avatar:hover { transform: rotate(-8deg) scale(1.1); }

.orbit-ring {
  position: absolute;
  inset: -8px;
  border-radius: 26px;
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

.header-text { flex: 1; margin-left: 14px; }

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
  font-size: 24px;
  font-weight: 800;
  color: var(--ink);
  line-height: 1.1;
  animation: textReveal 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.2s both;
}

@keyframes textReveal { from { clip-path: inset(0 100% 0 0); } to { clip-path: inset(0 0% 0 0); } }

.header-text h1 em { font-style: normal; color: var(--coral); }
.header-sub { font-size: 13px; color: var(--muted); font-weight: 500; margin-top: 2px; }

.header-right { display: flex; flex-direction: column; align-items: flex-end; gap: 7px; }

.parent-dash-link {
  text-decoration: none;
  background: linear-gradient(135deg, rgba(44, 201, 122, 0.2), rgba(59, 158, 255, 0.16));
  border: 1.5px solid rgba(44, 140, 112, 0.32);
  border-radius: 999px;
  padding: 7px 12px;
  font-size: 12px;
  font-weight: 700;
  color: var(--ink);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 6px 16px rgba(34, 112, 94, 0.12);
}

.parent-dash-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 18px rgba(34, 112, 94, 0.18);
}

.parent-door-svg {
  width: 15px;
  height: 15px;
}

.dark-mode .parent-dash-link {
  background: linear-gradient(135deg, rgba(44, 201, 122, 0.22), rgba(99, 155, 255, 0.16));
  border-color: rgba(130, 206, 174, 0.35);
  color: #f1f6ff;
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

.date-tag {
  background: var(--bg);
  border: 1.5px solid var(--border);
  border-radius: 20px;
  padding: 5px 12px;
  font-size: 12px;
  font-weight: 600;
  color: var(--ink2);
  display: flex;
  align-items: center;
  gap: 5px;
}

.streak-tag {
  background: linear-gradient(135deg, #FFF8E8, #FFEEC8);
  border: 1.5px solid #FFD980;
  border-radius: 20px;
  padding: 5px 14px;
  font-size: 12px;
  font-weight: 700;
  color: #A06800;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.25s;
  animation: streakPop 3s ease-in-out infinite 3s;
  border-style: solid;
}

@keyframes streakPop {
  0%, 94%, 100% { transform: scale(1); }
  96% { transform: scale(1.12) rotate(-4deg); }
  98% { transform: scale(1.12) rotate(4deg); }
}

.streak-tag:hover { transform: scale(1.08); box-shadow: 0 4px 14px rgba(255, 176, 32, 0.3); }
.flame-icon { animation: flameDance 0.35s ease-in-out infinite alternate; }
@keyframes flameDance { from { transform: scaleY(1) rotate(-4deg); } to { transform: scaleY(1.15) rotate(4deg); } }

.boost-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}

.boost-pill {
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 22px;
  border: 1.5px solid var(--border);
  background: var(--surface);
  box-shadow: var(--card-shadow);
  cursor: pointer;
  animation: floatIn 0.65s cubic-bezier(0.22, 1, 0.36, 1) both;
}

.boost-pill:nth-child(2) { animation-delay: 0.1s; }
.boost-pill:nth-child(3) { animation-delay: 0.2s; }

@keyframes floatIn {
  from { opacity: 0; transform: translateY(20px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.boost-pill::after {
  content: "";
  position: absolute;
  inset: auto -10% -55% auto;
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  filter: blur(6px);
}

.boost-icon {
  width: 42px;
  height: 42px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.34);
  backdrop-filter: blur(8px);
}

.boost-label {
  font-family: "Baloo 2", cursive;
  font-size: 16px;
  font-weight: 800;
  line-height: 1;
}

.boost-sub {
  font-size: 11px;
  color: rgba(24, 25, 43, 0.68);
  font-weight: 700;
  margin-top: 4px;
}

.boost-pill strong {
  margin-left: auto;
  font-size: 13px;
  font-weight: 800;
}

.boost-coral {
  background: linear-gradient(135deg, rgba(255, 96, 88, 0.18), rgba(255, 176, 32, 0.16), rgba(255, 255, 255, 0.84));
}

.boost-sky {
  background: linear-gradient(135deg, rgba(59, 158, 255, 0.18), rgba(30, 200, 200, 0.14), rgba(255, 255, 255, 0.84));
}

.boost-violet {
  background: linear-gradient(135deg, rgba(155, 114, 255, 0.18), rgba(255, 126, 179, 0.14), rgba(255, 255, 255, 0.84));
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

.main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }

.section-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.3px;
  color: var(--muted);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.mission-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.94), rgba(255, 243, 241, 0.98));
  border-radius: 26px;
  padding: 22px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  box-shadow: var(--card-shadow);
  animation: missionReveal 0.7s cubic-bezier(0.22, 1, 0.36, 1) 0.3s both;
  border: 1.5px solid var(--border);
  transition: box-shadow 0.3s;
}

@keyframes missionReveal {
  from { transform: translateX(-30px) rotate(-2deg); opacity: 0; }
  to { transform: translateX(0) rotate(0deg); opacity: 1; }
}

.mission-card:hover { box-shadow: var(--card-shadow-hover); }

.mission-card::before {
  content: "";
  position: absolute;
  top: -60%;
  left: -60%;
  width: 50%;
  height: 220%;
  background: linear-gradient(90deg, transparent, rgba(255, 96, 88, 0.06), transparent);
  transform: skewX(-15deg) translateX(-100%);
  transition: none;
}

.mission-card:hover::before {
  transform: skewX(-15deg) translateX(400%);
  transition: transform 0.7s ease;
}

.mission-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }

.mission-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  background: linear-gradient(145deg, #FFF0EE, #FFDFDD);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  animation: iconWobble 3s ease-in-out infinite 1s;
}

@keyframes iconWobble {
  0%, 100% { transform: rotate(0); }
  25% { transform: rotate(-6deg); }
  75% { transform: rotate(6deg); }
}

.mission-title { font-family: "Baloo 2", cursive; font-size: 20px; font-weight: 800; color: var(--ink); }
.mission-desc { font-size: 13px; color: var(--muted); font-weight: 500; margin-bottom: 16px; line-height: 1.5; }

.tag-row { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 18px; }

.tag {
  background: var(--bg);
  border: 1.5px solid var(--border);
  border-radius: 20px;
  padding: 5px 11px;
  font-size: 11px;
  font-weight: 600;
  color: var(--ink2);
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.tag:hover { background: var(--ink); color: white; border-color: var(--ink); transform: translateY(-3px) scale(1.06); }
.tag:hover :deep(svg) { color: white; }

.play-btn {
  width: 100%;
  padding: 13px;
  background: linear-gradient(135deg, var(--coral), #FF8C66);
  color: white;
  border: none;
  border-radius: 16px;
  font-family: "Baloo 2", cursive;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 5px 18px rgba(255, 96, 88, 0.38);
  position: relative;
  overflow: hidden;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s;
}

.play-btn:hover { transform: translateY(-4px); box-shadow: 0 10px 28px rgba(255, 96, 88, 0.45); }
.play-btn:hover .button-svg:last-child :deep(svg) { transform: translateX(4px); }
.play-btn:active { transform: scale(0.97); }

.play-btn::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 16px;
  box-shadow: 0 0 0 0 rgba(255, 96, 88, 0.5);
  animation: btnRing 2s ease-out infinite;
}

@keyframes btnRing {
  0% { box-shadow: 0 0 0 0 rgba(255, 96, 88, 0.4); }
  70% { box-shadow: 0 0 0 12px rgba(255, 96, 88, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 96, 88, 0); }
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
  border-radius: 26px;
  padding: 22px;
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
.hydration-title { font-family: "Baloo 2", cursive; font-size: 18px; font-weight: 800; color: #0A4A28; margin-bottom: 3px; }
.hydration-sub { font-size: 12px; color: #3A8060; font-weight: 500; margin-bottom: 14px; }
.drop-grid { display: flex; gap: 7px; flex-wrap: wrap; position: relative; z-index: 1; }

.drop-btn {
  width: 34px;
  height: 34px;
  border-radius: 12px;
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

.log-sip-btn {
  width: 100%;
  margin-top: 10px;
  padding: 9px;
  background: white;
  border: 2px dashed rgba(44, 201, 122, 0.4);
  border-radius: 13px;
  font-family: "Baloo 2", cursive;
  font-size: 13px;
  font-weight: 700;
  color: var(--mint);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  z-index: 1;
}

.log-sip-btn:hover {
  background: rgba(44, 201, 122, 0.1);
  border-style: solid;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(44, 201, 122, 0.2);
}

.log-sip-btn:hover .button-svg :deep(svg) { transform: scale(1.4) rotate(20deg); }

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
}

.water-fall-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9500;
  overflow: hidden;
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
.avatar-svg :deep(svg) { width: 30px; height: 30px; color: #D97A00; }
.mini-svg :deep(svg) { width: 13px; height: 13px; }
.stat-svg :deep(svg) { width: 20px; height: 20px; }
.section-svg :deep(svg),
.tag-svg :deep(svg) { width: 11px; height: 11px; }
.mission-svg :deep(svg) { width: 24px; height: 24px; color: var(--coral); }
.button-svg :deep(svg) { width: 16px; height: 16px; transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.win-svg :deep(svg) { width: 19px; height: 19px; }
.check-svg :deep(svg) { width: 12px; height: 12px; color: white; }
.link-svg :deep(svg) { width: 12px; height: 12px; }
.game-svg :deep(svg) { width: 24px; height: 24px; color: var(--gc); }
.star-svg :deep(svg) { width: 14px; height: 14px; }
.drop-svg :deep(svg) { width: 16px; height: 16px; transition: color 0.3s; }
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

.dark-mode .date-tag {
  background: rgba(255, 255, 255, 0.04);
  color: var(--ink2);
}

.dark-mode .streak-tag {
  background: linear-gradient(135deg, rgba(255, 176, 32, 0.18), rgba(255, 126, 179, 0.18));
  border-color: rgba(255, 176, 32, 0.3);
  color: #FFD98E;
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

.dark-mode .boost-pill strong,
.dark-mode .boost-label,
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

@media (max-width: 740px) {
  .boost-strip { grid-template-columns: 1fr; }
  .stats-row { grid-template-columns: 1fr 1fr; }
  .main-grid, .bottom-row, .games-row { grid-template-columns: 1fr; }
  .meal-float { display: none; }
  .meal-banner { flex-direction: column; gap: 14px; align-items: flex-start; }
  .nav-bar { width: calc(100% - 32px); justify-content: space-around; }
  .header { align-items: flex-start; flex-wrap: wrap; gap: 14px; }
  .header-right { width: 100%; align-items: flex-start; }
}
</style>
