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
          <RouterLink to="/parent-nutrition-tools" class="nav-a">Nutrition tools</RouterLink>
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
                <div
                  class="tsb-fill"
                  :class="getProgressColorClass(todayProgress)"
                  :style="{ width: todayProgress + '%' }"
                ></div>
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
              <div
                class="tsc-pb-fill"
                :class="getProgressColorClass(todayProgress)"
                :style="{ width: todayProgress + '%' }"
              ></div>
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
                  <div
                    class="rweek-fill"
                    :class="getProgressColorClass(week.progress)"
                    :style="{ width: week.progress + '%' }"
                  ></div>
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
                      <div
                        class="rdm-day-mini-fill"
                        :class="getProgressColorClass(day.progress)"
                        :style="{ width: day.progress + '%' }"
                      ></div>
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
                    :stroke="getProgressStroke(selectedRoadmapWeek.progress)"
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

                <div class="rfp-week-list">
                  <button
                    v-for="week in fourWeekRoadmap"
                    :key="week.id"
                    type="button"
                    class="rfp-week-row"
                    :class="{ current: week.id === activeRoadmapWeek }"
                    @click="activeRoadmapWeek = week.id"
                  >
                    <div class="rfp-week-row-top">
                      <span class="rfp-week-name">Week {{ week.week }}</span>
                      <span class="rfp-week-percent" :class="getProgressColorClass(week.progress)">
                        {{ week.progress }}%
                      </span>
                    </div>

                    <div class="rfp-week-progress-track">
                      <div
                        class="rfp-week-progress-fill"
                        :class="getProgressColorClass(week.progress)"
                        :style="{ width: week.progress + '%' }"
                      ></div>
                    </div>

                    <div class="rfp-week-row-meta">
                      <span>{{ week.status }}</span>
                      <span>{{ week.completed }}/{{ week.totalItems }} actions</span>
                    </div>
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
          <p class="footer-blurb">A SDG 3 project<br />Team TP25 · 2025</p>
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
        <p>© 2025 HealthyKids · SYRBYX · Good Health &amp; Wellbeing (UN SDG 3) · All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>


<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'
import { useDynamicPlan } from '../composables/useDynamicPlan'


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

function getProgressColorClass(progress) {
  if (progress >= 80) return 'progress-green'
  if (progress >= 60) return 'progress-lime'
  if (progress >= 40) return 'progress-amber'
  if (progress >= 20) return 'progress-orange'
  return 'progress-red'
}

function getProgressStroke(progress) {
  if (progress >= 80) return '#16a34a'
  if (progress >= 60) return '#65a30d'
  if (progress >= 40) return '#d97706'
  if (progress >= 20) return '#ea580c'
  return '#dc2626'
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

const todayFullSchedule = computed(() => {
  const week = fourWeekRoadmap.value.find(item => item.week === currentWeek.value)
  const today = week?.dailyPlan?.find(day => day.day === todayName.value)

  return today?.timeSlots || []
})


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

function getCanonicalActionId(slotOrId) {
  if (typeof slotOrId === 'string') {
    return slotOrId.replace('today-schedule-', '')
  }

  return (
    slotOrId?.sourceSlotId ||
    slotOrId?.id?.replace('today-schedule-', '') ||
    slotOrId?.id
  )
}

function togglePlanAction(slotOrId) {
  const actionId = getCanonicalActionId(slotOrId)

  if (!actionId) return

  const nextDone = !(state.roadmapProgress || {})[actionId]

  const updatedRoadmapProgress = {
    ...(state.roadmapProgress || {}),
    [actionId]: nextDone,
  }

  saveAndPersist({
    ...state,
    roadmapProgress: updatedRoadmapProgress,

   
    todaySchedule: {
      ...(state.todaySchedule || {}),
      [`today-schedule-${actionId}`]: nextDone,
    },
  })
}

function toggleTodayScheduleSlot(slot) {
  togglePlanAction(slot)
}

function toggleRoadmapDailyAction(actionId) {
  togglePlanAction(actionId)
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
    fetchPlan(state.username).then(() => {
      activeRoadmapWeek.value = currentWeek.value
    })
  } else {
    console.warn('No username found in state. Complete quiz or load profile first.')
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})

</script>

