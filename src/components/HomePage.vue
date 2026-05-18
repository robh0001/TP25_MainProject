<template>
  <div class="home-page" :class="{ 'home-loaded': isLoaded }" @mousemove="onMouseMove">

    <!-- Background -->
    <div class="home-bg" data-hover-read-ignore="true" aria-hidden="true">
      <img
        class="home-bg-img"
        :style="bgParallaxStyle"
        src="https://images.unsplash.com/photo-1542037104857-ffbb0b9155fb?auto=format&fit=crop&w=2400&q=90"
        alt=""
        aria-hidden="true"
      />
      <div class="home-bg-overlay"></div>
      <div class="home-bg-vignette"></div>
      <div class="home-bg-grain"></div>
    </div>

      <!-- Floating spark particles (no emoji) -->
    <div class="float-layer" aria-hidden="true">
      <span
        v-for="(sp, idx) in sparks"
        :key="`sp-${idx}`"
        class="spark-particle"
        :style="{
          left: `${sp.left}%`,
          top: `${sp.top}%`,
          width: `${sp.size}px`,
          height: `${sp.size}px`,
          animationDelay: `${sp.delay}s`,
          animationDuration: `${sp.duration}s`,
        }"
      ></span>
    </div>

    <!-- Animated wave divider -->
    <svg class="wave-divider" viewBox="0 0 1440 140" preserveAspectRatio="none" aria-hidden="true">
      <path class="wave wave-1" d="M0,80 C240,20 480,140 720,80 C960,20 1200,140 1440,80 L1440,140 L0,140 Z"></path>
      <path class="wave wave-2" d="M0,100 C240,40 480,160 720,100 C960,40 1200,160 1440,100 L1440,140 L0,140 Z"></path>
      <path class="wave wave-3" d="M0,120 C240,60 480,180 720,120 C960,60 1200,180 1440,120 L1440,140 L0,140 Z"></path>
    </svg>
    
    <!-- Header -->
    <header class="home-header" aria-label="Website header">
      <RouterLink
        to="/"
        class="home-logo"
        aria-label="Go to HealthyKids home page"
      >
        <div class="home-logo-icon" aria-hidden="true">
          <svg
            viewBox="0 0 36 36"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
            focusable="false"
          >
            <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2"/>
            <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor"/>
            <path d="M18 13C15.5 15.5 15 19 18 23" stroke="white" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.55"/>
          </svg>
        </div>

        <span class="home-logo-text">HealthyKids</span>
      </RouterLink>

      <RouterLink
        to="/parent-entry"
        class="home-header-pill"
        aria-label="Go to parent portal"
      >
        Parent portal
        <svg
          width="12"
          height="12"
          viewBox="0 0 12 12"
          aria-hidden="true"
          focusable="false"
        >
          <path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </RouterLink>
    </header>

    <!-- Main -->
    <main
      class="home-main"
      aria-label="HealthyKids home page introduction"
    >
      <div class="home-copy">

        <div
          class="home-eyebrow"
          aria-label="Australia 2026"
          data-hover-read-text
        >
          <span class="home-eyebrow-dot" aria-hidden="true"></span>
          Australia · 2026
        </div>

        <h1
          class="home-headline"
          aria-label="Healthier families start here."
          data-hover-read-text
        >
          <span class="home-headline-line home-headline-line-1 home-morph-line">
            <transition name="home-morph" mode="out-in">
              <span :key="cycleWord" class="home-morph-word">{{ cycleWord }}</span>
            </transition>
          </span>
          <span class="home-headline-line home-headline-line-2">
            <span class="home-line-2-word">
                families
                <svg
                  class="home-families-underline-svg"
                  viewBox="0 0 240 16"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  aria-hidden="true"
                >
                  <path
                    class="home-families-underline-path"
                    pathLength="100"
                    d="M 10 9 Q 120 14 230 9"
                    stroke="currentColor"
                    stroke-width="4"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    vector-effect="non-scaling-stroke"
                  />
                </svg>
              </span></span>
          <span class="home-headline-line home-headline-line-3">start here.</span>
        </h1>
        
        <p class="home-sub">
          A personalised health plan for children aged 5-12,
          built around nutrition, movement, sleep and daily routine.
        </p>
        <div
          class="home-tag-ticker"
          role="region"
          aria-label="HealthyKids feature highlights"
          data-hover-read-text="HealthyKids feature highlights. Nutrition made simple. Hydration habits. Better sleep routines. Playful movement. Plans parents trust. Experiences kids love."
        >
          <div class="home-tag-ticker-mask">
            <div class="home-tag-ticker-track">
              <span
                v-for="(phrase, i) in tickerLoop"
                :key="`tk-${i}`"
                class="home-tag-ticker-chip"
                :aria-hidden="i >= tickerPhrases.length ? 'true' : 'false'"
                :data-hover-read-text="i < tickerPhrases.length ? phrase : null"
              >
                {{ phrase }}
              </span>
            </div>
          </div>
        </div>
        <div
          class="home-ctas"
          aria-label="Primary actions"
        >
          <RouterLink
            to="/parent-entry"
            class="home-cta home-cta--primary"
            aria-label="Enter the HealthyKids site"
            :style="ctaMagneticStyle"
              @mousemove="onCtaMove"
              @mouseleave="onCtaLeave"
          >
            Enter site
          </RouterLink>
        </div>

        <div
          class="home-pills"
          aria-label="HealthyKids quick highlights"
        >
        
          <span
            class="home-pill"
            aria-label="More than 12,000 Australian families supported"
            data-hover-read-text
          >
            <span class="home-pill-dot" aria-hidden="true"></span>
            12,000+ families
          </span>

          <span
            class="home-pill"
            aria-label="Suitable for children aged 5 to 12"
            data-hover-read-text
          >
            <span class="home-pill-dot" aria-hidden="true"></span>
            Ages 5-12
          </span>

          <span
            class="home-pill"
            aria-label="Three minute onboarding"
            data-hover-read-text
          >
            <span class="home-pill-dot" aria-hidden="true"></span>
            3-min onboarding
          </span>
        </div>
      </div>
    </main>

    <!-- Footer bar -->
    <footer class="home-footer-shell" aria-label="Website footer">
      <svg
        class="home-footer-waves"
        viewBox="0 0 1200 96"
        preserveAspectRatio="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="homeFootMainGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="rgba(94, 234, 212, 0.38)" />
            <stop offset="18%" stop-color="rgba(34, 197, 94, 0.22)" />
            <stop offset="42%" stop-color="rgba(15, 55, 38, 0.82)" />
            <stop offset="100%" stop-color="rgba(3, 12, 8, 0.96)" />
          </linearGradient>

          <linearGradient id="homeFootBackWaveGrad" x1="0" y1="0" x2="1200" y2="0" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stop-color="rgba(45, 212, 191, 0.14)" />
            <stop offset="35%" stop-color="rgba(74, 222, 128, 0.2)" />
            <stop offset="70%" stop-color="rgba(56, 189, 248, 0.1)" />
            <stop offset="100%" stop-color="rgba(45, 212, 191, 0.12)" />
          </linearGradient>

          <radialGradient id="homeFootGlowA" cx="22%" cy="28%" r="55%">
            <stop offset="0%" stop-color="rgba(167, 243, 208, 0.35)" />
            <stop offset="55%" stop-color="rgba(74, 222, 128, 0.08)" />
            <stop offset="100%" stop-color="rgba(74, 222, 128, 0)" />
          </radialGradient>

          <radialGradient id="homeFootGlowB" cx="82%" cy="22%" r="48%">
            <stop offset="0%" stop-color="rgba(103, 232, 249, 0.28)" />
            <stop offset="60%" stop-color="rgba(45, 212, 191, 0.06)" />
            <stop offset="100%" stop-color="rgba(45, 212, 191, 0)" />
          </radialGradient>

          <linearGradient id="homeFootRimLight" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="rgba(255, 255, 255, 0.45)" />
            <stop offset="100%" stop-color="rgba(255, 255, 255, 0)" />
          </linearGradient>
        </defs>

        <rect
          class="home-footer-wave-plate"
          x="-400"
          y="74"
          width="2000"
          height="22"
          fill="#050f0b"
        />

        <g class="home-footer-wave-parallax">
          <path
            fill="url(#homeFootBackWaveGrad)"
            d="M0 56 C220 34 380 72 600 48 C780 28 960 62 1200 46 L1200 96 L0 96 Z"
          />
        </g>

        <g class="home-footer-wave-aurora-wrap">
          <rect class="home-footer-wave-aurora" x="0" y="0" width="1200" height="96" fill="url(#homeFootGlowA)" />
          <rect class="home-footer-wave-aurora home-footer-wave-aurora--b" x="0" y="0" width="1200" height="96" fill="url(#homeFootGlowB)" />
        </g>

        <g class="home-footer-wave-motion">
          <path
            class="home-footer-wave-fill"
            fill="url(#homeFootMainGrad)"
            d="M0 42 C200 14 400 64 600 34 C800 6 1000 52 1200 30 L1200 96 L0 96 Z"
          />
          <path
            class="home-footer-wave-rim"
            fill="none"
            stroke="url(#homeFootRimLight)"
            stroke-width="1.25"
            stroke-linecap="round"
            opacity="0.55"
            d="M0 40 C205 12 405 62 605 32 C805 4 1005 50 1200 28"
          />
          <path
            class="home-footer-wave-stroke home-footer-wave-stroke--a"
            fill="none"
            stroke="rgba(167, 243, 208, 0.55)"
            stroke-width="2"
            stroke-linecap="round"
            d="M0 38 C210 10 410 60 610 30 C810 2 1010 48 1200 26"
          />
          <path
            class="home-footer-wave-stroke home-footer-wave-stroke--b"
            fill="none"
            stroke="rgba(255, 255, 255, 0.2)"
            stroke-width="1.5"
            stroke-linecap="round"
            d="M0 48 C195 26 395 68 595 40 C795 14 995 56 1200 36"
          />
          <circle class="home-footer-wave-bubble home-footer-wave-bubble--a" cx="168" cy="36" r="2.2" fill="rgba(236, 253, 245, 0.55)" />
          <circle class="home-footer-wave-bubble home-footer-wave-bubble--b" cx="612" cy="30" r="1.6" fill="rgba(165, 243, 252, 0.45)" />
          <circle class="home-footer-wave-bubble home-footer-wave-bubble--c" cx="972" cy="34" r="1.8" fill="rgba(190, 242, 100, 0.4)" />
        </g>
      </svg>

      <div class="home-footer">
        <div
          class="home-footer-left"
          aria-label="Supporting families across Australia"
          data-hover-read-text
        >
          <span class="home-live-dot" aria-hidden="true"></span>
          Supporting families across Australia
        </div>

        <div
          class="home-footer-right"
          aria-label="UN Sustainable Development Goal 3, Good Health and Wellbeing. Developed by Team SYRBYX."
          data-hover-read-text
        >
          <span>UN SDG 3 · Good Health &amp; Wellbeing</span>
          <span class="home-footer-divider" aria-hidden="true">·</span>
          <span>Developed by Team SYRBYX</span>
        </div>
      </div>
    </footer>
    <Teleport to="body">
        <div
          v-if="showOnboarding"
          class="onboarding-backdrop"
          role="presentation"
          @click.self="closeOnboarding"
        >
          <div
            ref="onboardingDialogEl"
            class="onboarding-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="onboarding-title"
            tabindex="-1"
            @keydown.escape.prevent="closeOnboarding"
          >
            <div class="onboarding-head">
              <p class="onboarding-kicker">Quick tour · about 3 minutes</p>
              <h2 id="onboarding-title" class="onboarding-title">{{ currentOnboardingStep.title }}</h2>
              <div class="onboarding-progress" aria-hidden="true">
                <span
                  v-for="(_, i) in onboardingSteps"
                  :key="`ob-${i}`"
                  class="onboarding-dot"
                  :class="{ active: i === onboardingStepIndex }"
                ></span>
              </div>
            </div>
            <p class="onboarding-body">{{ currentOnboardingStep.body }}</p>
            <div class="onboarding-actions">
              <button type="button" class="ob-btn ob-btn--ghost" @click="closeOnboarding">Close</button>
              <div class="ob-btn-row">
                <button
                  v-if="onboardingStepIndex > 0"
                  type="button"
                  class="ob-btn ob-btn--ghost"
                  @click="prevOnboarding"
                >
                  Back
                </button>
                <button
                  v-if="onboardingStepIndex < onboardingSteps.length - 1"
                  type="button"
                  class="ob-btn ob-btn--primary"
                  @click="nextOnboarding"
                >
                  Next
                </button>
                <template v-else>
                  <RouterLink to="/parent-entry" class="ob-btn ob-btn--primary" @click="closeOnboarding">
                    Parent portal
                  </RouterLink>
                  <RouterLink to="/kids-dashboard" class="ob-btn ob-btn--ghost ob-btn--outline" @click="closeOnboarding">
                    Kids zone
                  </RouterLink>
                </template>
              </div>
            </div>
          </div>
        </div>
      </Teleport>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router"
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue"


