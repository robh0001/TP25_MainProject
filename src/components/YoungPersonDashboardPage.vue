<template>
  <div
    ref="pageRef"
    class="child-page"
    @pointermove="handlePointerMove"
    @pointerleave="handlePointerLeave"
  >
    <div class="blob-background" aria-hidden="true">
      <div class="pointer-glow" :style="pointerGlowStyle"></div>
      <div
        v-for="blob in interactiveBlobs"
        :key="blob.id"
        class="ui-blob"
        :style="blob.style"
      ></div>
    </div>
    <header class="child-header">
      <RouterLink to="/" class="brand">HealthyKids</RouterLink>
      <RouterLink to="/parent-entry" class="parent-link">Parent area</RouterLink>
    </header>

    <main class="child-main">
      <section class="hero">
        <p class="kicker">Kids Game Zone</p>
        <h1>Play healthy habit games.</h1>
        <p>Switch between Bubble, Explorer, and Smash games in the Games section.</p>
      </section>

      <section class="game-tabs" role="tablist" aria-label="Kids games">
        <button
          type="button"
          class="game-tab"
          :class="{ active: activeGame === 'bubble' }"
          @click="activeGame = 'bubble'"
        >
          Bubble Game
        </button>
        <button
          type="button"
          class="game-tab"
          :class="{ active: activeGame === 'explorer' }"
          @click="activeGame = 'explorer'"
        >
          Explorer Game
        </button>
        <button
          type="button"
          class="game-tab"
          :class="{ active: activeGame === 'smash' }"
          @click="activeGame = 'smash'"
        >
          Smash Game
        </button>
      </section>

      <section v-if="activeGame === 'bubble'" class="controls">
        <button type="button" class="btn primary" @click="toggleMic">
          {{ isMicEnabled ? "Stop bouncing" : "Start bouncing" }}
        </button>
        <label class="control">
          Sensitivity
          <input v-model.number="sensitivity" type="range" min="0.5" max="3" step="0.1" />
        </label>
        <label class="control">
          Noise alert
          <select v-model="alertMode" class="fancy-select">
            <option value="none">No sound</option>
            <option value="beep">Beep</option>
            <option value="shush">Shush</option>
          </select>
        </label>
        <div class="meter">
          <span>Noise</span>
          <strong>{{ Math.round(displayLevel) }}</strong>
          <small>{{ points }} pts</small>
        </div>
      </section>

      <section v-if="activeGame === 'bubble'" class="bubble-stage" ref="stageRef">
        <div class="status-banner" :class="noiseState">
          <strong>{{ statusTitle }}</strong>
          <span>{{ statusHint }}</span>
        </div>
        <div
          v-for="bubble in bubbles"
          :key="bubble.id"
          class="bubble"
          :style="bubbleStyle(bubble)"
          @click="burstBubble(bubble)"
        >
        </div>
        <div
          v-for="burst in burstEffects"
          :key="burst.id"
          class="bubble-burst"
          :style="burstStyle(burst)"
        ></div>
      </section>

      <section v-else-if="activeGame === 'explorer'" class="explorer-shell">
        <HealthyHabitsLab />
      </section>

      <section v-else class="explorer-shell">
        <SmashWiggleGame />
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue"
import { RouterLink } from "vue-router"
import HealthyHabitsLab from "./game/HealthyHabitsLab.vue"
import SmashWiggleGame from "./game/SmashWiggleGame.vue"

const pageRef = ref(null)
const stageRef = ref(null)
const stage = reactive({ width: 900, height: 520 })
const bubbles = ref([])
const burstEffects = ref([])
const sensitivity = ref(1.6)
const displayLevel = ref(0)
const isMicEnabled = ref(false)
const alertMode = ref("none")
const points = ref(0)
const activeGame = ref("bubble")
const pointer = reactive({ x: 0.5, y: 0.5 })
const pointerTarget = reactive({ x: 0.5, y: 0.5 })

const blobSeeds = [
  { id: 1, size: 260, x: 0.12, y: 0.2, hueA: 190, hueB: 232, drift: 0.9 },
  { id: 2, size: 340, x: 0.86, y: 0.16, hueA: 280, hueB: 232, drift: 1.2 },
  { id: 3, size: 280, x: 0.84, y: 0.78, hueA: 34, hueB: 302, drift: 1.15 },
  { id: 4, size: 220, x: 0.2, y: 0.8, hueA: 174, hueB: 220, drift: 0.8 },
]

