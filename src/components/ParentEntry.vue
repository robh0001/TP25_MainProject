<!--
  ParentEntryPage.vue

  Parent entry page for HealthyKids.

  Main features:
  - Shows the brand header and back home link.
  - Provides access for new and returning parents.
  - Lets new parents create a plan with a family code.
  - Checks whether the family code is available.
  - Lets returning parents reopen a saved dashboard.
  - Loads saved profiles from the parent profiles API.
  - Stores family code/profile data in the shared family plan store.
  - Redirects users to the quiz, dashboard, or requested redirect page.

  API requirement:
  - Requires VITE_PARENT_PROFILES_API_BASE_URL.
  - Checks new codes with GET /check-username?username={familyCode}.
  - Loads returning profiles with GET /{familyCode}.
  - Shows clear errors if the API URL is missing or the profile is not found.

  Accessibility:
  - Uses aria-labels, aria-labelledby, aria-describedby, aria-invalid, role="alert", and aria-live.
  - Uses proper form labels and keyboard-friendly links/buttons.
  - Supports hover-to-read with data-hover-read-text.
  - Hides decorative visuals with aria-hidden="true".
-->

<template>
  <div class="entry-page" :class="{ loaded: isLoaded }">
    <!-- Background -->
    <div class="entry-bg" aria-hidden="true">
      <img
        class="entry-bg__img"
        src="https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=2400&q=90"
        alt=""
        aria-hidden="true"
      />
      <div class="entry-bg__overlay"></div>
      <div class="entry-bg__grain"></div>
    </div>

    <!-- Header -->
    <header class="entry-site-header" aria-label="HealthyKids site header">
      <!-- HealthyKids brand link that returns users to the home page -->
    </header>
    <!-- Main -->
    <main class="entry-main" id="main-content">
      <FamilyJourneyBar :current-step="1" />
      <!-- Main card containing both new and returning parent options -->
      <section class="entry-card" aria-labelledby="entry-page-title">
        <!-- Introductory text for the parent access page -->
        <div class="entry-intro">
          
          <p class="entry-step-kicker" aria-label="Parent access">
            <span class="entry-kicker-dot" aria-hidden="true"></span>
            Parent access
          </p>

          <h1 id="entry-page-title">
            Let's build a calmer
            <span>family routine.</span>
          </h1>

          <p class="entry-intro-text" id="entry-page-description">
            Start a new plan or open your saved family dashboard.
          </p>
        </div>

        <!-- Two parent access paths: new parent and returning parent -->
        <div class="entry-options" aria-label="Parent access options">
          <!-- New parent -->
          <article
            class="entry-path-card entry-path-card--new"
            aria-labelledby="new-parent-title"
            aria-describedby="new-parent-description"
          >
            <!-- Decorative icon for the new parent option -->
            <div class="entry-path-icon entry-path-icon--new" aria-hidden="true">
              <span>&#127804;</span>
            </div>

            <h2 id="new-parent-title">New parent</h2>
            <p id="new-parent-description">Create your family plan.</p>

            <!-- Form for creating a new family plan -->
            <form class="entry-form-block" @submit.prevent="startNewUser" novalidate>
              <label for="new-username">Family code</label>
              <input
                id="new-username"
                v-model.trim="newUsername"
                type="text"
                placeholder="e.g. sunnyfamily01"
                autocomplete="off"
                inputmode="text"
                aria-label="New family code. Example: sunnyfamily01"
                data-hover-read-text="Family code. Enter a simple code for your new family plan. Example: sunnyfamily01."
                :aria-invalid="newUserError ? 'true' : 'false'"
                :aria-describedby="newUserError ? 'new-username-error entry-code-help' : 'entry-code-help'"
              />

              <!-- Screen-reader-only guidance for the new family code field -->
              <p id="entry-code-help" class="entry-sr-only">
                Choose a simple family code without personal details.
              </p>

              <!-- Validation error shown when the new family code is missing or unavailable -->
              <p
                v-if="newUserError"
                id="new-username-error"
                class="entry-form-error"
                role="alert"
                aria-live="assertive"
                :data-hover-read-text="newUserError"
              >
                {{ newUserError }}
              </p>     

              <button
                type="submit"
                class="entry-btn-primary"
                :aria-busy="false"
              >
                Start new plan
              </button>
            </form>
          </article>

          <!-- Returning parent -->
          <article
            class="entry-path-card entry-path-card--return"
            aria-labelledby="returning-parent-title"
            aria-describedby="returning-parent-description"
          >
            <!-- Decorative icon for the returning parent option -->
            <div class="entry-path-icon entry-path-icon--return" aria-hidden="true">
              <span>&#128273;</span>
            </div>

            <h2 id="returning-parent-title">Returning parent</h2>
            <p id="returning-parent-description">Continue your progress.</p>

            <!-- Form for loading an existing family dashboard -->
            <form class="entry-form-block" @submit.prevent="continueReturningUser" novalidate>
              <label for="returning-username">Family code</label>
              <input
                id="returning-username"
                v-model.trim="returningUsername"
                type="text"
                placeholder="Enter your code"
                autocomplete="off"
                inputmode="text"
                aria-label="Returning family code. Enter your saved family code."
                data-hover-read-text="Family code. Enter your saved family code to open your dashboard."
                :aria-invalid="returningUserError ? 'true' : 'false'"
                :aria-describedby="returningUserError ? 'returning-username-error returning-code-help' : 'returning-code-help'"
              />

              <!-- Screen-reader-only guidance for the returning family code field -->
              <p id="returning-code-help" class="entry-sr-only">
                Enter the family code you used when creating your plan.
              </p>

              <!-- Validation or loading error for returning users -->
              <p
                v-if="returningUserError"
                id="returning-username-error"
                class="entry-form-error"
                role="alert"
                aria-live="assertive"
                :data-hover-read-text="returningUserError"
              >
                {{ returningUserError }}
              </p>

              <button
                type="submit"
                class="entry-btn-secondary"
                :aria-busy="false"
              >
                Open dashboard
              </button>
            </form>
          </article>
        </div>

        <!-- Privacy note reminding users not to use personal details -->
        <p class="entry-privacy-note">
          Use a simple code you can remember. No personal details needed.
        </p>
      </section>
    </main>

    <!-- Footer copied from the home page style for visual consistency -->
    <footer
      class="home-footer entry-home-footer"
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
import { ref, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'
import { useHoverToRead } from '../composables/useHoverToRead'
import { useSpeechSynthesis } from '../composables/useSpeechSynthesis'
import FamilyJourneyBar from '../components/FamilyJourneyBar.vue'

// Gives access to Vue Router navigation.
const router = useRouter()

// Gives access to the shared family plan store.
const { state, savePlan, clearPlan } = useFamilyPlanStore()

// Parent profile API base URL from the Vite environment variables.
const API_BASE_URL = import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL

// Controls the entry page loaded animation.
const isLoaded = ref(false)

// Stores the new family code typed by a new parent.
const newUsername = ref('')

// Stores the family code typed by a returning parent.
const returningUsername = ref('')

// Stores validation or API errors for the new parent form.
const newUserError = ref('')

// Stores validation or API errors for the returning parent form.
const returningUserError = ref('')

// Reads whether the hover-to-read accessibility feature is enabled.
const { isHoverToReadEnabled } = useHoverToRead()

// Provides text-to-speech output for form error messages.
const { speakText } = useSpeechSynthesis()

// Announces form errors aloud when hover-to-read is enabled.
function announceFormError(message) {
  if (!message) return

  if (isHoverToReadEnabled.value) {
    speakText(message)
  }
}

// Starts the page entrance animation after the component mounts.
onMounted(() => {
  setTimeout(() => {
    isLoaded.value = true
  }, 80)
})

// Normalises the family code so spacing and casing stay consistent.
function normalizeUsername(value) {
  return String(value || '').trim().toLowerCase().replace(/\s+/g, '')
}

// Saves the family code locally and updates the shared family plan store.
function saveUsernameSession(username) {
  localStorage.setItem('hk-parent-username', username)

  savePlan({
    ...state,
    username,
    userName: username,
    user_name: username,
  })
}
const entrySteps = [
  {
    number: '01',
    label: 'Create profile',
  },
  {
    number: '02',
    label: 'Guided plan',
  },
  {
    number: '03',
    label: 'Daily actions',
  },
  {
    number: '04',
    label: 'Kids zone',
  },
]
// Starts the flow for a new parent after checking whether the family code is available.
async function startNewUser() {
  newUserError.value = ''

  if (!newUsername.value) {
    const message = 'Please choose a family code before continuing.'
    newUserError.value = message
    announceFormError(message)
    return
  }

  if (!API_BASE_URL) {
    newUserError.value = 'Missing API URL. Please check VITE_PARENT_PROFILES_API_BASE_URL.'
    return
  }

  const username = normalizeUsername(newUsername.value)

  try {
    const response = await fetch(
      `${API_BASE_URL}/check-username?username=${encodeURIComponent(username)}`
    )

    const data = await response.json().catch(() => ({}))

    if (!response.ok) {
      throw new Error(data.error || data.message || 'Family code check failed')
    }

    if (!data.available) {
      const message = 'That family code is already taken. Please choose another one.'
      newUserError.value = message
      announceFormError(message)
      return
    }

    clearPlan()
    saveUsernameSession(username)

    router.push({
      path: '/parent-quiz',
      query: { username },
    })
  } catch (error) {
    console.error('Family code check failed:', error)
    newUserError.value = 'Unable to check family code right now. Please try again.'
  }
}

// Loads an existing family profile and sends the returning parent to the dashboard.
async function continueReturningUser() {
  returningUserError.value = ''

  if (!returningUsername.value) {
    returningUserError.value = 'Please enter your family code.'
    return
  }

  if (!API_BASE_URL) {
    returningUserError.value = 'Missing API URL. Please check VITE_PARENT_PROFILES_API_BASE_URL.'
    return
  }

  const username = normalizeUsername(returningUsername.value)

  try {
    const response = await fetch(
      `${API_BASE_URL}/${encodeURIComponent(username)}`
    )

    const data = await response.json().catch(() => ({}))

    if (response.status === 404) {
      const message = 'We could not find that family plan. Check your code or start a new plan.'
      returningUserError.value = message
      announceFormError(message)
      return
    }

    if (!response.ok) {
      throw new Error(data.error || data.message || 'Load failed')
    }

    savePlan({
      ...data,
      username: data.username || username,
      userName: data.userName || data.username || username,
      user_name: data.user_name || data.username || username,

      roadmapProgress: data.roadmapProgress || data.roadmap_progress || {},
      roadmap_progress: data.roadmap_progress || data.roadmapProgress || {},

      todaySchedule: data.todaySchedule || data.today_schedule || {},
      today_schedule: data.today_schedule || data.todaySchedule || {},

      plannerOverrides: data.plannerOverrides || data.planner_overrides || {},
      planner_overrides: data.planner_overrides || data.plannerOverrides || {},
    })

    localStorage.setItem('hk-parent-username', username)

    const redirectPath = router.currentRoute.value.query.redirect

    router.push({
      path: typeof redirectPath === 'string' ? redirectPath : '/parent-dashboard',
      query: { username },
    })
  } catch (error) {
    console.error('Returning profile load failed:', error)
    returningUserError.value = 'Unable to load your profile right now. Please try again.'
  }
}
</script>