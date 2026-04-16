<template>
  <div class="dashboard-page">
    <header class="site-header">
      <div class="container header-row">
        <RouterLink to="/" class="brand">HealthyKids</RouterLink>

        <nav class="nav" aria-label="Primary">
          <RouterLink to="/" class="nav-link">Home</RouterLink>
          <RouterLink to="/parent-entry" class="nav-link">Parent access</RouterLink>
          <RouterLink to="/parent-quiz" class="nav-link">Retake quiz</RouterLink>
        </nav>

        <RouterLink to="/parent-quiz" class="header-btn">Quiz</RouterLink>
      </div>
    </header>

    <main>
      <section class="dashboard-top">
        <div class="container">
          <div class="top-shell">
            <div class="top-copy">
              <p class="eyebrow">Parent dashboard</p>
              <h1>Your family plan</h1>
              <p class="top-text">
                A practical view of what to do today, what is coming next this week, and how your
                family is progressing over time.
              </p>

              <div class="top-pills">
                <span>{{ state.ageRange || 'Age range not set yet' }}</span>
                <span>{{ state.supportStyle || 'Daily micro-actions' }}</span>
                <span>{{ streakDays }} day streak</span>
              </div>
            </div>

            <div class="top-side">
              <article class="summary-card mission-card" :class="{ celebrate: showCelebration }">
                <div v-if="showCelebration" class="confetti-layer" aria-hidden="true">
                  <span
                    v-for="piece in confettiPieces"
                    :key="piece.id"
                    class="confetti-piece"
                    :style="piece.style"
                  ></span>
                </div>

                <p class="card-kicker">Daily mission</p>
                <h2>{{ mission }}</h2>
                <p>Keep momentum by completing one healthy action today.</p>

                <div class="mission-progress-top">
                  <span>Family streak: </span>
                  <strong>{{ streakDays }} days</strong>
                </div>

                <div class="progress-track">
                  <div class="progress-fill" :style="{ width: `${streakProgress}%` }"></div>
                </div>

                <button type="button" class="pill-btn dark" @click="completeMission">
                  Mark mission done
                </button>
              </article>
            </div>
          </div>
        </div>
      </section>

      <section class="today-plan-section">
        <div class="container">
          <div class="section-head">
            <p class="section-label">Today's plan</p>
            <h2>{{ todayName }}</h2>
          </div>

          <div class="today-plan-grid">
            <article class="glass-card">
              <p class="today-focus-label">Today's tasks</p>
              <h3>{{ todayName }}</h3>
              <p class="today-progress-copy">
                {{ completedTodayCount }} of {{ todayTasks.length }} tasks completed
              </p>

              <div class="progress-track large">
                <div class="progress-fill" :style="{ width: `${todayProgress}%` }"></div>
              </div>

              <div class="task-list">
                <label
                  v-for="task in todayTasks"
                  :key="task.id"
                  class="task-item"
                  :class="{ done: task.done }"
                >
                  <input
                    type="checkbox"
                    :checked="task.done"
                    @change="toggleTodayTask(task.id)"
                  />
                  <span>{{ task.text }}</span>
                </label>

                <p v-if="!todayTasks.length" class="empty-state">
                  No tasks yet. Complete the parent quiz to generate a daily plan.
                </p>
              </div>
            </article>

            <article class="glass-card side-info-card">
              <p class="section-label">This week</p>
              <h3>What matters most</h3>
              <p class="info-copy">{{ weeklyNarrative }}</p>

              <ul class="detail-list">
                <li><strong>Main concerns:</strong> {{ concernSummary }}</li>
                <li><strong>Habit focus:</strong> {{ habitSummary }}</li>
                <li><strong>Expected win:</strong> {{ winNarrative }}</li>
              </ul>
            </article>
          </div>
        </div>
      </section>

      <section class="weekly-plan-section">
        <div class="container">
          <div class="section-head">
            <p class="section-label">Day-by-day plan</p>
            <h2>Your weekly family routine</h2>
          </div>

          <div class="weekly-days-grid">
            <article
              v-for="day in orderedDays"
              :key="day"
              class="glass-card weekday-card"
              :class="{ active: day === todayName }"
            >
              <h3>{{ day }}</h3>

              <ul v-if="resolvedDailyPlan[day]?.length" class="weekday-list">
                <li v-for="task in resolvedDailyPlan[day]" :key="task.id">
                  {{ task.text }}
                </li>
              </ul>

              <p v-else class="empty-state">No tasks planned.</p>
            </article>
          </div>
        </div>
      </section>

      <section class="tracker-section">
        <div class="container tracker-grid">
          <article class="glass-card tracker-card">
            <div class="section-head compact">
              <div>
                <p class="section-label">Progress tracker</p>
                <h2>Track healthy wins</h2>
              </div>
              <div class="tracker-badge">{{ progressCompletion }}%</div>
            </div>

            <div class="task-list">
              <label
                v-for="item in resolvedProgressItems"
                :key="item.id"
                class="task-item"
                :class="{ done: item.done }"
              >
                <input
                  type="checkbox"
                  :checked="item.done"
                  @change="toggleProgressItem(item.id)"
                />
                <span>{{ item.text }}</span>
              </label>
            </div>
          </article>

          <article class="glass-card tracker-card">
            <p class="section-label">Add your own</p>
            <h2>Custom progress item</h2>

            <div class="custom-item-form">
              <input
                v-model="newProgressItem"
                type="text"
                placeholder="e.g. Packed fruit for school"
                class="custom-input"
                @keyup.enter="addProgressItem"
              />
              <button type="button" class="pill-btn dark" @click="addProgressItem">
                Add item
              </button>
            </div>
          </article>
        </div>
      </section>

      <section class="chart-section">
        <div class="container">
          <div class="section-head">
            <p class="section-label">Weekly progress</p>
            <h2>Daily consistency across the week</h2>
          </div>

          <article class="glass-card chart-card">
            <div class="chart-header">
              <div>
                <p class="chart-label">Habit consistency</p>
                <h3>7-day progress view</h3>
              </div>
              <div class="chart-summary">{{ weeklyAverage }}% average</div>
            </div>

            <div class="chart-interactive-wrap">
              <div class="bar-chart">
                <button
                  v-for="day in weeklyProgress"
                  :key="day.label"
                  type="button"
                  class="bar-column interactive-bar"
                  :class="{ active: selectedDay.label === day.label }"
                  :title="`${day.fullLabel}: ${day.value}%`"
                  @click="selectedDayLabel = day.label"
                >
                  <div class="bar-value">{{ day.value }}%</div>
                  <div class="bar-track">
                    <div class="bar-fill" :style="{ height: `${day.value}%` }"></div>
                  </div>
                  <div class="bar-label">{{ day.label }}</div>
                </button>
              </div>

              <div class="chart-detail-card">
                <p class="card-kicker">Selected day</p>
                <h4>{{ selectedDay.fullLabel }}</h4>
                <p class="chart-detail-score">{{ selectedDay.value }}% completed</p>
                <p class="chart-detail-text">
                  {{ selectedDay.completed }} of {{ selectedDay.total }} planned tasks completed.
                </p>

                <ul class="chart-detail-list" v-if="selectedDay.tasks.length">
                  <li v-for="task in selectedDay.tasks" :key="task.id">
                    <span :class="{ 'done-text': task.done }">{{ task.text }}</span>
                  </li>
                </ul>
              </div>
            </div>
          </article>
        </div>
      </section>

      <section class="overview-section">
        <div class="container overview-grid single">
          <article class="glass-card">
            <p class="section-label">Why this matters</p>
            <h2>This week</h2>

            <p class="summary-text">{{ weeklyNarrative }}</p>

            <ul class="detail-list">
              <li><strong>Risk if ignored:</strong> {{ riskNarrative }}</li>
              <li><strong>Expected win:</strong> {{ winNarrative }}</li>
              <li><strong>Best support style:</strong> {{ state.supportStyle || 'Daily micro-actions' }}</li>
            </ul>
          </article>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'

