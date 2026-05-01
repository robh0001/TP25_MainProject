<template>
  <div class="dashboard-page">
    <div class="noise-overlay" aria-hidden="true"></div>

    <header class="header" :class="{ scrolled: isScrolled }">
      <div class="header-inner">
        <RouterLink to="/" class="logo">
          <div class="logo-icon">
            <svg viewBox="0 0 36 36" fill="none">
              <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2" />
              <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor" />
              <path d="M18 13C15.5 15.5 15 19 18 23" stroke="white" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.55" />
            </svg>
          </div>
          <span class="logo-text">HealthyKids</span>
        </RouterLink>

        <nav class="nav">
          <RouterLink to="/" class="nav-a">Home</RouterLink>
          <RouterLink to="/parent-entry" class="nav-a">Parent access</RouterLink>
          <RouterLink to="/young-person-dashboard" class="nav-a">Kids dashboard</RouterLink>
        </nav>

        <div class="nav-cta">
          <RouterLink to="/parent-quiz" class="nav-link">Retake quiz</RouterLink>
          <RouterLink to="/parent-quiz" class="nav-btn">
            New plan
            <svg width="12" height="12" viewBox="0 0 12 12">
              <path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </RouterLink>
        </div>
      </div>
    </header>

    <div v-if="planLoading" class="plan-loading">
      <p>Loading your personalised family plan...</p>
    </div>

    <div v-else-if="planError" class="plan-error">
      <p>Could not load your family plan: {{ planError }}</p>
      <button type="button" @click="fetchPlan(state.username)">Retry</button>
    </div>

    <div v-else-if="!isPlanReady" class="plan-error">
      <p>No family plan found yet. Please complete the parent quiz first.</p>
      <RouterLink to="/parent-quiz" class="nav-btn">Complete quiz</RouterLink>
    </div>

    <main v-else>
      <section class="dash-hero">
        <div class="dash-hero-bg">
          <div class="hero-blob hb-1"></div>
          <div class="hero-blob hb-2"></div>
          <div class="hero-lines" aria-hidden="true">
            <span v-for="n in 8" :key="n"></span>
          </div>
        </div>

        <div class="dash-hero-inner">
          <div class="dash-hero-left">
            <div class="eyebrow-row">
              <div class="live-badge">
                <span class="live-dot"></span>
                Parent dashboard · Week {{ currentWeek }}
              </div>
            </div>

            <h1 class="dash-h1">
              <span class="dh-serif">Good {{ timeOfDay }},</span>
            </h1>

            <p class="dash-hero-desc">
              Your 4-week planner is loaded from the database and displayed as weekly and daily scheduled actions.
            </p>

            <div class="hero-kpi-row">
              <div class="hkpi">
                <div class="hkpi-val">{{ streakDays }}</div>
                <div class="hkpi-lbl">Day streak</div>
              </div>
              <div class="hkpi-div"></div>
              <div class="hkpi">
                <div class="hkpi-val">{{ roadmapCompletion }}%</div>
                <div class="hkpi-lbl">Roadmap done</div>
              </div>
              <div class="hkpi-div"></div>
              <div class="hkpi">
                <div class="hkpi-val">{{ completedTodayCount }}/{{ todayFullSchedule.length }}</div>
                <div class="hkpi-lbl">Today's tasks</div>
              </div>
              <div class="hkpi-div"></div>
              <div class="hkpi">
                <div class="hkpi-val">{{ weeklyAverage }}%</div>
                <div class="hkpi-lbl">Weekly avg.</div>
              </div>
            </div>
          </div>

          <div class="dash-hero-right">
            <div class="mission-card" :class="{ celebrate: showCelebration }">
              <div v-if="showCelebration" class="confetti-layer" aria-hidden="true">
                <span v-for="p in confettiPieces" :key="p.id" class="confetti-piece" :style="p.style"></span>
              </div>

              <div class="mission-top">
                <div class="mission-eyebrow">Daily progress</div>
                <div class="streak-chip">{{ streakDays }}-day streak</div>
              </div>

              <h2 class="mission-title">{{ completedTodayCount }} of {{ todayFullSchedule.length }} actions done today</h2>
              <p class="mission-desc">Track the database-fetched plan as your family completes each scheduled action.</p>

              <div class="mission-progress-wrap">
                <div class="mp-labels">
                  <span>Today's progress</span>
                  <span>{{ todayProgress }}%</span>
                </div>
                <div class="mp-track">
                  <div class="mp-fill" :style="{ width: todayProgress + '%' }"></div>
                </div>
              </div>

              <button class="mission-btn" @click="completeMission">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M3 8l3.5 3.5L13 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                Add to streak
              </button>
            </div>
          </div>
        </div>
      </section>

      <section class="today-section">
        <div class="section-wrap">
          <div class="section-head-row">
            <div class="section-head-left">
              <div class="section-eyebrow">Today's plan</div>
              <h2 class="section-h2">
                {{ todayName }}'s<br />
                <em>actions.</em>
              </h2>
              <p class="section-desc">
                {{ completedTodayCount }} of {{ todayFullSchedule.length }} scheduled actions completed today.
              </p>
            </div>

            <div class="today-score-block">
              <div class="tsb-pct">{{ todayProgress }}<span>%</span></div>
              <div class="tsb-lbl">Today's progress</div>
              <div class="tsb-track">
                <div class="tsb-fill" :style="{ width: todayProgress + '%' }"></div>
              </div>
            </div>
          </div>

          <div class="today-schedule-card">
            <div class="tsc-header">
              <div>
                <div class="tsc-day">{{ todayName }}</div>
                <div class="tsc-sub">{{ childName }}'s database-fetched schedule</div>
              </div>
              <div class="tsc-pct-chip" :class="todayProgress === 100 ? 'chip-green' : 'chip-default'">{{ todayProgress }}%</div>
            </div>

            <div class="tsc-progress-bar">
              <div class="tsc-pb-fill" :style="{ width: todayProgress + '%' }"></div>
            </div>

            <div class="tsc-timeline">
              <div
                v-for="slot in todayFullSchedule"
                :key="slot.id"
                class="tsc-slot"
                :class="['tsc-' + slot.category, { done: slot.done }]"
              >
                <div class="tsc-time-col">
                  <span class="tsc-time">{{ slot.time }}</span>
                </div>
                <div class="tsc-slot-line">
                  <div class="tsc-dot" :class="{ done: slot.done }"></div>
                  <div class="tsc-line"></div>
                </div>
                <label class="tsc-content">
                  <input type="checkbox" :checked="slot.done" @change="toggleTodayScheduleSlot(slot)" />
                  <div class="tsc-card" :class="{ done: slot.done }">
                    <div class="tsc-card-row">
                      <span class="tsc-cat-badge" :class="'badge-' + slot.category">{{ slot.categoryLabel }}</span>
                      <span class="tsc-check" :class="{ done: slot.done }">
                        <svg v-if="slot.done" width="10" height="10" viewBox="0 0 10 10">
                          <path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                      </span>
                    </div>
                    <span class="tsc-text">{{ slot.text }}</span>
                    <span v-if="slot.detail" class="tsc-detail">{{ slot.detail }}</span>
                    <span v-if="slot.tip" class="tsc-detail">{{ slot.tip }}</span>
                  </div>
                </label>
              </div>

              <p v-if="!todayFullSchedule.length" class="tsc-empty">
                No scheduled actions found for {{ todayName }}.
              </p>
            </div>
          </div>
        </div>
      </section>
