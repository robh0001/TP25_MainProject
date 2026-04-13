<template>
  <main class="page-main container section-gap">
    <section class="dashboard-hero coral-soft">
      <div>
        <p class="eyebrow">Parent dashboard</p>
        <h1>{{ childName }}'s family health plan</h1>
        <p class="hero-subtext narrow-copy">
          A detailed, practical view of what is going well, what needs support, and exactly what to do next.
        </p>
      </div>
      <RouterLink to="/parent-quiz" class="btn btn-coral link-btn">Retake quiz</RouterLink>
    </section>

    <section class="parent-summary-grid">
      <article class="form-card">
        <h2>Family profile</h2>
        <p><strong>Child age:</strong> {{ state.ageRange || 'Not set yet' }}</p>
        <p><strong>Main concerns:</strong> {{ concernSummary }}</p>
        <p><strong>Current habits to improve:</strong> {{ habitSummary }}</p>
        <p><strong>Parent confidence:</strong> {{ state.confidence || 'Not set yet' }}</p>
      </article>

      <article class="form-card">
        <h2>Why this matters this week</h2>
        <p>{{ weeklyNarrative }}</p>
        <ul class="detail-list">
          <li><strong>Risk if ignored:</strong> {{ riskNarrative }}</li>
          <li><strong>Expected win:</strong> {{ winNarrative }}</li>
          <li><strong>Best support style:</strong> {{ state.supportStyle || 'Daily micro-actions' }}</li>
        </ul>
      </article>
    </section>

    <section class="dashboard-grid">
      <article v-for="metric in metrics" :key="metric.title" class="dashboard-card">
        <h3>{{ metric.title }}</h3>
        <p>{{ metric.message }}</p>
        <div class="meter-row">
          <div class="meter-track">
            <div class="meter-fill" :style="{ width: `${metric.score}%` }"></div>
          </div>
          <span>{{ metric.score }}%</span>
        </div>
        <div class="metric-pill" :class="metric.pillClass">{{ metric.pill }}</div>
      </article>
    </section>

    <section class="insight-grid">
      <article class="form-card action-card">
        <h2>What to do next</h2>
        <p>{{ nextAction }}</p>
        <p class="insight-note">Streak: {{ streakDays }} days of consistent effort.</p>
      </article>

      <article class="form-card action-card mission-card">
        <h2>Daily family mission</h2>
        <p>{{ mission }}</p>
        <button type="button" class="btn btn-primary" @click="completeMission">Mark mission done (+20 XP)</button>
      </article>
    </section>

    <section class="parent-summary-grid">
      <article class="form-card">
        <h2>7-day action roadmap</h2>
        <ol class="detail-list numbered">
          <li v-for="step in weeklyRoadmap" :key="step">
            {{ step }}
          </li>
        </ol>
      </article>
      <article class="form-card">
        <h2>Daily routine guide</h2>
        <ul class="detail-list">
          <li><strong>Morning:</strong> Breakfast + hydration check before school.</li>
          <li><strong>After school:</strong> {{ afterSchoolRoutine }}</li>
          <li><strong>Evening:</strong> Keep one calm routine cue before bedtime.</li>
          <li><strong>Parent note:</strong> Celebrate effort, not perfection.</li>
        </ul>
      </article>
    </section>

    <section class="recommendation-list">
      <article v-for="recommendation in recommendations" :key="recommendation.title" class="dashboard-card recommendation-card">
        <p class="recommendation-title">{{ recommendation.title }}</p>
        <p>{{ recommendation.description }}</p>
      </article>
    </section>
  </main>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'

const { state, savePlan } = useFamilyPlanStore()

const childName = computed(() => state.childName || 'Your child')
const nextAction = computed(
  () => state.nextAction || 'Take the parent quiz to unlock a personalized next action.'
)
const mission = computed(() => state.mission || 'Complete one healthy habit win together today.')
const streakDays = computed(() => state.streakDays || 0)
const concernSummary = computed(() =>
  state.concerns.length ? state.concerns.join(', ') : 'Nutrition, activity, sleep, and routine'
)
const habitSummary = computed(() =>
  state.habits.length ? state.habits.join(', ') : 'Balanced meals and bedtime consistency'
)

const recommendations = computed(() =>
  state.recommendations.length
    ? state.recommendations
    : [
        {
          title: 'Starter tip',
          description: 'Complete onboarding to generate recommendations tailored to your child.',
        },
      ]
)

const weeklyNarrative = computed(() => {
  if (state.concerns.includes('Sleep consistency')) {
    return `${childName.value} may struggle with energy and mood if sleep stays inconsistent. Prioritizing bedtime structure can improve appetite, attention, and after-school behavior.`
  }
  if (state.concerns.includes('Nutrition')) {
    return `${childName.value} needs consistent fuel through the day. Better snack quality can stabilize energy, reduce irritability, and support healthy growth habits.`
  }
  return `${childName.value}'s plan is focused on consistency. One repeated healthy action each day is the strongest predictor of long-term habit success.`
})

const riskNarrative = computed(() => {
  if (state.concerns.includes('Routine battles')) return 'Daily friction increases and healthy habits become harder to sustain.'
  if (state.concerns.includes('Physical activity')) return 'Lower movement can affect mood regulation and sleep quality.'
  return 'Inconsistent habits reduce progress and make routines harder to maintain.'
})

const winNarrative = computed(() => {
  if (state.concerns.includes('Nutrition')) return 'Higher energy and fewer snack-related conflicts after school.'
  if (state.concerns.includes('Sleep consistency')) return 'Calmer evenings and more predictable morning routines.'
  return 'Better consistency with less parent-child conflict across the day.'
})

const weeklyRoadmap = computed(() => [
  `Day 1-2: Start small with "${nextAction.value}" and keep expectations realistic.`,
  'Day 3-4: Repeat the same action at the same time to build routine memory.',
  `Day 5: Review what worked and simplify where resistance appeared (${state.struggle || 'common routine friction'}).`,
  `Day 6-7: Celebrate wins and set next week focus around ${state.concerns[0] || 'your priority concern'}.`,
])

const afterSchoolRoutine = computed(() => {
  if (state.concerns.includes('Physical activity')) return '15-20 minutes movement before screen time.'
  if (state.concerns.includes('Nutrition')) return 'Prepare one visible healthy snack before pickup.'
  return 'Transition with one predictable cue and a small healthy habit task.'
})

const metrics = computed(() => [
  {
    title: 'Nutrition',
    message: 'Small swaps are easier than full meal overhauls this week.',
    score: state.concerns.includes('Nutrition') ? 45 : 70,
    pill: 'Low-friction snack swap ready',
    pillClass: 'coral-pill',
  },
  {
    title: 'Physical activity',
    message: 'After-school movement is your strongest consistency window.',
    score: state.concerns.includes('Physical activity') ? 52 : 74,
    pill: '15 minute mission suggested',
    pillClass: 'mint-pill',
  },
  {
    title: 'Sleep',
    message: 'Sleep consistency drives mood and appetite quality.',
    score: state.concerns.includes('Sleep consistency') ? 41 : 68,
    pill: 'Bedtime anchor routine',
    pillClass: 'sky-pill',
  },
  {
    title: 'Routine',
    message: 'One repeated cue before tough moments can reduce friction.',
    score: state.concerns.includes('Routine battles') ? 48 : 72,
    pill: 'One-goal weekly focus',
    pillClass: 'lilac-pill',
  },
])

function completeMission() {
  savePlan({
    ...state,
    streakDays: state.streakDays + 1,
  })
}
</script>