<style scoped>
:global(:root) {
  --c-black: #0a0b0a;
  --c-900: #111312;
  --c-800: #1c1f1d;
  --c-700: #2d3230;
  --c-500: #52605a;
  --c-400: #7a8880;
  --c-300: #a8b5ae;
  --c-100: #e8ece9;
  --c-50: #f4f5f2;
  --c-white: #ffffff;

  --c-green: #16a34a;
  --c-green-mid: #22c55e;
  --c-green-soft: #f0fdf4;
  --c-green-pale: #dcfce7;
  --c-amber-soft: #fffbeb;

  --border: rgba(10,11,10,0.08);
  --border-mid: rgba(10,11,10,0.14);

  --shadow-xs: 0 1px 4px rgba(0,0,0,0.06);
  --shadow-sm: 0 2px 12px rgba(0,0,0,0.07);
  --shadow-md: 0 8px 28px rgba(0,0,0,0.09);
  --shadow-lg: 0 20px 56px rgba(0,0,0,0.12);

  --f-display: 'Fraunces', Georgia, serif;
  --f-body: 'General Sans', 'Helvetica Neue', ui-sans-serif, sans-serif;
  --f-mono: 'JetBrains Mono', monospace;

  --section-v: clamp(80px, 9vw, 120px);

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

:global(*, *::before, *::after) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  font-family: var(--f-body), system-ui;
  background: var(--c-white);
  color: var(--c-black);
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

.dashboard-page {
  min-height: 100vh;
  overflow-x: clip;
  position: relative;
}

.noise-overlay {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  opacity: .025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 256px;
}

/* Base typography */
h1,
h2,
h3 {
  margin: 0;
  font-family: var(--f-display);
  font-weight: 400;
  letter-spacing: -0.03em;
  line-height: 1.02;
}

em {
  font-style: italic;
  color: var(--c-green);
}

p {
  margin: 0 0 1em;
  font-family: var(--f-body);
  font-size: clamp(.9rem, 1vw, 1rem);
  line-height: 1.75;
  color: var(--c-500);
}

p:last-child {
  margin-bottom: 0;
}

.section-wrap {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px;
}

.section-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 26px;
  padding: 0 11px;
  margin-bottom: 18px;
  border-radius: 999px;
  border: 1px solid var(--border-mid);
  font-size: .68rem;
  font-weight: 600;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--c-500);
}

.section-h2 {
  margin-bottom: 14px;
  font-size: clamp(2rem, 3.5vw, 3.2rem);
}

.section-desc {
  max-width: 32rem;
  font-size: clamp(.9rem, 1vw, .98rem);
}

/* Header */
.header {
  position: fixed;
  inset: 0 0 auto;
  z-index: 500;
  transition: background .3s, border-color .3s, box-shadow .3s;
}

.header.scrolled {
  background: rgba(255,255,255,.92);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(20px);
  box-shadow: var(--shadow-xs);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1280px;
  height: 76px;
  margin: 0 auto;
  padding: 0 40px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 9px;
  text-decoration: none;
  color: var(--c-black);
}

.logo-icon {
  width: 28px;
  height: 28px;
  color: var(--c-black);
}

.logo-text {
  font-family: var(--f-display);
  font-size: 1.22rem;
  letter-spacing: -.03em;
  color: var(--c-black);
}

.nav,
.nav-cta {
  display: flex;
  align-items: center;
}

.nav {
  gap: 2px;
}

.nav-cta {
  gap: 8px;
}

.nav-a,
.nav-link {
  display: flex;
  align-items: center;
  height: 36px;
  padding: 0 12px;
  border-radius: 8px;
  font-size: .86rem;
  font-weight: 500;
  color: var(--c-500);
  text-decoration: none;
  transition: color .18s, background .18s;
}

.nav-link {
  padding: 0 14px;
}

.nav-a:hover,
.nav-link:hover {
  color: var(--c-black);
  background: var(--c-50);
}

.nav-btn {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  height: 38px;
  padding: 0 16px;
  border-radius: 10px;
  border: 1px solid var(--c-900);
  background: var(--c-black);
  color: var(--c-white);
  font-size: .86rem;
  font-weight: 600;
  text-decoration: none;
  box-shadow: 0 1px 3px rgba(0,0,0,.2), 0 0 0 1px rgba(255,255,255,.06) inset;
  transition: all .2s;
}

.nav-btn:hover {
  background: var(--c-800);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,.24);
}

/* Hero */
.dash-hero {
  position: relative;
  padding: 120px 0 0;
  overflow: hidden;
  background: var(--c-white);
}

.dash-hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.hero-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
}

