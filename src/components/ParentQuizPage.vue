<template>
  <div class="quiz-page">
    <header class="site-header">
      <div class="container header-row">
        <RouterLink to="/" class="brand">HealthyKids</RouterLink>

        <nav class="nav" aria-label="Primary">
          <RouterLink to="/" class="nav-link">Home</RouterLink>
          <RouterLink to="/parent-entry" class="nav-link">Parent access</RouterLink>
          <a href="#quiz-form" class="nav-link">Quiz</a>
        </nav>

        <RouterLink to="/parent-entry" class="header-btn light-btn">Back</RouterLink>
      </div>
    </header>

    <main>
      <section class="quiz-top">
        <div class="container">
          <div class="intro-shell">
            <div class="intro-copy">
              <p class="step-kicker">Step 2 of 3</p>
              <h1>Build a plan</h1>
            </div>

            <div class="journey-card">
              <p class="journey-label">Journey</p>
              <div class="journey-steps">
                <div class="journey-step complete">
                  <span>1</span>
                  <small>Parent access</small>
                </div>
                <div class="journey-line"></div>
                <div class="journey-step active">
                  <span>2</span>
                  <small>Quiz</small>
                </div>
                <div class="journey-line"></div>
                <div class="journey-step">
                  <span>3</span>
                  <small>Dashboard</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="quiz-form" class="quiz-form-section">
        <div class="container">
          <div class="form-shell">
            <div class="form-head">
              <p class="wizard-step">Step {{ currentStep + 1 }} of {{ steps.length }}</p>
              <h2>{{ activeStep.title }}</h2>
              <p class="wizard-subtitle">{{ activeStep.subtitle }}</p>
            </div>

            <div v-if="currentStep === 0" class="form-grid">
              <div class="form-group">
                <label for="username">Username</label>
                <input id="username" v-model.trim="form.username" placeholder="Enter your username" />
              </div>

              <div class="form-group">
                <label for="child-age">Child age range</label>
                <select id="child-age" v-model="form.ageRange">
                  <option disabled value="">Select age range</option>
                  <option>5-7 years</option>
                  <option>8-10 years</option>
                  <option>11-12 years</option>
                </select>
              </div>

              <div class="form-group full-row">
                <label for="routine-type">How would you describe your weekly family routine?</label>
                <select id="routine-type" v-model="form.routineType">
                  <option disabled value="">Choose one</option>
                  <option>Mostly structured</option>
                  <option>Busy and sometimes inconsistent</option>
                  <option>Very busy and hard to manage</option>
                </select>
              </div>
            </div>

            <div v-if="currentStep === 1" class="form-grid">
              <div class="form-group full-row">
                <label>Which everyday habits need the most support right now?</label>
                <div class="chip-grid">
                  <button
                    v-for="habit in habitOptions"
                    :key="habit"
                    type="button"
                    class="option-chip"
                    :class="{ selected: form.habits.includes(habit) }"
                    @click="toggleSelection(form.habits, habit)"
                  >
                    {{ habit }}
                  </button>
                </div>
              </div>

              <div class="form-group full-row">
                <label for="struggle">What feels hardest in daily family life right now?</label>
                <textarea
                  id="struggle"
                  v-model.trim="form.struggle"
                  rows="5"
                  placeholder="For example: my child wants screens after school, healthy meals are difficult on busy days, or bedtime becomes a battle."
                ></textarea>
              </div>
            </div>

            <div v-if="currentStep === 2" class="form-grid">
              <div class="form-group full-row">
                <label>What are you most worried about right now?</label>
                <div class="chip-grid">
                  <button
                    v-for="concern in concernOptions"
                    :key="concern"
                    type="button"
                    class="option-chip"
                    :class="{ selected: form.concerns.includes(concern) }"
                    @click="toggleSelection(form.concerns, concern)"
                  >
                    {{ concern }}
                  </button>
                </div>
              </div>

              <div class="form-group">
                <label for="confidence">How supported do you currently feel?</label>
                <select id="confidence" v-model="form.confidence">
                  <option disabled value="">Choose one</option>
                  <option>I feel confident</option>
                  <option>I know what to do but struggle to stay consistent</option>
                  <option>I need simple guidance and structure</option>
                </select>
              </div>

              <div class="form-group">
                <label for="support-style">What type of support would help most?</label>
                <select id="support-style" v-model="form.supportStyle">
                  <option disabled value="">Choose one</option>
                  <option>Small daily actions</option>
                  <option>Weekly family plan</option>
                  <option>Visual tips and reminders</option>
                  <option>Easy routines with less conflict</option>
                </select>
              </div>
            </div>

            <div v-if="currentStep === 3" class="preview-stack">
              <article class="preview-card">
                <p class="card-kicker">Plan preview</p>
                <h3>Your family plan</h3>

                <ul class="preview-list">
                  <li><strong>Username:</strong> {{ form.username }}</li>
                  <li><strong>Top habits to support:</strong> {{ form.habits.join(', ') }}</li>
                  <li><strong>Main concerns:</strong> {{ form.concerns.join(', ') }}</li>
                  <li><strong>Support style:</strong> {{ form.supportStyle }}</li>
                  <li><strong>Routine context:</strong> {{ form.routineType }}</li>
                </ul>

                <p class="preview-note">
                  Your answers will generate a saved parent dashboard with practical next steps, a
                  weekly plan, and trackable tasks.
                </p>
              </article>
            </div>

            <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>

            <div class="form-actions wizard-actions">
              <button
                v-if="currentStep > 0"
                type="button"
                class="outline-btn"
                @click="currentStep -= 1"
              >
                Back
              </button>

              <button
                v-if="currentStep < steps.length - 1"
                type="button"
                class="soft-brown-btn"
                @click="goNext"
              >
                Continue
              </button>

              <button
                v-else
                type="button"
                class="soft-brown-btn"
                @click="submitQuiz"
              >
                Save and generate my family plan
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'

