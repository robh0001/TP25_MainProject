<template>
  <div class="dashboard-page">
    <div class="page-bg" aria-hidden="true">
      <div class="bg-blob bg-blob-1"></div>
      <div class="bg-blob bg-blob-2"></div>
      <div class="bg-blob bg-blob-3"></div>
      <div class="grain"></div>
    </div>

    <!-- HEADER -->
    <header class="header" :class="{ scrolled: isScrolled }">
      <div class="header-inner">
        <RouterLink to="/" class="logo">
          <div class="logo-icon">
            <svg viewBox="0 0 36 36" fill="none">
              <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.5" />
              <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor" />
            </svg>
          </div>
          <span>HealthyKids</span>
        </RouterLink>
        <nav class="nav">
          <RouterLink to="/" class="nav-a">Home</RouterLink>
          <!-- <RouterLink to="/parent-entry" class="nav-a">New Plan</RouterLink> -->
          <RouterLink to="/parent-nutrition-tools" class="nav-a">Nutrition</RouterLink>
          <RouterLink to="/young-person-dashboard" class="nav-a">Kids view</RouterLink>
        </nav>
        <div class="nav-cta">
          <RouterLink to="/parent-quiz" class="nav-link">Retake quiz</RouterLink>
          <RouterLink to="/parent-quiz" class="nav-btn">
            New plan
            <svg width="11" height="11" viewBox="0 0 12 12"><path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" /></svg>
          </RouterLink>
        </div>
      </div>
    </header>

    <!-- LOADING / ERROR STATES -->
    <div v-if="planLoading" class="state-screen">
      <div class="state-spinner"></div>
      <p>Loading your personalised family plan...</p>
    </div>
    <div v-else-if="planError" class="state-screen">
      <p class="state-error">Could not load your family plan: {{ planError }}</p>
      <button class="nav-btn" @click="fetchPlan(state.username)">Retry</button>
    </div>
    <div v-else-if="!isPlanReady" class="state-screen">
      <p>No family plan found yet.</p>
      <RouterLink to="/parent-quiz" class="nav-btn">Complete quiz</RouterLink>
    </div>

    <main v-else>
      <section class="hero">
        <div class="hero-inner">
          <div class="hero-left">
            <div class="live-badge">
              <span class="live-dot"></span>
              Parent dashboard · Week {{ currentWeek }}
            </div>

            <h1 class="hero-h1">
              Good {{ timeOfDay }},<br />
              <em>{{ childName }} family.</em>
            </h1>

            <p class="hero-sub">
              Your personalised 4-week plan is live. Track today's habits and explore your weekly roadmap below.
            </p>

            <div class="kpi-row">
              <div class="kpi">
                <div class="kpi-val">{{ streakDays }}</div>
                <div class="kpi-lbl">Day streak</div>
              </div>
              <div class="kpi-div"></div>
              <div class="kpi">
                <div class="kpi-val">{{ roadmapCompletion }}%</div>
                <div class="kpi-lbl">Roadmap done</div>
              </div>
              <div class="kpi-div"></div>
              <div class="kpi">
                <div class="kpi-val">{{ completedTodayCount }}/{{ todayFullSchedule.length }}</div>
                <div class="kpi-lbl">Today's tasks</div>
              </div>
              <div class="kpi-div"></div>
              <div class="kpi">
                <div class="kpi-val">{{ weeklyAverage }}%</div>
                <div class="kpi-lbl">Weekly avg.</div>
              </div>
            </div>
          </div>

          <!-- MISSION CARD -->
          <div class="mission-card" :class="{ celebrate: showCelebration }">
            <div v-if="showCelebration" class="confetti-layer" aria-hidden="true">
              <span v-for="p in confettiPieces" :key="p.id" class="confetti-piece" :style="p.style"></span>
            </div>
            <div class="mission-top">
              <div class="mission-eyebrow">Daily progress</div>
              <div class="streak-pill">{{ streakDays }}-day streak <span>&#128293;</span></div>
            </div>
            <h2 class="mission-title">{{ completedTodayCount }} of {{ todayFullSchedule.length }} done today</h2>
            <p class="mission-desc">Check off actions as your family completes them throughout the day.</p>
            <div class="mp-labels">
              <span>Today's progress</span>
              <span>{{ todayProgress }}%</span>
            </div>
            <div class="mp-track">
              <div class="mp-fill" :style="{ width: todayProgress + '%' }"></div>
            </div>
            <button class="mission-btn" @click="completeMission">
              <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><path d="M3 8l3.5 3.5L13 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" /></svg>
              Add to streak
            </button>
          </div>
        </div>
      </section>

      <section class="today-section">
        <div class="section-wrap">

          <div class="section-head-row">
            <div>
              <div class="section-eyebrow">Today's plan</div>
              <h2 class="section-h2">{{ todayName }}'s<br /><em>actions.</em></h2>
              <p class="section-desc">{{ completedTodayCount }} of {{ todayFullSchedule.length }} scheduled actions completed.</p>
            </div>
            <div class="today-score">
              <div class="tsb-pct">{{ todayProgress }}<span>%</span></div>
              <div class="tsb-lbl">Today's progress</div>
              <div class="tsb-track">
                <div class="tsb-fill" :style="{ width: todayProgress + '%' }"></div>
              </div>
            </div>
          </div>

          <!-- DAY CYCLE BAR -->
          <div class="day-cycle-card">
            <div class="dc-header">
              <span class="dc-title">Day at a glance</span>
              <span class="dc-sub">{{ completedTodayCount }} complete · {{ todayFullSchedule.length - completedTodayCount }} remaining</span>
            </div>
            <div class="dc-track-wrap">
              <div class="dc-track">
                <!-- Background time zones -->
                <div class="dc-zone dc-zone-dawn" style="left:0;width:18%">
                  <span class="dc-zone-label">Morning</span>
                </div>
                <div class="dc-zone dc-zone-day" style="left:18%;width:40%">
                  <span class="dc-zone-label">Afternoon</span>
                </div>
                <div class="dc-zone dc-zone-dusk" style="left:58%;width:27%">
                  <span class="dc-zone-label">Evening</span>
                </div>
                <div class="dc-zone dc-zone-night" style="left:85%;width:15%">
                  <span class="dc-zone-label">Night</span>
                </div>

                <!-- Progress fill -->
                <div class="dc-progress" :style="{ width: currentTimePercent + '%' }"></div>

                <!-- NOW indicator -->
                <div class="dc-now" :style="{ left: currentTimePercent + '%' }">
                  <div class="dc-now-line"></div>
                  <div class="dc-now-label">now</div>
                </div>

                <!-- Habit nodes -->
                <div
                  v-for="slot in todayFullSchedule"
                  :key="slot.id"
                  class="dc-node"
                  :class="['dc-node-' + slot.category, { done: slot.done, upcoming: isUpcoming(slot) }]"
                  :style="{ left: slotTimePercent(slot.time) + '%' }"
                  :title="slot.text"
                  @click="toggleTodayScheduleSlot(slot)"
                >
                  <div class="dc-node-icon">
                    <svg v-if="slot.done" width="9" height="9" viewBox="0 0 10 10"><path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
                    <span v-else class="dc-cat-initial">{{ catInitial(slot.category) }}</span>
                  </div>
                  <div class="dc-node-tooltip">
                    <div class="dc-tt-time">{{ slot.time }}</div>
                    <div class="dc-tt-text">{{ slot.text }}</div>
                  </div>
                </div>
              </div>

              <div class="dc-time-labels">
                <span>6 am</span><span>9 am</span><span>12 pm</span><span>3 pm</span><span>6 pm</span><span>9 pm</span>
              </div>
            </div>

            <!-- Legend -->
            <div class="dc-legend">
              <div v-for="cat in scheduleCategories" :key="cat.key" class="dc-legend-item" :class="'dcl-' + cat.key">
                <span class="dc-legend-dot"></span>{{ cat.label }}
              </div>
            </div>
          </div>

          <!-- TIMELINE -->
          <div class="timeline-card">
            <div class="tsc-header">
              <div class="tsc-day">{{ todayName }}</div>
              <div class="tsc-chip" :class="todayProgress === 100 ? 'chip-sage' : 'chip-default'">{{ todayProgress }}%</div>
            </div>
            <div class="tsc-prog-bar">
              <div class="tsc-prog-fill" :style="{ width: todayProgress + '%' }"></div>
            </div>
            <div class="tsc-timeline">
              <div
                v-for="slot in todayFullSchedule"
                :key="slot.id"
                class="tsc-slot"
                :class="['tsc-' + slot.category, { done: slot.done }]"
              >
                <div class="tsc-time-col"><span class="tsc-time">{{ slot.time }}</span></div>
                <div class="tsc-dot-col">
                  <div class="tsc-dot" :class="{ done: slot.done }"></div>
                  <div class="tsc-line"></div>
                </div>
                <label class="tsc-content">
                  <input type="checkbox" :checked="slot.done" @change="toggleTodayScheduleSlot(slot)" />
                  <div class="tsc-card" :class="{ done: slot.done }">
                    <div class="tsc-card-top">
                      <span class="tsc-badge" :class="'badge-' + slot.category">{{ slot.categoryLabel }}</span>
                      <div class="tsc-check" :class="{ done: slot.done }">
                        <svg v-if="slot.done" width="9" height="9" viewBox="0 0 10 10"><path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
                      </div>
                    </div>
                    <span class="tsc-text">{{ slot.text }}</span>
                    <span v-if="slot.detail || slot.tip" class="tsc-detail">{{ slot.detail || slot.tip }}</span>
                  </div>
                </label>
              </div>
              <p v-if="!todayFullSchedule.length" class="tsc-empty">No actions scheduled for {{ todayName }}.</p>
            </div>
          </div>

        </div>
      </section>

      <section class="roadmap-section roadmap-refresh" id="roadmap">
        <div class="section-wrap">
          <div class="planner-hero">
            <div>
              <div class="section-eyebrow">4-week planner</div>
              <h2 class="section-h2">A calmer view of<br /><em>the family plan.</em></h2>
              <p class="section-desc">
                Instead of showing every task at once, this planner shows one week and one day at a time.
                Parents can scan progress quickly, then open the day they need.
              </p>
            </div>

            <div class="planner-total-card">
              <div class="planner-ring" :style="roadmapRingStyle">
                <div>
                  <strong>{{ roadmapCompletion }}%</strong>
                  <span>complete</span>
                </div>
              </div>
              <div>
                <span class="planner-small-label">Overall progress</span>
                <strong class="planner-total-number">{{ completedRoadmapActions }}/{{ totalRoadmapActions }}</strong>
                <p>actions completed across the 4-week journey</p>
              </div>
            </div>
          </div>

          <div class="planner-shell">
            <aside class="planner-week-list" aria-label="Choose a roadmap week">
              <div class="planner-side-head">
                <span>Weeks</span>
                <strong>{{ currentWeek }}/4 active</strong>
              </div>

              <button
                v-for="week in fourWeekRoadmap"
                :key="week.id"
                type="button"
                class="planner-week-pill"
                :class="{ active: week.id === activeRoadmapWeek }"
                @click="activeRoadmapWeek = week.id"
              >
                <span class="week-dot">W{{ week.week }}</span>
                <span class="week-copy">
                  <strong>{{ week.title || week.focus || `Week ${week.week}` }}</strong>
                </span>
              </button>
            </aside>

            <article class="planner-main-card">
              <div class="planner-main-head">
                <div>
                  <span class="planner-kicker">Selected week</span>
                  <h3>Week {{ selectedRoadmapWeek.week }} · {{ selectedRoadmapWeek.title }}</h3>
                  <p>{{ selectedRoadmapWeek.summary || selectedRoadmapWeek.detail || selectedRoadmapWeek.parentTip || 'Focus on a small number of repeatable family actions this week.' }}</p>
                </div>

                <div class="planner-actions">
                  <button v-if="!isEditingPlanner" type="button" class="planner-edit-btn" @click="startEditingPlanner">
                    Edit planner
                  </button>

                  <template v-else>
                    <button type="button" class="planner-cancel-btn" @click="cancelEditingPlanner">Cancel</button>
                    <button type="button" class="planner-save-btn" @click="saveEditedPlanner">Save changes</button>
                  </template>
                </div>
              </div>

              <div class="planner-summary-grid">
                <div class="planner-summary-card">
                  <span>Week progress</span>
                  <strong>{{ selectedRoadmapWeek.progress }}%</strong>
                  <i><b :style="{ width: selectedRoadmapWeek.progress + '%' }"></b></i>
                </div>

                <div class="planner-summary-card">
                  <span>Completed</span>
                  <strong>{{ selectedRoadmapWeek.completed }}</strong>
                  <p>of {{ selectedRoadmapWeek.totalItems }} actions</p>
                </div>

                <div class="planner-summary-card">
                  <span>Remaining</span>
                  <strong>{{ selectedWeekOpenItems }}</strong>
                  <p>small steps left</p>
                </div>
              </div>

              <div class="day-picker">
                <button
                  v-for="day in currentFirstRoadmapDailyPlan"
                  :key="day.day"
                  type="button"
                  class="day-picker-btn"
                  :class="{ active: selectedPlannerDayData.day === day.day, today: activeRoadmapWeek === currentWeek && day.day === todayName }"
                  @click="selectedPlannerDay = day.day"
                >
                  <span>{{ getShortDayName(day.day) }}</span>
                  <strong>{{ day.progress }}%</strong>
                  <i><b :style="{ width: day.progress + '%' }"></b></i>
                </button>
              </div>

              <div class="selected-day-panel">
                <div class="selected-day-head">
                  <div>
                    <span class="planner-kicker">Daily view</span>
                    <h4>{{ selectedPlannerDayData.day || todayName }}</h4>
                    <p>
                      {{ selectedPlannerDayData.completed || 0 }} of
                      {{ selectedPlannerDayData.timeSlots?.length || 0 }} actions completed.
                    </p>
                  </div>
                  <strong class="selected-day-score">{{ selectedPlannerDayData.progress || 0 }}%</strong>
                </div>

                <div class="simple-slot-list">
                  <div
                    v-for="slot in selectedPlannerDayData.timeSlots || []"
                    :key="slot.id"
                    class="simple-slot"
                    :class="['slot-' + slot.category, { done: slot.done, editing: isEditingPlanner }]"
                  >
                    <template v-if="!isEditingPlanner">
                      <span class="slot-time">{{ slot.time }}</span>
                      <label class="slot-action">
                        <input type="checkbox" :checked="slot.done" @change="toggleRoadmapDailyAction(slot.id)" />
                        <span class="slot-check" :class="{ done: slot.done }">
                          <svg v-if="slot.done" width="8" height="8" viewBox="0 0 10 10">
                            <path d="M2 5l2.5 2.5L8 3" stroke="white" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none" />
                          </svg>
                        </span>
                        <span class="slot-copy">
                          <strong>{{ slot.text }}</strong>
                          <small v-if="slot.tip || slot.detail">{{ slot.tip || slot.detail }}</small>
                        </span>
                      </label>
                    </template>

                    <template v-else>
                      <div class="slot-edit-form">
                        <div class="slot-edit-row">
                          <input v-model="editablePlanner[slot.id].time" class="slot-edit-input" type="text" placeholder="Time" />
                          <select v-model="editablePlanner[slot.id].category" class="slot-edit-input">
                            <option value="nutrition">Nutrition</option>
                            <option value="movement">Movement</option>
                            <option value="sleep">Sleep</option>
                            <option value="routine">Routine</option>
                            <option value="family">Family</option>
                          </select>
                        </div>
                        <input v-model="editablePlanner[slot.id].text" class="slot-edit-input" type="text" placeholder="Habit action" />
                        <input v-model="editablePlanner[slot.id].tip" class="slot-edit-input" type="text" placeholder="Parent tip optional" />
                      </div>
                    </template>
                  </div>

                  <p v-if="!(selectedPlannerDayData.timeSlots || []).length" class="planner-empty">
                    No actions scheduled for this day.
                  </p>
                </div>
              </div>
            </article>

          </div>
        </div>
      </section>
    </main>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="footer-inner">
        <div class="footer-col">
          <RouterLink to="/" class="logo footer-logo">
            <div class="logo-icon footer-logo-icon">
              <svg viewBox="0 0 36 36" fill="none"><circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2"/><path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor"/></svg>
            </div>
            HealthyKids
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
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
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
const DAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
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
const selectedPlannerDay = ref(getTodayName())
const isEditingPlanner = ref(false)
const editablePlanner = ref({})


