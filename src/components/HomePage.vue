<template>
  <div class="home-page">
    <header class="site-header">
      <div class="container header-row">
        <RouterLink to="/" class="brand">HealthySteps</RouterLink>

        <nav class="nav" aria-label="Primary">
          <a href="#about">About</a>
          <a href="#focus">Focus</a>
          <a href="#how">How it works</a>
        </nav>

        <RouterLink to="/parent-quiz" class="header-btn">Start quiz</RouterLink>
      </div>
    </header>

    <main>
      <section class="hero">
        <div class="container hero-grid">
          <div class="hero-copy">
            <p class="eyebrow">Personalised family health support</p>
            <h1>Health guidance for families, made simple.</h1>
            <p class="hero-text">
              HealthySteps helps parents of children aged 5–12 build healthier routines around
              nutrition, movement, sleep, screen time, and everyday habits.
            </p>
            <p class="hero-subtext">
              Complete a short quiz and receive tailored recommendations designed to fit real
              family life.
            </p>

            <div class="hero-actions">
              <RouterLink to="/parent-quiz" class="btn btn-dark">Start your plan</RouterLink>
              <RouterLink to="/parent-dashboard" class="btn btn-light">Open dashboard</RouterLink>
            </div>
          </div>

          <div class="hero-visual" aria-hidden="true">
            <div class="visual-backdrop"></div>
            <div class="visual-glow visual-glow-one"></div>
            <div class="visual-glow visual-glow-two"></div>

            <div class="hero-card">
              <div class="hero-card-inner">
                <p class="card-label">Today’s focus</p>
                <h2>Build a calmer evening routine</h2>
                <p>
                  Small, realistic steps to improve sleep, reduce friction, and support healthier
                  family habits.
                </p>

                <div class="progress-group">
                  <div class="progress-item">
                    <span>Sleep support</span>
                    <div class="progress-line"><i style="width: 82%"></i></div>
                  </div>
                  <div class="progress-item">
                    <span>Screen balance</span>
                    <div class="progress-line"><i style="width: 64%"></i></div>
                  </div>
                  <div class="progress-item">
                    <span>Daily routine</span>
                    <div class="progress-line"><i style="width: 74%"></i></div>
                  </div>
                </div>
              </div>
            </div>

            <div class="floating-tag floating-tag-top">Tailored support</div>
            <div class="floating-tag floating-tag-bottom">For busy families</div>
          </div>
        </div>
      </section>

      <section id="about" class="intro">
        <div class="container intro-grid">
          <div>
            <p class="section-label">About HealthySteps</p>
            <h2>Practical support for parents who want clear next steps.</h2>
          </div>

          <div>
            <p>
              HealthySteps is designed for busy parents who want to support their child’s health
              without feeling overwhelmed by conflicting advice or unrealistic expectations.
            </p>
            <p>
              The platform turns quiz responses into clear, tailored recommendations that help
              families build healthier routines gradually and confidently.
            </p>
          </div>
        </div>
      </section>

      <section id="focus" class="focus">
        <div class="container">
          <div class="section-head">
            <p class="section-label">Core focus areas</p>
            <h2>Support across the habits that matter most.</h2>
          </div>

          <div class="focus-grid">
            <article class="focus-card">
              <div class="focus-icon">🍎</div>
              <h3>Nutrition</h3>
              <p>
                Encourage healthier meals and snack habits with practical changes that fit daily
                family routines.
              </p>
            </article>

            <article class="focus-card">
              <div class="focus-icon">🌙</div>
              <h3>Movement and sleep</h3>
              <p>
                Support more activity, calmer evenings, and better sleep through small and
                manageable habit changes.
              </p>
            </article>

            <article class="focus-card">
              <div class="focus-icon">📱</div>
              <h3>Screen time and routine</h3>
              <p>
                Build more structure around devices, after-school habits, and consistent daily
                routines.
              </p>
            </article>
          </div>
        </div>
      </section>

      <section id="how" class="how">
        <div class="container">
          <div class="section-head">
            <p class="section-label">How it works</p>
            <h2>A simple three-step experience.</h2>
          </div>

          <div class="steps-grid">
            <article class="step-card">
              <span>01</span>
              <h3>Complete the quiz</h3>
              <p>Parents answer a few short questions about routines, concerns, and habits.</p>
            </article>

            <article class="step-card">
              <span>02</span>
              <h3>Receive recommendations</h3>
              <p>The system identifies key focus areas and generates tailored guidance.</p>
            </article>

            <article class="step-card">
              <span>03</span>
              <h3>Follow the plan</h3>
              <p>Parents use the dashboard to take clear and realistic next steps over time.</p>
            </article>
          </div>
        </div>
      </section>

      <section class="cta">
        <div class="container cta-box">
          <div>
            <p class="section-label light">Get started</p>
            <h2>Start building a healthier family routine today.</h2>
          </div>

          <RouterLink to="/parent-quiz" class="btn btn-white">Begin now</RouterLink>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
