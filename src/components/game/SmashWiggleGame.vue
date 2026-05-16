<template>
  <section
    class="smash-game"
    :class="{ 'smash-game--dark': isDarkMode }"
    @pointermove="onPointerMove"
    @pointerup="onPointerUp"
    @pointercancel="onPointerUp"
    @pointerleave="onPointerUp"
  >
    <header class="smash-head">
      <p class="smash-kicker">Routine Rumble</p>
      <div class="smash-title-row">
        <h3>Smash bright healthy habit targets with the hero</h3>
        <button type="button" class="info-btn" @click="showInfo = true" aria-label="Show smash game info">i</button>
      </div>
      <div class="smash-badges" aria-hidden="true">
        <span class="smash-badge">{{ currentMission.title }}</span>
        <span class="smash-badge level-chip">Lvl {{ levelInMission }} / {{ LEVELS_PER_MISSION }}</span>
        <span class="smash-badge">{{ currentMission.short }}</span>
      </div>
    </header>

    <div class="mission-strip" aria-label="Habit missions">
      <div
        v-for="(mission, index) in missions"
        :key="mission.id"
        class="mission-chip"
        :class="{
          active: missionIndex === index,
          done: missionIndex > index || gameState === 'won',
        }"
      >
        <span aria-hidden="true">{{ mission.icon }}</span>
        <div>
          <strong>{{ mission.title }}</strong>
          <small>{{ mission.short }}</small>
        </div>
      </div>
    </div>

    <div class="arena">
      <div class="hud-row">
        <div class="meter-card">
          <span>Mission meter</span>
          <div class="meter-track">
            <i :style="{ width: `${missionProgress}%` }"></i>
          </div>
          <small>{{ collected }} / {{ hitsNeededThisLevel }} hits · round {{ displayRoundLabel }}</small>
        </div>

        <div class="mini-stats">
          <div class="mini-stat">
            <span>Score</span>
            <strong>{{ score }}</strong>
          </div>
          <div class="mini-stat">
            <span>Combo</span>
            <strong>x{{ combo }}</strong>
          </div>
          <div class="mini-stat">
            <span>Best</span>
            <strong>x{{ bestCombo }}</strong>
          </div>
        </div>
      </div>

      <div class="hero-stage" @pointerdown="onPointerDown" @click="tapBoost">
        <div ref="stageViewportRef" class="stage-viewport">
          <div class="target-cloud" aria-hidden="true">
            <button
              v-for="target in targets"
              :key="target.id"
              type="button"
              class="habit-target"
              :class="[target.kind, { current: target.kind === currentMission.id }]"
              :style="{
                left: `${(target.x / VIEW_W) * 100}%`,
                top: `${(target.y / VIEW_H) * 100}%`,
                width: `${(target.r * 2 / VIEW_W) * 100}%`,
              }"
              tabindex="-1"
              :title="target.labelTip || target.label"
            >
              <span class="habit-target__inner">
                <span class="target-icon" aria-hidden="true">{{ target.icon }}</span>
                <span class="target-label">{{ target.displayLabel }}</span>
              </span>
            </button>
          </div>

          <svg class="hero-svg" viewBox="0 0 420 360" preserveAspectRatio="xMidYMid meet">
          <defs>
            <linearGradient id="suitBody" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#313848" />
              <stop offset="55%" stop-color="#1b2231" />
              <stop offset="100%" stop-color="#080c15" />
            </linearGradient>
            <linearGradient id="maskGlow" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#8599ff" />
              <stop offset="100%" stop-color="#a46cff" />
            </linearGradient>
            <radialGradient id="skinTone" cx="35%" cy="25%">
              <stop offset="0%" stop-color="#ffd4b3" />
              <stop offset="100%" stop-color="#f0a26e" />
            </radialGradient>
            <radialGradient id="gloveTone" cx="35%" cy="25%">
              <stop offset="0%" stop-color="#6fd2ff" />
              <stop offset="100%" stop-color="#415cf3" />
            </radialGradient>
            <filter id="softShadow" x="-50%" y="-50%" width="200%" height="200%">
              <feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="rgba(24,34,60,0.22)" />
            </filter>
          </defs>

          <ellipse class="hero-shadow" :cx="hero.torso.x" :cy="320" rx="88" ry="20" />

          <line class="leg shadow" :x1="leftHip.x" :y1="leftHip.y" :x2="leftFoot.x" :y2="leftFoot.y" />
          <line class="leg shadow" :x1="rightHip.x" :y1="rightHip.y" :x2="rightFoot.x" :y2="rightFoot.y" />
          <line class="leg main" :x1="leftHip.x" :y1="leftHip.y" :x2="leftFoot.x" :y2="leftFoot.y" />
          <line class="leg main" :x1="rightHip.x" :y1="rightHip.y" :x2="rightFoot.x" :y2="rightFoot.y" />
          <ellipse class="boot" :cx="leftFoot.x" :cy="leftFoot.y + 3" rx="22" ry="11" />
          <ellipse class="boot" :cx="rightFoot.x" :cy="rightFoot.y + 3" rx="22" ry="11" />

          <line class="arm shadow" :x1="leftShoulder.x" :y1="leftShoulder.y" :x2="hero.leftHand.x" :y2="hero.leftHand.y" />
          <line class="arm shadow" :x1="rightShoulder.x" :y1="rightShoulder.y" :x2="hero.rightHand.x" :y2="hero.rightHand.y" />
          <line class="arm main" :x1="leftShoulder.x" :y1="leftShoulder.y" :x2="hero.leftHand.x" :y2="hero.leftHand.y" />
          <line class="arm main" :x1="rightShoulder.x" :y1="rightShoulder.y" :x2="hero.rightHand.x" :y2="hero.rightHand.y" />

          <circle class="fist" :cx="hero.leftHand.x" :cy="hero.leftHand.y" r="20" />
          <circle class="fist" :cx="hero.rightHand.x" :cy="hero.rightHand.y" r="20" />
          <circle class="fist-highlight" :cx="hero.leftHand.x - 5" :cy="hero.leftHand.y - 5" r="5" />
          <circle class="fist-highlight" :cx="hero.rightHand.x - 5" :cy="hero.rightHand.y - 5" r="5" />

          <g filter="url(#softShadow)">
            <ellipse class="torso" :cx="hero.torso.x" :cy="hero.torso.y + 2" rx="58" ry="72" :class="{ charged: celebration }" />
            <rect class="belt" :x="hero.torso.x - 42" :y="hero.torso.y + 28" width="84" height="16" rx="8" />
            <circle class="belt-core" :cx="hero.torso.x" :cy="hero.torso.y + 36" r="10" />
            <path class="chest-mark" :d="chestPath" />
          </g>

          <circle class="neck" :cx="hero.torso.x" :cy="hero.torso.y - 63" r="14" />
          <circle class="head-shape" :cx="hero.head.x" :cy="hero.head.y" r="38" />
          <path class="mask-shell" :d="maskPath" />
          <path class="mask-panel" :d="maskPanelPath" />
          <circle class="eye-white" :cx="hero.head.x - 12" :cy="hero.head.y - 4" r="6.2" />
          <circle class="eye-white" :cx="hero.head.x + 12" :cy="hero.head.y - 4" r="6.2" />
          <circle class="eye-pupil" :cx="hero.head.x - 12" :cy="hero.head.y - 4" r="2.8" />
          <circle class="eye-pupil" :cx="hero.head.x + 12" :cy="hero.head.y - 4" r="2.8" />
          <path class="mouth-smile" :d="mouthPath" />
          <circle class="cheek" :cx="hero.head.x - 20" :cy="hero.head.y + 11" r="5" />
          <circle class="cheek" :cx="hero.head.x + 20" :cy="hero.head.y + 11" r="5" />
          </svg>

          <div class="burst-layer" aria-hidden="true">
            <span
              v-for="spark in sparks"
              :key="spark.id"
              class="spark"
              :style="{
                left: `${spark.x}%`,
                top: `${spark.y}%`,
                background: spark.color,
                animationDelay: `${spark.delay}ms`,
                '--sx': spark.sx,
                '--sy': spark.sy,
              }"
            ></span>
          </div>
        </div>
      </div>

      <p class="status">{{ statusText }}</p>
    </div>
    <div v-if="showInfo" class="info-modal-backdrop" @click.self="showInfo = false">
      <div class="info-modal">
        <div class="info-modal-head">
          <div>
            <p class="smash-kicker">How to play</p>
            <h4>Routine Rumble</h4>
          </div>
          <button type="button" class="info-close" @click="showInfo = false" aria-label="Close info">×</button>
        </div>
        <ul class="info-list">
          <li>Drag the hero and swing so the glowing gloves hit bubbles.</li>
          <li>Each mission has three levels — smash enough correct bubbles each round.</li>
          <li>Faster combos score more points. Wrong bubbles reset your combo.</li>
          <li>Finish all levels in every zone to beat Routine Rumble.</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from "vue"
