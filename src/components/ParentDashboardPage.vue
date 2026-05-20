<!--
  ParentDashboardPage.vue

  Creates the HelthyKidz parent dashboard. It loads a saved family plan, shows today's schedule,
  meal actions, movement actions, the 4-week planner, and basic settings.

  API requirement:
  - Requires VITE_PARENT_PROFILES_API_BASE_URL.
  - Uses GET /{familyCode} to load the saved profile.
  - Uses PUT /{familyCode} to save progress and planner updates.

  Accessibility:
  - Uses aria-labels, aria-live, role="status", role="alert", and role="progressbar".
  - Uses aria-pressed for selected tabs, weeks, and days.
  - Uses aria-disabled for locked planner controls.
  - Uses data-hover-read-text for hover-to-read support.
-->

<template>
  <div class="dashboard-page">
    <!-- Background -->
    <div class="dashboard-page-bg" aria-hidden="true">
      <img
        class="dashboard-page-bg__img"
        src="https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=2400&q=90"
        alt=""
        aria-hidden="true"
      />
      <div class="dashboard-page-bg__overlay"></div>
      <div class="dashboard-page-bg__grain"></div>
    </div>

    <!-- LOADING / ERROR STATES -->
    <div
      v-if="planLoading"
      class="dashboard-state-screen"
      role="status"
      aria-live="polite"
      data-hover-read-text="Loading your personalised family plan."
    >
      <div class="dashboard-state-spinner" aria-hidden="true"></div>
      <p class="dashboard-state-msg">Loading your personalised family plan...</p>
    </div>

    <!-- Error state shown when the dashboard plan cannot load -->
    <div
      v-else-if="planError"
      class="dashboard-state-screen"
      role="alert"
      aria-live="assertive"
      :data-hover-read-text="`Could not load your family plan. ${planError}`"
    >
      <p class="dashboard-state-error">Could not load your family plan: {{ planError }}</p>
      <button
        class="dashboard-nav-btn"
        type="button"
        data-hover-read-text="Retry loading your family plan"
        @click="fetchPlan(state.username)"
      >
        Retry
      </button>
    </div>

    <!-- Empty state shown when there is no saved family plan yet -->
    <div
      v-else-if="!isPlanReady"
      class="dashboard-state-screen"
      role="status"
      aria-live="polite"
      data-hover-read-text="No family plan found yet. Complete the quiz to create your plan."
    >
      <p class="dashboard-state-msg">No family plan found yet.</p>
      <RouterLink to="/parent-quiz" class="dashboard-nav-btn">Complete quiz</RouterLink>
    </div>

    <!-- Main dashboard content appears once the plan is ready -->
    <main
      v-else
      id="main-content"
      class="dashboard-main"
      aria-labelledby="dashboard-page-title"
    >
      <!-- Website journey progress bar -->
      <FamilyJourneyBar :current-step="3" />


    <section
        class="dashboard-content-card dashboard-content-card--wide"
        aria-labelledby="dashboard-page-title"
        aria-describedby="dashboard-section-description"
      >
        <div class="dashboard-content-header">
          <div class="dashboard-content-header-text">
            <div
              class="dashboard-content-eyebrow"
              data-hover-read-text="Step 03. Daily activities."
            >
              <span class="dashboard-eyebrow-dot" aria-hidden="true"></span>
              Step 03 · Daily activities
            </div>

            <h1
              id="dashboard-page-title"
              class="dashboard-content-title"
              data-hover-read-text="Today's family actions"
            >
              Today's family actions
            </h1>

            <p
              id="dashboard-section-description"
              class="dashboard-content-subtitle"
              data-hover-read-text="Follow small daily actions across nutrition, movement, sleep and routine."
            >
              Follow small daily actions across nutrition, movement, sleep and routine.
            </p>
          </div>

          <div
            class="dashboard-today-progress-ring"
            role="progressbar"
            :aria-valuenow="todayProgress"
            aria-valuemin="0"
            aria-valuemax="100"
            :aria-label="`Today's progress is ${todayProgress} percent`"
            :data-hover-read-text="`Today's progress is ${todayProgress} percent`"
          >
            <svg aria-hidden="true" viewBox="0 0 64 64" width="64" height="64">
              <circle
                cx="32"
                cy="32"
                r="26"
                fill="none"
                stroke="rgba(22,48,43,0.08)"
                stroke-width="5"
              />
              <circle
                cx="32"
                cy="32"
                r="26"
                fill="none"
                stroke="#13806f"
                stroke-width="5"
                stroke-linecap="round"
                stroke-dasharray="163.4"
                :stroke-dashoffset="163.4 - (163.4 * todayProgress / 100)"
                transform="rotate(-90 32 32)"
                style="transition: stroke-dashoffset 0.6s ease"
              />
            </svg>

            <div class="dashboard-ring-inner">
              <strong>{{ todayProgress }}%</strong>
            </div>
          </div>
        </div>

        <div class="dashboard-daily-summary-row">
          <div class="dashboard-daily-summary-card">
            <span>Family code</span>
            <strong>{{ familyCode }}</strong>
          </div>

          <div class="dashboard-daily-summary-card">
            <span>Today</span>
            <strong>{{ selectedDateLabel }}</strong>
          </div>

          <div class="dashboard-daily-summary-card">
            <span>Completed</span>
            <strong>{{ completedTodayCount }} / {{ todayFullSchedule.length }}</strong>
          </div>
        </div>

        <div class="dashboard-slot-list">
          <div
            class="dashboard-day-cycle-card"
            role="region"
            aria-label="Day at a glance timeline"
            :data-hover-read-text="`Day at a glance. ${completedTodayCount} complete and ${todayFullSchedule.length - completedTodayCount} remaining.`"
          >
            <div class="dashboard-day-cycle-header">
              <span class="dashboard-day-cycle-title">Day at a glance</span>
              <span class="dashboard-day-cycle-sub">
                {{ completedTodayCount }} complete · {{ todayFullSchedule.length - completedTodayCount }} remaining
              </span>
            </div>

            <div class="dashboard-day-cycle-track-wrap">
              <div class="dashboard-day-cycle-track">
                <div class="dashboard-day-cycle-zone dashboard-day-cycle-zone-morning" style="left: 0%; width: 18%;">
                  <span>Morning</span>
                </div>

                <div class="dashboard-day-cycle-zone dashboard-day-cycle-zone-afternoon" style="left: 18%; width: 40%;">
                  <span>Afternoon</span>
                </div>

                <div class="dashboard-day-cycle-zone dashboard-day-cycle-zone-evening" style="left: 58%; width: 27%;">
                  <span>Evening</span>
                </div>

                <div class="dashboard-day-cycle-zone dashboard-day-cycle-zone-night" style="left: 85%; width: 15%;">
                  <span>Night</span>
                </div>

                <div
                  class="dashboard-day-cycle-progress"
                  :style="{ width: currentTimePercent + '%' }"
                  aria-hidden="true"
                ></div>

                <div
                  class="dashboard-day-cycle-now"
                  :style="{ left: currentTimePercent + '%' }"
                  aria-hidden="true"
                >
                  <div class="dashboard-day-cycle-now-line"></div>
                  <div class="dashboard-day-cycle-now-label">now</div>
                </div>

                <button
                  v-for="slot in todayFullSchedule"
                  :key="slot.id"
                  type="button"
                  class="dashboard-day-cycle-node"
                  :class="[
                    'dashboard-day-cycle-node-' + slot.category,
                    {
                      'dashboard-day-cycle-node--done': slot.done,
                      'dashboard-day-cycle-node--upcoming': isUpcoming(slot)
                    }
                  ]"
                  :style="{ left: slotTimePercent(slot.time) + '%' }"
                  :aria-label="`${slot.time}. ${slot.text}. ${slot.done ? 'Completed' : 'Not completed'}`"
                  :data-hover-read-text="`${slot.time}. ${slot.text}. ${slot.done ? 'Completed' : 'Not completed'}`"
                  @click="toggleTodayScheduleSlot(slot)"
                >
                  <span class="dashboard-day-cycle-node-icon" aria-hidden="true">
                    <svg v-if="slot.done" width="10" height="10" viewBox="0 0 10 10">
                      <path
                        d="M2 5l2.5 2.5L8 3"
                        stroke="white"
                        stroke-width="1.7"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        fill="none"
                      />
                    </svg>
                    <span v-else>{{ catInitial(slot.category) }}</span>
                  </span>

                  <span class="dashboard-day-cycle-tooltip" aria-hidden="true">
                    <strong>{{ slot.time }}</strong>
                    <span>{{ slot.text }}</span>
                  </span>
                </button>
              </div>

              <div class="dashboard-day-cycle-time-labels" aria-hidden="true">
                <span>6 am</span>
                <span>9 am</span>
                <span>12 pm</span>
                <span>3 pm</span>
                <span>6 pm</span>
                <span>9 pm</span>
              </div>
            </div>

            <div class="dashboard-day-cycle-legend" aria-label="Timeline category legend">
              <div
                v-for="cat in scheduleCategories"
                :key="cat.key"
                class="dashboard-day-cycle-legend-item"
                :class="'dashboard-day-cycle-legend-' + cat.key"
              >
                <span aria-hidden="true"></span>
                {{ cat.label }}
              </div>
            </div>
          </div>

          <label
            v-for="slot in todayFullSchedule"
            :key="slot.id"
            class="dashboard-slot-row"
            :class="['dashboard-cat-' + slot.category, { 'dashboard-slot-row--done': slot.done }]"
            :data-hover-read-text="getSlotReadableText(slot)"
          >
            <div class="dashboard-slot-time-col">
              <span class="dashboard-slot-time">{{ slot.time }}</span>
              <span class="dashboard-slot-cat-badge">{{ getCategoryLabel(slot.category) }}</span>
            </div>

            <input
              type="checkbox"
              :checked="slot.done"
              :aria-label="`${slot.done ? 'Mark incomplete' : 'Mark complete'}: ${slot.text}`"
              @change="toggleTodayScheduleSlot(slot)"
            />

            <span
              class="dashboard-slot-checkbox"
              :class="{ 'dashboard-slot-checkbox--checked': slot.done }"
              aria-hidden="true"
            >
              <svg v-if="slot.done" width="10" height="10" viewBox="0 0 10 10">
                <path
                  d="M2 5l2.5 2.5L8 3"
                  stroke="white"
                  stroke-width="1.7"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  fill="none"
                />
              </svg>
            </span>

            <div class="dashboard-slot-body">
              <strong class="dashboard-slot-title">{{ slot.text }}</strong>
              <span v-if="slot.detail || slot.tip" class="dashboard-slot-tip">
                {{ slot.detail || slot.tip }}
              </span>
            </div>
          </label>

          <p v-if="!todayFullSchedule.length" class="dashboard-empty-state">
            No actions scheduled for today.
          </p>
        </div>

        <div class="dashboard-next-step-card dashboard-next-step-card--split">
          <RouterLink
            to="/parent-quiz"
            class="dashboard-next-step-btn dashboard-next-step-btn--previous"
            aria-label="Go back to build profile page"
            data-hover-read-text="Previous step. Go back to build profile."
          >
            <span aria-hidden="true">←</span>
            Previous step
          </RouterLink>

          <div class="dashboard-next-step-copy">
            <span>Step 03 of 05</span>
            <strong>Continue to your 4-week plan</strong>
            <p>Review the longer weekly roadmap after completing today's actions.</p>
          </div>

          <RouterLink
            to="/parent-roadmap"
            class="dashboard-next-step-btn"
            aria-label="Go to the four week roadmap"
            data-hover-read-text="Go to the four week plan"
          >
            Open 4-week plan
            <span aria-hidden="true">→</span>
          </RouterLink>
        </div>
      </section>

      <!-- Dashboard footer -->
      <footer
        class="dashboard-inner-footer"
        aria-label="Website footer"
      >
        <div
          class="dashboard-inner-footer-left"
          aria-label="Supporting families across Australia"
          data-hover-read-text
        >
          <span class="dashboard-inner-footer-live-dot" aria-hidden="true"></span>
          Supporting families across Australia
        </div>

        <div
          class="dashboard-inner-footer-right"
          aria-label="UN Sustainable Development Goal 3, Good Health and Wellbeing. Developed by Team SYRBYX."
          data-hover-read-text
        >
          <span>UN SDG 3 · Good Health &amp; Wellbeing</span>
          <span class="dashboard-home-footer-divider" aria-hidden="true">·</span>
          <span>Developed by Team SYRBYX</span>
        </div>
      </footer>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'