<section class="roadmap-section" id="roadmap">
        <div class="section-wrap">
          <div class="section-head-row">
            <div class="section-head-left">
              <div class="section-eyebrow">4-week habit roadmap</div>
              <h2 class="section-h2">
                Your personalised<br />
                <em>habit journey.</em>
              </h2>
              <p class="section-desc">
                These weeks, days, meals, workouts, exercises and sleep tips are fetched from the family-plan API.
              </p>
            </div>

            <div class="roadmap-score-block">
              <div class="rsb-ring" :style="roadmapRingStyle">
                <div class="rsb-ring-inner">
                  <div class="rsb-pct">{{ roadmapCompletion }}<span>%</span></div>
                  <div class="rsb-lbl">complete</div>
                </div>
              </div>
              <div class="rsb-meta">
                <div class="rsb-num">{{ completedRoadmapActions }}<span>/{{ totalRoadmapActions }}</span></div>
                <div class="rsb-desc">scheduled actions completed</div>
                <div class="rsb-focus-chip">{{ childName }}</div>
              </div>
            </div>
          </div>

          <div class="roadmap-weeks">
            <button
              v-for="week in fourWeekRoadmap"
              :key="week.id"
              class="rweek-card"
              :class="{
                active: week.id === activeRoadmapWeek,
                completed: week.statusKey === 'completed',
                'in-progress': week.statusKey === 'in-progress'
              }"
              @click="activeRoadmapWeek = week.id"
            >
              <div class="rweek-top">
                <span class="rweek-num">Week {{ week.week }}</span>
                <span class="rweek-status" :class="'rs-' + week.statusKey">{{ week.status }}</span>
              </div>
              <h3 class="rweek-title">{{ week.title }}</h3>
              <p class="rweek-summary">{{ week.summary }}</p>
              <div class="rweek-progress-wrap">
                <div class="rweek-track">
                  <div class="rweek-fill" :style="{ width: week.progress + '%' }"></div>
                </div>
                <span class="rweek-pct">{{ week.progress }}%</span>
              </div>
              <div class="rweek-done-count">{{ week.completed }}/{{ week.totalItems }} actions</div>
            </button>
          </div>

          <div class="roadmap-detail">
            <div class="roadmap-detail-main">
              <div class="rdm-header">
                <div>
                  <div class="rdm-eyebrow">Selected · Week {{ selectedRoadmapWeek.week }}</div>
                  <h3 class="rdm-title">{{ selectedRoadmapWeek.title }}</h3>
                </div>
                <div class="rdm-header-actions">
                  <div class="rdm-week-badge">Week {{ selectedRoadmapWeek.week }}</div>
                </div>
              </div>

              <div class="rdm-day-plan-block">
                <div class="rdm-day-plan-head">
                  <div>
                    <span>Daily schedule for Week {{ selectedRoadmapWeek.week }}</span>
                    <p>Only API-fetched time slots are shown below.</p>
                  </div>
                  <strong>{{ selectedRoadmapWeek.dailyCompleted }}/{{ selectedRoadmapWeek.dailyTotal }} done</strong>
                </div>

                <div class="rdm-day-plan-grid">
                  <article
                    v-for="day in currentFirstRoadmapDailyPlan"
                    :key="day.day"
                    class="rdm-day-card"
                    :class="{ today: day.day === todayName }"
                  >
                    <div class="rdm-day-card-head">
                      <div>
                        <span class="rdm-day-name">{{ getShortDayName(day.day) }}</span>
                        <small v-if="day.day === todayName">Today</small>
                      </div>
                      <strong>{{ day.completed }}/{{ day.timeSlots?.length || 0 }}</strong>
                    </div>

                    <div class="rdm-day-mini-track">
                      <div class="rdm-day-mini-fill" :style="{ width: day.progress + '%' }"></div>
                    </div>

                    <div class="rdm-day-schedule">
                      <div
                        v-for="slot in day.timeSlots || []"
                        :key="slot.id"
                        class="rdm-time-slot"
                        :class="['slot-' + slot.category, { done: slot.done }]"
                      >
                        <div class="slot-time-col">
                          <span class="slot-time">{{ slot.time }}</span>
                          <span class="slot-cat-dot"></span>
                        </div>
                        <label class="slot-action-col">
                          <input type="checkbox" :checked="slot.done" @change="toggleRoadmapDailyAction(slot.id)" />
                          <span class="slot-check" :class="{ done: slot.done }">
                            <svg v-if="slot.done" width="8" height="8" viewBox="0 0 8 8">
                              <path d="M1.5 4l2 2 3-3" stroke="white" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" />
                            </svg>
                          </span>
                          <div class="slot-text-wrap">
                            <span class="slot-text">{{ slot.text }}</span>
                            <span v-if="slot.tip" class="slot-tip">{{ slot.tip }}</span>
                            <span v-if="slot.detail" class="slot-tip">{{ slot.detail }}</span>
                          </div>
                        </label>
                      </div>
                    </div>
                  </article>
                </div>

                <div class="schedule-legend">
                  <div v-for="cat in scheduleCategories" :key="cat.key" class="legend-item" :class="'legend-' + cat.key">
                    <span class="legend-dot"></span>
                    <span>{{ cat.label }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="roadmap-feedback-panel">
              <div class="rfp-status-row">
                <div class="rfp-status-indicator" :class="'rfi-' + selectedRoadmapWeek.statusKey">
                  <svg v-if="selectedRoadmapWeek.statusKey === 'completed'" width="18" height="18" viewBox="0 0 18 18">
                    <path d="M3 9l4 4 8-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                  <svg v-else-if="selectedRoadmapWeek.statusKey === 'in-progress'" width="18" height="18" viewBox="0 0 18 18">
                    <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="1.5" />
                    <path d="M9 5v4l2.5 2.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
                  </svg>
                  <svg v-else width="18" height="18" viewBox="0 0 18 18">
                    <circle cx="9" cy="9" r="7" stroke="currentColor" stroke-width="1.5" />
                    <path d="M9 6v4M9 12v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
                  </svg>
                </div>
                <div>
                  <div class="rfp-status-label">Weekly progress</div>
                  <div class="rfp-status-text">{{ selectedRoadmapWeek.status }}</div>
                </div>
              </div>

              <div class="rfp-progress-donut">
                <svg width="88" height="88" viewBox="0 0 88 88">
                  <circle cx="44" cy="44" r="36" stroke="rgba(0,0,0,0.06)" stroke-width="8" fill="none" />
                  <circle
                    cx="44" cy="44" r="36"
                    :stroke="selectedRoadmapWeek.statusKey === 'completed' ? '#16a34a' : selectedRoadmapWeek.statusKey === 'in-progress' ? '#d97706' : '#e2e8f0'"
                    stroke-width="8" fill="none" stroke-linecap="round"
                    :stroke-dasharray="`${(selectedRoadmapWeek.progress / 100) * 226} 226`"
                    transform="rotate(-90 44 44)"
                    style="transition: stroke-dasharray 0.6s ease"
                  />
                  <text x="44" y="49" text-anchor="middle" font-size="14" font-weight="700" fill="#0a0b0a">{{ selectedRoadmapWeek.progress }}%</text>
                </svg>
              </div>

              <div class="rfp-all-weeks">
                <div class="rfp-aw-head">All weeks at a glance</div>
                <div class="rfp-week-bars">
                  <div
                    v-for="week in fourWeekRoadmap"
                    :key="week.id"
                    class="rfp-wbar-col"
                    :class="{ current: week.id === activeRoadmapWeek }"
                  >
                    <div class="rfp-wbar-track">
                      <div class="rfp-wbar-fill" :class="'rfp-wfill-' + week.statusKey" :style="{ height: week.progress + '%' }"></div>
                    </div>
                    <div class="rfp-wbar-label">W{{ week.week }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

            <section class="food-ai-section">
        <div class="section-wrap">
          <div class="food-ai-card">
            <div>
              <div class="section-eyebrow">AI nutrition helper</div>
              <h2 class="section-h2">
                Check a food's<br />
                <em>health score.</em>
              </h2>
              <p class="section-desc">
                Enter a food item and the AI model will estimate a health score using its nutrition profile.
              </p>
            </div>

            <div class="food-ai-panel">
              <div class="food-ai-form">
                <input
                  v-model="foodInput"
                  type="text"
                  placeholder="Try banana, apple, rice, milk..."
                  class="food-ai-input"
                  @keyup.enter="submitFoodPrediction"
                />

                <button
                  type="button"
                  class="food-ai-btn"
                  :disabled="foodPredictionLoading"
                  @click="submitFoodPrediction"
                >
                  {{ foodPredictionLoading ? 'Checking...' : 'Check score' }}
                </button>
              </div>

              <p v-if="foodPredictionError" class="food-ai-error">
                {{ foodPredictionError }}
              </p>

              <div v-if="foodPredictionCandidates.length" class="food-ai-candidates">
                <button
                  v-for="candidate in foodPredictionCandidates"
                  :key="candidate"
                  type="button"
                  class="food-ai-candidate"
                  @click="chooseFoodCandidate(candidate)"
                >
                  {{ candidate }}
                </button>
              </div>

              <div v-if="foodPredictionResult" class="food-ai-result">
                <div class="food-ai-score">
                  {{ Math.round(foodPredictionResult.health_score) }}
                  <span>/100</span>
                </div>

                <div>
                  <h3>{{ foodPredictionResult.matched_food }}</h3>
                  <p>{{ foodPredictionResult.category }}</p>

                  <div class="food-ai-nutrition-grid">
                    <div>
                      <span>Calories</span>
                      <strong>{{ foodPredictionResult.nutrition.calories }}</strong>
                    </div>
                    <div>
                      <span>Protein</span>
                      <strong>{{ foodPredictionResult.nutrition.protein_g }}g</strong>
                    </div>
                    <div>
                      <span>Fat</span>
                      <strong>{{ foodPredictionResult.nutrition.fat_g }}g</strong>
                    </div>
                    <div>
                      <span>Carbs</span>
                      <strong>{{ foodPredictionResult.nutrition.carbs_g }}g</strong>
                    </div>
                    <div>
                      <span>Fiber</span>
                      <strong>{{ foodPredictionResult.nutrition.fiber_g }}g</strong>
                    </div>
                    <div>
                      <span>Sugar</span>
                      <strong>{{ foodPredictionResult.nutrition.sugar_g }}g</strong>
                    </div>
                  </div>

                  <button type="button" class="food-ai-clear" @click="clearPrediction">
                    Clear result
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-col">
          <RouterLink to="/" class="logo footer-logo">
            <div class="logo-icon footer-logo-icon">
              <svg viewBox="0 0 36 36" fill="none">
                <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2" />
                <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor" />
              </svg>
            </div>
            <span class="logo-text">HealthyKids</span>
          </RouterLink>
          <p class="footer-blurb">A Monash University SDG 3 project<br />Team TP25 · 2025</p>
        </div>
        <div class="footer-col">
          <div class="footer-col-head">Navigate</div>
          <RouterLink to="/">Home</RouterLink>
          <RouterLink to="/parent-entry">Parent access</RouterLink>
          <RouterLink to="/parent-quiz">Retake quiz</RouterLink>
          <RouterLink to="/young-person-dashboard">Kids dashboard</RouterLink>
        </div>
        <div class="footer-col">
          <div class="footer-col-head">Legal</div>
          <a href="#">Privacy policy</a>
          <a href="#">Terms of use</a>
          <a href="#">Contact us</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2025 HealthyKids · Monash University · Good Health &amp; Wellbeing (UN SDG 3) · All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>


<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'
import { useDynamicPlan } from '../composables/useDynamicPlan'
import { useFoodHealthPredictor } from '../composables/useFoodHealthPredictor'

const { state, savePlan } = useFamilyPlanStore()

const {
  loading: planLoading,
  error: planError,
  fetchPlan,
  getTodaySlots,
  buildRoadmapWeeks,
} = useDynamicPlan()

const TIME_ZONE = 'Australia/Melbourne'
const LOCALE = 'en-AU'
const DAY_LABEL_LENGTH = 3
const API_BASE_URL = import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL

const scheduleCategories = [
  { key: 'nutrition', label: 'Nutrition' },
  { key: 'movement', label: 'Movement' },
  { key: 'sleep', label: 'Sleep / Wind-down' },
  { key: 'routine', label: 'Routine' },
  { key: 'family', label: 'Family time' },
]

const isScrolled = ref(false)
const showCelebration = ref(false)
const activeRoadmapWeek = ref(1)

function getTodayName() {
  return new Date().toLocaleDateString(LOCALE, {
    weekday: 'long',
    timeZone: TIME_ZONE,
  })
}

function getShortDayName(dayName) {
  return dayName.slice(0, DAY_LABEL_LENGTH)
}

const childName = computed(() => state.childName || state.child_name || 'Your child')
const streakDays = computed(() => state.streakDays || state.streak_days || 0)

const timeOfDay = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'morning'
  if (hour < 17) return 'afternoon'
  return 'evening'
})