import { injectKidsTheme } from "../../composables/useKidsTheme.js"

const { isDarkMode } = injectKidsTheme()

const VIEW_W = 420
const VIEW_H = 360
/** Levels (rounds) to clear inside each habit zone before the next mission unlocks. */
const LEVELS_PER_MISSION = 3
const ACTIVE_TARGETS_MIN = 8
const ACTIVE_TARGETS_MAX = 15

function hitsNeededForMissionLevel(mission, levelSlot) {
  const cap = mission.targetCount
  if (levelSlot === 1) return Math.max(4, Math.ceil(cap * 0.5))
  if (levelSlot === 2) return Math.max(hitsNeededForMissionLevel(mission, 1) + 1, Math.ceil(cap * 0.78))
  return cap
}

const missions = [
  {
    id: "food",
    title: "Food Fuel",
    short: "Smash the healthy bites",
    icon: "🥦",
    color: "#4caf50",
    targetCount: 9,
  },
  {
    id: "water",
    title: "Water Rush",
    short: "Catch the hydration drops",
    icon: "💧",
    color: "#29b6f6",
    targetCount: 9,
  },
  {
    id: "sleep",
    title: "Sleep Boost",
    short: "Smash sleepy good habits",
    icon: "🌙",
    color: "#8c6cff",
    targetCount: 8,
  },
  {
    id: "routine",
    title: "Routine Ready",
    short: "Lock in healthy routine wins",
    icon: "🪥",
    color: "#ff9f43",
    targetCount: 8,
  },
]