import { useDynamicPlan } from '../composables/useDynamicPlan'
import FamilyJourneyBar from '../components/FamilyJourneyBar.vue'

// Shared family plan store and dynamic plan helpers.
const { state, savePlan } = useFamilyPlanStore()
const { loading: planLoading, error: planError, fetchPlan, buildRoadmapWeeks } = useDynamicPlan()

// Date, locale, and API configuration.
const TIME_ZONE = 'Australia/Melbourne'
const LOCALE = 'en-AU'
const DAY_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
const API_BASE_URL = import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL
const route = useRoute()

// Saving state for backend sync.
const isSavingDashboard = ref(false)

// Categories used in today's timeline and action labels.
const scheduleCategories = [
  { key: 'nutrition', label: 'Nutrition' },
  { key: 'movement', label: 'Movement' },
  { key: 'sleep', label: 'Sleep / Wind-down' },
  { key: 'routine', label: 'Routine' },
  { key: 'family', label: 'Family time' },
]

// Timer value used to refresh the current-time marker.
const nowTick = ref(Date.now())
let nowTimer = null

// Returns today's weekday name using the configured timezone.
function getTodayName() {
  return new Date().toLocaleDateString(LOCALE, {
    weekday: 'long',
    timeZone: TIME_ZONE,
  })
}

