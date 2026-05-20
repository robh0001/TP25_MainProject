<!--
  ParentQuizPage.vue

  Creates the HealthyKids parent quiz page. Parents answer a short multi-step quiz to create
  or update a personalised family routine plan.

  API requirement:
  - Requires VITE_PARENT_PROFILES_API_BASE_URL.
  - Uses POST /parent-profiles to create a new parent profile.
  - Uses PUT /{familyCode} to update an existing parent profile.
  - Falls back between create and update when needed.

  Accessibility:
  - Uses aria-labels, aria-describedby, role="progressbar", role="alert", and aria-live.
  - Uses aria-pressed for selectable chips.
  - Uses data-hover-read-text for hover-to-read support.
  - Moves focus to validation errors when they appear.
-->

<template>
  <div class="quiz-page">
    <!-- Decorative background image and overlay layers -->
    <div class="quiz-bg" aria-hidden="true">
      <img
        class="quiz-bg__img"
        src="https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=2400&q=90"
        alt=""
        aria-hidden="true"
      />
      <div class="quiz-bg__overlay"></div>
      <div class="quiz-bg__grain"></div>
    </div>

    <!-- Main quiz content -->
    <main class="quiz-main" id="main-content">
      <!-- Website journey step bar -->
      <FamilyJourneyBar :current-step="2" />

        <section
          class="quiz-card"
          id="quiz-form"
          aria-labelledby="quiz-page-title"
          aria-describedby="quiz-page-description"
        >
        <!-- Quiz intro, step label, and progress bar -->
        <div class="quiz-intro">
          <p
            class="quiz-step-kicker"
            :aria-label="`Step ${currentStep + 1} of ${steps.length}`"
            :data-hover-read-text="`Step ${currentStep + 1} of ${steps.length}`"
          >
            <span class="quiz-kicker-dot" aria-hidden="true"></span>
            Step {{ currentStep + 1 }} of {{ steps.length }}
          </p>
          <h1 id="quiz-page-title">{{ isRetakeMode ? 'Review your routine' : 'Personalise your routine' }}</h1>

          <p class="quiz-intro-text" id="quiz-page-description">
            {{ activeStep.subtitle }}
          </p>

          <!-- Visual and accessible progress indicator -->
          <div
            class="quiz-progress-track"
            role="progressbar"
            :aria-valuenow="currentStep + 1"
            aria-valuemin="1"
            :aria-valuemax="steps.length"
            :aria-label="`Quiz progress: step ${currentStep + 1} of ${steps.length}`"
          >
            <div
              class="quiz-progress-fill"
              :style="{ width: `${((currentStep + 1) / steps.length) * 100}%` }"
            ></div>
          </div>
        </div>

        <!-- Main quiz form panel -->
        <div class="quiz-form-panel">
          <h2>{{ activeStep.title }}</h2>

          <!-- Step 1: family basics -->
          <div v-if="currentStep === 0" class="quiz-form-grid">
            <div class="quiz-form-group">
              <label for="username">Family code</label>
              <input
                id="username"
                v-model.trim="form.username"
                :disabled="hasFamilyCode"
                type="text"
                autocomplete="off"
                inputmode="text"
                placeholder="e.g. sunnyfamily01"
                data-hover-read-text="Family code. Enter a simple family code. Example sunny family zero one."
                :aria-invalid="errorMessage && !form.username ? 'true' : 'false'"
                aria-describedby="username-help"
              />
              <p id="username-help" class="quiz-sr-only">
                Enter a simple family code using letters, numbers, underscores, or hyphens.
              </p>
            </div>

            <div class="quiz-form-group">
              <label for="child-age">Child age range</label>
              <select
                id="child-age"
                v-model="form.ageRange"
                data-hover-read-text="Child age range. Select the age range for your child."
                :aria-invalid="errorMessage && !form.ageRange ? 'true' : 'false'"
                aria-describedby="child-age-help"
              >
                <option disabled value="">Select age range</option>
                <option>5-7 years</option>
                <option>8-10 years</option>
                <option>11-12 years</option>
              </select>
              <p id="child-age-help" class="quiz-sr-only">
                Choose one age range for the child this plan is for.
              </p>
            </div>

            <div class="quiz-form-group quiz-full-row">
              <label for="routine-type">Current family routine</label>
              <select
                id="routine-type"
                v-model="form.routineType"
                data-hover-read-text="Current family routine. Choose the option that best describes your routine."
                :aria-invalid="errorMessage && !form.routineType ? 'true' : 'false'"
                aria-describedby="routine-type-help"
              >
                <option disabled value="">Choose one</option>
                <option>Mostly structured</option>
                <option>Busy and sometimes inconsistent</option>
                <option>Very busy and hard to manage</option>
              </select>
              <p id="routine-type-help" class="quiz-sr-only">
                Choose the option that best describes your current family routine.
              </p>
            </div>
          </div>

          <!-- Step 2: priority habit areas -->
          <div v-if="currentStep === 1" class="quiz-form-grid">
            <div class="quiz-form-group quiz-full-row">
              <p id="habit-options-label" class="quiz-field-label">Priority areas</p>

              <div
                class="quiz-chip-grid"
                role="group"
                aria-labelledby="habit-options-label"
                aria-describedby="habit-options-help"
              >
                <button
                  v-for="habit in habitOptions"
                  :key="habit"
                  type="button"
                  class="quiz-option-chip"
                  :class="{ selected: form.habits.includes(habit) }"
                  :aria-pressed="form.habits.includes(habit) ? 'true' : 'false'"
                  :data-hover-read-text="`${habit}. ${form.habits.includes(habit) ? 'Selected' : 'Not selected'}. Click to toggle.`"
                  @click="toggleSelection(form.habits, habit)"
                >
                  {{ habit }}
                </button>
              </div>

              <p id="habit-options-help" class="quiz-sr-only">
                Select one or more priority areas that need support.
              </p>
            </div>
          </div>

          <!-- Step 3: parent concerns and support style -->
          <div v-if="currentStep === 2" class="quiz-form-grid">
            <div class="quiz-form-group quiz-full-row">
              <p id="concern-options-label" class="quiz-field-label">Key concerns</p>

              <div
                class="quiz-chip-grid"
                role="group"
                aria-labelledby="concern-options-label"
                aria-describedby="concern-options-help"
              >
                <button
                  v-for="concern in concernOptions"
                  :key="concern"
                  type="button"
                  class="quiz-option-chip"
                  :class="{ selected: form.concerns.includes(concern) }"
                  :aria-pressed="form.concerns.includes(concern) ? 'true' : 'false'"
                  :data-hover-read-text="`${concern}. ${form.concerns.includes(concern) ? 'Selected' : 'Not selected'}. Click to toggle.`"
                  @click="toggleSelection(form.concerns, concern)"
                >
                  {{ concern }}
                </button>
              </div>

              <p id="concern-options-help" class="quiz-sr-only">
                Select one or more concerns you want help with.
              </p>
            </div>

            <div class="quiz-form-group quiz-full-row">
              <label for="confidence">Confidence level</label>
              <select
                id="confidence"
                v-model="form.confidence"
                data-hover-read-text="Confidence level. Select how supported you currently feel."
                :aria-invalid="errorMessage && !form.confidence ? 'true' : 'false'"
                aria-describedby="confidence-help"
              >
                <option disabled value="">Choose one</option>
                <option>I feel confident</option>
                <option>I know what to do but struggle to stay consistent</option>
                <option>I need simple guidance and structure</option>
              </select>
              <p id="confidence-help" class="quiz-sr-only">
                Choose the option that best describes how confident you feel.
              </p>
            </div>
          </div>

          <!-- Step 4: review summary before saving -->
          <div
              v-if="currentStep === 3"
              class="quiz-preview-card"
              role="region"
              aria-labelledby="quiz-summary-title"
              :data-hover-read-text="reviewSummaryText"
            >
              <p
                id="quiz-summary-title"
                class="quiz-card-kicker"
                data-hover-read-text="Summary of your family plan answers."
              >
                Summary
              </p>

              <div class="quiz-review-grid" role="list" aria-label="Review your plan answers">
                <div
                  role="listitem"
                  tabindex="0"
                  :aria-label="`Family code: ${form.username || 'Not provided'}`"
                  :data-hover-read-text="`Family code: ${form.username || 'Not provided'}`"
                >
                  <span aria-hidden="true">Family code</span>
                  <strong aria-hidden="true">{{ form.username || 'Not provided' }}</strong>
                </div>

                <div
                  role="listitem"
                  tabindex="0"
                  :aria-label="`Routine: ${form.routineType || 'Not selected'}`"
                  :data-hover-read-text="`Routine: ${form.routineType || 'Not selected'}`"
                >
                  <span aria-hidden="true">Routine</span>
                  <strong aria-hidden="true">{{ form.routineType || 'Not selected' }}</strong>
                </div>

                <div
                  role="listitem"
                  tabindex="0"
                  :aria-label="`Priority areas: ${form.habits.length ? form.habits.join(', ') : 'None selected'}`"
                  :data-hover-read-text="`Priority areas: ${form.habits.length ? form.habits.join(', ') : 'None selected'}`"
                >
                  <span aria-hidden="true">Priority areas</span>
                  <strong aria-hidden="true">
                    {{ form.habits.length ? form.habits.join(', ') : 'None selected' }}
                  </strong>
                </div>
              </div>
            </div>

          <!-- Validation and save error message -->
          <p
            v-if="errorMessage"
            id="quiz-form-error"
            class="quiz-form-error"
            role="alert"
            aria-live="assertive"
            tabindex="-1"
            :data-hover-read-text="errorMessage"
          >
            {{ errorMessage }}
          </p>

          <!-- Wizard navigation buttons -->
          <div class="quiz-wizard-actions" aria-label="Quiz navigation controls">
            <button
              v-if="currentStep > 0"
              type="button"
              class="quiz-outline-btn"
              :disabled="saving"
              :aria-disabled="saving ? 'true' : 'false'"
              data-hover-read-text="Go back to the previous quiz step."
              @click="currentStep -= 1"
            >
              Back
            </button>

            <button
              v-if="currentStep < steps.length - 1"
              type="button"
              class="quiz-primary-btn"
              :disabled="saving"
              :aria-disabled="saving ? 'true' : 'false'"
              data-hover-read-text="Go to the next quiz step."
              @click="goNext"
            >
              Next
            </button>

            <button
              v-else
              type="button"
              class="quiz-primary-btn"
              :disabled="saving"
              :aria-disabled="saving ? 'true' : 'false'"
              :aria-busy="saving ? 'true' : 'false'"
              :data-hover-read-text="saving ? 'Saving your plan. Please wait.' : isRetakeMode ? 'Update my plan.' : 'Generate my plan.'"
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

    <!-- Footer copied from the home page styling -->
    <footer
      class="home-footer quiz-home-footer"
      aria-label="Website footer"
    >
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
        aria-label="UN Sustainable Development Goal 3, Good Health and Wellbeing. Developed by Team Syrbyx."
        data-hover-read-text
      >
        <span>UN SDG 3 · Good Health &amp; Wellbeing</span>
        <span class="home-footer-divider" aria-hidden="true">·</span>
        <span>Developed by Team Syrbyx</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, nextTick, reactive, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'