const todayName = computed(() => getTodayName())

const fourWeekRoadmap = computed(() =>
  buildRoadmapWeeks(state.roadmapProgress || {})
)

const isPlanReady = computed(() => fourWeekRoadmap.value.length > 0)

const emptyRoadmapWeek = {
  id: 1,
  week: 1,
  title: 'Loading plan',
  summary: '',
  detail: '',
  parentTip: '',
  actions: [],
  dailyPlan: [],
  dailyCompleted: 0,
  dailyTotal: 0,
  weeklyCompleted: 0,
  totalItems: 0,
  completed: 0,
  progress: 0,
  status: 'Not started',
  statusKey: 'not-started',
}

const selectedRoadmapWeek = computed(() =>
  fourWeekRoadmap.value.find(week => week.id === activeRoadmapWeek.value)
  || fourWeekRoadmap.value[0]
  || emptyRoadmapWeek
)

const currentWeek = computed(() => {
  const firstIncomplete = fourWeekRoadmap.value.find(week => week.progress < 100)
  return firstIncomplete?.week || fourWeekRoadmap.value[0]?.week || 1
})

const currentFirstRoadmapDailyPlan = computed(() => {
  const plan = selectedRoadmapWeek.value?.dailyPlan || []
  const todayIndex = plan.findIndex(day => day.day === todayName.value)

  if (todayIndex === -1) return plan

  return [
    plan[todayIndex],
    ...plan.slice(0, todayIndex),
    ...plan.slice(todayIndex + 1),
  ]
})

const todayFullSchedule = computed(() =>
  getTodaySlots(
    currentWeek.value,
    todayName.value,
    state.todaySchedule || {}
  )
)

const completedTodayCount = computed(() =>
  todayFullSchedule.value.filter(slot => slot.done).length
)

const todayProgress = computed(() =>
  todayFullSchedule.value.length
    ? Math.round((completedTodayCount.value / todayFullSchedule.value.length) * 100)
    : 0
)

const weeklyProgress = computed(() => {
  const week = fourWeekRoadmap.value.find(item => item.week === currentWeek.value)
  if (!week?.dailyPlan?.length) return []

  return week.dailyPlan.map((day) => ({
    label: day.day.slice(0, DAY_LABEL_LENGTH),
    fullLabel: day.day,
    value: day.progress,
    completed: day.completed,
    total: day.timeSlots.length,
    tasks: day.timeSlots,
  }))
})

const weeklyAverage = computed(() => {
  if (!weeklyProgress.value.length) return 0
  const total = weeklyProgress.value.reduce((sum, day) => sum + day.value, 0)
  return Math.round(total / weeklyProgress.value.length)
})

const totalRoadmapActions = computed(() =>
  fourWeekRoadmap.value.reduce((sum, week) => sum + week.totalItems, 0)
)

const completedRoadmapActions = computed(() =>
  fourWeekRoadmap.value.reduce((sum, week) => sum + week.completed, 0)
)

const roadmapCompletion = computed(() =>
  totalRoadmapActions.value
    ? Math.round((completedRoadmapActions.value / totalRoadmapActions.value) * 100)
    : 0
)

const roadmapRingStyle = computed(() => {
  const percentage = roadmapCompletion.value
  const color = percentage === 100 ? '#16a34a' : percentage > 0 ? '#d97706' : '#e2e8f0'

  return {
    background: `conic-gradient(${color} ${percentage}%, rgba(0,0,0,0.07) ${percentage}%)`,
  }
})

const confettiPieces = computed(() =>
  Array.from({ length: 16 }, (_, index) => ({
    id: index,
    style: {
      left: `${4 + index * 6}%`,
      animationDelay: `${index * 0.04}s`,
      transform: `rotate(${index * 22}deg)`,
    },
  }))
)

function toggleTodayScheduleSlot(slot) {
  const todaySlotId = typeof slot === 'string' ? slot : slot.id
  const sourceSlotId = typeof slot === 'string' ? slot.replace('today-schedule-', '') : slot.sourceSlotId
  const nextDone = !(state.todaySchedule || {})[todaySlotId]

  const updatedTodaySchedule = {
    ...(state.todaySchedule || {}),
    [todaySlotId]: nextDone,
  }

  const updatedRoadmapProgress = sourceSlotId
    ? {
        ...(state.roadmapProgress || {}),
        [sourceSlotId]: nextDone,
      }
    : state.roadmapProgress || {}

  saveAndPersist({
    ...state,
    todaySchedule: updatedTodaySchedule,
    roadmapProgress: updatedRoadmapProgress,
  })
}

function toggleRoadmapDailyAction(actionId) {
  const updated = {
    ...(state.roadmapProgress || {}),
    [actionId]: !state.roadmapProgress?.[actionId],
  }

  saveAndPersist({
    ...state,
    roadmapProgress: updated,
  })
}

function completeMission() {
  saveAndPersist({
    ...state,
    streakDays: (state.streakDays || 0) + 1,
  })

  showCelebration.value = true

  setTimeout(() => {
    showCelebration.value = false
  }, 2000)
}

function saveAndPersist(updatedState) {
  savePlan(updatedState)

  persistDashboardUpdate(updatedState).catch((error) => {
    console.error('Failed to sync dashboard update:', error)
  })
}

async function persistDashboardUpdate(updatedState) {
  const username = updatedState.username || state.username

  if (!username) throw new Error('Missing username')
  if (!API_BASE_URL) throw new Error('Missing VITE_PARENT_PROFILES_API_BASE_URL')

  const response = await fetch(
    `${API_BASE_URL}/parent-profiles/${encodeURIComponent(username)}`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dailyPlan: updatedState.dailyPlan ?? state.dailyPlan,
        roadmapProgress: updatedState.roadmapProgress ?? state.roadmapProgress ?? {},
        todaySchedule: updatedState.todaySchedule ?? state.todaySchedule ?? {},
        streakDays: updatedState.streakDays ?? state.streakDays ?? 0,
        nextAction: updatedState.nextAction ?? state.nextAction,
        mission: updatedState.mission ?? state.mission,
      }),
    }
  )

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(data.error || `Dashboard update failed: ${response.status}`)
  }

  return data
}