const router = useRouter()
const { state, savePlan } = useFamilyPlanStore()

const form = reactive({
  username: state.username || '',
  ageRange: '',
  routineType: '',
  habits: [],
  concerns: [],
  struggle: '',
  confidence: '',
  supportStyle: '',
})

const steps = [
  {
    title: 'Family basics',
    subtitle: 'Tell us who this plan is for and what daily life looks like.',
  },
  {
    title: 'Everyday habits',
    subtitle: 'Identify which habits need the most support right now.',
  },
  {
    title: 'Parent worries and support',
    subtitle: 'Capture your concerns and what kind of guidance would help most.',
  },
  {
    title: 'Review your plan',
    subtitle: 'Check your answers before generating your family dashboard.',
  },
]

const habitOptions = [
  'Balanced meals',
  'Healthier snacks',
  'Daily movement',
  'Sleep routine',
  'Morning routine',
  'After-school routine',
  'Screen time balance',
]

const concernOptions = [
  'My child is not active enough',
  'My child prefers screens over outdoor activity',
  'My child snacks too often',
  'Healthy meals are hard on busy days',
  'Bedtime feels inconsistent',
  'Our family routine feels hard to manage',
  'I am worried about weight or long-term health',
  'I am not sure what the right approach is',
]

const currentStep = ref(0)
const errorMessage = ref('')

const activeStep = computed(() => steps[currentStep.value])

function toggleSelection(list, value) {
  const index = list.indexOf(value)
  if (index === -1) {
    list.push(value)
    return
  }
  list.splice(index, 1)
}

function validateStep() {
  errorMessage.value = ''

  if (currentStep.value === 0) {
    if (!form.username || !form.ageRange || !form.routineType) {
      errorMessage.value = 'Please complete all family basics fields before continuing.'
      return false
    }
  }

  if (currentStep.value === 1) {
    if (!form.habits.length || !form.struggle) {
      errorMessage.value =
        'Please select at least one habit and describe what feels hardest right now.'
      return false
    }
  }

  if (currentStep.value === 2) {
    if (!form.concerns.length || !form.confidence || !form.supportStyle) {
      errorMessage.value = 'Please complete all parent support questions.'
      return false
    }
  }

  return true
}

