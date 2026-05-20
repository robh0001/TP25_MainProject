<!--
  HomePage.vue

  Main HealthyKids landing page.

  Main features:
  - Shows the brand header and parent portal link.
  - Displays animated background particles, waves, and hero text.
  - Highlights the rotating headline and "families" underline.
  - Explains the website and links users to the parent entry page.
  - Shows quick trust pills, SDG 3 footer, and team attribution.

  Accessibility:
  - Uses aria-labels for key landmarks and actions.
  - Supports hover-to-read with data-hover-read-text.
  - Hides decorative visuals with aria-hidden="true".
  - Uses keyboard-friendly RouterLink and button elements.
  - Uses an accessible onboarding modal with dialog, aria-modal, focus handling, and Escape close.
-->
<template>
  <div class="home-page" :class="{ 'home-loaded': isLoaded }">
    <!-- Hero / header section -->
    <section class="home-hero-shell" aria-label="HealthyKids introduction" @mousemove="onMouseMove">
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

      <svg class="wave-divider" viewBox="0 0 1440 140" preserveAspectRatio="none" aria-hidden="true">
        <path class="wave wave-1" d="M0,80 C240,20 480,140 720,80 C960,20 1200,140 1440,80 L1440,140 L0,140 Z"></path>
        <path class="wave wave-2" d="M0,100 C240,40 480,160 720,100 C960,40 1200,160 1440,100 L1440,140 L0,140 Z"></path>
        <path class="wave wave-3" d="M0,120 C240,60 480,180 720,120 C960,60 1200,180 1440,120 L1440,140 L0,140 Z"></path>
      </svg>

      <main class="home-main" aria-label="HealthyKids home page introduction">
        <div class="home-copy">
          <div class="home-eyebrow" aria-label="Australia 2026" data-hover-read-text>
            <span class="home-eyebrow-dot" aria-hidden="true"></span>
            Australia · 2026
          </div>

          <h1 class="home-headline" aria-label="Healthier families start here." data-hover-read-text>
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
              </span>
            </span>

            <span class="home-headline-line home-headline-line-3">start here.</span>
          </h1>

          <p class="home-sub">
            A personalised health plan for children aged 5-12,
            built around nutrition, movement, sleep and daily routine.
          </p>


          <div class="home-ctas" aria-label="Primary actions">
            <RouterLink
              to="/parent-entry"
              class="home-cta home-cta--primary"
              aria-label="Enter the HealthyKids site"
              :style="ctaMagneticStyle"
              @mousemove="onCtaMove"
              @mouseleave="onCtaLeave"
            >
              Get Started
            </RouterLink>

            <button
              type="button"
              class="home-cta home-cta--secondary"
              aria-label="Learn how HealthyKids works"
              @click="openOnboarding"
            >
              How it works
            </button>
          </div>

          <div class="home-pills" aria-label="HealthyKids quick highlights">
            <span class="home-pill" aria-label="More than 12,000 Australian families supported" data-hover-read-text>
              <span class="home-pill-dot" aria-hidden="true"></span>
              12,000+ families
            </span>

            <span class="home-pill" aria-label="Suitable for children aged 5 to 12" data-hover-read-text>
              <span class="home-pill-dot" aria-hidden="true"></span>
              Ages 5-12
            </span>

            <span class="home-pill" aria-label="Three minute onboarding" data-hover-read-text>
              <span class="home-pill-dot" aria-hidden="true"></span>
              3-min onboarding
            </span>
          </div>
        </div>
      </main>
    </section>

    <!-- Updated content after the header -->
    <div class="home-content-sections">
      <section class="section section--about" aria-labelledby="about-heading">
        <div class="section-inner">
          <div class="section-header">
            <p class="kicker">What HealthyKids does</p>
            <h2 id="about-heading" class="section-title">
              One place to plan, guide and track healthier family routines.
            </h2>
          </div>

          <div class="pillars" aria-label="Core features">
            <article v-for="pillar in pillars" :key="pillar.title" class="pillar-card" :aria-label="pillar.title">
              <div class="pillar-icon" aria-hidden="true">{{ pillar.icon }}</div>
              <h3 class="pillar-title">{{ pillar.title }}</h3>
              <p class="pillar-body">{{ pillar.body }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="section section--steps" aria-labelledby="steps-heading">
        <div class="section-inner section-inner--split">
          <div class="steps-copy">
            <p class="kicker">How to begin</p>
            <h2 id="steps-heading" class="section-title">
              Start with the parent portal, then follow the daily plan.
            </h2>
            <p class="section-body">
              The website is designed to be simple. Create a parent profile,
              complete the short setup, and use the dashboard to follow daily
              health actions with your family.
            </p>
            <RouterLink to="/parent-entry" class="btn btn--primary steps-cta" aria-label="Go to parent portal">
              Go to parent portal
            </RouterLink>
          </div>

          <ol class="steps-list" aria-label="Getting started steps">
            <li
              v-for="step in steps"
              :key="step.number"
              class="step-item"
              :aria-label="`Step ${step.number}: ${step.title}`"
            >
              <span class="step-num" aria-hidden="true">{{ step.number }}</span>
              <div class="step-text">
                <h3 class="step-title">{{ step.title }}</h3>
                <p class="step-body">{{ step.body }}</p>
              </div>
            </li>
          </ol>
        </div>
      </section>

      <section class="section section--audience" aria-labelledby="audience-heading">
        <div class="section-inner">
          <p class="kicker" id="audience-heading">Two experiences, one goal</p>

          <div class="audience-grid">
            <article class="audience-card audience-card--parent" aria-label="For parents">
              <div class="audience-card-inner">
                <div class="audience-icon" aria-hidden="true">
                  <svg viewBox="0 0 40 40" fill="none">
                    <circle cx="20" cy="14" r="6" stroke="currentColor" stroke-width="1.6" />
                    <path
                      d="M8 34c0-6.627 5.373-12 12-12s12 5.373 12 12"
                      stroke="currentColor"
                      stroke-width="1.6"
                      stroke-linecap="round"
                    />
                  </svg>
                </div>

                <h3>For parents</h3>
                <p>
                  Set up the family profile, review personalised plans,
                  and track daily progress from the parent dashboard.
                </p>

                <RouterLink to="/parent-entry" class="audience-link" aria-label="Go to parent portal">
                  Parent portal
                  <svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">
                    <path
                      d="M2 7h10M8 4l3 3-3 3"
                      stroke="currentColor"
                      stroke-width="1.4"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </RouterLink>
              </div>
            </article>

            <article class="audience-card audience-card--kids" aria-label="For children">
              <div class="audience-card-inner">
                <div class="audience-icon" aria-hidden="true">
                  <svg viewBox="0 0 40 40" fill="none">
                    <path
                      d="M20 8l2.5 7.5H30l-6.5 4.5 2.5 7.5L20 23l-6 4.5 2.5-7.5L10 15.5h7.5L20 8Z"
                      stroke="currentColor"
                      stroke-width="1.6"
                      stroke-linejoin="round"
                    />
                  </svg>
                </div>

                <h3>For children</h3>
                <p>
                  Children aged 5–12 can view their goals, build streaks,
                  and stay motivated through the playful kids zone.
                </p>

                <RouterLink to="/kids-dashboard" class="audience-link" aria-label="Go to kids zone">
                  Kids zone
                  <svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">
                    <path
                      d="M2 7h10M8 4l3 3-3 3"
                      stroke="currentColor"
                      stroke-width="1.4"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </RouterLink>
              </div>
            </article>
          </div>
        </div>
      </section>

      <footer class="site-footer" aria-label="Site footer">
        <div class="footer-inner">
          <div>
            <p class="footer-brand-name">HealthyKids</p>
            <p class="footer-tagline">Supporting families across Australia.</p>
          </div>

          <div class="footer-meta">
            <span>UN SDG 3 · Good Health &amp; Wellbeing</span>
            <span class="footer-sep" aria-hidden="true">·</span>
            <span>Developed by Team SYRBYX</span>
          </div>
        </div>
      </footer>
    </div>

    <!-- Onboarding modal -->
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
            <h2 id="onboarding-title" class="onboarding-title">
              {{ currentOnboardingStep.title }}
            </h2>

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
            <button type="button" class="ob-btn ob-btn--ghost" @click="closeOnboarding">
              Close
            </button>

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

                <RouterLink
                  to="/kids-dashboard"
                  class="ob-btn ob-btn--ghost ob-btn--outline"
                  @click="closeOnboarding"
                >
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
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from "vue"
import { RouterLink } from "vue-router"

const isLoaded = ref(false)

const mouse = reactive({
  x: 0,
  y: 0,
})

const ctaOffset = reactive({
  x: 0,
  y: 0,
})

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


const pillars = [
  {
    icon: "🥗",
    title: "Nutrition",
    body: "Simple, family-friendly food and drink guidance built around everyday habits.",
  },
  {
    icon: "🏃",
    title: "Movement",
    body: "Realistic daily activity goals that suit primary-school children.",
  },
  {
    icon: "🌙",
    title: "Sleep & routine",
    body: "Steadier sleep, screen-time and daily structure developed over time.",
  },
  {
    icon: "📊",
    title: "Parent dashboard",
    body: "A clear view of plans, progress and next actions for the whole family.",
  },
]

const steps = [
  {
    number: "01",
    title: "Get Started",
    body: "Begin by opening HelthyKidz and starting the family health journey.",
  },
  {
    number: "02",
    title: "Build Profile",
    body: "Create a parent profile by entering your child's age range, habits, concerns and routine.",
  },
  {
    number: "03",
    title: "Today's Plan",
    body: "Use the dashboard to follow today's nutrition, movement, sleep and routine actions.",
  },
  {
    number: "04",
    title: "4-week Roadmap",
    body: "Review the weekly roadmap to understand the focus areas and next steps for your family.",
  },
  {
    number: "05",
    title: "Meal Ideas",
    body: "Explore nutrition tools and recipe ideas that support healthier everyday choices.",
  },
]

const onboardingSteps = [
  {
    title: "Welcome to HealthyKids",
    body: "HealthyKids helps families build steady routines around food, drinks, sleep, and movement without turning health into a chore.",
  },
  {
    title: "Plans tuned to ages 5-12",
    body: "You get a structured path that fits primary-school life: simple targets, gentle reminders, and clarity on what to try next.",
  },
  {
    title: "Two sides of the same journey",
    body: "Parents use tools and dashboards to steer the plan. Kids get a playful zone with games and streaks so wins feel rewarding.",
  },
  {
    title: "Daily rhythm, not perfection",
    body: "Small consistent actions beat big sporadic ones. Log meals, sips, and wins when it works for you — progress compounds over time.",
  },
  {
    title: "You're ready to dive in",
    body: "That's the essence of our quick onboarding. Pick where you want to start: set things up as a parent or jump into the kids experience.",
  },
]

const showOnboarding = ref(false)
const onboardingStepIndex = ref(0)
const onboardingDialogEl = ref(null)

const currentOnboardingStep = computed(() => onboardingSteps[onboardingStepIndex.value])

const bgParallaxStyle = computed(() => ({
  transform: `scale(1.08) translate(${mouse.x * -10}px, ${mouse.y * -10}px)`,
}))

const ctaMagneticStyle = computed(() => ({
  transform: `translate(${ctaOffset.x}px, ${ctaOffset.y}px)`,
}))

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

function onMouseMove(e) {
  const width = window.innerWidth || 1
  const height = window.innerHeight || 1

  mouse.x = (e.clientX / width) * 2 - 1
  mouse.y = (e.clientY / height) * 2 - 1
}

function onCtaMove(e) {
  const target = e.currentTarget

  if (!target) return

  const rect = target.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2

  ctaOffset.x = (e.clientX - centerX) * 0.18
  ctaOffset.y = (e.clientY - centerY) * 0.22
}

function onCtaLeave() {
  ctaOffset.x = 0
  ctaOffset.y = 0
}

onMounted(() => {
  window.setTimeout(() => {
    isLoaded.value = true
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
  if (cycleTimer) {
    window.clearInterval(cycleTimer)
  }

  document.documentElement.classList.remove("hk-onboarding-lock")
})
</script>



<style>
.hk-onboarding-lock {
  overflow: hidden;
}
</style>