const targetPools = {
  food: [
    { label: "apple", icon: "🍎" },
    { label: "pear", icon: "🍐" },
    { label: "grape", icon: "🍇" },
    { label: "cherry", icon: "🍒" },
    { label: "banana", icon: "🍌" },
    { label: "mango", icon: "🥭" },
    { label: "carrot", icon: "🥕" },
    { label: "pepper", icon: "🫑" },
    { label: "broccoli", icon: "🥦" },
    { label: "tomato", icon: "🍅" },
    { label: "salad", icon: "🥗" },
    { label: "corn", icon: "🌽" },
    { label: "oats", icon: "🌾" },
    { label: "rice", icon: "🍚" },
    { label: "cheese", icon: "🧀" },
    { label: "egg", icon: "🥚" },
    { label: "toast", icon: "🍞" },
    { label: "soup", icon: "🍲" },
    { label: "waffle", icon: "🧇" },
    { label: "berries", icon: "🫐" },
    { label: "yogurt", icon: "🥛" },
  ],
  water: [
    { label: "sip", icon: "💧" },
    { label: "gulp", icon: "💦" },
    { label: "swig", icon: "💧" },
    { label: "faucet", icon: "🚰" },
    { label: "ice", icon: "🧊" },
    { label: "pitcher", icon: "🏺" },
    { label: "bottle", icon: "🍼" },
    { label: "cup", icon: "🥤" },
    { label: "splash", icon: "💧" },
    { label: "drink", icon: "💦" },
    { label: "refill", icon: "♻️" },
    { label: "cool", icon: "🧊" },
    { label: "pure", icon: "✨" },
    { label: "flow", icon: "🌀" },
  ],
  sleep: [
    { label: "bedtime", icon: "🌙" },
    { label: "story", icon: "📖" },
    { label: "cozy", icon: "✨" },
    { label: "pjs", icon: "🛌" },
    { label: "breathe", icon: "🫁" },
    { label: "music", icon: "🎵" },
    { label: "teddy", icon: "🧸" },
    { label: "snooze", icon: "😴" },
    { label: "yawn", icon: "😮" },
    { label: "stars", icon: "⭐" },
    { label: "hug", icon: "🫶" },
    { label: "dim", icon: "🔆" },
    { label: "quiet", icon: "🤫" },
    { label: "dream", icon: "💭" },
  ],
  routine: [
    { label: "brush", icon: "🪥" },
    { label: "backpack", icon: "🎒" },
    { label: "soap", icon: "🫧" },
    { label: "stretch", icon: "🤸" },
    { label: "socks", icon: "🧦" },
    { label: "clock", icon: "⏰" },
    { label: "lunchbox", icon: "🍱" },
    { label: "shoes", icon: "👟" },
    { label: "tidy", icon: "✨" },
    { label: "keys", icon: "🔑" },
    { label: "towel", icon: "🏖️" },
    { label: "comb", icon: "💇" },
    { label: "sun", icon: "☀️" },
    { label: "route", icon: "🛤️" },
  ],
}

const drag = reactive({
  active: false,
  pointerId: null,
  lastX: VIEW_W / 2,
  lastY: 180,
  lastAt: 0,
  speed: 0,
})

const pointer = reactive({ x: VIEW_W / 2, y: 180 })
const hero = reactive({
  torso: { x: VIEW_W / 2, y: 212, vx: 0, vy: 0 },
  head: { x: VIEW_W / 2, y: 132, vx: 0, vy: 0 },
  leftHand: { x: VIEW_W / 2 - 82, y: 214, vx: 0, vy: 0, lastX: VIEW_W / 2 - 82, lastY: 214, speed: 0 },
  rightHand: { x: VIEW_W / 2 + 82, y: 214, vx: 0, vy: 0, lastX: VIEW_W / 2 + 82, lastY: 214, speed: 0 },
})

const stageViewportRef = ref(null)

const missionIndex = ref(0)
const showInfo = ref(false)
const gameState = ref("playing")
const levelInMission = ref(1)
const collected = ref(0)
const score = ref(0)
const combo = ref(0)
const bestCombo = ref(0)
const celebration = ref(false)
const targets = ref([])
const sparks = ref([])
const statusLine = ref("Swing the hero into the matching healthy habit targets.")

let targetId = 1
let sparkId = 1
let rafId = null
let missionTimer = null
let levelAdvanceTimer = null

const currentMission = computed(() => missions[missionIndex.value] ?? missions[0])
const hitsNeededThisLevel = computed(() => hitsNeededForMissionLevel(currentMission.value, levelInMission.value))
const displayRoundLabel = computed(() => `${levelInMission.value}/${LEVELS_PER_MISSION}`)
const missionProgress = computed(() => {
  const need = hitsNeededThisLevel.value
  if (!need) return 0
  return Math.min(100, Math.round((collected.value / need) * 100))
})

const statusText = computed(() => {
  if (gameState.value === "won") return "Routine Rumble complete! Tap the arena to play again."
  return statusLine.value
})

const leftShoulder = computed(() => ({ x: hero.torso.x - 40, y: hero.torso.y - 28 }))
const rightShoulder = computed(() => ({ x: hero.torso.x + 40, y: hero.torso.y - 28 }))
const leftHip = computed(() => ({ x: hero.torso.x - 24, y: hero.torso.y + 52 }))
const rightHip = computed(() => ({ x: hero.torso.x + 24, y: hero.torso.y + 52 }))
const leftFoot = computed(() => ({ x: hero.torso.x - 34, y: 302 }))
const rightFoot = computed(() => ({ x: hero.torso.x + 34, y: 302 }))

const chestPath = computed(() => {
  const x = hero.torso.x
  const y = hero.torso.y - 16
  return `M ${x - 16} ${y} C ${x - 4} ${y - 16}, ${x + 4} ${y - 16}, ${x + 16} ${y} C ${x + 12} ${y + 18}, ${x - 12} ${y + 18}, ${x - 16} ${y} Z`
})

const maskPath = computed(() => {
  const x = hero.head.x
  const y = hero.head.y
  return `M ${x - 30} ${y - 12} Q ${x} ${y - 34} ${x + 30} ${y - 12} L ${x + 24} ${y + 12} Q ${x} ${y + 26} ${x - 24} ${y + 12} Z`
})

const maskPanelPath = computed(() => {
  const x = hero.head.x
  const y = hero.head.y
  return `M ${x - 10} ${y - 22} L ${x + 10} ${y - 22} L ${x + 20} ${y + 8} L ${x - 20} ${y + 8} Z`
})

const mouthPath = computed(() => {
  const x = hero.head.x
  const y = hero.head.y
  return `M ${x - 11} ${y + 15} Q ${x} ${y + 24} ${x + 11} ${y + 15}`
})

function randomBetween(min, max) {
  return min + Math.random() * (max - min)
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value))
}

function pickRandom(list) {
  return list[Math.floor(Math.random() * list.length)]
}

function activeBubbleQuota() {
  return clamp(9 + missionIndex.value + (levelInMission.value - 1), ACTIVE_TARGETS_MIN, ACTIVE_TARGETS_MAX)
}

function currentCorrectProbability() {
  return clamp(0.73 - (levelInMission.value - 1) * 0.06 - missionIndex.value * 0.035, 0.48, 0.73)
}

