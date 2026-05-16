<template>
  <section class="bubble-adventure" :class="{ 'bubble-adventure--dark': isDarkMode }">
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
              Make more bubbles
            </button>
            <div class="toolbar-stats">
              <span>{{ autoPopped }} auto pops</span>
              <span>{{ producedTotal }} made</span>
            </div>
          </div>

          <div
            v-for="bubble in bubbles"
            :key="bubble.id"
            class="bubble"
            :class="[
              `type-${bubble.category}`,
              { target: bubble.category === currentRound.targetCategory, giant: bubble.isGiant },
            ]"
            :style="bubbleStyle(bubble)"
            @click="popBubble(bubble)"
          >
            <span class="bubble-word">{{ bubble.word }}</span>
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

const initialBubbleCount = 26
const bubbleBatchSize = 14
const maxBubbleCount = 90

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
const burstEffects = ref([])
const score = ref(0)
const combo = ref(0)
const bestCombo = ref(0)
const wrongPops = ref(0)
const autoPopped = ref(0)
const producedTotal = ref(0)
const collected = ref(0)
const roundIndex = ref(0)
const gameState = ref("playing")
const stage = reactive({ width: 980, height: 560 })
const message = reactive({
  title: "Press the button to start the bubble storm",
  text: "Pop the bright target words. Some bubbles will pop by themselves, so move fast.",
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

function createBubble(categoryOverride = null) {
  const category = categoryOverride ?? weightedCategory()
  const isTarget = category === currentRound.value.targetCategory
  const isGiant = isTarget ? Math.random() < 0.22 : Math.random() < 0.1
  const radius = isGiant ? 52 + Math.random() * 16 : 30 + Math.random() * 18
  const position = randomBubblePosition(radius)
  const ttlMs = 5200 + Math.random() * 6200
  const paletteIndex = Math.floor(Math.random() * 50)
  const hueBase = (paletteIndex * 7.2 + Math.random() * 4) % 360
  const hueShift = 18 + Math.random() * 24

  return {
    id: nextBubbleId++,
    category,
    word: pickRandom(wordPools[category]),
    x: position.x,
    y: position.y,
    vx: (Math.random() - 0.5) * 1.4,
    vy: (Math.random() - 0.5) * 1.4,
    radius,
    mass: Math.max(1, radius * radius * 0.015),
    isGiant,
    drift: 0.7 + Math.random() * 0.32,
    wobble: Math.random() * Math.PI * 2,
    spin: Math.random() * 360,
    buoyancy: 0.06 + Math.random() * 0.04,
    drag: 0.014 + Math.random() * 0.012,
    hueBase,
    hueShift,
    alphaOuter: 0.34 + Math.random() * 0.12,
    alphaMid: 0.26 + Math.random() * 0.1,
    alphaInner: 0.18 + Math.random() * 0.08,
    ttlMs,
    startTtlMs: ttlMs,
    lifeRatio: 1,
  }
}

function addBubbleWithSpacing(categoryOverride = null) {
  const bubble = createBubble(categoryOverride)
  for (let attempt = 0; attempt < 18; attempt += 1) {
    const overlap = bubbles.value.some(existing => {
      const dx = existing.x - bubble.x
      const dy = existing.y - bubble.y
      return Math.hypot(dx, dy) < existing.radius + bubble.radius + 6
    })
    if (!overlap) break
    const position = randomBubblePosition(bubble.radius)
    bubble.x = position.x
    bubble.y = position.y
  }
  bubbles.value.push(bubble)
}

function seedBubbles(count) {
  for (let i = 0; i < count; i += 1) {
    if (bubbles.value.length >= maxBubbleCount) break
    addBubbleWithSpacing()
  }
}

function produceBubbles(count = bubbleBatchSize) {
  if (gameState.value !== "playing") return
  const room = maxBubbleCount - bubbles.value.length
  const amount = Math.max(0, Math.min(count, room))
  if (!amount) {
    setMessage("Bubble board is full", "Pop a few bubbles first, then press the button again.", "info")
    return
  }

  seedBubbles(amount)
  producedTotal.value += amount
  setMessage("Fresh bubbles mixed", `${amount} new bubbles appeared.`, "success")
}

function measureStage() {
  if (!stageRef.value) return
  const rect = stageRef.value.getBoundingClientRect()
  stage.width = rect.width
  stage.height = rect.height
}

function applyBubbleForces(bubble, stepScale, now) {
  const currentX = Math.sin((bubble.y + now * 0.04 + bubble.id * 17) / 54) * 0.028 * bubble.drift
  const currentY = Math.cos((bubble.x + now * 0.03 + bubble.id * 11) / 64) * 0.018 * bubble.drift
  const buoyancy = -bubble.buoyancy * (1.04 - bubble.radius / 110)
  const centerX = (stage.width * 0.5 - bubble.x) * 0.00018

  bubble.vx += (currentX + centerX) * stepScale
  bubble.vy += (buoyancy + currentY) * stepScale
  bubble.vx += Math.sin((now * 0.006 + bubble.id) + bubble.wobble) * 0.01 * stepScale
  bubble.vy += Math.cos((now * 0.005 + bubble.id) + bubble.wobble) * 0.006 * stepScale
}

function integrateBubble(bubble, stepScale) {
  const damping = Math.pow(1 - bubble.drag, stepScale)
  bubble.vx *= damping
  bubble.vy *= damping
  bubble.vx = Math.max(-4.8, Math.min(4.8, bubble.vx))
  bubble.vy = Math.max(-4.2, Math.min(4.2, bubble.vy))
  bubble.x += bubble.vx * stepScale
  bubble.y += bubble.vy * stepScale
  bubble.spin += (bubble.vx * 0.18) * stepScale
}

function keepBubbleInBounds(bubble) {
  if (bubble.x <= bubble.radius || bubble.x >= stage.width - bubble.radius) {
    bubble.vx *= -0.92
    bubble.x = Math.max(bubble.radius, Math.min(stage.width - bubble.radius, bubble.x))
  }
  if (bubble.y <= bubble.radius || bubble.y >= stage.height - bubble.radius) {
    bubble.vy *= -0.9
    bubble.y = Math.max(bubble.radius, Math.min(stage.height - bubble.radius, bubble.y))
  }
}

function resolveBubbleCollisions() {
  for (let i = 0; i < bubbles.value.length; i += 1) {
    const a = bubbles.value[i]
    for (let j = i + 1; j < bubbles.value.length; j += 1) {
      const b = bubbles.value[j]
      const dx = b.x - a.x
      const dy = b.y - a.y
      const minDist = a.radius + b.radius + 1.5
      const distSq = dx * dx + dy * dy
      if (distSq >= minDist * minDist) continue

      const dist = Math.sqrt(distSq) || 0.0001
      const nx = dx / dist
      const ny = dy / dist
      const overlap = minDist - dist
      const totalMass = a.mass + b.mass
      const aShift = overlap * (b.mass / totalMass)
      const bShift = overlap * (a.mass / totalMass)

      a.x -= nx * aShift
      a.y -= ny * aShift
      b.x += nx * bShift
      b.y += ny * bShift

      const relativeVelocity = (b.vx - a.vx) * nx + (b.vy - a.vy) * ny
      if (relativeVelocity > 0) continue

      const restitution = 0.92
      const impulse = (-(1 + restitution) * relativeVelocity) / ((1 / a.mass) + (1 / b.mass))
      a.vx -= (impulse * nx) / a.mass
      a.vy -= (impulse * ny) / a.mass
      b.vx += (impulse * nx) / b.mass
      b.vy += (impulse * ny) / b.mass
    }
  }
}

function bubbleStyle(bubble) {
  const meta = categoryMeta[bubble.category]
  const hueA = bubble.hueBase
  const hueB = (bubble.hueBase + bubble.hueShift) % 360
  const hueC = (bubble.hueBase + bubble.hueShift * 1.8) % 360
  return {
    width: `${bubble.radius * 2}px`,
    height: `${bubble.radius * 2}px`,
    transform: `translate(${bubble.x - bubble.radius}px, ${bubble.y - bubble.radius}px) rotate(${bubble.spin}deg)`,
    background: `radial-gradient(circle at 30% 24%, rgba(255,255,255,0.94) 0%, rgba(255,255,255,0.38) 16%, hsla(${hueA}, 94%, 66%, ${bubble.alphaInner}) 40%, hsla(${hueB}, 92%, 54%, ${bubble.alphaMid}) 67%, hsla(${hueC}, 90%, 44%, ${bubble.alphaOuter}) 100%)`,
    boxShadow: `0 0 36px hsla(${hueB}, 85%, 48%, 0.24), inset -16px -20px 26px rgba(255,255,255,0.14), inset 12px 14px 20px rgba(255,255,255,0.06)`,
    "--bubble-font-size": `${Math.max(0.74, Math.min(1.08, bubble.radius / 42))}rem`,
    "--bubble-text-color": bubble.category === currentRound.value.targetCategory ? "rgba(255,255,255,0.98)" : "rgba(255,255,255,0.92)",
    "--bubble-highlight-a": `hsla(${hueA}, 100%, 98%, 0.88)`,
    "--bubble-highlight-b": `hsla(${hueB}, 96%, 96%, 0.22)`,
    "--bubble-outline": `hsla(${hueC}, 96%, 97%, 0.24)`,
    "--bubble-glow": `hsla(${hueB}, 92%, 78%, 0.24)`,
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

function expireBubble(bubble) {
  autoPopped.value += 1
  spawnBurst(bubble, "poof", categoryMeta[bubble.category].accent)
  removeBubble(bubble.id)
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
    producedTotal.value += initialBubbleCount
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
  autoPopped.value = 0
  producedTotal.value = 0
  collected.value = 0
  bubbles.value = []
  gameState.value = "playing"
  seedBubbles(initialBubbleCount)
  producedTotal.value += initialBubbleCount
  setMessage("Fresh game", rounds[0].story, "info")
}

function pruneBursts() {
  const now = performance.now()
  burstEffects.value = burstEffects.value.filter(effect => now - effect.createdAt < 460)
}

function updateBubbleLifetimes(deltaMs) {
  const expired = []
  for (const bubble of bubbles.value) {
    bubble.ttlMs -= deltaMs
    bubble.lifeRatio = Math.max(0, bubble.ttlMs / bubble.startTtlMs)
    if (bubble.ttlMs <= 0) expired.push(bubble)
  }

  for (const bubble of expired) {
    expireBubble(bubble)
  }
}

function tick(now) {
  pruneBursts()

  const deltaMs = lastFrameAt ? Math.min(26, now - lastFrameAt) : 16.67
  lastFrameAt = now
  const stepScale = deltaMs / 16.67
  const substeps = deltaMs > 18 ? 3 : 2

  if (gameState.value === "playing") {
    for (let pass = 0; pass < substeps; pass += 1) {
      const localScale = stepScale / substeps
      for (const bubble of bubbles.value) {
        applyBubbleForces(bubble, localScale, now)
        integrateBubble(bubble, localScale)
        keepBubbleInBounds(bubble)
      }
      resolveBubbleCollisions()
    }

    updateBubbleLifetimes(deltaMs)

    if (bubbles.value.length < 8) {
      setMessage("Need more bubbles", "Press Produce more bubbles to mix a fresh batch.", "info")
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
  producedTotal.value += initialBubbleCount
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
    radial-gradient(circle at 20% 14%, rgba(255, 255, 255, 0.44), transparent 28%),
    radial-gradient(circle at 82% 18%, rgba(255, 255, 255, 0.24), transparent 18%),
    linear-gradient(180deg, #86daf7 0%, #aee0ff 30%, #cfd7ff 66%, #f2dfee 100%);
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
}

.inside-stage {
  min-height: 42px;
  padding: 0 16px;
  box-shadow: 0 12px 22px rgba(41, 62, 121, 0.24);
}

.toolbar-stats {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.toolbar-stats span {
  border-radius: 999px;
  padding: 8px 12px;
  background: linear-gradient(135deg, rgba(247, 248, 255, 0.97), rgba(237, 244, 255, 0.94));
  border: 1.5px solid rgba(114, 133, 214, 0.2);
  color: #37517b;
  font-size: 0.76rem;
  font-weight: 800;
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

.bubble-adventure--dark .stage-toolbar .toolbar-stats span {
  color: rgba(226, 234, 255, 0.9);
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
    radial-gradient(circle at 20% 14%, rgba(59, 158, 255, 0.2), transparent 28%),
    radial-gradient(circle at 82% 18%, rgba(155, 114, 255, 0.18), transparent 22%),
    linear-gradient(180deg, rgba(24, 40, 72, 0.95) 0%, rgba(14, 22, 46, 0.98) 100%);
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
  display: grid;
  justify-items: center;
  align-content: center;
  cursor: pointer;
  user-select: none;
  transition: filter 0.12s ease, transform 0.12s ease;
  text-align: center;
  padding: 12px 10px 14px;
  box-sizing: border-box;
  border: 1px solid var(--bubble-outline);
  backdrop-filter: blur(6px);
}

.bubble:hover {
  filter: brightness(1.08) saturate(1.08);
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
    inset -14px -18px 24px rgba(255,255,255,0.16),
    inset 10px 12px 18px rgba(255,255,255,0.08);
}

.bubble-word {
  position: relative;
  z-index: 1;
  width: 80%;
  color: var(--bubble-text-color);
  font-size: calc(var(--bubble-font-size) + 0.12rem);
  font-weight: 900;
  line-height: 1.02;
  text-shadow: 0 2px 8px rgba(48, 61, 97, 0.22);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-wrap: balance;
  word-break: normal;
  hyphens: none;
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
