<template>
  <div class="landing" :class="{ loaded: isLoaded }">

    <!-- Background -->
    <div class="landing__bg">
      <img
        class="landing__bg-img"
        src="https://images.unsplash.com/photo-1542037104857-ffbb0b9155fb?auto=format&fit=crop&w=2400&q=90"
        alt=""
        aria-hidden="true"
      />
      <div class="landing__bg-overlay"></div>
      <div class="landing__bg-vignette"></div>
      <div class="landing__bg-grain"></div>
    </div>

    <!-- Header -->
    <header class="landing__header">
      <RouterLink to="/" class="landing__logo">
        <div class="logo-icon">
          <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2"/>
            <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor"/>
            <path d="M18 13C15.5 15.5 15 19 18 23" stroke="white" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.55"/>
          </svg>
        </div>
        <span class="logo-text">HealthyKids</span>
      </RouterLink>

      <RouterLink to="/parent-entry" class="header-pill">
        Parent portal
        <svg width="12" height="12" viewBox="0 0 12 12"><path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </RouterLink>
    </header>

    <!-- Main -->
    <main class="landing__main">

      <!-- Left: copy -->
      <div class="landing__copy">

        <div class="landing__eyebrow">
          <span class="eyebrow-dot"></span>
          Australia · 2025
        </div>

        <h1 class="landing__headline">
          <span class="h-line h-line-1">Healthier</span>
          <span class="h-line h-line-2">families</span>
          <span class="h-line h-line-3">start here.</span>
        </h1>

        <p class="landing__sub">
          A personalised health plan for children aged 5-12,
          built around nutrition, movement, sleep and daily routine.
        </p>

        <div class="landing__ctas">
          <RouterLink to="/parent-entry" class="cta cta--primary">
            Enter site
            <!-- <svg width="16" height="16" viewBox="0 0 16 16">
              <path d="M3 8h10M9 4.5l4 3.5-4 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg> -->
          </RouterLink>
          <!-- <RouterLink to="/parent-entry" class="cta cta--ghost">
            I'm a parent
          </RouterLink> -->
        </div>

        <div class="landing__pills">
          <span class="pill">
            <span class="pill-dot"></span>
            12,000+ families
          </span>
          <span class="pill">
            <span class="pill-dot"></span>
            Ages 5-12
          </span>
          <span class="pill">
            <span class="pill-dot"></span>
            3-min onboarding
          </span>
        </div>
      </div>
    </main>

    <!--  Footer bar  -->
    <footer class="landing__footer">
      <div class="landing__footer-left">
        <span class="live-dot"></span>
        Supporting families across Australia
      </div>
      <div class="landing__footer-right">
        UN SDG 3 · Good Health &amp; Wellbeing
      </div>
    </footer>

  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { onMounted, ref } from 'vue'

const isLoaded = ref(false)
onMounted(() => { setTimeout(() => { isLoaded.value = true }, 80) })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;1,300;1,400&family=DM+Sans:wght@400;500;600;700;800&display=swap');

*,*::before,*::after { box-sizing: border-box; margin: 0; padding: 0; }

.landing {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow-x: hidden;
  overflow-y: auto;
}

.landing__bg {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.landing__bg-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 38%;
  transform: scale(1.06);
  transition: transform 9s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.loaded .landing__bg-img { transform: scale(1); }

.landing__bg-overlay {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(100deg,
      rgba(4, 10, 6, 0.94) 0%,
      rgba(4, 10, 6, 0.80) 30%,
      rgba(4, 10, 6, 0.40) 60%,
      rgba(4, 10, 6, 0.16) 100%
    ),
    linear-gradient(180deg,
      rgba(4, 10, 6, 0.54) 0%,
      transparent 38%,
      rgba(4, 10, 6, 0.72) 100%
    );
}

.landing__bg-vignette {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 18% 62%, rgba(34,197,94,0.15) 0%, transparent 52%),
    radial-gradient(ellipse at 78% 22%, rgba(255,255,255,0.04) 0%, transparent 30%);
  pointer-events: none;
}

.landing__bg-grain {
  position: absolute;
  inset: 0;
  opacity: 0.045;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 180px;
}


.landing__header {
  position: absolute;
  top: 0; left: 0; right: 0;
  z-index: 30;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 32px 52px;
  opacity: 0;
  transform: translateY(-10px);
  transition: opacity 0.65s 0.1s ease, transform 0.65s 0.1s ease;
}
.loaded .landing__header { opacity: 1; transform: translateY(0); }