.hb-1 {
  width: 700px;
  height: 700px;
  top: -200px;
  right: -100px;
  background: radial-gradient(circle, rgba(22,163,74,.08) 0%, transparent 70%);
}

.hb-2 {
  width: 500px;
  height: 500px;
  bottom: 0;
  left: -100px;
  background: radial-gradient(circle, rgba(59,130,246,.05) 0%, transparent 70%);
}

.hero-lines {
  position: absolute;
  inset: 0;
  display: grid;
  grid-template-columns: repeat(8, 1fr);
}

.hero-lines span {
  border-right: 1px solid rgba(10,11,10,.03);
}

.dash-hero-inner {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 60px;
  align-items: center;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px;
}

.eyebrow-row {
  margin-bottom: 28px;
}

.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  border: 1px solid rgba(22,163,74,.2);
  background: var(--c-green-soft);
  font-size: .72rem;
  font-weight: 600;
  color: var(--c-green);
}

.live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--c-green-mid);
  animation: live-pulse 2.4s ease-in-out infinite;
}

@keyframes live-pulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(34,197,94,.45);
  }

  50% {
    box-shadow: 0 0 0 4px rgba(34,197,94,0);
  }
}

.dash-h1 {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.dh-serif {
  font-family: var(--f-display);
  font-size: clamp(2.4rem, 5vw, 5.6rem);
  font-weight: 300;
  line-height: .96;
  letter-spacing: -.04em;
  color: var(--c-black);
}

.dash-hero-desc {
  max-width: 28rem;
  margin-bottom: 36px;
  font-size: clamp(.94rem, 1.05vw, 1.02rem);
  color: var(--c-500);
}

.hero-kpi-row {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: var(--c-white);
  box-shadow: var(--shadow-sm);
}

.hkpi {
  flex: 1;
  text-align: center;
}

.hkpi-val {
  font-family: var(--f-display);
  font-size: 1.8rem;
  line-height: 1;
  letter-spacing: -.03em;
  color: var(--c-black);
}

.hkpi-lbl {
  margin-top: 4px;
  font-size: .68rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: var(--c-400);
}

.hkpi-div {
  width: 1px;
  height: 40px;
  background: var(--border);
  flex-shrink: 0;
}

/* Mission card */
.mission-card {
  position: relative;
  overflow: hidden;
  padding: 28px;
  border-radius: 24px;
  border: 1.5px solid rgba(22,163,74,.2);
  background: linear-gradient(145deg, #f0fdf4, #dcfce7);
  box-shadow: var(--shadow-md);
}

.mission-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.mission-eyebrow {
  font-size: .68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .12em;
  color: var(--c-green);
}

.streak-chip {
  display: inline-flex;
  align-items: center;
  height: 26px;
  padding: 0 10px;
  border-radius: 999px;
  border: 1px solid rgba(22,163,74,.2);
  background: rgba(22,163,74,.12);
  font-size: .72rem;
  font-weight: 700;
  color: var(--c-green);
}

.mission-title {
  margin-bottom: 10px;
  font-size: 1.5rem;
  font-weight: 500;
  line-height: 1.2;
  letter-spacing: -.02em;
  color: var(--c-black);
}

.mission-desc {
  margin-bottom: 18px;
  font-size: .86rem;
  color: var(--c-500);
}

.mission-progress-wrap {
  margin-bottom: 20px;
}

.mp-labels {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: .74rem;
  font-weight: 600;
  color: var(--c-500);
}

.mp-track,
.tsb-track,
.tsc-progress-bar,
.rweek-track,
.rdm-day-mini-track,
.rfp-week-progress-track {
  overflow: hidden;
  border-radius: 999px;
  background: rgba(0,0,0,.07);
}

.mp-track {
  height: 8px;
  background: rgba(22,163,74,.15);
}

.mp-fill,
.tsb-fill,
.tsc-pb-fill,
.rweek-fill,
.rdm-day-mini-fill,
.rfp-week-progress-fill {
  height: 100%;
  border-radius: inherit;
  transition: width .45s ease, background .25s ease;
}

.mp-fill {
  background: linear-gradient(90deg, #4ade80, #16a34a);
}

.mission-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 48px;
  padding: 0 22px;
  border: none;
  border-radius: 12px;
  background: var(--c-black);
  color: var(--c-white);
  font-family: var(--f-body);
  font-size: .9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all .2s;
}

.mission-btn:hover {
  background: var(--c-800);
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(0,0,0,.2);
}

.confetti-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.confetti-piece {
  position: absolute;
  top: -14px;
  width: 10px;
  height: 18px;
  border-radius: 4px;
  background: linear-gradient(180deg, #86efac 0%, #facc15 100%);
  animation: confettiFall 1.4s ease forwards;
}

@keyframes confettiFall {
  0% {
    opacity: 0;
    transform: translateY(0) rotate(0deg);
  }

  10% {
    opacity: 1;
  }

  100% {
    opacity: 0;
    transform: translateY(260px) rotate(240deg);
  }
}

/* Today's plan */
.today-section {
  padding: var(--section-v) 0;
  background: var(--c-white);
  border-top: 1px solid var(--border);
}

.section-head-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 48px;
  align-items: start;
  margin-bottom: 48px;
}

.today-score-block {
  min-width: 180px;
  padding: 24px 32px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--c-50);
  text-align: center;
  flex-shrink: 0;
}

.tsb-pct {
  font-family: var(--f-display);
  font-size: 3rem;
  font-weight: 300;
  line-height: 1;
  letter-spacing: -.04em;
  color: var(--c-black);
}

.tsb-pct span {
  font-size: .4em;
  color: var(--c-400);
}

.tsb-lbl {
  margin: 6px 0 14px;
  font-size: .72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: var(--c-400);
}

.tsb-track {
  height: 8px;
}

.today-schedule-card {
  overflow: hidden;
  margin-top: 32px;
  margin-bottom: 24px;
  border-radius: 24px;
  border: 1px solid var(--border);
  background: var(--c-white);
  box-shadow: var(--shadow-md);
}

.tsc-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px 28px 16px;
  border-bottom: 1px solid var(--border);
  background: var(--c-50);
}

