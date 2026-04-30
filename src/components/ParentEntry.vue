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
  :global(:root) {
    --c-black: #0a0b0a;
    --c-900: #111312;
    --c-800: #1c1f1d;
    --c-700: #2d3230;
    --c-500: #52605a;
    --c-400: #7a8880;
    --c-300: #a8b5ae;
    --c-100: #e8ece9;
    --c-50: #f4f5f2;
    --c-white: #ffffff;
  
    --c-green: #16a34a;
    --c-green-mid: #22c55e;
    --c-green-soft: #f0fdf4;
    --c-green-pale: #dcfce7;
  
    --border: rgba(10, 11, 10, 0.08);
    --border-mid: rgba(10, 11, 10, 0.14);
  
    --shadow-xs: 0 1px 4px rgba(0, 0, 0, 0.06);
    --shadow-md: 0 8px 28px rgba(0, 0, 0, 0.09);
    --shadow-lg: 0 20px 56px rgba(0, 0, 0, 0.12);
  
    --f-display: 'Fraunces', Georgia, serif;
    --f-body: 'General Sans', 'Helvetica Neue', ui-sans-serif, sans-serif;
    --f-mono: 'JetBrains Mono', monospace;
  
    --r-card: 28px;
  }
  
  :global(*, *::before, *::after) {
    box-sizing: border-box;
  }
  
  :global(body) {
    margin: 0;
    font-family: var(--f-body), system-ui;
    background: var(--c-white);
    color: var(--c-black);
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }
  
  .entry-page {
    min-height: 100vh;
    position: relative;
    overflow-x: clip;
    background:
      radial-gradient(circle at 82% 12%, rgba(34, 197, 94, 0.08), transparent 28rem),
      radial-gradient(circle at 8% 28%, rgba(59, 130, 246, 0.04), transparent 26rem),
      var(--c-white);
  }
  
  .entry-page::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    opacity: 0.025;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    background-size: 256px;
  }
  
  .container {
    width: min(1180px, calc(100% - 48px));
    margin: 0 auto;
    position: relative;
    z-index: 1;
  }
  
  /* HEADER */
  .site-header {
    position: sticky;
    top: 0;
    z-index: 500;
    background: rgba(255, 255, 255, 0.92);
    border-bottom: 1px solid var(--border);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow: var(--shadow-xs);
  }
  
  .header-row {
    min-height: 76px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
  }
  
  .brand {
    text-decoration: none;
    color: var(--c-black);
    font-family: var(--f-display);
    font-size: 1.25rem;
    font-weight: 400;
    letter-spacing: -0.03em;
  }
  
  .nav {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .nav a,
  .nav-link {
    height: 36px;
    padding: 0 12px;
    display: flex;
    align-items: center;
    font-family: var(--f-body);
    font-size: 0.86rem;
    font-weight: 500;
    color: var(--c-500);
    text-decoration: none;
    border-radius: 8px;
    transition: color 0.18s, background 0.18s;
  }
  
  .nav a:hover,
  .nav-link:hover {
    color: var(--c-black);
    background: var(--c-50);
  }
  
  .header-btn {
    height: 38px;
    padding: 0 16px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-family: var(--f-body);
    font-size: 0.86rem;
    font-weight: 600;
    color: var(--c-white);
    background: var(--c-black);
    text-decoration: none;
    border-radius: 10px;
    border: 1px solid var(--c-900);
    box-shadow:
      0 1px 3px rgba(0, 0, 0, 0.2),
      0 0 0 1px rgba(255, 255, 255, 0.06) inset;
    transition: all 0.2s;
  }
  
  .header-btn:hover {
    background: var(--c-800);
    transform: translateY(-1px);
  }
  
  /* HERO INTRO */
  .entry-intro {
    position: relative;
    padding: 92px 0 70px;
    overflow: hidden;
    border-bottom: 1px solid var(--border);
  }
  
  .entry-intro::before {
    content: "";
    position: absolute;
    width: 620px;
    height: 620px;
    top: -220px;
    right: -120px;
    border-radius: 50%;
    filter: blur(100px);
    background: radial-gradient(circle, rgba(22, 163, 74, 0.1), transparent 70%);
    pointer-events: none;
  }
  
  .entry-intro::after {
    content: "";
    position: absolute;
    width: 460px;
    height: 460px;
    bottom: -180px;
    left: -120px;
    border-radius: 50%;
    filter: blur(100px);
    background: radial-gradient(circle, rgba(59, 130, 246, 0.055), transparent 70%);
    pointer-events: none;
  }
  
  .intro-shell {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 420px;
    gap: 70px;
    align-items: center;
  }
  
  .step-kicker {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    height: 30px;
    padding: 0 12px;
    border-radius: 999px;
    background: var(--c-green-soft);
    border: 1px solid rgba(22, 163, 74, 0.2);
    font-size: 0.72rem;
    font-weight: 800;
    color: var(--c-green);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 0 0 28px;
  }
  
  .step-kicker::before {
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--c-green-mid);
    animation: livePulse 2.4s ease-in-out infinite;
  }
  
  @keyframes livePulse {
    0%,
    100% {
      box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.45);
    }
  
    50% {
      box-shadow: 0 0 0 4px rgba(34, 197, 94, 0);
    }
  }
  
  .intro-copy h1,
  .path-top h2,
  .flow-copy h2,
  .flow-card h3 {
    margin: 0;
    font-family: var(--f-display);
    font-weight: 400;
    line-height: 1.02;
    letter-spacing: -0.04em;
    color: var(--c-black);
  }
  
  .intro-copy h1 {
    max-width: 12ch;
    font-size: clamp(3rem, 6vw, 6.4rem);
    font-weight: 300;
    line-height: 0.96;
    letter-spacing: -0.055em;
  }
  
  .intro-text {
    max-width: 42rem;
    margin: 28px 0 0;
    font-family: var(--f-body);
    font-size: 1.02rem;
    line-height: 1.75;
    color: var(--c-500);
  }
  
  .intro-status-card {
    padding: 28px;
    border-radius: 26px;
    background:
      linear-gradient(145deg, rgba(255, 255, 255, 0.94), rgba(244, 245, 242, 0.92));
    border: 1px solid var(--border);
    box-shadow: var(--shadow-lg);
  }
  
  .status-label,
  .section-eyebrow,
  .card-kicker {
    margin: 0;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--c-400);
  }
  
  .status-label {
    margin-bottom: 22px;
  }
  
  .status-steps {
    display: grid;
    gap: 12px;
  }
  
  .status-step {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    min-width: 0;
  }
  
  .status-step span {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: grid;
    place-items: center;
    flex-shrink: 0;
    background: var(--c-50);
    border: 1px solid var(--border);
    font-family: var(--f-mono);
    font-size: 0.74rem;
    font-weight: 800;
    color: var(--c-400);
  }
  
  .status-step.active span {
    background: var(--c-black);
    color: var(--c-white);
    border-color: var(--c-black);
    box-shadow: none;
  }
  
  .status-step small {
    display: block;
    padding-top: 11px;
    font-family: var(--f-body);
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--c-black);
  }
  
  .status-line {
    width: 1px;
    height: 24px;
    margin-left: 21px;
    background: var(--border-mid);
  }
  
  /* ENTRY OPTIONS */
  .entry-options-section {
    padding: 86px 0 90px;
    background: var(--c-white);
  }
  
  .entry-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 22px;
  }
  
  .path-card {
    display: grid;
    gap: 22px;
    padding: 32px;
    border-radius: 28px;
    background: var(--c-white);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-md);
    transition: transform 0.25s, box-shadow 0.25s, border-color 0.25s;
  }
  
  .path-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--border-mid);
  }
  
  .new-parent-card {
    background:
      radial-gradient(circle at top right, rgba(34, 197, 94, 0.08), transparent 18rem),
      var(--c-white);
  }
  
  .returning-parent-card {
    background: var(--c-white);
  }
  
  .path-top h2 {
    margin-top: 12px;
    font-size: clamp(1.55rem, 2.5vw, 2.15rem);
    line-height: 1.08;
    letter-spacing: -0.035em;
  }
  
  .path-top p {
    margin: 14px 0 0;
    font-family: var(--f-body);
    font-size: 0.95rem;
    line-height: 1.72;
    color: var(--c-500);
  }
  
  .path-visual {
    padding: 20px;
    border-radius: 18px;
    background: var(--c-green-soft);
    border: 1px solid rgba(22, 163, 74, 0.14);
    display: grid;
    gap: 14px;
  }
  
  .returning-parent-card .path-visual {
    background: var(--c-50);
    border-color: var(--border);
  }
  
  .visual-badge {
    width: fit-content;
    height: 26px;
    padding: 0 11px;
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    background: var(--c-black);
    color: var(--c-white);
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  
  .visual-badge.muted {
    background: var(--c-green-soft);
    color: var(--c-green);
    border: 1px solid rgba(22, 163, 74, 0.16);
  }
  
  .visual-panel strong {
    display: block;
    margin-bottom: 12px;
    font-size: 0.92rem;
    color: var(--c-black);
  }
  
  .visual-panel ul {
    margin: 0;
    padding-left: 18px;
    color: var(--c-500);
    font-size: 0.9rem;
    line-height: 1.75;
  }
  
  /* FORM */
  .form-block {
    display: grid;
    gap: 10px;
  }
  
  .form-block label {
    font-family: var(--f-body);
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--c-black);
  }
  
  .form-block input {
    width: 100%;
    height: 54px;
    padding: 0 16px;
    border-radius: 12px;
    border: 1px solid var(--border-mid);
    background: var(--c-white);
    color: var(--c-black);
    font-family: var(--f-body);
    font-size: 0.96rem;
    outline: none;
    transition: border-color 0.15s, box-shadow 0.15s;
  }
  
  .form-block input:focus {
    border-color: var(--c-green);
    box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.12);
  }
  
  .form-error {
    margin: 0;
    color: #b42318;
    font-size: 0.88rem;
    font-weight: 700;
    line-height: 1.5;
  }
  
  .soft-brown-btn,
  .outline-btn {
    width: 100%;
    height: 52px;
    margin-top: 4px;
    border-radius: 12px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    font-family: var(--f-body);
    font-size: 0.94rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.22s;
  }
  
  .soft-brown-btn {
    color: var(--c-white);
    background: var(--c-black);
    border: 1px solid var(--c-black);
    box-shadow: none;
  }
  
  .soft-brown-btn:hover {
    background: var(--c-800);
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
  }
  
  .outline-btn {
    color: var(--c-black);
    background: var(--c-white);
    border: 1px solid var(--border-mid);
  }
  
  .outline-btn:hover {
    background: var(--c-50);
    transform: translateY(-1px);
  }
  
  .full-btn {
    width: 100%;
  }
  
  /* FLOW */
  .flow-section {
    padding: 84px 0 96px;
    background: var(--c-50);
    border-top: 1px solid var(--border);
  }
  
  .flow-shell {
    display: grid;
    gap: 34px;
    padding: 0;
  }
  
  .flow-copy {
    max-width: 560px;
  }
  
  .flow-copy h2 {
    margin-top: 14px;
    font-size: clamp(2.2rem, 4vw, 4rem);
    line-height: 1.02;
  }
  
  .flow-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-top: 0;
  }
  
  .flow-card {
    padding: 28px;
    border-radius: 24px;
    background: var(--c-white);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-xs);
  }
  
  .flow-card span {
    display: inline-block;
    margin-bottom: 18px;
    font-family: var(--f-mono);
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    color: var(--c-300);
  }
  
  .flow-card h3 {
    font-size: 1.35rem;
    font-weight: 500;
    line-height: 1.2;
    letter-spacing: -0.025em;
  }
  
  .flow-card p {
    margin: 12px 0 0;
    font-family: var(--f-body);
    font-size: 0.92rem;
    line-height: 1.7;
    color: var(--c-500);
  }
  
  /* RESPONSIVE */
  @media (max-width: 980px) {
    .intro-shell,
    .entry-grid,
    .flow-grid {
      grid-template-columns: 1fr;
    }
  
    .intro-status-card {
      max-width: 560px;
    }
  
    .intro-copy h1 {
      max-width: 11ch;
    }
  }
  
  @media (max-width: 760px) {
    .container {
      width: calc(100% - 32px);
    }
  
    .header-row {
      min-height: auto;
      padding: 14px 0;
      gap: 14px;
      flex-wrap: wrap;
    }
  
    .nav {
      display: none;
    }
  
    .header-btn {
      width: 100%;
    }
  
    .entry-intro {
      padding: 64px 0 52px;
    }
  
    .intro-copy h1 {
      font-size: clamp(2.75rem, 12vw, 4rem);
    }
  
    .path-card,
    .intro-status-card,
    .flow-card {
      padding: 24px;
    }
  
    .entry-options-section,
    .flow-section {
      padding: 64px 0;
    }
  }
  
  @media (max-width: 520px) {
    .status-step small {
      font-size: 0.82rem;
    }
  }
  </style>