function onScroll() {
  isScrolled.value = window.scrollY > 40
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })

  if (state.username) {
    fetchPlan(state.username)
  } else {
    console.warn('No username found in state. Complete quiz or load profile first.')
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})

const foodInput = ref('')

const {
  loading: foodPredictionLoading,
  error: foodPredictionError,
  result: foodPredictionResult,
  candidates: foodPredictionCandidates,
  predictFood,
  clearPrediction,
} = useFoodHealthPredictor()

function submitFoodPrediction() {
  predictFood(foodInput.value)
}

function chooseFoodCandidate(candidate) {
  foodInput.value = candidate
  predictFood(candidate)
}
</script>

<style scoped>
:global(:root) {
  --c-black:#0a0b0a; --c-900:#111312; --c-800:#1c1f1d; --c-700:#2d3230;
  --c-500:#52605a; --c-400:#7a8880; --c-300:#a8b5ae; --c-100:#e8ece9;
  --c-50:#f4f5f2; --c-white:#ffffff;
  --c-green:#16a34a; --c-green-mid:#22c55e; --c-green-soft:#f0fdf4; --c-green-pale:#dcfce7;
  --c-amber-soft:#fffbeb;
  --border:rgba(10,11,10,0.08); --border-mid:rgba(10,11,10,0.14);
  --shadow-xs:0 1px 4px rgba(0,0,0,0.06); --shadow-sm:0 2px 12px rgba(0,0,0,0.07);
  --shadow-md:0 8px 28px rgba(0,0,0,0.09); --shadow-lg:0 20px 56px rgba(0,0,0,0.12);
  --f-display:'Fraunces',Georgia,serif;
  --f-body:'General Sans','Helvetica Neue',ui-sans-serif,sans-serif;
  --f-mono:'JetBrains Mono',monospace;
  --r-md:14px; --r-lg:20px; --r-xl:28px;
  --section-v:clamp(80px,9vw,120px);
  /* Schedule slot category colors */
  --slot-nutrition: #16a34a;
  --slot-nutrition-bg: #f0fdf4;
  --slot-nutrition-border: rgba(22,163,74,0.2);
  --slot-movement: #2563eb;
  --slot-movement-bg: #eff6ff;
  --slot-movement-border: rgba(37,99,235,0.18);
  --slot-sleep: #7c3aed;
  --slot-sleep-bg: #f5f3ff;
  --slot-sleep-border: rgba(124,58,237,0.18);
  --slot-routine: #d97706;
  --slot-routine-bg: #fffbeb;
  --slot-routine-border: rgba(217,119,6,0.2);
  --slot-family: #db2777;
  --slot-family-bg: #fdf2f8;
  --slot-family-border: rgba(219,39,119,0.18);
}

:global(*,*::before,*::after){box-sizing:border-box}
:global(body){margin:0;font-family:var(--f-body),system-ui;background:var(--c-white);color:var(--c-black);-webkit-font-smoothing:antialiased;overflow-x:hidden}

.dashboard-page{min-height:100vh;overflow-x:clip;position:relative}
.noise-overlay{position:fixed;inset:0;pointer-events:none;z-index:9999;opacity:.025;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");background-size:256px}

/* TYPOGRAPHY */
h1,h2,h3{margin:0;font-family:var(--f-display);font-weight:400;letter-spacing:-0.03em;line-height:1.02}
em{font-style:italic;color:var(--c-green)}
p{font-family:var(--f-body);font-size:clamp(.9rem,1vw,1rem);line-height:1.75;color:var(--c-500);margin:0 0 1em}
p:last-child{margin-bottom:0}

.section-eyebrow{display:inline-flex;align-items:center;gap:8px;height:26px;padding:0 11px;border-radius:999px;border:1px solid var(--border-mid);font-family:var(--f-body);font-size:.68rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--c-500);margin-bottom:18px}
.section-eyebrow.light{border-color:rgba(255,255,255,.25);color:rgba(255,255,255,.55)}
.section-wrap{max-width:1280px;margin:0 auto;padding:0 40px}
.section-h2{font-size:clamp(2rem,3.5vw,3.2rem);margin-bottom:14px}
.section-desc{max-width:32rem;font-size:clamp(.9rem,1vw,.98rem)}

/* HEADER */
.header{position:fixed;top:0;left:0;right:0;z-index:500;transition:background .3s,border-color .3s,box-shadow .3s}
.header.scrolled{background:rgba(255,255,255,.92);border-bottom:1px solid var(--border);backdrop-filter:blur(20px);box-shadow:var(--shadow-xs)}
.header-inner{display:flex;align-items:center;justify-content:space-between;max-width:1280px;margin:0 auto;padding:0 40px;height:76px}
.logo{display:flex;align-items:center;gap:9px;text-decoration:none;color:var(--c-black)}
.logo-icon{width:28px;height:28px;color:var(--c-black)}
.logo-text{font-family:var(--f-display);font-size:1.22rem;font-weight:400;letter-spacing:-.03em;color:var(--c-black)}
.nav{display:flex;align-items:center;gap:2px}
.nav-a{height:36px;padding:0 12px;display:flex;align-items:center;font-family:var(--f-body);font-size:.86rem;font-weight:500;color:var(--c-500);text-decoration:none;border-radius:8px;transition:color .18s,background .18s}
.nav-a:hover{color:var(--c-black);background:var(--c-50)}
.nav-cta{display:flex;align-items:center;gap:8px}
.nav-link{height:36px;padding:0 14px;display:flex;align-items:center;font-family:var(--f-body);font-size:.86rem;font-weight:500;color:var(--c-500);text-decoration:none;border-radius:8px;transition:all .18s}
.nav-link:hover{color:var(--c-black);background:var(--c-50)}
.nav-btn{height:38px;padding:0 16px;display:inline-flex;align-items:center;gap:7px;font-family:var(--f-body);font-size:.86rem;font-weight:600;color:var(--c-white);background:var(--c-black);text-decoration:none;border-radius:10px;border:1px solid var(--c-900);box-shadow:0 1px 3px rgba(0,0,0,.2),0 0 0 1px rgba(255,255,255,.06) inset;transition:all .2s}
.nav-btn:hover{background:var(--c-800);transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,.24)}

.dash-hero{position:relative;padding:120px 0 0;overflow:hidden;background:var(--c-white)}
.dash-hero-bg{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.hero-blob{position:absolute;border-radius:50%;filter:blur(90px)}
.hb-1{width:700px;height:700px;top:-200px;right:-100px;background:radial-gradient(circle,rgba(22,163,74,.08) 0%,transparent 70%)}
.hb-2{width:500px;height:500px;bottom:0;left:-100px;background:radial-gradient(circle,rgba(59,130,246,.05) 0%,transparent 70%)}
.hero-lines{position:absolute;inset:0;display:grid;grid-template-columns:repeat(8,1fr)}
.hero-lines span{border-right:1px solid rgba(10,11,10,.03)}
.dash-hero-inner{max-width:1280px;margin:0 auto;padding:0 40px 0;display:grid;grid-template-columns:1fr 420px;gap:60px;align-items:center;position:relative;z-index:2}
.eyebrow-row{margin-bottom:28px}
.live-badge{display:inline-flex;align-items:center;gap:8px;height:30px;padding:0 12px;border-radius:999px;background:var(--c-green-soft);border:1px solid rgba(22,163,74,.2);font-family:var(--f-body);font-size:.72rem;font-weight:600;color:var(--c-green)}
.live-dot{width:6px;height:6px;border-radius:50%;background:var(--c-green-mid);animation:live-pulse 2.4s ease-in-out infinite}
@keyframes live-pulse{0%,100%{box-shadow:0 0 0 0 rgba(34,197,94,.45)}50%{box-shadow:0 0 0 4px rgba(34,197,94,0)}}
.dash-h1{display:flex;flex-direction:column;margin-bottom:20px}
.dh-serif{font-family:var(--f-display);font-weight:300;font-size:clamp(2.4rem,5vw,5.6rem);color:var(--c-black);letter-spacing:-.04em;line-height:.96}
.dash-hero-desc{max-width:28rem;font-size:clamp(.94rem,1.05vw,1.02rem);color:var(--c-500);margin-bottom:36px}
.hero-kpi-row{display:flex;align-items:center;gap:0;padding:20px 24px;background:var(--c-white);border:1px solid var(--border);border-radius:16px;box-shadow:var(--shadow-sm)}
.hkpi{flex:1;text-align:center}
.hkpi-val{font-family:var(--f-display);font-size:1.8rem;font-weight:400;color:var(--c-black);letter-spacing:-.03em;line-height:1}
.hkpi-lbl{font-family:var(--f-body);font-size:.68rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--c-400);margin-top:4px}
.hkpi-div{width:1px;height:40px;background:var(--border);flex-shrink:0}

