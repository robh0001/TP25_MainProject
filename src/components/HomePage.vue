<template>
  <div class="page">

    <!-- HEADER -->
    <header class="header">
      <div class="wrap header-inner">
        <RouterLink to="/" class="logo">HealthyKids</RouterLink>
        <nav class="nav">
          <a href="#about">About</a>
          <a href="#focus">Focus</a>
          <a href="#how">How it works</a>
          <a href="#kids">Kids</a>
        </nav>
        <div class="header-cta">
          <RouterLink to="/parent-entry" class="btn-outline">Parent plan</RouterLink>
          <RouterLink to="/young-person-dashboard" class="btn-fill">Kids dashboard</RouterLink>
        </div>
      </div>
    </header>

    <main>

      <!-- HERO -->
      <section class="hero">
        <div class="wrap hero-inner">
          <div class="hero-copy">
            <p class="label">Personalised family health</p>
            <h1>Health guidance<br>for families,<br>made simple.</h1>
            <p class="body-text">
              HealthyKids helps parents of children aged 5-12 build healthier routines around
              nutrition, movement, sleep, and everyday habits - one small step at a time.
            </p>
            <div class="hero-actions">
              <RouterLink to="/parent-entry" class="btn-fill">Start your plan</RouterLink>
              <RouterLink to="/parent-dashboard" class="btn-ghost">Open dashboard</RouterLink>
            </div>
            <ul class="trust-row">
              <li>3-min onboarding</li>
              <li>Built for busy parents</li>
              <li>Weekly actionable goals</li>
            </ul>
          </div>
          <div class="hero-media">
            <img
              src="https://images.unsplash.com/photo-1609220136736-443140cffec6?auto=format&fit=crop&w=1400&q=80"
              alt="Parent and child doing a healthy home routine together"
              class="hero-img"
            />
            <div class="hero-float-card">
              <span class="float-label">Today's focus</span>
              <strong>Build a calmer evening routine</strong>
              <div class="mini-bars">
                <div class="mini-bar-row">
                  <span>Sleep support</span>
                  <div class="bar"><i style="width:82%"></i></div>
                </div>
                <div class="mini-bar-row">
                  <span>Screen balance</span>
                  <div class="bar"><i style="width:64%"></i></div>
                </div>
                <div class="mini-bar-row">
                  <span>Daily routine</span>
                  <div class="bar"><i style="width:74%"></i></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- PATHWAYS -->
      <section class="pathways">
        <div class="wrap paths-grid">
          <article class="path-card path-parent">
            <p class="label">For parents</p>
            <h3>Build and manage your family plan</h3>
            <p>Complete the quiz, set priorities, and track routines across nutrition, movement, sleep, and screen habits.</p>
            <RouterLink to="/parent-entry" class="btn-fill">Go to parent entry</RouterLink>
          </article>
          <article class="path-card path-kids">
            <p class="label">For kids</p>
            <h3>Playful healthy habit dashboard</h3>
            <p>Explore missions, earn progress, and learn healthy habits in a fun way designed just for children.</p>
            <RouterLink to="/young-person-dashboard" class="btn-kids">Go to kids dashboard</RouterLink>
          </article>
        </div>
      </section>

      <!-- ABOUT -->
      <section id="about" class="about">
        <div class="wrap about-grid">
          <div>
            <p class="label">About</p>
            <h2>Practical support for parents who want clear next steps.</h2>
          </div>
          <div class="about-copy">
            <p>HealthyKids is designed for busy families who want to support their child's wellbeing without being overwhelmed by conflicting advice or unrealistic expectations.</p>
            <p>The platform turns quiz responses into clear, tailored recommendations that help families build healthier routines gradually and confidently.</p>
          </div>
        </div>
      </section>

      <!-- FOCUS AREAS -->
      <section id="focus" class="focus">
        <div class="wrap focus-shell">
    <div class="section-head focus-head">
      <p class="label">Core focus areas</p>
      <h2>Support across the habits that matter most.</h2>
    </div>

    <div class="focus-grid">
      <article class="focus-card">
        <div class="focus-img-wrap">
          <img src="https://images.unsplash.com/photo-1498837167922-ddd27525d352?auto=format&fit=crop&w=900&q=80" alt="Healthy meal" />
        </div>
        <div class="focus-card-body">
          <h3>Nutrition</h3>
          <p>Encourage healthier meals and snack habits with practical changes that fit daily family routines.</p>
        </div>
      </article>

      <article class="focus-card">
        <div class="focus-img-wrap">
          <img src="https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?auto=format&fit=crop&w=900&q=80" alt="Movement activity" />
        </div>
        <div class="focus-card-body">
          <h3>Movement &amp; Sleep</h3>
          <p>Support more activity, calmer evenings, and better sleep through small, manageable habit changes.</p>
        </div>
      </article>

      <article class="focus-card">
        <div class="focus-img-wrap">
          <img src="https://images.unsplash.com/photo-1588072432836-e10032774350?auto=format&fit=crop&w=900&q=80" alt="Daily routine" />
        </div>
        <div class="focus-card-body">
          <h3>Daily Routine</h3>
          <p>Build more structure around devices, after-school habits, and consistent everyday patterns.</p>
        </div>
      </article>
    </div>
  </div>
