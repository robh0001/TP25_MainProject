<template>
  <div class="entry-page" :class="{ loaded: isLoaded }">
    <!-- Background -->
    <div class="entry-bg">
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
    <header class="entry-site-header">
      <RouterLink to="/" class="entry-brand">
        <div class="entry-brand-icon">
          <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
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

      <RouterLink to="/" class="entry-header-btn">
        Back home
      </RouterLink>
    </header>

    <!-- Main -->
    <main class="entry-main">
      <section class="entry-card">
        <div class="entry-intro">
          <p class="entry-step-kicker">
            <span class="entry-kicker-dot"></span>
            Parent access
          </p>

          <h1>
            Let's build a calmer
            <span>family routine.</span>
          </h1>

          <p class="entry-intro-text">
            Start a new plan or open your saved family dashboard.
          </p>
        </div>

        <div class="entry-options">
          <!-- New parent -->
          <article class="entry-path-card entry-path-card--new">
            <div class="entry-path-icon entry-path-icon--new">
              <span>&#127804;</span>
            </div>

            <h2>New parent</h2>
            <p>Create your family plan.</p>

            <div class="entry-form-block">
              <label for="new-username">Family code</label>
              <input
                id="new-username"
                v-model.trim="newUsername"
                type="text"
                placeholder="e.g. sunnyfamily01"
                autocomplete="off"
              />

              <p v-if="newUserError" class="entry-form-error">
                {{ newUserError }}
              </p>

              <button type="button" class="entry-btn-primary" @click="startNewUser">
                Start new plan
              </button>
            </div>
          </article>

          <!-- Returning parent -->
          <article class="entry-path-card entry-path-card--return">
            <div class="entry-path-icon entry-path-icon--return">
              <span>&#128273;</span>
            </div>

            <h2>Returning parent</h2>
            <p>Continue your progress.</p>

            <div class="entry-form-block">
              <label for="returning-username">Family code</label>
              <input
                id="returning-username"
                v-model.trim="returningUsername"
                type="text"
                placeholder="Enter your code"
                autocomplete="off"
              />

              <p v-if="returningUserError" class="entry-form-error">
                {{ returningUserError }}
              </p>

              <button type="button" class="entry-btn-secondary" @click="continueReturningUser">
                Open dashboard
              </button>
            </div>
          </article>
        </div>

        <p class="entry-privacy-note">
          Use a simple code you can remember. No personal details needed.
        </p>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'

const router = useRouter()
const { state, savePlan, clearPlan } = useFamilyPlanStore()

const API_BASE_URL = import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL

const isLoaded = ref(false)
const newUsername = ref('')
const returningUsername = ref('')
const newUserError = ref('')
const returningUserError = ref('')

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
    newUserError.value = 'Please choose a family code before continuing.'
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
      newUserError.value = 'That family code is already taken. Please choose another one.'
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
      returningUserError.value = 'We could not find that family plan. Check your code or start a new plan.'
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