function getTodayName() {
  return new Date().toLocaleDateString(LOCALE, { weekday: 'long', timeZone: TIME_ZONE })
}

function getShortDayName(dayName) {
  return dayName.slice(0, DAY_LABEL_LENGTH)
}

/** Convert a time string like "7:00 am" or "14:30" to a percentage of 6am-9pm (15h window) */
function slotTimePercent(timeStr) {
  if (!timeStr) return 0
  const str = timeStr.toLowerCase().trim()
  let h = 0, m = 0
  const ampm = str.includes('am') || str.includes('pm')
  if (ampm) {
    const [timePart, period] = str.split(/\s*(am|pm)/i)
    const parts = timePart.trim().split(':')
    h = parseInt(parts[0]) || 0
    m = parseInt(parts[1]) || 0
    if (period === 'pm' && h !== 12) h += 12
    if (period === 'am' && h === 12) h = 0
  } else {
    const parts = str.split(':')
    h = parseInt(parts[0]) || 0
    m = parseInt(parts[1]) || 0
  }
  const totalMins = h * 60 + m
  const startMins = 6 * 60  // 6am
  const endMins = 21 * 60   // 9pm
  return Math.min(100, Math.max(0, ((totalMins - startMins) / (endMins - startMins)) * 100))
}

/** % of the current time through the day (6am-9pm) */
const currentTimePercent = computed(() => {
  const now = new Date()
  const totalMins = now.getHours() * 60 + now.getMinutes()
  const startMins = 6 * 60
  const endMins = 21 * 60
  return Math.min(100, Math.max(0, ((totalMins - startMins) / (endMins - startMins)) * 100))
})

