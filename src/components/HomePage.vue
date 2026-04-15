<template>
  <div class="home-page">
    <header class="site-header">
      <div class="container header-row">
        <RouterLink to="/" class="brand">HealthyKids</RouterLink>

        <nav class="nav" aria-label="Primary">
          <a href="#about">About</a>
          <a href="#services">Services</a>
          <a href="#testimonials">Stories</a>
          <a href="#faq">FAQs</a>
        </nav>

        <div class="header-actions">
          <RouterLink to="/parent-entry" class="header-btn light-btn">Parent entry</RouterLink>
          <RouterLink to="/parent-entry" class="header-btn dark-btn">Start plan</RouterLink>
        </div>
      </div>
    </header>

    <main>
      <section class="hero-section">
        <div class="container hero-shell">
          <div class="hero-background">
            <img
              src="https://images.unsplash.com/photo-1516627145497-ae6968895b74?auto=format&fit=crop&w=1600&q=80"
              alt="Parent and child spending calm family time together"
            />
          </div>

          <div class="hero-panel">
            <p class="hero-kicker">HealthySteps</p>
            <h1>Family Health Balance</h1>

            <div class="hero-divider"></div>

            <div class="hero-meta">
              <p>
                Transforming family wellbeing through practical support for nutrition, movement,
                sleep, and routine.
              </p>

              <RouterLink to="/parent-entry" class="hero-cta">Start Your Plan</RouterLink>
            </div>

            <div class="hero-bottom-image">
              <img
                src="https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=1200&q=80"
                alt="Family wellbeing support"
              />
            </div>
          </div>
        </div>
      </section>

      <section id="about" class="about-section">
        <div class="container about-wrap">
          <p class="section-eyebrow">About</p>
          <h2>Our mission</h2>
          <p class="about-copy">
            HealthySteps helps parents of children aged 5-12 build healthier routines in ways that
            feel manageable in real family life. Through tailored guidance, small daily actions, and
            a practical dashboard, the platform supports healthier habits across food, movement,
            sleep, screen time, and everyday structure.
          </p>

          <RouterLink to="/parent-entry" class="soft-brown-btn">Discover More</RouterLink>
        </div>
      </section>

      <section id="services" class="services-section">
        <div class="container">
          <div class="section-heading center">
            <p class="section-eyebrow">Our services</p>
            <h2>Support designed for everyday family life</h2>
          </div>

          <div class="services-grid">
            <article class="service-card">
              <div class="service-image">
                <img
                  src="https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=1200&q=80"
                  alt="Healthy food and nutrition support"
                />
              </div>
              <div class="service-body">
                <h3>Nutrition support</h3>
                <p>
                  Help your child build healthier eating and snack habits with practical changes
                  that fit busy schedules.
                </p>
              </div>
            </article>

            <article class="service-card">
              <div class="service-image">
                <img
                  src="https://images.unsplash.com/photo-1485965120184-e220f721d03e?auto=format&fit=crop&w=1200&q=80"
                  alt="Movement and activity support"
                />
              </div>
              <div class="service-body">
                <h3>Movement and activity</h3>
                <p>
                  Encourage short, realistic movement habits that help reduce sedentary behaviour
                  and support healthier routines.
                </p>
              </div>
            </article>

            <article class="service-card">
              <div class="service-image">
                <img
                  src="https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?auto=format&fit=crop&w=1200&q=80"
                  alt="Sleep and bedtime routine support"
                />
              </div>
              <div class="service-body">
                <h3>Sleep and routines</h3>
                <p>
                  Create calmer evenings, better sleep consistency, and more structure across the
                  day.
                </p>
              </div>
            </article>
          </div>
        </div>
      </section>

      <section class="insights-section" id="insights">
        <div class="container insights-grid">
          <div class="insights-copy">
            <p class="section-eyebrow">Why it matters</p>
              <h2>Simple patterns can reveal where families need the most support.</h2>
            <p>
              HealthySteps turns complex health data into clear signals that help parents focus on
              nutrition, sleep, movement, and everyday routine with more confidence.
            </p>

            <div class="insight-toggle">
              <button
                type="button"
                class="insight-tab"
                :class="{ active: activeInsight === 'body' }"
                @click="activeInsight = 'body'"
              >
                Body balance
              </button>

              <button
                type="button"
                class="insight-tab"
                :class="{ active: activeInsight === 'sleep' }"
                @click="activeInsight = 'sleep'"
              >
                Sleep
              </button>

              <button
                type="button"
                class="insight-tab"
                :class="{ active: activeInsight === 'activity' }"
                @click="activeInsight = 'activity'"
              >
                Activity
              </button>
            </div>
          </div>

          <div class="insight-panel">
            <article v-if="loadingInsights" class="hero-insight-card">
              <span class="insight-overline">Loading</span>
              <p class="visual-subtitle">Fetching the latest homepage insights...</p>
            </article>

            <article v-else-if="insightsError" class="hero-insight-card">
              <span class="insight-overline">Insights unavailable</span>
              <p class="visual-subtitle">{{ insightsError }}</p>
            </article>

            <div v-else-if="insights" class="tab-view">
              <!-- BODY -->
              <div v-show="activeInsight === 'body'" class="tab-content">
                <article class="hero-insight-card body-visual-card">
                  <div class="visual-header">
                    <span class="insight-overline">Body balance</span>
                    <h3 class="visual-title">Weight category distribution</h3>
                    <p class="visual-subtitle">
                      A simple view of how weight categories are distributed across children aged 5-17.
                    </p>
                  </div>

                  <div class="body-visual-layout">
                    <div class="body-ring-panel">
                      <div class="body-ring" :style="bodyRingStyle">
                        <div class="body-ring-inner">
                          <div class="body-ring-number">{{ insights.bodyBalance.headlinePct }}%</div>
                          <div class="body-ring-label">Healthy range</div>
                        </div>
                      </div>

                      <p class="body-ring-caption">
                        {{ insights.bodyBalance.headlineText }}
                      </p>
                    </div>

                    <div class="body-breakdown-panel">
                      <div
                        v-for="segment in insights.bodyBalance.segments"
                        :key="segment.key"
                        class="metric-row"
                      >
                        <div class="metric-row-top">
                          <div class="metric-label-wrap">
                            <span class="metric-dot" :class="segment.key"></span>
                            <span class="metric-label">{{ segment.label }}</span>
                          </div>
                          <strong class="metric-value">{{ segment.value }}%</strong>
                        </div>

                        <div class="metric-track">
                          <div
                            class="metric-fill"
                            :class="segment.key"
                            :style="{ width: segment.value + '%' }"
                          ></div>
                        </div>
                      </div>

                      <div class="summary-chip-grid">
                        <div class="summary-chip">
                          <span>Main signal</span>
                          <strong>Most children fall in the healthy range</strong>
                        </div>
                        <div class="summary-chip">
                          <span>Focus area</span>
                          <strong>Early support still matters</strong>
                        </div>
                      </div>
                    </div>
                  </div>
                </article>

                <div class="insight-mini-grid">
                  <article class="mini-insight-card">
                    <span class="mini-insight-label">Main signal</span>
                    <strong>Healthy range remains the largest group</strong>
                    <p>
                      The largest share of children fall within the healthy range, while overweight and
                      obesity still remain important areas for early support.
                    </p>
                  </article>

                  <article class="mini-insight-card">
                    <span class="mini-insight-label">What parents can do</span>
                    <strong>Focus on small routine shifts</strong>
                    <p>
                      Practical changes in food choices, active play, and consistency often matter more
                      than dramatic one-off efforts.
                    </p>
                  </article>
                </div>
              </div>

              <!-- SLEEP -->
              <div v-show="activeInsight === 'sleep'" class="tab-content">
                <article class="hero-insight-card polished-visual-card">
                  <div class="visual-header">
                    <span class="insight-overline">Sleep</span>
                    <h3 class="visual-title">Weeknight and weekend sleep patterns</h3>
                    <p class="visual-subtitle">
                      {{ insights.sleep.headlineBand }} {{ insights.sleep.headlineText }}
                    </p>
                  </div>

                  <div class="sleep-grid">
                    <section class="comparison-card">
                      <div class="comparison-card-head">
                        <span class="comparison-pill">Weeknight</span>
                        <strong>{{ insights.sleep.headlinePct }}%</strong>
                      </div>

                      <div
                        v-for="item in insights.sleep.weeknight"
                        :key="'weeknight-' + item.label"
                        class="comparison-row"
                      >
                        <span class="comparison-label">{{ item.label }}</span>
                        <div class="comparison-track">
                          <div
                            class="comparison-fill sleep-weeknight"
                            :style="{ width: item.value + '%' }"
                          ></div>
                        </div>
                        <strong class="comparison-value">{{ item.value }}%</strong>
                      </div>
                    </section>

                    <section class="comparison-card">
                      <div class="comparison-card-head">
                        <span class="comparison-pill muted">Weekend night</span>
                        <strong>{{ insights.sleep.weekend[3]?.value || 0 }}%</strong>
                      </div>

                      <div
                        v-for="item in insights.sleep.weekend"
                        :key="'weekend-' + item.label"
                        class="comparison-row"
                      >
                        <span class="comparison-label">{{ item.label }}</span>
                        <div class="comparison-track">
                          <div
                            class="comparison-fill sleep-weekend"
                            :style="{ width: item.value + '%' }"
                          ></div>
                        </div>
                        <strong class="comparison-value">{{ item.value }}%</strong>
                      </div>
                    </section>
                  </div>
                </article>

                <div class="insight-mini-grid">
                  <article class="mini-insight-card">
                    <span class="mini-insight-label">Weeknights</span>
                    <strong>8 to less than 9 hours is the strongest band</strong>
                    <p>
                      This is the most common weeknight sleep range, closely followed by 9 to less than
                      10 hours.
                    </p>
                  </article>

                  <article class="mini-insight-card">
                    <span class="mini-insight-label">Weekends</span>
                    <strong>Sleep patterns widen slightly</strong>
                    <p>
                      Weekend nights show a broader spread, which suggests routines can become less
                      consistent outside school days.
                    </p>
                  </article>
                </div>
              </div>

            <!-- ACTIVITY -->
            <div v-show="activeInsight === 'activity'" class="tab-content">
              <article class="hero-insight-card polished-visual-card">
                <div class="visual-header">
                  <span class="insight-overline">Activity</span>
                  <h3 class="visual-title">Average daily inactivity</h3>
                  <p class="visual-subtitle">
                    {{ insights.activity.headlineBand }} {{ insights.activity.headlineText }}
                  </p>
                </div>

                <section class="comparison-card activity-card">
                  <div class="comparison-card-head">
                    <span class="comparison-pill warm">Daily inactivity</span>
                    <strong>{{ insights.activity.headlinePct }}%</strong>
                  </div>

                  <div
                    v-for="item in insights.activity.bands"
                    :key="item.label"
                    class="comparison-row"
                  >
                    <span class="comparison-label">{{ item.label }}</span>
                    <div class="comparison-track">
                      <div
                        class="comparison-fill activity-fill"
                        :style="{ width: item.value + '%' }"
                      ></div>
                    </div>
                    <strong class="comparison-value">{{ item.value }}%</strong>
                  </div>
                </section>
              </article>

              <div class="insight-mini-grid">
                <article class="mini-insight-card">
                  <span class="mini-insight-label">Key takeaway</span>
                  <strong>Inactivity clusters around the 9-12 hour range</strong>
                  <p>
                    Several neighbouring inactivity bands are similarly high, which means long sedentary
                    periods are common rather than isolated.
                  </p>
                </article>

                <article class="mini-insight-card">
                  <span class="mini-insight-label">What helps</span>
                  <strong>Short movement breaks can make a real difference</strong>
                  <p>
                    Small bursts of movement before school, after school, and between screen-heavy
                    activities can improve daily balance.
                  </p>
                </article>
              </div>
            </div>
            </div>
          </div>
        </div>
      </section>

      <section class="feature-band">
        <div class="container feature-grid">
          <div class="feature-copy">
            <p class="section-eyebrow">How it works</p>
            <h2>One clear path from concern to action</h2>
            <p>
              Parents begin with a guided quiz, receive a personalised family plan, and use a
              dashboard to track daily actions, progress, and weekly priorities.
            </p>

            <div class="feature-points">
              <div class="feature-point">
                <strong>Step 1</strong>
                <span>Complete the parent quiz</span>
              </div>
              <div class="feature-point">
                <strong>Step 2</strong>
                <span>Receive tailored recommendations</span>
              </div>
              <div class="feature-point">
                <strong>Step 3</strong>
                <span>Follow a relevant weekly plan</span>
              </div>
            </div>
          </div>

          <div class="feature-image-block">
            <img
              src="https://images.unsplash.com/photo-1519340241574-2cec6aef0c01?auto=format&fit=crop&w=1200&q=80"
              alt="Parent and child planning together"
            />
          </div>
        </div>
      </section>

      <section id="testimonials" class="testimonials-section">
        <div class="container">
          <div class="section-heading center">
            <p class="section-eyebrow">Client stories</p>
            <h2>What parents value most</h2>
          </div>

          <div class="testimonials-grid">
            <article class="testimonial-card">
              <p>
                "HealthySteps gave us a clearer way to manage after-school time. The actions felt
                small enough to follow, and that made a huge difference."
              </p>
              <span>Parent of a 7-year-old</span>
            </article>

            <article class="testimonial-card">
              <p>
                "The dashboard helped me understand exactly what to do each day instead of just
                reading general advice. That made it feel realistic."
              </p>
              <span>Parent of a 9-year-old</span>
            </article>

            <article class="testimonial-card">
              <p>
                "I liked that it focused on progress, not perfection. It made improving routines
                feel achievable for our whole family."
              </p>
              <span>Parent of an 11-year-old</span>
            </article>
          </div>
        </div>
      </section>

      <section id="faq" class="faq-section">
        <div class="container faq-wrap">
          <div class="section-heading center">
            <p class="section-eyebrow">FAQs</p>
            <h2>Common questions</h2>
          </div>

          <div class="faq-list">
            <article class="faq-item">
              <h3>Who is HealthySteps for?</h3>
              <p>It is designed for parents of children aged 5-12 who want practical family health support.</p>
            </article>

            <article class="faq-item">
              <h3>How does the plan become personalised?</h3>
              <p>Your quiz responses shape the recommended actions, daily plan, and progress tracker shown in the dashboard.</p>
            </article>

            <article class="faq-item">
              <h3>What kinds of habits does it support?</h3>
              <p>HealthySteps focuses on nutrition, movement, sleep, screen balance, and consistent daily routines.</p>
            </article>
          </div>
        </div>
      </section>

      <section class="final-cta-section">
        <div class="container final-cta-box">
          <div>
            <p class="section-eyebrow light-eyebrow">Get started</p>
            <h2>Build a healthier routine for your family.</h2>
          </div>

          <RouterLink to="/parent-entry" class="final-cta-btn">Begin now</RouterLink>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { ref, onMounted, computed } from 'vue'

