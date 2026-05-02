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
              <h1>{{ isRetakeMode ? 'Update plan' : 'Build a plan' }}</h1>
              <p class="intro-text">
                {{
                  isRetakeMode
                    ? 'Update your answers so your parent dashboard reflects your current family routine.'
                    : 'Answer a few questions so we can shape a more realistic family routine and build your parent dashboard.'
                }}
              </p>
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

              <div class="progress-track" aria-hidden="true">
                <div
                  class="progress-fill"
                  :style="{ width: `${((currentStep + 1) / steps.length) * 100}%` }"
                ></div>
              </div>
            </div>

            <div v-if="currentStep === 0" class="form-grid">
              <div class="form-group">
                <label for="username">Family code</label>
                <input
                  id="username"
                  v-model.trim="form.username"
                  :disabled="isRetakeMode"
                  placeholder="Enter your username"
                />
                <small v-if="isRetakeMode" class="field-hint">
                  Family code is locked because you are updating your existing profile.
                </small>
                <small v-else class="field-hint">
                  Use the same private family code you created earlier. Avoid real names or contact details.
                </small>
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
                <small class="field-hint">
                  Keep this general. Avoid real names, medical details, addresses, or contact information.
                </small>
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
                  <li><strong>Family code:</strong> {{ form.username || 'Not provided' }}</li>
                  <li>
                    <strong>Top habits to support:</strong>
                    {{ form.habits.length ? form.habits.join(', ') : 'None selected' }}
                  </li>
                  <li>
                    <strong>Main concerns:</strong>
                    {{ form.concerns.length ? form.concerns.join(', ') : 'None selected' }}
                  </li>
                  <li><strong>Support style:</strong> {{ form.supportStyle || 'Not selected' }}</li>
                  <li><strong>Routine context:</strong> {{ form.routineType || 'Not selected' }}</li>
                </ul>

                <p class="preview-note">
                  {{
                    isRetakeMode
                      ? 'Your updated answers will replace your existing dashboard plan.'
                      : 'Your answers will generate a saved parent dashboard with practical next steps, a weekly plan, and trackable tasks.'
                  }}
                </p>
              </article>
            </div>

            <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>

            <div class="form-actions wizard-actions">
              <button
                v-if="currentStep > 0"
                type="button"
                class="outline-btn"
                :disabled="saving"
                @click="currentStep -= 1"
              >
                Back
              </button>

              <button
                v-if="currentStep < steps.length - 1"
                type="button"
                class="soft-brown-btn"
                :disabled="saving"
                @click="goNext"
              >
                Continue
              </button>

              <button
                v-else
                type="button"
                class="soft-brown-btn"
                :disabled="saving"
                @click="submitQuiz"
              >
                {{
                  saving
                    ? 'Saving your plan...'
                    : isRetakeMode
                      ? 'Update my family plan'
                      : 'Save and generate my family plan'
                }}
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
import { RouterLink, useRouter } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'

const router = useRouter()
const { state, savePlan } = useFamilyPlanStore()

const API_BASE = import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL

const form = reactive({
  username: state.username || '',
  ageRange: state.ageRange || '',
  routineType: state.routineType || '',
  habits: Array.isArray(state.habits) ? [...state.habits] : [],
  concerns: Array.isArray(state.concerns) ? [...state.concerns] : [],
  struggle: state.struggle || '',
  confidence: state.confidence || '',
  supportStyle: state.supportStyle || '',
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
    subtitle: 'Check your answers before saving your family dashboard.',
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
  'I am worried about healthy growth or long-term wellbeing',
  'I am not sure what the right approach is',
]

const currentStep = ref(0)
const errorMessage = ref('')
const saving = ref(false)

const activeStep = computed(() => steps[currentStep.value])
const isRetakeMode = computed(() => Boolean(state.username))

function toggleSelection(list, value) {
  const index = list.indexOf(value)

  if (index === -1) {
    list.push(value)
    return
  }

  list.splice(index, 1)
}

function isValidUsername(username) {
  return /^[a-zA-Z0-9_-]{3,24}$/.test(username)
}

function validateStep() {
  errorMessage.value = ''

  if (currentStep.value === 0) {
    if (!form.username) {
      errorMessage.value = 'Please enter a family code.'
      return false
    }

    if (!isValidUsername(form.username)) {
      errorMessage.value =
        'Family code must be 3-24 characters and can only include letters, numbers, underscores, or hyphens.'
      return false
    }

    if (!form.ageRange) {
      errorMessage.value = "Please select your child's age range."
      return false
    }

    if (!form.routineType) {
      errorMessage.value = 'Please select your family routine type.'
      return false
    }
  }

  if (currentStep.value === 1) {
    if (!form.habits.length) {
      errorMessage.value = 'Please select at least one habit to support.'
      return false
    }

    if (!form.struggle) {
      errorMessage.value = 'Please describe what feels hardest in daily family life right now.'
      return false
    }
  }

  if (currentStep.value === 2) {
    if (!form.concerns.length) {
      errorMessage.value = 'Please select at least one parent concern.'
      return false
    }

    if (!form.confidence) {
      errorMessage.value = 'Please select how supported you currently feel.'
      return false
    }

    if (!form.supportStyle) {
      errorMessage.value = 'Please select the type of support that would help most.'
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
    trackerItems.push('Planned snack time used', 'Portioned snack served')
  }

  if (form.concerns.includes('Healthy meals are hard on busy days')) {
    tasks.push(
      'Choose one simple low-effort meal for today',
      "Decide tonight's meal before the busy part of the day begins"
    )
    trackerItems.push('Simple low-effort meal used', 'Meal decided early')
  }

  if (form.concerns.includes('Bedtime feels inconsistent')) {
    tasks.push(
      'Keep bedtime within the same 20-minute window tonight',
      'Repeat the same final bedtime activity tonight'
    )
    trackerItems.push('Bedtime kept within the target window', 'Same final bedtime activity repeated')
  }

  if (form.concerns.includes('Our family routine feels hard to manage')) {
    tasks.push(
      'Focus on just one habit today instead of trying to fix everything',
      'Use one visible cue such as a note, bottle, or snack setup'
    )
    trackerItems.push('One-habit focus maintained', 'Visible routine cue used')
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
    trackerItems.push('Easiest version of the task completed', 'One thing prepped early')
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

  if (
    form.habits.includes('Screen time balance') ||
    form.concerns.includes('My child prefers screens over outdoor activity')
  ) {
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
        description: `Start with one small ${
          form.habits[0]?.toLowerCase() || 'healthy routine'
        } action each day and keep the goal realistic.`,
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

function buildPayload() {
  const taskPool = buildTaskPool()

  return {
    username: form.username,
    ageRange: form.ageRange,
    routineType: form.routineType,
    habits: [...form.habits],
    concerns: [...form.concerns],
    struggle: form.struggle,
    confidence: form.confidence,
    supportStyle: form.supportStyle,
    recommendations: createRecommendations(),
    dailyPlan: buildDailyPlan(taskPool),
    progressItems: buildProgressItems(taskPool),
    nextAction: createNextAction(taskPool),
    mission: createMission(),
    streakDays: state.streakDays || 0,
  }
}

async function requestJson(url, options) {
  const response = await fetch(url, options)
  const data = await response.json().catch(() => ({}))

  return {
    response,
    data,
  }
}

async function createProfile(payload) {
  return requestJson(`${API_BASE}/parent-profiles`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

async function updateProfile(payload) {
  const encodedUsername = encodeURIComponent(payload.username)

  return requestJson(`${API_BASE}/parent-profiles/${encodedUsername}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

async function saveProfile(payload) {
  if (isRetakeMode.value) {
    return updateProfile(payload)
  }

  const createResult = await createProfile(payload)

  if (createResult.response.status === 409) {
    return updateProfile(payload)
  }

  return createResult
}

async function submitQuiz() {
  if (!validateStep() || saving.value) return

  if (!API_BASE) {
    errorMessage.value = 'Missing VITE_PARENT_PROFILES_API_BASE_URL.'
    return
  }

  saving.value = true
  errorMessage.value = ''

  const payload = buildPayload()

  try {
    const { response, data } = await saveProfile(payload)

    if (!response.ok) {
      if (response.status === 409) {
        errorMessage.value = 'That family code is already taken. Please use your existing family code or choose another one.'
        return
      }

      throw new Error(data.error || `Save failed with status ${response.status}`)
    }

    savePlan(payload)
    router.push('/parent-dashboard')
  } catch (error) {
    console.error(error)
    errorMessage.value =
      'Something went wrong while saving your plan. Please try again in a moment.'
  } finally {
    saving.value = false
  }
}
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

  --border: rgba(10, 11, 10, 0.08);
  --border-mid: rgba(10, 11, 10, 0.14);

  --shadow-xs: 0 1px 4px rgba(0, 0, 0, 0.06);
  --shadow-sm: 0 2px 12px rgba(0, 0, 0, 0.07);
  --shadow-md: 0 8px 28px rgba(0, 0, 0, 0.09);
  --shadow-lg: 0 20px 56px rgba(0, 0, 0, 0.12);

  --f-display: 'Fraunces', Georgia, serif;
  --f-body: 'General Sans', 'Helvetica Neue', ui-sans-serif, sans-serif;
  --f-mono: 'JetBrains Mono', monospace;

  --r-card: 28px;
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

.quiz-page {
  min-height: 100vh;
  position: relative;
  overflow-x: clip;
  background:
    radial-gradient(circle at 82% 12%, rgba(34, 197, 94, 0.08), transparent 28rem),
    radial-gradient(circle at 8% 28%, rgba(59, 130, 246, 0.04), transparent 26rem),
    var(--c-white);
}

.quiz-page::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 256px;
}

.container {
  width: min(1180px, calc(100% - 48px));
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

/* HEADER */
.site-header {
  position: sticky;
  top: 0;
  z-index: 500;
  background: rgba(255, 255, 255, 0.92);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: var(--shadow-xs);
}

.header-row {
  min-height: 76px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.brand {
  text-decoration: none;
  color: var(--c-black);
  font-family: var(--f-display);
  font-size: 1.25rem;
  font-weight: 400;
  letter-spacing: -0.03em;
}

.nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav a,
.nav-link {
  height: 36px;
  padding: 0 12px;
  display: flex;
  align-items: center;
  font-family: var(--f-body);
  font-size: 0.86rem;
  font-weight: 500;
  color: var(--c-500);
  text-decoration: none;
  border-radius: 8px;
  transition: color 0.18s, background 0.18s;
}

.nav a:hover,
.nav-link:hover {
  color: var(--c-black);
  background: var(--c-50);
}

.header-btn {
  height: 38px;
  padding: 0 16px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--f-body);
  font-size: 0.86rem;
  font-weight: 600;
  color: var(--c-white);
  background: var(--c-black);
  text-decoration: none;
  border-radius: 10px;
  border: 1px solid var(--c-900);
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.06) inset;
  transition: all 0.2s;
}

.header-btn:hover {
  background: var(--c-800);
  transform: translateY(-1px);
}

.light-btn {
  color: var(--c-white);
}

/* HERO / INTRO */
.quiz-top {
  position: relative;
  padding: 92px 0 70px;
  overflow: hidden;
  border-bottom: 1px solid var(--border);
}

.quiz-top::before {
  content: "";
  position: absolute;
  width: 620px;
  height: 620px;
  top: -220px;
  right: -120px;
  border-radius: 50%;
  filter: blur(100px);
  background: radial-gradient(circle, rgba(22, 163, 74, 0.1), transparent 70%);
  pointer-events: none;
}

.quiz-top::after {
  content: "";
  position: absolute;
  width: 460px;
  height: 460px;
  bottom: -180px;
  left: -120px;
  border-radius: 50%;
  filter: blur(100px);
  background: radial-gradient(circle, rgba(59, 130, 246, 0.055), transparent 70%);
  pointer-events: none;
}

.intro-shell {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 420px;
  gap: 70px;
  align-items: center;
}

.step-kicker {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  background: var(--c-green-soft);
  border: 1px solid rgba(22, 163, 74, 0.2);
  font-size: 0.72rem;
  font-weight: 800;
  color: var(--c-green);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin: 0 0 28px;
}

.step-kicker::before {
  content: "";
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--c-green-mid);
  animation: livePulse 2.4s ease-in-out infinite;
}

@keyframes livePulse {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.45);
  }

  50% {
    box-shadow: 0 0 0 4px rgba(34, 197, 94, 0);
  }
}

.intro-copy h1,
.form-head h2,
.preview-card h3 {
  margin: 0;
  font-family: var(--f-display);
  font-weight: 400;
  line-height: 1.02;
  letter-spacing: -0.04em;
  color: var(--c-black);
}

.intro-copy h1 {
  max-width: 11ch;
  font-size: clamp(3rem, 6vw, 6.4rem);
  font-weight: 300;
  line-height: 0.96;
  letter-spacing: -0.055em;
}

.intro-text {
  max-width: 42rem;
  margin: 28px 0 0;
  font-family: var(--f-body);
  font-size: 1.02rem;
  line-height: 1.75;
  color: var(--c-500);
}

/* JOURNEY CARD */
.journey-card {
  padding: 28px;
  border-radius: 26px;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.94), rgba(244, 245, 242, 0.92));
  border: 1px solid var(--border);
  box-shadow: var(--shadow-lg);
}

.journey-label,
.wizard-step,
.card-kicker {
  margin: 0;
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--c-400);
}

.journey-label {
  margin-bottom: 22px;
}

.journey-steps {
  display: grid;
  gap: 12px;
}

.journey-step {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  min-width: 0;
}

.journey-step span {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  background: var(--c-50);
  border: 1px solid var(--border);
  font-family: var(--f-mono);
  font-size: 0.74rem;
  font-weight: 800;
  color: var(--c-400);
}

.journey-step.complete span,
.journey-step.active span {
  background: var(--c-black);
  color: var(--c-white);
  border-color: var(--c-black);
}

.journey-step small {
  display: block;
  padding-top: 11px;
  font-family: var(--f-body);
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--c-black);
  line-height: 1.35;
}

.journey-line {
  width: 1px;
  height: 24px;
  margin-left: 21px;
  background: var(--border-mid);
}

/* FORM SECTION */
.quiz-form-section {
  padding: 86px 0 96px;
  background: var(--c-white);
  position: relative;
  z-index: 1;
}

.form-shell {
  max-width: 900px;
  margin: 0 auto;
  padding: 32px;
  border-radius: 28px;
  background: var(--c-white);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-md);
}

.form-head {
  margin-bottom: 28px;
}

.wizard-step {
  margin-bottom: 12px;
  color: var(--c-green);
}

.form-head h2 {
  font-size: clamp(2rem, 3.5vw, 3.25rem);
  font-weight: 400;
  line-height: 1.04;
  letter-spacing: -0.045em;
}

.wizard-subtitle {
  max-width: 44rem;
  margin: 12px 0 0;
  font-size: 0.98rem;
  line-height: 1.72;
  color: var(--c-500);
}

.progress-track {
  width: 100%;
  height: 8px;
  margin-top: 22px;
  border-radius: 999px;
  background: var(--c-100);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: inherit;
  background: var(--c-black);
  transition: width 0.25s ease;
}

/* FORM CONTROLS */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
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
  font-family: var(--f-body);
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--c-black);
  line-height: 1.5;
}

.field-hint {
  color: var(--c-400);
  font-size: 0.78rem;
  line-height: 1.5;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  border-radius: 12px;
  border: 1px solid var(--border-mid);
  background: #fffefb;
  padding: 0 16px;
  font-family: var(--f-body);
  font-size: 0.96rem;
  color: var(--c-black);
  outline: none;
  resize: vertical;
  transition: border-color 0.15s, box-shadow 0.15s, background 0.15s;
}

.form-group input,
.form-group select {
  height: 54px;
}

.form-group input:disabled {
  color: var(--c-500);
  background: var(--c-50);
  cursor: not-allowed;
}

.form-group textarea {
  min-height: 140px;
  padding-top: 16px;
  line-height: 1.65;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: var(--c-300);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--c-green);
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.12);
}

/* OPTION CHIPS */
.chip-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.option-chip {
  min-height: 44px;
  padding: 0 16px;
  border-radius: 999px;
  border: 1px solid var(--border-mid);
  background: var(--c-white);
  color: var(--c-700);
  font-family: var(--f-body);
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  transition:
    transform 0.16s ease,
    background 0.16s ease,
    border-color 0.16s ease,
    color 0.16s ease,
    box-shadow 0.16s ease;
}

.option-chip:hover {
  transform: translateY(-1px);
  background: var(--c-50);
  border-color: rgba(22, 163, 74, 0.24);
}

.option-chip.selected {
  color: var(--c-white);
  background: var(--c-black);
  border-color: var(--c-black);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.14);
}

.option-chip.selected::after {
  content: " ✓";
}

/* PREVIEW */
.preview-stack {
  display: grid;
  gap: 18px;
}

.preview-card {
  padding: 28px;
  border-radius: 24px;
  background:
    radial-gradient(circle at top right, rgba(34, 197, 94, 0.08), transparent 18rem),
    var(--c-50);
  border: 1px solid var(--border);
}

.card-kicker {
  margin-bottom: 12px;
}

.preview-card h3 {
  font-size: clamp(1.55rem, 2.4vw, 2.15rem);
  line-height: 1.08;
  letter-spacing: -0.035em;
}

.preview-list {
  margin: 20px 0 0;
  padding-left: 20px;
  color: var(--c-500);
  font-size: 0.94rem;
  line-height: 1.85;
}

.preview-list strong {
  color: var(--c-black);
}

.preview-note {
  margin: 18px 0 0;
  font-size: 0.94rem;
  line-height: 1.7;
  color: var(--c-500);
}

/* ERRORS */
.form-error {
  margin: 22px 0 0;
  padding: 12px 14px;
  border-radius: 12px;
  background: rgba(180, 35, 24, 0.08);
  border: 1px solid rgba(180, 35, 24, 0.16);
  color: #b42318;
  font-size: 0.9rem;
  font-weight: 700;
  line-height: 1.5;
}

/* BUTTONS */
.form-actions,
.wizard-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 30px;
}

.soft-brown-btn,
.outline-btn {
  min-height: 52px;
  padding: 0 24px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  font-family: var(--f-body);
  font-size: 0.94rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.22s;
}

.soft-brown-btn {
  color: var(--c-white);
  background: var(--c-black);
  border: 1px solid var(--c-black);
  box-shadow: none;
}

.soft-brown-btn:hover:not(:disabled) {
  background: var(--c-800);
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
}

.outline-btn {
  color: var(--c-black);
  background: var(--c-white);
  border: 1px solid var(--border-mid);
}

.outline-btn:hover:not(:disabled) {
  background: var(--c-50);
  transform: translateY(-1px);
}

.soft-brown-btn:disabled,
.outline-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* RESPONSIVE */
@media (max-width: 980px) {
  .intro-shell,
  .form-grid {
    grid-template-columns: 1fr;
  }

  .journey-card {
    max-width: 560px;
  }

  .intro-copy h1 {
    max-width: 11ch;
  }
}

@media (max-width: 760px) {
  .container {
    width: calc(100% - 32px);
  }

  .header-row {
    min-height: auto;
    padding: 14px 0;
    gap: 14px;
    flex-wrap: wrap;
  }

  .nav {
    display: none;
  }

  .header-btn {
    width: 100%;
  }

  .quiz-top {
    padding: 64px 0 52px;
  }

  .intro-copy h1 {
    font-size: clamp(2.75rem, 12vw, 4rem);
  }

  .quiz-form-section {
    padding: 64px 0;
  }

  .form-shell,
  .journey-card,
  .preview-card {
    padding: 24px;
  }

  .form-actions,
  .wizard-actions {
    flex-direction: column;
  }

  .form-actions button,
  .wizard-actions button {
    width: 100%;
  }
}

@media (max-width: 520px) {
  .journey-step small {
    font-size: 0.82rem;
  }

  .form-shell {
    padding: 20px;
  }

  .chip-grid {
    gap: 10px;
  }

  .option-chip {
    width: 100%;
    justify-content: center;
  }
}
</style>