function goNext() {
  if (!validateStep()) return
  currentStep.value += 1
}

function uniqueStrings(values) {
  return [...new Set(values.filter(Boolean))]
}

function buildTaskPool() {
  const tasks = []
  const trackerItems = []

  if (form.habits.includes('Balanced meals')) {
    tasks.push(
      'Include one fruit or vegetable in one main meal today',
      "Plan tomorrow's lunch or dinner before 6 pm",
      'Offer water with the main meal'
    )
    trackerItems.push(
      'Fruit or vegetable included in a meal',
      'Meal planned ahead',
      'Water offered at mealtime'
    )
  }

  if (form.habits.includes('Healthier snacks')) {
    tasks.push(
      'Prepare one healthy after-school snack before pickup or school finish',
      'Keep one healthy snack visible and easy to reach',
      'Swap one processed snack for fruit, yoghurt, or nuts if suitable'
    )
    trackerItems.push(
      'Healthy after-school snack prepared',
      'Healthy snack made visible',
      'One snack swap completed'
    )
  }

  if (form.habits.includes('Daily movement')) {
    tasks.push(
      'Do 15-20 minutes of movement before screen time',
      'Add one family movement break today',
      'Encourage outdoor or active play for a short block'
    )
    trackerItems.push(
      '15 minutes of movement completed',
      'Family movement break completed',
      'Outdoor or active play completed'
    )
  }

  if (form.habits.includes('Sleep routine')) {
    tasks.push(
      'Use one calm bedtime cue at the same time tonight',
      'Start wind-down 20 minutes earlier than usual',
      'Reduce stimulating screen use before bed'
    )
    trackerItems.push(
      'Bedtime cue followed',
      'Earlier wind-down started',
      'Pre-bed screen use reduced'
    )
  }

  if (form.habits.includes('Morning routine')) {
    tasks.push(
      'Prepare one school item the night before',
      'Set one simple morning order: wake, dress, breakfast',
      'Use one repeated morning reminder instead of multiple prompts'
    )
    trackerItems.push(
      'School item prepared the night before',
      'Morning order followed',
      'Single reminder used in the morning'
    )
  }

  if (form.habits.includes('After-school routine')) {
    tasks.push(
      'Use one predictable after-school transition cue',
      'Offer snack first, then move into the next activity',
      'Keep the first 20 minutes after school calm and structured'
    )
    trackerItems.push(
      'After-school transition cue used',
      'Snack-first routine followed',
      'Calm first 20 minutes maintained'
    )
  }

  if (form.habits.includes('Screen time balance')) {
    tasks.push(
      'Delay screens until after one healthy task is completed',
      'Create one short screen-free family block today',
      'Use a clear end point for screen time'
    )
    trackerItems.push(
      'Screen delayed until after a healthy task',
      'Screen-free family block completed',
      'Screen end point followed'
    )
  }

  if (form.concerns.includes('My child prefers screens over outdoor activity')) {
    tasks.push(
      'Offer one active choice before any device is turned on',
      'Pair movement with something enjoyable like music or a game'
    )
    trackerItems.push(
      'Active choice offered before screen time',
      'Movement paired with something enjoyable'
    )
  }

  if (form.concerns.includes('My child snacks too often')) {
    tasks.push(
      'Set one planned snack time instead of frequent grazing',
      'Use a portioned snack instead of eating from a large pack'
    )
    trackerItems.push(
      'Planned snack time used',
      'Portioned snack served'
    )
  }

  if (form.concerns.includes('Healthy meals are hard on busy days')) {
    tasks.push(
      'Choose one simple low-effort meal for today',
      "Decide tonight's meal before the busy part of the day begins"
    )
    trackerItems.push(
      'Simple low-effort meal used',
      'Meal decided early'
    )
  }

  if (form.concerns.includes('Bedtime feels inconsistent')) {
    tasks.push(
      'Keep bedtime within the same 20-minute window tonight',
      'Repeat the same final bedtime activity tonight'
    )
    trackerItems.push(
      'Bedtime kept within the target window',
      'Same final bedtime activity repeated'
    )
  }

  if (form.concerns.includes('Our family routine feels hard to manage')) {
    tasks.push(
      'Focus on just one habit today instead of trying to fix everything',
      'Use one visible cue such as a note, bottle, or snack setup'
    )
    trackerItems.push(
      'One-habit focus maintained',
      'Visible routine cue used'
    )
  }

  if (form.supportStyle === 'Visual tips and reminders') {
    tasks.push('Place one visible reminder where the habit needs to happen')
    trackerItems.push('Visible reminder placed')
  }

  if (form.supportStyle === 'Easy routines with less conflict') {
    tasks.push('Use one calm instruction instead of repeated reminders')
    trackerItems.push('Calm single instruction used')
  }

  if (form.supportStyle === 'Small daily actions') {
    tasks.push('Choose only one non-negotiable healthy task for today')
    trackerItems.push('One daily action completed')
  }

  if (form.supportStyle === 'Weekly family plan') {
    tasks.push("Review tomorrow's task before the day ends")
    trackerItems.push('Next day task reviewed')
  }

  if (form.routineType === 'Very busy and hard to manage') {
    tasks.push(
      "Pick the easiest possible version of today's task",
      'Prep one thing early to reduce pressure later'
    )
    trackerItems.push(
      'Easiest version of the task completed',
      'One thing prepped early'
    )
  }

  if (form.routineType === 'Busy and sometimes inconsistent') {
    tasks.push('Repeat the same healthy cue at the same time today')
    trackerItems.push('Healthy cue repeated at the same time')
  }

  return {
    tasks: uniqueStrings(tasks),
    trackerItems: uniqueStrings(trackerItems),
  }
}

