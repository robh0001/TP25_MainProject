<template>
  <div class="page">
    <header class="topbar">
      <div class="brand">
        <div class="brand-icon">❤</div>
        <span>HealthySteps</span>
      </div>

      <nav class="nav-links">
        <a href="#how-it-works">How it works</a>
        <a href="#resources">Resources</a>
        <a href="#community">Community</a>
      </nav>

      <button class="btn btn-primary">Get Started</button>
    </header>

    <main>
      <section class="hero split-bg">
        <div class="container">
          <div class="hero-grid">
            <div class="hero-text">
              <p class="eyebrow">Small steps, real change.</p>
              <h1>
                Your family,<br />
                <span>your pace.</span>
              </h1>
              <p class="hero-subtext">
                Supporting Australian families with practical, judgment-free tools to build
                healthier habits together.
              </p>
            </div>

            <div class="hero-choices">
              <article class="choice-card parent-card">
                <div class="choice-icon coral">👨‍👩‍👧</div>
                <h3>I'm a parent</h3>
                <p>
                  Navigate family health with warmth and realism. Get practical tools that fit
                  real family life—no judgment, just support.
                </p>
                <ul>
                  <li>Family overview dashboard</li>
                  <li>Daily snapshot cards with personalised tips</li>
                  <li>Gentle alerts when you're overloading changes</li>
                </ul>
                <button class="btn btn-coral full">Start as a Parent</button>
              </article>

              <article class="choice-card teen-card">
                <div class="choice-icon blue">🚀</div>
                <h3>I'm a young person</h3>
                <p>
                  Your body, your pace. Level up your health with tools designed for you—private,
                  fun, and zero lectures.
                </p>
                <ul>
                  <li>Earn XP and badges for trying</li>
                  <li>Fully private food and energy tracking</li>
                  <li>Control what you share with parents</li>
                </ul>
                <button class="btn btn-blue full">Start Your Journey</button>
              </article>
            </div>
          </div>
        </div>
      </section>

      <section class="container stats-banner">
        <div class="stats-icon">❤</div>
        <div>
          <h3>You're not alone</h3>
          <p>
            <strong>1 in 4 Australian children</strong> carry excess weight. This isn't about
            blame—it's about supporting families with practical, evidence-based tools that work in
            real life.
          </p>
          <div class="stats-links">
            <a href="#">Raising Children Network</a>
            <a href="#">Heart Foundation</a>
          </div>
        </div>
      </section>

      <section id="resources" class="tools-section container section-gap">
        <div class="section-heading center">
          <h2>Start right now. No sign-up needed.</h2>
          <p>
            Every core tool works instantly. Create an account later to save progress and unlock
            your dashboard.
          </p>
        </div>

        <div class="tool-grid three">
          <article class="mini-tool" v-for="tool in tools" :key="tool.title">
            <div class="tool-icon" :class="tool.className">{{ tool.icon }}</div>
            <h4>{{ tool.title }}</h4>
            <p>{{ tool.description }}</p>
            <a href="#">{{ tool.linkText }}</a>
          </article>
        </div>
      </section>

      <section class="tip-section split-bg-alt section-gap">
        <div class="container">
          <div class="section-heading center narrow">
            <span class="badge yellow">Updated every Monday</span>
            <h2>This week's parent tip</h2>
            <p>Real advice from Australian families like yours</p>
          </div>

          <article class="tip-card">
            <div class="tip-header">
              <div class="avatar">S</div>
              <div>
                <h4>Sarah from Melbourne</h4>
                <p>Parent of two, ages 8 &amp; 11</p>
              </div>
            </div>

            <blockquote>
              “Instead of banning screens before dinner, we started a 10-minute dance party rule.
              The kids pick the songs, we all move around like idiots, and somehow they're less
              grumpy about eating veggies afterwards. It's chaotic but it works!”
            </blockquote>

            <div class="tip-footer">
              <span>❤ 247 families liked this</span>
              <span>💬 32</span>
              <button class="btn btn-coral">Share your tip</button>
            </div>
          </article>
        </div>
      </section>

      <section class="container section-gap">
        <div class="section-heading center narrow">
          <h2>Get your personalized starting point</h2>
          <p>60-second quiz. No sign-up. Instant action plan tailored to your family.</p>
        </div>

        <div class="quiz-grid">
          <article class="quiz-card parent-quiz">
            <h3>Parent Quiz</h3>
            <ul>
              <li>Your child's age &amp; stage</li>
              <li>Top three health concerns</li>
              <li>Biggest daily struggle</li>
              <li>What you've already tried</li>
            </ul>
            <button class="btn btn-coral full">Start Parent Quiz</button>
          </article>

          <article class="quiz-card teen-quiz">
            <h3>Teen Quiz</h3>
            <ul>
              <li>What you want to feel different about</li>
              <li>What's hardest to change</li>
              <li>How independent you want to be</li>
              <li>Your biggest win this week</li>
            </ul>
            <button class="btn btn-blue full">Start Teen Quiz</button>
          </article>
        </div>

        <div class="quiz-output">
          <p>Quiz output example:</p>
          <div class="output-pill">
            “Your biggest win this week could be here’s your first action card—replacing afternoon
            chips with fruit &amp; yogurt.”
          </div>
        </div>
      </section>

      <section class="container section-gap">
        <div class="section-heading center narrow">
          <h2>Two experiences, one goal</h2>
          <p>
            Different language, different tools—both designed to support healthy habits at your
            own pace.
          </p>
        </div>

        <div class="experience-grid">
          <article class="experience-card coral-panel">
            <div class="panel-header">
              <h3>❤ Parent Pulse</h3>
              <p>Warm, realistic, zero judgment. Small steps for real family life.</p>
            </div>
            <div class="snapshot-card">
              <strong>Daily Snapshot Card</strong>
              <p>
                “Your child’s energy might be low today based on last night’s sleep log—there are 2
                quick after-school snack swaps.”
              </p>
            </div>
            <div class="panel-placeholder"></div>
          </article>

          <article class="experience-card blue-panel">
            <div class="panel-header">
              <h3>⚡ Teen Track</h3>
              <p>Private, motivating, and built around progress—not perfection.</p>
            </div>
            <div class="teen-progress">
              <div class="xp-ring">+120 XP</div>
              <div>
                <strong>Current streak</strong>
                <p>3 days of breakfast before school</p>
              </div>
            </div>
            <div class="badge-row">
              <span class="tiny-badge">Tried a new fruit</span>
              <span class="tiny-badge">Hydration streak</span>
              <span class="tiny-badge">Walked after school</span>
            </div>
          </article>
        </div>
      </section>

      <section id="how-it-works" class="how-section split-bg section-gap">
        <div class="container">
          <div class="section-heading center narrow">
            <h2>How It Works</h2>
            <p>Three simple steps to transform your family’s wellness journey</p>
          </div>

          <div class="steps-grid">
            <article class="step-card" v-for="step in steps" :key="step.title">
              <h4>{{ step.title }}</h4>
              <p>{{ step.description }}</p>
            </article>
          </div>
        </div>
      </section>

      <section class="container section-gap">
        <div class="cta-banner">
          <h2>Ready to Start Your Family Journey?</h2>
          <p>
            Join thousands of families building healthier habits together with our conflict-free
            approach.
          </p>
          <div class="cta-actions">
            <button class="btn btn-light">Get Started Free</button>
            <button class="btn btn-outline-light">Watch Demo</button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
