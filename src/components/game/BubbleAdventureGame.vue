<template>
  <section class="bubble-adventure" :class="{ 'bubble-adventure--dark': isDarkMode }">
    <div class="bubble-scene" aria-hidden="true">
      <div class="bubble-scene__water"></div>
      <div class="bubble-scene__beams"></div>
      <div class="bubble-scene__caustic"></div>
      <div class="bubble-scene__surface"></div>
    </div>

    <div class="bubble-scene-front" aria-hidden="true">
      <span
        v-for="b in sceneBubbles"
        :key="`sb-${b.id}`"
        class="scene-bubble"
        :style="{
          left: `${b.left}%`,
          width: `${b.size}px`,
          height: `${b.size}px`,
          animationDelay: `${b.delay}s`,
          animationDuration: `${b.duration}s`,
        }"
      ></span>

      <svg class="scene-jelly scene-jelly-1" viewBox="0 0 120 160" aria-hidden="true">
        <ellipse cx="60" cy="42" rx="44" ry="36" fill="rgba(255, 126, 179, 0.92)" />
        <ellipse cx="60" cy="38" rx="32" ry="22" fill="rgba(255, 255, 255, 0.42)" />
        <path d="M30 70 Q34 110 28 150" stroke="rgba(255, 126, 179, 0.85)" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        <path d="M48 76 Q52 120 46 158" stroke="rgba(255, 126, 179, 0.85)" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        <path d="M72 76 Q68 122 74 158" stroke="rgba(255, 126, 179, 0.85)" stroke-width="3.5" fill="none" stroke-linecap="round"/>
        <path d="M90 70 Q86 112 92 150" stroke="rgba(255, 126, 179, 0.85)" stroke-width="3.5" fill="none" stroke-linecap="round"/>
      </svg>

      <svg class="scene-jelly scene-jelly-2" viewBox="0 0 120 160" aria-hidden="true">
        <ellipse cx="60" cy="42" rx="36" ry="30" fill="rgba(155, 114, 255, 0.9)" />
        <ellipse cx="60" cy="38" rx="26" ry="18" fill="rgba(255, 255, 255, 0.4)" />
        <path d="M36 64 Q40 100 34 140" stroke="rgba(155, 114, 255, 0.85)" stroke-width="3" fill="none" stroke-linecap="round"/>
        <path d="M52 70 Q56 108 50 148" stroke="rgba(155, 114, 255, 0.85)" stroke-width="3" fill="none" stroke-linecap="round"/>
        <path d="M68 70 Q64 108 70 148" stroke="rgba(155, 114, 255, 0.85)" stroke-width="3" fill="none" stroke-linecap="round"/>
        <path d="M84 64 Q80 100 86 140" stroke="rgba(155, 114, 255, 0.85)" stroke-width="3" fill="none" stroke-linecap="round"/>
      </svg>

      <svg class="scene-fish" viewBox="0 0 80 40" aria-hidden="true">
        <path d="M10 20 Q30 4 56 20 Q30 36 10 20 Z" fill="rgba(58, 168, 255, 0.95)" />
        <path d="M56 20 L72 8 L72 32 Z" fill="rgba(58, 168, 255, 0.95)" />
        <circle cx="22" cy="18" r="2.8" fill="#0a2f4a" />
        <circle cx="22.6" cy="17.2" r="1" fill="#fff" />
      </svg>

      <svg class="scene-fish scene-fish-2" viewBox="0 0 80 40" aria-hidden="true">
        <path d="M10 20 Q30 4 56 20 Q30 36 10 20 Z" fill="rgba(255, 154, 62, 0.92)" />
        <path d="M56 20 L72 8 L72 32 Z" fill="rgba(255, 154, 62, 0.92)" />
        <circle cx="22" cy="18" r="2.6" fill="#3d1a08" />
        <circle cx="22.6" cy="17.2" r="0.9" fill="#fff" />
      </svg>
    </div>

    <section class="mission-grid">
      <div class="mission-card">
        <div class="mission-head">
          <div>
            <p class="panel-label">Bubble mission</p>
            <h4>Pop {{ activeCategoryMeta.label }}</h4>
          </div>
          <button type="button" class="info-btn" @click="showInfo = true" aria-label="Show bubble game info">i</button>
        </div>
        <div class="mission-progress">
          <span class="progress-fill" :style="{ width: `${roundProgress}%` }"></span>
        </div>
        <small>{{ collected }} / {{ currentRound.targetCount }} popped</small>
      </div>

      <div class="stats-card">
        <div class="stat-pill">
          <span>Round</span>
          <strong>{{ roundIndex + 1 }} / {{ rounds.length }}</strong>
        </div>
        <div class="stat-pill">
          <span>Score</span>
          <strong>{{ score }}</strong>
        </div>
        <div class="stat-pill">
          <span>Combo</span>
          <strong>x{{ combo }}</strong>
        </div>
        <div class="stat-pill">
          <span>Bubbles</span>
          <strong>{{ bubbleCount }}</strong>
        </div>
      </div>
    </section>

    <section class="stage-shell">
      <div class="stage-scene">
        <div class="scene-deco fruit-one" aria-hidden="true"></div>
        <div class="scene-deco fruit-two" aria-hidden="true"></div>
        <div class="scene-deco wave-one" aria-hidden="true"></div>
        <div class="scene-deco wave-two" aria-hidden="true"></div>
        <div class="scene-glow" aria-hidden="true"></div>

        <div class="hud-row">
          <div class="message-card" :class="message.tone">
            <strong>{{ message.title }}</strong>
            <span>{{ message.text }}</span>
          </div>
          <div class="target-chip">
            <span class="target-dot" :style="{ background: activeCategoryMeta.accent }"></span>
            <span>Now popping: {{ activeCategoryMeta.label }}</span>
          </div>
        </div>

        <div ref="stageRef" class="bubble-stage">
          <div class="stage-toolbar">
            <button type="button" class="mix-btn inside-stage" @click="produceBubbles()">
              Add bubbles
            </button>
          </div>

          <div
            v-for="bubble in bubbles"
            :key="bubble.id"
            class="bubble"
            :class="[
              `type-${bubble.category}`,
              {
                target: bubble.category === currentRound.targetCategory,
                giant: bubble.isGiant,
                'bubble--single': isSingleWord(bubble.word),
              },
            ]"
            :style="bubbleStyle(bubble)"
            @click="popBubble(bubble)"
          >
            <span class="bubble-word">{{ formatBubbleWord(bubble.word) }}</span>
          </div>

          <div
            v-for="burst in burstEffects"
            :key="burst.id"
            class="bubble-burst"
            :style="burstStyle(burst)"
          >
            <span>{{ burst.text }}</span>
          </div>

          <div v-if="overlayCard" class="overlay-card" :class="overlayCard.tone">
            <p class="overlay-kicker">{{ overlayCard.kicker }}</p>
            <h4>{{ overlayCard.title }}</h4>
            <p>{{ overlayCard.text }}</p>
            <button v-if="overlayCard.action" type="button" class="overlay-btn" @click="overlayCard.action()">
              {{ overlayCard.actionLabel }}
            </button>
          </div>
        </div>
      </div>
    </section>
    <div v-if="showInfo" class="info-modal-backdrop" @click.self="showInfo = false">
      <div class="info-modal">
        <div class="info-modal-head">
          <div>
            <p class="panel-label">How to play</p>
            <h4>Healthy Bubble Game</h4>
          </div>
          <button type="button" class="info-close" @click="showInfo = false" aria-label="Close info">×</button>
        </div>
        <ul class="info-list">
          <li>Tap the bright target bubbles as fast as you can.</li>
          <li>Skip the wrong bubble words so your combo keeps growing.</li>
          <li>Use the bubble button anytime to make more bubbles appear.</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from "vue"