function buildDailyPlan(taskPool) {
  const pool = taskPool.tasks.length
    ? taskPool.tasks
    : [
        'Complete one healthy task together today',
        'Repeat one routine cue at the same time',
        'Celebrate one small effort',
      ]

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

  return days.reduce((acc, day, dayIndex) => {
    const firstTask = pool[dayIndex % pool.length]
    const secondTask = pool[(dayIndex + 2) % pool.length]

    acc[day] = [
      {
        id: Number(`${dayIndex + 1}01`),
        text: firstTask,
        done: false,
      },
      {
        id: Number(`${dayIndex + 1}02`),
        text: secondTask,
        done: false,
      },
    ]
    return acc
  }, {})
}

function buildProgressItems(taskPool) {
  const items = taskPool.trackerItems.length
    ? taskPool.trackerItems
    : [
        'One healthy action completed',
        'One routine cue repeated',
        'One small family win noticed',
      ]

  return items.slice(0, 8).map((text, index) => ({
    id: index + 1,
    text,
    done: false,
    custom: false,
  }))
}

function createRecommendations() {
  const recommendations = []

  if (form.habits.includes('Healthier snacks') || form.concerns.includes('My child snacks too often')) {
    recommendations.push({
      title: 'Snack support',
      description:
        'Plan one visible, portioned healthy snack each day so snacking becomes more predictable and lower in stress.',
    })
  }

  if (form.habits.includes('Daily movement') || form.concerns.includes('My child is not active enough')) {
    recommendations.push({
      title: 'Movement support',
      description:
        'Use the after-school period as the main movement window because short, consistent activity is easier to sustain than big exercise goals.',
    })
  }

  if (form.habits.includes('Sleep routine') || form.concerns.includes('Bedtime feels inconsistent')) {
    recommendations.push({
      title: 'Sleep support',
      description:
        'Focus on one repeatable bedtime cue and a consistent wind-down start time instead of trying to redesign the whole evening at once.',
    })
  }

  if (form.habits.includes('Screen time balance') || form.concerns.includes('My child prefers screens over outdoor activity')) {
    recommendations.push({
      title: 'Screen balance support',
      description:
        'Link screen access to one healthy action first, so screens become part of a routine instead of the starting point.',
    })
  }

  if (form.concerns.includes('Healthy meals are hard on busy days')) {
    recommendations.push({
      title: 'Busy-day meals',
      description:
        'Choose simpler meals ahead of time on busy days so healthy eating feels manageable rather than idealistic.',
    })
  }

  if (form.supportStyle === 'Visual tips and reminders') {
    recommendations.push({
      title: 'Reminder strategy',
      description:
        'Use visible cues such as snack setup, water bottles, or bedtime reminders to reduce the need for repeated prompting.',
    })
  }

  if (recommendations.length < 3) {
    recommendations.push(
      {
        title: "This week's first step",
        description: `Start with one small ${form.habits[0]?.toLowerCase() || 'healthy routine'} action each day and keep the goal realistic.`,
      },
      {
        title: 'Before the hard moment',
        description: `Because "${form.struggle}", set one clear cue before the difficult time of day begins.`,
      }
    )
  }

  return recommendations.slice(0, 4)
}

