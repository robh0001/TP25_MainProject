<template>
  <main class="page-main container section-gap">
    <section class="form-hero parent-quiz-hero">
      <div>
        <p class="eyebrow">Parent onboarding</p>
        <h1>Build a plan for {{ namePreview }}</h1>
        <p class="hero-subtext narrow-copy">
          A guided 4-step quiz to create realistic actions for nutrition, activity, sleep, and routines.
        </p>
      </div>
      <div class="progress-stack">
        <p class="progress-label">Step {{ currentStep + 1 }} of {{ steps.length }}</p>
        <div class="progress-track">
          <div class="progress-fill" :style="{ width: `${progressPercent}%` }"></div>
        </div>
      </div>
    </section>

    <section class="form-card">
      <p class="wizard-title">{{ activeStep.title }}</p>
      <p class="wizard-subtitle">{{ activeStep.subtitle }}</p>

      <div v-if="currentStep === 0" class="form-grid">
        <div class="form-group">
          <label for="child-name">Child first name</label>
          <input id="child-name" v-model.trim="form.childName" placeholder="e.g. Sam" />
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
      </div>

      <div v-if="currentStep === 1" class="form-grid">
        <div class="form-group full-row">
          <label>Current habits that need support</label>
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
          <label for="struggle">Biggest daily struggle</label>
          <textarea
            id="struggle"
            v-model.trim="form.struggle"
            rows="4"
            placeholder="For example: dinner battles, late bedtime, or after-school snacking."
          ></textarea>
        </div>
      </div>

      <div v-if="currentStep === 2" class="form-grid">
        <div class="form-group full-row">
          <label>Main concerns right now</label>
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
          <label for="confidence">Confidence level</label>
          <select id="confidence" v-model="form.confidence">
            <option disabled value="">Choose confidence level</option>
            <option>Very confident</option>
            <option>Somewhat confident</option>
            <option>Need gentle support</option>
          </select>
        </div>
        <div class="form-group">
          <label for="support-style">Preferred support style</label>
          <select id="support-style" v-model="form.supportStyle">
            <option disabled value="">Choose support style</option>
            <option>Daily micro-actions</option>
            <option>Weekly focus plan</option>
            <option>Visual dashboard nudges</option>
          </select>
        </div>
      </div>

      <div v-if="currentStep === 3" class="preview-stack">
        <article class="dashboard-card preview-card">
          <h3>{{ namePreview }}'s starter plan preview</h3>
          <ul>
            <li><strong>Top habits:</strong> {{ form.habits.join(', ') }}</li>
            <li><strong>Main concerns:</strong> {{ form.concerns.join(', ') }}</li>
            <li><strong>Support mode:</strong> {{ form.supportStyle }}</li>
          </ul>
          <p class="preview-note">You can retake this quiz anytime from the parent dashboard.</p>
        </article>
      </div>

      <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>

      <div class="form-actions wizard-actions">
        <button
          v-if="currentStep > 0"
          type="button"
          class="btn btn-outline-neutral"
          @click="currentStep -= 1"
        >
          Back
        </button>
        <button
          v-if="currentStep < steps.length - 1"
          type="button"
          class="btn btn-coral"
          @click="goNext"
        >
          Continue
        </button>
        <button v-else type="button" class="btn btn-coral" @click="submitQuiz">Generate my action plan</button>
      </div>
    </section>
  </main>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'

const router = useRouter()
const { savePlan } = useFamilyPlanStore()

const form = reactive({
  childName: '',
  ageRange: '',
  habits: [],
  concerns: [],
  struggle: '',
  confidence: '',
  supportStyle: '',
})

const steps = [
  { title: 'Step 1: Family basics', subtitle: 'Tell us who this plan is for.' },
  { title: 'Step 2: Habit baseline', subtitle: 'Pick habits and current friction points.' },
  { title: 'Step 3: Parent priorities', subtitle: 'Capture concerns and support style.' },
  { title: 'Step 4: Confirm plan', subtitle: 'Review your personalized starter setup.' },
]

const habitOptions = ['Balanced meals', 'Daily movement', 'Bedtime routine', 'Morning routine']
const concernOptions = ['Nutrition', 'Physical activity', 'Sleep consistency', 'Routine battles']

const currentStep = ref(0)
const errorMessage = ref('')

const activeStep = computed(() => steps[currentStep.value])
const progressPercent = computed(() => ((currentStep.value + 1) / steps.length) * 100)
const namePreview = computed(() => form.childName || 'your child')

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
    if (!form.childName || !form.ageRange) {
      errorMessage.value = 'Please enter your child name and age range.'
      return false
    }
  }

  if (currentStep.value === 1) {
    if (!form.habits.length || !form.struggle) {
      errorMessage.value = 'Select at least one habit and describe your daily challenge.'
      return false
    }
  }

  if (currentStep.value === 2) {
    if (!form.concerns.length || !form.confidence || !form.supportStyle) {
      errorMessage.value = 'Please complete all parent priority fields.'
      return false
    }
  }

  return true
}

function goNext() {
  if (!validateStep()) {
    return
  }
  currentStep.value += 1
}

function createRecommendations() {
  const focusArea = form.concerns[0]
  const primaryHabit = form.habits[0]

  return [
    {
      title: 'Daily mission',
      description: `Try one ${primaryHabit.toLowerCase()} action this afternoon and celebrate effort, not perfection.`,
    },
    {
      title: 'Family cue',
      description: `Because ${form.struggle.toLowerCase()}, set a visible cue (fridge note or timer) before the hard moment starts.`,
    },
    {
      title: 'Weekly insight',
      description: `${focusArea} is your highest-impact area. Focus on one tiny repeatable win for the next 7 days.`,
    },
  ]
}

function submitQuiz() {
  if (!validateStep()) {
    return
  }

  const recommendations = createRecommendations()

  savePlan({
    ...form,
    recommendations,
    nextAction: recommendations[0].description,
    mission: `Complete 3 ${form.habits[0].toLowerCase()} wins this week with ${form.childName}.`,
    streakDays: 2,
  })

  router.push('/parent-dashboard')
}
</script>