import { injectKidsTheme } from "../../composables/useKidsTheme.js"

const { isDarkMode } = injectKidsTheme()

const initialBubbleCount = 20
const bubbleBatchSize = 8
const maxBubbleCount = 48
const minimumBubbleCount = 12

const categoryMeta = {
  food: {
    label: "healthy food choices",
    chip: "Food",
    accent: "#69c86b",
    shadow: "rgba(105, 200, 107, 0.34)",
    points: 12,
  },
  healthy: {
    label: "healthy choices",
    chip: "Habit",
    accent: "#62b6ff",
    shadow: "rgba(98, 182, 255, 0.34)",
    points: 12,
  },
  funny: {
    label: "funny choices",
    chip: "Funny",
    accent: "#ff8bb9",
    shadow: "rgba(255, 139, 185, 0.34)",
    points: 8,
  },
}

const wordPools = {
  food: [
    "apple",
    "banana",
    "berries",
    "carrots",
    "yogurt",
    "water",
    "orange",
    "pear",
    "toast",
    "oatmeal",
    "veggies",
    "cucumber",
    "cheese",
    "egg",
    "hummus",
    "avocado",
    "rice",
    "corn",
    "spinach",
    "trail mix",
    "melon",
    "salad",
  ],
  healthy: [
    "hydrate",
    "bike ride",
    "play outside",
    "stretch",
    "bedtime",
    "brush teeth",
    "family walk",
    "breathe",
    "dance",
    "wash hands",
    "story time",
    "screen break",
    "pack lunch",
    "sleep early",
    "tidy toys",
    "sunshine",
    "sunscreen",
    "breakfast",
    "jump rope",
    "fruit snack",
    "refill",
  ],
  funny: [
    "banana board",
    "moon sandwich",
    "pickle dance",
    "rocket radish",
    "giggle noodles",
    "laugh lettuce",
    "pea pirate",
    "sleepy pineapple",
    "oat alien",
    "tomato bounce",
    "rainbow sneeze",
    "broccoli shades",
    "waffle whisper",
    "jelly boots",
    "carrot hat",
    "brush song",
    "yogurt rocket",
    "celery hero",
    "gum broccoli",
    "marsh backpack",
    "pickle parade",
    "tickle taco",
  ],
}

const rounds = [
  {
    id: "food",
    title: "Healthy Food Choices",
    targetCategory: "food",
    targetCount: 12,
    story: "Food words fill the board.",
    objective: "Find the healthy food bubbles.",
  },
  {
    id: "healthy",
    title: "Healthy Choices",
    targetCategory: "healthy",
    targetCount: 12,
    story: "Habit words are drifting in.",
    objective: "Pop the healthy choice bubbles.",
  },
  {
    id: "funny",
    title: "Funny Choice Finder",
    targetCategory: "funny",
    targetCount: 10,
    story: "Now the silly words arrive.",
    objective: "Catch the funny choice bubbles.",
  },
]

const stageRef = ref(null)
const bubbles = ref([])

const sceneBubbles = Array.from({ length: 18 }, (_, id) => ({
  id,
  left: Math.random() * 100,
  size: 8 + Math.random() * 28,
  delay: Math.random() * 8,
  duration: 9 + Math.random() * 8,
}))
const burstEffects = ref([])
const score = ref(0)
const combo = ref(0)
const bestCombo = ref(0)
const wrongPops = ref(0)
const collected = ref(0)
const roundIndex = ref(0)
const gameState = ref("playing")
const stage = reactive({ width: 980, height: 560 })
const message = reactive({
  title: "Bubble stream is ready",
  text: "Tap the glowing target words and let the lighter bubbles drift past.",
  tone: "info",
})

let animationFrame = null
let nextBubbleId = 1
let nextBurstId = 1
let lastFrameAt = 0
let roundTimer = null
const showInfo = ref(false)

const currentRound = computed(() => rounds[roundIndex.value] ?? rounds[0])
const activeCategoryMeta = computed(() => categoryMeta[currentRound.value.targetCategory])
const bubbleCount = computed(() => bubbles.value.length)
const roundProgress = computed(() =>
  Math.min(100, Math.round((collected.value / currentRound.value.targetCount) * 100))
)

const overlayCard = computed(() => {
  if (gameState.value === "playing") return null
  if (gameState.value === "won") {
    return {
      kicker: "Game complete",
      title: "You finished the healthy bubble board",
      text: `Final score: ${score.value}. Press play again for a new random word mix.`,
      tone: "success",
      actionLabel: "Play again",
      action: restartGame,
    }
  }
  return {
    kicker: "Next round",
    title: "Get ready for a new target",
    text: "Fresh words are coming in now.",
    tone: "info",
  }
})

function setMessage(title, text, tone = "info") {
  message.title = title
  message.text = text
  message.tone = tone
}

function formatBubbleWord(word) {
  const parts = String(word).trim().split(/\s+/).filter(Boolean)
  if (parts.length <= 1) return word
  if (parts.length === 2) return `${parts[0]}\n${parts[1]}`
  const middle = Math.ceil(parts.length / 2)
  return `${parts.slice(0, middle).join(" ")}\n${parts.slice(middle).join(" ")}`
}

function isSingleWord(word) {
  return !/\s/.test(String(word).trim())
}

function pickRandom(list) {
  return list[Math.floor(Math.random() * list.length)]
}

function weightedCategory() {
  const target = currentRound.value.targetCategory
  const roll = Math.random()
  if (roll < 0.48) return target

  const others = Object.keys(categoryMeta).filter(category => category !== target)
  return pickRandom(others)
}

function randomBubblePosition(radius) {
  return {
    x: radius + Math.random() * Math.max(10, stage.width - radius * 2),
    y: radius + Math.random() * Math.max(10, stage.height - radius * 2),
  }
}