/* Mission card */
.mission-card{position:relative;overflow:hidden;padding:28px;border-radius:24px;background:linear-gradient(145deg,#f0fdf4,#dcfce7);border:1.5px solid rgba(22,163,74,.2);box-shadow:var(--shadow-md)}
.mission-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.mission-eyebrow{font-family:var(--f-body);font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--c-green)}
.streak-chip{display:inline-flex;align-items:center;gap:5px;height:26px;padding:0 10px;border-radius:999px;background:rgba(22,163,74,.12);border:1px solid rgba(22,163,74,.2);font-size:.72rem;font-weight:700;color:var(--c-green)}
.mission-title{font-family:var(--f-display);font-size:1.5rem;font-weight:500;color:var(--c-black);letter-spacing:-.02em;line-height:1.2;margin-bottom:10px}
.mission-desc{font-size:.86rem;color:var(--c-500);margin-bottom:18px}
.mission-progress-wrap{margin-bottom:20px}
.mp-labels{display:flex;justify-content:space-between;font-size:.74rem;font-weight:600;color:var(--c-500);margin-bottom:8px}
.mp-track{height:8px;border-radius:999px;background:rgba(22,163,74,.15);overflow:hidden}
.mp-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#4ade80,#16a34a);transition:width .5s ease}
.mission-btn{display:inline-flex;align-items:center;gap:8px;height:48px;padding:0 22px;border-radius:12px;border:none;background:var(--c-black);color:var(--c-white);font-family:var(--f-body);font-size:.9rem;font-weight:600;cursor:pointer;transition:all .2s;width:100%;justify-content:center}
.mission-btn:hover{background:var(--c-800);transform:translateY(-1px);box-shadow:0 6px 20px rgba(0,0,0,.2)}
.confetti-layer{position:absolute;inset:0;pointer-events:none;overflow:hidden}
.confetti-piece{position:absolute;top:-14px;width:10px;height:18px;border-radius:4px;background:linear-gradient(180deg,#86efac 0%,#facc15 100%);animation:confettiFall 1.4s ease forwards}
@keyframes confettiFall{0%{opacity:0;transform:translateY(0) rotate(0deg)}10%{opacity:1}100%{opacity:0;transform:translateY(260px) rotate(240deg)}}


.roadmap-section{padding:var(--section-v) 0;background:var(--c-50);border-top:1px solid var(--border)}
.section-head-row{display:grid;grid-template-columns:1fr auto;gap:48px;align-items:start;margin-bottom:48px}
.roadmap-score-block{display:flex;align-items:center;gap:20px;padding:24px 28px;background:var(--c-white);border:1px solid var(--border);border-radius:20px;box-shadow:var(--shadow-sm);flex-shrink:0}
.rsb-ring{width:90px;height:90px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 4px 16px rgba(0,0,0,.1)}
.rsb-ring-inner{width:62px;height:62px;border-radius:50%;background:var(--c-white);display:flex;flex-direction:column;align-items:center;justify-content:center}
.rsb-pct{font-family:var(--f-display);font-size:1.3rem;font-weight:400;color:var(--c-black);line-height:1}
.rsb-pct span{font-size:.7em}
.rsb-lbl{font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--c-400)}
.rsb-num{font-family:var(--f-display);font-size:2rem;font-weight:400;color:var(--c-black);letter-spacing:-.03em;line-height:1;margin-bottom:2px}
.rsb-num span{font-size:.55em;color:var(--c-400)}
.rsb-desc{font-size:.76rem;font-weight:500;color:var(--c-400);margin-bottom:10px}
.rsb-focus-chip{display:inline-flex;height:24px;padding:0 10px;border-radius:999px;background:var(--c-green-pale);color:var(--c-green);font-size:.68rem;font-weight:700;align-items:center;letter-spacing:.06em;text-transform:uppercase}
.roadmap-weeks{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:28px}
.rweek-card{text-align:left;padding:22px;border-radius:20px;background:var(--c-white);border:1.5px solid var(--border);box-shadow:var(--shadow-xs);cursor:pointer;transition:all .25s ease;display:flex;flex-direction:column;gap:0}
.rweek-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-md);border-color:var(--border-mid)}
.rweek-card.active{border-color:rgba(22,163,74,.35);box-shadow:0 0 0 3px rgba(22,163,74,.08),var(--shadow-md)}
.rweek-card.completed{border-color:rgba(22,163,74,.25);background:linear-gradient(145deg,#f0fdf4,var(--c-white))}
.rweek-card.in-progress{border-color:rgba(217,119,6,.25)}
.rweek-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.rweek-num{font-family:var(--f-mono);font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400)}
.rweek-status{height:22px;padding:0 9px;border-radius:999px;font-size:.64rem;font-weight:700;display:inline-flex;align-items:center}
.rs-not-started{background:var(--c-50);color:var(--c-400)}
.rs-in-progress{background:var(--c-amber-soft);color:#b45309}
.rs-completed{background:var(--c-green-pale);color:var(--c-green)}
.rweek-icon{font-size:1.6rem;margin-bottom:12px}
.rweek-title{font-family:var(--f-display);font-size:1.1rem;font-weight:500;color:var(--c-black);letter-spacing:-.02em;line-height:1.2;margin-bottom:8px}
.rweek-summary{font-size:.82rem;color:var(--c-500);line-height:1.55;margin-bottom:16px;flex:1}
.rweek-progress-wrap{display:flex;align-items:center;gap:10px;margin-bottom:6px}
.rweek-track{flex:1;height:6px;border-radius:999px;background:rgba(0,0,0,.07);overflow:hidden}
.rweek-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#4ade80,#16a34a);transition:width .4s ease}
.rweek-pct{font-family:var(--f-mono);font-size:.7rem;font-weight:700;color:var(--c-400);min-width:28px;text-align:right}
.rweek-done-count{font-size:.72rem;font-weight:600;color:var(--c-400)}
.roadmap-detail{display:grid;grid-template-columns:1.1fr .9fr;gap:20px}
.roadmap-detail-main{padding:32px;background:var(--c-white);border-radius:20px;border:1px solid var(--border);box-shadow:var(--shadow-sm)}
.rdm-header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:16px}
.rdm-eyebrow{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--c-400);margin-bottom:6px}
.rdm-title{font-family:var(--f-display);font-size:1.6rem;font-weight:500;color:var(--c-black);letter-spacing:-.02em;line-height:1.15}
.rdm-week-badge{display:inline-flex;height:32px;padding:0 14px;border-radius:999px;background:var(--c-50);border:1px solid var(--border-mid);font-size:.8rem;font-weight:700;color:var(--c-500);align-items:center;white-space:nowrap}
.rdm-header-actions{display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:flex-end}
.planner-edit-btn,.planner-save-btn,.planner-cancel-btn{height:34px;padding:0 13px;border-radius:999px;font-family:var(--f-body);font-size:.76rem;font-weight:700;cursor:pointer;transition:all .18s ease}
.planner-edit-btn{border:1px solid rgba(22,163,74,.25);background:var(--c-green-pale);color:var(--c-green)}
.planner-edit-btn:hover{background:var(--c-green);color:white;transform:translateY(-1px)}
.planner-edit-actions{display:flex;gap:8px;align-items:center}
.planner-cancel-btn{border:1px solid var(--border-mid);background:var(--c-white);color:var(--c-500)}
.planner-cancel-btn:hover{background:var(--c-50);color:var(--c-black)}
.planner-save-btn{border:1px solid var(--c-black);background:var(--c-black);color:white}
.planner-save-btn:hover{background:var(--c-800);transform:translateY(-1px)}
.rdm-detail{font-size:.9rem;color:var(--c-500);line-height:1.7;margin-bottom:24px}
.rdm-actions-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px}
.rdm-actions-head span{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400)}
.rdm-actions-count{background:var(--c-green-pale);color:var(--c-green);padding:3px 10px;border-radius:999px;font-size:.7rem}
.rdm-actions-list{display:flex;flex-direction:column;gap:10px}
.rdm-action{display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:14px;background:var(--c-50);border:1px solid var(--border);cursor:pointer;transition:all .18s}
.rdm-action:hover{background:var(--c-white);border-color:var(--border-mid);box-shadow:var(--shadow-xs)}
.rdm-action.done{opacity:.65}
.rdm-action input{position:absolute;opacity:0;pointer-events:none}
.rdm-check{width:22px;height:22px;border-radius:50%;border:1.5px solid var(--c-100);display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all .2s}
.rdm-check.done{background:var(--c-green);border-color:var(--c-green)}
.rdm-action-text{font-family:var(--f-body);font-size:.88rem;font-weight:500;color:var(--c-700)}
.rdm-action.done .rdm-action-text{text-decoration:line-through;color:var(--c-400)}