function spawnTarget() {
  const useCurrent = Math.random() < currentCorrectProbability()
  const kind = useCurrent
    ? currentMission.value.id
    : pickRandom(missions.filter(mission => mission.id !== currentMission.value.id)).id
  const meta = pickRandom(targetPools[kind])
  const displayLabel = (meta.short || meta.label || "").trim()
  targets.value.push({
    id: targetId++,
    kind,
    label: (meta.label || displayLabel).trim(),
    displayLabel,
    labelTip: meta.tip || meta.label || displayLabel,
    icon: meta.icon,
    x: randomBetween(52, VIEW_W - 52),
    y: randomBetween(48, 168),
    vx: randomBetween(-0.42, 0.42),
    vy: randomBetween(-0.24, 0.24),
    r: kind === currentMission.value.id ? 31 : 27,
  })
}

function refillTargets() {
  while (targets.value.length < activeBubbleQuota()) spawnTarget()
}

function resetMissionTargets() {
  targets.value = []
  refillTargets()
}

function onPointerDown(event) {
  drag.active = true
  drag.pointerId = event.pointerId
  const p = toLocal(event)
  pointer.x = p.x
  pointer.y = p.y
  drag.lastX = p.x
  drag.lastY = p.y
  drag.lastAt = performance.now()
  if (event.currentTarget?.setPointerCapture) event.currentTarget.setPointerCapture(event.pointerId)
}

function onPointerMove(event) {
  if (!drag.active || event.pointerId !== drag.pointerId) return
  const p = toLocal(event)
  const now = performance.now()
  const dx = p.x - drag.lastX
  const dy = p.y - drag.lastY
  const dt = Math.max(12, now - drag.lastAt)
  drag.speed = (Math.hypot(dx, dy) / dt) * 100
  drag.lastX = p.x
  drag.lastY = p.y
  drag.lastAt = now
  pointer.x = p.x
  pointer.y = p.y
}

function onPointerUp(event) {
  if (drag.pointerId !== null && event.pointerId !== drag.pointerId) return
  drag.active = false
  drag.pointerId = null
  drag.speed = 0
}

function tapBoost() {
  if (gameState.value !== "playing") {
    restartGame()
    return
  }
  const nudgeX = (Math.random() - 0.5) * 34
  const nudgeY = (Math.random() - 0.5) * 26
  pointer.x = clamp(pointer.x + nudgeX, 48, VIEW_W - 48)
  pointer.y = clamp(pointer.y + nudgeY, 70, VIEW_H - 120)
  hero.leftHand.vx -= nudgeX * 0.08
  hero.rightHand.vx += nudgeX * 0.08
  hero.leftHand.vy -= nudgeY * 0.12
  hero.rightHand.vy += nudgeY * 0.12
  statusLine.value = "Tap and drag fast to whip the hero gloves into the targets."
}

function toLocal(event) {
  const stage = stageViewportRef.value
  if (!stage) {
    return { x: VIEW_W / 2, y: VIEW_H / 2 }
  }
  const rect = stage.getBoundingClientRect()
  if (rect.width < 8 || rect.height < 8) {
    return { x: VIEW_W / 2, y: VIEW_H / 2 }
  }
  const x = ((event.clientX - rect.left) / rect.width) * VIEW_W
  const y = ((event.clientY - rect.top) / rect.height) * VIEW_H
  return {
    x: clamp(x, 24, VIEW_W - 24),
    y: clamp(y, 36, VIEW_H - 24),
  }
}

function updateNode(node, targetX, targetY, stiffness = 0.12, damping = 0.86) {
  node.vx += (targetX - node.x) * stiffness
  node.vy += (targetY - node.y) * stiffness
  node.vx *= damping
  node.vy *= damping
  node.x += node.vx
  node.y += node.vy
}

function updateHandSpeed(hand) {
  const dx = hand.x - hand.lastX
  const dy = hand.y - hand.lastY
  hand.speed = Math.hypot(dx, dy)
  hand.lastX = hand.x
  hand.lastY = hand.y
}

function updateTargets(time) {
  targets.value.forEach(target => {
    target.x += target.vx + Math.sin(time / 520 + target.id) * 0.12
    target.y += target.vy + Math.cos(time / 610 + target.id) * 0.08

    if (target.x < 36 || target.x > VIEW_W - 36) target.vx *= -1
    if (target.y < 34 || target.y > 184) target.vy *= -1
    target.x = clamp(target.x, 36, VIEW_W - 36)
    target.y = clamp(target.y, 34, 184)
  })
}

function hitTarget(target, hitSpeed) {
  const correct = target.kind === currentMission.value.id

  if (correct) {
    collected.value += 1
    combo.value += 1
    bestCombo.value = Math.max(bestCombo.value, combo.value)
    score.value += 14 + combo.value * 3 + levelInMission.value
    statusLine.value = `Nice hit! Combo x${combo.value} — Round ${levelInMission.value}/${LEVELS_PER_MISSION}.`
    spawnSparksAt(target.x, target.y, currentMission.value.color)
  } else {
    combo.value = 0
    score.value = Math.max(0, score.value - 8)
    statusLine.value = `Wrong zone (${target.kind}). Only smash the glowing ${currentMission.value.title.toLowerCase()} bubbles.`
    spawnSparksAt(target.x, target.y, "#ff7a7a")
  }

  targets.value = targets.value.filter(entry => entry.id !== target.id)

  if (correct && collected.value >= hitsNeededThisLevel.value) {
    if (levelInMission.value >= LEVELS_PER_MISSION) {
      completeMission()
    } else {
      advanceAfterLevelComplete()
    }
    return
  }

  refillTargets()
}

function advanceAfterLevelComplete() {
  clearTimeout(levelAdvanceTimer)
  celebration.value = true
  spawnSparksAt(VIEW_W / 2, 118, currentMission.value.color)
  statusLine.value = `Round ${levelInMission.value} cleared — bigger waves incoming!`

  levelAdvanceTimer = window.setTimeout(() => {
    celebration.value = false
    levelInMission.value += 1
    collected.value = 0
    statusLine.value = `Round ${levelInMission.value}/${LEVELS_PER_MISSION}: Keep smashing glowing ${currentMission.value.title.toLowerCase()} bubbles.`
    resetMissionTargets()
    levelAdvanceTimer = null
  }, 980)
}