function spawnBubbleAtBottom(bubble) {
  bubble.x = bubble.radius + Math.random() * Math.max(10, stage.width - bubble.radius * 2)
  bubble.y = stage.height + bubble.radius * (0.4 + Math.random() * 0.8)
  bubble.vx = (Math.random() - 0.5) * 0.45
  bubble.vy = -(0.75 + Math.random() * 0.85)
  bubble.wobble = Math.random() * Math.PI * 2
  bubble.spin = -8 + Math.random() * 16
  bubble.ageMs = 0
  bubble.lifeRatio = 1
}

function createBubble(categoryOverride = null, startMode = "stage") {
  const category = categoryOverride ?? weightedCategory()
  const isTarget = category === currentRound.value.targetCategory
  const word = pickRandom(wordPools[category])
  const textLength = word.length
  const isGiant = isTarget ? Math.random() < 0.18 : Math.random() < 0.08
  const baseRadius = isGiant ? 58 + Math.random() * 14 : 40 + Math.random() * 16
  const textRadiusBoost = Math.min(36, Math.max(0, textLength - 5) * 3.4)
  const radius = baseRadius + textRadiusBoost
  const position = randomBubblePosition(radius)
  const maxAgeMs = 22000 + Math.random() * 12000
  const paletteIndex = Math.floor(Math.random() * 50)
  const hueBase = (paletteIndex * 7.2 + Math.random() * 4) % 360
  const hueShift = 18 + Math.random() * 24
  const bubble = {
    id: nextBubbleId++,
    category,
    word,
    x: position.x,
    y: position.y,
    vx: (Math.random() - 0.5) * 0.55,
    vy: -(0.4 + Math.random() * 0.5),
    radius,
    mass: Math.max(0.8, radius * radius * 0.0075),
    isGiant,
    drift: 0.9 + Math.random() * 0.45,
    wobble: Math.random() * Math.PI * 2,
    spin: Math.random() * 18 - 9,
    buoyancy: 0.1 + Math.random() * 0.06,
    drag: 0.028 + Math.random() * 0.016,
    hueBase,
    hueShift,
    alphaOuter: 0.32 + Math.random() * 0.08,
    alphaMid: 0.24 + Math.random() * 0.08,
    alphaInner: 0.16 + Math.random() * 0.06,
    ageMs: 0,
    maxAgeMs,
    lifeRatio: 1,
  }

  if (startMode === "bottom") {
    spawnBubbleAtBottom(bubble)
  } else {
    bubble.y = Math.max(radius, Math.min(stage.height - radius, bubble.y))
  }

  return bubble
}

function addBubbleWithSpacing(categoryOverride = null, startMode = "stage") {
  const bubble = createBubble(categoryOverride, startMode)
  for (let attempt = 0; attempt < 18; attempt += 1) {
    const overlap = bubbles.value.some(existing => {
      const dx = existing.x - bubble.x
      const dy = existing.y - bubble.y
      return Math.hypot(dx, dy) < existing.radius + bubble.radius + 10
    })
    if (!overlap) break
    if (startMode === "bottom") {
      spawnBubbleAtBottom(bubble)
    } else {
      const position = randomBubblePosition(bubble.radius)
      bubble.x = position.x
      bubble.y = position.y
    }
  }
  bubbles.value.push(bubble)
}

function seedBubbles(count, startMode = "stage") {
  for (let i = 0; i < count; i += 1) {
    if (bubbles.value.length >= maxBubbleCount) break
    addBubbleWithSpacing(null, startMode)
  }
}

function produceBubbles(count = bubbleBatchSize) {
  const desired = Math.max(1, count)
  let room = maxBubbleCount - bubbles.value.length

  if (room < desired) {
    const overflow = desired - room
    bubbles.value.splice(0, overflow)
    room = maxBubbleCount - bubbles.value.length
  }

  const amount = Math.max(1, Math.min(desired, room))
  seedBubbles(amount, "bottom")
  setMessage("Fresh bubbles mixed", `${amount} light bubbles floated in.`, "success")
}

function measureStage() {
  if (!stageRef.value) return
  const rect = stageRef.value.getBoundingClientRect()
  stage.width = rect.width
  stage.height = rect.height
}

function applyBubbleForces(bubble, stepScale, now) {
  const currentX = Math.sin((bubble.y + now * 0.052 + bubble.id * 17) / 56) * 0.036 * bubble.drift
  const currentY = Math.cos((bubble.x + now * 0.02 + bubble.id * 11) / 72) * 0.01 * bubble.drift
  const buoyancy = -bubble.buoyancy * (1.08 - bubble.radius / 120)
  const centerX = (stage.width * 0.5 - bubble.x) * 0.0002
  const upperLift = bubble.y < stage.height * 0.22 ? -0.015 : 0
  const lowerLift = bubble.y > stage.height * 0.78 ? -0.022 : 0

  bubble.vx += (currentX + centerX) * stepScale
  bubble.vy += (buoyancy + currentY + upperLift + lowerLift) * stepScale
  bubble.vx += Math.sin((now * 0.004 + bubble.id) + bubble.wobble) * 0.012 * stepScale
  bubble.vy += Math.cos((now * 0.0035 + bubble.id) + bubble.wobble) * 0.003 * stepScale
}

function integrateBubble(bubble, stepScale) {
  const damping = Math.pow(1 - bubble.drag, stepScale)
  bubble.vx *= damping
  bubble.vy *= damping
  bubble.vx = Math.max(-2.2, Math.min(2.2, bubble.vx))
  bubble.vy = Math.max(-3.2, Math.min(1.1, bubble.vy))
  bubble.x += bubble.vx * stepScale
  bubble.y += bubble.vy * stepScale
  bubble.spin += (bubble.vx * 0.12) * stepScale
}

function keepBubbleInBounds(bubble) {
  if (bubble.x <= bubble.radius || bubble.x >= stage.width - bubble.radius) {
    bubble.vx *= -0.78
    bubble.x = Math.max(bubble.radius, Math.min(stage.width - bubble.radius, bubble.x))
  }
  if (bubble.y <= -bubble.radius * 1.3) {
    spawnBubbleAtBottom(bubble)
    return
  }
  if (bubble.y >= stage.height + bubble.radius * 1.2) {
    bubble.y = stage.height + bubble.radius * 0.4
    bubble.vy = -Math.abs(bubble.vy) * 0.92
  }
}

