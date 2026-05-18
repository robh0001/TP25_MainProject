<template>
    <section
      class="humit"
      :class="{
        'humit--dark': isDarkMode,
        'humit--panic': isTimerPanic,
        'humit--near-lock': isNearResonanceLock,
        'humit--shell-spike': shellSpike,
      }"
      :style="sectionAura"
    >
      <div class="humit__sky" aria-hidden="true"></div>
      <div class="humit__aurora" aria-hidden="true"></div>
      <div class="humit__stars-field" aria-hidden="true">
        <span v-for="s in starDots" :key="s.i" class="humit__star" :style="s.style"></span>
      </div>
      <div class="humit__hills" aria-hidden="true"></div>
      <div class="humit__glyphs" aria-hidden="true">
        <span class="humit__glyph humit__glyph--a">♪</span>
        <span class="humit__glyph humit__glyph--b">♫</span>
        <span class="humit__glyph humit__glyph--c">✧</span>
        <span class="humit__glyph humit__glyph--d">◇</span>
      </div>
  
      <header class="humit__top">
        <div>
          <h4 class="humit__title">
            <template v-if="phase !== 'welcome' && buddyName">{{ buddyName }}</template>
            <template v-else>Hum It</template>
          </h4>
        </div>
        <div class="humit__top-aside">
          <button
            v-if="phase !== 'welcome'"
            type="button"
            class="humit__music-btn"
            :class="{ 'humit__music-btn--muted': humitOst.muted }"
            :aria-pressed="humitOst.muted"
            :aria-label="humitOst.muted ? 'Unmute background music' : 'Mute background music'"
            @click="humitOst.toggleMuted()"
          >
            <span aria-hidden="true">♫</span>
          </button>
          <div class="humit__stats" :class="{ 'humit__stats--pulse': isTimerPanic }">
            <span class="humit__pill humit__pill--stat" title="Score"><span class="humit__pill-ico" aria-hidden="true">✦</span>{{ score }}</span>
            <span class="humit__pill humit__pill--stat" title="Streak"><span class="humit__pill-ico" aria-hidden="true">⚡</span>×{{ streak }}</span>
          </div>
        </div>
      </header>
  
      <div v-if="phase === 'welcome'" class="humit__panel humit__panel--hero humit__welcome">
        <p class="humit__welcome-lead">Hum · your buddy grows · beat quick prompts.</p>
        <div class="humit__actions humit__actions--welcome">
          <button type="button" class="humit__btn humit__btn--primary" @click="goBirth(false)">
            🎤 Mic
          </button>
          <button type="button" class="humit__btn humit__btn--ghost" @click="goBirth(true)">
            🎚 Demo
          </button>
        </div>
        <p v-if="audio.errorMessage" class="humit__err">{{ audio.errorMessage }}</p>
      </div>
  
      <div v-else-if="phase === 'birth'" class="humit__panel">
        <p class="humit__challenge">{{ birthLabel }}</p>
        <div class="humit__birth-meter">
          <span :style="{ width: `${birthProgress * 100}%` }"></span>
        </div>
        <div
          class="humit__creature-shell"
          :class="{
            'humit__creature-shell--pop': creaturePop,
            'humit__creature-shell--micro-spike': shellSpike,
          }"
        >
          <div class="humit__ripple-pack" :class="{ 'humit__ripple-pack--fire': rippleFire }" aria-hidden="true">
            <span class="humit__ripple"></span>
            <span class="humit__ripple humit__ripple--d"></span>
            <span class="humit__ripple humit__ripple--dd"></span>
          </div>
          <div class="humit__orbit" aria-hidden="true">
            <span class="humit__orbit-ring humit__orbit-ring--a"></span>
            <span class="humit__orbit-ring humit__orbit-ring--b"></span>
          </div>
          <div class="humit__creature-wrap">
            <HumItCreature
              v-bind="creatureVisual"
              :wobble="creatureWobble"
              :volume="creatureExpressVol"
              :pitch-norm="creatureExpressPitch"
              :vol-spike="volSpike"
              :near-win="phase === 'birth' ? false : isNearResonanceLock"
            />
          </div>
        </div>
        <p class="humit__hint humit__hint--compact">
          {{ demoMode ? "Move sliders · 3s" : "Hum · 3s" }}
        </p>
        <details v-if="demoMode" class="humit__demo">
          <summary>Levels</summary>
          <label>Pitch <input v-model.number="audio.demoPitch" type="range" min="0" max="1" step="0.01" /></label>
          <label>Volume <input v-model.number="audio.demoVolume" type="range" min="0" max="1" step="0.01" /></label>
        </details>
      </div>
  
      <div v-else class="humit__play">
        <div
          class="humit__challenge-card"
          :class="[
            `humit__challenge-card--${currentChallenge.id}`,
            { 'humit__challenge-card--panic': isTimerPanic, 'humit__challenge-card--locking': isNearResonanceLock },
          ]"
        >
          <div class="humit__challenge-row">
            <span class="humit__emoji" aria-hidden="true">{{ currentChallenge.emoji }}</span>
            <div class="humit__challenge-copy">
              <p class="humit__challenge-line">{{ currentChallenge.hint }}</p>
              <span class="humit__sr-only">{{ currentChallenge.whisper }}</span>
            </div>
          </div>
          <div class="humit__lockon" aria-hidden="true">
            <div class="humit__lockon-track">
              <span class="humit__lockon-fill" :style="{ width: `${resonanceLockPct}%` }"></span>
              <span class="humit__lockon-threshold"></span>
            </div>
          </div>
          <div
            class="humit__timer"
            :class="{ 'humit__timer--panic': isTimerPanic, 'humit__timer--rush': challengeTimerPct < 45 }"
          >
            <span :style="{ width: `${challengeTimerPct}%` }"></span>
          </div>
        </div>
  
        <div class="humit__stage">
          <div class="humit__sonic" aria-hidden="true">
            <span class="humit__sonic-arc humit__sonic-arc--a"></span>
            <span class="humit__sonic-arc humit__sonic-arc--b"></span>
            <span class="humit__sonic-arc humit__sonic-arc--c"></span>
          </div>
          <div v-if="flowTier" class="humit__flow-badge" :title="`Flow ×${flowTier}`">
            <span class="humit__flow-mult">×{{ flowTier }}</span>
          </div>
  
          <div class="humit__constellation" aria-hidden="true">
            <span
              v-for="n in 10"
              :key="n"
              class="humit__cstar"
              :class="{ 'humit__cstar--lit': streak >= n }"
            ></span>
          </div>
  
          <div
            class="humit__creature-shell humit__creature-shell--play"
            :class="{
              'humit__creature-shell--pop': creaturePop,
              'humit__creature-shell--micro-spike': shellSpike,
            }"
          >
            <div class="humit__ripple-pack" :class="{ 'humit__ripple-pack--fire': rippleFire }" aria-hidden="true">
              <span class="humit__ripple"></span>
              <span class="humit__ripple humit__ripple--d"></span>
              <span class="humit__ripple humit__ripple--dd"></span>
            </div>
            <div class="humit__orbit" aria-hidden="true">
              <span class="humit__orbit-ring humit__orbit-ring--a"></span>
              <span class="humit__orbit-ring humit__orbit-ring--b"></span>
            </div>
            <HumItCreature
              v-bind="creatureVisual"
              :wobble="creatureWobble"
              :boost="lastWinBoost"
              :volume="creatureExpressVol"
              :pitch-norm="creatureExpressPitch"
              :vol-spike="volSpike"
              :near-win="isNearResonanceLock"
            />
            <div v-if="burstTicks" class="humit__burst" aria-hidden="true">
              <i v-for="b in 14" :key="b" class="humit__burst-ray"></i>
            </div>
          </div>
          <div class="humit__cloud humit__cloud--a"></div>
          <div class="humit__cloud humit__cloud--b"></div>
          <div class="humit__cloud humit__cloud--c"></div>
        </div>
  
        <div class="humit__meters humit__meters--compact">
          <div class="humit__meter" role="group" aria-label="Pitch">
            <span class="humit__meter-label" aria-hidden="true">♪</span>
            <div class="humit__bar"><i :style="{ width: `${pitchBarPct}%` }"></i></div>
          </div>
          <div class="humit__meter" role="group" aria-label="Volume">
            <span class="humit__meter-label" aria-hidden="true">●</span>
            <div class="humit__bar humit__bar--vol"><i :style="{ width: `${volumeBarPct}%` }"></i></div>
          </div>
        </div>
  
        <details v-if="demoMode" class="humit__demo humit__demo--inline">
          <summary>Levels</summary>
          <label>Pitch <input v-model.number="audio.demoPitch" type="range" min="0" max="1" step="0.01" /></label>
          <label>Volume <input v-model.number="audio.demoVolume" type="range" min="0" max="1" step="0.01" /></label>
        </details>
  
        <p v-if="badgeToast" class="humit__toast" :class="{ 'humit__toast--spark': toastSpark }">
          {{ badgeToast }}
        </p>
  
        <div class="humit__footer-actions">
          <button type="button" class="humit__btn humit__btn--ghost humit__btn--sm" aria-label="Exit game" @click="restartWelcome">
            ✕
          </button>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import HumItCreature from "./HumItCreature.vue"
  import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue"
  import { injectKidsTheme } from "../../composables/useKidsTheme.js"
  import { useHumAudio } from "../../composables/useHumAudio.js"
  import { useHumItOst } from "../../composables/useHumItOst.js"
  
  const { isDarkMode } = injectKidsTheme()
  const audio = useHumAudio()
  const humitOst = useHumItOst()
  
  const CREATURE_KEY = "humit-creature-v1"
  
  const phase = ref("welcome")
  const demoMode = ref(false)
  const score = ref(0)
  const streak = ref(0)
  const birthProgress = ref(0)
  const birthLabel = ref("")
  const badgeToast = ref("")
  const toastSpark = ref(false)
  const creatureWobble = ref(0)
  const lastWinBoost = ref(false)
  const creatureExpressVol = ref(0)
  const creatureExpressPitch = ref(0.5)
  const creaturePop = ref(false)
  const burstTicks = ref(false)
  const buddyName = ref("")
  
  const syncOkMs = ref(0)
  const volSpike = ref(0)
  const shellSpike = ref(false)
  const rippleFire = ref(false)
  let prevVolPlay = 0
  let shellSpikeTimer = 0
  let rippleTimer = 0
  
  let popTimer = 0
  let burstTimer = 0
  let toastSparkTimer = 0
  
  const STAR_FIELD = Array.from({ length: 26 }, (_, i) => ({
    i,
    style: {
      left: `${(i * 41 + 5) % 94}%`,
      top: `${(i * 59 + 9) % 72}%`,
      animationDelay: `${(i % 9) * 0.31}s`,
    },
  }))
  
  const starDots = STAR_FIELD
  
  const creatureVisual = ref({
    hue: 168,
    limbs: 4,
    roundness: 0.45,
  })
  
  let badgeTimer = 0
  let birthRaf = 0
  let playRaf = 0
  let challengeStart = 0
  let challengeIndex = 0
  let okMs = 0
  let demoHumHeld = 0
  let lastPlayTs = 0
  
  const CHALLENGES = [
    {
      id: "high",
      emoji: "⬆️",
      hint: "Hum higher.",
      whisper: "Slide pitch upward, steady tone.",
      windowMs: 5200,
      satisfied: s => s.p > 0.58 && s.v > 0.038,
    },
    {
      id: "low",
      emoji: "⬇️",
      hint: "Hum lower.",
      whisper: "Drop pitch warm and slow.",
      windowMs: 5200,
      satisfied: s => s.p < 0.42 && s.v > 0.038,
    },
    {
      id: "loud",
      emoji: "📣",
      hint: "Hum louder.",
      whisper: "Comfortable volume into the mic.",
      windowMs: 4500,
      satisfied: s => s.v > 0.13,
    },
    {
      id: "soft",
      emoji: "🤫",
      hint: "Tiny hum.",
      whisper: "Quiet but steady.",
      windowMs: 5000,
      satisfied: s => s.v > 0.025 && s.v < 0.085,
    },
    {
      id: "silent",
      emoji: "✨",
      hint: "Shhh — silence.",
      whisper: "Hold quiet to recharge.",
      windowMs: 4200,
      satisfied: s => s.v < 0.024,
    },
    {
      id: "steady",
      emoji: "🏃",
      hint: "Smooth steady hum.",
      whisper: "Same pitch, no wobble.",
      windowMs: 5500,
      satisfied: s => s.v > 0.042 && s.stable,
    },
    {
      id: "long",
      emoji: "🪽",
      hint: "Hold one long hum.",
      whisper: "One sustained note.",
      windowMs: 8200,
      satisfied: s => s.contHum > 1700,
    },
  ]
  
  const currentChallenge = computed(() => CHALLENGES[challengeIndex % CHALLENGES.length])
  
  const pitchBarPct = computed(() => Math.round(audio.effectivePitchNorm() * 100))
  const volumeBarPct = computed(() => Math.round(audio.effectiveVolume() * 100))
  
  const challengeTimerPct = computed(() => {
    if (phase.value !== "play") return 100
    const w = currentChallenge.value.windowMs
    const t = performance.now() - challengeStart
    return Math.max(0, Math.min(100, (1 - t / w) * 100))
  })
  
  const resonanceLockPct = computed(() => Math.min(100, Math.round((syncOkMs.value / 240) * 100)))
  
  const isNearResonanceLock = computed(
    () => phase.value === "play" && syncOkMs.value >= 140 && syncOkMs.value < 240,
  )
  
  const isTimerPanic = computed(
    () => phase.value === "play" && challengeTimerPct.value < 26 && syncOkMs.value < 95,
  )
  
  const flowTier = computed(() => {
    if (streak.value < 3) return null
    return (1 + 0.5 * Math.floor(streak.value / 3)).toFixed(1)
  })
  
  const sectionAura = computed(() => {
    const hue = creatureVisual.value.hue ?? 168
    const v = creatureExpressVol.value
    const streakGlow = Math.min(1, streak.value / 10)
    const spin = phase.value === "play" ? Math.max(2.4, 9 - v * 6.5) : 6.5
    const auroraShift = (creatureExpressPitch.value - 0.5) * 55
    return {
      "--hum-spin": `${spin}s`,
      "--hum-hue-core": hue,
      "--hum-hue-ring": hue + 48,
      "--hum-streak-glow": streakGlow,
      "--hum-aurora-shift": `${auroraShift}deg`,
      "--hum-breathe": `${0.92 + v * 0.14}`,
    }
  })
  
  function deriveBuddyName(data) {
    const hue = typeof data.hue === "number" ? data.hue : 168
    const limbs = typeof data.limbs === "number" ? data.limbs : 4
    const roundness = typeof data.roundness === "number" ? data.roundness : 0.45
    const PREFIX = ["Glim", "Hum", "Zhu", "Woo", "Mel", "Du", "Ba", "Lo", "Ki", "Flo"]
    const SUFFIX = ["blob", "muffin", "pip", "loom", "bean", "fuzz", "drop", "note", "roll", "mist"]
    const seed = Math.abs(Math.round(hue * 13 + limbs * 19 + roundness * 100))
    const a = PREFIX[seed % PREFIX.length]
    const b = SUFFIX[Math.floor(seed / 7) % SUFFIX.length]
    return `${a}${b}`
  }
  
  function pulseCelebrate() {
    if (popTimer) window.clearTimeout(popTimer)
    creaturePop.value = true
    popTimer = window.setTimeout(() => {
      creaturePop.value = false
      popTimer = 0
    }, 620)
  
    if (burstTimer) window.clearTimeout(burstTimer)
    burstTicks.value = true
    burstTimer = window.setTimeout(() => {
      burstTicks.value = false
      burstTimer = 0
    }, 780)
  }
  
  function loadCreature() {
    try {
      const raw = localStorage.getItem(CREATURE_KEY)
      if (!raw) return
      const data = JSON.parse(raw)
      if (typeof data.hue === "number") creatureVisual.value = { ...creatureVisual.value, ...data }
      buddyName.value = deriveBuddyName(creatureVisual.value)
    } catch {
      //
    }
  }
  
  function saveCreature(patch) {
    creatureVisual.value = { ...creatureVisual.value, ...patch }
    buddyName.value = deriveBuddyName(creatureVisual.value)
    try {
      localStorage.setItem(CREATURE_KEY, JSON.stringify(creatureVisual.value))
    } catch {
      //
    }
  }
  
  function showBadge(text, sparkle = false) {
    badgeToast.value = text
    toastSpark.value = sparkle
    if (toastSparkTimer) window.clearTimeout(toastSparkTimer)
    toastSparkTimer = window.setTimeout(() => {
      toastSpark.value = false
      toastSparkTimer = 0
    }, 900)
    if (badgeTimer) window.clearTimeout(badgeTimer)
    badgeTimer = window.setTimeout(() => {
      badgeToast.value = ""
      badgeTimer = 0
    }, 2800)
  }
  
  function cancelBirthAnim() {
    if (birthRaf) window.cancelAnimationFrame(birthRaf)
    birthRaf = 0
  }
  
  function cancelPlayLoop() {
    if (playRaf) window.cancelAnimationFrame(playRaf)
    playRaf = 0
  }
  
  async function goBirth(asDemo) {
    await humitOst.start()
    demoMode.value = asDemo
    audio.errorMessage.value = ""
    if (asDemo) {
      audio.stop()
      audio.demoPitch.value = 0.45
      audio.demoVolume.value = 0.12
    } else {
      audio.demoVolume.value = 0
    }
  
    phase.value = "birth"
    birthProgress.value = 0
    birthLabel.value = asDemo ? "Sliders · 3s" : "Mic…"
  
    if (!asDemo) {
      await audio.start()
      if (audio.status.value !== "live") {
        birthLabel.value = "Mic off · Demo"
        demoMode.value = true
      } else {
        birthLabel.value = "Hum · 3s"
      }
    }
  
    const samples = { pitch: 0, vol: 0, n: 0 }
    const started = performance.now()
  
    function birthFrame(t) {
      const elapsed = t - started
      birthProgress.value = Math.min(1, elapsed / 3000)
  
      const p = audio.effectivePitchNorm()
      const v = audio.effectiveVolume()
      creatureExpressPitch.value = p
      creatureExpressVol.value = v
      humitOst.tick(p, v)
      if (v > 0.03) {
        samples.pitch += p
        samples.vol += v
        samples.n += 1
      }
  
      if (elapsed < 3000) {
        birthRaf = window.requestAnimationFrame(birthFrame)
      } else {
        cancelBirthAnim()
        const avgP = samples.n ? samples.pitch / samples.n : 0.45
        const avgV = samples.n ? samples.vol / samples.n : 0.08
        const hue = Math.round(120 + avgP * 200 + avgV * 40)
        const limbs = avgP > 0.55 ? 3 : avgP < 0.4 ? 5 : 4
        const roundness = Math.min(0.85, 0.35 + avgV * 1.2)
        saveCreature({ hue, limbs, roundness })
        pulseCelebrate()
        showBadge(`${buddyName.value} ready!`, true)
        startPlay()
      }
    }
  
    birthRaf = window.requestAnimationFrame(birthFrame)
  }
  
  function startPlay() {
    cancelPlayLoop()
    phase.value = "play"
    score.value = 0
    streak.value = 0
    challengeIndex = Math.floor(Math.random() * CHALLENGES.length)
    challengeStart = performance.now()
    okMs = 0
    demoHumHeld = 0
    lastPlayTs = performance.now()
    lastWinBoost.value = false
    syncOkMs.value = 0
    prevVolPlay = 0
    volSpike.value = 0
    shellSpike.value = false
    rippleFire.value = false
  
    playRaf = window.requestAnimationFrame(playLoop)
  }
  
  function playLoop(ts) {
    if (phase.value !== "play") return
  
    const dt = lastPlayTs ? Math.min(48, ts - lastPlayTs) : 16
    lastPlayTs = ts
  
    const p = audio.effectivePitchNorm()
    const v = audio.effectiveVolume()
    const stable = audio.humStable.value
  
    if (demoMode.value && v > 0.045) demoHumHeld += dt
    else if (!demoMode.value) demoHumHeld = 0
  
    const contHum = demoMode.value ? demoHumHeld : audio.continuousHumMs.value
  
    creatureExpressPitch.value = p
    creatureExpressVol.value = v
  
    creatureWobble.value = Math.sin(ts / 220) * (0.04 + v * 0.22)
  
    const ch = CHALLENGES[challengeIndex % CHALLENGES.length]
    const snap = { p, v, stable, contHum }
  
    if (ch.satisfied(snap)) okMs += dt
    else okMs = Math.max(0, okMs - dt * 1.8)
  
    syncOkMs.value = okMs
  
    volSpike.value = Math.min(1, volSpike.value * 0.86 + Math.max(0, v - prevVolPlay) * 9)
    if (v - prevVolPlay > 0.042) {
      shellSpike.value = true
      if (shellSpikeTimer) window.clearTimeout(shellSpikeTimer)
      shellSpikeTimer = window.setTimeout(() => {
        shellSpike.value = false
        shellSpikeTimer = 0
      }, 220)
      rippleFire.value = true
      if (rippleTimer) window.clearTimeout(rippleTimer)
      rippleTimer = window.setTimeout(() => {
        rippleFire.value = false
        rippleTimer = 0
      }, 900)
    }
    prevVolPlay = v
  
    humitOst.tick(p, v)
  
    if (okMs > 240) {
      score.value += 25 + streak.value * 3
      streak.value += 1
      lastWinBoost.value = true
      pulseCelebrate()
      window.setTimeout(() => {
        lastWinBoost.value = false
      }, 550)
  
      if (ch.id === "long") showBadge("Wings!", true)
      else if (ch.id === "silent") showBadge("Charged!", true)
      else if (ch.id === "loud") showBadge("Bright!", true)
      else showBadge("Nice!", true)
  
      nextChallenge()
    } else if (ts - challengeStart > ch.windowMs) {
      streak.value = 0
      score.value += 5
      lastWinBoost.value = false
      showBadge("Next!")
      nextChallenge()
    }
  
    playRaf = window.requestAnimationFrame(playLoop)
  }
  
  function nextChallenge() {
    challengeIndex += 1
    challengeStart = performance.now()
    okMs = 0
    syncOkMs.value = 0
    demoHumHeld = 0
    lastPlayTs = performance.now()
  }
  
  function restartWelcome() {
    cancelBirthAnim()
    cancelPlayLoop()
    audio.stop()
    humitOst.stop()
    if (shellSpikeTimer) window.clearTimeout(shellSpikeTimer)
    if (rippleTimer) window.clearTimeout(rippleTimer)
    shellSpikeTimer = 0
    rippleTimer = 0
    shellSpike.value = false
    rippleFire.value = false
    prevVolPlay = 0
    volSpike.value = 0
    syncOkMs.value = 0
    creatureExpressVol.value = 0
    creatureExpressPitch.value = 0.5
    phase.value = "welcome"
  }
  
  watch(phase, val => {
    if (val !== "play") cancelPlayLoop()
  })
  
  onMounted(() => {
    loadCreature()
  })
  
  onBeforeUnmount(() => {
    if (badgeTimer) window.clearTimeout(badgeTimer)
    if (popTimer) window.clearTimeout(popTimer)
    if (burstTimer) window.clearTimeout(burstTimer)
    if (toastSparkTimer) window.clearTimeout(toastSparkTimer)
    if (shellSpikeTimer) window.clearTimeout(shellSpikeTimer)
    if (rippleTimer) window.clearTimeout(rippleTimer)
    cancelBirthAnim()
    cancelPlayLoop()
    audio.stop()
    humitOst.stop()
  })
  </script>
  
  <style scoped>
  @import url("https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=DM+Sans:wght@500;600;700&display=swap");
  
  .humit__sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
  
  .humit {
    --hum-bg: linear-gradient(180deg, #cfeaff 0%, #e8fff4 42%, #fff8e7 100%);
    --hum-ink: #1b2540;
    --hum-muted: #5a6687;
    --hum-card: rgba(255, 255, 255, 0.88);
    --hum-border: rgba(80, 120, 200, 0.18);
    --hum-spin: 6s;
    --hum-hue-core: 168;
    --hum-hue-ring: 216;
    --hum-streak-glow: 0;
    --hum-aurora-shift: 0deg;
    --hum-breathe: 1;
  
    position: relative;
    border-radius: 22px;
    padding: 14px 14px 18px;
    min-height: 420px;
    overflow: hidden;
    font-family: "DM Sans", sans-serif;
    color: var(--hum-ink);
    background: var(--hum-bg);
    border: 1.5px solid var(--hum-border);
  }
  
  .humit--dark {
    --hum-bg: linear-gradient(180deg, #0f1730 0%, #142238 40%, #10252e 100%);
    --hum-ink: #eef3ff;
    --hum-muted: #a7b4da;
    --hum-card: rgba(22, 30, 54, 0.92);
    --hum-border: rgba(130, 170, 255, 0.22);
  }
  
  .humit__sky {
    position: absolute;
    inset: 0;
    background:
      radial-gradient(circle at 22% 18%, hsla(calc(var(--hum-hue-core) + 48), 92%, 72%, 0.42), transparent 46%),
      radial-gradient(circle at 78% 12%, hsla(calc(var(--hum-hue-ring)), 85%, 68%, 0.32), transparent 42%),
      radial-gradient(circle at 50% 88%, hsla(calc(var(--hum-hue-core) + 22), 70%, 58%, 0.18), transparent 55%);
    pointer-events: none;
    transform: scale(var(--hum-breathe));
    transition: transform 0.25s ease-out;
  }
  
  .humit__aurora {
    position: absolute;
    inset: -40% -20%;
    background: conic-gradient(
      from calc(120deg + var(--hum-aurora-shift)),
      hsla(calc(var(--hum-hue-core) + 80), 95%, 70%, 0) 0deg,
      hsla(calc(var(--hum-hue-ring) + 40), 90%, 72%, 0.22) 58deg,
      hsla(calc(var(--hum-hue-core) + 120), 88%, 68%, 0.14) 118deg,
      hsla(calc(var(--hum-hue-ring)), 92%, 62%, 0) 220deg,
      hsla(calc(var(--hum-hue-core) + 60), 95%, 74%, 0.18) 300deg,
      hsla(calc(var(--hum-hue-core) + 80), 95%, 70%, 0) 360deg
    );
    opacity: 0.85;
    animation: humitAuroraDrift 14s ease-in-out infinite;
    pointer-events: none;
    mix-blend-mode: multiply;
  }
  
  .humit--dark .humit__aurora {
    mix-blend-mode: screen;
    opacity: 0.55;
  }
  
  .humit__stars-field {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1;
  }
  
  .humit__star {
    position: absolute;
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background: #fff;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.85);
    opacity: 0.45;
    animation: humitStarTwinkle 3.2s ease-in-out infinite;
  }
  
  .humit__glyphs {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    overflow: hidden;
  }
  
  .humit__glyph {
    position: absolute;
    font-size: 1.35rem;
    opacity: 0.22;
    color: hsl(calc(var(--hum-hue-ring)), 72%, 42%);
    animation: humitGlyphFloat 7s ease-in-out infinite;
  }
  
  .humit__glyph--a {
    left: 10%;
    top: 22%;
  }
  .humit__glyph--b {
    right: 12%;
    top: 18%;
    animation-duration: 9s;
    animation-delay: -2s;
  }
  .humit__glyph--c {
    left: 18%;
    bottom: 34%;
    animation-duration: 8s;
    animation-delay: -1s;
  }
  .humit__glyph--d {
    right: 16%;
    bottom: 38%;
    animation-duration: 10s;
    animation-delay: -3s;
  }
  
  .humit__hills {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 38%;
    background:
      radial-gradient(
        ellipse 120% 80% at 50% 100%,
        hsla(calc(var(--hum-hue-core) + 80), 72%, 52%, calc(0.28 + var(--hum-streak-glow) * 0.28)),
        transparent 72%
      ),
      radial-gradient(ellipse 90% 70% at 30% 100%, rgba(90, 200, 140, 0.22), transparent 66%);
    pointer-events: none;
    z-index: 0;
  }
  
  .humit__top {
    position: relative;
    z-index: 2;
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 12px;
  }
  
  .humit__title {
    font-family: "Baloo 2", cursive;
    font-size: 1.35rem;
    font-weight: 800;
    margin: 0;
    line-height: 1.15;
  }
  
  .humit__top-aside {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: flex-end;
    gap: 8px;
  }
  
  .humit__music-btn {
    width: 44px;
    height: 44px;
    border-radius: 999px;
    border: 1px solid var(--hum-border);
    background: var(--hum-card);
    cursor: pointer;
    font-size: 1.15rem;
    display: grid;
    place-items: center;
    box-shadow: 0 6px 16px hsla(calc(var(--hum-hue-core)), 55%, 48%, 0.08);
    transition: opacity 0.2s ease, transform 0.2s ease;
  }
  
  .humit__music-btn:hover {
    transform: translateY(-2px);
  }
  
  .humit__music-btn--muted {
    opacity: 0.45;
  }
  
  .humit__stats {
    display: flex;
    gap: 8px;
  }
  
  .humit__pill {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 5px 10px;
    border-radius: 999px;
    background: var(--hum-card);
    border: 1px solid var(--hum-border);
  }
  
  .humit__pill strong {
    font-family: "Baloo 2", cursive;
    margin-left: 4px;
  }
  
  .humit__pill--stat {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: "Baloo 2", cursive;
    font-weight: 800;
    font-size: 0.78rem;
  }
  
  .humit__pill-ico {
    opacity: 0.88;
    font-size: 0.72rem;
  }
  
  .humit__panel {
    position: relative;
    z-index: 2;
    padding: 14px;
    border-radius: 18px;
    background: var(--hum-card);
    border: 1px solid var(--hum-border);
  }
  
  .humit__panel--hero {
    padding: 18px;
  }
  
  .humit__welcome-lead {
    margin: 0;
    font-size: 0.84rem;
    color: var(--hum-muted);
    line-height: 1.35;
  }
  
  .humit__actions--welcome {
    margin-top: 12px;
  }
  
  .humit__actions {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .humit__btn {
    cursor: pointer;
    border-radius: 14px;
    padding: 11px 16px;
    font-family: "Baloo 2", cursive;
    font-weight: 800;
    font-size: 0.92rem;
    border: none;
  }
  
  .humit__btn--primary {
    background: linear-gradient(135deg, #7c5cff, #4fd1ff);
    color: #fff;
    box-shadow: 0 8px 22px rgba(100, 140, 255, 0.35);
  }
  
  .humit__btn--ghost {
    background: rgba(120, 160, 255, 0.12);
    color: var(--hum-ink);
    border: 1px solid var(--hum-border);
  }
  
  .humit__btn--sm {
    font-size: 0.85rem;
    padding: 8px 14px;
    min-width: 44px;
    min-height: 44px;
    border-radius: 12px;
  }
  
  .humit__err {
    margin-top: 12px;
    font-size: 0.82rem;
    color: #c24141;
  }
  
  .humit__challenge {
    font-family: "Baloo 2", cursive;
    font-weight: 800;
    font-size: 1rem;
  }
  
  .humit__birth-meter {
    height: 8px;
    border-radius: 999px;
    background: rgba(120, 140, 200, 0.15);
    margin: 10px 0 14px;
    overflow: hidden;
  }
  
  .humit__birth-meter span {
    display: block;
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, #7c5cff, #4fd1ff);
    transition: width 0.05s linear;
  }
  
  .humit__creature-shell {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  
  .humit__creature-shell--pop {
    animation: humitCreaturePop 0.62s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  
  .humit__creature-shell--play {
    min-height: 200px;
  }
  
  .humit__orbit {
    position: absolute;
    width: min(300px, 78vw);
    height: min(300px, 78vw);
    pointer-events: none;
  }
  
  .humit__orbit-ring {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 2px dashed hsla(calc(var(--hum-hue-ring)), 82%, 62%, 0.35);
    animation: humitOrbitSpin var(--hum-spin) linear infinite;
  }
  
  .humit__orbit-ring--b {
    inset: 14%;
    border-style: solid;
    border-width: 1px;
    opacity: 0.5;
    animation-direction: reverse;
    animation-duration: calc(var(--hum-spin) * 1.35);
  }
  
  .humit__creature-shell--micro-spike {
    animation: humitMicroSpike 0.22s ease-out;
  }
  
  .humit__ripple-pack {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
    z-index: 1;
  }
  
  .humit__ripple {
    position: absolute;
    width: 42%;
    aspect-ratio: 1;
    border-radius: 50%;
    border: 2px solid hsla(calc(var(--hum-hue-ring)), 88%, 68%, 0.38);
    opacity: 0;
    transform: scale(0.55);
  }
  
  .humit__ripple-pack--fire .humit__ripple {
    animation: humitRippleOut 0.88s ease-out forwards;
  }
  
  .humit__ripple-pack--fire .humit__ripple--d {
    animation-delay: 0.12s;
  }
  
  .humit__ripple-pack--fire .humit__ripple--dd {
    animation-delay: 0.24s;
  }
  
  .humit__creature-wrap {
    display: flex;
    justify-content: center;
    margin: 8px 0;
    position: relative;
    z-index: 2;
  }
  
  .humit__burst {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
    z-index: 3;
  }
  
  .humit__burst-ray {
    position: absolute;
    width: 4px;
    height: 44%;
    border-radius: 4px;
    background: linear-gradient(
      180deg,
      hsla(calc(var(--hum-hue-ring)), 92%, 72%, 0.95),
      hsla(calc(var(--hum-hue-core) + 40), 88%, 62%, 0)
    );
    transform-origin: center bottom;
    bottom: 50%;
    left: calc(50% - 2px);
    opacity: 0;
    animation: humitBurstRay 0.72s ease-out forwards;
  }
  
  .humit__burst-ray:nth-child(1) {
    transform: rotate(-75deg);
  }
  .humit__burst-ray:nth-child(2) {
    transform: rotate(-50deg);
    animation-delay: 0.03s;
  }
  .humit__burst-ray:nth-child(3) {
    transform: rotate(-25deg);
    animation-delay: 0.06s;
  }
  .humit__burst-ray:nth-child(4) {
    transform: rotate(0deg);
    animation-delay: 0.09s;
  }
  .humit__burst-ray:nth-child(5) {
    transform: rotate(25deg);
    animation-delay: 0.12s;
  }
  .humit__burst-ray:nth-child(6) {
    transform: rotate(50deg);
    animation-delay: 0.15s;
  }
  .humit__burst-ray:nth-child(7) {
    transform: rotate(75deg);
    animation-delay: 0.18s;
  }
  .humit__burst-ray:nth-child(8) {
    transform: rotate(100deg);
    animation-delay: 0.05s;
  }
  .humit__burst-ray:nth-child(9) {
    transform: rotate(-100deg);
    animation-delay: 0.08s;
  }
  .humit__burst-ray:nth-child(10) {
    transform: rotate(115deg);
    animation-delay: 0.11s;
  }
  .humit__burst-ray:nth-child(11) {
    transform: rotate(-115deg);
    animation-delay: 0.14s;
  }
  .humit__burst-ray:nth-child(12) {
    transform: rotate(135deg);
    animation-delay: 0.17s;
  }
  .humit__burst-ray:nth-child(13) {
    transform: rotate(-135deg);
    animation-delay: 0.2s;
  }
  .humit__burst-ray:nth-child(14) {
    transform: rotate(155deg);
    animation-delay: 0.23s;
  }
  
  .humit__constellation {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 7px;
    z-index: 1;
  }
  
  .humit__cstar {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.28);
    transition: transform 0.35s ease, box-shadow 0.35s ease, background 0.35s ease;
  }
  
  .humit__cstar--lit {
    background: hsl(calc(var(--hum-hue-ring)), 92%, 72%);
    border-color: hsla(calc(var(--hum-hue-ring)), 92%, 82%, 0.95);
    box-shadow: 0 0 14px hsla(calc(var(--hum-hue-ring)), 92%, 68%, 0.65);
    transform: scale(1.15) translateY(-2px);
  }
  
  .humit__hint {
    font-size: 0.82rem;
    color: var(--hum-muted);
    text-align: center;
  }
  
  .humit__hint--compact {
    margin-top: 8px;
    font-size: 0.76rem;
  }
  
  .humit__demo {
    margin-top: 12px;
    font-size: 0.8rem;
  }
  
  .humit__demo label {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 8px;
  }
  
  .humit__demo--inline {
    position: relative;
    z-index: 2;
  }
  
  .humit__play {
    position: relative;
    z-index: 2;
  }
  
  .humit__challenge-card {
    padding: 14px;
    border-radius: 18px;
    background: var(--hum-card);
    border: 1px solid var(--hum-border);
    margin-bottom: 12px;
    box-shadow: 0 14px 34px hsla(calc(var(--hum-hue-core)), 62%, 48%, 0.08);
    transition: border-color 0.35s ease, box-shadow 0.35s ease;
  }
  
  .humit__challenge-card--high {
    border-color: hsla(calc(var(--hum-hue-ring) + 20), 82%, 62%, 0.35);
  }
  .humit__challenge-card--low {
    border-color: hsla(calc(var(--hum-hue-core) + 40), 58%, 42%, 0.38);
  }
  .humit__challenge-card--loud {
    border-color: hsla(32, 92%, 58%, 0.42);
    box-shadow: 0 14px 36px rgba(255, 176, 60, 0.14);
  }
  .humit__challenge-card--soft {
    border-color: hsla(270, 52%, 72%, 0.35);
  }
  .humit__challenge-card--silent {
    border-color: hsla(210, 72%, 72%, 0.35);
  }
  .humit__challenge-card--steady {
    border-color: hsla(155, 62%, 48%, 0.38);
  }
  .humit__challenge-card--long {
    border-color: hsla(calc(var(--hum-hue-ring)), 78%, 68%, 0.42);
  }
  
  .humit__challenge-card--locking {
    box-shadow:
      0 0 0 2px hsla(calc(var(--hum-hue-ring)), 88%, 62%, 0.42),
      0 14px 34px hsla(calc(var(--hum-hue-core)), 62%, 48%, 0.08);
  }
  
  .humit__challenge-card--panic {
    animation: humitCardNudge 0.55s ease-in-out infinite;
  }
  
  .humit__timer--panic span {
    background: linear-gradient(90deg, #fb7185, #f97316) !important;
  }
  
  .humit__timer--rush {
    opacity: 0.92;
  }
  
  .humit__challenge-row {
    display: flex;
    gap: 12px;
    align-items: center;
  }
  
  .humit__challenge-copy {
    flex: 1;
    min-width: 0;
  }
  
  .humit__challenge-row .humit__emoji {
    margin: 0;
    font-size: 1.85rem;
    flex-shrink: 0;
  }
  
  .humit__emoji {
    font-size: 1.6rem;
    display: inline-block;
    margin-bottom: 4px;
    filter: drop-shadow(0 4px 10px hsla(calc(var(--hum-hue-ring)), 70%, 55%, 0.25));
  }
  
  .humit__challenge-line {
    font-size: 1rem;
    font-weight: 700;
    line-height: 1.25;
    margin: 0;
  }
  
  .humit__lockon {
    margin-top: 12px;
  }
  
  .humit__lockon-track {
    position: relative;
    height: 7px;
    border-radius: 999px;
    background: rgba(120, 140, 200, 0.12);
    overflow: hidden;
  }
  
  .humit__lockon-fill {
    display: block;
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(
      90deg,
      hsl(155, 72%, 52%),
      hsl(calc(var(--hum-hue-ring)), 82%, 58%)
    );
    transition: width 0.07s linear;
  }
  
  .humit__lockon-threshold {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: rgba(255, 255, 255, 0.55);
    opacity: 0.65;
    pointer-events: none;
  }
  
  .humit__timer {
    height: 6px;
    border-radius: 999px;
    margin-top: 10px;
    background: rgba(120, 140, 200, 0.15);
    overflow: hidden;
  }
  
  .humit__timer span {
    display: block;
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(
      90deg,
      hsl(calc(var(--hum-hue-core) + 60), 72%, 62%),
      hsl(calc(var(--hum-hue-ring)), 82%, 58%)
    );
  }
  
  .humit__sonic {
    position: absolute;
    left: 8%;
    right: 8%;
    top: 8%;
    height: 100px;
    pointer-events: none;
    z-index: 0;
  }
  
  .humit__sonic-arc {
    position: absolute;
    left: 50%;
    bottom: 0;
    width: 130%;
    height: 72px;
    margin-left: -65%;
    border-radius: 50% 50% 0 0 / 100% 100% 0 0;
    border: 2px solid hsla(calc(var(--hum-hue-ring)), 72%, 62%, 0.14);
    border-bottom: none;
    animation: humitSonicPulse 2.8s ease-in-out infinite;
  }
  
  .humit__sonic-arc--b {
    animation-delay: 0.4s;
    opacity: 0.65;
    transform: scale(0.9);
  }
  
  .humit__sonic-arc--c {
    animation-delay: 0.8s;
    opacity: 0.4;
    transform: scale(0.78);
  }
  
  .humit__flow-badge {
    position: absolute;
    top: 6px;
    right: 8px;
    z-index: 2;
    padding: 6px 11px;
    border-radius: 999px;
    background: var(--hum-card);
    border: 1px solid hsla(calc(var(--hum-hue-ring)), 72%, 58%, 0.35);
    box-shadow: 0 8px 22px hsla(calc(var(--hum-hue-core)), 55%, 48%, 0.12);
  }
  
  .humit__flow-mult {
    font-family: "Baloo 2", cursive;
    font-weight: 800;
    font-size: 1.05rem;
    color: var(--hum-ink);
  }
  
  .humit__stage {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 18px 8px 34px;
  }
  
  .humit__cloud {
    position: absolute;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.55);
    filter: blur(0.5px);
    opacity: 0.85;
  }
  
  .humit__cloud--a {
    width: 70px;
    height: 26px;
    top: 26%;
    left: 8%;
    animation: cloudDrift 8s ease-in-out infinite;
  }
  
  .humit__cloud--b {
    width: 90px;
    height: 30px;
    top: 38%;
    right: 6%;
    animation: cloudDrift 10s ease-in-out infinite reverse;
  }
  
  .humit__cloud--c {
    width: 56px;
    height: 20px;
    top: 52%;
    left: 42%;
    opacity: 0.65;
    animation: cloudDrift 12s ease-in-out infinite 1s;
  }
  
  @keyframes humitAuroraDrift {
    0%,
    100% {
      transform: translate(0, 0) rotate(0deg);
    }
    50% {
      transform: translate(2%, -3%) rotate(4deg);
    }
  }
  
  @keyframes humitStarTwinkle {
    0%,
    100% {
      opacity: 0.25;
      transform: scale(0.85);
    }
    50% {
      opacity: 0.95;
      transform: scale(1.05);
    }
  }
  
  @keyframes humitGlyphFloat {
    0%,
    100% {
      transform: translateY(0) rotate(-6deg);
      opacity: 0.18;
    }
    50% {
      transform: translateY(-16px) rotate(8deg);
      opacity: 0.32;
    }
  }
  
  @keyframes humitOrbitSpin {
    to {
      transform: rotate(360deg);
    }
  }
  
  @keyframes humitCreaturePop {
    0% {
      transform: scale(1);
    }
    35% {
      transform: scale(1.07);
    }
    100% {
      transform: scale(1);
    }
  }
  
  @keyframes humitBurstRay {
    0% {
      opacity: 0;
      height: 10%;
    }
    30% {
      opacity: 1;
      height: 48%;
    }
    100% {
      opacity: 0;
      height: 62%;
    }
  }
  
  @keyframes humitRippleOut {
    0% {
      opacity: 0;
      transform: scale(0.55);
    }
    35% {
      opacity: 0.55;
    }
    100% {
      opacity: 0;
      transform: scale(1.38);
    }
  }
  
  @keyframes humitMicroSpike {
    0%,
    100% {
      transform: scale(1);
    }
    45% {
      transform: scale(1.035);
    }
  }
  
  @keyframes humitCardNudge {
    0%,
    100% {
      transform: translateX(0);
    }
    50% {
      transform: translateX(-2px);
    }
  }
  
  @keyframes humitStatPulse {
    0%,
    100% {
      transform: scale(1);
      opacity: 1;
    }
    50% {
      transform: scale(1.03);
      opacity: 0.92;
    }
  }
  
  @keyframes humitPanicTint {
    0%,
    100% {
      box-shadow: inset 0 0 0 transparent;
    }
    50% {
      box-shadow: inset 0 0 42px rgba(255, 96, 96, 0.12);
    }
  }
  
  @keyframes humitSonicPulse {
    0%,
    100% {
      opacity: 0.22;
    }
    50% {
      opacity: 0.72;
    }
  }
  
  @keyframes cloudDrift {
    0%,
    100% {
      transform: translateX(0);
    }
    50% {
      transform: translateX(12px);
    }
  }
  
  .humit--panic {
    animation: humitPanicTint 0.85s ease-in-out infinite;
  }
  
  .humit__stats--pulse .humit__pill {
    animation: humitStatPulse 0.65s ease-in-out infinite;
  }
  
  .humit__meter {
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: center;
    gap: 8px;
  }
  
  .humit__meter-label {
    font-size: 0.95rem;
    opacity: 0.72;
    width: 1.1rem;
    text-align: center;
  }
  
  .humit__meters--compact {
    margin-top: 4px;
  }
  
  .humit__meters {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--hum-muted);
  }
  
  .humit__meter .humit__bar {
    margin-top: 0;
  }
  
  .humit__bar {
    margin-top: 4px;
    height: 10px;
    border-radius: 999px;
    background: rgba(120, 140, 200, 0.12);
    overflow: hidden;
  }
  
  .humit__bar i {
    display: block;
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
  }
  
  .humit__bar--vol i {
    background: linear-gradient(90deg, #34d399, #fbbf24);
  }
  
  .humit__toast {
    margin-top: 12px;
    text-align: center;
    font-family: "Baloo 2", cursive;
    font-weight: 800;
    font-size: 0.95rem;
    color: #047857;
    padding: 10px 14px;
    border-radius: 14px;
    background: hsla(calc(var(--hum-hue-core) + 80), 72%, 94%, 0.65);
    border: 1px solid hsla(calc(var(--hum-hue-ring)), 62%, 72%, 0.28);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
  }
  
  .humit__toast--spark {
    animation: humitToastGlow 0.85s ease-out;
    box-shadow: 0 12px 36px hsla(calc(var(--hum-hue-ring)), 72%, 58%, 0.28);
  }
  
  .humit--dark .humit__toast {
    color: #a7f3d0;
    background: hsla(calc(var(--hum-hue-core)), 42%, 22%, 0.65);
    border-color: hsla(calc(var(--hum-hue-ring)), 52%, 52%, 0.35);
  }
  
  @keyframes humitToastGlow {
    0% {
      transform: scale(0.96);
    }
    40% {
      transform: scale(1.02);
    }
    100% {
      transform: scale(1);
    }
  }
  
  .humit__footer-actions {
    margin-top: 12px;
    display: flex;
    justify-content: flex-end;
  }
  
  @media (max-width: 520px) {
    .humit__top-aside {
      width: 100%;
      justify-content: space-between;
    }
  
    .humit__stats {
      flex: 1;
      justify-content: flex-end;
    }
  }
  </style>
  