// Safely returns an object, or an empty object when the value is invalid.
function safeObject(value) {
  if (!value || Array.isArray(value) || typeof value !== 'object') return {}
  return value
}

// Converts internal category keys into user-facing labels.
function getCategoryLabel(category) {
  return {
    nutrition: 'Nutrition',
    movement: 'Movement',
    sleep: 'Wind-down',
    routine: 'Routine',
    family: 'Family',
  }[category] || 'Routine'
}

// Normalises API profile fields so both camelCase and snake_case responses work.
function normalizeDashboardProfile(profile = {}) {
  const progressItems = safeObject(profile.progressItems || profile.progress_items)

  return {
    ...profile,

    username: profile.username || state.username || '',
    userName: profile.username || state.userName || '',
    user_name: profile.username || state.user_name || '',

    childName: profile.childName ?? profile.child_name ?? state.childName,
    child_name: profile.childName ?? profile.child_name ?? state.child_name,

    parentName: profile.parentName ?? profile.parent_name ?? state.parentName,
    parent_name: profile.parentName ?? profile.parent_name ?? state.parent_name,

    dailyPlan: profile.dailyPlan ?? profile.daily_plan ?? state.dailyPlan ?? {},

    progressItems,

    roadmapProgress: safeObject(
      profile.roadmapProgress ||
        profile.roadmap_progress ||
        progressItems.roadmapProgress ||
        state.roadmapProgress
    ),

    todaySchedule: safeObject(
      profile.todaySchedule ||
        profile.today_schedule ||
        progressItems.todaySchedule ||
        state.todaySchedule
    ),

    plannerOverrides: safeObject(
      profile.plannerOverrides ||
        profile.planner_overrides ||
        progressItems.plannerOverrides ||
        state.plannerOverrides
    ),

    streakDays: profile.streakDays ?? profile.streak_days ?? state.streakDays ?? 0,
    streak_days: profile.streakDays ?? profile.streak_days ?? state.streak_days ?? 0,

    nextAction: profile.nextAction ?? profile.next_action ?? state.nextAction,
    next_action: profile.nextAction ?? profile.next_action ?? state.next_action,

    mission: profile.mission ?? state.mission,
  }
}