.tsc-day {
  font-family: var(--f-display);
  font-size: 1.6rem;
  font-weight: 500;
  letter-spacing: -.02em;
  color: var(--c-black);
}

.tsc-sub {
  margin-top: 4px;
  font-size: .76rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: var(--c-400);
}

.tsc-pct-chip {
  display: inline-flex;
  align-items: center;
  height: 32px;
  padding: 0 14px;
  border-radius: 999px;
  font-size: .86rem;
  font-weight: 700;
}

.chip-green {
  background: var(--c-green-pale);
  color: var(--c-green);
}

.chip-default {
  border: 1px solid var(--border-mid);
  background: var(--c-50);
  color: var(--c-500);
}

.tsc-progress-bar {
  height: 5px;
}

.tsc-timeline {
  display: grid;
  gap: 0;
  padding: 16px 24px 24px;
}

.tsc-slot {
  display: grid;
  grid-template-columns: 56px 24px 1fr;
  gap: 0 12px;
  align-items: stretch;
  min-height: 72px;
  position: relative;
}

.tsc-slot:last-child .tsc-line {
  display: none;
}

.tsc-time-col {
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  padding-top: 16px;
}

.tsc-time {
  font-family: var(--f-mono);
  font-size: .68rem;
  font-weight: 700;
  color: var(--c-400);
  white-space: nowrap;
}

.tsc-slot-line {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 16px;
}

.tsc-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid var(--c-100);
  background: var(--c-white);
  z-index: 1;
  transition: all .2s;
}

.tsc-dot.done {
  background: var(--c-green);
  border-color: var(--c-green);
}

.tsc-line {
  flex: 1;
  width: 2px;
  margin-top: 4px;
  background: var(--border);
}

.tsc-nutrition .tsc-dot {
  border-color: rgba(22,163,74,.4);
}

.tsc-nutrition .tsc-dot.done {
  background: var(--slot-nutrition);
  border-color: var(--slot-nutrition);
}

.tsc-movement .tsc-dot {
  border-color: rgba(37,99,235,.3);
}

.tsc-movement .tsc-dot.done {
  background: var(--slot-movement);
  border-color: var(--slot-movement);
}

.tsc-sleep .tsc-dot {
  border-color: rgba(124,58,237,.3);
}

.tsc-sleep .tsc-dot.done {
  background: var(--slot-sleep);
  border-color: var(--slot-sleep);
}

.tsc-routine .tsc-dot {
  border-color: rgba(217,119,6,.3);
}

.tsc-routine .tsc-dot.done {
  background: var(--slot-routine);
  border-color: var(--slot-routine);
}

.tsc-family .tsc-dot {
  border-color: rgba(219,39,119,.3);
}

.tsc-family .tsc-dot.done {
  background: var(--slot-family);
  border-color: var(--slot-family);
}