const { state, savePlan } = useFamilyPlanStore()

const showCelebration = ref(false)
const newProgressItem = ref('')
const selectedDayLabel = ref('Mon')

const orderedDays = [
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
  'Sunday',
]

const defaultDailyPlan = {
  Monday: [
    { id: 101, text: 'Prepare one healthy after-school snack', done: false },
    { id: 102, text: 'Encourage 15 minutes of movement', done: false },
  ],
  Tuesday: [
    { id: 201, text: 'Do one screen-free activity together', done: false },
    { id: 202, text: 'Keep a calm bedtime cue', done: false },
  ],
  Wednesday: [
    { id: 301, text: 'Repeat the after-school snack routine', done: false },
    { id: 302, text: 'Offer water before snacks', done: false },
  ],
  Thursday: [
    { id: 401, text: 'Encourage active play before screens', done: false },
    { id: 402, text: 'Use one predictable routine cue', done: false },
  ],
  Friday: [
    { id: 501, text: 'Celebrate one healthy win from the week', done: false },
    { id: 502, text: 'Choose one easy family meal together', done: false },
  ],
  Saturday: [
    { id: 601, text: 'Do one family movement activity', done: false },
    { id: 602, text: 'Keep one healthy snack visible', done: false },
  ],
  Sunday: [
    { id: 701, text: 'Review the week and reset for Monday', done: false },
    { id: 702, text: 'Plan one routine goal for next week', done: false },
  ],
}

