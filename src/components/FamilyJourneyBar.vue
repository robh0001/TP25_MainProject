<!--
  FamilyJourneyBar.vue

  This component creates the reusable HelthyKidz journey progress bar shown across
  the parent flow pages.

  Purpose:
  - Shows the 5-step family journey:
    1. Get Started
    2. Build Profile
    3. Today's Plan
    4. 4-week Roadmap
    5. Meal Ideas
  - Highlights the current page using the currentStep prop.
  - Marks previous steps as complete.
  - Locks future steps until the user has:
    - entered or opened a family code, and
    - visited the previous step.
  - Shows helpful hover/read-aloud messages when a step is locked.
  - Stores the highest step reached in localStorage so progress is remembered
    across page refreshes.
-->

<template>
    <nav
      class="dashboard-journey"
      aria-label="HelthyKidz website journey"
      data-hover-read-text="Website journey. Get started, build profile, today's plan, four week roadmap, meal ideas."
    >
      <!-- Loop through each journey step and render it as either an open link or a locked button -->
      <template v-for="step in journeySteps" :key="step.number">
        <!-- Open step: user is allowed to visit this page -->
        <RouterLink
          v-if="canOpenStep(step)"
          :to="step.to"
          class="dashboard-journey-item"
          :class="getStepClass(step)"
          :aria-current="step.number === currentStep ? 'step' : undefined"
          :aria-label="getStepAriaLabel(step)"
          :data-hover-read-text="getStepAriaLabel(step)"
          @click="markStepSeen(step.number)"
        >
          <span class="dashboard-journey-badge">{{ step.number }}</span>
          <span class="dashboard-journey-label">{{ step.label }}</span>
  
          <!-- Connector line between journey steps -->
          <span
            v-if="step.number !== journeySteps.length"
            class="dashboard-journey-line"
            aria-hidden="true"
          ></span>
        </RouterLink>
  
        <!-- Locked step: user cannot visit this page yet -->
        <button
          v-else
          type="button"
          class="dashboard-journey-item dashboard-journey-item--locked"
          :class="getStepClass(step)"
          :aria-label="getLockedMessage(step)"
          :title="getLockedMessage(step)"
          :data-hover-read-text="getLockedMessage(step)"
          @click="handleLockedStep(step)"
        >
          <span class="dashboard-journey-badge">{{ step.number }}</span>
          <span class="dashboard-journey-label">{{ step.label }}</span>
  
          <!-- Connector line between journey steps -->
          <span
            v-if="step.number !== journeySteps.length"
            class="dashboard-journey-line"
            aria-hidden="true"
          ></span>
        </button>
      </template>
    </nav>
  </template>
  
  <script setup>
  import { computed, onMounted } from 'vue'
  import { RouterLink, useRouter } from 'vue-router'
  import { useFamilyPlanStore } from '../stores/familyPlanStore'
  
  // Receives the active step number from the page using this component.
  const props = defineProps({
    currentStep: {
      type: Number,
      required: true,
    },
  })
  
  // Router is used to redirect users when they click a locked step.
  const router = useRouter()
  
  // Shared family plan store gives access to the saved username/family code.
  const { state } = useFamilyPlanStore()
  
  // LocalStorage keys used to remember family access and journey progress.
  const STORAGE_USERNAME_KEY = 'hk-parent-username'
  const STORAGE_HIGHEST_STEP_KEY = 'hk-family-journey-highest-step'
  
  // Main journey step configuration.
  // Each item controls the step number, label, and route.
  const journeySteps = [
    {
      number: 1,
      label: 'Get Started',
      to: '/parent-entry',
    },
    {
      number: 2,
      label: 'Build Profile',
      to: '/parent-quiz',
    },
    {
      number: 3,
      label: "Today's plan",
      to: '/parent-dashboard',
    },
    {
      number: 4,
      label: '4-week roadmap',
      to: '/parent-roadmap',
    },
    {
      number: 5,
      label: 'Meal Ideas',
      to: '/parent-nutrition-tools',
    },
  ]
  
  // Gets the current family code from the store first,
  // then falls back to localStorage if the page was refreshed.
  const familyCode = computed(() =>
    String(
      state.username ||
        state.userName ||
        state.user_name ||
        localStorage.getItem(STORAGE_USERNAME_KEY) ||
        ''
    ).trim()
  )
  
  // Checks whether a family code exists.
  // Protected journey steps are locked until this is true.
  const hasFamilyCode = computed(() => Boolean(familyCode.value))
  
  // Reads the highest journey step the user has reached.
  // Defaults to step 1 when no progress is stored yet.
  const highestSeenStep = computed(() => {
    const storedStep = Number(localStorage.getItem(STORAGE_HIGHEST_STEP_KEY) || '1')
  
    return Number.isFinite(storedStep) && storedStep > 0 ? storedStep : 1
  })
  
  // Saves the highest step the user has visited.
  // This prevents progress from being lost after refreshing the page.
  function markStepSeen(stepNumber) {
    const currentHighest = Number(localStorage.getItem(STORAGE_HIGHEST_STEP_KEY) || '1')
    const nextHighest = Math.max(currentHighest, stepNumber)
  
    localStorage.setItem(STORAGE_HIGHEST_STEP_KEY, String(nextHighest))
  }
  
  // Checks whether the user has already visited the previous step.
  // Example: Step 4 requires Step 3 to have been reached first.
  function hasSeenPreviousStep(step) {
    if (step.number === 1) return true
  
    return highestSeenStep.value >= step.number - 1
  }
  
  // Controls whether a journey step should be clickable.
  // Step 1 is always available.
  // Later steps require a family code and previous-step progress.
  function canOpenStep(step) {
    if (step.number === 1) return true
  
    return hasFamilyCode.value && hasSeenPreviousStep(step)
  }
  
  // Applies visual classes for current and completed steps.
  function getStepClass(step) {
    return {
      'dashboard-journey-item--active': step.number === props.currentStep,
      'dashboard-journey-item--complete': step.number < props.currentStep && canOpenStep(step),
    }
  }
  
  // Builds accessible text for open steps.
  // This is used by screen readers and hover-to-read.
  function getStepAriaLabel(step) {
    if (step.number === props.currentStep) {
      return `Step ${step.number} current. ${step.label}.`
    }
  
    if (step.number < props.currentStep) {
      return `Step ${step.number} complete. ${step.label}.`
    }
  
    return `Step ${step.number}. ${step.label}.`
  }
  
  // Builds the message shown when a step is locked.
  function getLockedMessage(step) {
    if (!hasFamilyCode.value) {
      return `Step ${step.number} locked. Enter or open your family code first.`
    }
  
    return `Step ${step.number} locked. Complete the previous step first.`
  }
  
  // Handles clicks on locked steps.
  // If there is no family code, send the user back to the parent entry page.
  function handleLockedStep() {
    if (!hasFamilyCode.value) {
      router.push('/parent-entry')
    }
  }
  
  // When the component loads, mark the current page as seen.
  onMounted(() => {
    markStepSeen(props.currentStep)
  })
  </script>