const isLoaded = ref(false)
const mouse = reactive({ x: 0, y: 0 })
const ctaOffset = reactive({ x: 0, y: 0 })

const cycleWords = ["Healthier", "Happier", "Stronger", "Brighter", "Active"]
const cycleIndex = ref(0)
const cycleWord = computed(() => cycleWords[cycleIndex.value])
let cycleTimer = 0

const sparks = Array.from({ length: 28 }, (_, i) => ({
  id: i,
  left: Math.random() * 100,
  top: Math.random() * 100,
  size: 2 + Math.random() * 3,
  delay: Math.random() * 6,
  duration: 4 + Math.random() * 6,
}))

const counters = reactive({
  families: 0,
  ageMin: 0,
  ageMax: 0,
})

const targetCounters = { families: 12000, ageMin: 5, ageMax: 12 }

const tickerPhrases = [
  'Nutrition made simple',
  'Hydration habits',
  'Better sleep routines',
  'Plans parents trust',
  'Experiences kids love',
  'Track habits gently',
  'Mini-games for healthy choices',
  'One hub for family wellbeing',
  'Tune it to your child',
]

const tickerLoop = computed(() => [...tickerPhrases, ...tickerPhrases])

const onboardingSteps = [
  {
    title: "Welcome to HealthyKids",
    body:
      "HealthyKids helps families build steady routines around food, drinks, sleep, and movement without turning health into a chore.",
  },
  {
    title: "Plans tuned to ages 5-12",
    body:
      "You get a structured path that fits primary-school life: simple targets, gentle reminders, and clarity on what to try next.",
  },
  {
    title: "Two sides of the same journey",
    body:
      "Parents use tools and dashboards to steer the plan. Kids get a playful zone with games and streaks so wins feel rewarding.",
  },
  {
    title: "Daily rhythm, not perfection",
    body:
      "Small consistent actions beat big sporadic ones. Log meals, sips, and wins when it works for you - progress compounds over time.",
  },
  {
    title: "You're ready to dive in",
    body:
      "That's the essence of our ~3-minute onboarding. Pick where you want to start: set things up as a parent or jump into the kids experience.",
  },
]