const defaultProgressItems = [
  { id: 1, text: 'Healthy snack prepared', done: false, custom: false },
  { id: 2, text: 'Active play completed', done: false, custom: false },
  { id: 3, text: 'Bedtime routine followed', done: false, custom: false },
  { id: 4, text: 'Screen-free family time completed', done: false, custom: false },
]

const childName = computed(() => state.childName || 'Your child')
const nextAction = computed(
  () => state.nextAction || 'Take the parent quiz to unlock a personalized next action.'
)
const mission = computed(() => state.mission || 'Complete one healthy habit win together today.')
const streakDays = computed(() => state.streakDays || 0)
const streakProgress = computed(() => Math.min((streakDays.value / 7) * 100, 100))

const concernSummary = computed(() =>
  state.concerns?.length ? state.concerns.join(', ') : 'Nutrition, activity, sleep, and routine'
)

const habitSummary = computed(() =>
  state.habits?.length ? state.habits.join(', ') : 'Balanced meals and bedtime consistency'
)

const resolvedDailyPlan = computed(() => {
  const existing = state.dailyPlan && Object.keys(state.dailyPlan).length ? state.dailyPlan : defaultDailyPlan
  return orderedDays.reduce((acc, day) => {
    acc[day] = existing[day] || []
    return acc
  }, {})
})

const resolvedProgressItems = computed(() =>
  state.progressItems?.length ? state.progressItems : defaultProgressItems
)

const todayName = computed(() =>
  new Date().toLocaleDateString('en-AU', { weekday: 'long' })
)

const todayTasks = computed(() => resolvedDailyPlan.value[todayName.value] || [])

const completedTodayCount = computed(() =>
  todayTasks.value.filter(task => task.done).length
)

const todayProgress = computed(() =>
  todayTasks.value.length
    ? Math.round((completedTodayCount.value / todayTasks.value.length) * 100)
    : 0
)

const completedProgressItems = computed(() =>
  resolvedProgressItems.value.filter(item => item.done).length
)

const progressCompletion = computed(() =>
  resolvedProgressItems.value.length
    ? Math.round((completedProgressItems.value / resolvedProgressItems.value.length) * 100)
    : 0
)

const weeklyNarrative = computed(() => {
  if (state.concerns?.includes('Sleep consistency') || state.concerns?.includes('Bedtime feels inconsistent')) {
    return `${childName.value} may struggle with energy and mood if sleep stays inconsistent. Prioritising bedtime structure can improve appetite, attention, and after-school behaviour.`
  }
  if (state.concerns?.includes('Nutrition') || state.concerns?.includes('My child snacks too often')) {
    return `${childName.value} needs consistent fuel through the day. Better snack quality can stabilise energy, reduce irritability, and support healthy growth habits.`
  }
  return `${childName.value}'s plan is focused on consistency. One repeated healthy action each day is the strongest predictor of long-term habit success.`
})

