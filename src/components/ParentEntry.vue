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
    <header class="site-header">
      <RouterLink to="/" class="brand">
        <div class="brand-icon">
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

      <RouterLink to="/" class="header-btn">
        ← Back home
      </RouterLink>
    </header>

    <!-- Main -->
    <main class="entry-main">
      <section class="entry-card">
        <div class="entry-intro">
          <p class="step-kicker">
            <span class="kicker-dot"></span>
            Parent access
          </p>

          <h1>
            Let's build a calmer
            <span>family routine.</span>
          </h1>

          <p class="intro-text">
            Start a new plan or open your saved family dashboard.
          </p>
        </div>

        <div class="entry-options">
          <!-- New parent -->
          <article class="path-card path-card--new">
            <div class="path-icon path-icon--new">🌼</div>

            <h2>New parent</h2>
            <p>Create your family plan.</p>

            <div class="form-block">
              <label for="new-username">Family code</label>
              <input
                id="new-username"
                v-model.trim="newUsername"
                type="text"
                placeholder="e.g. sunnyfamily01"
                autocomplete="off"
              />

              <p v-if="newUserError" class="form-error">{{ newUserError }}</p>

              <button type="button" class="btn-primary" @click="startNewUser">
                Start new plan →
              </button>
            </div>
          </article>

          <!-- Returning parent -->
          <article class="path-card path-card--return">
            <div class="path-icon path-icon--return">🔑</div>

            <h2>Returning parent</h2>
            <p>Continue your progress.</p>

            <div class="form-block">
              <label for="returning-username">Family code</label>
              <input
                id="returning-username"
                v-model.trim="returningUsername"
                type="text"
                placeholder="Enter your code"
                autocomplete="off"
              />

              <p v-if="returningUserError" class="form-error">{{ returningUserError }}</p>

              <button type="button" class="btn-secondary" @click="continueReturningUser">
                Open dashboard →
              </button>
            </div>
          </article>
        </div>

        <p class="privacy-note">
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
const { savePlan, clearPlan } = useFamilyPlanStore()

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
  return value.trim().toLowerCase().replace(/\s+/g, '')
}

async function startNewUser() {
  newUserError.value = ''

  if (!newUsername.value) {
    newUserError.value = 'Please choose a family code before continuing.'
    return
  }

  const username = normalizeUsername(newUsername.value)

  try {
    const response = await fetch(
      `${import.meta.env.VITE_PARENT_PROFILE_CHECK_API_BASE_URL}/test/check-username?username=${encodeURIComponent(username)}`
    )

    if (!response.ok) throw new Error('Family code check failed')

    const data = await response.json()

    if (!data.available) {
      newUserError.value = 'That family code is already taken. Please choose another one.'
      return
    }

    clearPlan()
    savePlan({ username })
    router.push('/parent-quiz')
  } catch {
    newUserError.value = 'Unable to check family code right now. Please try again.'
  }
}

async function continueReturningUser() {
  returningUserError.value = ''

  if (!returningUsername.value) {
    returningUserError.value = 'Please enter your family code.'
    return
  }

  const username = normalizeUsername(returningUsername.value)

  try {
    const response = await fetch(
      `${import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL}/parent-profiles/${encodeURIComponent(username)}`
    )

    const data = await response.json()

    if (response.status === 404) {
      returningUserError.value = 'We could not find that family plan. Check your code or start a new plan.'
      return
    }

    if (!response.ok) throw new Error(data.error || 'Load failed')

    savePlan(data)

    const redirectPath = router.currentRoute.value.query.redirect
    router.push(typeof redirectPath === 'string' ? redirectPath : '/parent-dashboard')
  } catch {
    returningUserError.value = 'Unable to load your profile right now. Please try again.'
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;1,300;1,400&family=DM+Sans:wght@400;500;600;700;800;900&display=swap');

:global(*),
:global(*::before),
:global(*::after) {
  box-sizing: border-box;
}


:global(body) {
  margin: 0;
  font-family: 'DM Sans', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
  overflow-y: auto;
}

.entry-page {
  --ink: #172033;
  --muted: #667085;

  --cream: #fff8ef;
  --coral: #ff725f;
  --coral-dark: #ed5f4d;
  --coral-soft: #fff0ec;

  --sage: #7a9b76;
  --sage-soft: #eef6ea;

  --navy: #172033;

  position: relative;
  inset: 0;
  overflow: hidden;
  color: var(--ink);
  background: #f7efe4;
  min-height: 100vh;
}

/* BACKGROUND */
.entry-bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.entry-bg__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center center;
  transform: scale(1.02);
  transition: transform 9s ease;
}

.loaded .entry-bg__img {
  transform: scale(1);
}

.entry-bg__overlay {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(
      90deg,
      rgba(255, 248, 239, 0.72) 0%,
      rgba(255, 248, 239, 0.48) 28%,
      rgba(255, 248, 239, 0.28) 52%,
      rgba(255, 248, 239, 0.18) 100%
    ),
    linear-gradient(
      180deg,
      rgba(255, 248, 239, 0.56) 0%,
      rgba(255, 248, 239, 0.12) 46%,
      rgba(23, 32, 51, 0.34) 100%
    ),
    radial-gradient(
      circle at 50% 48%,
      rgba(255, 248, 239, 0.32),
      transparent 34rem
    ),
    radial-gradient(
      circle at 24% 72%,
      rgba(255, 114, 95, 0.18),
      transparent 28rem
    ),
    radial-gradient(
      circle at 78% 22%,
      rgba(122, 155, 118, 0.18),
      transparent 28rem
    );
}

.entry-bg__grain {
  position: absolute;
  inset: 0;
  opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 180px;
}

/* HEADER */
.site-header {
  position: relative;
  z-index: 20;
  height: 68px;
  padding: 0 clamp(22px, 5vw, 64px);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--ink);
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.24rem;
  letter-spacing: -0.04em;
  font-weight: 400;
}