const tools = [
  {
    icon: '🍽️',
    title: 'Meal Builder',
    description: 'Mix and match healthy Aussie meals your family will actually eat.',
    linkText: 'Try now',
    className: 'lilac',
  },
  {
    icon: '🏃',
    title: 'Activity Finder',
    description: 'Discover fun ways to move that don’t feel like exercise.',
    linkText: 'Explore',
    className: 'mint',
  },
  {
    icon: '🌙',
    title: 'Sleep Tracker',
    description: 'See how sleep connects to energy and mood.',
    linkText: 'Start tracking',
    className: 'sky',
  },
]

const steps = [
  {
    title: 'Choose a Challenge',
    description: 'Select from pre-made challenges or create your own custom family goal.',
  },
  {
    title: 'Complete Together',
    description: 'Work as a family unit. Everyone participates, no one gets singled out.',
  },
  {
    title: 'Earn Rewards',
    description: 'Celebrate success with meaningful, non-food rewards your family chooses together.',
  },
]
</script>

<style scoped>
* {
  box-sizing: border-box;
}

:global(html) {
  scroll-behavior: smooth;
}

:global(body) {
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #f7f7f8;
  color: #172033;
}

:global(a) {
  color: inherit;
  text-decoration: none;
}

:global(button) {
  font: inherit;
}

.page {
  min-height: 100vh;
}

.container {
  width: min(1120px, calc(100% - 32px));
  margin: 0 auto;
}