:global(*) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #f6f3ee;
  color: #171717;
  -webkit-font-smoothing: antialiased;
}

.home-page {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(220, 209, 193, 0.35), transparent 28%),
    #f6f3ee;
}

.container {
  width: min(1160px, calc(100% - 48px));
  margin: 0 auto;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(246, 243, 238, 0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(23, 23, 23, 0.08);
}

.header-row {
  min-height: 78px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.brand {
  text-decoration: none;
  color: #171717;
  font-size: 1.3rem;
  font-weight: 800;
  letter-spacing: -0.04em;
}

.nav {
  display: flex;
  align-items: center;
  gap: 28px;
}

.nav a {
  text-decoration: none;
  color: #363636;
  font-size: 0.96rem;
  font-weight: 500;
}

.nav a:hover {
  color: #000;
}

.header-btn {
  text-decoration: none;
  background: #171717;
  color: #fff;
  padding: 12px 18px;
  border-radius: 999px;
  font-size: 0.95rem;
  font-weight: 700;
}

.hero {
  padding: 72px 0 64px;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 34px;
  align-items: center;
}

.hero-copy {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-right: 20px;
}

.eyebrow,
.section-label {
  margin: 0 0 14px;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-weight: 800;
  color: #6c6258;
}

.section-label.light {
  color: rgba(255,255,255,0.72);
}

.hero-copy h1 {
  margin: 0;
  font-size: clamp(3rem, 6vw, 5.6rem);
  line-height: 0.95;
  letter-spacing: -0.07em;
  font-weight: 800;
  max-width: 8ch;
}

.hero-text,
.hero-subtext,
.intro p,
.focus-card p,
.step-card p {
  font-size: 1.02rem;
  line-height: 1.75;
  color: #5e564e;
}

.hero-text {
  margin: 24px 0 0;
  max-width: 35rem;
}

.hero-subtext {
  margin: 14px 0 0;
  max-width: 35rem;
}

.hero-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 28px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 54px;
  padding: 0 22px;
  border-radius: 999px;
  text-decoration: none;
  font-weight: 700;
  border: 1px solid #171717;
  transition: 0.18s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

.btn-dark {
  background: #171717;
  color: #fff;
}

.btn-light {
  background: transparent;
  color: #171717;
}

.btn-white {
  background: #fff;
  color: #171717;
  border-color: #fff;
}

.hero-visual {
  position: relative;
  min-height: 560px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.visual-backdrop {
  position: absolute;
  inset: 40px 24px 24px 24px;
  border-radius: 34px;
  background: linear-gradient(145deg, #d8cdbf 0%, #b8a895 100%);
  box-shadow: 0 24px 60px rgba(50, 39, 26, 0.12);
}

.visual-glow {
  position: absolute;
  border-radius: 999px;
  filter: blur(2px);
}

.visual-glow-one {
  width: 180px;
  height: 180px;
  top: 10px;
  right: 30px;
  background: rgba(255, 255, 255, 0.35);
}

.visual-glow-two {
  width: 130px;
  height: 130px;
  bottom: 40px;
  left: 12px;
  background: rgba(255, 214, 166, 0.35);
}

.hero-card {
  position: relative;
  z-index: 2;
  width: min(430px, 92%);
  border-radius: 28px;
  background: rgba(255,255,255,0.84);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.5);
  box-shadow: 0 20px 50px rgba(23, 23, 23, 0.12);
}

.hero-card-inner {
  padding: 28px;
}

.card-label {
  margin: 0 0 10px;
  font-size: 0.76rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-weight: 800;
  color: #6f645a;
}

.hero-card-inner h2 {
  margin: 0;
  font-size: 1.9rem;
  line-height: 1.05;
  letter-spacing: -0.05em;
}

.hero-card-inner p {
  margin: 14px 0 0;
  color: #5d544b;
  line-height: 1.7;
}

.progress-group {
  margin-top: 24px;
  display: grid;
  gap: 16px;
}

.progress-item span {
  display: inline-block;
  margin-bottom: 8px;
  font-size: 0.92rem;
  font-weight: 700;
  color: #41372f;
}

.progress-line {
  width: 100%;
  height: 10px;
  border-radius: 999px;
  background: #ece5dd;
  overflow: hidden;
}

.progress-line i {
  display: block;
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, #1d1d1d 0%, #6d7f99 100%);
}

.floating-tag {
  position: absolute;
  z-index: 3;
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(255,255,255,0.82);
  color: #3d352d;
  font-size: 0.9rem;
  font-weight: 700;
  box-shadow: 0 12px 24px rgba(23, 23, 23, 0.08);
}

.floating-tag-top {
  top: 70px;
  left: 30px;
}

.floating-tag-bottom {
  right: 20px;
  bottom: 40px;
}

.intro,
.focus,
.how {
  padding: 72px 0;
}

.intro-grid {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  gap: 28px;
  align-items: start;
}

.intro h2,
.section-head h2,
.cta-box h2 {
  margin: 0;
  font-size: clamp(2rem, 4vw, 3.4rem);
  line-height: 1.05;
  letter-spacing: -0.05em;
  max-width: 12ch;
}

.intro p {
  margin: 0 0 16px;
}

.section-head {
  margin-bottom: 28px;
}

.focus-grid,
.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.focus-card,
.step-card {
  background: #fbf9f6;
  border: 1px solid rgba(23, 23, 23, 0.08);
  border-radius: 22px;
  padding: 24px;
  box-shadow: 0 10px 24px rgba(23, 23, 23, 0.03);
}

.focus-icon {
  width: 54px;
  height: 54px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  margin-bottom: 18px;
  background: #efe9e1;
  font-size: 1.4rem;
}

.focus-card h3,
.step-card h3 {
  margin: 0 0 12px;
  font-size: 1.18rem;
  line-height: 1.25;
}

.step-card span {
  display: inline-block;
  margin-bottom: 16px;
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  color: #7a6d61;
}

.cta {
  padding: 0 0 72px;
}

.cta-box {
  background: linear-gradient(135deg, #171717 0%, #292929 100%);
  color: #fff;
  border-radius: 28px;
  padding: 34px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

@media (max-width: 980px) {
  .hero-grid,
  .intro-grid,
  .focus-grid,
  .steps-grid,
  .cta-box {
    grid-template-columns: 1fr;
  }

  .hero-copy {
    padding-right: 0;
  }

  .hero-copy h1 {
    max-width: none;
  }

  .hero-visual {
    min-height: 460px;
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

  .header-btn,
  .hero-actions .btn,
  .cta-box .btn {
    width: 100%;
  }

  .hero {
    padding-top: 42px;
  }

  .container {
    width: calc(100% - 24px);
  }

  .hero-copy h1 {
    font-size: clamp(2.6rem, 13vw, 4.2rem);
  }

  .floating-tag {
    display: none;
  }
}


</style>