const showOnboarding = ref(false)
const onboardingStepIndex = ref(0)
const onboardingDialogEl = ref(null)

const currentOnboardingStep = computed(() => onboardingSteps[onboardingStepIndex.value])

function openOnboarding() {
  onboardingStepIndex.value = 0
  showOnboarding.value = true
  nextTick(() => onboardingDialogEl.value?.focus?.())
}

function closeOnboarding() {
  showOnboarding.value = false
}

function nextOnboarding() {
  if (onboardingStepIndex.value < onboardingSteps.length - 1) {
    onboardingStepIndex.value += 1
  }
}

function prevOnboarding() {
  if (onboardingStepIndex.value > 0) {
    onboardingStepIndex.value -= 1
  }
}

const bgParallaxStyle = computed(() => ({
  transform: `scale(1.08) translate(${mouse.x * -10}px, ${mouse.y * -10}px)`,
}))

const ctaMagneticStyle = computed(() => ({
  transform: `translate(${ctaOffset.x}px, ${ctaOffset.y}px)`,
}))

function onMouseMove(e) {
  const w = window.innerWidth || 1
  const h = window.innerHeight || 1
  mouse.x = (e.clientX / w) * 2 - 1
  mouse.y = (e.clientY / h) * 2 - 1
}

function onCtaMove(e) {
  const target = e.currentTarget
  if (!target) return
  const rect = target.getBoundingClientRect()
  const cx = rect.left + rect.width / 2
  const cy = rect.top + rect.height / 2
  ctaOffset.x = (e.clientX - cx) * 0.18
  ctaOffset.y = (e.clientY - cy) * 0.22
}