const riskNarrative = computed(() => {
  if (
    state.concerns?.includes('Routine battles') ||
    state.concerns?.includes('Our family routine feels hard to manage')
  ) {
    return 'Daily friction increases and healthy habits become harder to sustain.'
  }

  if (
    state.concerns?.includes('Physical activity') ||
    state.concerns?.includes('My child is not active enough')
  ) {
    return 'Lower movement can affect mood regulation and sleep quality.'
  }

  return 'Inconsistent habits reduce progress and make routines harder to maintain.'
})

const winNarrative = computed(() => {
  if (state.concerns?.includes('Nutrition') || state.concerns?.includes('My child snacks too often')) {
    return 'Higher energy and fewer snack-related conflicts after school.'
  }
  if (state.concerns?.includes('Sleep consistency') || state.concerns?.includes('Bedtime feels inconsistent')) {
    return 'Calmer evenings and more predictable morning routines.'
  }
  return 'Better consistency with less parent-child conflict across the day.'
})

const weeklyProgress = computed(() => {
  return orderedDays.map(day => {
    const tasks = resolvedDailyPlan.value[day] || []
    const completed = tasks.filter(task => task.done).length
    const value = tasks.length ? Math.round((completed / tasks.length) * 100) : 0
    return {
      label: day.slice(0, 3),
      fullLabel: day,
      value,
      completed,
      total: tasks.length,
      tasks,
    }
  })
})

const selectedDay = computed(() => {
  return (
    weeklyProgress.value.find(day => day.label === selectedDayLabel.value) ||
    weeklyProgress.value[0]
  )
})

const weeklyAverage = computed(() => {
  const total = weeklyProgress.value.reduce((sum, item) => sum + item.value, 0)
  return Math.round(total / weeklyProgress.value.length)
})

const confettiPieces = computed(() =>
  Array.from({ length: 14 }, (_, i) => ({
    id: i,
    style: {
      left: `${6 + i * 6.2}%`,
      animationDelay: `${i * 0.05}s`,
      transform: `rotate(${i * 17}deg)`,
    },
  }))
)

async function toggleTodayTask(taskId) {
  const updatedDailyPlan = {
    ...resolvedDailyPlan.value,
    [todayName.value]: resolvedDailyPlan.value[todayName.value].map(task =>
      task.id === taskId ? { ...task, done: !task.done } : task
    ),
  }

  const updatedState = {
    ...state,
    dailyPlan: updatedDailyPlan,
  }

  savePlan(updatedState)

  try {
    await persistDashboardUpdate(updatedState)
  } catch (error) {
    console.error('Failed to persist today task update', error)
  }
}

async function toggleProgressItem(itemId) {
  const updatedItems = resolvedProgressItems.value.map(item =>
    item.id === itemId ? { ...item, done: !item.done } : item
  )

  const updatedState = {
    ...state,
    progressItems: updatedItems,
  }

  savePlan(updatedState)

  try {
    await persistDashboardUpdate(updatedState)
  } catch (error) {
    console.error('Failed to persist progress item update', error)
  }
}

async function addProgressItem() {
  const value = newProgressItem.value.trim()
  if (!value) return

  const newItem = {
    id: Date.now(),
    text: value,
    done: false,
    custom: true,
  }

  const updatedState = {
    ...state,
    progressItems: [...resolvedProgressItems.value, newItem],
  }

  savePlan(updatedState)
  newProgressItem.value = ''

  try {
    const result = await persistDashboardUpdate(updatedState)
    console.log('Custom progress item persisted:', result)
  } catch (error) {
    console.error('Failed to persist custom progress item', error)
    alert(`Failed to save custom item to database: ${error.message}`)
  }
}

async function completeMission() {
  const updatedState = {
    ...state,
    streakDays: (state.streakDays || 0) + 1,
  }

  savePlan(updatedState)

  try {
    await persistDashboardUpdate(updatedState)
  } catch (error) {
    console.error('Failed to persist mission completion', error)
  }

  showCelebration.value = true
  window.setTimeout(() => {
    showCelebration.value = false
  }, 1800)
}