.tsc-content {
  display: flex;
  align-items: flex-start;
  padding: 10px 0 14px;
  cursor: pointer;
}

.tsc-content input,
.slot-action-col input,
.rdm-action input,
.rdm-day-action input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.tsc-card {
  flex: 1;
  padding: 12px 16px;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: var(--c-50);
  transition: all .18s;
}

.tsc-card:hover {
  background: var(--c-white);
  box-shadow: var(--shadow-xs);
  border-color: var(--border-mid);
}

.tsc-card.done {
  opacity: .55;
}

.tsc-card-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.tsc-cat-badge {
  display: inline-flex;
  align-items: center;
  height: 20px;
  padding: 0 8px;
  border-radius: 999px;
  font-size: .62rem;
  font-weight: 700;
  letter-spacing: .06em;
  text-transform: uppercase;
}

.badge-nutrition {
  background: var(--slot-nutrition-bg);
  color: var(--slot-nutrition);
  border: 1px solid var(--slot-nutrition-border);
}

.badge-movement {
  background: var(--slot-movement-bg);
  color: var(--slot-movement);
  border: 1px solid var(--slot-movement-border);
}

.badge-sleep {
  background: var(--slot-sleep-bg);
  color: var(--slot-sleep);
  border: 1px solid var(--slot-sleep-border);
}

.badge-routine {
  background: var(--slot-routine-bg);
  color: var(--slot-routine);
  border: 1px solid var(--slot-routine-border);
}

.badge-family {
  background: var(--slot-family-bg);
  color: var(--slot-family);
  border: 1px solid var(--slot-family-border);
}

.tsc-check {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1.5px solid var(--c-100);
  flex-shrink: 0;
  transition: all .2s;
}

.tsc-check.done {
  background: var(--c-green);
  border-color: var(--c-green);
}

.tsc-text {
  display: block;
  font-size: .9rem;
  font-weight: 500;
  line-height: 1.4;
  color: var(--c-700);
}

.tsc-card.done .tsc-text {
  text-decoration: line-through;
  color: var(--c-400);
}

.tsc-detail {
  display: block;
  margin-top: 5px;
  font-size: .78rem;
  line-height: 1.5;
  font-style: italic;
  color: var(--c-400);
}

.tsc-empty {
  padding: 24px 0;
  margin: 0;
  text-align: center;
  font-size: .9rem;
  font-style: italic;
  color: var(--c-400);
}

/* Roadmap */
.roadmap-section {
  padding: var(--section-v) 0;
  background: var(--c-50);
  border-top: 1px solid var(--border);
}

.roadmap-score-block {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px 28px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: var(--c-white);
  box-shadow: var(--shadow-sm);
  flex-shrink: 0;
}

.rsb-ring {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 90px;
  height: 90px;
  border-radius: 50%;
  box-shadow: 0 4px 16px rgba(0,0,0,.1);
  flex-shrink: 0;
}

.rsb-ring-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 62px;
  height: 62px;
  border-radius: 50%;
  background: var(--c-white);
}

.rsb-pct {
  font-family: var(--f-display);
  font-size: 1.3rem;
  line-height: 1;
  color: var(--c-black);
}

.rsb-pct span {
  font-size: .7em;
}

.rsb-lbl {
  font-size: .6rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .08em;
  color: var(--c-400);
}

.rsb-num {
  margin-bottom: 2px;
  font-family: var(--f-display);
  font-size: 2rem;
  line-height: 1;
  letter-spacing: -.03em;
  color: var(--c-black);
}

.rsb-num span {
  font-size: .55em;
  color: var(--c-400);
}

.rsb-desc {
  margin-bottom: 10px;
  font-size: .76rem;
  font-weight: 500;
  color: var(--c-400);
}

.rsb-focus-chip {
  display: inline-flex;
  align-items: center;
  height: 24px;
  padding: 0 10px;
  border-radius: 999px;
  background: var(--c-green-pale);
  color: var(--c-green);
  font-size: .68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .06em;
}

.roadmap-weeks {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}

.rweek-card {
  display: flex;
  flex-direction: column;
  padding: 22px;
  border-radius: 20px;
  border: 1.5px solid var(--border);
  background: var(--c-white);
  box-shadow: var(--shadow-xs);
  cursor: pointer;
  text-align: left;
  transition: all .25s ease;
}

.rweek-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--border-mid);
}