function createNextAction(taskPool) {
  return taskPool.tasks[0] || 'Complete one healthy family habit today.'
}

function createMission() {
  if (form.habits.includes('Daily movement')) {
    return 'Complete one short movement activity today before screen time.'
  }

  if (form.habits.includes('Healthier snacks')) {
    return 'Prepare one healthy snack choice today and make it the easy option.'
  }

  if (form.habits.includes('Sleep routine')) {
    return 'Use one calm bedtime cue tonight and keep it consistent.'
  }

  if (form.habits.includes('Screen time balance')) {
    return 'Keep one short screen-free block today before devices are used.'
  }

  return 'Complete one healthy habit win today.'
}

async function submitQuiz() {
  if (!validateStep()) return

  const taskPool = buildTaskPool()
  const recommendations = createRecommendations()
  const dailyPlan = buildDailyPlan(taskPool)
  const progressItems = buildProgressItems(taskPool)
  const nextAction = createNextAction(taskPool)
  const mission = createMission()

  const payload = {
    ...form,
    recommendations,
    dailyPlan,
    progressItems,
    nextAction,
    mission,
    streakDays: state.streakDays || 0,
  }

  try {
    const response = await fetch(
      `${import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL}/test/parent-profiles`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      }
    )

    const data = await response.json()

    if (response.status === 409) {
      errorMessage.value = 'That username is already taken. Please go back and choose another one.'
      return
    }

    if (!response.ok) {
      throw new Error(data.error || 'Save failed')
    }

    savePlan(payload)
    router.push('/parent-dashboard')
  } catch (error) {
    errorMessage.value = 'Something went wrong while saving your plan. Please try again.'
    console.error(error)
  }
}
</script>

<style scoped>
:global(*) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  background: #ece7df;
  font-family: 'Montserrat', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  -webkit-font-smoothing: antialiased;
  color: #2f2a26;
}

.quiz-page {
  min-height: 100vh;
  background: #ece7df;
}

.container {
  width: min(980px, calc(100% - 48px));
  margin: 0 auto;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(236, 231, 223, 0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(47, 42, 38, 0.12);
}

.header-row {
  min-height: 82px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}

.brand {
  text-decoration: none;
  color: #2f2a26;
  /* font-size: 1.75rem; */
  font-weight: 900;
}

.nav {
  display: flex;
  align-items: center;
  gap: 28px;
}

.nav a,
.nav-link {
  text-decoration: none;
  color: #3e3631;
  font-size: 0.96rem;
  font-weight: 500;
}

.header-btn {
  text-decoration: none;
  min-height: 46px;
  padding: 0 18px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.94rem;
  font-weight: 700;
  border: 1px solid #3b312b;
  color: #3b312b;
  background: transparent;
}

.quiz-top {
  padding: 24px 0 14px;
}

.intro-shell {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 20px;
  align-items: start;
}

.intro-copy h1,
.form-head h2 {
  margin: 0;
  line-height: 0.96;
  font-weight: 800;
  color: #2f2a26;
}

.step-kicker,
.card-kicker,
.journey-label,
.wizard-step {
  margin: 0 0 12px;
  font-size: 0.78rem;
  text-transform: uppercase;
  font-weight: 800;
  color: #6c6258;
}

.intro-text,
.wizard-subtitle,
.form-group label,
.preview-note,
.preview-card li {
  font-size: 0.98rem;
  line-height: 1.65;
  color: #5e5248;
}

.intro-text {
  margin: 10px 0 0;
  max-width: 32rem;
}

.journey-card {
  background: #f3eee8;
  border: 1px solid rgba(47, 42, 38, 0.12);
  padding: 18px;
}

.journey-steps {
  display: flex;
  align-items: center;
  gap: 12px;
}

.journey-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 72px;
}