function bubbleStyle(bubble) {
  const meta = categoryMeta[bubble.category]
  const hueA = bubble.hueBase
  const hueB = (bubble.hueBase + bubble.hueShift) % 360
  const hueC = (bubble.hueBase + bubble.hueShift * 1.8) % 360
  const targetGlow = bubble.category === currentRound.value.targetCategory ? meta.shadow : `hsla(${hueB}, 85%, 78%, 0.16)`
  const trimmedWord = String(bubble.word).trim()
  const wordLength = Math.max(1, trimmedWord.length)
  const singleWord = !/\s/.test(trimmedWord)
  const baseFont = bubble.radius / (wordLength > 14 ? 72 : wordLength > 10 ? 62 : 54)
  // Bubble has 10px padding all around; chip will use ~6px padding when single.
  // Available text width = (2r - 20) - 12 = 2r - 32
  const innerWidthPx = Math.max(20, bubble.radius * 2 - 32)
  // For bold sans-serif, average char width  font-size * 0.6
  const fitFontRem = singleWord ? innerWidthPx / (wordLength * 0.6 * 16) : baseFont
  const dynamicFont = singleWord
    ? Math.max(0.42, Math.min(0.96, fitFontRem))
    : Math.max(0.54, Math.min(0.98, baseFont))
  return {
    width: `${bubble.radius * 2}px`,
    height: `${bubble.radius * 2}px`,
    transform: `translate3d(${bubble.x - bubble.radius}px, ${bubble.y - bubble.radius}px, 0)`,
    background: `radial-gradient(circle at 32% 24%, rgba(255,255,255,0.98) 0%, rgba(255,255,255,0.68) 12%, rgba(255,255,255,0.28) 24%, hsla(${hueA}, 96%, 80%, ${bubble.alphaInner}) 48%, hsla(${hueB}, 92%, 69%, ${bubble.alphaMid}) 72%, hsla(${hueC}, 88%, 58%, ${bubble.alphaOuter}) 100%)`,
    boxShadow: `0 0 0 2px rgba(255,255,255,0.48), 0 12px 24px rgba(67, 101, 173, 0.18), 0 0 28px ${targetGlow}, inset -18px -20px 24px rgba(255,255,255,0.16), inset 10px 12px 18px rgba(255,255,255,0.22)`,
    "--bubble-font-size": `${dynamicFont}rem`,
    "--bubble-text-color": "rgba(18, 34, 64, 0.98)",
    "--bubble-text-shadow": bubble.category === currentRound.value.targetCategory
      ? "0 1px 0 rgba(255,255,255,0.65)"
      : "0 1px 0 rgba(255,255,255,0.72)",
    "--bubble-text-bg": bubble.category === currentRound.value.targetCategory
      ? "rgba(255,255,255,0.82)"
      : "rgba(255,255,255,0.88)",
    "--bubble-highlight-a": `hsla(${hueA}, 100%, 99%, 0.94)`,
    "--bubble-highlight-b": `hsla(${hueB}, 96%, 98%, 0.3)`,
    "--bubble-outline": `hsla(${hueC}, 96%, 100%, 0.48)`,
    "--bubble-glow": targetGlow,
  }
}

function burstStyle(burst) {
  return {
    width: `${burst.size}px`,
    height: `${burst.size}px`,
    left: `${burst.x - burst.size / 2}px`,
    top: `${burst.y - burst.size / 2}px`,
    borderColor: burst.color,
  }
}

function spawnBurst(bubble, text, color) {
  burstEffects.value.push({
    id: nextBurstId++,
    x: bubble.x,
    y: bubble.y,
    size: bubble.radius * 2.2,
    text,
    color,
    createdAt: performance.now(),
  })
}

function removeBubble(bubbleId) {
  bubbles.value = bubbles.value.filter(bubble => bubble.id !== bubbleId)
}

function popBubble(bubble) {
  if (gameState.value !== "playing") return

  const meta = categoryMeta[bubble.category]

  if (bubble.category === currentRound.value.targetCategory) {
    combo.value += 1
    bestCombo.value = Math.max(bestCombo.value, combo.value)
    collected.value += 1
    score.value += meta.points + Math.max(0, combo.value - 1) * 3 + (bubble.isGiant ? 6 : 0)
    spawnBurst(bubble, `+${meta.points}`, meta.accent)
    setMessage("Nice catch", `${bubble.word} fits this round.`, "success")
  } else {
    combo.value = 0
    wrongPops.value += 1
    score.value = Math.max(0, score.value - 6)
    spawnBurst(bubble, "oops", meta.accent)
    setMessage("Wrong bubble", `${bubble.word} is not the target.`, "danger")
  }

  removeBubble(bubble.id)

  if (collected.value >= currentRound.value.targetCount) {
    completeRound()
  }
}

function completeRound() {
  gameState.value = "transition"
  combo.value = 0
  setMessage("Round complete", `You finished ${currentRound.value.title}.`, "success")

  window.clearTimeout(roundTimer)
  roundTimer = window.setTimeout(() => {
    if (roundIndex.value === rounds.length - 1) {
      gameState.value = "won"
      setMessage("Board complete", "You finished all healthy bubble rounds.", "success")
      return
    }

    roundIndex.value += 1
    collected.value = 0
    combo.value = 0
    bubbles.value = []
    gameState.value = "playing"
    seedBubbles(initialBubbleCount)
    setMessage("New target", currentRound.value.story, "info")
  }, 1200)
}

function restartGame() {
  window.clearTimeout(roundTimer)
  roundIndex.value = 0
  score.value = 0
  combo.value = 0
  bestCombo.value = 0
  wrongPops.value = 0
  collected.value = 0
  bubbles.value = []
  gameState.value = "playing"
  seedBubbles(initialBubbleCount)
  setMessage("Fresh game", rounds[0].story, "info")
}

function pruneBursts() {
  const now = performance.now()
  burstEffects.value = burstEffects.value.filter(effect => now - effect.createdAt < 460)
}

function recycleBubble(bubble, categoryOverride = null) {
  bubble.category = categoryOverride ?? weightedCategory()
  bubble.word = pickRandom(wordPools[bubble.category])
  bubble.isGiant = bubble.category === currentRound.value.targetCategory ? Math.random() < 0.18 : Math.random() < 0.08
  const textLength = bubble.word.length
  const baseRadius = bubble.isGiant ? 58 + Math.random() * 14 : 40 + Math.random() * 16
  const textRadiusBoost = Math.min(36, Math.max(0, textLength - 5) * 3.4)
  bubble.radius = baseRadius + textRadiusBoost
  bubble.mass = Math.max(0.8, bubble.radius * bubble.radius * 0.0075)
  bubble.drift = 0.9 + Math.random() * 0.45
  bubble.buoyancy = 0.1 + Math.random() * 0.06
  bubble.drag = 0.028 + Math.random() * 0.016
  bubble.hueBase = (Math.floor(Math.random() * 50) * 7.2 + Math.random() * 4) % 360
  bubble.hueShift = 18 + Math.random() * 24
  bubble.alphaOuter = 0.32 + Math.random() * 0.08
  bubble.alphaMid = 0.24 + Math.random() * 0.08
  bubble.alphaInner = 0.16 + Math.random() * 0.06
  bubble.maxAgeMs = 22000 + Math.random() * 12000
  spawnBubbleAtBottom(bubble)
}