const activeInsight = ref('body')
const insights = ref(null)
const loadingInsights = ref(false)
const insightsError = ref('')

const API_URL = import.meta.env.VITE_PARENT_DATA_INSIGHTS_API_BASE_URL+'/test/data-insights'

async function fetchHomepageInsights() {
  loadingInsights.value = true
  insightsError.value = ''

  try {
    const res = await fetch(API_URL)

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`)
    }

    insights.value = await res.json()
  } catch (err) {
    console.error('Homepage insights fetch failed:', err)
    insightsError.value = err.message || 'Unable to load homepage insights right now.'
  } finally {
    loadingInsights.value = false
  }
}

onMounted(fetchHomepageInsights)

const bodySegments = computed(() => insights.value?.bodyBalance?.segments || [])

const bodyRingStyle = computed(() => {
  if (!bodySegments.value.length) {
    return {
      background: 'conic-gradient(#ddd4c9 0% 100%)'
    }
  }

  const underweight = bodySegments.value.find(s => s.key === 'underweight')?.value || 0
  const normal = bodySegments.value.find(s => s.key === 'normal')?.value || 0
  const overweight = bodySegments.value.find(s => s.key === 'overweight')?.value || 0
  const obese = bodySegments.value.find(s => s.key === 'obese')?.value || 0

  const a = underweight
  const b = underweight + normal
  const c = underweight + normal + overweight
  const d = underweight + normal + overweight + obese

  return {
    background: `conic-gradient(
      #88b6d7 0% ${a}%,
      #b9845b ${a}% ${b}%,
      #db7f27 ${b}% ${c}%,
      #5f89a3 ${c}% ${d}%,
      #ddd4c9 ${d}% 100%
    )`
  }
})
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

.home-page {
  min-height: 100vh;
  background: #ece7df;
}

.container {
  width: min(1240px, calc(100% - 48px));
  margin: 0 auto;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(236, 231, 223, 0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(20, 20, 20, 0.12);
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
  color: #111;
  font-size: 1.75rem;
  font-weight: 900;
  letter-spacing: -0.05em;
}

.nav {
  display: flex;
  align-items: center;
  gap: 28px;
}

.nav a {
  text-decoration: none;
  color: #1d1d1d;
  font-size: 0.96rem;
  font-weight: 500;
}

.nav a:hover {
  opacity: 0.72;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
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
  border: 1px solid #151515;
}

.light-btn {
  color: #151515;
  background: transparent;
}

.dark-btn {
  color: #fff;
  background: #151515;
}

.hero-section {
  padding: 28px 0 72px;
}

.hero-shell {
  position: relative;
  min-height: 820px;
}

.hero-background {
  width: 100%;
  min-height: 820px;
  border-radius: 0;
  overflow: hidden;
  background: #d8cec4;
}

.hero-background img {
  width: 100%;
  height: 820px;
  object-fit: cover;
  display: block;
}

.hero-panel {
  position: absolute;
  left: 70px;
  top: 90px;
  width: min(470px, calc(100% - 40px));
  background: rgba(241, 236, 231, 0.96);
  padding: 34px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08);
}

.hero-kicker,
.section-eyebrow {
  margin: 0 0 12px;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-weight: 800;
  color: #6c6258;
}

.hero-panel h1,
.about-wrap h2,
.section-heading h2,
.feature-copy h2,
.final-cta-box h2 {
  margin: 0;
  font-size: clamp(3rem, 6vw, 5.2rem);
  line-height: 0.92;
  /* letter-spacing: -0.08em; */
  font-weight: 800;
  color: #b2805c;
}

.hero-divider {
  width: 100%;
  height: 1px;
  background: rgba(20, 20, 20, 0.4);
  margin: 28px 0;
}

.hero-meta {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 18px;
  align-items: center;
}

.hero-meta p {
  margin: 0;
  color: #272727;
  font-size: 1rem;
  line-height: 1.55;
  max-width: 14rem;
}

.hero-cta,
.soft-brown-btn,
.final-cta-btn {
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 52px;
  padding: 0 26px;
  border-radius: 999px;
  font-size: 0.98rem;
  font-weight: 700;
}

.hero-cta,
.soft-brown-btn {
  background: #b2805c;
  color: #fff;
}

.hero-bottom-image {
  margin-top: 28px;
  border-top: 1px solid rgba(20, 20, 20, 0.45);
  padding-top: 28px;
}

.hero-bottom-image img {
  width: 100%;
  height: 220px;
  object-fit: cover;
  display: block;
}

.about-section,
.services-section,
.feature-band,
.testimonials-section,
.faq-section {
  padding: 90px 0;
}

.about-wrap {
  text-align: center;
  max-width: 980px;
  margin: 0 auto;
}

.about-wrap h2 {
  font-size: clamp(2.8rem, 5vw, 4.8rem);
  max-width: none;
}

.about-copy {
  max-width: 62rem;
  margin: 28px auto 0;
  font-size: 1.18rem;
  line-height: 1.8;
  color: #242424;
}

.about-wrap .soft-brown-btn {
  margin-top: 28px;
}

.section-heading {
  margin-bottom: 40px;
}

.section-heading.center {
  text-align: center;
}

.section-heading h2 {
  /* font-size: clamp(2.6rem, 4vw, 4.6rem); */
  max-width: none;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 26px;
}

.service-card {
  background: #efeae3;
  border: 1px solid rgba(20, 20, 20, 0.14);
}

.service-image img {
  width: 100%;
  height: 420px;
  object-fit: cover;
  display: block;
}

.service-body {
  padding: 22px 24px 28px;
  border-top: 1px solid rgba(20, 20, 20, 0.14);
}

.service-body h3,
.faq-item h3 {
  margin: 0 0 10px;
  font-size: 1.3rem;
  line-height: 1.2;
  color: #111;
}

.service-body p,
.feature-copy p,
.testimonial-card p,
.faq-item p {
  margin: 0;
  font-size: 1rem;
  line-height: 1.75;
  color: #2d2d2d;
}

.feature-grid {
  display: grid;
  grid-template-columns: 0.95fr 1.05fr;
  gap: 40px;
  align-items: center;
}

.feature-copy h2 {
  /* font-size: clamp(2.5rem, 4.6vw, 4.6rem); */
  max-width: 10ch;
}

.feature-copy p {
  margin-top: 18px;
  max-width: 38rem;
}

.feature-points {
  display: grid;
  gap: 18px;
  margin-top: 28px;
}

.feature-point {
  padding-top: 16px;
  border-top: 1px solid rgba(20, 20, 20, 0.18);
  display: grid;
  gap: 6px;
}

.feature-point strong {
  font-size: 1rem;
  color: #111;
}

.feature-point span {
  color: #4d4d4d;
  line-height: 1.6;
}

.feature-image-block img {
  width: 100%;
  height: 620px;
  object-fit: cover;
  display: block;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
  border: 1px solid rgba(20, 20, 20, 0.18);
}

.testimonial-card {
  min-height: 420px;
  padding: 54px 42px 36px;
  background: #ece7df;
  border-right: 1px solid rgba(20, 20, 20, 0.18);
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}

.testimonial-card:last-child {
  border-right: none;
}

.testimonial-card p {
  font-size: 1.1rem;
  line-height: 1.8;
}

.testimonial-card span {
  display: block;
  margin-top: 28px;
  font-size: 0.98rem;
  color: #3f3f3f;
}

.faq-wrap {
  max-width: 1020px;
  margin: 0 auto;
}

.faq-list {
  display: grid;
  gap: 18px;
}

.faq-item {
  background: #efeae3;
  padding: 24px 26px;
  border: 1px solid rgba(20, 20, 20, 0.12);
}

.final-cta-section {
  padding: 0 0 80px;
}

.final-cta-box {
  background: #181818;
  color: #fff;
  padding: 38px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.final-cta-box h2 {
  color: #fff;
  /* font-size: clamp(2.2rem, 4vw, 4rem); */
  max-width: 11ch;
}

.light-eyebrow {
  color: rgba(255, 255, 255, 0.72);
}

.final-cta-btn {
  background: #fff;
  color: #111;
  min-width: 160px;
}

@media (max-width: 1100px) {
  .services-grid,
  .feature-grid,
  .testimonials-grid,
  .final-cta-box {
    grid-template-columns: 1fr;
  }

  .feature-grid,
  .final-cta-box {
    display: grid;
  }

  .hero-panel {
    left: 34px;
    top: 34px;
  }

  .testimonial-card {
    border-right: none;
    border-bottom: 1px solid rgba(20, 20, 20, 0.18);
  }

  .testimonial-card:last-child {
    border-bottom: none;
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

  .header-actions {
    width: 100%;
  }

  .header-btn {
    flex: 1;
  }

  .container {
    width: calc(100% - 24px);
  }

  .hero-shell,
  .hero-background,
  .hero-background img {
    min-height: 720px;
    height: 720px;
  }

  .hero-panel {
    position: absolute;
    left: 18px;
    right: 18px;
    top: 18px;
    width: auto;
    padding: 24px;
  }


  .hero-meta {
    grid-template-columns: 1fr;
  }

  .hero-bottom-image img {
    height: 160px;
  }

  .service-image img {
    height: 300px;
  }

  .feature-image-block img {
    height: 360px;
  }

  .testimonial-card {
    min-height: 300px;
    padding: 34px 24px;
  }
}

.insights-section {
  padding: 90px 0;
}

.insights-grid {
  display: grid;
  grid-template-columns: 0.85fr 1.15fr;
  gap: 34px;
  align-items: start;
}

.insights-copy h2 {
  margin: 0;
  font-size: clamp(2.4rem, 4vw, 4.4rem);
  line-height: 0.95;
  font-weight: 800;
  color: #1f2940;
  max-width: 11ch;
}

.insights-copy p {
  margin: 18px 0 0;
  max-width: 34rem;
  font-size: 1rem;
  line-height: 1.75;
  color: #2d2d2d;
}

.insight-toggle {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 26px;
}

.insight-tab {
  min-height: 46px;
  padding: 0 18px;
  border-radius: 999px;
  border: 1px solid rgba(31, 41, 64, 0.15);
  background: #f5efe8;
  color: #3b312b;
  font: inherit;
  font-size: 0.96rem;
  font-weight: 700;
  cursor: pointer;
  appearance: none;
  transition: all 0.18s ease;
}

.insight-tab:hover {
  transform: translateY(-1px);
}

.insight-tab.active {
  background: #1f2940;
  color: #fff;
  border-color: #1f2940;
}

.insight-panel,
.tab-view,
.tab-content {
  display: grid;
  gap: 18px;
}

.hero-insight-card,
.mini-insight-card {
  background: #efe7df;
  border: 1px solid rgba(20, 20, 20, 0.08);
  border-radius: 28px;
  box-shadow: 0 8px 24px rgba(32, 28, 24, 0.04);
}

.hero-insight-card {
  padding: 30px;
}

.mini-insight-card {
  padding: 24px;
}

.insight-overline,
.mini-insight-label {
  display: block;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 800;
  color: #7a6d62;
}

.visual-header {
  margin-bottom: 24px;
}

.visual-title {
  margin: 10px 0 0;
  font-size: 1.7rem;
  line-height: 1.15;
  font-weight: 800;
  color: #1d2233;
}

.visual-subtitle {
  margin: 12px 0 0;
  font-size: 1rem;
  line-height: 1.7;
  color: #5a5148;
  max-width: 42rem;
}

.insight-mini-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.mini-insight-card strong {
  display: block;
  margin-top: 10px;
  font-size: 1.22rem;
  line-height: 1.28;
  color: #161616;
}

.mini-insight-card p {
  margin: 12px 0 0;
  font-size: 0.98rem;
  line-height: 1.7;
  color: #3e3a36;
}

/* BODY */
.body-visual-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 28px;
  align-items: center;
}

.body-ring-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.body-ring {
  width: 235px;
  height: 235px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.body-ring-inner {
  width: 148px;
  height: 148px;
  border-radius: 50%;
  background: #f8f3ed;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 14px;
  box-shadow: inset 0 0 0 1px rgba(20, 20, 20, 0.05);
}

.body-ring-number {
  font-size: 2.8rem;
  line-height: 1;
  font-weight: 800;
  color: #111;
}

.body-ring-label {
  margin-top: 8px;
  font-size: 0.86rem;
  font-weight: 800;
  color: #6f6359;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.body-ring-caption {
  margin: 18px 0 0;
  max-width: 240px;
  text-align: center;
  font-size: 0.98rem;
  line-height: 1.65;
  color: #4a433d;
}

.body-breakdown-panel {
  display: grid;
  gap: 16px;
}

.metric-row {
  background: #f6f0e8;
  border: 1px solid rgba(20, 20, 20, 0.06);
  border-radius: 20px;
  padding: 16px 18px;
}

.metric-row-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 10px;
}

.metric-label-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}

.metric-dot {
  width: 12px;
  height: 12px;
  border-radius: 999px;
  display: inline-block;
}

.metric-label {
  font-size: 1rem;
  font-weight: 700;
  color: #2f2a26;
}

.metric-value {
  font-size: 1rem;
  color: #111;
}

.metric-track,
.comparison-track {
  width: 100%;
  height: 12px;
  border-radius: 999px;
  background: #ddd4c9;
  overflow: hidden;
}

.metric-fill,
.comparison-fill {
  height: 100%;
  border-radius: 999px;
}

.metric-dot.underweight,
.metric-fill.underweight {
  background: #88b6d7;
}

.metric-dot.normal,
.metric-fill.normal {
  background: #b9845b;
}

.metric-dot.overweight,
.metric-fill.overweight {
  background: #db7f27;
}

.metric-dot.obese,
.metric-fill.obese {
  background: #5f89a3;
}

.summary-chip-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 6px;
}

.summary-chip {
  background: #f3ece5;
  border: 1px solid rgba(20, 20, 20, 0.06);
  border-radius: 22px;
  padding: 18px;
}

.summary-chip span {
  display: block;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 800;
  color: #7a6d62;
}

.summary-chip strong {
  display: block;
  margin-top: 8px;
  font-size: 1rem;
  line-height: 1.35;
  color: #161616;
}

/* SLEEP + ACTIVITY */
.polished-visual-card {
  display: grid;
  gap: 22px;
}

.sleep-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.comparison-card {
  background: #f6f0e8;
  border: 1px solid rgba(20, 20, 20, 0.06);
  border-radius: 24px;
  padding: 20px;
}

.comparison-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 18px;
}

.comparison-card-head strong {
  font-size: 1.45rem;
  color: #1d2233;
}

.comparison-pill {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0 14px;
  border-radius: 999px;
  background: #b9845b;
  color: #fff;
  font-size: 0.83rem;
  font-weight: 800;
  letter-spacing: 0.04em;
}

.comparison-pill.muted {
  background: #8f6f58;
}

.comparison-pill.warm {
  background: #db7f27;
}

.comparison-row {
  display: grid;
  grid-template-columns: 165px 1fr 58px;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.comparison-row:last-child {
  margin-bottom: 0;
}

.comparison-label {
  font-size: 0.93rem;
  color: #5a5148;
  line-height: 1.45;
}

.comparison-value {
  font-size: 0.95rem;
  color: #1d2233;
  text-align: right;
}

.comparison-fill.sleep-weeknight {
  background: #b9845b;
}

.comparison-fill.sleep-weekend {
  background: #8f6f58;
}

.comparison-fill.activity-fill {
  background: #db7f27;
}

/* RESPONSIVE */
@media (max-width: 1180px) {
  .insights-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 980px) {
  .body-visual-layout,
  .sleep-grid,
  .summary-chip-grid,
  .insight-mini-grid {
    grid-template-columns: 1fr;
  }

  .body-ring-panel {
    align-items: flex-start;
  }

  .body-ring-caption {
    text-align: left;
    max-width: none;
  }
}

@media (max-width: 760px) {
  .hero-insight-card,
  .mini-insight-card {
    padding: 22px;
    border-radius: 22px;
  }

  .body-ring {
    width: 210px;
    height: 210px;
  }

  .body-ring-inner {
    width: 132px;
    height: 132px;
  }

  .body-ring-number {
    font-size: 2.2rem;
  }

  .comparison-row {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .comparison-value {
    text-align: left;
  }
}

.insights-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
  align-items: stretch;
}

.insights-copy {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 760px;
}

.insights-copy h2 {
  margin: 0;
  font-size: clamp(3.8rem, 6vw, 6.2rem);
  line-height: 0.92;
  font-weight: 800;
  color: #1f2940;
  max-width: 8ch;
}

.insights-copy p {
  max-width: 30rem;
}

.insight-panel,
.tab-view,
.tab-content {
  height: 100%;
}

.tab-content {
  display: grid;
  grid-template-rows: 1fr auto;
  gap: 18px;
}

.hero-insight-card {
  min-height: 760px;
}

.insight-mini-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.mini-insight-card {
  padding: 22px;
}

.mini-insight-card strong {
  font-size: 1.12rem;
  line-height: 1.3;
}

.mini-insight-card p {
  font-size: 0.96rem;
  line-height: 1.65;
}

/* body card balance */
.body-visual-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
  align-items: center;
}

.body-ring {
  width: 215px;
  height: 215px;
}

.body-ring-inner {
  width: 136px;
  height: 136px;
}

.body-ring-number {
  font-size: 2.45rem;
}

.summary-chip-grid {
  gap: 14px;
}

.summary-chip {
  padding: 16px;
}

/* sleep + activity rows slightly tighter */
.comparison-row {
  grid-template-columns: 150px 1fr 56px;
  gap: 10px;
  margin-bottom: 10px;
}

.comparison-card {
  padding: 18px;
}

@media (max-width: 1180px) {
  .insights-grid {
    grid-template-columns: 1fr;
  }

  .insights-copy,
  .hero-insight-card {
    min-height: auto;
  }

  .insights-copy h2 {
    max-width: 11ch;
    font-size: clamp(3rem, 8vw, 5rem);
  }
}

@media (max-width: 760px) {
  .insight-mini-grid,
  .summary-chip-grid,
  .body-visual-layout,
  .sleep-grid {
    grid-template-columns: 1fr;
  }

  .comparison-row {
    grid-template-columns: 1fr;
  }
}
</style>