.topbar {
  width: min(1120px, calc(100% - 32px));
  margin: 16px auto 0;
  padding: 14px 18px;
  border: 1px solid #d9dde5;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  position: sticky;
  top: 12px;
  z-index: 20;
  backdrop-filter: blur(10px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 800;
  color: #ff654f;
}

.brand-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  color: white;
  background: linear-gradient(135deg, #6ea8ff, #ff7f74);
  box-shadow: 0 6px 16px rgba(93, 133, 255, 0.24);
}

.nav-links {
  display: flex;
  gap: 28px;
  color: #4e5a70;
  font-size: 14px;
}

.nav-links a:hover {
  color: #1f2b43;
}

.btn {
  border: 0;
  border-radius: 12px;
  padding: 12px 18px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease, opacity 0.2s ease, box-shadow 0.2s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

.btn-primary,
.btn-blue {
  background: linear-gradient(135deg, #ff7b6f, #458bff);
  color: white;
  box-shadow: 0 12px 24px rgba(81, 116, 255, 0.18);
}

.btn-coral {
  background: #f4513f;
  color: white;
  box-shadow: 0 12px 24px rgba(244, 81, 63, 0.22);
}

.btn-light {
  background: white;
  color: #4a48ec;
}

.btn-outline-light {
  background: transparent;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.8);
}

.full {
  width: 100%;
}

.section-gap {
  padding: 56px 0;
}

.split-bg {
  background: linear-gradient(90deg, #f7f1eb 0 50%, #edf2fb 50% 100%);
}

.split-bg-alt {
  background: linear-gradient(90deg, #f8f1f2 0 50%, #ecf3fd 50% 100%);
}

.hero {
  padding: 40px 0 56px;
  margin-top: 16px;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
  align-items: start;
}

.hero-text {
  text-align: center;
  padding-top: 12px;
}

.eyebrow {
  font-size: 18px;
  font-weight: 800;
  margin: 0 0 10px;
  color: #1e2433;
}

.hero h1 {
  margin: 0;
  font-size: clamp(2.7rem, 6vw, 4.8rem);
  line-height: 1.05;
  letter-spacing: -0.04em;
  color: #172033;
}

.hero h1 span {
  color: #f4513f;
}

.hero-subtext {
  max-width: 740px;
  margin: 18px auto 0;
  font-size: 18px;
  color: #4f5c72;
  line-height: 1.7;
}

.hero-choices {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 28px;
  margin-top: 10px;
}

.choice-card,
.mini-tool,
.quiz-card,
.step-card,
.experience-card,
.tip-card {
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid #e5e8ef;
  border-radius: 24px;
  box-shadow: 0 16px 40px rgba(20, 30, 60, 0.08);
}

.choice-card {
  padding: 28px;
}

.choice-card h3,
.quiz-card h3,
.experience-card h3,
.mini-tool h4,
.step-card h4 {
  margin: 16px 0 12px;
  font-size: 1.7rem;
  letter-spacing: -0.02em;
}

.choice-card p,
.mini-tool p,
.quiz-card li,
.step-card p,
.experience-card p {
  color: #556176;
  line-height: 1.7;
}

.choice-card ul,
.quiz-card ul {
  padding-left: 18px;
  margin: 16px 0 24px;
}

.choice-card li,
.quiz-card li {
  margin-bottom: 10px;
}

.choice-icon,
.tool-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  font-size: 1.55rem;
}

.coral {
  background: #ffe1dc;
}

.blue {
  background: #dcebff;
}

.lilac {
  background: #efe5ff;
}

.mint {
  background: #dbf7e7;
}

.sky {
  background: #deecff;
}

.parent-card {
  background: linear-gradient(180deg, #fff9f7, #ffffff);
}

.teen-card {
  background: linear-gradient(180deg, #f6faff, #ffffff);
}

.stats-banner {
  margin-top: 28px;
  background: #f4ebdf;
  border: 1px solid #e8dccb;
  border-radius: 24px;
  padding: 28px;
  display: flex;
  gap: 20px;
  align-items: flex-start;
  box-shadow: 0 12px 30px rgba(48, 46, 32, 0.05);
}

.stats-icon {
  width: 58px;
  height: 58px;
  border-radius: 18px;
  display: grid;
  place-items: center;
  background: #ffcb64;
  font-size: 1.4rem;
  flex-shrink: 0;
}

.stats-banner h3 {
  margin: 0 0 8px;
  font-size: 1.8rem;
}

.stats-banner p {
  margin: 0;
  color: #5a5a5a;
  line-height: 1.7;
}

.stats-links {
  display: flex;
  gap: 18px;
  flex-wrap: wrap;
  margin-top: 14px;
  color: #d05f2f;
  font-weight: 600;
}

.section-heading h2 {
  font-size: clamp(2rem, 4vw, 3rem);
  margin: 10px 0 10px;
  letter-spacing: -0.03em;
}

.section-heading p {
  color: #5b667a;
  max-width: 760px;
  margin: 0 auto;
  line-height: 1.7;
}

.center {
  text-align: center;
}

.narrow {
  max-width: 760px;
  margin: 0 auto 28px;
}

.badge {
  display: inline-block;
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
}

.yellow {
  background: #ffd98f;
  color: #815108;
}

.tool-grid.three,
.steps-grid,
.experience-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.mini-tool,
.step-card {
  padding: 24px;
}

.mini-tool a {
  color: #6a4cf0;
  font-weight: 700;
}

.tip-card {
  padding: 28px;
  max-width: 820px;
  margin: 0 auto;
}

.tip-header {
  display: flex;
  gap: 14px;
  align-items: center;
}

.tip-header h4 {
  margin: 0;
  font-size: 1.1rem;
}

.tip-header p {
  margin: 4px 0 0;
  color: #6a7487;
}

.avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-weight: 800;
  background: linear-gradient(135deg, #ffd8cc, #d7e7ff);
}

blockquote {
  margin: 20px 0;
  padding: 22px;
  background: #fff4ed;
  border-radius: 18px;
  color: #514840;
  line-height: 1.8;
}

.tip-footer {
  display: flex;
  gap: 18px;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  color: #6a7487;
}

.quiz-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 28px;
}

.quiz-card {
  padding: 28px;
}

.parent-quiz {
  background: linear-gradient(180deg, #fff7f3, #ffffff);
}

.teen-quiz {
  background: linear-gradient(180deg, #f4f8ff, #ffffff);
}

.quiz-output {
  text-align: center;
  margin-top: 26px;
}

.quiz-output p {
  color: #6a7487;
  margin-bottom: 10px;
}

.output-pill {
  max-width: 620px;
  margin: 0 auto;
  padding: 18px 22px;
  border-radius: 16px;
  background: linear-gradient(90deg, #ffeaea, #e6f0ff);
  color: #22304a;
  font-weight: 600;
}

.experience-card {
  padding: 0;
  overflow: hidden;
}

.panel-header {
  padding: 28px 28px 18px;
  color: white;
}

.coral-panel .panel-header {
  background: linear-gradient(135deg, #ff6f5d, #ff8664);
}

.blue-panel .panel-header {
  background: linear-gradient(135deg, #4d7df5, #8e53f7);
}

.panel-header h3 {
  margin: 0 0 8px;
}

.panel-header p {
  color: rgba(255, 255, 255, 0.88);
  margin: 0;
}

.snapshot-card,
.teen-progress,
.badge-row,
.panel-placeholder {
  margin: 22px 24px 24px;
}

.snapshot-card {
  background: #fff4f1;
  padding: 18px;
  border-radius: 18px;
}

.snapshot-card p {
  margin-bottom: 0;
}

.panel-placeholder {
  height: 18px;
  border-radius: 999px;
  background: #f4e3dd;
}

.teen-progress {
  display: flex;
  align-items: center;
  gap: 20px;
}

.xp-ring {
  width: 92px;
  height: 92px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  color: #4d7df5;
  font-weight: 800;
  background: white;
  box-shadow: inset 0 0 0 10px #ddebff;
}

.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tiny-badge {
  padding: 10px 12px;
  border-radius: 999px;
  background: #eff4ff;
  color: #3a5db8;
  font-size: 14px;
  font-weight: 700;
}

.cta-banner {
  border-radius: 28px;
  padding: 42px 28px;
  color: white;
  text-align: center;
  background: linear-gradient(135deg, #5a5bf4, #ff4ca0);
  box-shadow: 0 18px 40px rgba(94, 73, 236, 0.24);
}

.cta-banner h2 {
  margin: 0 0 12px;
  font-size: clamp(2rem, 4vw, 2.8rem);
}

.cta-banner p {
  margin: 0 auto;
  max-width: 680px;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.9);
}

.cta-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 22px;
  flex-wrap: wrap;
}

@media (max-width: 960px) {
  .nav-links {
    display: none;
  }

  .hero-choices,
  .quiz-grid,
  .tool-grid.three,
  .steps-grid,
  .experience-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .topbar {
    padding: 12px 14px;
  }

  .btn-primary {
    padding: 10px 14px;
  }

  .hero {
    padding-top: 24px;
  }

  .choice-card,
  .mini-tool,
  .quiz-card,
  .step-card,
  .tip-card {
    padding: 22px;
  }

  .stats-banner {
    flex-direction: column;
  }

  .tip-footer {
    align-items: flex-start;
  }
}
</style>