function detectHits() {
  if (gameState.value !== "playing" || celebration.value) return

  const handStates = [
    { x: hero.leftHand.x, y: hero.leftHand.y, speed: hero.leftHand.speed },
    { x: hero.rightHand.x, y: hero.rightHand.y, speed: hero.rightHand.speed },
  ]

  /** Fist radius in viewBox units ≈ 20; allow modest overlap + spring smoothing. */
  const fistRadius = 20
  const minHandSpeed = 0.75
  const dragBoost = drag.active ? Math.min(drag.speed * 0.04, 4) : 0

  for (const target of targets.value) {
    for (const hand of handStates) {
      const dist = Math.hypot(hand.x - target.x, hand.y - target.y)
      const hitRadius = target.r + fistRadius + 6
      const impact = hand.speed + dragBoost
      if (dist < hitRadius && impact > minHandSpeed) {
        hitTarget(target, hand.speed)
        return
      }
    }
  }
}

function completeMission() {
  clearTimeout(levelAdvanceTimer)
  levelAdvanceTimer = null
  celebration.value = true
  clearTimeout(missionTimer)
  statusLine.value = `${currentMission.value.title} finished — powering up the next zone!`
  spawnSparksAt(VIEW_W / 2, 112, currentMission.value.color)

  missionTimer = window.setTimeout(() => {
    celebration.value = false
    if (missionIndex.value >= missions.length - 1) {
      gameState.value = "won"
      statusLine.value = "Routine Rumble complete! Tap the arena to play again."
      targets.value = []
      return
    }

    missionIndex.value += 1
    levelInMission.value = 1
    collected.value = 0
    combo.value = 0
    statusLine.value = `New zone: ${currentMission.value.title}. Round 1/${LEVELS_PER_MISSION}.`
    resetMissionTargets()
  }, 1150)
}

function spawnSparksAt(x, y, color) {
  sparks.value = Array.from({ length: 20 }, (_, index) => ({
    id: sparkId++,
    x: (x / VIEW_W) * 100,
    y: (y / VIEW_H) * 100,
    sx: Math.random(),
    sy: Math.random(),
    delay: index * 10,
    color,
  }))
  window.setTimeout(() => {
    sparks.value = []
  }, 780)
}

function updatePhysics(time) {
  const idleX = VIEW_W / 2 + Math.sin(time / 520) * 8
  const idleY = 196 + Math.sin(time / 760) * 7
  const torsoTargetX = drag.active ? pointer.x : idleX
  const torsoTargetY = drag.active ? clamp(pointer.y + 28, 168, 244) : idleY

  updateNode(hero.torso, torsoTargetX, torsoTargetY, drag.active ? 0.16 : 0.06, drag.active ? 0.8 : 0.9)
  updateNode(hero.head, hero.torso.x, hero.torso.y - 80, 0.16, 0.84)

  const sway = drag.active ? drag.speed * 0.16 : Math.sin(time / 220) * 6
  const leftTargetX = hero.torso.x - 84 - sway
  const rightTargetX = hero.torso.x + 84 + sway
  const handTargetY = hero.torso.y - 6 + Math.sin(time / 180) * 4

  updateNode(hero.leftHand, leftTargetX, handTargetY, 0.2, 0.82)
  updateNode(hero.rightHand, rightTargetX, handTargetY, 0.2, 0.82)
  updateHandSpeed(hero.leftHand)
  updateHandSpeed(hero.rightHand)

  updateTargets(time)
  detectHits()
  rafId = window.requestAnimationFrame(updatePhysics)
}

function restartGame() {
  clearTimeout(missionTimer)
  clearTimeout(levelAdvanceTimer)
  levelAdvanceTimer = null
  missionIndex.value = 0
  levelInMission.value = 1
  gameState.value = "playing"
  collected.value = 0
  score.value = 0
  combo.value = 0
  bestCombo.value = 0
  celebration.value = false
  statusLine.value = "Swing the hero into the matching healthy habit targets."
  resetMissionTargets()
}

onMounted(() => {
  resetMissionTargets()
  rafId = window.requestAnimationFrame(updatePhysics)
})

onBeforeUnmount(() => {
  if (rafId) window.cancelAnimationFrame(rafId)
  clearTimeout(missionTimer)
  clearTimeout(levelAdvanceTimer)
})
</script>

<style scoped>
.smash-game {
  --coral: #FF6058;
  --sky: #3B9EFF;
  --mint: #2CC97A;
  --amber: #FFB020;
  --violet: #9B72FF;
  --rose: #FF7EB3;
  color: #1d2748;
  font-family: "DM Sans", sans-serif;
  position: relative;
}

.smash-kicker {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.78rem;
  font-weight: 900;
  color: var(--violet);
}

.smash-head h3 {
  margin: 8px 0 0;
  font-size: clamp(1.5rem, 3vw, 2rem);
  color: #1e315b;
  font-family: "Baloo 2", cursive;
}

.smash-head {
  padding: 18px 18px 0;
  border-radius: 26px;
  background:
    radial-gradient(circle at 8% 16%, rgba(255, 176, 32, 0.16), transparent 24%),
    radial-gradient(circle at 88% 10%, rgba(255, 126, 179, 0.08), transparent 20%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(247, 243, 255, 0.94));
  animation: smashFloat 5.4s ease-in-out infinite;
}