.landing__logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: rgba(255,255,255,0.94);
  text-decoration: none;
}
.logo-icon { width: 28px; height: 28px; color: currentColor; }
.logo-text {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.22rem;
  font-weight: 400;
  letter-spacing: -0.03em;
}

.header-pill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  height: 40px;
  padding: 0 18px;
  border-radius: 999px;
  color: rgba(255,255,255,0.9);
  text-decoration: none;
  font-size: 0.84rem;
  font-weight: 700;
  background: rgba(255,255,255,0.10);
  border: 1px solid rgba(255,255,255,0.18);
  backdrop-filter: blur(14px);
  transition: background 0.2s, transform 0.22s cubic-bezier(0.34,1.56,0.64,1);
}
.header-pill:hover {
  background: rgba(255,255,255,0.18);
  transform: translateY(-2px);
}

.landing__main {
  position: relative;
  z-index: 10;
  height: 100vh;
  display: grid;
  grid-template-columns: minmax(0, 580px) 1fr;
  align-items: center;
  gap: 40px;
  padding: 0 52px;
  margin: 0 auto;
  min-height: 100vh;
}

.landing__copy {
  display: flex;
  flex-direction: column;
}

/* Eyebrow */
.landing__eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 30px;
  padding: 0 13px;
  border-radius: 999px;
  margin-bottom: 28px;
  color: #86efac;
  background: rgba(34,197,94,0.13);
  border: 1px solid rgba(134,239,172,0.22);
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  align-self: flex-start;
  opacity: 0;
  transition: opacity 0.55s 0.2s ease;
}
.loaded .landing__eyebrow { opacity: 1; }

.eyebrow-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: #4ade80;
  animation: pulse 2.4s ease-in-out infinite;
}

/* Headline */
.landing__headline {
  display: flex;
  flex-direction: column;
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 300;
  font-size: clamp(4.2rem, 7vw, 8.8rem);
  line-height: 0.88;
  letter-spacing: -0.055em;
  color: #fff;
  margin-bottom: 28px;
}

.h-line {
  display: block;
  opacity: 0;
  transform: translateY(34px);
  transition: opacity 0.72s ease, transform 0.72s cubic-bezier(0.16, 1, 0.3, 1);
}
.h-line-1 { transition-delay: 0.28s; }
.h-line-2 {
  font-style: italic;
  color: #4ade80;
  text-shadow: 0 6px 28px rgba(74,222,128,0.22);
  transition-delay: 0.43s;
}
.h-line-3 { transition-delay: 0.58s; }
.loaded .h-line { opacity: 1; transform: translateY(0); }

/* Sub */
.landing__sub {
  font-size: clamp(0.96rem, 1.15vw, 1.1rem);
  line-height: 1.76;
  color: rgba(255,255,255,0.62);
  margin-bottom: 36px;
  max-width: 420px;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.6s 0.74s ease, transform 0.6s 0.74s ease;
}
.loaded .landing__sub { opacity: 1; transform: translateY(0); }

/* CTAs */
.landing__ctas {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 24px;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.6s 0.88s ease, transform 0.6s 0.88s ease;
}
.loaded .landing__ctas { opacity: 1; transform: translateY(0); }

.cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  height: 54px;
  padding: 0 28px;
  border-radius: 999px;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.92rem;
  font-weight: 800;
  text-decoration: none;
  white-space: nowrap;
  transition:
    transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1),
    box-shadow 0.22s ease,
    background 0.2s;
}
.cta--primary {
  background: #16a34a;
  color: #fff;
  box-shadow: 0 10px 32px rgba(22,163,74,0.44);
}
.cta--primary:hover {
  transform: translateY(-3px);
  background: #15803d;
  box-shadow: 0 16px 42px rgba(22,163,74,0.56);
}
.cta--ghost {
  color: rgba(255,255,255,0.88);
  background: rgba(255,255,255,0.10);
  border: 1.5px solid rgba(255,255,255,0.22);
  backdrop-filter: blur(12px);
}
.cta--ghost:hover {
  transform: translateY(-3px);
  color: #fff;
  background: rgba(255,255,255,0.18);
}

/* Stat pills */
.landing__pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.55s 1.02s ease;
}
.loaded .landing__pills { opacity: 1; }

