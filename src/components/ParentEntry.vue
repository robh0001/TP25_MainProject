<template>
    <div class="entry-page">
      <header class="site-header">
        <div class="container header-row">
          <RouterLink to="/" class="brand">HealthySteps</RouterLink>
  
          <nav class="nav" aria-label="Primary">
            <RouterLink to="/" class="nav-link">Home</RouterLink>
            <a href="#entry-options" class="nav-link">Parent access</a>
            <a href="#flow" class="nav-link">How it works</a>
          </nav>
  
          <RouterLink to="/" class="header-btn light-btn">Back home</RouterLink>
        </div>
      </header>
  
      <main>
        <section class="entry-intro">
          <div class="container intro-shell">
            <div class="intro-copy">
              <p class="step-kicker">Step 1 of 3</p>
              <h1>How would you like to continue?</h1>
              <p class="intro-text">
                Start a new family plan or return to an existing one. This page is the parent access
                point before the quiz and dashboard.
              </p>
            </div>
  
            <div class="intro-status-card">
              <p class="status-label">Journey</p>
              <div class="status-steps">
                <div class="status-step active">
                  <span>1</span>
                  <small>Parent access</small>
                </div>
                <div class="status-line"></div>
                <div class="status-step">
                  <span>2</span>
                  <small>Quiz</small>
                </div>
                <div class="status-line"></div>
                <div class="status-step">
                  <span>3</span>
                  <small>Dashboard</small>
                </div>
              </div>
            </div>
          </div>
        </section>
  
        <section id="entry-options" class="entry-options-section">
          <div class="container">
            <div class="entry-grid">
              <article class="path-card new-parent-card">
                <div class="path-top">
                  <p class="card-kicker">New parent</p>
                  <h2>Create a new family plan</h2>
                  <p>
                    Choose a username, complete the parent quiz, and generate a personalised family
                    dashboard with practical next steps.
                  </p>
                </div>
  
                <div class="path-visual">
                  <div class="visual-badge">New profile</div>
                  <div class="visual-panel">
                    <strong>What happens next?</strong>
                    <ul>
                      <li>Create username</li>
                      <li>Complete parent quiz</li>
                      <li>Unlock dashboard</li>
                    </ul>
                  </div>
                </div>
  
                <div class="form-block">
                  <label for="new-username">Choose a username</label>
                  <input
                    id="new-username"
                    v-model.trim="newUsername"
                    type="text"
                    placeholder="e.g. healthyparent01"
                  />
                  <p v-if="newUserError" class="form-error">{{ newUserError }}</p>
                  <button type="button" class="soft-brown-btn full-btn" @click="startNewUser">
                    Start as new parent
                  </button>
                </div>
              </article>
  
              <article class="path-card returning-parent-card">
                <div class="path-top">
                  <p class="card-kicker">Returning parent</p>
                  <h2>Open your saved dashboard</h2>
                  <p>
                    Enter your saved username to continue with your child's daily tasks, weekly plan,
                    progress tracker, and recommendations.
                  </p>
                </div>
  
                <div class="path-visual">
                  <div class="visual-badge muted">Saved access</div>
                  <div class="visual-panel">
                    <strong>Continue where you left off</strong>
                    <ul>
                      <li>Load saved profile</li>
                      <li>View current plan</li>
                      <li>Track daily progress</li>
                    </ul>
                  </div>
                </div>
  
                <div class="form-block">
                  <label for="returning-username">Enter your username</label>
                  <input
                    id="returning-username"
                    v-model.trim="returningUsername"
                    type="text"
                    placeholder="Enter your username"
                  />
                  <p v-if="returningUserError" class="form-error">{{ returningUserError }}</p>
                  <button type="button" class="outline-btn full-btn" @click="continueReturningUser">
                    Open my dashboard
                  </button>
                </div>
              </article>
            </div>
          </div>
        </section>
  
        <section id="flow" class="flow-section">
          <div class="container flow-shell">
            <div class="flow-copy">
              <p class="section-eyebrow">What happens next</p>
              <h2>A simple flow for busy parents</h2>
            </div>
  
            <div class="flow-grid">
              <article class="flow-card">
                <span>01</span>
                <h3>Choose your path</h3>
                <p>Select whether you are starting fresh or returning with an existing profile.</p>
              </article>
  
              <article class="flow-card">
                <span>02</span>
                <h3>Complete the quiz</h3>
                <p>Answer a few questions about routines, habits, and daily challenges.</p>
              </article>
  
              <article class="flow-card">
                <span>03</span>
                <h3>Follow your dashboard</h3>
                <p>Get relevant daily actions, weekly guidance, and progress tracking.</p>
              </article>
            </div>
          </div>
        </section>
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter, RouterLink } from 'vue-router'
  import { useFamilyPlanStore } from '../stores/familyPlanStore'
  
  const router = useRouter()
  const { state, savePlan } = useFamilyPlanStore()
  
  const newUsername = ref('')
  const returningUsername = ref('')
  const newUserError = ref('')
  const returningUserError = ref('')
  
  function normalizeUsername(value) {
    return value.trim().toLowerCase().replace(/\s+/g, '')
  }
  
  async function startNewUser() {
    newUserError.value = ''

    if (!newUsername.value) {
        newUserError.value = 'Please choose a username before continuing.'
        return
    }

    const username = normalizeUsername(newUsername.value)

    try {
        const response = await fetch(
        `${import.meta.env.VITE_PARENT_PROFILE_CHECK_API_BASE_URL}/test/check-username?username=${encodeURIComponent(username)}`
        )

        if (!response.ok) {
        throw new Error('Username check failed')
        }

        const data = await response.json()

        if (!data.available) {
        newUserError.value = 'That username is already taken. Please choose another one.'
        return
        }

        savePlan({
        ...state,
        username,
        })

        router.push('/parent-quiz')
    } catch (error) {
        newUserError.value = 'Unable to check username right now. Please try again.'
    }
    }
  
  async function continueReturningUser() {
    returningUserError.value = ''
  
    if (!returningUsername.value) {
      returningUserError.value = 'Please enter your username.'
      return
    }
  
    const username = normalizeUsername(returningUsername.value)
  
    try {
      if (state.username === username && state.childName) {
        router.push('/parent-dashboard')
        return
      }
  
      throw new Error('Profile not found')
    } catch (error) {
      returningUserError.value =
        'We could not find that profile. Check your username or start a new family plan.'
    }
  }
  </script>
  
  <style scoped>
  :global(*) {
    box-sizing: border-box;
  }
  
  :global(body) {
  margin: 0;
  background: #ece7df;
  font-family: 'Montserrat', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  -webkit-font-smoothing: antialiased;
  color: #2f2a26;
}
  .entry-page {
    min-height: 100vh;
    background: #ece7df;
  }
  
  .container {
    width: min(1200px, calc(100% - 48px));
    margin: 0 auto;
  }
  
  .site-header {
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(236, 231, 223, 0.92);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(47, 42, 38, 0.12);
  }
  
  .header-row {
    min-height: 82px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
  }
  
  .brand {
    text-decoration: none;
    color: #2f2a26;
    font-size: 1.75rem;
    font-weight: 900;
    letter-spacing: -0.05em;
  }
  
  .nav {
    display: flex;
    align-items: center;
    gap: 28px;
  }
  
  .nav a,
  .nav-link {
    text-decoration: none;
    color: #3e3631;
    font-size: 0.96rem;
    font-weight: 500;
  }
  
  .nav a:hover,
  .nav-link:hover {
    opacity: 0.72;
  }
  
  .header-btn {
    text-decoration: none;
    min-height: 46px;
    padding: 0 18px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.94rem;
    font-weight: 700;
    border: 1px solid #3b312b;
  }
  
  .light-btn {
    color: #3b312b;
    background: transparent;
  }
  
  .entry-intro {
    padding: 46px 0 34px;
  }
  
  .intro-shell {
    display: grid;
    grid-template-columns: 1fr 420px;
    gap: 28px;
    align-items: end;
  }
  
  .step-kicker,
  .section-eyebrow,
  .card-kicker {
    margin: 0 0 12px;
    /* font-size: 0.78rem; */
    text-transform: uppercase;
    /* font-weight: 800; */
    color: #6c6258;
  }
  
  .intro-copy h1,
  .flow-copy h2,
  .support-note-box h2 {
    margin: 0;
    line-height: 0.95;
    font-weight: 800;
    color: #2f2a26;
  }
  
  .intro-text,
  .path-top p,
  .flow-card p,
  .visual-panel ul,
  .form-block label {
    font-size: 1rem;
    line-height: 1.75;
    color: #5e5248;
  }
  
  .intro-text {
    margin: 18px 0 0;
    max-width: 42rem;
  }
  
  .intro-status-card {
    background: #f3eee8;
    border: 1px solid rgba(47, 42, 38, 0.12);
    padding: 24px;
  }
  
  .status-label {
    margin: 0 0 16px;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6c6258;
  }
  
  .status-steps {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  
  .status-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    min-width: 82px;
  }
  
  .status-step span {
    width: 42px;
    height: 42px;
    border-radius: 999px;
    display: grid;
    place-items: center;
    background: #e5ddd3;
    color: #3b312b;
    font-weight: 800;
  }
  
  .status-step.active span {
    background: #b2805c;
    color: #fff;
  }
  
  .status-step small {
    font-size: 0.8rem;
    color: #5e5248;
    font-weight: 700;
  }
  
  .status-line {
    flex: 1;
    height: 1px;
    background: rgba(47, 42, 38, 0.18);
  }
  
  .entry-options-section {
    padding: 28px 0 80px;
  }
  
  .entry-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }
  
  .path-card {
    background: #f3eee8;
    border: 1px solid rgba(47, 42, 38, 0.12);
    padding: 28px;
    display: grid;
    gap: 24px;
  }
  
  .path-top h2,
  .flow-card h3 {
    margin: 0;
    font-size: 2rem;
    line-height: 1;
    letter-spacing: -0.05em;
    color: #2f2a26;
  }
  
  .path-top p {
    margin: 14px 0 0;
  }
  
  .path-visual {
    background: #fbf7f2;
    border: 1px solid rgba(47, 42, 38, 0.08);
    padding: 20px;
    display: grid;
    gap: 14px;
  }
  
  .visual-badge {
    width: fit-content;
    padding: 8px 12px;
    border-radius: 999px;
    background: #b2805c;
    color: #fff;
    font-size: 0.85rem;
    font-weight: 700;
  }
  
  .visual-badge.muted {
    background: #8a7668;
  }
  
  .visual-panel strong {
    display: block;
    margin-bottom: 10px;
    font-size: 1rem;
    color: #2f2a26;
  }
  
  .visual-panel ul {
    margin: 0;
    padding-left: 18px;
  }
  
  .form-block {
    display: grid;
    gap: 10px;
  }
  
  .form-block label {
    font-weight: 700;
    color: #3b312b;
  }
  
  .form-block input {
    width: 100%;
    min-height: 56px;
    border-radius: 18px;
    border: 1px solid rgba(47, 42, 38, 0.14);
    background: #fffdf9;
    padding: 0 18px;
    font: inherit;
    font-size: 1rem;
    color: #2f2a26;
    outline: none;
  }
  
  .form-block input:focus {
    border-color: #b2805c;
    box-shadow: 0 0 0 4px rgba(178, 128, 92, 0.14);
  }
  
  .form-error {
    margin: 0;
    color: #b42318;
    font-size: 0.95rem;
    font-weight: 600;
  }
  
  .soft-brown-btn,
  .final-cta-btn,
  .outline-btn {
    min-height: 52px;
    padding: 0 24px;
    border-radius: 999px;
    font-size: 0.98rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  
  .soft-brown-btn {
    background: #b2805c;
    color: #fff;
    border: none;
    cursor: pointer;
  }
  
  .outline-btn {
    background: transparent;
    color: #3b312b;
    border: 1px solid #3b312b;
    cursor: pointer;
  }
  
  .full-btn {
    width: 100%;
  }
  
  .flow-section {
    padding: 0 0 90px;
  }
  
  .flow-shell {
    background: #efe8de;
    border: 1px solid rgba(47, 42, 38, 0.1);
    padding: 34px;
  }
  
  .flow-copy p {
    margin: 0 0 12px;
  }
  
  .flow-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-top: 24px;
  }
  
  .flow-card {
    background: #fbf7f2;
    border: 1px solid rgba(47, 42, 38, 0.08);
    padding: 22px;
  }
  
  .flow-card span {
    display: inline-block;
    margin-bottom: 14px;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    color: #7a6d61;
  }
  
  .flow-card p {
    margin: 12px 0 0;
  }
  
  .support-note-section {
    padding: 0 0 80px;
  }
  
  .support-note-box {
    background: #3b312b;
    color: #fff;
    padding: 38px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
  }
  
  .support-note-box h2 {
    color: #fff;
    max-width: 12ch;
  }
  
  .light-eyebrow {
    color: rgba(255, 255, 255, 0.72);
  }
  
  .final-cta-btn {
    text-decoration: none;
    background: #fff;
    color: #2f2a26;
    min-width: 160px;
  }
  
  @media (max-width: 1100px) {
    .intro-shell,
    .entry-grid,
    .flow-grid,
    .support-note-box {
      grid-template-columns: 1fr;
    }
  
    .intro-shell,
    .support-note-box {
      display: grid;
    }
  }
  
  @media (max-width: 760px) {
    .nav {
      display: none;
    }
  
    .header-row {
      flex-wrap: wrap;
      padding: 14px 0;
    }
  
    .header-btn {
      width: 100%;
    }
  
    .container {
      width: calc(100% - 24px);
    }
  
    .path-card,
    .flow-shell,
    .support-note-box {
      padding: 24px;
    }
  
    .status-steps {
      gap: 8px;
    }
  
    .status-step {
      min-width: 68px;
    }
  }
  </style>