function updateBubbleLifetimes(deltaMs) {
  for (const bubble of bubbles.value) {
    bubble.ageMs += deltaMs
    bubble.lifeRatio = Math.max(0.35, 1 - bubble.ageMs / bubble.maxAgeMs)
    if (bubble.ageMs >= bubble.maxAgeMs) {
      recycleBubble(bubble)
    }
  }
}

function tick(now) {
  pruneBursts()

  const deltaMs = lastFrameAt ? Math.min(26, now - lastFrameAt) : 16.67
  lastFrameAt = now
  const stepScale = deltaMs / 16.67
  const substeps = deltaMs > 18 ? 2 : 1

  if (gameState.value === "playing") {
    for (let pass = 0; pass < substeps; pass += 1) {
      const localScale = stepScale / substeps
      for (const bubble of bubbles.value) {
        applyBubbleForces(bubble, localScale, now)
        integrateBubble(bubble, localScale)
        keepBubbleInBounds(bubble)
      }
    }

    updateBubbleLifetimes(deltaMs)

    if (bubbles.value.length < minimumBubbleCount) {
      seedBubbles(minimumBubbleCount - bubbles.value.length, "bottom")
    }
  }

  animationFrame = window.requestAnimationFrame(tick)
}

function handleResize() {
  measureStage()
}

onMounted(() => {
  measureStage()
  seedBubbles(initialBubbleCount)
  setMessage("Bubble stream is ready", currentRound.value.story, "info")
  lastFrameAt = performance.now()
  animationFrame = window.requestAnimationFrame(tick)
  window.addEventListener("resize", handleResize)
})

onBeforeUnmount(() => {
  if (animationFrame) window.cancelAnimationFrame(animationFrame)
  window.clearTimeout(roundTimer)
  window.removeEventListener("resize", handleResize)
})
</script>

<style scoped>
.bubble-adventure {
  --coral: #FF6058;
  --sky: #3B9EFF;
  --mint: #2CC97A;
  --amber: #FFB020;
  --violet: #9B72FF;
  --rose: #FF7EB3;
  --ink: #18192B;
  --ink2: #444562;
  --muted: #9395A8;
  color: #173055;
  font-family: "DM Sans", sans-serif;
  position: relative;
  overflow: hidden;
  border-radius: 28px;
}

/* === Underwater scene === */
.bubble-scene {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  border-radius: inherit;
  overflow: hidden;
}

.bubble-scene__water {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, #b4e3ff 0%, #7ec8ee 30%, #4ea4dc 65%, #1f6cb0 100%);
  opacity: 1;
}

.bubble-adventure--dark .bubble-scene__water {
  background: linear-gradient(180deg, #06112a 0%, #0a1e44 35%, #0e2c6a 65%, #15356e 100%);
  opacity: 1;
}

.bubble-scene__beams {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(105deg, transparent 30%, rgba(255, 255, 255, 0.55) 32%, transparent 34%) no-repeat,
    linear-gradient(115deg, transparent 50%, rgba(255, 255, 255, 0.4) 53%, transparent 56%) no-repeat,
    linear-gradient(95deg, transparent 70%, rgba(255, 255, 255, 0.5) 73%, transparent 76%) no-repeat;
  mix-blend-mode: screen;
  opacity: 0.55;
  animation: beamSway 14s ease-in-out infinite alternate;
}

.bubble-adventure--dark .bubble-scene__beams {
  opacity: 0.22;
}

@keyframes beamSway {
  from { transform: translateX(-20px) skewX(-2deg); }
  to   { transform: translateX(20px) skewX(2deg); }
}

.bubble-scene__caustic {
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 0.35) 0%, transparent 8%),
    radial-gradient(circle at 70% 35%, rgba(255, 255, 255, 0.3) 0%, transparent 7%),
    radial-gradient(circle at 50% 60%, rgba(255, 255, 255, 0.32) 0%, transparent 8%),
    radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.28) 0%, transparent 7%),
    radial-gradient(circle at 85% 75%, rgba(255, 255, 255, 0.3) 0%, transparent 7%);
  mix-blend-mode: overlay;
  animation: causticShift 18s ease-in-out infinite alternate;
}

@keyframes causticShift {
  from { transform: translate(0, 0) scale(1); opacity: 0.55; }
  to   { transform: translate(18px, -10px) scale(1.06); opacity: 0.9; }
}

.bubble-scene__surface {
  position: absolute;
  top: 0;
  left: -10%;
  width: 120%;
  height: 18px;
  background:
    radial-gradient(circle at 0 100%, transparent 12px, rgba(255, 255, 255, 0.4) 13px, transparent 16px) repeat-x,
    linear-gradient(180deg, rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0));
  background-size: 26px 18px, 100% 100%;
  animation: surfaceSlide 9s linear infinite;
}

@keyframes surfaceSlide {
  from { background-position: 0 0, 0 0; }
  to   { background-position: 52px 0, 0 0; }
}

.bubble-scene-front {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
  border-radius: inherit;
}

.scene-bubble {
  position: absolute;
  bottom: -40px;
  border-radius: 50%;
  background:
    radial-gradient(circle at 30% 28%, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.55) 38%, rgba(180, 220, 255, 0.32) 75%, transparent 100%);
  box-shadow: inset -2px -3px 6px rgba(58, 139, 208, 0.28), 0 0 10px rgba(255, 255, 255, 0.55);
  animation: sceneBubbleRise linear infinite;
  opacity: 1;
}

.bubble-adventure--dark .scene-bubble {
  background:
    radial-gradient(circle at 30% 28%, rgba(255, 255, 255, 0.65), rgba(180, 220, 255, 0.18) 50%, transparent 100%);
}

@keyframes sceneBubbleRise {
  0%   { transform: translateY(0) translateX(0); opacity: 0; }
  10%  { opacity: 0.8; }
  50%  { transform: translateY(-50vh) translateX(20px); }
  100% { transform: translateY(-120vh) translateX(-30px); opacity: 0; }
}

.scene-jelly {
  position: absolute;
  width: 80px;
  height: 110px;
  filter: drop-shadow(0 8px 20px rgba(255, 126, 179, 0.5));
  animation: jellyFloat 12s ease-in-out infinite alternate;
}

.scene-jelly-1 { right: 3%; top: 22%; }
.scene-jelly-2 { left: 3%; top: 60%; width: 64px; height: 90px; animation-duration: 14s; animation-delay: -3s; }

@keyframes jellyFloat {
  0%, 100% { transform: translateY(0) rotate(-3deg); }
  50%      { transform: translateY(-22px) rotate(4deg); }
}