.rweek-card.active {
  border-color: rgba(22,163,74,.35);
  box-shadow: 0 0 0 3px rgba(22,163,74,.08), var(--shadow-md);
}

.rweek-card.completed {
  border-color: rgba(22,163,74,.25);
  background: linear-gradient(145deg, #f0fdf4, var(--c-white));
}

.rweek-card.in-progress {
  border-color: rgba(217,119,6,.25);
}

.rweek-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.rweek-num {
  font-family: var(--f-mono);
  font-size: .62rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: var(--c-400);
}

.rweek-status {
  display: inline-flex;
  align-items: center;
  height: 22px;
  padding: 0 9px;
  border-radius: 999px;
  font-size: .64rem;
  font-weight: 700;
}

.rs-not-started {
  background: var(--c-50);
  color: var(--c-400);
}

.rs-in-progress {
  background: var(--c-amber-soft);
  color: #b45309;
}

.rs-completed {
  background: var(--c-green-pale);
  color: var(--c-green);
}

.rweek-title {
  margin-bottom: 8px;
  font-family: var(--f-display);
  font-size: 1.1rem;
  font-weight: 500;
  line-height: 1.2;
  letter-spacing: -.02em;
  color: var(--c-black);
}

.rweek-summary {
  flex: 1;
  margin-bottom: 16px;
  font-size: .82rem;
  line-height: 1.55;
  color: var(--c-500);
}

.rweek-progress-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.rweek-track {
  flex: 1;
  height: 6px;
}

.rweek-pct {
  min-width: 28px;
  text-align: right;
  font-family: var(--f-mono);
  font-size: .7rem;
  font-weight: 700;
  color: var(--c-400);
}

.rweek-done-count {
  font-size: .72rem;
  font-weight: 600;
  color: var(--c-400);
}

/* Roadmap detail: bigger planner, smaller progress panel */
.roadmap-detail {
  display: grid;
  grid-template-columns: minmax(0, 1.75fr) minmax(280px, .5fr);
  gap: 28px;
  align-items: stretch;
}

.roadmap-detail-main {
  min-width: 0;
  min-height: 680px;
  padding: 40px;
  border-radius: 24px;
  border: 1px solid var(--border);
  background: var(--c-white);
  box-shadow: var(--shadow-sm);
}

.rdm-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  padding-bottom: 22px;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--border);
}

.rdm-eyebrow {
  margin-bottom: 6px;
  font-size: .66rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .12em;
  color: var(--c-400);
}

.rdm-title {
  font-family: var(--f-display);
  font-size: clamp(1.8rem, 2.4vw, 2.4rem);
  font-weight: 500;
  line-height: 1.15;
  letter-spacing: -.02em;
  color: var(--c-black);
}

.rdm-week-badge {
  display: inline-flex;
  align-items: center;
  height: 32px;
  padding: 0 14px;
  border-radius: 999px;
  border: 1px solid var(--border-mid);
  background: var(--c-50);
  font-size: .8rem;
  font-weight: 700;
  color: var(--c-500);
  white-space: nowrap;
}

.rdm-day-plan-block {
  margin-top: 0;
  padding-top: 0;
  border-top: none;
}

.rdm-day-plan-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 18px;
  margin-bottom: 18px;
}

.rdm-day-plan-head span {
  display: block;
  margin-bottom: 6px;
  font-size: .72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: var(--c-green);
}

.rdm-day-plan-head p {
  margin: 0;
  font-size: .84rem;
  line-height: 1.6;
  color: var(--c-500);
}

.rdm-day-plan-head strong {
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  background: var(--c-green-pale);
  color: var(--c-green);
  font-size: .78rem;
  font-weight: 800;
  flex-shrink: 0;
}

.rdm-day-plan-grid {
  display: flex;
  gap: 18px;
  min-height: 560px;
  padding: 4px 4px 18px;
  overflow-x: auto;
  overflow-y: hidden;
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
  display: flex;
  flex-direction: column;
  flex: 0 0 300px;
  min-width: 300px;
  max-width: 330px;
  padding: 18px;
  border-radius: 18px;
  border: 1px solid var(--border);
  background: var(--c-50);
  scroll-snap-align: start;
  transition: .18s ease;
}

.rdm-day-card:hover {
  background: var(--c-white);
  box-shadow: var(--shadow-sm);
}

.rdm-day-card.today {
  border: 2px solid rgba(22,163,74,.42);
  background: linear-gradient(160deg, #f0fdf4, #ffffff);
  box-shadow: 0 12px 30px rgba(22,163,74,.13);
}

.rdm-day-card-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 8px;
}