async function persistDashboardUpdate(updatedState) {
  const username = updatedState.username || state.username
  if (!username) {
    throw new Error('Missing username for dashboard persistence')
  }

  const response = await fetch(
    `${import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL}/parent-profiles/${encodeURIComponent(username)}`,
    {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dailyPlan: updatedState.dailyPlan ?? state.dailyPlan,
        progressItems: updatedState.progressItems ?? state.progressItems,
        streakDays: updatedState.streakDays ?? state.streakDays ?? 0,
        nextAction: updatedState.nextAction ?? state.nextAction,
        mission: updatedState.mission ?? state.mission,
      }),
    }
  )

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(data.error || `Dashboard update failed with status ${response.status}`)
  }

  return data
}
</script>

<style scoped>
:global(*) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #f6f3ee;
  color: #171717;
  -webkit-font-smoothing: antialiased;
}

.dashboard-page {
  min-height: 100vh;
  background:
    radial-gradient(circle at 14% 18%, rgba(109, 195, 216, 0.18), transparent 34%),
    radial-gradient(circle at 84% 14%, rgba(116, 130, 255, 0.16), transparent 34%),
    radial-gradient(circle at 86% 78%, rgba(255, 176, 132, 0.16), transparent 36%),
    linear-gradient(145deg, #eef4ff 0%, #f7f1ff 46%, #fff5ee 100%);
  position: relative;
  overflow-x: clip;
}

.dashboard-page::before,
.dashboard-page::after {
  content: "";
  position: fixed;
  z-index: 0;
  pointer-events: none;
  border-radius: 999px;
  filter: blur(56px);
  opacity: 0.42;
}

.dashboard-page::before {
  width: 420px;
  height: 420px;
  top: -120px;
  left: -150px;
  background: radial-gradient(circle, rgba(116, 203, 225, 0.46), rgba(116, 203, 225, 0));
}

.dashboard-page::after {
  width: 460px;
  height: 460px;
  top: 40vh;
  right: -180px;
  background: radial-gradient(circle, rgba(147, 146, 255, 0.34), rgba(147, 146, 255, 0));
}

.container {
  width: min(1180px, calc(100% - 48px));
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(246, 243, 238, 0.88);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(88, 109, 166, 0.12);
}

.header-row {
  min-height: 78px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}

.brand {
  text-decoration: none;
  color: #18233b;
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.04em;
}

.nav {
  display: flex;
  align-items: center;
  gap: 28px;
}

.nav-link,
.nav a {
  text-decoration: none;
  color: #4b556f;
  font-size: 0.95rem;
  font-weight: 500;
}

.nav-link:hover,
.nav a:hover {
  color: #18233b;
}

.header-btn {
  text-decoration: none;
  min-height: 44px;
  padding: 0 18px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.92rem;
  font-weight: 700;
  border: 1px solid rgba(88, 109, 166, 0.16);
  color: #18233b;
  background: rgba(255, 255, 255, 0.72);
}

.header-btn:hover {
  background: rgba(255, 255, 255, 0.9);
}

.dashboard-top {
  padding: 40px 0 24px;
  position: relative;
  z-index: 1;
}

.top-shell {
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 24px;
  align-items: start;
}

.eyebrow,
.section-label,
.card-kicker,
.chart-label {
  margin: 0 0 12px;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-weight: 800;
  color: #6f6a86;
}

.top-copy h1,
.section-head h2,
.summary-card h2,
.chart-card h3,
.glass-card h3,
.chart-detail-card h4 {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  line-height: 0.96;
  letter-spacing: -0.05em;
  font-weight: 700;
  color: #18233b;
}

.top-copy h1 {
  font-size: clamp(2.8rem, 5vw, 4.6rem);
}

.section-head h2 {
  font-size: clamp(2rem, 3vw, 2.9rem);
}

.summary-card h2,
.chart-card h3,
.glass-card h3,
.chart-detail-card h4 {
  font-size: 1.5rem;
  line-height: 1.05;
}

.top-text,
.summary-text,
.info-copy,
.today-progress-copy,
.detail-list,
.task-item span,
.weekday-list,
.chart-summary,
.chart-detail-text {
  color: #5f5a74;
  line-height: 1.68;
}

.top-text {
  margin: 14px 0 0;
  max-width: 42rem;
  font-size: 1rem;
}

.top-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 22px;
}