</section>

      <!-- INSIGHTS -->
      <section id="insights" class="insights">
        <div class="wrap insights-inner">
          <div class="insights-left">
            <p class="label">Health insights</p>
            <h2>Simple visuals that make health data easier to understand.</h2>
            <p>HealthyKids turns population-level information into clear signals that help parents focus on what matters.</p>
            <div class="tab-row">
              <button
                v-for="tab in tabs"
                :key="tab.key"
                :class="['tab-btn', { active: activeInsight === tab.key }]"
                @click="activeInsight = tab.key"
              >{{ tab.label }}</button>
            </div>
          </div>

          <div class="insights-right">
            <div v-if="loadingInsights" class="insight-card state-card">
              <p class="label">Loading insights..</p>
            </div>
            <div v-else-if="insightsError" class="insight-card state-card">
              <p class="label">Insights unavailable</p>
              <p>{{ insightsError }}</p>
            </div>
            <template v-else-if="insights">

              <!-- BODY -->
              <div v-show="activeInsight === 'body'" class="tab-pane">
                <div class="insight-card">
                  <span class="insight-overline">Body balance</span>
                  <h3>Weight category distribution</h3>
                  <p class="insight-sub">A clear view of how weight categories are distributed across children aged 5-17.</p>
                  <div class="body-layout">
                    <div class="ring-wrap">
                      <div class="ring" :style="bodyRingStyle">
                        <div class="ring-inner">
                          <span class="ring-num">{{ insights.bodyBalance.headlinePct }}%</span>
                          <span class="ring-lbl">Healthy range</span>
                        </div>
                      </div>
                      <p class="ring-caption">{{ insights.bodyBalance.headlineText }}</p>
                    </div>
                    <div class="bars-wrap">
                      <div v-for="seg in insights.bodyBalance.segments" :key="seg.key" class="bar-row">
                        <span>{{ seg.label }}</span>
                        <div class="bar"><i :class="seg.key" :style="{ width: seg.value + '%' }"></i></div>
                        <strong>{{ seg.value }}%</strong>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="subcards">
                  <div class="subcard">
                    <span class="sub-label">Main signal</span>
                    <strong>Healthy range remains the largest group</strong>
                    <p>Most children remain in the healthy range, while overweight and obesity are important areas for early support.</p>
                  </div>
                  <div class="subcard">
                    <span class="sub-label">What helps</span>
                    <strong>Small routine shifts can have real impact</strong>
                    <p>Practical changes in meals, active play, and daily structure can support healthier outcomes over time.</p>
                  </div>
                </div>
              </div>

              <!-- SLEEP -->
              <div v-show="activeInsight === 'sleep'" class="tab-pane">
                <div class="insight-card">
                  <span class="insight-overline">Sleep</span>
                  <h3>Weeknight and weekend sleep patterns</h3>
                  <p class="insight-sub">{{ insights.sleep.headlineBand }} {{ insights.sleep.headlineText }}</p>
                  <div class="sleep-grid">
                    <div class="inner-card">
                      <div class="inner-head">
                        <span class="pill">Weeknight</span>
                        <strong>{{ insights.sleep.headlinePct }}%</strong>
                      </div>
                      <div v-for="item in insights.sleep.weeknight" :key="'wn-'+item.label" class="bar-row">
                        <span>{{ item.label }}</span>
                        <div class="bar"><i class="sleep-wn" :style="{ width: item.value + '%' }"></i></div>
                        <strong>{{ item.value }}%</strong>
                      </div>
                    </div>
                    <div class="inner-card">
                      <div class="inner-head">
                        <span class="pill muted">Weekend</span>
                        <strong>{{ insights.sleep.weekend[3]?.value || 0 }}%</strong>
                      </div>
                      <div v-for="item in insights.sleep.weekend" :key="'we-'+item.label" class="bar-row">
                        <span>{{ item.label }}</span>
                        <div class="bar"><i class="sleep-we" :style="{ width: item.value + '%' }"></i></div>
                        <strong>{{ item.value }}%</strong>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="subcards">
                  <div class="subcard">
                    <span class="sub-label">Weeknights</span>
                    <strong>8-9 hours is the strongest band</strong>
                    <p>The most common weeknight range, where routine improvements can make the biggest difference.</p>
                  </div>
                  <div class="subcard">
                    <span class="sub-label">Weekends</span>
                    <strong>Sleep patterns widen slightly</strong>
                    <p>Weekend nights show a broader spread, suggesting routines become less consistent outside school days.</p>
                  </div>
                </div>
              </div>

              <!-- ACTIVITY -->
              <div v-show="activeInsight === 'activity'" class="tab-pane">
                <div class="insight-card">
                  <span class="insight-overline">Activity</span>
                  <h3>Average daily inactivity</h3>
                  <p class="insight-sub">{{ insights.activity.headlineBand }} {{ insights.activity.headlineText }}</p>
                  <div class="inner-card">
                    <div class="inner-head">
                      <span class="pill warm">Daily inactivity</span>
                      <strong>{{ insights.activity.headlinePct }}%</strong>
                    </div>
                    <div v-for="item in insights.activity.bands" :key="item.label" class="bar-row">
                      <span>{{ item.label }}</span>
                      <div class="bar"><i class="activity" :style="{ width: item.value + '%' }"></i></div>
                      <strong>{{ item.value }}%</strong>
                    </div>
                  </div>
                </div>
                <div class="subcards">
                  <div class="subcard">
                    <span class="sub-label">Key takeaway</span>
                    <strong>Inactivity clusters in the mid-to-high bands</strong>
                    <p>Sedentary periods are common rather than isolated - widespread across age groups.</p>
                  </div>
                  <div class="subcard">
                    <span class="sub-label">What helps</span>
                    <strong>Short movement breaks can add up</strong>
                    <p>Small bursts of movement before school, after school, and between screen activities improve daily balance.</p>
                  </div>
                </div>
              </div>

            </template>
          </div>
        </div>
      </section>

      <!-- HOW IT WORKS -->
      <section id="how" class="how">
        <div class="wrap">
          <div class="section-head">
            <p class="label">How it works</p>
            <h2>A simple three-step experience.</h2>
          </div>
          <div class="steps-grid">
            <article class="step-card">
              <span class="step-num">01</span>
              <h3>Complete the quiz</h3>
              <p>Parents answer short questions about routines, concerns, and daily habits.</p>
            </article>
            <article class="step-card">
              <span class="step-num">02</span>
              <h3>Receive recommendations</h3>
              <p>We identify priority areas and generate tailored guidance for your family.</p>
            </article>
            <article class="step-card">
              <span class="step-num">03</span>
              <h3>Follow the plan</h3>
              <p>Use the dashboard to take clear, realistic next steps and track progress over time.</p>
            </article>
          </div>
        </div>
      </section>

      <!-- TESTIMONIALS -->
      <section class="stories">
        <div class="wrap">
          <div class="section-head">
            <p class="label">What parents say</p>
            <h2>More clarity, less overwhelm.</h2>
          </div>
          <div class="stories-grid">
            <blockquote class="story-card">
              <p>"HealthyKids gave us a clearer way to manage after-school time. The actions felt small enough to follow - that made a huge difference."</p>
              <cite>Parent of a 7-year-old</cite>
            </blockquote>
            <blockquote class="story-card">
              <p>"The dashboard helped me understand exactly what to do each day instead of general advice. Everything felt realistic."</p>
              <cite>Parent of a 9-year-old</cite>
            </blockquote>
            <blockquote class="story-card">
              <p>"It focused on progress, not perfection. Improving our routines felt achievable for the whole family."</p>
              <cite>Parent of an 11-year-old</cite>
            </blockquote>
          </div>
        </div>
      </section>

      <!-- KIDS ZONE -->
      <section id="kids" class="kids-zone">
        <div class="wrap">
          <div class="kids-shell">
            <div class="kids-copy">
              <p class="kids-label">Kids Zone</p>
              <h2>Adventure missions for healthy heroes.</h2>
              <p>Kids have a dedicated dashboard with friendly activities, simple habit goals, and playful missions that connect back to the parent plan.</p>
            </div>
            <div class="kids-actions">
              <RouterLink to="/young-person-dashboard" class="btn-white">Open Kids Dashboard</RouterLink>
              <RouterLink to="/parent-entry" class="btn-ghost-white">Preview parent sync</RouterLink>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section class="cta">
        <div class="wrap cta-inner">
          <div>
            <p class="label">Get started</p>
            <h2>Start building healthier family routines today.</h2>
          </div>
          <RouterLink to="/parent-entry" class="btn-fill-light">Begin now</RouterLink>
        </div>
      </section>

    </main>

    <footer class="footer">
      <div class="wrap footer-inner">
        <span class="logo">HealthyKids</span>
        <p>A Monash University SDG 3 project · Team TP25 · 2025</p>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { computed, onMounted, ref } from 'vue'