/* DAILY PLAN INSIDE ROADMAP */
.rdm-day-plan-block{margin-top:28px;padding-top:24px;border-top:1px solid var(--border)}
.rdm-day-plan-head{display:flex;justify-content:space-between;align-items:flex-start;gap:18px;margin-bottom:18px}
.rdm-day-plan-head span{display:block;font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:var(--c-green);margin-bottom:6px}
.rdm-day-plan-head p{font-size:.84rem;color:var(--c-500);line-height:1.6;margin:0}
.rdm-day-plan-head strong{flex-shrink:0;min-height:30px;padding:0 12px;display:inline-flex;align-items:center;border-radius:999px;background:var(--c-green-pale);color:var(--c-green);font-size:.78rem;font-weight:800}
.rdm-day-plan-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:10px}

/* Day card in roadmap */
.rdm-day-card{padding:14px;border-radius:16px;background:var(--c-50);border:1px solid var(--border);transition:.18s ease}
.rdm-day-card:hover{background:var(--c-white);box-shadow:var(--shadow-xs)}
.rdm-day-card.today{border-color:rgba(22,163,74,.35);background:linear-gradient(160deg,#f0fdf4,var(--c-white))}
.rdm-day-card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;margin-bottom:8px}
.rdm-day-name{display:block;font-family:var(--f-mono);font-size:.66rem;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400)}
.rdm-day-card-head small{display:inline-flex;margin-top:4px;padding:2px 6px;border-radius:999px;background:var(--c-green);color:white;font-size:.55rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em}
.rdm-day-card-head strong{font-size:.68rem;color:var(--c-400);font-weight:800}
.rdm-day-mini-track{height:5px;border-radius:999px;overflow:hidden;background:rgba(0,0,0,.07);margin-bottom:10px}
.rdm-day-mini-fill{height:100%;border-radius:inherit;background:linear-gradient(90deg,#4ade80,#16a34a);transition:width .3s ease}

/* TIME SLOTS in roadmap day cards */
.rdm-day-schedule{display:grid;gap:6px}
.rdm-time-slot{display:flex;gap:7px;align-items:flex-start;padding:7px 8px;border-radius:10px;border:1px solid transparent;transition:all .15s}
.rdm-time-slot.slot-nutrition{background:var(--slot-nutrition-bg);border-color:var(--slot-nutrition-border)}
.rdm-time-slot.slot-movement{background:var(--slot-movement-bg);border-color:var(--slot-movement-border)}
.rdm-time-slot.slot-sleep{background:var(--slot-sleep-bg);border-color:var(--slot-sleep-border)}
.rdm-time-slot.slot-routine{background:var(--slot-routine-bg);border-color:var(--slot-routine-border)}
.rdm-time-slot.slot-family{background:var(--slot-family-bg);border-color:var(--slot-family-border)}
.rdm-time-slot.done{opacity:.5}
.rdm-time-slot.editing{padding:10px;background:var(--c-white);border-color:rgba(22,163,74,.22);box-shadow:var(--shadow-xs)}
.slot-edit-form{width:100%;display:grid;gap:8px}
.slot-edit-row{display:grid;grid-template-columns:90px 1fr;gap:8px}
.slot-edit-time,.slot-edit-category,.slot-edit-text,.slot-edit-tip{width:100%;min-height:34px;border-radius:9px;border:1px solid var(--border-mid);background:var(--c-white);padding:0 10px;font-family:var(--f-body);font-size:.72rem;color:var(--c-700);outline:none}
.slot-edit-text,.slot-edit-tip{min-height:36px}
.slot-edit-time:focus,.slot-edit-category:focus,.slot-edit-text:focus,.slot-edit-tip:focus{border-color:var(--c-green);box-shadow:0 0 0 3px rgba(22,163,74,.1)}
.slot-time-col{display:flex;flex-direction:column;align-items:center;gap:3px;flex-shrink:0;padding-top:2px}
.slot-time{font-family:var(--f-mono);font-size:.56rem;font-weight:700;color:var(--c-400);white-space:nowrap}
.slot-cat-dot{width:5px;height:5px;border-radius:50%;background:currentColor;opacity:.4}
.slot-action-col{display:flex;align-items:flex-start;gap:5px;cursor:pointer;flex:1}
.slot-action-col input{position:absolute;opacity:0;pointer-events:none}
.slot-check{width:12px;height:12px;margin-top:2px;border-radius:50%;border:1.5px solid rgba(0,0,0,.15);flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:all .15s}
.slot-check.done{background:var(--c-green);border-color:var(--c-green)}
.slot-text-wrap{display:flex;flex-direction:column;gap:2px}
.slot-text{font-size:.68rem;line-height:1.4;color:var(--c-700);font-weight:500}
.rdm-time-slot.done .slot-text{text-decoration:line-through;color:var(--c-300)}
.slot-tip{font-size:.6rem;color:var(--c-400);line-height:1.3;font-style:italic}

/* Legacy day actions fallback */
.rdm-day-actions{display:grid;gap:7px}
.rdm-day-action{position:relative;display:flex;align-items:flex-start;gap:7px;cursor:pointer}
.rdm-day-action input{position:absolute;opacity:0;pointer-events:none}
.rdm-day-check{width:13px;height:13px;margin-top:3px;border-radius:50%;border:1.5px solid var(--c-100);flex-shrink:0}
.rdm-day-action.done .rdm-day-check{background:var(--c-green);border-color:var(--c-green)}
.rdm-day-action span:last-child{font-size:.72rem;line-height:1.4;color:var(--c-500)}
.rdm-day-action.done span:last-child{color:var(--c-300);text-decoration:line-through}

/* SCHEDULE LEGEND */
.schedule-legend{display:flex;flex-wrap:wrap;gap:12px;margin-top:16px;padding-top:14px;border-top:1px solid var(--border)}
.legend-item{display:flex;align-items:center;gap:6px;font-size:.7rem;font-weight:600;color:var(--c-500)}
.legend-nutrition .legend-dot{background:var(--slot-nutrition)}
.legend-movement .legend-dot{background:var(--slot-movement)}
.legend-sleep .legend-dot{background:var(--slot-sleep)}
.legend-routine .legend-dot{background:var(--slot-routine)}
.legend-family .legend-dot{background:var(--slot-family)}
.legend-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}

/* Feedback panel */
.roadmap-feedback-panel{padding:28px;background:var(--c-900);border-radius:20px;border:1px solid rgba(255,255,255,.06);display:flex;flex-direction:column;gap:20px}
.rfp-status-row{display:flex;align-items:center;gap:14px}
.rfp-status-indicator{width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.rfi-completed{background:rgba(74,222,128,.15);color:#4ade80}
.rfi-in-progress{background:rgba(251,191,36,.12);color:#fbbf24}
.rfi-not-started{background:rgba(255,255,255,.07);color:rgba(255,255,255,.4)}
.rfp-status-label{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.35);margin-bottom:3px}
.rfp-status-text{font-family:var(--f-body);font-size:.88rem;font-weight:600;color:rgba(255,255,255,.8)}
.rfp-progress-donut{display:flex;justify-content:center}
.rfp-fb-title{font-family:var(--f-display);font-size:1.1rem;font-weight:500;color:var(--c-white);margin-bottom:8px;letter-spacing:-.02em}
.rfp-fb-body{font-size:.84rem;color:rgba(255,255,255,.5);line-height:1.65;margin:0}

/* Quiz insights */
.rfp-quiz-insights{padding:16px 18px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08)}
.rfp-qi-head{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.3);margin-bottom:10px}
.rfp-qi-chips{display:flex;flex-wrap:wrap;gap:6px}
.rfp-qi-chip{height:22px;padding:0 9px;border-radius:999px;background:rgba(22,163,74,.18);border:1px solid rgba(22,163,74,.25);color:#4ade80;font-size:.68rem;font-weight:700;display:inline-flex;align-items:center}

.rfp-tip{padding:16px 18px;border-radius:14px;background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.18)}
.rfp-tip-head{display:flex;align-items:center;gap:6px;font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#4ade80;margin-bottom:8px}
.rfp-tip p{font-size:.82rem;color:rgba(255,255,255,.55);margin:0;line-height:1.65}
.rfp-all-weeks{border-top:1px solid rgba(255,255,255,.06);padding-top:18px}
.rfp-aw-head{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.35);margin-bottom:14px}
.rfp-week-bars{display:flex;gap:12px;align-items:flex-end;height:60px}
.rfp-wbar-col{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;justify-content:flex-end}
.rfp-wbar-col.current .rfp-wbar-track{box-shadow:0 0 0 2px rgba(255,255,255,.2)}
.rfp-wbar-track{width:100%;flex:1;background:rgba(255,255,255,.07);border-radius:6px 6px 0 0;overflow:hidden;display:flex;align-items:flex-end}
.rfp-wbar-fill{width:100%;border-radius:6px 6px 0 0;transition:height .5s ease}
.rfp-wfill-completed{background:#4ade80}
.rfp-wfill-in-progress{background:#fbbf24}
.rfp-wfill-not-started{background:rgba(255,255,255,.12)}
.rfp-wbar-label{font-family:var(--f-mono);font-size:.6rem;font-weight:700;color:rgba(255,255,255,.35)}

.today-section{padding:var(--section-v) 0;background:var(--c-white);border-top:1px solid var(--border)}
.today-score-block{text-align:center;padding:24px 32px;background:var(--c-50);border:1px solid var(--border);border-radius:20px;min-width:180px;flex-shrink:0}
.tsb-pct{font-family:var(--f-display);font-size:3rem;font-weight:300;color:var(--c-black);letter-spacing:-.04em;line-height:1}
.tsb-pct span{font-size:.4em;color:var(--c-400)}
.tsb-lbl{font-size:.72rem;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin:6px 0 14px}
.tsb-track{height:8px;border-radius:999px;background:rgba(0,0,0,.07);overflow:hidden}
.tsb-fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#4ade80,#16a34a);transition:width .5s ease}

/* TODAY FULL SCHEDULE CARD */
.today-schedule-card{background:var(--c-white);border:1px solid var(--border);border-radius:24px;box-shadow:var(--shadow-md);overflow:hidden;margin-top:32px;margin-bottom:24px}
.tsc-header{display:flex;justify-content:space-between;align-items:flex-start;padding:24px 28px 16px;background:var(--c-50);border-bottom:1px solid var(--border)}
.tsc-day{font-family:var(--f-display);font-size:1.6rem;font-weight:500;color:var(--c-black);letter-spacing:-.02em}
.tsc-sub{font-size:.76rem;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--c-400);margin-top:4px}
.tsc-pct-chip{height:32px;padding:0 14px;border-radius:999px;font-size:.86rem;font-weight:700;display:inline-flex;align-items:center}
.chip-green{background:var(--c-green-pale);color:var(--c-green)}
.chip-default{background:var(--c-50);border:1px solid var(--border-mid);color:var(--c-500)}
.tsc-progress-bar{height:5px;background:rgba(0,0,0,.06);overflow:hidden}
.tsc-pb-fill{height:100%;background:linear-gradient(90deg,#4ade80,#16a34a);transition:width .5s ease}

/* TIMELINE */
.tsc-timeline{padding:16px 24px 24px;display:grid;gap:0}
.tsc-slot{display:grid;grid-template-columns:56px 24px 1fr;gap:0 12px;align-items:stretch;min-height:72px;position:relative}
.tsc-slot:last-child .tsc-line{display:none}
.tsc-time-col{display:flex;align-items:flex-start;padding-top:16px;justify-content:flex-end}
.tsc-time{font-family:var(--f-mono);font-size:.68rem;font-weight:700;color:var(--c-400);white-space:nowrap}
.tsc-slot-line{display:flex;flex-direction:column;align-items:center;padding-top:16px}
.tsc-dot{width:12px;height:12px;border-radius:50%;border:2px solid var(--c-100);background:var(--c-white);flex-shrink:0;transition:all .2s;z-index:1}
.tsc-dot.done{background:var(--c-green);border-color:var(--c-green)}
.tsc-line{flex:1;width:2px;background:var(--border);margin-top:4px}

/* Slot category colors on dot */
.tsc-nutrition .tsc-dot{border-color:rgba(22,163,74,.4)}
.tsc-nutrition .tsc-dot.done{background:var(--slot-nutrition);border-color:var(--slot-nutrition)}
.tsc-movement .tsc-dot{border-color:rgba(37,99,235,.3)}
.tsc-movement .tsc-dot.done{background:var(--slot-movement);border-color:var(--slot-movement)}
.tsc-sleep .tsc-dot{border-color:rgba(124,58,237,.3)}
.tsc-sleep .tsc-dot.done{background:var(--slot-sleep);border-color:var(--slot-sleep)}
.tsc-routine .tsc-dot{border-color:rgba(217,119,6,.3)}
.tsc-routine .tsc-dot.done{background:var(--slot-routine);border-color:var(--slot-routine)}
.tsc-family .tsc-dot{border-color:rgba(219,39,119,.3)}
.tsc-family .tsc-dot.done{background:var(--slot-family);border-color:var(--slot-family)}

.tsc-content{display:flex;align-items:flex-start;padding:10px 0 14px;cursor:pointer}
.tsc-content input{position:absolute;opacity:0;pointer-events:none}
.tsc-card{flex:1;padding:12px 16px;border-radius:14px;background:var(--c-50);border:1px solid var(--border);transition:all .18s}
.tsc-card:hover{background:var(--c-white);box-shadow:var(--shadow-xs);border-color:var(--border-mid)}
.tsc-card.done{opacity:.55}
.tsc-card-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
.tsc-cat-badge{height:20px;padding:0 8px;border-radius:999px;font-size:.62rem;font-weight:700;display:inline-flex;align-items:center;letter-spacing:.06em;text-transform:uppercase}
.badge-nutrition{background:var(--slot-nutrition-bg);color:var(--slot-nutrition);border:1px solid var(--slot-nutrition-border)}
.badge-movement{background:var(--slot-movement-bg);color:var(--slot-movement);border:1px solid var(--slot-movement-border)}
.badge-sleep{background:var(--slot-sleep-bg);color:var(--slot-sleep);border:1px solid var(--slot-sleep-border)}
.badge-routine{background:var(--slot-routine-bg);color:var(--slot-routine);border:1px solid var(--slot-routine-border)}
.badge-family{background:var(--slot-family-bg);color:var(--slot-family);border:1px solid var(--slot-family-border)}
.tsc-check{width:20px;height:20px;border-radius:50%;border:1.5px solid var(--c-100);display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all .2s}
.tsc-check.done{background:var(--c-green);border-color:var(--c-green)}
.tsc-text{display:block;font-size:.9rem;font-weight:500;color:var(--c-700);line-height:1.4}
.tsc-card.done .tsc-text{text-decoration:line-through;color:var(--c-400)}
.tsc-detail{display:block;margin-top:5px;font-size:.78rem;color:var(--c-400);line-height:1.5;font-style:italic}
.tsc-empty{font-size:.9rem;color:var(--c-400);font-style:italic;padding:24px 0;text-align:center;margin:0}

/* Today context row */
.today-context-row{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.today-context-card{padding:24px;background:var(--c-900);border-radius:20px;border:1px solid rgba(255,255,255,.06)}
.tcc-eyebrow{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:rgba(255,255,255,.35);margin-bottom:8px}
.tcc-title{font-family:var(--f-display);font-size:1.15rem;font-weight:500;color:var(--c-white);letter-spacing:-.02em;margin-bottom:10px;line-height:1.2}
.tcc-body{font-size:.84rem;color:rgba(255,255,255,.5);line-height:1.65;margin-bottom:20px}
.tcc-facts{display:flex;flex-direction:column;gap:12px}
.tcc-fact{padding:12px 14px;border-radius:12px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.07)}
.tcc-fact-label{font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.3);margin-bottom:4px}
.tcc-fact-val{font-size:.82rem;font-weight:500;color:rgba(255,255,255,.65);line-height:1.4}
.today-week-card{padding:24px;background:var(--c-50);border-radius:20px;border:1px solid var(--border)}
.twc-eyebrow{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:var(--c-400);margin-bottom:8px}
.twc-title{font-family:var(--f-display);font-size:1.1rem;font-weight:500;color:var(--c-black);letter-spacing:-.02em;margin-bottom:10px;line-height:1.2}
.twc-body{font-size:.84rem;color:var(--c-500);line-height:1.65;margin-bottom:20px}
.tss-label{font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:6px}
.tss-val{font-family:var(--f-display);font-size:1.1rem;font-weight:400;color:var(--c-black);letter-spacing:-.01em}


.why-section{padding:var(--section-v) 0;background:var(--c-900);border-top:1px solid rgba(255,255,255,.04)}
.why-inner{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:center}
.why-h2{color:var(--c-white);margin-bottom:20px;font-size:clamp(2rem,3.8vw,3.6rem)}
.why-copy{color:rgba(255,255,255,.55);margin-bottom:32px;max-width:28rem}
.why-facts{display:flex;flex-direction:column;gap:14px}
.why-fact{padding:16px 18px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.07)}
.wf-label{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,.35);margin-bottom:5px}
.wf-val{font-size:.86rem;font-weight:500;color:rgba(255,255,255,.65);line-height:1.5}
.why-stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.wsg-card{padding:28px 24px;border-radius:18px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);transition:all .25s}
.wsg-card:hover{background:rgba(255,255,255,.07);transform:translateY(-3px)}
.wsg-n{font-family:var(--f-display);font-size:clamp(2.2rem,3.5vw,3.2rem);font-weight:300;color:var(--c-white);letter-spacing:-.04em;line-height:1;margin-bottom:10px}
.wsg-l{font-size:.82rem;color:rgba(255,255,255,.45);line-height:1.5}