.scene-fish {
  position: absolute;
  width: 76px;
  height: 38px;
  right: -90px;
  top: 80%;
  filter: drop-shadow(0 6px 14px rgba(58, 168, 255, 0.5));
  animation: fishSwim 22s linear infinite;
}

.scene-fish-2 {
  width: 60px;
  height: 30px;
  top: 30%;
  right: -90px;
  animation-duration: 28s;
  animation-delay: -6s;
  filter: drop-shadow(0 6px 14px rgba(255, 154, 62, 0.5));
}

@keyframes fishSwim {
  0%   { transform: translateX(0) translateY(0); }
  45%  { transform: translateX(-80vw) translateY(-30px); }
  50%  { transform: translateX(-80vw) translateY(-30px) scaleX(-1); }
  95%  { transform: translateX(0) translateY(10px) scaleX(-1); }
  100% { transform: translateX(0) translateY(10px); }
}

.mission-grid,
.stage-shell,
.victory-overlay {
  position: relative;
  z-index: 3;
}

.mission-card,
.stats-card,
.stage-scene {
  border-radius: 24px;
  background:
    radial-gradient(circle at 12% 18%, rgba(255, 176, 32, 0.18), transparent 22%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(248, 244, 255, 0.95));
  border: 1px solid rgba(86, 109, 184, 0.14);
  box-shadow: 0 18px 30px rgba(33, 52, 106, 0.1);
  padding: 18px;
}

.panel-label,
.overlay-kicker {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.76rem;
  color: var(--violet);
  font-weight: 900;
}

.mission-card p,
.message-card span {
  color: #556586;
  line-height: 1.6;
}

.mission-grid {
  margin-top: 16px;
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 14px;
}

.mission-card h4 {
  margin: 8px 0 0;
  font-size: 1.15rem;
  font-family: "Baloo 2", cursive;
  color: var(--ink);
}

.mission-progress {
  margin-top: 12px;
  height: 12px;
  border-radius: 999px;
  background: rgba(92, 114, 196, 0.12);
  overflow: hidden;
}

.progress-fill {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--sky) 0%, var(--violet) 60%, var(--rose) 100%);
  background-size: 200% 100%;
  animation: progressGlow 2.8s linear infinite;
}

.mission-card small {
  display: block;
  margin-top: 8px;
  color: #536286;
  font-weight: 800;
  font-size: 0.8rem;
}

.stats-card {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.stat-pill {
  border-radius: 18px;
  padding: 10px 12px;
  background: linear-gradient(135deg, rgba(255, 244, 246, 0.96), rgba(244, 240, 255, 0.92));
  box-shadow: 0 10px 18px rgba(33, 52, 106, 0.08);
  animation: bubblePillBounce 4.4s ease-in-out infinite;
}

.stat-pill:nth-child(2) {
  background: linear-gradient(135deg, rgba(235, 248, 255, 0.98), rgba(230, 244, 255, 0.92));
}

.stat-pill:nth-child(3) {
  background: linear-gradient(135deg, rgba(245, 238, 255, 0.98), rgba(255, 236, 246, 0.92));
}

.stat-pill:nth-child(4) {
  background: linear-gradient(135deg, rgba(238, 255, 244, 0.98), rgba(236, 251, 255, 0.92));
}

.stat-pill span {
  display: block;
  color: #63739d;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.stat-pill strong {
  display: block;
  margin-top: 6px;
  font-size: 1.18rem;
  color: #21345f;
  font-family: "Baloo 2", cursive;
}

.mission-head {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 10px;
}

.mix-btn {
  border: 0;
  border-radius: 999px;
  min-height: 48px;
  padding: 0 20px;
  background: linear-gradient(135deg, #ff7a55 0%, #ffb85a 100%);
  color: #fff;
  font-weight: 900;
  cursor: pointer;
  font-family: "Baloo 2", cursive;
  box-shadow: 0 12px 26px rgba(255, 152, 70, 0.24);
  animation: bubblePulse 3.2s ease-in-out infinite;
}

.stage-shell {
  margin-top: 16px;
}

.stage-scene {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(circle at 14% 18%, rgba(157, 228, 255, 0.48), transparent 26%),
    radial-gradient(circle at 86% 18%, rgba(255, 171, 203, 0.24), transparent 28%),
    radial-gradient(circle at 50% 90%, rgba(44, 201, 122, 0.14), transparent 28%),
    linear-gradient(180deg, #fafcff 0%, #ebf6ff 38%, #f3f0ff 100%);
}

.hud-row {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 12px;
}

.message-card {
  max-width: 620px;
  border-radius: 18px;
  padding: 14px;
  border: 1px solid rgba(100, 123, 196, 0.14);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(243, 247, 255, 0.78));
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 20px rgba(33, 52, 106, 0.08);
}

.message-card strong {
  display: block;
  color: var(--ink);
  font-family: "Baloo 2", cursive;
  font-size: 1.05rem;
}

.message-card.info {
  background: linear-gradient(135deg, rgba(239, 246, 255, 0.95), rgba(223, 242, 255, 0.86));
}

.message-card.success {
  background: linear-gradient(135deg, rgba(232, 255, 242, 0.94), rgba(214, 255, 232, 0.88));
}

.message-card.danger {
  background: linear-gradient(135deg, rgba(255, 236, 242, 0.94), rgba(255, 221, 232, 0.88));
}

.target-chip {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  border-radius: 999px;
  padding: 10px 14px;
  background: linear-gradient(135deg, rgba(233, 246, 255, 0.98), rgba(229, 240, 255, 0.94));
  border: 1.5px solid rgba(87, 120, 255, 0.18);
  color: #31508c;
  font-weight: 800;
  animation: bubblePillBounce 4.2s ease-in-out infinite 0.3s;
}

.target-dot {
  width: 26px;
  height: 26px;
  border-radius: 999px;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.7);
}

.bubble-stage {
  position: relative;
  margin-top: 16px;
  min-height: 560px;
  height: 62vh;
  overflow: hidden;
  border-radius: 24px;
  border: 1px solid rgba(78, 103, 190, 0.15);
  background:
    radial-gradient(circle at 20% 14%, rgba(255, 255, 255, 0.3), transparent 28%),
    radial-gradient(circle at 82% 18%, rgba(255, 255, 255, 0.16), transparent 18%),
    linear-gradient(180deg, #67bde8 0%, #8fd0f4 30%, #b8c8f5 66%, #e4d4eb 100%);
  box-shadow: inset 0 0 80px rgba(255, 255, 255, 0.14);
  animation: stageGlow 7s ease-in-out infinite;
}

.stage-toolbar {
  position: absolute;
  right: 14px;
  top: 14px;
  z-index: 3;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 22px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.72), rgba(239, 246, 255, 0.48));
  border: 1px solid rgba(255, 255, 255, 0.42);
  box-shadow: 0 16px 28px rgba(41, 62, 121, 0.14);
}