function isUpcoming(slot) {
  return !slot.done && slotTimePercent(slot.time) >= currentTimePercent.value - 4
}

function catInitial(cat) {
  return { nutrition: 'N', movement: 'M', sleep: 'S', routine: 'R', family: 'F' }[cat] || '·'
}

function getProgressColorClass(progress) {
  if (progress >= 80) return 'progress-green'
  if (progress >= 60) return 'progress-lime'
  if (progress >= 40) return 'progress-amber'
  if (progress >= 20) return 'progress-orange'
  return 'progress-red'
}

function getProgressStroke(progress) {
  if (progress >= 80) return '#327c70'
  if (progress >= 40) return '#e6865f'
  if (progress >= 20) return '#d97706'
  return 'rgba(255,255,255,.25)'
}

function getCategoryLabel(category) {
  return { nutrition: 'Nutrition', movement: 'Movement', sleep: 'Wind-down', routine: 'Routine', family: 'Family' }[category] || 'Routine'
}


function applyPlannerOverridesToSlot(slot) {
  const overrides = state.plannerOverrides || {}
  const edited = overrides[slot.id]
  if (!edited) return slot
  const category = edited.category || slot.category
  return { ...slot, time: edited.time || slot.time, text: edited.text || slot.text, tip: edited.tip ?? slot.tip, category, categoryLabel: getCategoryLabel(category) }
}


const childName = computed(() => state.childName || state.child_name || 'Your child')
const streakDays = computed(() => state.streakDays || state.streak_days || 0)

const timeOfDay = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'morning'
  if (h < 17) return 'afternoon'
  return 'evening'
})

const todayName = computed(() => getTodayName())

const fourWeekRoadmap = computed(() =>
  buildRoadmapWeeks(state.roadmapProgress || {}).map(week => ({
    ...week,
    dailyPlan: (week.dailyPlan || []).map(day => {
      const timeSlots = (day.timeSlots || []).map(applyPlannerOverridesToSlot)
      const completed = timeSlots.filter(s => s.done).length
      const progress = timeSlots.length ? Math.round((completed / timeSlots.length) * 100) : 0
      return { ...day, timeSlots, completed, progress }
    }),
  }))
)

const isPlanReady = computed(() => fourWeekRoadmap.value.length > 0)

const emptyRoadmapWeek = {
  id: 1, week: 1, title: 'Loading...', summary: '', detail: '', parentTip: '',
  actions: [], dailyPlan: [], dailyCompleted: 0, dailyTotal: 0,
  weeklyCompleted: 0, totalItems: 0, completed: 0, progress: 0,
  status: 'Not started', statusKey: 'not-started',
}

const selectedRoadmapWeek = computed(() =>
  fourWeekRoadmap.value.find(w => w.id === activeRoadmapWeek.value)
  || fourWeekRoadmap.value[0]
  || emptyRoadmapWeek
)

const currentWeek = computed(() => {
  const first = fourWeekRoadmap.value.find(w => w.progress < 100)
  return first?.week || fourWeekRoadmap.value[0]?.week || 1
})

const currentFirstRoadmapDailyPlan = computed(() => {
  const plan = selectedRoadmapWeek.value?.dailyPlan || []

  return [...plan].sort((a, b) => {
    const aIndex = DAY_ORDER.indexOf(a.day)
    const bIndex = DAY_ORDER.indexOf(b.day)

    return (aIndex === -1 ? 99 : aIndex) - (bIndex === -1 ? 99 : bIndex)
  })
})

const selectedPlannerDayData = computed(() => {
  const plan = selectedRoadmapWeek.value?.dailyPlan || []
  const selectedDay = plan.find(day => day.day === selectedPlannerDay.value)
  const monday = plan.find(day => day.day === 'Monday')
  const today = activeRoadmapWeek.value === currentWeek.value
    ? plan.find(day => day.day === todayName.value)
    : null

  return selectedDay
    || today
    || monday
    || plan[0]
    || { day: activeRoadmapWeek.value === currentWeek.value ? todayName.value : 'Monday', timeSlots: [], completed: 0, progress: 0 }
})

const selectedWeekOpenItems = computed(() =>
  Math.max(0, (selectedRoadmapWeek.value?.totalItems || 0) - (selectedRoadmapWeek.value?.completed || 0))
)

const todayFullSchedule = computed(() => {
  const week = fourWeekRoadmap.value.find(w => w.week === currentWeek.value)
  const today = week?.dailyPlan?.find(d => d.day === todayName.value)
  return today?.timeSlots || []
})

const completedTodayCount = computed(() => todayFullSchedule.value.filter(s => s.done).length)
const todayProgress = computed(() => todayFullSchedule.value.length ? Math.round((completedTodayCount.value / todayFullSchedule.value.length) * 100) : 0)

const weeklyProgress = computed(() => {
  const week = fourWeekRoadmap.value.find(w => w.week === currentWeek.value)
  if (!week?.dailyPlan?.length) return []
  return week.dailyPlan.map(day => ({
    label: day.day.slice(0, DAY_LABEL_LENGTH),
    value: day.progress,
    completed: day.completed,
    total: day.timeSlots.length,
  }))
})

const weeklyAverage = computed(() => {
  if (!weeklyProgress.value.length) return 0
  return Math.round(weeklyProgress.value.reduce((s, d) => s + d.value, 0) / weeklyProgress.value.length)
})

const totalRoadmapActions = computed(() => fourWeekRoadmap.value.reduce((s, w) => s + w.totalItems, 0))
const completedRoadmapActions = computed(() => fourWeekRoadmap.value.reduce((s, w) => s + w.completed, 0))
const roadmapCompletion = computed(() => totalRoadmapActions.value ? Math.round((completedRoadmapActions.value / totalRoadmapActions.value) * 100) : 0)

const roadmapRingStyle = computed(() => {
  const p = roadmapCompletion.value
  const color = p === 100 ? '#327c70' : p > 0 ? '#e6865f' : 'rgba(22,48,43,.12)'
  return { background: `conic-gradient(${color} ${p}%, rgba(23,32,51,0.07) ${p}%)` }
})

// Journey path visualisation
const journeyPathColor = computed(() => {
  const p = roadmapCompletion.value
  return p > 0 ? '#e6865f' : 'rgba(22,48,43,0.08)'
})

const journeyFillDash = computed(() => {
  // SVG path total length ~520 for our curve
  const len = 520
  const filled = (roadmapCompletion.value / 100) * len
  return `${filled} ${len}`
})

const confettiPieces = computed(() =>
  Array.from({ length: 16 }, (_, i) => ({
    id: i,
    style: { left: `${4 + i * 6}%`, animationDelay: `${i * 0.04}s`, transform: `rotate(${i * 22}deg)` },
  }))
)

function getCanonicalActionId(slotOrId) {
  if (typeof slotOrId === 'string') return slotOrId.replace('today-schedule-', '')
  return slotOrId?.sourceSlotId || slotOrId?.id?.replace('today-schedule-', '') || slotOrId?.id
}

function togglePlanAction(slotOrId) {
  const actionId = getCanonicalActionId(slotOrId)
  if (!actionId) return
  const nextDone = !(state.roadmapProgress || {})[actionId]
  saveAndPersist({
    ...state,
    roadmapProgress: { ...(state.roadmapProgress || {}), [actionId]: nextDone },
    todaySchedule: { ...(state.todaySchedule || {}), [`today-schedule-${actionId}`]: nextDone },
  })
}

function toggleTodayScheduleSlot(slot) { togglePlanAction(slot) }
function toggleRoadmapDailyAction(actionId) { togglePlanAction(actionId) }

function completeMission() {
  saveAndPersist({ ...state, streakDays: (state.streakDays || 0) + 1 })
  showCelebration.value = true
  setTimeout(() => { showCelebration.value = false }, 2000)
}

function startEditingPlanner() {
  const editable = {}
  selectedRoadmapWeek.value.dailyPlan.forEach(day => {
    ;(day.timeSlots || []).forEach(slot => {
      editable[slot.id] = { time: slot.time, text: slot.text, tip: slot.tip || slot.detail || '', category: slot.category }
    })
  })
  editablePlanner.value = editable
  isEditingPlanner.value = true
}

