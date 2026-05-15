<template>
  <div class="quiz-page">
    <div class="quiz-bg">
      <img
        class="quiz-bg__img"
        src="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=2400&q=90"
        alt=""
        aria-hidden="true"
      />
      <div class="quiz-bg__overlay"></div>
      <div class="quiz-bg__grain"></div>
    </div>

    <header class="quiz-site-header">
      <RouterLink to="/" class="quiz-brand">
        <span class="quiz-brand-icon" aria-hidden="true">
          <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2" />
            <path
              d="M18 9C13.8 12.3 11.5 16.2 12.4 20.4C13.1 23.8 15.5 26.1 18 27.6C20.5 26.1 22.9 23.8 23.6 20.4C24.5 16.2 22.2 12.3 18 9Z"
              fill="currentColor"
              opacity="0.9"
            />
            <path
              d="M18 14.2V24.5"
              stroke="white"
              stroke-width="1.4"
              stroke-linecap="round"
              opacity="0.72"
            />
          </svg>
        </span>
        <span>HealthyKids</span>
      </RouterLink>

      <RouterLink to="/parent-entry" class="quiz-header-btn">
        <span>&#8592;</span> Parent access
      </RouterLink>
    </header>

    <main class="quiz-main">
      <section class="quiz-card" id="quiz-form">
        <div class="quiz-intro">
          <p class="quiz-step-kicker">
            <span class="quiz-kicker-dot"></span>
            Step {{ currentStep + 1 }} of {{ steps.length }}
          </p>

          <h1>{{ isRetakeMode ? 'Review your routine' : 'Personalise your routine' }}</h1>

          <p class="quiz-intro-text">
            {{ activeStep.subtitle }}
          </p>

          <div class="quiz-progress-track" aria-hidden="true">
            <div
              class="quiz-progress-fill"
              :style="{ width: `${((currentStep + 1) / steps.length) * 100}%` }"
            ></div>
          </div>
        </div>

        <div class="quiz-form-panel">
          <h2>{{ activeStep.title }}</h2>

          <div v-if="currentStep === 0" class="quiz-form-grid">
            <div class="quiz-form-group">
              <label for="username">Family code</label>
              <input
                id="username"
                v-model.trim="form.username"
                :disabled="hasFamilyCode"
                placeholder="e.g. sunnyfamily01"
              />
            </div>

            <div class="quiz-form-group">
              <label for="child-age">Child age range</label>
              <select id="child-age" v-model="form.ageRange">
                <option disabled value="">Select age range</option>
                <option>5-7 years</option>
                <option>8-10 years</option>
                <option>11-12 years</option>
              </select>
            </div>

            <div class="quiz-form-group quiz-full-row">
              <label for="routine-type">Current family routine</label>
              <select id="routine-type" v-model="form.routineType">
                <option disabled value="">Choose one</option>
                <option>Mostly structured</option>
                <option>Busy and sometimes inconsistent</option>
                <option>Very busy and hard to manage</option>
              </select>
            </div>
          </div>

          <div v-if="currentStep === 1" class="quiz-form-grid">
            <div class="quiz-form-group quiz-full-row">
              <label>Priority areas</label>
              <div class="quiz-chip-grid">
                <button
                  v-for="habit in habitOptions"
                  :key="habit"
                  type="button"
                  class="quiz-option-chip"
                  :class="{ selected: form.habits.includes(habit) }"
                  @click="toggleSelection(form.habits, habit)"
                >
                  {{ habit }}
                </button>
              </div>
            </div>
          </div>

          <div v-if="currentStep === 2" class="quiz-form-grid">
            <div class="quiz-form-group quiz-full-row">
              <label>Key concerns</label>
              <div class="quiz-chip-grid">
                <button
                  v-for="concern in concernOptions"
                  :key="concern"
                  type="button"
                  class="quiz-option-chip"
                  :class="{ selected: form.concerns.includes(concern) }"
                  @click="toggleSelection(form.concerns, concern)"
                >
                  {{ concern }}
                </button>
              </div>
            </div>

            <div class="quiz-form-group">
              <label for="confidence">Confidence level</label>
              <select id="confidence" v-model="form.confidence">
                <option disabled value="">Choose one</option>
                <option>I feel confident</option>
                <option>I know what to do but struggle to stay consistent</option>
                <option>I need simple guidance and structure</option>
              </select>
            </div>

            <div class="quiz-form-group">
              <label for="support-style">Preferred guidance style</label>
              <select id="support-style" v-model="form.supportStyle">
                <option disabled value="">Choose one</option>
                <option>Small daily actions</option>
                <option>Structured weekly plan</option>
                <option>Visual reminders</option>
                <option>Low-conflict routine strategies</option>
              </select>
            </div>
          </div>

          <div v-if="currentStep === 3" class="quiz-preview-card">
            <p class="quiz-card-kicker">Summary</p>

            <div class="quiz-review-grid">
              <div>
                <span>Family code</span>
                <strong>{{ form.username || 'Not provided' }}</strong>
              </div>

              <div>
                <span>Routine</span>
                <strong>{{ form.routineType || 'Not selected' }}</strong>
              </div>

              <div>
                <span>Priority areas</span>
                <strong>{{ form.habits.length ? form.habits.join(', ') : 'None selected' }}</strong>
              </div>

              <div>
                <span>Guidance style</span>
                <strong>{{ form.supportStyle || 'Not selected' }}</strong>
              </div>
            </div>
          </div>

          <p v-if="errorMessage" class="quiz-form-error">{{ errorMessage }}</p>

          <div class="quiz-wizard-actions">
            <button
              v-if="currentStep > 0"
              type="button"
              class="quiz-outline-btn"
              :disabled="saving"
              @click="currentStep -= 1"
            >
              Back
            </button>

            <button
              v-if="currentStep < steps.length - 1"
              type="button"
              class="quiz-primary-btn"
              :disabled="saving"
              @click="goNext"
            >
              Next
            </button>

            <button
              v-else
              type="button"
              class="quiz-primary-btn"
              :disabled="saving"
              @click="submitQuiz"
            >
              {{
                saving
                  ? 'Saving...'
                  : isRetakeMode
                    ? 'Update my plan'
                    : 'Generate my plan'
              }}
            </button>
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
const hasFamilyCode = computed(() => Boolean(state.username))