.inside-stage {
  min-height: 42px;
  padding: 0 16px;
  box-shadow: 0 12px 22px rgba(41, 62, 121, 0.24);
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
  animation: bubblePulse 3s ease-in-out infinite;
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
    radial-gradient(circle at 100% 0%, rgba(255, 126, 179, 0.18), transparent 30%),
    radial-gradient(circle at 0% 100%, rgba(59, 158, 255, 0.18), transparent 28%),
    rgba(255, 255, 255, 0.98);
  border: 1.5px solid rgba(86, 109, 184, 0.14);
  box-shadow: 0 18px 30px rgba(33, 52, 106, 0.16);
  animation: bubblePanelFloat 5.4s ease-in-out infinite;
}

.info-modal-head {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 12px;
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

/* Dark skin when kid route shell / theme is dark */
.bubble-adventure--dark {
  --ink: #f2f7ff;
  --ink2: rgba(224, 232, 255, 0.92);
  --muted: rgba(198, 208, 240, 0.88);
  color: #e8eeff;
}

.bubble-adventure--dark .mission-card,
.bubble-adventure--dark .stats-card,
.bubble-adventure--dark .stage-scene {
  background:
    radial-gradient(circle at 12% 18%, rgba(255, 176, 32, 0.1), transparent 22%),
    linear-gradient(135deg, rgba(22, 28, 52, 0.96), rgba(14, 18, 40, 0.94));
  border-color: rgba(143, 154, 227, 0.22);
  box-shadow: 0 18px 40px rgba(3, 7, 23, 0.45);
}

.bubble-adventure--dark .panel-label,
.bubble-adventure--dark .overlay-kicker {
  color: #c4b5fd;
}

.bubble-adventure--dark .mission-card h4,
.bubble-adventure--dark .message-card strong {
  color: var(--ink);
}

.bubble-adventure--dark .stage-toolbar {
  background: linear-gradient(135deg, rgba(18, 28, 56, 0.84), rgba(14, 20, 44, 0.72));
  border-color: rgba(143, 154, 227, 0.26);
  box-shadow: 0 16px 32px rgba(3, 7, 23, 0.34);
}

.bubble-adventure--dark .mix-btn {
  background: linear-gradient(135deg, #78c7ff 0%, #8a8fff 54%, #c487ff 100%);
  color: #081224;
  box-shadow: 0 14px 28px rgba(91, 124, 255, 0.34);
}

.bubble-adventure--dark .mission-card p,
.bubble-adventure--dark .message-card span,
.bubble-adventure--dark .mission-card small {
  color: rgba(210, 220, 255, 0.88);
}

.bubble-adventure--dark .mission-progress {
  background: rgba(255, 255, 255, 0.1);
}

.bubble-adventure--dark .stat-pill {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.04));
  border: 1px solid rgba(143, 154, 227, 0.2);
  box-shadow: 0 8px 20px rgba(3, 7, 23, 0.35);
}

.bubble-adventure--dark .stat-pill:nth-child(2),
.bubble-adventure--dark .stat-pill:nth-child(3),
.bubble-adventure--dark .stat-pill:nth-child(4) {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.09), rgba(255, 255, 255, 0.04));
}

.bubble-adventure--dark .stat-pill span {
  color: rgba(198, 208, 240, 0.85);
}

.bubble-adventure--dark .stat-pill strong {
  color: #f2f7ff;
}

.bubble-adventure--dark .stage-scene {
  background:
    radial-gradient(circle at 14% 18%, rgba(59, 158, 255, 0.22), transparent 26%),
    radial-gradient(circle at 86% 18%, rgba(255, 171, 203, 0.12), transparent 28%),
    linear-gradient(180deg, rgba(14, 20, 44, 0.95) 0%, rgba(10, 14, 32, 0.98) 100%);
}

.bubble-adventure--dark .message-card {
  border-color: rgba(143, 154, 227, 0.22);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.04));
}

.bubble-adventure--dark .message-card.info {
  background: linear-gradient(135deg, rgba(59, 158, 255, 0.16), rgba(22, 28, 52, 0.88));
}

.bubble-adventure--dark .message-card.success {
  background: linear-gradient(135deg, rgba(44, 201, 122, 0.14), rgba(22, 28, 52, 0.88));
}

.bubble-adventure--dark .message-card.danger {
  background: linear-gradient(135deg, rgba(255, 126, 179, 0.14), rgba(22, 28, 52, 0.88));
}

.bubble-adventure--dark .target-chip {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.09), rgba(255, 255, 255, 0.04));
  border-color: rgba(143, 154, 227, 0.28);
  color: rgba(226, 234, 255, 0.95);
}

.bubble-adventure--dark .bubble-stage {
  border-color: rgba(143, 154, 227, 0.22);
  background:
    radial-gradient(circle at 18% 14%, rgba(114, 208, 255, 0.26), transparent 28%),
    radial-gradient(circle at 82% 18%, rgba(155, 114, 255, 0.2), transparent 22%),
    radial-gradient(circle at 50% 100%, rgba(44, 201, 122, 0.12), transparent 28%),
    linear-gradient(180deg, rgba(20, 40, 74, 0.96) 0%, rgba(13, 22, 47, 0.98) 58%, rgba(10, 16, 36, 0.98) 100%);
  box-shadow: inset 0 0 60px rgba(3, 7, 23, 0.35);
}

.bubble-adventure--dark .overlay-card {
  background: linear-gradient(135deg, rgba(22, 28, 52, 0.96), rgba(14, 18, 38, 0.96));
  border: 1px solid rgba(143, 154, 227, 0.24);
}

.bubble-adventure--dark .overlay-card h4,
.bubble-adventure--dark .overlay-card p {
  color: rgba(226, 234, 255, 0.95);
}

.bubble-adventure--dark .overlay-btn {
  color: #0f1729;
}

.bubble-adventure--dark .info-btn,
.bubble-adventure--dark .info-close {
  border-color: rgba(143, 154, 227, 0.35);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.05));
  color: #e0e7ff;
}

.bubble-adventure--dark .info-modal-backdrop {
  background: rgba(3, 7, 23, 0.62);
}

.bubble-adventure--dark .info-modal {
  background:
    radial-gradient(circle at 100% 0%, rgba(155, 114, 255, 0.12), transparent 30%),
    rgba(18, 22, 43, 0.97);
  border-color: rgba(143, 154, 227, 0.22);
}

.bubble-adventure--dark .info-modal h4 {
  color: rgba(226, 234, 255, 0.98);
}

.bubble-adventure--dark .info-list {
  color: rgba(210, 220, 255, 0.9);
}

.bubble-adventure--dark .wave-one,
.bubble-adventure--dark .wave-two {
  background: rgba(255, 255, 255, 0.06);
}