// Loads the saved parent profile from the parent profiles API.
async function fetchParentProfile(username) {
  if (!username) throw new Error('Missing username')
  if (!API_BASE_URL) throw new Error('Missing VITE_PARENT_PROFILES_API_BASE_URL')

  const response = await fetch(`${API_BASE_URL}/${encodeURIComponent(username)}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  })

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(data.error || `Profile load failed: ${response.status}`)
  }

  return data
}

// Loads the dashboard plan and profile for the selected family code.
async function loadDashboard(username) {
  if (!username) return

  localStorage.setItem('hk-parent-username', username)

  savePlan({
    ...state,
    username,
    userName: username,
    user_name: username,
  })

  await fetchPlan(username)

  const profile = await fetchParentProfile(username)
  const normalizedProfile = normalizeDashboardProfile(profile)

  savePlan({
    ...state,
    ...normalizedProfile,
  })
}

// Applies saved planner edits to a generated slot without changing the original slot shape.
function applyPlannerOverridesToSlot(slot) {
  const overrides = safeObject(state.plannerOverrides)
  const edited = overrides[slot.id]

  if (!edited) return slot

  const category = edited.category || slot.category

  return {
    ...slot,
    time: edited.time || slot.time,
    text: edited.text || slot.text,
    tip: edited.tip ?? slot.tip,
    category,
    categoryLabel: getCategoryLabel(category),
  }
}

// Builds the 4-week roadmap and calculates day-level progress.
const fourWeekRoadmap = computed(() => {
  const roadmapProgress = safeObject(state.roadmapProgress)

  return buildRoadmapWeeks(roadmapProgress).map(week => ({
    ...week,

    dailyPlan: [...(week.dailyPlan || [])]
      .sort((a, b) => {
        const aIndex = DAY_ORDER.indexOf(a.day)
        const bIndex = DAY_ORDER.indexOf(b.day)

        return (aIndex === -1 ? 99 : aIndex) - (bIndex === -1 ? 99 : bIndex)
      })
      .map(day => {
        const timeSlots = (day.timeSlots || []).map(applyPlannerOverridesToSlot)
        const completed = timeSlots.filter(slot => slot.done).length
        const progress = timeSlots.length
          ? Math.round((completed / timeSlots.length) * 100)
          : 0

        return {
          ...day,
          timeSlots,
          completed,
          progress,
        }
      }),
  }))
})

// Checks whether the roadmap has been generated.
const isPlanReady = computed(() => fourWeekRoadmap.value.length > 0)

// Finds the first incomplete week and treats it as the active/current week.
const currentWeek = computed(() => {
  const firstIncompleteWeek = fourWeekRoadmap.value.find(week => week.progress < 100)

  return firstIncompleteWeek?.week || fourWeekRoadmap.value[0]?.week || 1
})

// Today's weekday name.
const todayName = computed(() => getTodayName())

// Today's full schedule from the current week.
const todayFullSchedule = computed(() => {
  const week = fourWeekRoadmap.value.find(item => item.week === currentWeek.value)
  const today = week?.dailyPlan?.find(day => day.day === todayName.value)

  return today?.timeSlots || []
})

// Completed action count for today.
const completedTodayCount = computed(() =>
  todayFullSchedule.value.filter(slot => slot.done).length
)

// Completion percentage for today's progress ring.
const todayProgress = computed(() =>
  todayFullSchedule.value.length
    ? Math.round((completedTodayCount.value / todayFullSchedule.value.length) * 100)
    : 0
)

// Current family code from store or localStorage.
const familyCode = computed(() =>
  state.username ||
  state.userName ||
  state.user_name ||
  localStorage.getItem('hk-parent-username') ||
  'Family'
)

// Formatted date label for the dashboard.
const selectedDateLabel = computed(() =>
  new Date().toLocaleDateString(LOCALE, {
    weekday: 'long',
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    timeZone: TIME_ZONE,
  })
)

// Calculates where the current time should appear on the day timeline.
const currentTimePercent = computed(() => {
  nowTick.value

  const now = new Date()
  const totalMins = now.getHours() * 60 + now.getMinutes()
  const startMins = 6 * 60
  const endMins = 21 * 60

  return Math.min(
    100,
    Math.max(0, ((totalMins - startMins) / (endMins - startMins)) * 100)
  )
})

// Converts a time string into a percentage position on the daily timeline.
function slotTimePercent(timeStr) {
  if (!timeStr) return 0

  const str = String(timeStr).toLowerCase().trim()
  const match = str.match(/^(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$/i)

  if (!match) return 0

  let h = parseInt(match[1], 10) || 0
  const m = parseInt(match[2] || '0', 10) || 0
  const period = match[3]

  if (period === 'pm' && h !== 12) h += 12
  if (period === 'am' && h === 12) h = 0

  const totalMins = h * 60 + m
  const startMins = 6 * 60
  const endMins = 21 * 60

  return Math.min(
    100,
    Math.max(0, ((totalMins - startMins) / (endMins - startMins)) * 100)
  )
}

// Identifies upcoming timeline items.
function isUpcoming(slot) {
  return !slot.done && slotTimePercent(slot.time) >= currentTimePercent.value - 4
}

// Returns a one-letter category marker for timeline nodes.
function catInitial(category) {
  return {
    nutrition: 'N',
    movement: 'M',
    sleep: 'S',
    routine: 'R',
    family: 'F',
  }[category] || '·'
}

// Builds readable text for hover-to-read and assistive features.
function getSlotReadableText(slot) {
  const status = slot.done ? 'Completed' : 'Not completed'
  const category = getCategoryLabel(slot.category)
  const detail = slot.detail || slot.tip || ''

  return `${status}. ${slot.time}. ${category}. ${slot.text}. ${detail}`
}

// Converts different slot ID formats into one canonical action ID.
function getCanonicalActionId(slotOrId) {
  if (slotOrId === null || slotOrId === undefined) return ''

  if (typeof slotOrId === 'string' || typeof slotOrId === 'number') {
    return String(slotOrId).replace('today-schedule-', '')
  }

  return String(slotOrId.sourceSlotId || slotOrId.id || '').replace('today-schedule-', '')
}

// Combines progress, today schedule, and planner overrides into progressItems.
function buildProgressItems(updatedState) {
  return {
    ...safeObject(updatedState.progressItems),
    roadmapProgress: safeObject(updatedState.roadmapProgress),
    todaySchedule: safeObject(updatedState.todaySchedule),
    plannerOverrides: safeObject(updatedState.plannerOverrides),
  }
}

// Toggles a roadmap or today action and persists the updated progress.
function togglePlanAction(slotOrId) {
  const actionId = getCanonicalActionId(slotOrId)

  if (!actionId) return

  const currentRoadmapProgress = safeObject(state.roadmapProgress)
  const currentTodaySchedule = safeObject(state.todaySchedule)
  const nextDone = !currentRoadmapProgress[actionId]

  const updatedState = {
    ...state,
    roadmapProgress: {
      ...currentRoadmapProgress,
      [actionId]: nextDone,
    },
    todaySchedule: {
      ...currentTodaySchedule,
      [`today-schedule-${actionId}`]: nextDone,
    },
  }

  updatedState.progressItems = buildProgressItems(updatedState)

  saveAndPersist(updatedState)
}

// Toggles an action from today's schedule.
function toggleTodayScheduleSlot(slot) {
  togglePlanAction(slot)
}

// Saves updates locally first, then syncs them to the backend.
function saveAndPersist(updatedState) {
  savePlan(updatedState)

  persistDashboardUpdate(updatedState).catch(error => {
    console.error('Dashboard sync failed:', error)
  })
}

// Persists dashboard progress and planner updates to the parent profile API.
async function persistDashboardUpdate(updatedState) {
  const username = updatedState.username || state.username

  if (!username) throw new Error('Missing username')
  if (!API_BASE_URL) throw new Error('Missing VITE_PARENT_PROFILES_API_BASE_URL')

  const roadmapProgress = safeObject(updatedState.roadmapProgress)
  const todaySchedule = safeObject(updatedState.todaySchedule)
  const plannerOverrides = safeObject(updatedState.plannerOverrides)

  const progressItems = {
    ...safeObject(updatedState.progressItems),
    roadmapProgress,
    todaySchedule,
    plannerOverrides,
  }

  const payload = {
    dailyPlan: updatedState.dailyPlan ?? state.dailyPlan ?? {},
    progressItems,
    roadmapProgress,
    todaySchedule,
    plannerOverrides,
    streakDays: updatedState.streakDays ?? state.streakDays ?? 0,
    nextAction: updatedState.nextAction ?? state.nextAction,
    mission: updatedState.mission ?? state.mission,
  }

  isSavingDashboard.value = true

  try {
    const response = await fetch(`${API_BASE_URL}/${encodeURIComponent(username)}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    const data = await response.json().catch(() => ({}))

    if (!response.ok) {
      throw new Error(data.error || `Update failed: ${response.status}`)
    }

    const normalizedResponse = normalizeDashboardProfile({
      ...updatedState,
      ...data,
    })

    savePlan({
      ...state,
      ...normalizedResponse,
    })

    return data
  } finally {
    isSavingDashboard.value = false
  }
}

// Sets up dashboard loading and starts the current-time timer.
onMounted(() => {
  const routeUsername = route.query.username || route.params.username || ''
  const savedUsername =
    state.username ||
    state.userName ||
    state.user_name ||
    localStorage.getItem('hk-parent-username') ||
    ''

  const username = String(routeUsername || savedUsername).trim()

  if (username) {
    loadDashboard(username).catch(error => {
      console.error('Dashboard load failed:', error)
    })
  }

  nowTimer = window.setInterval(() => {
    nowTick.value = Date.now()
  }, 60_000)
})

// Cleans up the timer when leaving the page.
onUnmounted(() => {
  if (nowTimer) {
    window.clearInterval(nowTimer)
  }
})
</script>