let animationFrame = null
let analyser = null
let audioContext = null
let sourceNode = null
let micStream = null
let simulationPhase = 0
let lastAlertAt = 0
let nextBurstId = 1

function initBubbles() {
  const count = 44
  bubbles.value = Array.from({ length: count }, (_, i) => {
    const radius = 16 + Math.random() * 34
    return {
      id: i,
      x: radius + Math.random() * Math.max(10, stage.width - radius * 2),
      y: radius + Math.random() * Math.max(10, stage.height - radius * 2),
      vx: (Math.random() - 0.5) * 1.8,
      vy: (Math.random() - 0.5) * 1.8,
      radius,
      hue: 185 + Math.random() * 95,
      alpha: 0.35 + Math.random() * 0.45,
      spin: Math.random() * 360,
    }
  })
}

function measureStage() {
  if (!stageRef.value) return
  const rect = stageRef.value.getBoundingClientRect()
  stage.width = rect.width
  stage.height = rect.height
}

function readMicLevel() {
  if (!analyser) return null
  const data = new Uint8Array(analyser.fftSize)
  analyser.getByteTimeDomainData(data)
  let sum = 0
  for (let i = 0; i < data.length; i += 1) {
    const centered = data[i] - 128
    sum += centered * centered
  }
  const rms = Math.sqrt(sum / data.length)
  return Math.min(100, (rms / 45) * 100)
}

function simulatedLevel() {
  simulationPhase += 0.03
  return 36 + Math.sin(simulationPhase * 1.8) * 24 + Math.sin(simulationPhase * 0.45) * 12
}

function maybeNoiseAlert(level) {
  if (alertMode.value === "none") return
  if (level < 72) return
  const now = Date.now()
  if (now - lastAlertAt < 1400) return
  lastAlertAt = now
  if (!audioContext) {
    audioContext = new window.AudioContext()
  }
  const osc = audioContext.createOscillator()
  const gain = audioContext.createGain()
  osc.connect(gain)
  gain.connect(audioContext.destination)
  osc.type = alertMode.value === "shush" ? "triangle" : "sine"
  osc.frequency.value = alertMode.value === "shush" ? 520 : 760
  gain.gain.setValueAtTime(0.0001, audioContext.currentTime)
  gain.gain.exponentialRampToValueAtTime(0.12, audioContext.currentTime + 0.01)
  gain.gain.exponentialRampToValueAtTime(0.0001, audioContext.currentTime + 0.2)
  osc.start()
  osc.stop(audioContext.currentTime + 0.22)
}

function tick() {
  pointer.x += (pointerTarget.x - pointer.x) * 0.08
  pointer.y += (pointerTarget.y - pointer.y) * 0.08
  pruneBursts()
  const measured = isMicEnabled.value ? readMicLevel() : null
  const baseLevel = measured ?? simulatedLevel()
  displayLevel.value = Math.max(0, Math.min(100, baseLevel))
  maybeNoiseAlert(displayLevel.value)

  const energy = (displayLevel.value / 100) * sensitivity.value * 1.55
  for (const bubble of bubbles.value) {
    bubble.vx += (Math.random() - 0.5) * (0.15 + energy * 0.52)
    bubble.vy += (Math.random() - 0.5) * (0.15 + energy * 0.52)

    bubble.vx *= 0.988
    bubble.vy *= 0.988
    bubble.vx = Math.max(-7.8, Math.min(7.8, bubble.vx))
    bubble.vy = Math.max(-7.8, Math.min(7.8, bubble.vy))
    bubble.spin += bubble.vx * 0.6

    bubble.x += bubble.vx
    bubble.y += bubble.vy

    if (bubble.x <= bubble.radius || bubble.x >= stage.width - bubble.radius) {
      bubble.vx *= -1
      bubble.x = Math.max(bubble.radius, Math.min(stage.width - bubble.radius, bubble.x))
    }
    if (bubble.y <= bubble.radius || bubble.y >= stage.height - bubble.radius) {
      bubble.vy *= -1
      bubble.y = Math.max(bubble.radius, Math.min(stage.height - bubble.radius, bubble.y))
    }
  }

  animationFrame = window.requestAnimationFrame(tick)
}