.bubble-adventure--dark .scene-glow {
  background: radial-gradient(circle, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0));
}

@keyframes bubblePillBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

@keyframes bubblePanelFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

@keyframes bubblePulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes progressGlow {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}

@keyframes sparkleDrift {
  from { transform: translateY(0); opacity: 0.72; }
  50% { opacity: 1; }
  to { transform: translateY(-16px); opacity: 0.72; }
}

@keyframes stageGlow {
  0%, 100% { box-shadow: inset 0 0 80px rgba(255, 255, 255, 0.14); }
  50% { box-shadow: inset 0 0 100px rgba(255, 255, 255, 0.2), 0 18px 34px rgba(123, 101, 255, 0.12); }
}

.bubble-stage::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at 12% 22%, rgba(255, 255, 255, 0.18), transparent 0 4px, transparent 5px),
    radial-gradient(circle at 76% 18%, rgba(255, 255, 255, 0.16), transparent 0 4px, transparent 5px),
    radial-gradient(circle at 62% 78%, rgba(255, 255, 255, 0.16), transparent 0 5px, transparent 6px),
    radial-gradient(circle at 22% 80%, rgba(255, 255, 255, 0.14), transparent 0 5px, transparent 6px);
  animation: sparkleDrift 12s linear infinite;
}

.bubble-stage::after {
  content: "";
  position: absolute;
  inset: auto -10% -24% auto;
  width: 260px;
  height: 260px;
  border-radius: 50%;
  pointer-events: none;
  background: radial-gradient(circle, rgba(255, 126, 179, 0.2), rgba(255, 126, 179, 0));
  animation: bubblePanelFloat 7s ease-in-out infinite reverse;
}

.scene-deco {
  position: absolute;
  pointer-events: none;
}

.fruit-one,
.fruit-two {
  width: 150px;
  height: 150px;
  border-radius: 999px;
  filter: blur(8px);
}

.fruit-one {
  left: -28px;
  bottom: -24px;
  background: radial-gradient(circle, rgba(122, 221, 116, 0.44), rgba(122, 221, 116, 0));
}

.fruit-two {
  right: -18px;
  top: 18px;
  background: radial-gradient(circle, rgba(255, 161, 193, 0.34), rgba(255, 161, 193, 0));
}

.wave-one,
.wave-two {
  height: 110px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.16);
}

.wave-one {
  left: 12%;
  right: 12%;
  bottom: 34px;
}

.wave-two {
  left: 20%;
  right: 20%;
  bottom: 10px;
}

.scene-glow {
  position: absolute;
  left: 50%;
  top: 52%;
  width: min(72vw, 760px);
  height: 320px;
  transform: translate(-50%, -50%);
  border-radius: 999px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0));
  filter: blur(16px);
}

.bubble {
  position: absolute;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
  transition: filter 0.12s ease, transform 0.12s ease;
  text-align: center;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid var(--bubble-outline);
  will-change: transform;
  overflow: hidden;
}

.bubble:hover {
  filter: brightness(1.08) saturate(1.04);
}

.bubble::before,
.bubble::after {
  content: "";
  position: absolute;
  border-radius: 999px;
  pointer-events: none;
}

.bubble::before {
  left: 16%;
  top: 12%;
  width: 34%;
  height: 22%;
  background: radial-gradient(circle, var(--bubble-highlight-a) 0%, rgba(255, 255, 255, 0) 76%);
  transform: rotate(-18deg);
  filter: blur(1px);
}

.bubble::after {
  inset: 7%;
  border: 1px solid var(--bubble-highlight-b);
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.05) inset,
    0 0 24px var(--bubble-glow);
}

.bubble.target {
  box-shadow:
    0 0 0 2px rgba(255, 255, 255, 0.2),
    0 0 34px var(--bubble-glow),
    inset -14px -18px 24px rgba(255,255,255,0.12),
    inset 10px 12px 18px rgba(255,255,255,0.14);
}

.bubble-word {
  position: relative;
  z-index: 1;
  width: 82%;
  max-width: 82%;
  padding: 6px 9px;
  border-radius: 18px;
  background: var(--bubble-text-bg);
  color: var(--bubble-text-color);
  font-size: calc(var(--bubble-font-size) + 0.02rem);
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: 0.01em;
  text-shadow: var(--bubble-text-shadow);
  box-shadow: 0 6px 14px rgba(102, 130, 185, 0.12);
  display: block;
  white-space: pre-line;
  overflow-wrap: anywhere;
  word-break: normal;
  text-wrap: balance;
  hyphens: none;
}

.bubble.bubble--single .bubble-word {
  width: auto;
  max-width: 94%;
  padding: 3px 6px;
  display: inline-block;
  white-space: nowrap;
  overflow: visible;
  text-align: center;
  overflow-wrap: normal;
  word-break: keep-all;
  text-wrap: nowrap;
}

.bubble-burst {
  position: absolute;
  display: grid;
  place-items: center;
  border-radius: 999px;
  border: 4px solid;
  pointer-events: none;
  animation: burst 460ms ease-out forwards;
}

.bubble-burst span {
  font-size: 0.82rem;
  font-weight: 900;
  color: #fff;
  text-shadow: 0 2px 10px rgba(31, 41, 77, 0.35);
}

@keyframes burst {
  from {
    opacity: 0.96;
    transform: scale(0.36);
  }
  to {
    opacity: 0;
    transform: scale(1.55);
  }
}

.overlay-card {
  position: absolute;
  inset: 50% auto auto 50%;
  transform: translate(-50%, -50%);
  width: min(92%, 420px);
  border-radius: 24px;
  padding: 22px;
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid rgba(95, 117, 196, 0.2);
  box-shadow: 0 24px 44px rgba(27, 41, 84, 0.24);
  text-align: center;
  z-index: 4;
}

.overlay-card h4 {
  margin: 8px 0 0;
  font-size: 1.5rem;
  color: #223860;
}

.overlay-card p:last-of-type {
  color: #556685;
  line-height: 1.6;
}

.overlay-card.success {
  background: rgba(246, 255, 250, 0.95);
}

.overlay-btn {
  border: 0;
  border-radius: 999px;
  min-height: 44px;
  padding: 0 18px;
  margin-top: 6px;
  background: linear-gradient(135deg, #2f60ea 0%, #7c43ef 100%);
  color: #fff;
  font-weight: 900;
  cursor: pointer;
}

@media (max-width: 1080px) {
  .mission-grid {
    grid-template-columns: 1fr;
  }

  .stats-card {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .hud-row {
    display: grid;
  }

  .stage-toolbar {
    left: 14px;
    right: 14px;
    top: 14px;
    display: grid;
  }

  .stats-card {
    grid-template-columns: 1fr;
  }

  .bubble-stage {
    min-height: 470px;
  }
}
</style>