import { useHoverToRead } from '../composables/useHoverToRead'
import { useSpeechSynthesis } from '../composables/useSpeechSynthesis'
import FamilyJourneyBar from '../components/FamilyJourneyBar.vue'

// Router and shared family plan store.
const router = useRouter()
const { state, savePlan } = useFamilyPlanStore()

// Parent profile API base URL from the Vite environment file.
const API_BASE = import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL

// Main quiz form state.
const form = reactive({
  username: state.username || '',
  ageRange: state.ageRange || '',
  routineType: state.routineType || '',
  habits: Array.isArray(state.habits) ? [...state.habits] : [],
  concerns: Array.isArray(state.concerns) ? [...state.concerns] : [],
  confidence: state.confidence || '',
})

// Quiz step labels and descriptions.
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
    title: 'Parent Concerns',
    subtitle: 'Capture your concerns and what kind of guidance would help most.',
  },
  {
    title: 'Review your plan',
    subtitle: 'Check your answers before saving your family dashboard.',
  },
]

// Habit choices shown as selectable chips.
const habitOptions = [
  'Balanced meals',
  'Healthier snacks',
  'Daily movement',
  'Sleep routine',
  'Morning routine',
  'After-school routine',
  'Screen time balance',
]

// Parent concern choices shown as selectable chips.
const concernOptions = [
  'My child is not active enough',
  'My child prefers screens over outdoor activity',
  'My child snacks too often',
  'My child needs healthier meals',
  'My child struggles with bedtime',
  'My child finds routines hard',
  'My child needs healthier habits',
  'I need help supporting my child',
]

