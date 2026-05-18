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
      <RouterLink to="/" class="entry-brand" aria-label="Go to HealthyKids home page">
        <div class="entry-brand-icon" aria-hidden="true">
          <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg" focusable="false">
            <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2" />
            <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor" />
            <path
              d="M18 13C15.5 15.5 15 19 18 23"
              stroke="white"
              stroke-width="1.2"
              stroke-linecap="round"
              fill="none"
              opacity="0.55"
            />
          </svg>
        </div>
        <span>HealthyKids</span>
      </RouterLink>

      <RouterLink to="/" class="entry-header-btn" aria-label="Go back to home page">
        Back home
      </RouterLink>
    </header>

    <!-- Main -->
    <main class="entry-main" id="main-content">
      <section class="entry-card" aria-labelledby="entry-page-title">
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

        <div class="entry-options" aria-label="Parent access options">
          <!-- New parent -->
          <article
            class="entry-path-card entry-path-card--new"
            aria-labelledby="new-parent-title"
            aria-describedby="new-parent-description"
          >
            <div class="entry-path-icon entry-path-icon--new" aria-hidden="true">
              <span>&#127804;</span>
            </div>

            <h2 id="new-parent-title">New parent</h2>
            <p id="new-parent-description">Create your family plan.</p>

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
              <p id="entry-code-help" class="entry-sr-only">
                Choose a simple family code without personal details.
              </p>

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
            <div class="entry-path-icon entry-path-icon--return" aria-hidden="true">
              <span>&#128273;</span>
            </div>

            <h2 id="returning-parent-title">Returning parent</h2>
            <p id="returning-parent-description">Continue your progress.</p>

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
              <p id="returning-code-help" class="entry-sr-only">
                Enter the family code you used when creating your plan.
              </p>

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

        <p class="entry-privacy-note">
          Use a simple code you can remember. No personal details needed.
        </p>
      </section>
    </main>

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

const router = useRouter()
const { state, savePlan, clearPlan } = useFamilyPlanStore()

const API_BASE_URL = import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL

const isLoaded = ref(false)
const newUsername = ref('')
const returningUsername = ref('')
const newUserError = ref('')
const returningUserError = ref('')

const { isHoverToReadEnabled } = useHoverToRead()
const { speakText } = useSpeechSynthesis()

function announceFormError(message) {
  if (!message) return

  if (isHoverToReadEnabled.value) {
    speakText(message)
  }
}

onMounted(() => {
  setTimeout(() => {
    isLoaded.value = true
  }, 80)
})

function normalizeUsername(value) {
  return String(value || '').trim().toLowerCase().replace(/\s+/g, '')
}

function saveUsernameSession(username) {
  localStorage.setItem('hk-parent-username', username)

  savePlan({
    ...state,
    username,
    userName: username,
    user_name: username,
  })
}

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