.top-pills span {
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.74);
  border: 1px solid rgba(88, 109, 166, 0.12);
  font-size: 0.9rem;
  font-weight: 700;
  color: #4f4a66;
}

.top-side {
  display: grid;
  gap: 14px;
}

.summary-card {
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(88, 109, 166, 0.12);
  border-radius: 28px;
  padding: 22px;
  position: relative;
  backdrop-filter: blur(8px);
  box-shadow: 0 16px 34px rgba(57, 73, 114, 0.08);
}

.mission-card {
  background:
    radial-gradient(circle at top right, rgba(124, 58, 237, 0.12), transparent 34%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.82), rgba(246, 242, 255, 0.92));
}

.summary-card p {
  margin: 10px 0 0;
}

.mission-progress-top {
  margin-top: 16px;
  color: #4f4a66;
  font-size: 0.95rem;
}

.mission-progress-top strong {
  color: #18233b;
}

.progress-track {
  width: 100%;
  height: 10px;
  border-radius: 999px;
  background: #ddd7ef;
  overflow: hidden;
  margin-top: 14px;
}

.progress-track.large {
  height: 12px;
  margin: 14px 0 20px;
}

.progress-fill {
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #3649f4 0%, #7c3aed 100%);
}

.pill-btn {
  text-decoration: none;
  border: none;
  cursor: pointer;
  padding: 14px 22px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.95rem;
}

.pill-btn.dark {
  margin-top: 16px;
  background: linear-gradient(135deg, #171717 0%, #3649f4 100%);
  color: #fff;
  box-shadow: 0 12px 24px rgba(58, 73, 170, 0.18);
}

.pill-btn.dark:hover {
  transform: translateY(-1px);
  opacity: 0.96;
}

.today-plan-section,
.weekly-plan-section,
.tracker-section,
.chart-section,
.overview-section {
  padding: 0 0 28px;
  position: relative;
  z-index: 1;
}

.section-head {
  margin-bottom: 18px;
}

.section-head.compact {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.today-plan-grid,
.tracker-grid,
.overview-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 20px;
}

.overview-grid.single {
  grid-template-columns: 1fr;
}

.weekly-days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 14px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.82);
  border: 1px solid rgba(88, 109, 166, 0.12);
  border-radius: 26px;
  padding: 22px;
  backdrop-filter: blur(8px);
  box-shadow: 0 14px 30px rgba(57, 73, 114, 0.08);
}

.today-focus-label {
  margin: 0 0 8px;
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #6f6a86;
}

.task-list {
  display: grid;
  gap: 10px;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 16px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.7), rgba(246, 242, 255, 0.95));
  border: 1px solid rgba(88, 109, 166, 0.08);
}

.task-item input {
  width: 18px;
  height: 18px;
  accent-color: #5d6df5;
  flex-shrink: 0;
}

.task-item.done {
  opacity: 0.72;
}

.task-item.done span {
  text-decoration: line-through;
}

.detail-list {
  margin: 16px 0 0;
  padding-left: 18px;
}

.detail-list li {
  margin-bottom: 8px;
}

.weekday-card {
  padding: 18px;
}

.weekday-card.active {
  border: 2px solid rgba(93, 109, 245, 0.48);
  box-shadow: 0 18px 32px rgba(93, 109, 245, 0.14);
}

.weekday-card h3 {
  margin-bottom: 10px;
  font-size: 1.08rem;
}

.weekday-list {
  margin: 0;
  padding-left: 18px;
  font-size: 0.93rem;
}

.weekday-list li {
  margin-bottom: 8px;
}