.brand-icon {
  width: 30px;
  height: 30px;
  display: grid;
  place-items: center;
  color: var(--sage);
  border-radius: 999px;
  background:
    linear-gradient(145deg, rgba(255, 114, 95, 0.24), rgba(122, 155, 118, 0.24)),
    rgba(255, 255, 255, 0.74);
  border: 1px solid rgba(23, 32, 51, 0.12);
  box-shadow: 0 8px 20px rgba(23, 32, 51, 0.08);
}

.header-btn {
  height: 42px;
  padding: 0 18px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  background: rgba(255, 248, 239, 0.76);
  border: 1px solid rgba(23, 32, 51, 0.1);
  box-shadow: 0 10px 26px rgba(23, 32, 51, 0.08);
  color: var(--ink);
  text-decoration: none;
  font-size: 0.84rem;
  font-weight: 900;
  backdrop-filter: blur(12px);
  transition:
    transform 0.2s ease,
    background 0.2s ease,
    box-shadow 0.2s ease;
}

.header-btn:hover {
  transform: translateY(-2px);
  background: #ffffff;
  box-shadow: 0 14px 34px rgba(23, 32, 51, 0.12);
}

/* MAIN */
.entry-main {
  position: relative;
  z-index: 5;
  height: calc(100vh - 68px);
  padding: 10px clamp(22px, 5vw, 64px) 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}


.entry-card {
  width: min(100%, 760px);
  padding: clamp(26px, 3.4vw, 38px);
  border-radius: 34px;
  background: rgba(255, 248, 239, 0.72);
  border: 1px solid rgba(255, 255, 255, 0.68);
  box-shadow:
    0 28px 76px rgba(23, 32, 51, 0.16),
    inset 0 1px 0 rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(14px);
  opacity: 0;
  transform: translateY(18px);
  transition:
    opacity 0.65s ease,
    transform 0.65s ease;
}

.loaded .entry-card {
  opacity: 1;
  transform: translateY(0);
}

/* INTRO */
.entry-intro {
  text-align: center;
}

.step-kicker {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 28px;
  padding: 0 12px;
  margin: 0 0 18px;
  border-radius: 999px;
  background: rgba(122, 155, 118, 0.16);
  border: 1px solid rgba(122, 155, 118, 0.28);
  color: #547650;
  font-size: 0.68rem;
  font-weight: 900;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.kicker-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--coral);
  box-shadow: 0 0 0 0 rgba(255, 114, 95, 0.42);
  animation: pulse 2.2s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(255, 114, 95, 0.42);
  }

  50% {
    box-shadow: 0 0 0 6px rgba(255, 114, 95, 0);
  }
}

.entry-intro h1 {
  max-width: 680px;
  margin: 0 auto;
  font-family: 'Fraunces', Georgia, serif;
  font-size: clamp(2.45rem, 4.4vw, 4.4rem);
  line-height: 0.98;
  letter-spacing: -0.06em;
  font-weight: 300;
  color: var(--ink);
}

.entry-intro h1 span {
  color: var(--coral);
  font-style: italic;
}

.intro-text {
  max-width: 500px;
  margin: 16px auto 28px;
  color: var(--muted);
  font-size: 0.98rem;
  line-height: 1.5;
}