function onCtaLeave() {
  ctaOffset.x = 0
  ctaOffset.y = 0
}

function formatNumber(n) {
  if (n >= 1000) return `${Math.round(n / 100) / 10}k`
  return Math.round(n).toString()
}

function runCounter(target, key, duration = 1800) {
  const start = performance.now()
  const from = counters[key]
  function tick(now) {
    const t = Math.min(1, (now - start) / duration)
    const eased = 1 - Math.pow(1 - t, 3)
    counters[key] = from + (target - from) * eased
    if (t < 1) requestAnimationFrame(tick)
    else counters[key] = target
  }
  requestAnimationFrame(tick)
}

onMounted(() => {
  setTimeout(() => {
    isLoaded.value = true
    runCounter(targetCounters.families, "families")
    runCounter(targetCounters.ageMin, "ageMin", 900)
    runCounter(targetCounters.ageMax, "ageMax", 900)
  }, 80)

  cycleTimer = window.setInterval(() => {
    cycleIndex.value = (cycleIndex.value + 1) % cycleWords.length
  }, 2600)
})



watch(showOnboarding, open => {
  if (typeof document === "undefined") return
  document.documentElement.classList.toggle("hk-onboarding-lock", open)
})

onBeforeUnmount(() => {
  if (cycleTimer) window.clearInterval(cycleTimer)
  document.documentElement.classList.remove("hk-onboarding-lock")
})
</script>