.footer{background:var(--c-black);padding:56px 0 0}
.footer-inner{max-width:1280px;margin:0 auto;padding:0 40px 44px;display:grid;grid-template-columns:1.6fr 1fr 1fr;gap:48px;border-bottom:1px solid rgba(255,255,255,.07)}
.footer-col{display:flex;flex-direction:column;gap:10px}
.footer-col-head{font-family:var(--f-body);font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:rgba(255,255,255,.35);margin-bottom:4px}
.footer-col a{font-family:var(--f-body);font-size:.86rem;font-weight:500;color:rgba(255,255,255,.5);text-decoration:none;transition:color .18s}
.footer-col a:hover{color:rgba(255,255,255,.9)}
.footer-bottom{max-width:1280px;margin:0 auto;padding:18px 40px}
.footer-bottom p{font-size:.76rem;color:rgba(255,255,255,.2);margin:0}
.footer-logo{color:rgba(255,255,255,.88);margin-bottom:12px}
.footer-logo-icon{color:rgba(255,255,255,.8)}
.footer-blurb{font-size:.8rem;color:rgba(255,255,255,.3);line-height:1.6;margin:0}


@media(max-width:1100px){
  .roadmap-weeks{grid-template-columns:repeat(2,1fr)}
  .roadmap-detail{grid-template-columns:1fr}
  .section-head-row{grid-template-columns:1fr}
  .rdm-day-plan-grid{grid-template-columns:repeat(2,1fr)}
  .today-context-row{grid-template-columns:1fr}
  .why-inner{grid-template-columns:1fr}
  .footer-inner{grid-template-columns:1fr 1fr}
}
@media(max-width:900px){
  .dash-hero-inner{grid-template-columns:1fr}
  .tracker-grid{grid-template-columns:1fr}
  .chart-card{grid-template-columns:1fr}
  .why-stat-grid{grid-template-columns:1fr 1fr}
  .section-wrap,.header-inner,.dash-hero-inner{padding-left:24px;padding-right:24px}
  .tsc-slot{grid-template-columns:48px 20px 1fr}
}
@media(max-width:700px){
  .nav,.nav-link{display:none}
  .hero-kpi-row{flex-wrap:wrap}
  .hkpi{flex:0 0 50%}
  .hkpi-div{display:none}
  .roadmap-weeks{grid-template-columns:1fr}
  .rdm-day-plan-grid{grid-template-columns:1fr}
  .rdm-day-plan-head{flex-direction:column}
  .chart-bars-wrap{grid-template-columns:repeat(7,1fr);gap:5px}
  .cbar-track{height:100px}
  .why-stat-grid{grid-template-columns:1fr}
  .footer-inner{grid-template-columns:1fr}
  h2{font-size:clamp(1.9rem,7vw,2.6rem)}
  .tsc-slot{grid-template-columns:40px 18px 1fr;gap:0 8px}
  .tsc-time{font-size:.6rem}
}