/* OPTION CARDS */
.entry-options {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.path-card {
  padding: 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(23, 32, 51, 0.08);
  box-shadow: 0 10px 30px rgba(23, 32, 51, 0.06);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.path-card:hover {
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 46px rgba(23, 32, 51, 0.12);
}

.path-card--new {
  border-color: rgba(255, 114, 95, 0.28);
}

.path-icon {
  width: 42px;
  height: 42px;
  border-radius: 15px;
  display: grid;
  place-items: center;
  margin-bottom: 14px;
  font-size: 1.1rem;
}

.path-icon--new {
  background: var(--coral-soft);
  border: 1px solid rgba(255, 114, 95, 0.24);
}

.path-icon--return {
  background: var(--sage-soft);
  border: 1px solid rgba(122, 155, 118, 0.28);
}

.path-card h2 {
  margin: 0 0 6px;
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 400;
  font-size: 1.42rem;
  line-height: 1.12;
  letter-spacing: -0.04em;
  color: var(--ink);
}

.path-card p {
  margin: 0 0 18px;
  color: var(--muted);
  font-size: 0.88rem;
  line-height: 1.45;
}

/* FORM */
.form-block {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-block label {
  font-size: 0.78rem;
  font-weight: 900;
  color: var(--ink);
}

.form-block input {
  width: 100%;
  height: 44px;
  padding: 0 13px;
  border-radius: 13px;
  border: 1px solid rgba(23, 32, 51, 0.12);
  background: rgba(255, 255, 255, 0.9);
  color: var(--ink);
  font-family: 'DM Sans', sans-serif;
  font-size: 0.92rem;
  font-weight: 600;
  outline: none;
  transition:
    border-color 0.15s ease,
    box-shadow 0.15s ease,
    background 0.15s ease;
}

.form-block input:focus {
  border-color: rgba(255, 114, 95, 0.55);
  box-shadow: 0 0 0 4px rgba(255, 114, 95, 0.12);
  background: #ffffff;
}

.form-block input::placeholder {
  color: rgba(23, 32, 51, 0.32);
}

.form-error {
  margin: 0;
  color: #dc2626;
  font-size: 0.78rem;
  font-weight: 800;
}

.btn-primary,
.btn-secondary {
  width: 100%;
  height: 44px;
  margin-top: 4px;
  border: none;
  border-radius: 13px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.88rem;
  font-weight: 900;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    background 0.18s ease;
}

.btn-primary {
  background: var(--coral);
  color: #ffffff;
  box-shadow: 0 10px 24px rgba(255, 114, 95, 0.26);
}

.btn-primary:hover {
  background: var(--coral-dark);
  transform: translateY(-2px);
  box-shadow: 0 16px 34px rgba(255, 114, 95, 0.36);
}

.btn-secondary {
  background: var(--navy);
  color: #ffffff;
  box-shadow: 0 10px 24px rgba(23, 32, 51, 0.16);
}

.btn-secondary:hover {
  background: #24304a;
  transform: translateY(-2px);
  box-shadow: 0 16px 34px rgba(23, 32, 51, 0.24);
}

.privacy-note {
  margin: 18px 0 0;
  color: rgba(23, 32, 51, 0.56);
  font-size: 0.74rem;
  font-weight: 800;
  text-align: center;
}

/* RESPONSIVE */
@media (max-width: 900px) {
  :global(body) {
    overflow: auto;
  }

  .entry-page {
    position: relative;
    min-height: 100vh;
    overflow-y: auto;
  }

  .entry-bg__img {
    object-position: 68% center;
  }

  .entry-main {
    height: auto;
    min-height: calc(100vh - 68px);
    align-items: flex-start;
    justify-content: center;
    padding-top: 16px;
  }

  .entry-card {
    width: 100%;
  }

  .entry-bg__overlay {
    background:
      linear-gradient(
        180deg,
        rgba(255, 248, 239, 0.94) 0%,
        rgba(255, 248, 239, 0.82) 54%,
        rgba(255, 248, 239, 0.72) 100%
      ),
      radial-gradient(
        circle at 50% 18%,
        rgba(255, 114, 95, 0.18),
        transparent 24rem
      ),
      radial-gradient(
        circle at 18% 82%,
        rgba(122, 155, 118, 0.2),
        transparent 22rem
      );
  }
}

@media (max-width: 680px) {
  .site-header {
    padding: 0 18px;
  }

  .header-btn {
    display: none;
  }

  .entry-main {
    padding: 10px 16px 24px;
  }

  .entry-card {
    padding: 24px 20px;
    border-radius: 26px;
  }

  .entry-intro h1 {
    font-size: clamp(2.35rem, 11vw, 3.8rem);
  }

  .entry-options {
    grid-template-columns: 1fr;
  }
}
</style>