.smash-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.smash-badges {
  margin-top: 12px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.smash-badge {
  border-radius: 999px;
  padding: 10px 14px;
  background: linear-gradient(135deg, rgba(244, 248, 255, 0.98), rgba(237, 243, 255, 0.95));
  border: 1.5px solid rgba(92, 111, 198, 0.16);
  color: #45608e;
  font-size: 0.84rem;
  font-weight: 800;
  animation: smashPulse 3.6s ease-in-out infinite;
}

.smash-badge.level-chip {
  animation: smashFloat 4.2s ease-in-out infinite;
  background: linear-gradient(135deg, rgba(238, 242, 255, 1), rgba(224, 231, 254, 0.96));
  border-color: rgba(99, 102, 241, 0.36);
  color: #3c2f9c;
}

.mission-strip {
  margin-top: 16px;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.mission-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  border-radius: 22px;
  padding: 12px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(244, 246, 255, 0.84));
  border: 1px solid rgba(91, 109, 196, 0.14);
  box-shadow: 0 12px 20px rgba(31, 48, 95, 0.06);
  animation: smashFloat 4.8s ease-in-out infinite;
}

.mission-chip span {
  width: 58px;
  height: 58px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #ffffff, #e7eeff);
  font-size: 1.8rem;
  flex: 0 0 auto;
  box-shadow: 0 12px 20px rgba(37, 54, 109, 0.14);
}

.mission-chip strong {
  display: block;
  color: #203256;
}

.mission-chip small {
  display: block;
  margin-top: 4px;
  color: #617093;
  line-height: 1.35;
}

.mission-chip.active {
  border-color: rgba(255, 126, 179, 0.22);
  background: linear-gradient(135deg, rgba(233, 245, 255, 0.98), rgba(240, 236, 255, 0.96));
  box-shadow: 0 16px 30px rgba(123, 101, 255, 0.16);
}

.mission-chip.done {
  background: linear-gradient(135deg, rgba(239, 255, 242, 0.96), rgba(244, 250, 255, 0.92));
  box-shadow: 0 14px 26px rgba(44, 201, 122, 0.14);
}

.arena {
  position: relative;
  margin-top: 16px;
  border-radius: 28px;
  border: 1px solid rgba(73, 92, 164, 0.18);
  background:
    radial-gradient(circle at 78% 18%, rgba(173, 161, 255, 0.18), transparent 28%),
    radial-gradient(circle at 18% 72%, rgba(125, 216, 255, 0.16), transparent 28%),
    radial-gradient(circle at 50% 96%, rgba(255, 176, 32, 0.12), transparent 26%),
    linear-gradient(180deg, #fcfdff 0%, #f3f7ff 100%);
  padding: 18px;
  min-height: 510px;
  overflow: hidden;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.52), 0 20px 36px rgba(37, 54, 109, 0.1);
  animation: arenaGlow 6s ease-in-out infinite;
}

.arena::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at 12% 22%, rgba(255, 255, 255, 0.16), transparent 0 4px, transparent 5px),
    radial-gradient(circle at 76% 18%, rgba(255, 255, 255, 0.14), transparent 0 4px, transparent 5px),
    radial-gradient(circle at 62% 78%, rgba(255, 255, 255, 0.14), transparent 0 5px, transparent 6px);
  animation: smashSparkle 13s linear infinite;
}

.hud-row {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 16px;
}

.meter-card {
  min-width: min(360px, 100%);
  border-radius: 22px;
  padding: 14px;
  background: linear-gradient(135deg, rgba(239, 247, 255, 0.98), rgba(232, 240, 255, 0.95));
  box-shadow: 0 12px 22px rgba(37, 54, 109, 0.08);
}

.meter-card span {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 800;
  color: #3f4f7b;
}

.meter-card small {
  display: block;
  margin-top: 7px;
  color: #5b6d92;
  font-weight: 700;
  font-size: 0.76rem;
}

.meter-track {
  margin-top: 8px;
  height: 14px;
  border-radius: 999px;
  background: #e7edff;
  overflow: hidden;
}

.meter-track i {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--mint) 0%, var(--sky) 38%, var(--violet) 70%, #ff8c4d 100%);
  transition: width 0.14s ease;
  background-size: 200% 100%;
  animation: smashWave 2.6s linear infinite;
}

.mini-stats {
  display: flex;
  gap: 8px;
}

.mini-stat {
  min-width: 92px;
  border-radius: 18px;
  padding: 10px 12px;
  background: linear-gradient(135deg, rgba(244, 247, 255, 0.96), rgba(239, 242, 255, 0.92));
  border: 1.5px solid rgba(92, 111, 198, 0.12);
  text-align: center;
  box-shadow: 0 10px 18px rgba(37, 54, 109, 0.08);
  animation: smashFloat 4.4s ease-in-out infinite;
}

.mini-stat span {
  display: block;
  color: #5b6d92;
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.mini-stat strong {
  display: block;
  margin-top: 6px;
  font-size: 1.22rem;
  color: #203256;
  font-family: "Baloo 2", cursive;
}

.hero-stage {
  margin-top: 22px;
  display: flex;
  justify-content: center;
  cursor: grab;
  user-select: none;
  touch-action: none;
}

.hero-stage:active {
  cursor: grabbing;
}

.stage-viewport {
  position: relative;
  width: min(100%, 440px);
  aspect-ratio: 420 / 360;
  max-height: min(72vh, 380px);
}

.target-cloud {
  position: absolute;
  inset: 0;
  z-index: 1;
}

.habit-target {
  position: absolute;
  transform: translate(-50%, -50%);
  container-type: size;
  box-sizing: border-box;
  aspect-ratio: 1;
  height: auto;
  max-width: 44%;
  border-radius: 999px;
  border: 2px solid rgba(30, 52, 112, 0.22);
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.98), rgba(224, 238, 255, 0.92));
  color: #101828;
  display: flex;
  align-items: stretch;
  padding: 0;
  overflow: hidden;
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.75) inset,
    0 10px 22px rgba(12, 28, 72, 0.12);
  pointer-events: none;
}

.habit-target__inner {
  width: 100%;
  min-height: 0;
  box-sizing: border-box;
  padding: clamp(4px, 11cqmin, 10px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: clamp(0px, 1.5cqmin, 4px);
  overflow: hidden;
  text-align: center;
}

@supports not (padding: clamp(4px, 11cqmin, 10px)) {
  .habit-target__inner {
    padding: clamp(4px, 6%, 12px);
  }
}

.habit-target.current {
  border-color: rgba(37, 99, 235, 0.45);
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.85) inset,
    0 16px 28px rgba(37, 99, 235, 0.2);
  animation: smashTargetGlow 2.8s ease-in-out infinite;
}