const activeInsight = ref('body')
const insights = ref(null)
const loadingInsights = ref(false)
const insightsError = ref('')

const tabs = [
  { key: 'body', label: 'Body balance' },
  { key: 'sleep', label: 'Sleep' },
  { key: 'activity', label: 'Activity' },
]

const API_BASE_URL = import.meta.env.VITE_PARENT_DATA_INSIGHTS_API_BASE_URL || ''
const API_URL = API_BASE_URL ? `${API_BASE_URL}/test/data-insights` : '/test/data-insights'

async function fetchHomepageInsights() {
  loadingInsights.value = true
  insightsError.value = ''
  try {
    const res = await fetch(API_URL)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    insights.value = await res.json()
  } catch (err) {
    insightsError.value = err.message || 'Unable to load insights right now.'
  } finally {
    loadingInsights.value = false
  }
}

onMounted(fetchHomepageInsights)

const bodyRingStyle = computed(() => {
  const segs = insights.value?.bodyBalance?.segments
  if (!segs?.length) return { background: 'conic-gradient(#e8e4de 0% 100%)' }
  const uw = segs.find(s => s.key === 'underweight')?.value || 0
  const nm = segs.find(s => s.key === 'normal')?.value || 0
  const ow = segs.find(s => s.key === 'overweight')?.value || 0
  const ob = segs.find(s => s.key === 'obese')?.value || 0
  const a = uw, b = uw + nm, c = uw + nm + ow, d = uw + nm + ow + ob
  return {
    background: `conic-gradient(
      #a8c5da ${0}% ${a}%,
      #6aaa8a ${a}% ${b}%,
      #e8a84c ${b}% ${c}%,
      #c97158 ${c}% ${d}%,
      #e8e4de ${d}% 100%
    )`
  }
})
</script>

