<template>
    <section
      class="smash-game"
      @pointermove="onPointerMove"
      @pointerup="onPointerUp"
      @pointercancel="onPointerUp"
      @pointerleave="onPointerUp"
    >
      <header class="smash-head">
        <p class="smash-kicker">Smash Game</p>
        <h3>Grab and shake the dancing balloon</h3>
        <p>Drag the head and whip it around. Fast shakes charge the fun meter.</p>
      </header>
  
      <div class="arena">
        <div class="meter">
          <span>Shake Power</span>
          <div class="meter-track">
            <i :style="{ width: `${Math.round(power)}%` }"></i>
          </div>
        </div>
  
        <div class="wiggle-wrap" @pointerdown="onPointerDown" @click="tapNudge">
          <svg class="balloon-svg" viewBox="0 0 360 320" preserveAspectRatio="xMidYMid meet">
            <path class="tube tube-shadow" :d="tubePath" />
            <path class="tube tube-main" :d="tubePath" :class="{ charged: celebration }" />
            <circle class="head" :cx="head.x" :cy="head.y" r="24" :class="{ charged: celebration }" />
            <circle class="eye" :cx="head.x - 8" :cy="head.y - 5" r="3.5" />
            <circle class="eye" :cx="head.x + 8" :cy="head.y - 5" r="3.5" />
            <circle class="mouth" :cx="head.x" :cy="head.y + 7" r="2.6" />
          </svg>
        </div>
  
        <p class="status">{{ statusText }}</p>
  
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
    </section>
  </template>
  
  <script setup>
  import { computed, onBeforeUnmount, onMounted, reactive, ref } from "vue"
  
  const VIEW_W = 360
  const VIEW_H = 320
  const NODE_COUNT = 17
  const SEGMENT_LENGTH = 14
  const TAIL = { x: VIEW_W / 2, y: 286 }
  
  const drag = reactive({
    active: false,
    pointerId: null,
    lastX: VIEW_W / 2,
    lastY: 84,
    lastAt: 0,
  })
  const pointer = reactive({ x: VIEW_W / 2, y: 84 })
  const power = ref(0)
  const celebration = ref(false)
  const sparks = ref([])
  const nodes = ref(initNodes())
  
  let sparkId = 1
  let rafId = null
  
  const statusText = computed(() => {
    if (celebration.value) return "Mega shake unlocked! Nice energy!"
    if (power.value > 70) return "So close! Keep shaking fast."
    if (power.value > 35) return "Great! The balloon is dancing."
    return "Drag and shake to charge the meter."
  })
  
  const head = computed(() => nodes.value[0] ?? { x: VIEW_W / 2, y: 84 })
  
  const tubePath = computed(() => {
    const list = nodes.value
    if (!list.length) return ""
    let d = `M ${list[0].x.toFixed(2)} ${list[0].y.toFixed(2)}`
    for (let i = 1; i < list.length - 1; i += 1) {
      const xc = (list[i].x + list[i + 1].x) / 2
      const yc = (list[i].y + list[i + 1].y) / 2
      d += ` Q ${list[i].x.toFixed(2)} ${list[i].y.toFixed(2)} ${xc.toFixed(2)} ${yc.toFixed(2)}`
    }
    const end = list[list.length - 1]
    d += ` T ${end.x.toFixed(2)} ${end.y.toFixed(2)}`
    return d
  })
  
  function initNodes() {
    const list = []
    for (let i = 0; i < NODE_COUNT; i += 1) {
      list.push({
        x: TAIL.x,
        y: TAIL.y - SEGMENT_LENGTH * (NODE_COUNT - 1 - i),
        vx: 0,
        vy: 0,
      })
    }
    return list
  }
  
  function onPointerDown(event) {
    drag.active = true
    drag.pointerId = event.pointerId
    const p = toLocal(event)
    drag.lastX = p.x
    drag.lastY = p.y
    drag.lastAt = performance.now()
    pointer.x = p.x
    pointer.y = p.y
    if (event.currentTarget?.setPointerCapture) {
      event.currentTarget.setPointerCapture(event.pointerId)
    }
  }
  
  function onPointerMove(event) {
    if (!drag.active || event.pointerId !== drag.pointerId) return
    const p = toLocal(event)
    const now = performance.now()
    const dx = p.x - drag.lastX
    const dy = p.y - drag.lastY
    const dt = Math.max(12, now - drag.lastAt)
    const speed = (Math.hypot(dx, dy) / dt) * 100
  
    drag.lastX = p.x
    drag.lastY = p.y
    drag.lastAt = now
    pointer.x = p.x
    pointer.y = p.y
    power.value = Math.min(100, power.value + Math.min(7, speed / 24))
  
    if (power.value >= 100 && !celebration.value) {
      triggerCelebration()
    }
  }
  
  function onPointerUp(event) {
    if (event.pointerId !== drag.pointerId) return
    drag.active = false
    drag.pointerId = null
  }
  
  function tapNudge() {
    const jitterX = (Math.random() - 0.5) * 52
    const jitterY = (Math.random() - 0.5) * 26
    pointer.x = clamp(pointer.x + jitterX, 36, VIEW_W - 36)
    pointer.y = clamp(pointer.y + jitterY, 46, VIEW_H - 94)
    nodes.value[0].vx += jitterX * 0.15
    nodes.value[0].vy += jitterY * 0.15
    power.value = Math.min(100, power.value + 5)
    if (power.value >= 100 && !celebration.value) triggerCelebration()
  }
  
  function triggerCelebration() {
    celebration.value = true
    spawnSparks()
    window.setTimeout(() => {
      celebration.value = false
      power.value = 42
    }, 1400)
  }
  
  function spawnSparks() {
    sparks.value = Array.from({ length: 22 }, (_, i) => ({
      id: sparkId++,
      x: 32 + Math.random() * 36,
      y: 34 + Math.random() * 30,
      sx: Math.random(),
      sy: Math.random(),
      delay: i * 14,
      color: ["#4f7cff", "#7a48ff", "#ff6b9f", "#ffbe55"][i % 4],
    }))
    window.setTimeout(() => {
      sparks.value = []
    }, 820)
  }
  
  function updatePhysics() {
    const list = nodes.value
    if (!list.length) return
  
    for (let i = 0; i < list.length - 1; i += 1) {
      list[i].vy += 0.18
      list[i].vx *= 0.98
      list[i].vy *= 0.98
      list[i].x += list[i].vx
      list[i].y += list[i].vy
    }
  
    const headNode = list[0]
    if (drag.active) {
      headNode.vx += (pointer.x - headNode.x) * 0.24
      headNode.vy += (pointer.y - headNode.y) * 0.24
    } else {
      const idleX = VIEW_W / 2 + Math.sin(performance.now() / 420) * 12
      const idleY = 84 + Math.sin(performance.now() / 680) * 6
      headNode.vx += (idleX - headNode.x) * 0.06
      headNode.vy += (idleY - headNode.y) * 0.06
      power.value = Math.max(0, power.value - 0.45)
    }
  
    for (let pass = 0; pass < 5; pass += 1) {
      const tail = list[list.length - 1]
      tail.x = TAIL.x
      tail.y = TAIL.y
      tail.vx = 0
      tail.vy = 0
  
      for (let i = 0; i < list.length - 1; i += 1) {
        const a = list[i]
        const b = list[i + 1]
        const dx = b.x - a.x
        const dy = b.y - a.y
        const dist = Math.hypot(dx, dy) || 0.0001
        const diff = (dist - SEGMENT_LENGTH) / dist
        const offsetX = dx * diff
        const offsetY = dy * diff
  
        if (i === list.length - 2) {
          a.x += offsetX
          a.y += offsetY
        } else if (i === 0) {
          b.x -= offsetX
          b.y -= offsetY
        } else {
          a.x += offsetX * 0.5
          a.y += offsetY * 0.5
          b.x -= offsetX * 0.5
          b.y -= offsetY * 0.5
        }
      }
    }
  
    for (let i = 0; i < list.length - 1; i += 1) {
      list[i].x = clamp(list[i].x, 20, VIEW_W - 20)
      list[i].y = clamp(list[i].y, 20, VIEW_H - 12)
    }
  
    rafId = window.requestAnimationFrame(updatePhysics)
  }
  
  function toLocal(event) {
    const arena = event.currentTarget.closest(".arena")
    const rect = arena.getBoundingClientRect()
    const x = ((event.clientX - rect.left) / rect.width) * VIEW_W
    const y = ((event.clientY - rect.top) / rect.height) * VIEW_H
    return {
      x: clamp(x, 20, VIEW_W - 20),
      y: clamp(y, 20, VIEW_H - 20),
    }
  }
  
  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value))
  }
  
  onMounted(() => {
    rafId = window.requestAnimationFrame(updatePhysics)
  })
  
  onBeforeUnmount(() => {
    if (rafId) window.cancelAnimationFrame(rafId)
  })
  </script>
  
  <style scoped>
  .smash-game {
    color: #1c2544;
  }
  
  .smash-head h3 {
    margin: 8px 0 0;
    font-size: 1.45rem;
  }
  
  .smash-head p {
    margin: 10px 0 0;
    color: #4b587f;
  }
  
  .smash-kicker {
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.78rem;
    font-weight: 800;
    color: #4a5ad2;
  }
  
  .arena {
    position: relative;
    margin-top: 14px;
    border-radius: 22px;
    border: 1px solid rgba(67, 88, 162, 0.24);
    background:
      radial-gradient(circle at 70% 18%, rgba(194, 179, 255, 0.38), transparent 36%),
      radial-gradient(circle at 20% 74%, rgba(140, 214, 255, 0.32), transparent 32%),
      #fff;
    padding: 16px;
    min-height: 420px;
    overflow: hidden;
  }
  
  .meter {
    max-width: 320px;
  }
  
  .meter span {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 800;
    color: #3f4f7b;
  }
  
  .meter-track {
    margin-top: 7px;
    height: 12px;
    border-radius: 999px;
    background: #e8edff;
    overflow: hidden;
  }
  
  .meter-track i {
    display: block;
    height: 100%;
    background: linear-gradient(90deg, #3e5fff 0%, #7d44ff 60%, #ff6e9b 100%);
    transition: width 0.08s linear;
  }
  
  .wiggle-wrap {
    margin-top: 26px;
    min-height: 260px;
    display: grid;
    place-items: center;
    cursor: grab;
  }
  
  .wiggle-wrap:active {
    cursor: grabbing;
  }
  
  .balloon-svg {
    width: min(92%, 460px);
    height: 260px;
    overflow: visible;
  }
  
  .tube {
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
  }
  
  .tube-shadow {
    stroke: rgba(13, 16, 24, 0.18);
    stroke-width: 44;
  }
  
  .tube-main {
    stroke: #11131b;
    stroke-width: 38;
    transition: filter 0.12s ease;
  }
  
  .tube-main.charged {
    filter: saturate(1.28);
  }
  
  .head {
    fill: #11131b;
    transition: filter 0.12s ease;
  }
  
  .head.charged {
    filter: brightness(1.1);
  }
  
  .eye {
    fill: #fff;
  }
  
  .mouth {
    fill: #fff;
  }
  
  .status {
    margin: 0;
    text-align: center;
    font-weight: 700;
    color: #2d3b67;
  }
  
  .burst-layer {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }
  
  .spark {
    position: absolute;
    width: 12px;
    height: 12px;
    border-radius: 3px;
    opacity: 0;
    animation: sparkOut 620ms ease-out forwards;
  }
  
  @keyframes sparkOut {
    from {
      transform: translate(0, 0) scale(0.4) rotate(0deg);
      opacity: 1;
    }
    to {
      transform: translate(
          calc((var(--sx, 0.5) - 0.5) * 160px),
          calc((var(--sy, 0.5) - 0.5) * 130px)
        )
        scale(1.2)
        rotate(220deg);
      opacity: 0;
    }
  }
  </style>
  