.habit-target.food.current {
  background: linear-gradient(160deg, rgba(238, 255, 246, 1), rgba(214, 250, 224, 0.94));
}

.habit-target.water.current {
  background: linear-gradient(160deg, rgba(232, 248, 255, 1), rgba(207, 235, 255, 0.94));
}

.habit-target.sleep.current {
  background: linear-gradient(160deg, rgba(244, 240, 255, 1), rgba(229, 222, 255, 0.94));
}

.habit-target.routine.current {
  background: linear-gradient(160deg, rgba(255, 248, 232, 1), rgba(255, 235, 210, 0.94));
}

.target-icon {
  flex: 0 0 auto;
  font-size: clamp(0.65rem, min(26cqmin, 6vmin), 1.08rem);
  line-height: 1;
}

.target-label {
  flex: 0 1 auto;
  width: 100%;
  max-width: 100%;
  min-height: 0;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  font-size: clamp(0.45rem, min(15cqmin, 2.4vmin), 0.74rem);
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: #0b1628;
  line-height: 1.05;
  text-align: center;
  word-break: break-word;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.93);
}

@supports not (font-size: min(26cqmin, 6vmin)) {
  .target-icon {
    font-size: clamp(0.62rem, 5.5vmin, 1rem);
  }
  .target-label {
    font-size: clamp(0.45rem, 2.1vmin, 0.72rem);
  }
}

.hero-svg {
  position: absolute;
  inset: 0;
  z-index: 2;
  width: 100%;
  height: 100%;
  display: block;
  margin: 0;
  overflow: visible;
}

.hero-shadow {
  fill: rgba(18, 30, 60, 0.12);
}

.arm,
.leg {
  stroke-linecap: round;
  stroke-linejoin: round;
}

.arm.shadow,
.leg.shadow {
  stroke: rgba(11, 18, 35, 0.14);
  stroke-width: 30;
}

.arm.main {
  stroke: url(#suitBody);
  stroke-width: 24;
}

.leg.main {
  stroke: url(#suitBody);
  stroke-width: 24;
}

.boot {
  fill: #131924;
}

.fist {
  fill: url(#gloveTone);
}

.fist-highlight {
  fill: rgba(255, 255, 255, 0.46);
}

.torso {
  fill: url(#suitBody);
}

.torso.charged {
  filter: saturate(1.3) brightness(1.08);
}

.belt {
  fill: #101522;
}

.belt-core {
  fill: #6ce8a2;
}

.chest-mark {
  fill: #72ecaa;
}

.neck {
  fill: url(#skinTone);
}

.head-shape {
  fill: url(#skinTone);
}

.mask-shell {
  fill: url(#maskGlow);
}

.mask-panel {
  fill: rgba(18, 24, 40, 0.72);
}

.eye-white {
  fill: #fff;
}

.eye-pupil {
  fill: #101728;
}

.mouth-smile {
  fill: none;
  stroke: #6f2f24;
  stroke-width: 4;
  stroke-linecap: round;
}

.cheek {
  fill: rgba(255, 146, 126, 0.28);
}

.status {
  margin: 14px 0 0;
  text-align: center;
  font-weight: 800;
  color: #2d3b67;
}

.info-btn,
.info-close {
  width: 48px;
  height: 48px;
  border-radius: 999px;
  border: 1.5px solid rgba(107, 45, 255, 0.18);
  background: linear-gradient(135deg, rgba(243, 240, 255, 0.98), rgba(232, 242, 255, 0.96));
  color: #5d57d8;
  font-weight: 900;
  font-size: 1.3rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 10px 18px rgba(33, 52, 106, 0.08);
  flex: 0 0 auto;
  animation: smashPulse 3s ease-in-out infinite;
}

.info-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 20;
  display: grid;
  place-items: center;
  padding: 20px;
  background: rgba(24, 25, 43, 0.28);
  backdrop-filter: blur(10px);
}

.info-modal {
  width: min(520px, 100%);
  border-radius: 26px;
  padding: 20px;
  background:
    radial-gradient(circle at 100% 0%, rgba(255, 126, 179, 0.18), transparent 28%),
    radial-gradient(circle at 0% 100%, rgba(59, 158, 255, 0.18), transparent 26%),
    rgba(255, 255, 255, 0.98);
  border: 1.5px solid rgba(86, 109, 184, 0.14);
  box-shadow: 0 18px 30px rgba(33, 52, 106, 0.16);
  animation: smashFloat 5.2s ease-in-out infinite;
}

.info-modal-head {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 12px;
}

.info-modal h4 {
  margin: 8px 0 0;
  font-size: 1.35rem;
  font-family: "Baloo 2", cursive;
  color: #1e315b;
}

.info-list {
  margin: 14px 0 0;
  padding-left: 18px;
  color: #556586;
  display: grid;
  gap: 10px;
  line-height: 1.6;
}

.info-list li::marker {
  color: var(--coral);
}

@keyframes smashPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes smashTargetGlow {
  0%, 100% {
    filter: brightness(1);
    box-shadow:
      0 1px 0 rgba(255, 255, 255, 0.85) inset,
      0 16px 28px rgba(37, 99, 235, 0.2);
  }
  50% {
    filter: brightness(1.07);
    box-shadow:
      0 1px 0 rgba(255, 255, 255, 0.95) inset,
      0 20px 34px rgba(37, 99, 235, 0.28);
  }
}

@keyframes smashFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

@keyframes smashWave {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}

@keyframes arenaGlow {
  0%, 100% { box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.52), 0 20px 36px rgba(37, 54, 109, 0.1); }
  50% { box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.7), 0 24px 40px rgba(123, 101, 255, 0.16); }
}

@keyframes smashSparkle {
  from { transform: translateY(0); opacity: 0.72; }
  50% { opacity: 1; }
  to { transform: translateY(-16px); opacity: 0.72; }
}

.burst-layer {
  position: absolute;
  inset: 0;
  z-index: 3;
  pointer-events: none;
}

.spark {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 4px;
  opacity: 0;
  animation: sparkOut 620ms ease-out forwards;
}

@keyframes sparkOut {
  from {
    transform: translate(0, 0) scale(0.5) rotate(0deg);
    opacity: 1;
  }
  to {
    transform: translate(
        calc((var(--sx, 0.5) - 0.5) * 180px),
        calc((var(--sy, 0.5) - 0.5) * 140px)
      )
      scale(1.16)
      rotate(220deg);
    opacity: 0;
  }
}

/* Dark theme — matches kid shell */
.smash-game--dark {
  color: rgba(226, 234, 255, 0.92);
}

.smash-game--dark .smash-kicker {
  color: #c4b5fd;
}

.smash-game--dark .smash-head h3 {
  color: #f2f7ff;
}

.smash-game--dark .smash-head {
  background:
    radial-gradient(circle at 8% 16%, rgba(255, 176, 32, 0.12), transparent 24%),
    linear-gradient(135deg, rgba(22, 28, 52, 0.95), rgba(14, 18, 42, 0.92));
  border: 1px solid rgba(143, 154, 227, 0.22);
}

.smash-game--dark .smash-badge {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.04));
  border-color: rgba(143, 154, 227, 0.22);
  color: rgba(226, 234, 255, 0.9);
}

.smash-game--dark .smash-badge.level-chip {
  background: linear-gradient(135deg, rgba(167, 139, 250, 0.24), rgba(88, 78, 226, 0.12));
  border-color: rgba(196, 181, 253, 0.45);
  color: #eef2ff;
}

.smash-game--dark .mission-chip {
  background: linear-gradient(135deg, rgba(22, 28, 52, 0.88), rgba(14, 18, 42, 0.86));
  border-color: rgba(143, 154, 227, 0.2);
  box-shadow: 0 8px 18px rgba(3, 7, 23, 0.35);
}

.smash-game--dark .mission-chip span {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.05));
}