async function toggleMic() {
  if (isMicEnabled.value) {
    stopMic()
    return
  }
  try {
    micStream = await navigator.mediaDevices.getUserMedia({ audio: true })
    audioContext = new window.AudioContext()
    sourceNode = audioContext.createMediaStreamSource(micStream)
    analyser = audioContext.createAnalyser()
    analyser.fftSize = 1024
    sourceNode.connect(analyser)
    isMicEnabled.value = true
  } catch (error) {
    isMicEnabled.value = false
  }
}

function stopMic() {
  if (micStream) {
    micStream.getTracks().forEach(track => track.stop())
  }
  if (audioContext) {
    audioContext.close()
  }
  analyser = null
  sourceNode = null
  micStream = null
  audioContext = null
  isMicEnabled.value = false
}

const bubbleStyle = computed(() => bubble => ({
  width: `${bubble.radius * 2}px`,
  height: `${bubble.radius * 2}px`,
  transform: `translate(${bubble.x - bubble.radius}px, ${bubble.y - bubble.radius}px) rotate(${bubble.spin}deg)`,
  background: `radial-gradient(circle at 30% 30%, rgba(255,255,255,0.92), hsla(${bubble.hue}, 90%, 62%, ${bubble.alpha}))`,
  boxShadow: `0 0 16px hsla(${bubble.hue}, 90%, 66%, 0.35), inset -8px -12px 18px rgba(255,255,255,0.26)`,
}))

const burstStyle = computed(() => burst => ({
  width: `${burst.size}px`,
  height: `${burst.size}px`,
  left: `${burst.x - burst.size / 2}px`,
  top: `${burst.y - burst.size / 2}px`,
  borderColor: `hsla(${burst.hue}, 95%, 72%, 0.95)`,
}))

const statusTitle = computed(() => {
  if (displayLevel.value < 38) return "Quiet!"
  if (displayLevel.value < 72) return "Nice energy"
  return "Too noisy!"
})

const statusHint = computed(() => {
  if (displayLevel.value < 38) return "Soft sounds keep bubbles calm."
  if (displayLevel.value < 72) return "Bubbles are bouncing smoothly."
  return "Shhhh! Try lowering your voice."
})

const noiseState = computed(() => {
  if (displayLevel.value < 38) return "quiet"
  if (displayLevel.value < 72) return "ok"
  return "loud"
})

const interactiveBlobs = computed(() =>
  blobSeeds.map(seed => {
    const offsetX = (pointer.x - 0.5) * seed.drift * 90
    const offsetY = (pointer.y - 0.5) * seed.drift * 90
    return {
      id: seed.id,
      style: {
        width: `${seed.size}px`,
        height: `${seed.size}px`,
        left: `calc(${seed.x * 100}% - ${seed.size / 2}px + ${offsetX}px)`,
        top: `calc(${seed.y * 100}% - ${seed.size / 2}px + ${offsetY}px)`,
        background: `radial-gradient(circle at 35% 30%, hsla(${seed.hueA}, 95%, 68%, 0.52), hsla(${seed.hueB}, 88%, 66%, 0.22) 62%, rgba(255,255,255,0) 100%)`,
        animationDuration: `${14 + seed.id * 2.8}s`,
      },
    }
  }),
)

const pointerGlowStyle = computed(() => ({
  left: `${pointer.x * 100}%`,
  top: `${pointer.y * 100}%`,
}))

function burstBubble(bubble) {
  const gained = Math.max(1, Math.round(20 - bubble.radius / 3))
  points.value += gained
  burstEffects.value.push({
    id: nextBurstId++,
    x: bubble.x,
    y: bubble.y,
    size: bubble.radius * 2,
    hue: bubble.hue,
    createdAt: performance.now(),
  })

  const radius = 16 + Math.random() * 34
  bubble.radius = radius
  bubble.x = radius + Math.random() * Math.max(10, stage.width - radius * 2)
  bubble.y = radius + Math.random() * Math.max(10, stage.height - radius * 2)
  bubble.vx = (Math.random() - 0.5) * 2.6
  bubble.vy = (Math.random() - 0.5) * 2.6
  bubble.hue = 185 + Math.random() * 95
  bubble.alpha = 0.35 + Math.random() * 0.45
  bubble.spin = Math.random() * 360
}