.tracker-badge {
  min-width: 54px;
  height: 54px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #3649f4 0%, #7c3aed 100%);
  color: #fff;
  font-weight: 800;
  box-shadow: 0 10px 24px rgba(80, 74, 220, 0.22);
}

.custom-item-form {
  display: grid;
  gap: 12px;
}

.custom-input {
  width: 100%;
  min-height: 52px;
  border-radius: 16px;
  border: 1px solid rgba(88, 109, 166, 0.14);
  padding: 0 16px;
  font: inherit;
  background: rgba(255, 255, 255, 0.95);
  outline: none;
}

.custom-input:focus {
  border-color: #5d6df5;
  box-shadow: 0 0 0 4px rgba(93, 109, 245, 0.12);
}

.chart-card {
  padding: 22px;
}

.chart-header {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.chart-summary {
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(88, 109, 166, 0.1);
  font-size: 0.9rem;
  font-weight: 800;
}

.chart-interactive-wrap {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 20px;
  align-items: stretch;
}

.bar-chart {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 14px;
  align-items: end;
  min-height: 250px;
}

.interactive-bar {
  border: none;
  background: transparent;
  padding: 0;
  cursor: pointer;
  transition: transform 0.18s ease;
}

.interactive-bar:hover {
  transform: translateY(-4px);
}

.interactive-bar.active .bar-track {
  box-shadow: 0 0 0 2px rgba(93, 109, 245, 0.3);
}

.interactive-bar.active .bar-fill {
  filter: brightness(0.96);
}

.bar-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.bar-value,
.bar-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: #5f5a74;
}

.bar-track {
  width: 100%;
  max-width: 44px;
  height: 180px;
  border-radius: 999px;
  background: #ddd7ef;
  overflow: hidden;
  display: flex;
  align-items: end;
  transition: box-shadow 0.18s ease, transform 0.18s ease;
}

.bar-fill {
  width: 100%;
  border-radius: 999px;
  background: linear-gradient(180deg, #8ea2ff 0%, #5d6df5 48%, #7c3aed 100%);
  transition: height 0.3s ease;
}

.chart-detail-card {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.7), rgba(246, 242, 255, 0.95));
  border: 1px solid rgba(88, 109, 166, 0.08);
  padding: 18px;
  border-radius: 20px;
}

.chart-detail-card h4 {
  font-size: 1.32rem;
  margin-top: 2px;
}

.chart-detail-score {
  margin: 10px 0 0;
  font-size: 1.35rem;
  font-weight: 800;
  color: #5d6df5;
}

.chart-detail-text {
  margin: 8px 0 0;
}

.chart-detail-list {
  margin: 14px 0 0;
  padding-left: 18px;
  color: #5f5a74;
  line-height: 1.6;
}

.chart-detail-list li {
  margin-bottom: 8px;
}

.done-text {
  text-decoration: line-through;
  opacity: 0.7;
}

.empty-state {
  margin: 0;
  font-style: italic;
  color: #6f6a86;
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
  background: linear-gradient(180deg, #8ea2ff 0%, #f0c98d 100%);
  animation: confettiDrop 1.2s ease forwards;
}

@keyframes confettiDrop {
  0% {
    opacity: 0;
    transform: translateY(0) rotate(0deg);
  }
  10% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: translateY(220px) rotate(220deg);
  }
}

@media (max-width: 1100px) {
  .top-shell,
  .today-plan-grid,
  .tracker-grid,
  .overview-grid,
  .chart-interactive-wrap {
    grid-template-columns: 1fr;
  }

  .weekly-days-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 760px) {
  .nav {
    display: none;
  }

  .header-row {
    flex-wrap: wrap;
    padding: 14px 0;
  }

  .header-btn {
    width: 100%;
  }

  .container {
    width: calc(100% - 24px);
  }

  .weekly-days-grid {
    grid-template-columns: 1fr;
  }

  .bar-chart {
    gap: 8px;
  }

  .bar-track {
    max-width: 34px;
    height: 140px;
  }

  .pill-btn {
    width: 100%;
  }

  .summary-card,
  .glass-card,
  .chart-detail-card {
    padding: 20px;
    border-radius: 22px;
  }
}
</style>