const isRetakeMode = computed(() =>
  Boolean(
    state.username &&
    (
      state.ageRange ||
      state.routineType ||
      state.confidence ||
      state.supportStyle ||
      state.dailyPlan ||
      state.progressItems ||
      state.recommendations ||
      (Array.isArray(state.habits) && state.habits.length > 0) ||
      (Array.isArray(state.concerns) && state.concerns.length > 0)
    )
  )
)

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

  if (form.supportStyle === 'Visual reminders') {
    tasks.push('Place one visible reminder where the habit needs to happen')
    trackerItems.push('Visible reminder placed')
  }

  if (form.supportStyle === 'Low-conflict routine strategies') {
    tasks.push('Use one calm instruction instead of repeated reminders')
    trackerItems.push('Calm single instruction used')
  }

  if (form.supportStyle === 'Small daily actions') {
    tasks.push('Choose only one non-negotiable healthy task for today')
    trackerItems.push('One daily action completed')
  }

  if (form.supportStyle === 'Structured weekly plan') {
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

  if (form.supportStyle === 'Visual reminders') {
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
        description: 'Set one clear cue before the difficult time of day begins.',
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

  return requestJson(`${API_BASE}/${encodedUsername}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

async function saveProfile(payload) {
  if (isRetakeMode.value) {
    const updateResult = await updateProfile(payload)

    if (updateResult.response.status !== 404) {
      return updateResult
    }

    return createProfile(payload)
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
        errorMessage.value =
          'That family code is already taken. Please use your existing family code or choose another one.'
        return
      }

      throw new Error(data.error || `Save failed with status ${response.status}`)
    }

    savePlan(payload)
    router.push('/parent-dashboard')
  } catch {
    errorMessage.value =
      'Something went wrong while saving your plan. Please try again in a moment.'
  } finally {
    saving.value = false
  }
}
</script>