function handleResize() {
  measureStage()
}

function handlePointerMove(event) {
  if (!pageRef.value) return
  const rect = pageRef.value.getBoundingClientRect()
  pointerTarget.x = Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width))
  pointerTarget.y = Math.max(0, Math.min(1, (event.clientY - rect.top) / rect.height))
}

function handlePointerLeave() {
  pointerTarget.x = 0.5
  pointerTarget.y = 0.5
}

watch(activeGame, game => {
  if (game !== "bubble" && isMicEnabled.value) {
    stopMic()
  }
})

function pruneBursts() {
  const now = performance.now()
  burstEffects.value = burstEffects.value.filter(effect => now - effect.createdAt < 320)
}

onMounted(() => {
  measureStage()
  initBubbles()
  animationFrame = window.requestAnimationFrame(tick)
  window.addEventListener("resize", handleResize)
})

onBeforeUnmount(() => {
  if (animationFrame) window.cancelAnimationFrame(animationFrame)
  stopMic()
  window.removeEventListener("resize", handleResize)
})
</script>

<style scoped>
.child-page {
  position: relative;
  min-height: 100vh;
  background:
    radial-gradient(circle at 15% 12%, rgba(117, 190, 255, 0.28), transparent 32%),
    radial-gradient(circle at 84% 16%, rgba(166, 137, 255, 0.24), transparent 36%),
    linear-gradient(155deg, #eff6ff 0%, #f5f0ff 48%, #fff8ef 100%);
  color: #13213a;
  overflow: hidden;
}

.blob-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.ui-blob {
  position: absolute;
  border-radius: 999px;
  filter: blur(6px);
  animation: driftBlob ease-in-out infinite alternate;
}

.pointer-glow {
  position: absolute;
  width: 420px;
  height: 420px;
  border-radius: 999px;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle, rgba(255, 255, 255, 0.52), rgba(255, 255, 255, 0));
  filter: blur(8px);
}

@keyframes driftBlob {
  from {
    transform: translate3d(-10px, -8px, 0) scale(0.98);
  }
  to {
    transform: translate3d(12px, 10px, 0) scale(1.04);
  }
}

.child-header {
  position: relative;
  z-index: 2;
  width: min(1160px, calc(100% - 28px));
  margin: 0 auto;
  min-height: 78px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  text-decoration: none;
  font-weight: 900;
  letter-spacing: -0.03em;
  color: #18243f;
  font-size: 1.35rem;
}

.parent-link {
  text-decoration: none;
  padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid rgba(24, 36, 63, 0.2);
  color: #18243f;
  font-weight: 700;
}

.child-main {
  position: relative;
  z-index: 2;
  width: min(1160px, calc(100% - 28px));
  margin: 0 auto;
  padding-bottom: 30px;
}

.hero h1 {
  margin: 8px 0 0;
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 0.95;
  letter-spacing: -0.05em;
}

.hero p {
  max-width: 62ch;
  color: #45546f;
  line-height: 1.7;
}

.kicker {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-weight: 800;
  color: #495dd4;
  font-size: 0.8rem;
}

.game-tabs {
  display: flex;
  gap: 10px;
  margin-top: 16px;
  flex-wrap: wrap;
}

.game-tab {
  border: 1px solid rgba(62, 87, 160, 0.25);
  border-radius: 999px;
  min-height: 40px;
  padding: 0 14px;
  background: rgba(255, 255, 255, 0.66);
  color: #1f2f52;
  font-weight: 700;
  cursor: pointer;
}