<style scoped>
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

.page,
.entry-page,
.quiz-page,
.dashboard-page {
  min-height: 100vh;
  position: relative;
  overflow-x: clip;
  background:
    radial-gradient(circle at 14% 18%, rgba(214, 194, 174, 0.18), transparent 34%),
    radial-gradient(circle at 84% 14%, rgba(235, 223, 210, 0.16), transparent 34%),
    radial-gradient(circle at 86% 78%, rgba(224, 198, 170, 0.12), transparent 36%),
    linear-gradient(145deg, #f7f3ee 0%, #f9f5f0 46%, #fcf9f5 100%);
}

.page::before,
.entry-page::before,
.quiz-page::before,
.dashboard-page::before,
.page::after,
.entry-page::after,
.quiz-page::after,
.dashboard-page::after {
  content: "";
  position: fixed;
  z-index: 0;
  pointer-events: none;
  border-radius: 999px;
  filter: blur(56px);
  opacity: 0.26;
}

.page::before,
.entry-page::before,
.quiz-page::before,
.dashboard-page::before {
  width: 420px;
  height: 420px;
  top: -120px;
  left: -150px;
  background: radial-gradient(circle, rgba(213, 191, 169, 0.34), rgba(213, 191, 169, 0));
}

.page::after,
.entry-page::after,
.quiz-page::after,
.dashboard-page::after {
  width: 460px;
  height: 460px;
  top: 40vh;
  right: -180px;
  background: radial-gradient(circle, rgba(234, 217, 199, 0.30), rgba(234, 217, 199, 0));
}

.wrap {
  width: min(1100px, calc(100% - 48px));
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

h1,
h2,
h3 {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  font-weight: 400;
  color: var(--c-text);
  letter-spacing: -0.03em;
  line-height: 1.05;
}

h1 {
  font-size: clamp(2.8rem, 5.5vw, 5rem);
}

h2 {
  font-size: clamp(1.8rem, 3.5vw, 3rem);
}

h3 {
  font-size: 1.25rem;
  line-height: 1.3;
}

.label {
  display: block;
  margin-bottom: 14px;
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--c-muted);
}

p,
.body-text {
  font-family: var(--font-sans);
  font-size: 1rem;
  line-height: 1.75;
  color: var(--c-muted);
}

.btn-fill,
.btn-outline,
.btn-ghost,
.btn-kids,
.btn-white,
.btn-ghost-white,
.btn-fill-light {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 50px;
  padding: 0 24px;
  border-radius: 8px;
  border: 1.5px solid transparent;
  text-decoration: none;
  font-family: var(--font-sans);
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 0.01em;
  cursor: pointer;
  transition: opacity 0.15s, transform 0.15s, background 0.15s, border-color 0.15s;
}

.btn-fill,
.btn-fill-light {
  background: var(--c-accent-dark);
  color: #fff;
  border-color: var(--c-accent-dark);
}

.btn-outline,
.btn-ghost {
  background: rgba(255, 252, 248, 0.82);
  color: var(--c-text);
}

.btn-outline {
  border-color: rgba(120, 102, 84, 0.18);
}

.btn-ghost {
  border-color: rgba(120, 102, 84, 0.14);
}

.btn-kids {
  background: var(--c-kids);
  color: #fff;
  border-color: var(--c-kids);
}

.btn-white {
  background: #fff;
  color: var(--c-text);
  border-color: rgba(255, 255, 255, 0.6);
}

.btn-ghost-white {
  background: transparent;
  color: #fff;
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-fill:hover,
.btn-kids:hover,
.btn-white:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-outline:hover,
.btn-ghost:hover {
  background: rgba(244, 237, 229, 0.82);
}

.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(250, 247, 243, 0.94);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--c-border);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  min-height: 70px;
}