.journey-step span {
  width: 40px;
  height: 40px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  background: #e5ddd3;
  color: #3b312b;
  font-weight: 800;
}

.journey-step.complete span,
.journey-step.active span {
  background: #b2805c;
  color: #fff;
}

.journey-step small {
  font-size: 0.78rem;
  color: #5e5248;
  font-weight: 700;
}

.journey-line {
  flex: 1;
  height: 1px;
  background: rgba(47, 42, 38, 0.18);
}

.quiz-form-section {
  padding: 6px 0 64px;
}

.form-shell {
  background: #f3eee8;
  border: 1px solid rgba(47, 42, 38, 0.12);
  padding: 24px;
}

.form-head {
  margin-bottom: 20px;
}

.wizard-subtitle {
  margin: 8px 0 0;
  max-width: 40rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 22px;
}

.full-row {
  grid-column: 1 / -1;
}

.form-group {
  display: grid;
  gap: 10px;
}

.form-group label {
  font-weight: 700;
  color: #3b312b;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  border-radius: 18px;
  border: 1px solid rgba(47, 42, 38, 0.14);
  background: #fffdf9;
  padding: 16px 18px;
  font: inherit;
  font-size: 1rem;
  color: #2f2a26;
  outline: none;
  resize: vertical;
}

.form-group input,
.form-group select {
  min-height: 58px;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #b2805c;
  box-shadow: 0 0 0 4px rgba(178, 128, 92, 0.14);
}

.chip-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.option-chip {
  border: 1px solid rgba(47, 42, 38, 0.12);
  background: #fbf7f2;
  color: #3b312b;
  padding: 12px 16px;
  border-radius: 999px;
  font: inherit;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.16s ease, background 0.16s ease, border-color 0.16s ease;
}

.option-chip:hover {
  transform: translateY(-1px);
  border-color: rgba(47, 42, 38, 0.22);
}

.option-chip.selected {
  background: #3b312b;
  color: #fff;
  border-color: #3b312b;
}

.preview-card {
  background: #fbf7f2;
  border: 1px solid rgba(47, 42, 38, 0.08);
  padding: 24px;
}

.preview-card h3 {
  margin: 0;
  font-size: 1.25rem;
  line-height: 1.1;
  color: #2f2a26;
}

.preview-list {
  margin: 18px 0 0;
  padding-left: 20px;
  color: #4f453d;
  line-height: 1.8;
}

.preview-note {
  margin: 18px 0 0;
}

.form-error {
  margin: 18px 0 0;
  color: #b42318;
  font-size: 0.95rem;
  font-weight: 600;
}

.form-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 30px;
}

.soft-brown-btn,
.outline-btn {
  min-height: 52px;
  padding: 0 24px;
  border-radius: 999px;
  font-size: 0.98rem;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.soft-brown-btn {
  background: #b2805c;
  color: #fff;
  border: none;
  cursor: pointer;
}

.outline-btn {
  background: transparent;
  color: #3b312b;
  border: 1px solid #3b312b;
  cursor: pointer;
}

@media (max-width: 900px) {
  .intro-shell,
  .form-grid {
    grid-template-columns: 1fr;
  }

  .intro-copy h1,
  .form-head h2 {
    max-width: none;
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

  .form-shell,
  .journey-card,
  .preview-card {
    padding: 20px;
  }

  .journey-steps {
    gap: 8px;
  }

  .journey-step {
    min-width: 62px;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions button {
    width: 100%;
  }
}
</style>