function cancelEditingPlanner() { editablePlanner.value = {}; isEditingPlanner.value = false }

function saveEditedPlanner() {
  saveAndPersist({ ...state, plannerOverrides: { ...(state.plannerOverrides || {}), ...editablePlanner.value } })
  editablePlanner.value = {}
  isEditingPlanner.value = false
}

function saveAndPersist(updatedState) {
  savePlan(updatedState)
  persistDashboardUpdate(updatedState).catch(e => console.error('Sync failed:', e))
}

async function persistDashboardUpdate(updatedState) {
  const username = updatedState.username || state.username
  if (!username) throw new Error('Missing username')
  if (!API_BASE_URL) throw new Error('Missing VITE_PARENT_PROFILES_API_BASE_URL')
  const response = await fetch(`${API_BASE_URL}/parent-profiles/${encodeURIComponent(username)}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      dailyPlan: updatedState.dailyPlan ?? state.dailyPlan,
      roadmapProgress: updatedState.roadmapProgress ?? state.roadmapProgress ?? {},
      todaySchedule: updatedState.todaySchedule ?? state.todaySchedule ?? {},
      plannerOverrides: updatedState.plannerOverrides ?? state.plannerOverrides ?? {},
      streakDays: updatedState.streakDays ?? state.streakDays ?? 0,
      nextAction: updatedState.nextAction ?? state.nextAction,
      mission: updatedState.mission ?? state.mission,
    }),
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.error || `Update failed: ${response.status}`)
  return data
}

function onScroll() { isScrolled.value = window.scrollY > 40 }

watch(currentWeek, (nextWeek, previousWeek) => {
  if (
    activeRoadmapWeek.value === previousWeek ||
    !fourWeekRoadmap.value.some(week => week.id === activeRoadmapWeek.value)
  ) {
    activeRoadmapWeek.value = nextWeek
  }
}, { immediate: true })

watch(activeRoadmapWeek, (weekId) => {
  selectedPlannerDay.value = weekId === currentWeek.value ? todayName.value : 'Monday'
})

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  if (state.username) {
    fetchPlan(state.username).then(() => { activeRoadmapWeek.value = currentWeek.value
      selectedPlannerDay.value = todayName.value })
  }
})
onUnmounted(() => { window.removeEventListener('scroll', onScroll) })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;1,300;1,400&family=DM+Sans:wght@400;500;600;700;800;900&display=swap');

:root {
  --cream: #fffaf2;
  --cream2: #f8f1e7;
  --ink: #16302b;
  --muted: #65746f;
  --coral: #f59f7a;
  --coral-dark: #e6865f;
  --coral-soft: #fff1e9;
  --sage: #5fae9b;
  --sage-soft: #e8f6f2;
  --sage-dark: #327c70;
  --navy: #16302b;
  --border: rgba(22,48,43,.09);
  --border-mid: rgba(22,48,43,.15);
  --glass: rgba(255,248,239,.76);
  --glass-strong: rgba(255,250,242,.9);
  --shadow-sm: 0 4px 16px rgba(22,48,43,.07);
  --shadow-md: 0 12px 36px rgba(22,48,43,.10);
  --shadow-lg: 0 24px 60px rgba(22,48,43,.13);

  --slot-nutrition:  #7a9b76; --slot-nutrition-bg:  #eef6ea; --slot-nutrition-border: rgba(122,155,118,.22);
  --slot-movement:   #2563eb; --slot-movement-bg:   #eff6ff; --slot-movement-border:  rgba(37,99,235,.18);
  --slot-sleep:      #7c3aed; --slot-sleep-bg:      #f5f3ff; --slot-sleep-border:     rgba(124,58,237,.18);
  --slot-routine:    #d97706; --slot-routine-bg:    #fffbeb; --slot-routine-border:   rgba(217,119,6,.2);
  --slot-family:     #db2777; --slot-family-bg:     #fdf2f8; --slot-family-border:    rgba(219,39,119,.18);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.dashboard-page {
  font-family: 'DM Sans', system-ui, sans-serif;
  background: #f8f1e7;
  color: var(--ink);
  -webkit-font-smoothing: antialiased;
  min-height: 100vh;
  overflow-x: hidden;
}


.page-bg {
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
}
.bg-blob { position: absolute; border-radius: 50%; filter: blur(100px); }
.bg-blob-1 { width: 700px; height: 700px; top: -200px; right: -150px; background: radial-gradient(circle, rgba(95,174,155,.20) 0%, transparent 70%); }
.bg-blob-2 { width: 500px; height: 500px; bottom: 100px; left: -100px; background: radial-gradient(circle, rgba(245,159,122,.16) 0%, transparent 70%); }
.bg-blob-3 { width: 400px; height: 400px; top: 50%; left: 45%; background: radial-gradient(circle, rgba(255,248,239,.6) 0%, transparent 70%); }
.grain {
  position: fixed; inset: 0; opacity: .022; pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 180px;
}


.header {
  position: fixed; inset: 0 0 auto; z-index: 500;
  transition: background .3s, border-color .3s, box-shadow .3s;
}
.header.scrolled {
  background: rgba(255,248,239,.88);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(20px);
  box-shadow: var(--shadow-sm);
}
.header-inner {
  display: flex; align-items: center; justify-content: space-between;
  max-width: 1240px; height: 72px; margin: 0 auto; padding: 0 40px;
}
.logo { display: flex; align-items: center; gap: 9px; text-decoration: none; color: var(--ink); font-family: 'Fraunces', Georgia, serif; font-size: 1.2rem; letter-spacing: -.03em; }
.logo-icon { width: 28px; height: 28px; background: linear-gradient(145deg, rgba(255,114,95,.22), rgba(122,155,118,.22)), rgba(255,255,255,.74); border: 1px solid var(--border-mid); border-radius: 999px; display: grid; place-items: center; color: var(--sage); }
.nav { display: flex; align-items: center; gap: 2px; }
.nav-a { display: flex; align-items: center; height: 36px; padding: 0 13px; border-radius: 999px; font-size: .84rem; font-weight: 600; color: var(--muted); text-decoration: none; transition: all .18s; }
.nav-a:hover { color: var(--ink); background: rgba(23,32,51,.05); }
.nav-cta { display: flex; align-items: center; gap: 8px; }
.nav-link { height: 36px; padding: 0 14px; border-radius: 999px; font-size: .84rem; font-weight: 600; color: var(--muted); text-decoration: none; display: flex; align-items: center; transition: all .18s; }
.nav-link:hover { color: var(--ink); background: rgba(23,32,51,.05); }
.nav-btn { display: inline-flex; align-items: center; gap: 7px; height: 38px; padding: 0 16px; border-radius: 999px; border: none; background: var(--ink); color: #fff; font-family: 'DM Sans', sans-serif; font-size: .84rem; font-weight: 800; text-decoration: none; cursor: pointer; box-shadow: 0 4px 14px rgba(23,32,51,.22); transition: all .2s; }
.nav-btn:hover { background: #24304a; transform: translateY(-1px); box-shadow: 0 8px 22px rgba(23,32,51,.28); }


.state-screen { min-height: 80vh; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; padding: 40px; }
.state-spinner { width: 40px; height: 40px; border: 3px solid rgba(23,32,51,.1); border-top-color: var(--coral); border-radius: 50%; animation: spin .8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.state-error { color: #dc2626; font-weight: 600; }


.hero { padding: 108px 0 0; position: relative; z-index: 1; }
.hero-inner {
  display: grid; grid-template-columns: 1fr 320px; gap: 48px; align-items: center;
  max-width: 1240px; margin: 0 auto; padding: 40px 40px 48px;
  border-radius: 0 0 32px 32px;
  background: var(--glass-strong);
  border: 1px solid rgba(255,255,255,.7);
  border-top: none;
  box-shadow: var(--shadow-md);
  backdrop-filter: blur(14px);
}

.live-badge { display: inline-flex; align-items: center; gap: 8px; height: 28px; padding: 0 12px; border-radius: 999px; border: 1px solid rgba(122,155,118,.28); background: rgba(122,155,118,.12); font-size: .66rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; color: var(--sage-dark); margin-bottom: 20px; }
.live-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--sage); animation: livepulse 2.4s ease-in-out infinite; }
@keyframes livepulse { 0%,100%{box-shadow:0 0 0 0 rgba(122,155,118,.45)}50%{box-shadow:0 0 0 5px rgba(122,155,118,0)} }

.hero-h1 { font-family: 'Fraunces', Georgia, serif; font-size: clamp(2.6rem, 5vw, 4.4rem); font-weight: 300; letter-spacing: -.05em; line-height: .96; color: var(--ink); margin-bottom: 16px; }
.hero-h1 em { font-style: italic; color: var(--coral); }
.hero-sub { font-size: .94rem; color: var(--muted); line-height: 1.7; max-width: 30rem; margin-bottom: 28px; }

.kpi-row { display: flex; align-items: center; padding: 18px 22px; border-radius: 18px; border: 1px solid var(--border); background: rgba(255,255,255,.55); backdrop-filter: blur(8px); }
.kpi { flex: 1; text-align: center; }
.kpi-val { font-family: 'Fraunces', serif; font-size: 1.9rem; line-height: 1; letter-spacing: -.03em; color: var(--ink); }
.kpi-lbl { margin-top: 4px; font-size: .62rem; font-weight: 800; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); }
.kpi-div { width: 1px; height: 38px; background: var(--border); flex-shrink: 0; }


.mission-card {
  position: relative; overflow: hidden; padding: 26px; border-radius: 24px;
  background: linear-gradient(145deg, #fff8ef, #fff0ec);
  border: 1.5px solid rgba(255,114,95,.22);
  box-shadow: 0 12px 36px rgba(255,114,95,.14);
}
.mission-card::before { content: ''; position: absolute; top: -50px; right: -50px; width: 160px; height: 160px; border-radius: 50%; background: rgba(255,114,95,.06); }
.mission-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
.mission-eyebrow { font-size: .62rem; font-weight: 900; text-transform: uppercase; letter-spacing: .14em; color: var(--coral); }
.streak-pill { display: inline-flex; align-items: center; height: 24px; padding: 0 9px; border-radius: 999px; background: rgba(255,114,95,.12); border: 1px solid rgba(255,114,95,.22); font-size: .68rem; font-weight: 800; color: var(--coral-dark); }
.mission-title { font-family: 'Fraunces', serif; font-size: 1.5rem; font-weight: 400; letter-spacing: -.02em; line-height: 1.2; color: var(--ink); margin-bottom: 8px; }
.mission-desc { font-size: .82rem; color: var(--muted); line-height: 1.6; margin-bottom: 16px; }
.mp-labels { display: flex; justify-content: space-between; font-size: .72rem; font-weight: 700; color: var(--muted); margin-bottom: 7px; }
.mp-track { height: 8px; border-radius: 999px; background: rgba(255,114,95,.15); }
.mp-fill { height: 100%; border-radius: inherit; background: linear-gradient(90deg, #ffb19e, var(--coral)); transition: width .5s ease; }
.mission-btn { margin-top: 16px; width: 100%; height: 46px; border: none; border-radius: 13px; background: var(--ink); color: #fff; font-family: 'DM Sans', sans-serif; font-size: .88rem; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: all .2s; }
.mission-btn:hover { background: #24304a; transform: translateY(-1px); box-shadow: 0 8px 24px rgba(23,32,51,.24); }

.confetti-layer { position: absolute; inset: 0; pointer-events: none; overflow: hidden; }
.confetti-piece { position: absolute; top: -14px; width: 10px; height: 18px; border-radius: 4px; background: linear-gradient(180deg, #fed7aa 0%, var(--coral) 100%); animation: confetti-fall 1.4s ease forwards; }
@keyframes confetti-fall { 0%{opacity:0;transform:translateY(0) rotate(0deg)} 10%{opacity:1} 100%{opacity:0;transform:translateY(260px) rotate(240deg)} }


.section-wrap { max-width: 1240px; margin: 0 auto; padding: 0 40px; }
.section-eyebrow { display: inline-flex; align-items: center; height: 24px; padding: 0 10px; border-radius: 999px; border: 1px solid var(--border-mid); font-size: .62rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin-bottom: 14px; }
.section-h2 { font-family: 'Fraunces', serif; font-size: clamp(2rem, 3.5vw, 3rem); font-weight: 300; letter-spacing: -.04em; line-height: 1.04; margin-bottom: 10px; }
.section-h2 em { font-style: italic; color: var(--coral); }
.section-desc { font-size: .9rem; color: var(--muted); line-height: 1.7; max-width: 32rem; }
.section-head-row { display: grid; grid-template-columns: 1fr auto; gap: 48px; align-items: start; margin-bottom: 32px; }


.today-section { position: relative; z-index: 1; padding: clamp(60px, 8vw, 100px) 0; background: transparent; }

.today-score { min-width: 180px; padding: 22px 28px; border-radius: 20px; border: 1px solid var(--border); background: var(--glass); backdrop-filter: blur(10px); text-align: center; }
.tsb-pct { font-family: 'Fraunces', serif; font-size: 3rem; font-weight: 300; line-height: 1; letter-spacing: -.05em; color: var(--ink); }
.tsb-pct span { font-size: .4em; color: var(--muted); }
.tsb-lbl { margin: 6px 0 12px; font-size: .66rem; font-weight: 800; text-transform: uppercase; letter-spacing: .1em; color: var(--muted); }
.tsb-track { height: 7px; border-radius: 999px; background: rgba(23,32,51,.08); }
.tsb-fill { height: 100%; border-radius: inherit; background: linear-gradient(90deg, #ffb19e, var(--coral)); transition: width .5s; }


.day-cycle-card {
  margin-bottom: 24px; padding: 28px 32px;
  border-radius: 24px;
  background: var(--glass-strong);
  border: 1px solid rgba(255,255,255,.7);
  box-shadow: var(--shadow-md);
  backdrop-filter: blur(12px);
}
.dc-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 22px; }
.dc-title { font-size: .72rem; font-weight: 800; text-transform: uppercase; letter-spacing: .12em; color: var(--muted); }
.dc-sub { font-size: .76rem; font-weight: 600; color: var(--coral); }

.dc-track-wrap { position: relative; }
.dc-track {
  position: relative; height: 56px; border-radius: 14px; overflow: visible;
  display: flex; align-items: center;
}
.dc-zone {
  position: absolute; top: 0; bottom: 0; border-radius: 0; display: flex; align-items: flex-end; padding: 0 10px 6px;
}
.dc-zone:first-child { border-radius: 14px 0 0 14px; }
.dc-zone:last-child { border-radius: 0 14px 14px 0; }
.dc-zone-dawn  { background: linear-gradient(135deg, rgba(255,200,140,.22), rgba(255,220,170,.15)); }
.dc-zone-day   { background: linear-gradient(135deg, rgba(255,245,200,.2), rgba(255,230,160,.12)); }
.dc-zone-dusk  { background: linear-gradient(135deg, rgba(255,180,100,.15), rgba(220,130,80,.14)); }
.dc-zone-night { background: linear-gradient(135deg, rgba(80,100,160,.15), rgba(40,60,120,.18)); border-radius: 0 14px 14px 0; }
.dc-zone-label { font-size: .58rem; font-weight: 700; text-transform: uppercase; letter-spacing: .1em; color: rgba(23,32,51,.3); }

.dc-progress {
  position: absolute; top: 0; bottom: 0; left: 0; border-radius: 14px;
  background: rgba(255,114,95,.12);
  transition: width .8s ease;
  pointer-events: none;
}
.dc-now {
  position: absolute; top: -4px; bottom: -4px; transform: translateX(-50%);
  display: flex; flex-direction: column; align-items: center; z-index: 3;
  pointer-events: none;
}
.dc-now-line { width: 2px; flex: 1; background: var(--coral); border-radius: 1px; }
.dc-now-label { font-size: .6rem; font-weight: 800; color: var(--coral); margin-top: 3px; }

.dc-node {
  position: absolute; width: 36px; height: 36px; top: 50%; transform: translate(-50%, -50%);
  z-index: 2; cursor: pointer;
}
.dc-node-icon {
  width: 100%; height: 100%; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  border: 2px solid rgba(255,255,255,.8);
  box-shadow: 0 3px 10px rgba(23,32,51,.15);
  font-size: .7rem; font-weight: 800;
  transition: transform .2s, box-shadow .2s;
  background: rgba(255,255,255,.55);
  color: var(--muted);
}
.dc-node:hover .dc-node-icon { transform: scale(1.15); box-shadow: 0 6px 18px rgba(23,32,51,.22); }
.dc-node.done .dc-node-icon { background: var(--sage); color: white; border-color: var(--sage); }
.dc-node.upcoming .dc-node-icon { border-color: var(--coral); color: var(--coral); box-shadow: 0 0 0 3px rgba(255,114,95,.18), 0 3px 10px rgba(23,32,51,.15); }
.dc-node-nutrition.done .dc-node-icon  { background: var(--slot-nutrition); border-color: var(--slot-nutrition); }
.dc-node-movement.done .dc-node-icon   { background: var(--slot-movement); border-color: var(--slot-movement); }
.dc-node-sleep.done .dc-node-icon      { background: var(--slot-sleep); border-color: var(--slot-sleep); }
.dc-node-routine.done .dc-node-icon    { background: var(--slot-routine); border-color: var(--slot-routine); }
.dc-node-family.done .dc-node-icon     { background: var(--slot-family); border-color: var(--slot-family); }

.dc-node-tooltip {
  position: absolute; bottom: calc(100% + 8px); left: 50%; transform: translateX(-50%);
  background: var(--ink); color: #fff; border-radius: 10px; padding: 6px 10px;
  white-space: nowrap; pointer-events: none; opacity: 0;
  transition: opacity .15s; z-index: 10; min-width: 130px; text-align: center;
}
.dc-node:hover .dc-node-tooltip { opacity: 1; }
.dc-tt-time { font-size: .62rem; color: rgba(255,255,255,.5); margin-bottom: 2px; }
.dc-tt-text { font-size: .72rem; font-weight: 600; }

.dc-time-labels {
  display: flex; justify-content: space-between;
  padding: 7px 0 0; font-size: .64rem; font-weight: 600; color: rgba(23,32,51,.35);
}
.dc-legend { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--border); }
.dc-legend-item { display: flex; align-items: center; gap: 6px; font-size: .7rem; font-weight: 600; color: var(--muted); }
.dc-legend-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }
.dcl-nutrition .dc-legend-dot { background: var(--slot-nutrition); }
.dcl-movement .dc-legend-dot  { background: var(--slot-movement); }
.dcl-sleep .dc-legend-dot     { background: var(--slot-sleep); }
.dcl-routine .dc-legend-dot   { background: var(--slot-routine); }
.dcl-family .dc-legend-dot    { background: var(--slot-family); }


.timeline-card { border-radius: 24px; border: 1px solid rgba(255,255,255,.65); background: var(--glass); box-shadow: var(--shadow-md); overflow: hidden; backdrop-filter: blur(10px); }
.tsc-header { display: flex; justify-content: space-between; align-items: center; padding: 22px 26px 14px; border-bottom: 1px solid var(--border); background: rgba(255,255,255,.35); }
.tsc-day { font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 400; letter-spacing: -.02em; }
.tsc-chip { display: inline-flex; align-items: center; height: 30px; padding: 0 13px; border-radius: 999px; font-size: .82rem; font-weight: 800; }
.chip-sage { background: rgba(122,155,118,.15); color: var(--sage-dark); border: 1px solid rgba(122,155,118,.22); }
.chip-default { border: 1px solid var(--border-mid); background: rgba(255,255,255,.45); color: var(--muted); }
.tsc-prog-bar { height: 4px; background: rgba(23,32,51,.06); }
.tsc-prog-fill { height: 100%; background: linear-gradient(90deg, #ffb19e, var(--coral)); transition: width .5s; }
.tsc-timeline { padding: 14px 22px 22px; display: flex; flex-direction: column; }

.tsc-slot { display: grid; grid-template-columns: 56px 22px 1fr; gap: 0 10px; align-items: stretch; min-height: 68px; }
.tsc-slot:last-child .tsc-line { display: none; }
.tsc-time-col { display: flex; justify-content: flex-end; align-items: flex-start; padding-top: 14px; }
.tsc-time { font-family: 'DM Sans', sans-serif; font-size: .68rem; font-weight: 700; color: var(--muted); }
.tsc-dot-col { display: flex; flex-direction: column; align-items: center; padding-top: 14px; }
.tsc-dot { width: 11px; height: 11px; border-radius: 50%; border: 2px solid rgba(23,32,51,.15); background: #fff; transition: all .2s; }
.tsc-dot.done { background: var(--coral); border-color: var(--coral); }
.tsc-nutrition .tsc-dot { border-color: rgba(122,155,118,.4); } .tsc-nutrition .tsc-dot.done { background: var(--slot-nutrition); border-color: var(--slot-nutrition); }
.tsc-movement .tsc-dot  { border-color: rgba(37,99,235,.3); }   .tsc-movement .tsc-dot.done  { background: var(--slot-movement); border-color: var(--slot-movement); }
.tsc-sleep .tsc-dot     { border-color: rgba(124,58,237,.3); }  .tsc-sleep .tsc-dot.done     { background: var(--slot-sleep); border-color: var(--slot-sleep); }
.tsc-routine .tsc-dot   { border-color: rgba(217,119,6,.3); }   .tsc-routine .tsc-dot.done   { background: var(--slot-routine); border-color: var(--slot-routine); }
.tsc-family .tsc-dot    { border-color: rgba(219,39,119,.3); }  .tsc-family .tsc-dot.done    { background: var(--slot-family); border-color: var(--slot-family); }
.tsc-line { flex: 1; width: 2px; margin-top: 3px; background: var(--border); }
.tsc-content { display: flex; align-items: flex-start; padding: 9px 0 12px; cursor: pointer; }
.tsc-content input { position: absolute; opacity: 0; pointer-events: none; }
.tsc-card { flex: 1; padding: 10px 14px; border-radius: 13px; border: 1px solid var(--border); background: rgba(255,255,255,.5); transition: all .18s; }
.tsc-card:hover { background: rgba(255,255,255,.82); box-shadow: var(--shadow-sm); }
.tsc-card.done { opacity: .52; }
.tsc-card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
.tsc-badge { display: inline-flex; align-items: center; height: 19px; padding: 0 7px; border-radius: 999px; font-size: .6rem; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; }
.badge-nutrition { background: var(--slot-nutrition-bg); color: var(--slot-nutrition); border: 1px solid var(--slot-nutrition-border); }
.badge-movement  { background: var(--slot-movement-bg);  color: var(--slot-movement);  border: 1px solid var(--slot-movement-border); }
.badge-sleep     { background: var(--slot-sleep-bg);     color: var(--slot-sleep);     border: 1px solid var(--slot-sleep-border); }
.badge-routine   { background: var(--slot-routine-bg);   color: var(--slot-routine);   border: 1px solid var(--slot-routine-border); }
.badge-family    { background: var(--slot-family-bg);    color: var(--slot-family);    border: 1px solid var(--slot-family-border); }
.tsc-check { width: 20px; height: 20px; border-radius: 50%; border: 1.5px solid rgba(23,32,51,.12); display: flex; align-items: center; justify-content: center; flex-shrink: 0; transition: all .2s; }
.tsc-check.done { background: var(--coral); border-color: var(--coral); }
.tsc-text { display: block; font-size: .88rem; font-weight: 600; line-height: 1.45; color: #2d3230; }
.tsc-card.done .tsc-text { text-decoration: line-through; color: var(--muted); }
.tsc-detail { display: block; margin-top: 4px; font-size: .76rem; font-style: italic; color: var(--muted); line-height: 1.5; }
.tsc-empty { text-align: center; padding: 24px 0; font-style: italic; color: var(--muted); font-size: .9rem; }

.roadmap-section {
  position: relative;
  z-index: 1;
  padding: clamp(60px, 8vw, 100px) 0;
}

.roadmap-refresh {
  --planner-ink: #16302b;
  --planner-muted: #65746f;
  --planner-cream: #fffaf2;
  --planner-card: rgba(255, 248, 239, 0.78);
  --planner-white: rgba(255, 255, 255, 0.72);
  --planner-sage: #5fae9b;
  --planner-sage-dark: #327c70;
  --planner-sage-soft: #e8f6f2;
  --planner-coral: #f59f7a;
  --planner-coral-dark: #e6865f;
}

.planner-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 24px;
  align-items: end;
  margin-bottom: 28px;
}

.planner-total-card,
.planner-shell,
.planner-main-card,
.planner-week-list {
  border: 1px solid rgba(255, 255, 255, 0.72);
  background: var(--planner-card);
  box-shadow: 0 24px 60px rgba(23, 32, 51, 0.11);
  backdrop-filter: blur(14px);
}

.planner-total-card {
  display: grid;
  grid-template-columns: 96px 1fr;
  gap: 18px;
  align-items: center;
  padding: 20px;
  border-radius: 28px;
}

.planner-ring {
  width: 92px;
  height: 92px;
  border-radius: 50%;
  display: grid;
  place-items: center;
}

.planner-ring div {
  width: 66px;
  height: 66px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  text-align: center;
  background: white;
  box-shadow: inset 0 0 0 1px rgba(22, 48, 43, 0.08);
}

.planner-ring strong {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.35rem;
  line-height: 1;
  color: var(--planner-ink);
}

.planner-ring span,
.planner-small-label {
  display: block;
  color: var(--planner-muted);
  font-size: 0.62rem;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.planner-total-number {
  display: block;
  margin: 6px 0 2px;
  font-family: 'Fraunces', Georgia, serif;
  font-size: 2rem;
  line-height: 1;
  color: var(--planner-ink);
  letter-spacing: -0.04em;
}

.planner-total-card p {
  margin: 0;
  color: var(--planner-muted);
  font-size: 0.82rem;
  line-height: 1.45;
}

.planner-shell {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  gap: 18px;
  padding: 18px;
  border-radius: 34px;
}

.planner-week-list {
  border-radius: 26px;
  padding: 18px;
}

.planner-side-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.planner-side-head span,
.planner-kicker {
  color: var(--planner-sage-dark);
  font-size: 0.68rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.planner-side-head strong {
  color: var(--planner-muted);
  font-size: 0.75rem;
  font-weight: 900;
}

.planner-week-pill {
  width: 100%;
  min-height: 76px;
  display: grid;
  grid-template-columns: 44px 1fr;
  gap: 12px;
  align-items: center;
  padding: 12px;
  margin-bottom: 10px;
  border: 1px solid rgba(22, 48, 43, 0.08);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.48);
  color: var(--planner-ink);
  text-align: left;
  cursor: pointer;
  transition: transform 0.18s ease, background 0.18s ease, box-shadow 0.18s ease;
}

.planner-week-pill:hover,
.planner-week-pill.active {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.82);
  box-shadow: 0 12px 30px rgba(23, 32, 51, 0.1);
}

.planner-week-pill.active {
  border-color: rgba(95, 174, 155, 0.42);
}

.week-dot {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  border-radius: 15px;
  background: rgba(95, 174, 155, 0.12);
  color: var(--planner-sage-dark);
  font-weight: 900;
}

.planner-week-pill.in-progress .week-dot {
  background: rgba(245, 159, 122, 0.16);
  color: var(--planner-coral-dark);
}

.planner-week-pill.completed .week-dot {
  background: var(--planner-sage-dark);
  color: white;
}

.week-copy {
  min-width: 0;
  display: grid;
  gap: 4px;
}

.week-copy strong {
  overflow: hidden;
  color: var(--planner-ink);
  font-size: 0.86rem;
  font-weight: 900;
  line-height: 1.25;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.week-copy small {
  color: var(--planner-muted);
  font-size: 0.72rem;
  font-weight: 700;
}

.week-percent {
  color: var(--planner-sage-dark);
  font-weight: 900;
  font-size: 0.82rem;
}

.planner-main-card {
  border-radius: 28px;
  padding: 24px;
}

.planner-main-head {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: flex-start;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(22, 48, 43, 0.08);
}

.planner-main-head h3 {
  margin: 6px 0 8px;
  font-family: 'Fraunces', Georgia, serif;
  font-size: clamp(1.6rem, 2.4vw, 2.25rem);
  font-weight: 400;
  line-height: 1.05;
  letter-spacing: -0.05em;
  color: var(--planner-ink);
}

.planner-main-head p {
  max-width: 620px;
  margin: 0;
  color: var(--planner-muted);
  line-height: 1.58;
}

.planner-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.planner-edit-btn,
.planner-cancel-btn,
.planner-save-btn {
  height: 36px;
  padding: 0 14px;
  border-radius: 999px;
  border: 0;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  font-weight: 900;
  cursor: pointer;
  transition: transform 0.18s ease, background 0.18s ease;
}

.planner-edit-btn {
  background: var(--planner-sage-dark);
  color: white;
}

.planner-cancel-btn {
  background: rgba(255, 255, 255, 0.72);
  color: var(--planner-muted);
  border: 1px solid rgba(22, 48, 43, 0.1);
}

.planner-save-btn {
  background: var(--planner-ink);
  color: white;
}

.planner-edit-btn:hover,
.planner-cancel-btn:hover,
.planner-save-btn:hover {
  transform: translateY(-1px);
}

.planner-summary-grid {
  display: grid;
  grid-template-columns: 1.25fr 1fr 1fr;
  gap: 12px;
  margin: 20px 0;
}

.planner-summary-card {
  padding: 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.56);
  border: 1px solid rgba(22, 48, 43, 0.07);
}

.planner-summary-card span {
  display: block;
  color: var(--planner-muted);
  font-size: 0.66rem;
  font-weight: 900;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  margin-bottom: 7px;
}

.planner-summary-card strong {
  display: block;
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.7rem;
  line-height: 1;
  color: var(--planner-ink);
  font-weight: 400;
}

.planner-summary-card p {
  margin: 5px 0 0;
  color: var(--planner-muted);
  font-size: 0.78rem;
}

.planner-summary-card i,

.day-picker-btn.today {
  border-color: rgba(245, 159, 122, 0.48);
  box-shadow: 0 0 0 3px rgba(245, 159, 122, 0.12);
}

.day-picker-btn.today span::after {
  content: 'Today';
  display: block;
  margin-top: 3px;
  color: var(--planner-coral-dark);
  font-size: 0.56rem;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.day-picker-btn i,
.mini-week-row i {
  display: block;
  height: 7px;
  margin-top: 12px;
  border-radius: 999px;
  overflow: hidden;
  background: rgba(22, 48, 43, 0.08);
}

.planner-summary-card b,
.day-picker-btn b,
.mini-week-row b {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--planner-sage), var(--planner-sage-dark));
  transition: width 0.25s ease;
}

.day-picker {
  display: grid;
  grid-template-columns: repeat(7, minmax(74px, 1fr));
  gap: 8px;
  margin-bottom: 18px;
}

.day-picker-btn {
  min-height: 76px;
  padding: 10px;
  border: 1px solid rgba(22, 48, 43, 0.08);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.46);
  text-align: left;
  cursor: pointer;
  transition: background 0.18s ease, transform 0.18s ease, box-shadow 0.18s ease;
}

.day-picker-btn:hover,
.day-picker-btn.active {
  background: rgba(255, 255, 255, 0.86);
  transform: translateY(-2px);
  box-shadow: 0 10px 22px rgba(23, 32, 51, 0.08);
}

.day-picker-btn.today {
  border-color: rgba(245, 159, 122, 0.36);
}

.day-picker-btn span {
  display: block;
  color: var(--planner-muted);
  font-size: 0.66rem;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.day-picker-btn strong {
  display: block;
  margin-top: 4px;
  color: var(--planner-ink);
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.22rem;
  font-weight: 400;
}

.selected-day-panel {
  padding: 18px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(22, 48, 43, 0.08);
}

.selected-day-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 14px;
}

.selected-day-head h4 {
  margin: 5px 0 4px;
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.6rem;
  font-weight: 400;
  letter-spacing: -0.04em;
}

.selected-day-head p {
  margin: 0;
  color: var(--planner-muted);
  font-size: 0.88rem;
}

.selected-day-score {
  align-self: flex-start;
  min-width: 64px;
  min-height: 44px;
  display: grid;
  place-items: center;
  padding: 0 12px;
  border-radius: 999px;
  background: var(--planner-sage-soft);
  color: var(--planner-sage-dark);
  font-weight: 900;
}

.simple-slot-list {
  display: grid;
  gap: 10px;
}

.simple-slot {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 10px;
  align-items: flex-start;
  padding: 12px;
  border-radius: 16px;
  border: 1px solid transparent;
}

.simple-slot.slot-nutrition { background: var(--slot-nutrition-bg); border-color: var(--slot-nutrition-border); }
.simple-slot.slot-movement  { background: var(--slot-movement-bg);  border-color: var(--slot-movement-border); }
.simple-slot.slot-sleep     { background: var(--slot-sleep-bg);     border-color: var(--slot-sleep-border); }
.simple-slot.slot-routine   { background: var(--slot-routine-bg);   border-color: var(--slot-routine-border); }
.simple-slot.slot-family    { background: var(--slot-family-bg);    border-color: var(--slot-family-border); }

.simple-slot.done {
  opacity: 0.58;
}

.slot-time {
  color: var(--planner-muted);
  font-size: 0.72rem;
  font-weight: 900;
  white-space: nowrap;
}

.slot-action {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  cursor: pointer;
}

.slot-action input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.slot-check {
  width: 18px;
  height: 18px;
  margin-top: 2px;
  border-radius: 50%;
  border: 1.5px solid rgba(22, 48, 43, 0.18);
  display: grid;
  place-items: center;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.52);
}

.slot-check.done {
  background: var(--planner-sage-dark);
  border-color: var(--planner-sage-dark);
}

.slot-copy {
  display: grid;
  gap: 4px;
}

.slot-copy strong {
  color: var(--planner-ink);
  font-size: 0.9rem;
  line-height: 1.38;
}

.simple-slot.done .slot-copy strong {
  color: var(--planner-muted);
  text-decoration: line-through;
}

.slot-copy small {
  color: var(--planner-muted);
  font-size: 0.76rem;
  font-style: italic;
  line-height: 1.45;
}

.slot-edit-form {
  grid-column: 1 / -1;
  display: grid;
  gap: 7px;
  width: 100%;
}

.slot-edit-row {
  display: grid;
  grid-template-columns: 92px 1fr;
  gap: 7px;
}

.slot-edit-input {
  width: 100%;
  min-height: 36px;
  border-radius: 10px;
  border: 1px solid rgba(22, 48, 43, 0.12);
  background: white;
  padding: 0 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.78rem;
  color: var(--planner-ink);
  outline: none;
}

.slot-edit-input:focus {
  border-color: rgba(95, 174, 155, 0.55);
  box-shadow: 0 0 0 3px rgba(95, 174, 155, 0.12);
}

.planner-empty {
  margin: 0;
  padding: 24px;
  text-align: center;
  color: var(--planner-muted);
  font-style: italic;
}



/* Fix: keep the Week Progress card content aligned and prevent old vertical progress styling */
.planner-stat-card:first-child {
  position: relative;
  overflow: hidden;
}

.planner-stat-card:first-child::before,
.planner-stat-card:first-child::after {
  display: none !important;
}

.planner-stat-card:first-child .planner-stat-value,
.planner-stat-card:first-child strong,
.planner-stat-card:first-child .stat-value {
  line-height: 1;
}

.planner-stat-grid,
.week-stat-grid,
.planner-summary-grid {
  align-items: stretch;
}

.planner-stat-card {
  min-height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.planner-day-pill.today,
.day-pill.today,
.planner-day-card.today {
  border-color: rgba(245, 159, 122, 0.45);
  box-shadow: 0 12px 30px rgba(245, 159, 122, 0.12);
}

@media (max-width: 1120px) {
  .planner-hero,
  .planner-shell {
    grid-template-columns: 1fr;
  }

  .planner-week-list {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
  }

  .planner-side-head {
    grid-column: 1 / -1;
  }

  .planner-week-pill {
    margin-bottom: 0;
    grid-template-columns: 1fr;
  }

  .week-percent {
    justify-self: start;
  }
}

@media (max-width: 760px) {
  .planner-week-list,
  .planner-summary-grid,
  .day-picker {
    grid-template-columns: 1fr;
  }

  .planner-main-head,
  .selected-day-head {
    flex-direction: column;
  }

  .simple-slot {
    grid-template-columns: 1fr;
  }

  .slot-edit-row {
    grid-template-columns: 1fr;
  }
}



.footer { padding: 52px 0 0; background: var(--ink); margin-top: clamp(60px, 8vw, 100px); }
.footer-inner { display: grid; grid-template-columns: 1.6fr 1fr 1fr; gap: 48px; max-width: 1240px; margin: 0 auto; padding: 0 40px 40px; border-bottom: 1px solid rgba(255,255,255,.07); }
.footer-col { display: flex; flex-direction: column; gap: 10px; }
.footer-col-head { margin-bottom: 4px; font-size: .68rem; font-weight: 800; text-transform: uppercase; letter-spacing: .14em; color: rgba(255,255,255,.32); }
.footer-col a { font-size: .84rem; font-weight: 500; color: rgba(255,255,255,.48); text-decoration: none; transition: color .18s; }
.footer-col a:hover { color: rgba(255,255,255,.88); }
.footer-bottom { max-width: 1240px; margin: 0 auto; padding: 18px 40px; }
.footer-bottom p { margin: 0; font-size: .74rem; color: rgba(255,255,255,.2); }
.footer-logo { color: rgba(255,255,255,.82); font-family: 'Fraunces', serif; }
.footer-logo-icon { color: rgba(255,255,255,.7); }
.footer-blurb { margin: 0; font-size: .78rem; line-height: 1.65; color: rgba(255,255,255,.3); }


@media (max-width: 1100px) {
  .roadmap-detail { grid-template-columns: 1fr; }
  .section-head-row { grid-template-columns: 1fr; }
  .journey-stations { gap: 0; }
}
@media (max-width: 900px) {
  .hero-inner { grid-template-columns: 1fr; }
  .header-inner, .section-wrap { padding-left: 22px; padding-right: 22px; }
  .hero-inner { padding-left: 22px; padding-right: 22px; }
  .footer-inner { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 700px) {
  .nav, .nav-link { display: none; }
  .kpi-row { flex-wrap: wrap; }
  .kpi { flex: 0 0 50%; }
  .kpi-div { display: none; }
  .rdm-day-card { min-width: 80vw; flex-basis: 80vw; }
  .footer-inner { grid-template-columns: 1fr; }
  .journey-stations { grid-template-columns: repeat(2, 1fr); grid-template-rows: repeat(2, auto); height: auto; gap: 20px; padding: 20px 0; }
  .journey-station { height: auto; padding: 0 !important; }
  .journey-path-svg { display: none; }
}


.dashboard-page {
  --cream: #fffaf2;
  --cream2: #f3eadf;
  --ink: #12352f;
  --muted: #64736d;
  --coral: #f28a68;
  --coral-dark: #d96d4d;
  --coral-soft: #fff0e9;
  --sage: #4f9f8d;
  --sage-soft: #e5f4ef;
  --sage-dark: #236b60;
  --navy: #12352f;
  --border: rgba(18, 53, 47, 0.10);
  --border-mid: rgba(18, 53, 47, 0.16);
  --glass: rgba(255, 250, 242, 0.78);
  --glass-strong: rgba(255, 252, 247, 0.92);
  --shadow-sm: 0 6px 18px rgba(18, 53, 47, 0.07);
  --shadow-md: 0 16px 40px rgba(18, 53, 47, 0.11);
  --shadow-lg: 0 28px 76px rgba(18, 53, 47, 0.15);
}

.page-bg {
  background:
    linear-gradient(110deg, rgba(255, 250, 242, 0.95) 0%, rgba(255, 250, 242, 0.82) 44%, rgba(229, 244, 239, 0.76) 100%),
    radial-gradient(circle at 18% 78%, rgba(242, 138, 104, 0.20), transparent 32rem),
    radial-gradient(circle at 84% 14%, rgba(79, 159, 141, 0.30), transparent 28rem),
    #f3eadf;
}

.bg-blob-1 { background: radial-gradient(circle, rgba(79,159,141,.24) 0%, transparent 70%); }
.bg-blob-2 { background: radial-gradient(circle, rgba(242,138,104,.18) 0%, transparent 70%); }
.bg-blob-3 { background: radial-gradient(circle, rgba(255,250,242,.72) 0%, transparent 70%); }

.header.scrolled {
  background: rgba(255, 250, 242, 0.86);
  border-bottom-color: rgba(18, 53, 47, 0.10);
}

.nav-btn,
.mission-btn {
  background: linear-gradient(135deg, var(--sage-dark), #17483f);
  box-shadow: 0 12px 28px rgba(18, 53, 47, 0.20);
}

.nav-btn:hover,
.mission-btn:hover {
  background: linear-gradient(135deg, #17483f, var(--sage-dark));
}

.mission-card {
  background: linear-gradient(145deg, rgba(255, 250, 242, 0.92), rgba(255, 240, 233, 0.82));
  border-color: rgba(242, 138, 104, 0.22);
}

.roadmap-refresh {
  --planner-ink: #12352f;
  --planner-muted: #64736d;
  --planner-cream: #fffaf2;
  --planner-card: rgba(255, 250, 242, 0.82);
  --planner-white: rgba(255, 255, 255, 0.78);
  --planner-sage: #4f9f8d;
  --planner-sage-dark: #236b60;
  --planner-sage-soft: #e5f4ef;
  --planner-coral: #f28a68;
  --planner-coral-dark: #d96d4d;
}

.planner-total-card,
.planner-shell,
.planner-main-card,
.planner-week-list {
  border-color: rgba(255, 255, 255, 0.78);
  background: rgba(255, 250, 242, 0.82);
  box-shadow: 0 24px 70px rgba(18, 53, 47, 0.11);
}

.planner-main-card,
.selected-day-panel,
.planner-summary-card,
.day-picker-btn,
.planner-week-pill {
  background: rgba(255, 255, 255, 0.58);
}

.planner-week-pill.active,
.day-picker-btn.active {
  border-color: rgba(79, 159, 141, 0.42);
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 18px 44px rgba(18, 53, 47, 0.10);
}

.day-picker-btn.today {
  border-color: rgba(242, 138, 104, 0.46);
  box-shadow: 0 14px 34px rgba(242, 138, 104, 0.14);
}

.day-picker-btn.today span::after {
  color: var(--planner-coral-dark);
}

.planner-edit-btn,
.planner-save-btn {
  background: linear-gradient(135deg, var(--planner-sage-dark), #17483f);
}

.selected-day-score {
  background: rgba(229, 244, 239, 0.92);
  color: var(--planner-sage-dark);
}

.planner-task-row {
  background: rgba(255, 255, 255, 0.62);
}

.planner-task-row.done {
  background: rgba(229, 244, 239, 0.74);
}

</style>