.logo {
  font-family: Georgia, serif;
  font-size: 1.2rem;
  font-weight: 400;
  color: var(--c-text);
  text-decoration: none;
  letter-spacing: -0.02em;
}

.nav {
  display: flex;
  gap: 32px;
}

.nav a {
  font-family: var(--font-sans);
  font-size: 0.88rem;
  font-weight: 500;
  color: var(--c-muted);
  text-decoration: none;
  transition: color 0.15s;
}

.nav a:hover {
  color: var(--c-text);
}

.header-cta {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-cta .btn-outline,
.header-cta .btn-fill {
  min-height: 42px;
  padding: 0 18px;
  font-size: 0.85rem;
}

.hero {
  padding: 80px 0 90px;
}

.hero-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 56px;
  align-items: center;
}

.hero-copy {
  display: flex;
  flex-direction: column;
}

.hero-copy h1 {
  margin-bottom: 24px;
}

.hero-copy .body-text {
  max-width: 32rem;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 32px;
}

.trust-row {
  display: flex;
  flex-wrap: wrap;
  margin-top: 24px;
  list-style: none;
  padding: 0;
}

.trust-row li {
  margin-right: 20px;
  padding-right: 20px;
  border-right: 1px solid var(--c-border);
  font-family: var(--font-sans);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--c-muted);
}