.rdm-day-name {
  display: block;
  font-family: var(--f-mono);
  font-size: .66rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: var(--c-400);
}

.rdm-day-card.today .rdm-day-name {
  color: var(--c-green);
}

.rdm-day-card-head small {
  display: inline-flex;
  margin-top: 4px;
  padding: 2px 6px;
  border-radius: 999px;
  background: var(--c-green);
  color: white;
  font-size: .55rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .06em;
}

.rdm-day-card-head strong {
  font-size: .68rem;
  font-weight: 800;
  color: var(--c-400);
}

.rdm-day-mini-track {
  height: 5px;
  margin-bottom: 10px;
}

.rdm-day-schedule {
  display: grid;
  gap: 8px;
  flex: 1;
}

.rdm-time-slot {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  padding: 12px;
  border-radius: 14px;
  border: 1px solid transparent;
  transition: all .15s;
}

.rdm-time-slot.slot-nutrition {
  background: var(--slot-nutrition-bg);
  border-color: var(--slot-nutrition-border);
}

.rdm-time-slot.slot-movement {
  background: var(--slot-movement-bg);
  border-color: var(--slot-movement-border);
}

.rdm-time-slot.slot-sleep {
  background: var(--slot-sleep-bg);
  border-color: var(--slot-sleep-border);
}

.rdm-time-slot.slot-routine {
  background: var(--slot-routine-bg);
  border-color: var(--slot-routine-border);
}

.rdm-time-slot.slot-family {
  background: var(--slot-family-bg);
  border-color: var(--slot-family-border);
}

.rdm-time-slot.done {
  opacity: .5;
}

.slot-time-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  padding-top: 2px;
  flex-shrink: 0;
}

.slot-time {
  font-family: var(--f-mono);
  font-size: .62rem;
  font-weight: 700;
  color: var(--c-400);
  white-space: nowrap;
}

.slot-cat-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
  opacity: .4;
}

.slot-action-col {
  display: flex;
  align-items: flex-start;
  gap: 7px;
  cursor: pointer;
  flex: 1;
}

.slot-check {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 13px;
  height: 13px;
  margin-top: 3px;
  border-radius: 50%;
  border: 1.5px solid rgba(0,0,0,.15);
  flex-shrink: 0;
  transition: all .15s;
}

.slot-check.done {
  background: var(--c-green);
  border-color: var(--c-green);
}

.slot-text-wrap {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.slot-text {
  font-size: .86rem;
  line-height: 1.45;
  font-weight: 700;
  color: var(--c-700);
}

.rdm-time-slot.done .slot-text {
  text-decoration: line-through;
  color: var(--c-300);
}

.slot-tip {
  font-size: .72rem;
  line-height: 1.45;
  font-style: italic;
  color: var(--c-400);
}

.schedule-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 16px;
  padding-top: 14px;
  border-top: 1px solid var(--border);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: .7rem;
  font-weight: 600;
  color: var(--c-500);
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-nutrition .legend-dot {
  background: var(--slot-nutrition);
}

.legend-movement .legend-dot {
  background: var(--slot-movement);
}

.legend-sleep .legend-dot {
  background: var(--slot-sleep);
}

.legend-routine .legend-dot {
  background: var(--slot-routine);
}

.legend-family .legend-dot {
  background: var(--slot-family);
}

/* Right roadmap feedback panel */
.roadmap-feedback-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0;
  height: 100%;
  padding: 28px;
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,.06);
  background: var(--c-900);
}

.rfp-status-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.rfp-status-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  flex-shrink: 0;
}

.rfi-completed {
  background: rgba(74,222,128,.15);
  color: #4ade80;
}

.rfi-in-progress {
  background: rgba(251,191,36,.12);
  color: #fbbf24;
}

.rfi-not-started {
  background: rgba(255,255,255,.07);
  color: rgba(255,255,255,.4);
}

.rfp-status-label {
  margin-bottom: 3px;
  font-size: .66rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: rgba(255,255,255,.35);
}

.rfp-status-text {
  font-size: .88rem;
  font-weight: 600;
  color: rgba(255,255,255,.8);
}

.rfp-progress-donut {
  display: flex;
  justify-content: center;
}

.rfp-all-weeks {
  padding-top: 18px;
  border-top: 1px solid rgba(255,255,255,.06);
}

.rfp-aw-head {
  margin-bottom: 14px;
  font-size: .66rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: rgba(255,255,255,.35);
}