.pill {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  height: 32px;
  padding: 0 13px;
  border-radius: 999px;
  font-size: 0.74rem;
  font-weight: 700;
  color: rgba(255,255,255,0.62);
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.11);
}
.pill-dot {
  width: 5px; height: 5px;
  border-radius: 50%;
  background: #4ade80;
  flex-shrink: 0;
}

.landing__stats {
  position: relative;
  height: 480px;
  pointer-events: none;
  user-select: none;
}

.stat-card {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 22px;
  border-radius: 20px;
  background: linear-gradient(145deg, rgba(255,255,255,0.14), rgba(255,255,255,0.07));
  border: 1px solid rgba(255,255,255,0.16);
  box-shadow: 0 20px 50px rgba(0,0,0,0.30), inset 0 1px 0 rgba(255,255,255,0.13);
  backdrop-filter: blur(18px);
  opacity: 0;
  transition: opacity 0.65s ease;
  white-space: nowrap;
}

.loaded .stat-card { opacity: 1; }

.stat-card-1 { top: 30px;  left: 0;    transition-delay: 0.55s; animation: float-a 6s   ease-in-out 1.2s infinite; }
.stat-card-2 { top: 148px; left: 55px; transition-delay: 0.72s; animation: float-b 7s   ease-in-out 1.5s infinite; }
.stat-card-3 { top: 265px; left: 5px;  transition-delay: 0.89s; animation: float-c 5.5s ease-in-out 1.0s infinite; }
.stat-card-4 { top: 375px; left: 70px; transition-delay: 1.05s; animation: float-a 6.5s ease-in-out 1.7s infinite; }

@keyframes float-a { 0%,100%{transform:translateY(0)}   50%{transform:translateY(-10px)} }
@keyframes float-b { 0%,100%{transform:translateY(0)}   50%{transform:translateY(-7px)}  }
@keyframes float-c { 0%,100%{transform:translateY(0)}   50%{transform:translateY(-12px)} }

.stat-card__icon {
  width: 42px; height: 42px;
  border-radius: 12px;
  background: rgba(255,255,255,0.10);
  display: grid;
  place-items: center;
  font-size: 1.25rem;
  flex-shrink: 0;
}

.stat-card__number {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 2.4rem;
  font-weight: 300;
  color: #4ade80;
  line-height: 1;
  letter-spacing: -0.04em;
  flex-shrink: 0;
}
.stat-card__number span { font-size: 1.1rem; vertical-align: super; }

.stat-card__body strong {
  display: block;
  font-size: 0.88rem;
  font-weight: 700;
  color: rgba(255,255,255,0.92);
  margin-bottom: 3px;
}
.stat-card__body span {
  font-size: 0.76rem;
  color: rgba(255,255,255,0.50);
  line-height: 1.45;
}

.landing__footer {
  position: absolute;
  left: 0; right: 0; bottom: 0;
  z-index: 30;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 15px 52px;
  color: rgba(255,255,255,0.40);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  background: rgba(4,10,6,0.55);
  border-top: 1px solid rgba(255,255,255,0.08);
  backdrop-filter: blur(14px);
  opacity: 0;
  transition: opacity 0.6s 1.12s ease;
}
.loaded .landing__footer { opacity: 1; }

.landing__footer-left {
  display: flex;
  align-items: center;
  gap: 9px;
}

.live-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #22c55e;
  animation: pulse 2.2s ease-in-out infinite;
}

@keyframes pulse {
  0%,100% { box-shadow: 0 0 0 0 rgba(34,197,94,0.50); }
  50%      { box-shadow: 0 0 0 6px rgba(34,197,94,0);  }
}

@media (max-width: 1000px) {
  .landing__main {
    grid-template-columns: 1fr;
    align-items: flex-end;
    padding: 0 32px 80px;
  }
  .landing__stats { display: none; }
}

@media (max-width: 700px) {
  .landing__header { padding: 22px 24px; }
  .header-pill { display: none; }
  .landing__main { padding: 0 22px 78px; }
  .landing__footer { padding: 14px 22px; flex-direction: column; align-items: flex-start; gap: 4px; }
  .landing__headline { font-size: clamp(3.4rem, 16vw, 5.2rem); }
  .landing__ctas { flex-direction: column; align-items: stretch; }
  .cta { width: 100%; }
  .landing__pills { flex-direction: column; }
  .pill { width: 100%; justify-content: flex-start; }
}
</style>