// Current quiz progress and save state.
const currentStep = ref(0)
const errorMessage = ref('')
const saving = ref(false)

// Active step data used by the template.
const activeStep = computed(() => steps[currentStep.value])

// Prevents family code editing when it already exists in the store.
const hasFamilyCode = computed(() => Boolean(state.username))

// Readable review summary for hover-to-read.
const reviewSummaryText = computed(() => {
  const familyCode = form.username || 'Not provided'
  const routine = form.routineType || 'Not selected'
  const priorities = form.habits.length ? form.habits.join(', ') : 'None selected'

  return `Summary. Family code: ${familyCode}. Routine: ${routine}. Priority areas: ${priorities}.`
})

// Hover-to-read and speech helpers for error feedback.
const { isHoverToReadEnabled } = useHoverToRead()
const { speakText } = useSpeechSynthesis()

// Sets an error message, focuses it, and optionally reads it aloud.
function setError(message) {
  errorMessage.value = message

  nextTick(() => {
    const errorElement = document.getElementById('quiz-form-error')
    errorElement?.focus?.()
  })

  if (isHoverToReadEnabled.value) {
    speakText(message)
  }
}

// Clears the current form error.
function clearError() {
  errorMessage.value = ''
}

// Checks whether the quiz is updating an existing plan instead of creating a new one.
const isRetakeMode = computed(() =>
  Boolean(
    state.username &&
    (
      state.ageRange ||
      state.routineType ||
      state.confidence ||
      state.dailyPlan ||
      state.progressItems ||
      state.recommendations ||
      (Array.isArray(state.habits) && state.habits.length > 0) ||
      (Array.isArray(state.concerns) && state.concerns.length > 0)
    )
  )
)