.smash-game--dark .mission-chip strong {
  color: #f2f7ff;
}

.smash-game--dark .mission-chip small {
  color: rgba(198, 208, 240, 0.88);
}

.smash-game--dark .mission-chip.active {
  background: linear-gradient(135deg, rgba(59, 158, 255, 0.18), rgba(22, 28, 52, 0.92));
}

.smash-game--dark .mission-chip.done {
  background: linear-gradient(135deg, rgba(44, 201, 122, 0.14), rgba(22, 28, 52, 0.92));
}

.smash-game--dark .arena {
  background:
    radial-gradient(circle at 78% 18%, rgba(155, 114, 255, 0.12), transparent 28%),
    linear-gradient(180deg, rgba(14, 20, 44, 0.96) 0%, rgba(10, 14, 32, 0.98) 100%);
  border-color: rgba(143, 154, 227, 0.22);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.06), 0 20px 40px rgba(3, 7, 23, 0.45);
}

.smash-game--dark .meter-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.04));
}

.smash-game--dark .meter-card span {
  color: rgba(198, 208, 240, 0.88);
}

.smash-game--dark .meter-card small {
  color: rgba(210, 220, 255, 0.85);
}

.smash-game--dark .meter-track {
  background: rgba(255, 255, 255, 0.12);
}

.smash-game--dark .mini-stat {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
  border-color: rgba(143, 154, 227, 0.22);
}

.smash-game--dark .mini-stat span {
  color: rgba(198, 208, 240, 0.85);
}

.smash-game--dark .mini-stat strong {
  color: #f2f7ff;
}

.smash-game--dark .status {
  color: rgba(226, 234, 255, 0.88);
}

.smash-game--dark .habit-target {
  border-color: rgba(15, 23, 42, 0.55);
  background: linear-gradient(160deg, rgba(250, 252, 255, 0.98), rgba(220, 234, 255, 0.94));
  color: #0a0f1a;
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.55) inset,
    0 10px 22px rgba(3, 7, 23, 0.35);
}

.smash-game--dark .target-label {
  color: #070b14;
  text-shadow: 0 1px 0 rgba(255, 255, 255, 0.95);
}

.smash-game--dark .habit-target.food.current {
  background: linear-gradient(160deg, rgba(230, 255, 240, 1), rgba(200, 245, 218, 0.95));
}

.smash-game--dark .habit-target.water.current {
  background: linear-gradient(160deg, rgba(224, 246, 255, 1), rgba(190, 230, 255, 0.95));
}

.smash-game--dark .habit-target.sleep.current {
  background: linear-gradient(160deg, rgba(236, 232, 255, 1), rgba(210, 200, 255, 0.92));
}

.smash-game--dark .habit-target.routine.current {
  background: linear-gradient(160deg, rgba(255, 244, 224, 1), rgba(255, 220, 180, 0.94));
}

.smash-game--dark .info-btn,
.smash-game--dark .info-close {
  border-color: rgba(143, 154, 227, 0.35);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.05));
  color: #e0e7ff;
}

.smash-game--dark .info-modal-backdrop {
  background: rgba(3, 7, 23, 0.62);
}

.smash-game--dark .info-modal {
  background: rgba(18, 22, 43, 0.97);
  border-color: rgba(143, 154, 227, 0.22);
}

.smash-game--dark .info-modal h4,
.smash-game--dark .info-modal-head .smash-kicker {
  color: rgba(226, 234, 255, 0.95);
}

.smash-game--dark .info-list li {
  color: rgba(210, 220, 255, 0.88);
}

@media (max-width: 980px) {
  .mission-strip {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .hud-row {
    display: grid;
  }
}

@media (max-width: 760px) {
  .mission-strip,
  .mini-stats {
    grid-template-columns: 1fr;
    display: grid;
  }
}
</style>
  