.trust-row li:last-child {
  margin-right: 0;
  padding-right: 0;
  border-right: none;
}

.hero-media {
  position: relative;
  min-height: 520px;
}

.hero-img {
  display: block;
  width: 100%;
  height: 520px;
  object-fit: cover;
  border-radius: var(--r-card);
}

.hero-float-card {
  position: absolute;
  right: 20px;
  bottom: 24px;
  left: 20px;
  padding: 22px 24px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 16px;
  background: var(--c-surface-strong);
  backdrop-filter: blur(14px);
  box-shadow: 0 16px 40px rgba(80, 64, 48, 0.1);
}

.float-label {
  display: block;
  margin-bottom: 6px;
  font-family: var(--font-sans);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--c-muted);
}

.hero-float-card strong {
  display: block;
  margin-bottom: 16px;
  font-family: Georgia, serif;
  font-size: 1.15rem;
  font-weight: 400;
  color: var(--c-text);
}

.mini-bars {
  display: grid;
  gap: 10px;
}

.mini-bar-row {
  display: grid;
  grid-template-columns: 110px 1fr;
  align-items: center;
  gap: 10px;
}

.mini-bar-row span {
  font-family: var(--font-sans);
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--c-muted);
}

.bar {
  height: 6px;
  border-radius: 999px;
  background: #e8ddd2;
  overflow: hidden;
}

.bar i {
  display: block;
  height: 100%;
  border-radius: 999px;
  background: var(--c-accent-dark);
}

.pathways,
.about,
.focus,
.insights,
.how,
.stories,
.kids-zone,
.cta {
  padding: 80px 0;
  border-top: 1px solid var(--c-border);
}

.pathways {
  padding-top: 0;
  border-top: none;
}

.paths-grid,
.about-grid,
.insights-inner,
.steps-grid,
.stories-grid {
  display: grid;
  gap: 20px;
}

.paths-grid,
.about-grid {
  grid-template-columns: 1fr 1fr;
}

.focus-grid,
.steps-grid,
.stories-grid {
  grid-template-columns: repeat(3, 1fr);
}

.insights-inner {
  grid-template-columns: 0.9fr 1.1fr;
  gap: 56px;
  align-items: start;
}

.path-card,
.focus-card,
.insight-card,
.subcard,
.step-card,
.story-card {
  border: 1px solid var(--c-border);
  border-radius: var(--r-card);
  background: var(--c-surface);
}

.path-card,
.step-card,
.story-card,
.insight-card,
.subcard {
  padding: 32px;
}

.path-card {
  display: flex;
  flex-direction: column;
}

.path-card h3 {
  margin-bottom: 12px;
  font-size: 1.3rem;
}

.path-card p {
  margin-bottom: 24px;
  flex: 1;
}

.path-kids {
  background: #f5efe7;
  border-color: rgba(116, 97, 79, 0.16);
}

.path-kids .label {
  color: var(--c-kids);
}

.about-grid {
  gap: 56px;
  align-items: start;
}

.about-grid h2 {
  max-width: 10ch;
}

.about-copy p {
  margin-bottom: 16px;
}