.game-tab.active {
  color: #fff;
  border-color: transparent;
  background: linear-gradient(135deg, #2e46dd 0%, #7a3df0 100%);
}

.controls {
  margin-top: 20px;
  display: grid;
  grid-template-columns: auto 1fr 1fr auto;
  gap: 14px;
  align-items: center;
  background: rgba(255, 255, 255, 0.76);
  border: 1px solid rgba(70, 92, 142, 0.16);
  border-radius: 20px;
  padding: 14px;
}

.btn {
  border: 0;
  border-radius: 999px;
  min-height: 46px;
  padding: 0 18px;
  font-weight: 800;
  cursor: pointer;
}

.btn.primary {
  background: linear-gradient(135deg, #2e46dd 0%, #7a3df0 100%);
  color: #fff;
}

.control {
  display: grid;
  gap: 6px;
  color: #2b3e60;
  font-weight: 700;
}

.control input {
  width: 100%;
}

.control select {
  min-height: 38px;
  border-radius: 10px;
  border: 1px solid rgba(60, 82, 128, 0.26);
  padding: 0 12px;
  font: inherit;
  color: #263757;
  background: #fff;
}

.fancy-select {
  appearance: none;
  background-image:
    linear-gradient(45deg, transparent 50%, #4a58c8 50%),
    linear-gradient(135deg, #4a58c8 50%, transparent 50%),
    linear-gradient(to right, rgba(74, 88, 200, 0.16), rgba(74, 88, 200, 0.04));
  background-position:
    calc(100% - 18px) calc(50% - 2px),
    calc(100% - 12px) calc(50% - 2px),
    0 0;
  background-size:
    6px 6px,
    6px 6px,
    100% 100%;
  background-repeat: no-repeat;
  border: 1px solid rgba(56, 72, 196, 0.34);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.75);
  cursor: pointer;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.fancy-select:focus {
  outline: none;
  border-color: #4a58c8;
  box-shadow: 0 0 0 3px rgba(74, 88, 200, 0.18);
}

.meter {
  min-width: 90px;
  border-radius: 14px;
  background: #0f1e39;
  color: #fff;
  padding: 10px 12px;
  display: grid;
  justify-items: center;
}

.meter span {
  font-size: 0.75rem;
  opacity: 0.75;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.meter strong {
  font-size: 1.3rem;
}

.meter small {
  margin-top: 3px;
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: rgba(255, 255, 255, 0.86);
}

.bubble-stage {
  position: relative;
  margin-top: 16px;
  height: 62vh;
  min-height: 460px;
  border-radius: 26px;
  border: 1px solid rgba(74, 95, 148, 0.2);
  overflow: hidden;
  background:
    radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.65), transparent 30%),
    linear-gradient(160deg, #13244d 0%, #1f3170 46%, #3e2d87 100%);
  box-shadow: inset 0 0 80px rgba(92, 116, 201, 0.3), 0 24px 46px rgba(19, 36, 77, 0.22);
}

.bubble {
  position: absolute;
  border-radius: 999px;
  display: grid;
  place-items: center;
  cursor: pointer;
  transition: transform 0.08s ease-out;
}

.bubble:hover {
  filter: brightness(1.1);
}

.bubble-burst {
  position: absolute;
  border-radius: 999px;
  border: 4px solid;
  pointer-events: none;
  animation: burst 320ms ease-out forwards;
}

@keyframes burst {
  from {
    opacity: 0.95;
    transform: scale(0.4);
  }
  to {
    opacity: 0;
    transform: scale(1.45);
  }
}

.status-banner {
  position: absolute;
  left: 14px;
  top: 14px;
  z-index: 2;
  min-width: 180px;
  border-radius: 14px;
  padding: 10px 12px;
  border: 1px solid rgba(255, 255, 255, 0.34);
  backdrop-filter: blur(8px);
}

.status-banner strong {
  display: block;
  font-size: 1rem;
  color: #fff;
}

.status-banner span {
  color: rgba(255, 255, 255, 0.86);
  font-size: 0.85rem;
}

.status-banner.quiet {
  background: rgba(18, 128, 85, 0.42);
}

.status-banner.ok {
  background: rgba(62, 94, 196, 0.46);
}

.status-banner.loud {
  background: rgba(196, 47, 72, 0.56);
}

.explorer-shell {
  margin-top: 14px;
  border-radius: 24px;
  border: 1px solid rgba(74, 95, 148, 0.2);
  padding: 16px;
  background: #fff;
  box-shadow: 0 16px 30px rgba(33, 49, 92, 0.12);
}

@media (max-width: 880px) {
  .controls {
    grid-template-columns: 1fr;
  }

  .meter {
    justify-self: start;
  }

  .bubble-stage {
    min-height: 420px;
  }
}
</style>