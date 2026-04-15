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
</style>