.about-copy p:last-child {
  margin-bottom: 0;
}

.section-head {
  margin-bottom: 40px;
}

.section-head h2 {
  max-width: 14ch;
}

.insights {
  background: #f3eee8;
}

.insights-left h2 {
  max-width: 9ch;
  margin-bottom: 18px;
}

.insights-left p {
  max-width: 30rem;
  font-size: 0.95rem;
}

.tab-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 28px;
}

.tab-btn {
  min-height: 44px;
  padding: 0 20px;
  border: 1.5px solid rgba(120, 102, 84, 0.18);
  border-radius: 8px;
  background: rgba(255, 252, 248, 0.82);
  font-family: var(--font-sans);
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--c-muted);
  cursor: pointer;
  transition: all 0.15s;
}

.tab-btn:hover {
  background: rgba(244, 237, 229, 0.82);
  color: var(--c-text);
}

.tab-btn.active {
  background: var(--c-accent-dark);
  color: #fff;
  border-color: var(--c-accent-dark);
}

.tab-pane {
  display: grid;
  gap: 18px;
}

.state-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 220px;
}

.insight-overline,
.sub-label,
.step-num,
.kids-label {
  display: block;
  font-family: var(--font-sans);
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.insight-overline {
  margin-bottom: 8px;
  font-size: 0.72rem;
  color: var(--c-muted);
}

.insight-card h3 {
  margin-bottom: 8px;
  font-size: 1.3rem;
}

.insight-sub {
  margin-bottom: 24px;
  font-size: 0.93rem;
}

.subcards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.sub-label {
  margin-bottom: 8px;
  font-size: 0.7rem;
  color: var(--c-muted);
}

.subcard strong {
  display: block;
  margin-bottom: 8px;
  font-family: Georgia, serif;
  font-size: 1rem;
  font-weight: 400;
  color: var(--c-text);
  line-height: 1.35;
}

.subcard p {
  font-size: 0.88rem;
}

.body-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 28px;
  align-items: center;
}

.ring-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.ring {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 200px;
  height: 200px;
  border-radius: 50%;
}

.ring-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 124px;
  height: 124px;
  border-radius: 50%;
  background: var(--c-surface-strong);
  text-align: center;
  box-shadow: inset 0 0 0 1px rgba(120, 102, 84, 0.08);
}

.ring-num {
  font-family: Georgia, serif;
  font-size: 2rem;
  font-weight: 400;
  color: var(--c-text);
}

.ring-lbl {
  margin-top: 4px;
  font-family: var(--font-sans);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--c-muted);
}

.ring-caption {
  max-width: 200px;
  margin-top: 14px;
  font-family: var(--font-sans);
  font-size: 0.85rem;
  line-height: 1.6;
  color: var(--c-muted);
  text-align: center;
}

.bars-wrap {
  display: grid;
  gap: 12px;
}

.bar-row {
  display: grid;
  grid-template-columns: 130px 1fr 52px;
  align-items: center;
  gap: 12px;
}

.bar-row span,
.bar-row strong {
  font-family: var(--font-sans);
  font-size: 0.88rem;
}

.bar-row span {
  color: var(--c-muted);
}

.bar-row strong {
  text-align: right;
  font-weight: 700;
  color: var(--c-text);
}

.bar-row .bar {
  height: 10px;
}

.bar i.underweight {
  background: #c7b299;
}

.bar i.normal {
  background: #8d9b7d;
}

.bar i.overweight {
  background: #c69a63;
}

.bar i.obese {
  background: #a96f58;
}

.bar i.sleep-wn {
  background: var(--c-accent-dark);
}

.bar i.sleep-we {
  background: #9c8774;
}

.bar i.activity {
  background: #b68052;
}

.sleep-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.inner-card {
  padding: 20px;
  border: 1px solid rgba(120, 102, 84, 0.08);
  border-radius: 14px;
  background: var(--c-surface-strong);
}

.inner-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.inner-head strong {
  font-family: var(--font-sans);
  font-size: 1rem;
  font-weight: 700;
  color: var(--c-text);
}