.rfp-week-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rfp-week-row {
  width: 100%;
  padding: 12px 14px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,.08);
  background: rgba(255,255,255,.04);
  cursor: pointer;
  text-align: left;
  transition: all .2s ease;
}

.rfp-week-row:hover {
  background: rgba(255,255,255,.07);
  border-color: rgba(255,255,255,.14);
  transform: translateY(-1px);
}

.rfp-week-row.current {
  background: rgba(255,255,255,.08);
  border-color: rgba(255,255,255,.22);
  box-shadow: 0 0 0 2px rgba(255,255,255,.08);
}

.rfp-week-row-top,
.rfp-week-row-meta {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.rfp-week-row-top {
  align-items: center;
  margin-bottom: 8px;
}

.rfp-week-name {
  font-size: .8rem;
  font-weight: 700;
  color: rgba(255,255,255,.78);
}

.rfp-week-percent {
  font-family: var(--f-mono);
  font-size: .75rem;
  font-weight: 800;
  background: transparent !important;
}

.rfp-week-progress-track {
  width: 100%;
  height: 8px;
  background: rgba(255,255,255,.08);
}

.rfp-week-row-meta {
  margin-top: 7px;
  font-size: .66rem;
  font-weight: 600;
  color: rgba(255,255,255,.38);
}

/* Progress colours */
.progress-green {
  background: #16a34a;
  color: #4ade80;
}

.progress-lime {
  background: #65a30d;
  color: #bef264;
}

.progress-amber {
  background: #d97706;
  color: #fbbf24;
}

.progress-orange {
  background: #ea580c;
  color: #fb923c;
}

.progress-red {
  background: #dc2626;
  color: #f87171;
}

/* Footer */
.footer {
  padding: 56px 0 0;
  background: var(--c-black);
}

.footer-inner {
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr;
  gap: 48px;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 40px 44px;
  border-bottom: 1px solid rgba(255,255,255,.07);
}

.footer-col {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-col-head {
  margin-bottom: 4px;
  font-size: .72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .12em;
  color: rgba(255,255,255,.35);
}

.footer-col a {
  font-size: .86rem;
  font-weight: 500;
  color: rgba(255,255,255,.5);
  text-decoration: none;
  transition: color .18s;
}

.footer-col a:hover {
  color: rgba(255,255,255,.9);
}

.footer-bottom {
  max-width: 1280px;
  margin: 0 auto;
  padding: 18px 40px;
}

.footer-bottom p {
  margin: 0;
  font-size: .76rem;
  color: rgba(255,255,255,.2);
}

.footer-logo {
  margin-bottom: 12px;
  color: rgba(255,255,255,.88);
}

.footer-logo-icon {
  color: rgba(255,255,255,.8);
}

.footer-blurb {
  margin: 0;
  font-size: .8rem;
  line-height: 1.6;
  color: rgba(255,255,255,.3);
}

/* Responsive */
@media (max-width: 1100px) {
  .roadmap-weeks {
    grid-template-columns: repeat(2, 1fr);
  }

  .roadmap-detail,
  .section-head-row {
    grid-template-columns: 1fr;
  }

  .rdm-day-card {
    min-width: 260px;
    flex-basis: 260px;
  }

  .footer-inner {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 900px) {
  .dash-hero-inner {
    grid-template-columns: 1fr;
  }

  .section-wrap,
  .header-inner,
  .dash-hero-inner {
    padding-left: 24px;
    padding-right: 24px;
  }

  .tsc-slot {
    grid-template-columns: 48px 20px 1fr;
  }
}

@media (max-width: 700px) {
  .nav,
  .nav-link {
    display: none;
  }

  .hero-kpi-row {
    flex-wrap: wrap;
  }

  .hkpi {
    flex: 0 0 50%;
  }

  .hkpi-div {
    display: none;
  }

  .roadmap-weeks {
    grid-template-columns: 1fr;
  }

  .rdm-day-card {
    min-width: 82vw;
    max-width: 82vw;
    flex-basis: 82vw;
  }

  .rdm-day-plan-head {
    flex-direction: column;
  }

  .footer-inner {
    grid-template-columns: 1fr;
  }

  h2 {
    font-size: clamp(1.9rem, 7vw, 2.6rem);
  }

  .tsc-slot {
    grid-template-columns: 40px 18px 1fr;
    gap: 0 8px;
  }

  .tsc-time {
    font-size: .6rem;
  }
}
</style>