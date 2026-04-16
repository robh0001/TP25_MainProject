<template>
    <div class="entry-page">
      <header class="site-header">
        <div class="container header-row">
          <RouterLink to="/" class="brand">HealthyKids</RouterLink>
  
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
        const response = await fetch(
        `${import.meta.env.VITE_PARENT_PROFILES_API_BASE_URL}/parent-profiles/${encodeURIComponent(username)}`
        )
        const data = await response.json()
  
        if (response.status === 404) {
        returningUserError.value =
            'We could not find that profile. Check your username or start a new family plan.'
        return
        }
  
        if (!response.ok) {
            throw new Error(data.error || 'Load failed')
        }

        savePlan(data)
        router.push('/parent-dashboard')
    } catch (error) {
        returningUserError.value = 'Unable to load your profile right now. Please try again.'
        console.error(error)
    }
  }
  </script>
  
  <style scoped>
  :global(*) {
    box-sizing: border-box;
  }
  
  :global(:root) {
    --c-text: #2f281f;
    --c-muted: #6d6256;
    --c-border: rgba(120, 102, 84, 0.14);
    --c-surface: rgba(255, 251, 246, 0.84);
    --c-surface-strong: rgba(255, 252, 248, 0.94);
    --c-accent: #8a6f58;
    --c-accent-dark: #5f4a3a;
    --c-accent-soft: #efe5da;
    --c-kids: #74614f;
    --r-card: 20px;
    --font-sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }
  
  :global(body) {
    margin: 0;
    font-family: var(--font-sans);
    background: #f7f3ee;
    color: #171717;
    -webkit-font-smoothing: antialiased;
  }
  
  .entry-page {
    min-height: 100vh;
    position: relative;
    overflow-x: clip;
    background:
      radial-gradient(circle at 14% 18%, rgba(214, 194, 174, 0.18), transparent 34%),
      radial-gradient(circle at 84% 14%, rgba(235, 223, 210, 0.16), transparent 34%),
      radial-gradient(circle at 86% 78%, rgba(224, 198, 170, 0.12), transparent 36%),
      linear-gradient(145deg, #f7f3ee 0%, #f9f5f0 46%, #fcf9f5 100%);
  }
  
  .entry-page::before,
  .entry-page::after {
    content: "";
    position: fixed;
    z-index: 0;
    pointer-events: none;
    border-radius: 999px;
    filter: blur(56px);
    opacity: 0.26;
  }
  
  .entry-page::before {
    width: 420px;
    height: 420px;
    top: -120px;
    left: -150px;
    background: radial-gradient(circle, rgba(213, 191, 169, 0.34), rgba(213, 191, 169, 0));
  }
  
  .entry-page::after {
    width: 460px;
    height: 460px;
    top: 40vh;
    right: -180px;
    background: radial-gradient(circle, rgba(234, 217, 199, 0.30), rgba(234, 217, 199, 0));
  }
  
  .container {
    width: min(1100px, calc(100% - 48px));
    margin: 0 auto;
    position: relative;
    z-index: 1;
  }
  
  .site-header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(250, 247, 243, 0.94);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--c-border);
  }
  
  .header-row {
    min-height: 70px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
  }
  
  .brand {
    text-decoration: none;
    color: var(--c-text);
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.2rem;
    font-weight: 400;
    letter-spacing: -0.02em;
  }
  
  .nav {
    display: flex;
    align-items: center;
    gap: 32px;
  }
  
  .nav a,
  .nav-link {
    text-decoration: none;
    color: var(--c-muted);
    font-family: var(--font-sans);
    font-size: 0.88rem;
    font-weight: 500;
    transition: color 0.15s;
  }
  
  .nav a:hover,
  .nav-link:hover {
    color: var(--c-text);
  }
  
  .header-btn {
    min-height: 42px;
    padding: 0 18px;
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    font-family: var(--font-sans);
    font-size: 0.85rem;
    font-weight: 600;
    border: 1.5px solid rgba(120, 102, 84, 0.18);
    background: rgba(255, 252, 248, 0.82);
    color: var(--c-text);
    transition: background 0.15s, transform 0.15s;
  }
  
  .header-btn:hover {
    background: rgba(244, 237, 229, 0.82);
  }
  
  .entry-intro {
    padding: 80px 0 42px;
  }
  
  .intro-shell {
    display: grid;
    grid-template-columns: 1fr 420px;
    gap: 56px;
    align-items: end;
  }
  
  .step-kicker,
  .section-eyebrow,
  .card-kicker,
  .status-label {
    margin: 0 0 12px;
    font-family: var(--font-sans);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--c-muted);
  }
  
  .intro-copy h1,
  .path-top h2,
  .flow-copy h2,
  .flow-card h3 {
    margin: 0;
    font-family: Georgia, "Times New Roman", serif;
    font-weight: 400;
    line-height: 1.02;
    letter-spacing: -0.03em;
    color: var(--c-text);
  }
  
  .intro-copy h1 {
    font-size: clamp(2.7rem, 5vw, 4.6rem);
    max-width: 12ch;
  }
  
  .path-top h2,
  .flow-copy h2 {
    font-size: clamp(1.8rem, 3vw, 2.4rem);
  }
  
  .flow-card h3 {
    font-size: 1.3rem;
  }
  
  .intro-text,
  .path-top p,
  .flow-card p,
  .visual-panel ul,
  .form-block label,
  .status-step small {
    font-family: var(--font-sans);
    font-size: 1rem;
    line-height: 1.72;
    color: var(--c-muted);
  }
  
  .intro-text {
    margin: 18px 0 0;
    max-width: 40rem;
  }
  
  .intro-status-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--r-card);
    padding: 24px;
    box-shadow: 0 14px 30px rgba(80, 64, 48, 0.08);
    backdrop-filter: blur(8px);
  }
  
  .status-label {
    margin-bottom: 16px;
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
    background: var(--c-accent-soft);
    color: var(--c-text);
    font-family: var(--font-sans);
    font-weight: 700;
    font-size: 0.88rem;
  }
  
  .status-step.active span {
    background: var(--c-accent-dark);
    color: #fff;
    box-shadow: 0 10px 24px rgba(95, 74, 58, 0.22);
  }
  
  .status-step small {
    font-size: 0.78rem;
    font-weight: 600;
  }
  
  .status-line {
    flex: 1;
    height: 1px;
    background: var(--c-border);
  }
  
  .entry-options-section {
    padding: 24px 0 80px;
  }
  
  .entry-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  
  .path-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--r-card);
    padding: 32px;
    display: grid;
    gap: 22px;
    box-shadow: 0 16px 34px rgba(80, 64, 48, 0.08);
    backdrop-filter: blur(8px);
  }
  
  .new-parent-card,
  .returning-parent-card {
    background: var(--c-surface);
  }
  
  .path-top p {
    margin: 14px 0 0;
  }
  
  .path-visual {
    background: linear-gradient(180deg, rgba(255, 252, 248, 0.9), rgba(245, 237, 228, 0.96));
    border: 1px solid rgba(120, 102, 84, 0.08);
    border-radius: 14px;
    padding: 20px;
    display: grid;
    gap: 14px;
  }
  
  .visual-badge {
    width: fit-content;
    padding: 8px 12px;
    border-radius: 6px;
    background: var(--c-accent-dark);
    color: #fff;
    font-family: var(--font-sans);
    font-size: 0.76rem;
    font-weight: 700;
  }
  
  .visual-badge.muted {
    background: #9c8774;
  }
  
  .visual-panel strong {
    display: block;
    margin-bottom: 10px;
    font-family: var(--font-sans);
    font-size: 1rem;
    color: var(--c-text);
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
    font-weight: 600;
    color: var(--c-text);
  }
  
  .form-block input {
    width: 100%;
    min-height: 54px;
    border-radius: 10px;
    border: 1px solid rgba(120, 102, 84, 0.14);
    background: rgba(255, 252, 248, 0.95);
    padding: 0 16px;
    font-family: var(--font-sans);
    font-size: 0.96rem;
    color: var(--c-text);
    outline: none;
    transition: border-color 0.15s, box-shadow 0.15s;
  }
  
  .form-block input:focus {
    border-color: var(--c-accent);
    box-shadow: 0 0 0 4px rgba(138, 111, 88, 0.12);
  }
  
  .form-error {
    margin: 0;
    font-family: var(--font-sans);
    color: #b42318;
    font-size: 0.92rem;
    font-weight: 600;
  }
  
  .soft-brown-btn,
  .outline-btn {
    min-height: 50px;
    padding: 0 24px;
    border-radius: 8px;
    font-family: var(--font-sans);
    font-size: 0.9rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: background 0.15s, transform 0.15s, opacity 0.15s;
  }
  
  .soft-brown-btn {
    background: var(--c-accent-dark);
    color: #fff;
    border: 1.5px solid var(--c-accent-dark);
    box-shadow: 0 12px 24px rgba(95, 74, 58, 0.18);
    cursor: pointer;
  }
  
  .soft-brown-btn:hover {
    opacity: 0.92;
    transform: translateY(-1px);
  }
  
  .outline-btn {
    background: rgba(255, 252, 248, 0.82);
    color: var(--c-text);
    border: 1.5px solid rgba(120, 102, 84, 0.18);
    cursor: pointer;
  }
  
  .outline-btn:hover {
    background: rgba(244, 237, 229, 0.82);
  }
  
  .full-btn {
    width: 100%;
  }
  
  .flow-section {
    padding: 0 0 90px;
    border-top: 1px solid var(--c-border);
  }
  
  .flow-shell {
    padding: 48px 0 0;
  }
  
  .flow-copy p {
    margin: 0 0 12px;
  }
  
  .flow-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 24px;
  }
  
  .flow-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--r-card);
    padding: 28px;
    box-shadow: 0 10px 22px rgba(80, 64, 48, 0.06);
  }
  
  .flow-card span {
    display: inline-block;
    margin-bottom: 18px;
    font-family: var(--font-sans);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    color: var(--c-muted);
  }
  
  .flow-card p {
    margin: 12px 0 0;
  }
  
  @media (max-width: 980px) {
    .intro-shell,
    .entry-grid,
    .flow-grid {
      grid-template-columns: 1fr;
    }
  
    .intro-copy h1,
    .path-top h2 {
      max-width: none;
    }
  }
  
  @media (max-width: 640px) {
    .nav {
      display: none;
    }
  
    .container {
      width: calc(100% - 32px);
    }
  
    .header-row {
      flex-wrap: wrap;
      padding: 12px 0;
    }
  
    .header-btn {
      width: 100%;
    }
  
    .entry-intro {
      padding: 52px 0 32px;
    }
  
    .path-card,
    .intro-status-card,
    .flow-card {
      padding: 22px;
    }
  
    .status-steps {
      gap: 8px;
    }
  
    .status-step {
      min-width: 68px;
    }
  }
  </style>