.rdm-day-plan-grid {
  display: flex;
  gap: 14px;
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 12px;
  scroll-snap-type: x mandatory;
  align-items: stretch;
}

.rdm-day-plan-grid::-webkit-scrollbar {
  height: 8px;
}

.rdm-day-plan-grid::-webkit-scrollbar-track {
  background: rgba(0,0,0,.05);
  border-radius: 999px;
}

.rdm-day-plan-grid::-webkit-scrollbar-thumb {
  background: rgba(22,163,74,.35);
  border-radius: 999px;
}

.rdm-day-plan-grid::-webkit-scrollbar-thumb:hover {
  background: rgba(22,163,74,.55);
}

.rdm-day-card {
  min-width: 230px;
  max-width: 250px;
  flex: 0 0 230px;
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
}

.rdm-day-card.today {
  border: 2px solid rgba(22,163,74,.42);
  background: linear-gradient(160deg,#f0fdf4,#ffffff);
  box-shadow: 0 10px 28px rgba(22,163,74,.12);
}

.rdm-day-card.today .rdm-day-name {
  color: var(--c-green);
}

.rdm-day-schedule {
  flex: 1;
}

.roadmap-detail {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(320px, .65fr);
  gap: 24px;
  align-items: stretch;
}

.roadmap-detail-main,
.roadmap-feedback-panel {
  min-width: 0;
  height: 100%;
}

.roadmap-feedback-panel {
  align-self: stretch;
}

.slot-text {
  font-size: .76rem;
  line-height: 1.45;
  color: var(--c-700);
  font-weight: 600;
}

.slot-time {
  font-family: var(--f-mono);
  font-size: .62rem;
  font-weight: 700;
  color: var(--c-400);
  white-space: nowrap;
}

@media(max-width:1100px){
  .roadmap-detail{grid-template-columns:1fr}
  .rdm-day-card{min-width:240px;flex-basis:240px}
}

@media(max-width:700px){
  .rdm-day-card{min-width:82vw;flex-basis:82vw;max-width:82vw}
}

.food-ai-section {
  padding: 72px 0;
  background: var(--c-white);
  border-top: 1px solid var(--border);
}

.food-ai-card {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(360px, 1.1fr);
  gap: 32px;
  padding: 34px;
  border-radius: 28px;
  background: var(--c-50);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}

.food-ai-panel {
  padding: 24px;
  border-radius: 22px;
  background: var(--c-white);
  border: 1px solid var(--border);
}

.food-ai-form {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  margin-bottom: 14px;
}

.food-ai-input {
  width: 100%;
  height: 48px;
  padding: 0 16px;
  border-radius: 14px;
  border: 1px solid var(--border-mid);
  font-size: .92rem;
  outline: none;
}

.food-ai-btn {
  height: 48px;
  padding: 0 18px;
  border-radius: 14px;
  border: 1px solid var(--c-black);
  background: var(--c-black);
  color: var(--c-white);
  font-weight: 700;
  cursor: pointer;
}

.food-ai-btn:disabled {
  opacity: .6;
  cursor: not-allowed;
}

.food-ai-error {
  padding: 12px 14px;
  border-radius: 12px;
  background: #fff7ed;
  border: 1px solid rgba(217,119,6,.18);
  color: #b45309;
  font-size: .84rem;
  margin: 0 0 12px;
}

.food-ai-candidates {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 14px;
}

.food-ai-candidate {
  min-height: 32px;
  padding: 0 12px;
  border-radius: 999px;
  border: 1px solid rgba(22,163,74,.24);
  background: var(--c-green-soft);
  color: var(--c-green);
  font-size: .78rem;
  font-weight: 700;
  cursor: pointer;
}

.food-ai-result {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 22px;
  margin-top: 16px;
  padding: 18px;
  border-radius: 18px;
  background: linear-gradient(145deg, #f0fdf4, #ffffff);
  border: 1px solid rgba(22,163,74,.18);
}

.food-ai-score {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--c-green);
  color: white;
  font-family: var(--f-display);
  font-size: 2rem;
  line-height: 1;
}

.food-ai-score span {
  margin-top: 4px;
  font-family: var(--f-body);
  font-size: .76rem;
  font-weight: 700;
  opacity: .82;
}

.food-ai-result h3 {
  margin: 0 0 4px;
  font-family: var(--f-display);
  font-size: 1.3rem;
  font-weight: 500;
  color: var(--c-black);
}

.food-ai-result p {
  margin: 0 0 14px;
  font-size: .82rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: var(--c-400);
}

.food-ai-nutrition-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.food-ai-nutrition-grid div {
  padding: 10px 12px;
  border-radius: 12px;
  background: rgba(255,255,255,.72);
  border: 1px solid var(--border);
}

.food-ai-nutrition-grid span {
  display: block;
  margin-bottom: 4px;
  font-size: .62rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--c-400);
}

.food-ai-nutrition-grid strong {
  font-size: .88rem;
  color: var(--c-black);
}

.food-ai-clear {
  margin-top: 14px;
  min-height: 34px;
  padding: 0 12px;
  border-radius: 999px;
  border: 1px solid var(--border-mid);
  background: white;
  color: var(--c-500);
  font-size: .78rem;
  font-weight: 700;
  cursor: pointer;
}

@media(max-width: 900px) {
  .food-ai-card {
    grid-template-columns: 1fr;
    padding: 24px;
  }

  .food-ai-form {
    grid-template-columns: 1fr;
  }

  .food-ai-result {
    grid-template-columns: 1fr;
  }

  .food-ai-nutrition-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>