.pill {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0 14px;
  border-radius: 6px;
  background: var(--c-accent-dark);
  color: #fff;
  font-family: var(--font-sans);
  font-size: 0.78rem;
  font-weight: 700;
}

.pill.muted {
  background: #9c8774;
}

.pill.warm {
  background: #b68052;
}

.step-card h3 {
  margin-bottom: 10px;
}

.step-num {
  margin-bottom: 20px;
  font-size: 0.7rem;
  color: var(--c-muted);
}

.story-card p {
  margin-bottom: 16px;
  font-family: Georgia, serif;
  font-size: 1.05rem;
  line-height: 1.7;
  color: var(--c-text);
  font-style: italic;
}

.story-card cite {
  font-family: var(--font-sans);
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--c-muted);
  font-style: normal;
}

.kids-shell {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 48px;
  align-items: center;
  padding: 52px;
  border-radius: var(--r-card);
  background: var(--c-kids);
  color: #fff;
}

.kids-label {
  margin-bottom: 14px;
  font-size: 0.72rem;
  color: rgba(255, 255, 255, 0.68);
}

.kids-shell h2 {
  margin-bottom: 14px;
  color: #fff;
}

.kids-shell p {
  max-width: 34rem;
  color: rgba(255, 255, 255, 0.82);
}

.kids-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-width: 200px;
}

.cta-inner {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
}

.cta-inner h2 {
  max-width: 14ch;
}

.footer {
  padding: 28px 0;
  border-top: 1px solid var(--c-border);
}

.footer-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.footer p {
  font-size: 0.82rem;
  color: var(--c-muted);
}

.focus {
  padding: 80px 0;
}

.focus-shell {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 28px;
  align-items: start;
}

.focus-head {
  margin: 0;
}

.focus-head h2 {
  margin: 0;
  max-width: none;
  font-size: clamp(2.3rem, 4.2vw, 4rem);
  line-height: 0.96;
}

.focus-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.focus-card {
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
  border-radius: var(--r-card);
  border: 1px solid var(--c-border);
  background: var(--c-surface);
  box-shadow: 0 10px 24px rgba(80, 64, 48, 0.06);
}

.focus-img-wrap {
  width: 100%;
  height: 220px;
  overflow: hidden;
  background: #ede3d7;
}

.focus-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.focus-card-body {
  display: flex;
  flex-direction: column;
  padding: 22px;
}

.focus-card h3 {
  margin: 0 0 10px;
  font-size: 1.1rem;
  line-height: 1.2;
  color: var(--c-text);
}

.focus-card p {
  margin: 0;
  font-size: 0.94rem;
  line-height: 1.65;
  color: var(--c-muted);
}

@media (max-width: 1100px) {
  .focus-shell {
    grid-template-columns: 1fr;
  }

  .focus-head h2 {
    max-width: 10ch;
  }

  .focus-grid,
  .hero-inner,
  .paths-grid,
  .about-grid,
  .insights-inner,
  .kids-shell,
  .steps-grid,
  .stories-grid,
  .subcards,
  .sleep-grid,
  .body-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 900px) {
  .focus-grid {
    grid-template-columns: 1fr;
  }

  .focus-head h2 {
    max-width: none;
  }
}

@media (max-width: 640px) {
  .nav,
  .header-cta .btn-outline {
    display: none;
  }

  .wrap {
    width: calc(100% - 32px);
  }

  .hero {
    padding: 48px 0 64px;
  }

  .kids-shell {
    padding: 32px;
  }

  .kids-actions {
    flex-direction: row;
  }

  .hero-float-card {
    right: 12px;
    bottom: 16px;
    left: 12px;
  }

  .trust-row {
    flex-direction: column;
    gap: 8px;
  }

  .trust-row li {
    margin-right: 0;
    padding-right: 0;
    border-right: none;
  }

  .focus {
    padding: 64px 0;
  }

  .focus-img-wrap {
    height: 200px;
  }

  .focus-card-body {
    padding: 20px;
  }
}
</style>