// Adds or removes a selected chip value.
function toggleSelection(list, value) {
  const index = list.indexOf(value)

  if (index === -1) {
    list.push(value)
    return
  }

  list.splice(index, 1)
}

// Validates the family code format.
function isValidUsername(username) {
  return /^[a-zA-Z0-9_-]{3,24}$/.test(username)
}

// Validates the current quiz step before moving forward or submitting.
function validateStep() {
  clearError()
  errorMessage.value = ''

  if (currentStep.value === 0) {
    if (!form.username) {
      setError('Please enter a family code.')
      return false
    }

    if (!isValidUsername(form.username)) {
      
        setError('Family code must be 3-24 characters and can only include letters, numbers, underscores, or hyphens.')
      return false
    }

    if (!form.ageRange) {
      setError("Please select your child's age range.")
      return false
    }

    if (!form.routineType) {
      setError('Please select your family routine type.')
      return false
    }
  }

  if (currentStep.value === 1) {
    if (!form.habits.length) {
      setError('Please select at least one habit to support.')
      return false
    }
  }

  if (currentStep.value === 2) {
    if (!form.concerns.length) {
      setError('Please select at least one parent concern.')
      return false
    }

    if (!form.confidence) {
      setError('Please select how supported you currently feel.')
      return false
    }

  }

  return true
}

// Moves to the next step if the current step is valid.
function goNext() {
  if (!validateStep()) return
  currentStep.value += 1
}

// Removes duplicate and empty strings from generated arrays.
function uniqueStrings(values) {
  return [...new Set(values.filter(Boolean))]
}

// Builds task and tracker suggestions from selected habits, concerns, routine type, and support style.
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

// Builds a simple daily plan for each day of the week.
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

// Builds checklist-style progress items for the dashboard.
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

// Creates personalised recommendations based on quiz answers.
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

// Chooses the next suggested dashboard action.
function createNextAction(taskPool) {
  return taskPool.tasks[0] || 'Complete one healthy family habit today.'
}

// Creates the main mission text for the dashboard.
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

// Combines all quiz answers and generated plan data into one API payload.
function buildPayload() {
  const taskPool = buildTaskPool()

  return {
    username: form.username,
    ageRange: form.ageRange,
    routineType: form.routineType,
    habits: [...form.habits],
    concerns: [...form.concerns],
    confidence: form.confidence,
    recommendations: createRecommendations(),
    dailyPlan: buildDailyPlan(taskPool),
    progressItems: buildProgressItems(taskPool),
    nextAction: createNextAction(taskPool),
    mission: createMission(),
    streakDays: state.streakDays || 0,
  }
}

// Fetch helper that returns both the raw response and parsed JSON data.
async function requestJson(url, options) {
  const response = await fetch(url, options)
  const data = await response.json().catch(() => ({}))

  return {
    response,
    data,
  }
}

// Creates a new parent profile.
async function createProfile(payload) {
  return requestJson(`${API_BASE}/parent-profiles`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

// Updates an existing parent profile using the family code.
async function updateProfile(payload) {
  const encodedUsername = encodeURIComponent(payload.username)

  return requestJson(`${API_BASE}/${encodedUsername}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}

// Saves the profile by updating or creating depending on quiz mode and API response.
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

// Final quiz submission handler.
async function submitQuiz() {
  if (!validateStep() || saving.value) return

  if (!API_BASE) {
    setError('Missing VITE_PARENT_PROFILES_API_BASE_URL.')
    return
  }

  saving.value = true
  clearError()

  const payload = buildPayload()

  try {
    const { response, data } = await saveProfile(payload)

    if (!response.ok) {
      if (response.status === 409) {
        setError('That family code is already taken. Please use your existing family code or choose another one.')
        return
      }

      throw new Error(data.error || `Save failed with status ${response.status}`)
    }

    savePlan(payload)
    router.push('/parent-dashboard')
  } catch {
    setError('Something went wrong while saving your plan. Please try again in a moment.')
  } finally {
    saving.value = false
  }
}
</script>