<!--
  KidsStatsPage.vue

  Creates the HelthyKidz kids stats page. Children can interact with steps, water,
  sleep, mood, weekly rhythm, and summary cards.

  Store requirement:
  - Uses useKidsProgressStore for live score, daily stats, progress bars, week bars, and summary cards.
  - Calls kp.hydrate() when the page loads to restore saved kids progress.

  Accessibility:
  - Uses aria-live for the live score.
  - Uses aria-labels for quantity and mood controls.
  - Uses aria-hidden for decorative emoji and visual-only elements.
-->

<template>
  <KidsRouteShell page-label="Stats">
    <div class="kids-subpage stats-page" :class="{ 'kids-context--dark': isDarkMode }">
      <div class="page-shell">
        <!-- Hero section with the page title and live healthy score -->
        <header class="hero-card">
          <div class="hero-copy">
            <span class="kicker">Stats</span>
            <h1>Move your healthy score</h1>
            <p>Tap cups, moods, moves — yesterday’s pretend numbers become today’s playful controls.</p>
          </div>

          <!-- Live score updates when progress changes across kids pages -->
          <div class="hero-score" aria-live="polite">
            <span>Live score</span>
            <strong>{{ kp.heroScorePct }}%</strong>
            <small>Updates from Meals, rainbow, taps here &amp; wins</small>
          </div>
        </header>

        <!-- Interactive stat cards -->
        <section class="stats-grid">
          <!-- Steps card -->
          <article class="stat-card tone-sky">
            <div class="stat-top">
              <span class="stat-icon">👟</span>
              <span class="stat-label">Steps</span>
            </div>
            <strong>{{ kp.stepsDisplay }}</strong>
            <p>Charge your step spark - each tap boosts your goal bar!</p>
            <div class="track"><span :style="{ width: kp.stepsProgressPct }"></span></div>
            <button type="button" class="stat-push" @click="kp.pulseSteps">Add a walk burst +</button>
          </article>

          <!-- Water card -->
          <article class="stat-card tone-mint">
            <div class="stat-top">
              <span class="stat-icon">💧</span>
              <span class="stat-label">Water</span>
            </div>
            <strong>{{ kp.waterDisplay }}</strong>
            <p>Use + / − to log cups (counts toward rainbow water too).</p>
            <div class="track"><span :style="{ width: kp.waterProgressPct }"></span></div>

            <!-- Water quantity controls -->
            <div class="qty-row">
              <button type="button" class="qty-btn" @click="kp.addWater(-1)" aria-label="Remove one cup">−</button>
              <span class="qty-label">{{ kp.daily.waterGlasses }} cups</span>
              <button type="button" class="qty-btn" @click="kp.addWater(1)" aria-label="Add one cup">+</button>
            </div>
          </article>

          <!-- Sleep card -->
          <article class="stat-card tone-violet">
            <div class="stat-top">
              <span class="stat-icon">🌙</span>
              <span class="stat-label">Sleep</span>
            </div>
            <strong>{{ kp.sleepDisplay }}</strong>
            <p>Flip the switch if bedtime felt solid last night.</p>
            <div class="track"><span :style="{ width: kp.sleepProgressPct }"></span></div>

            <!-- Sleep toggle button -->
            <button
              type="button"
              class="stat-chip-toggle"
              :class="{ active: kp.daily.sleepStars }"
              @click="kp.toggleSleepFlag"
            >
              {{ kp.daily.sleepStars ? '🌟 Great sleep vibes' : 'Tap if sleep rocked' }}
            </button>
          </article>

          <!-- Mood card -->
          <article class="stat-card tone-sun">
            <div class="stat-top">
              <span class="stat-icon">{{ kp.moodEmoji }}</span>
              <span class="stat-label">Mood</span>
            </div>
            <strong>{{ kp.moodLabel }}</strong>
            <p>Mood Mixer — pick whatever matches your energy!</p>
            <div class="track"><span :style="{ width: kp.moodProgressPct }"></span></div>

            <!-- Mood picker buttons -->
            <div class="mood-pick-row" role="group" aria-label="Pick mood bubble">
              <button
                v-for="(emo, idx) in moodEmojis"
                :key="idx"
                type="button"
                class="mood-pick"
                :class="{ active: kp.daily.mood === idx }"
                @click="kp.setMood(idx)"
              >
                <span>{{ emo }}</span>
              </button>
            </div>
          </article>
        </section>

        <!-- Weekly rhythm chart -->
        <section class="chart-card">
          <div class="chart-copy">
            <span class="kicker alt">Week view</span>
            <h2>This week’s rhythm</h2>
            <p>Bright tower on the far right is LIVE from your score meter above!</p>
          </div>

          <!-- Bar chart driven by the kids progress store -->
          <div class="bars">
            <div v-for="day in kp.weekBars" :key="day.label + '-' + day.value" class="bar-col">
              <span class="bar-value">{{ clampPct(day.value) }}%</span>
              <div class="bar-track">
                <span class="bar-fill" :style="{ height: clampPct(day.value) + '%' }"></span>
              </div>
              <span class="bar-label">{{ day.label }}</span>
            </div>
          </div>
        </section>

        <!-- Summary cards from the kids progress store -->
        <section class="summary-grid">
          <article v-for="card in kp.summaryCards" :key="card.title" class="summary-card">
            <span class="summary-icon">{{ card.icon }}</span>
            <strong>{{ card.title }}</strong>
            <p>{{ card.text }}</p>
          </article>
        </section>
      </div>
    </div>
  </KidsRouteShell>
</template>

<script setup>
import { onMounted } from 'vue'
import KidsRouteShell from "./KidsRouteShell.vue"
import { injectKidsTheme } from "../composables/useKidsTheme.js"
import { useKidsProgressStore } from "../stores/kidsProgressStore.js"

// Reads the current kids theme so the page can switch between light and dark styles.
const { isDarkMode } = injectKidsTheme()

// Kids progress store containing score, water, sleep, mood, steps, week bars, and summary cards.
const kp = useKidsProgressStore()

// Mood choices shown in the mood picker.
const moodEmojis = ["😌", "🤪", "😊", "⚡"]

// Restores saved kids progress when the page loads.
onMounted(() => {
  kp.hydrate()
})

// Keeps chart bar values within a visible range.
function clampPct(n) {
  return Math.min(99, Math.max(4, Number(n) || 0))
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=DM+Sans:wght@400;500;700&display=swap");

/* Main stats page wrapper */
.kids-subpage.stats-page {
  padding: 0 0 8px;
  color: var(--kids-ink);
}

/* Page layout container */
.page-shell {
  width: 100%;
  margin: 0 auto;
  display: grid;
  gap: 20px;
}

/* Shared card styling */
.hero-card,
.chart-card,
.stat-card,
.summary-card {
  background: var(--kids-surface);
  border: 1px solid var(--kids-border);
  box-shadow: var(--kids-card-shadow);
}

/* Hero card layout */
.hero-card {
  padding: 28px;
  border-radius: 34px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 220px;
  gap: 18px;
  align-items: center;
}

/* Small section label */
.kicker {
  display: inline-flex;
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(59, 158, 255, 0.12);
  color: #2268af;
  font-size: 0.74rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* Alternate label style */
.kicker.alt {
  background: rgba(44, 201, 122, 0.14);
  color: #188353;
}

/* Shared heading style */
.hero-copy h1,
.chart-copy h2 {
  margin: 12px 0 8px;
  font-family: "Baloo 2", cursive;
  line-height: 1;
  color: var(--kids-ink);
}

/* Main hero heading size */
.hero-copy h1 {
  font-size: clamp(1.95rem, 3.6vw, 2.9rem);
}

/* Shared paragraph styling */
.hero-copy p,
.chart-copy p,
.stat-card p,
.summary-card p {
  margin: 0;
  color: var(--kids-muted);
  line-height: 1.65;
  font-size: 0.92rem;
}

/* Live score panel */
.hero-score {
  min-height: 180px;
  border-radius: 30px;
  display: grid;
  place-items: center;
  text-align: center;
  background: radial-gradient(circle, #ffffff 0%, #eaf7ff 58%, #d6ebff 100%);
}

/* Small uppercase labels */
.hero-score span,
.bar-label,
.stat-label {
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--kids-soft);
}

/* Live score number */
.hero-score strong {
  font-family: "Baloo 2", cursive;
  font-size: 2.8rem;
  line-height: 1;
  color: var(--kids-ink);
}

/* Live score helper text */
.hero-score small {
  color: var(--kids-muted);
  font-weight: 700;
}

/* Main card grids */
.stats-grid,
.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}

/* Individual stat card */
.stat-card {
  padding: 20px;
  border-radius: 28px;
}

/* Stat card top row */
.stat-top {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

/* Stat icon bubble */
.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  background: rgba(255, 255, 255, 0.72);
  font-size: 1.4rem;
}

/* Stat value text */
.stat-card strong {
  display: block;
  margin-bottom: 6px;
  font-family: "Baloo 2", cursive;
  font-size: 1.7rem;
  color: var(--kids-ink);
}

/* Horizontal progress track */
.track {
  height: 10px;
  margin-top: 14px;
  margin-bottom: 12px;
  border-radius: 999px;
  overflow: hidden;
  background: rgba(24, 25, 43, 0.08);
}

/* Horizontal progress fill */
.track span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #56d4ff, #2cc97a);
  transition: width 0.25s ease;
}

/* Main action buttons on stat cards */
.stat-push,
.stat-chip-toggle {
  margin-top: 4px;
  width: 100%;
  padding: 10px 14px;
  border-radius: 999px;
  border: none;
  font-family: inherit;
  font-size: 0.78rem;
  font-weight: 800;
  cursor: pointer;
  background: linear-gradient(135deg, rgba(59, 158, 255, 0.22), rgba(44, 201, 122, 0.18));
  color: var(--kids-ink);
  transition: transform 0.12s ease, box-shadow 0.15s ease;
}

/* Pressed button feedback */
.stat-push:active,
.stat-chip-toggle:active {
  transform: scale(0.98);
}

/* Sleep toggle default state */
.stat-chip-toggle {
  background: rgba(68, 80, 102, 0.1);
}

/* Sleep toggle active state */
.stat-chip-toggle.active {
  box-shadow: inset 0 0 0 2px rgba(44, 201, 122, 0.45);
  background: rgba(44, 201, 122, 0.15);
}

/* Water quantity controls */
.qty-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

/* Plus and minus water buttons */
.qty-btn {
  flex: 0 0 auto;
  width: 42px;
  height: 42px;
  border-radius: 14px;
  border: none;
  font-size: 1.3rem;
  font-weight: 800;
  cursor: pointer;
  background: rgba(68, 80, 102, 0.1);
  color: var(--kids-ink);
}

/* Water cup count label */
.qty-label {
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--kids-soft);
}

/* Mood picker row */
.mood-pick-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* Mood option button */
.mood-pick {
  flex: 1;
  min-width: 56px;
  padding: 10px;
  border-radius: 14px;
  border: none;
  font-size: 1.55rem;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.55);
  box-shadow: inset 0 0 0 1px rgba(68, 80, 102, 0.12);
  transition:
    transform 0.14s ease,
    box-shadow 0.14s ease;
}

/* Selected mood state */
.mood-pick.active {
  box-shadow:
    inset 0 0 0 2px rgba(251, 191, 36, 0.55),
    0 10px 20px rgba(251, 191, 36, 0.15);
  transform: translateY(-2px);
}

/* Weekly chart container */
.chart-card {
  padding: 24px;
  border-radius: 30px;
  display: grid;
  grid-template-columns: 290px minmax(0, 1fr);
  gap: 18px;
}

/* Weekly bar layout */
.bars {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 12px;
  align-items: end;
  min-height: 240px;
}

/* Single bar column */
.bar-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

/* Bar value label */
.bar-value {
  font-size: 0.68rem;
  font-weight: 800;
  color: var(--kids-soft);
}

/* Vertical bar track */
.bar-track {
  width: 100%;
  height: 160px;
  border-radius: 18px;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
  background: rgba(68, 80, 102, 0.12);
}

/* Vertical bar fill */
.bar-fill {
  width: 100%;
  border-radius: 18px;
  transition: height 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: linear-gradient(180deg, #8ae5ff 0%, #3b9eff 42%, #2cc97a 100%);
}

/* Summary card */
.summary-card {
  padding: 20px;
  border-radius: 26px;
}

/* Summary card icon */
.summary-icon {
  display: inline-flex;
  margin-bottom: 12px;
  font-size: 2rem;
}

/* Summary card title */
.summary-card strong {
  display: block;
  margin-bottom: 6px;
  font-family: "Baloo 2", cursive;
  font-size: 1.2rem;
  color: var(--kids-ink);
}

/* Steps card background */
.tone-sky {
  background: linear-gradient(180deg, #eff7ff, rgba(255, 255, 255, 0.96));
}

/* Water card background */
.tone-mint {
  background: linear-gradient(180deg, #ebfff6, rgba(255, 255, 255, 0.96));
}

/* Sleep card background */
.tone-violet {
  background: linear-gradient(180deg, #f6f0ff, rgba(255, 255, 255, 0.96));
}

/* Mood card background */
.tone-sun {
  background: linear-gradient(180deg, #fff7e6, rgba(255, 255, 255, 0.96));
}

/* Dark mode kicker */
.kids-context--dark .kicker {
  background: rgba(59, 158, 255, 0.2);
  color: #bae6fd;
}

/* Dark mode alternate kicker */
.kids-context--dark .kicker.alt {
  background: rgba(74, 222, 128, 0.16);
  color: #bbf7d0;
}

/* Dark mode live score panel */
.kids-context--dark .hero-score {
  background:
    radial-gradient(circle, rgba(40, 50, 90, 0.95) 0%, rgba(18, 24, 48, 0.98) 68%, rgba(59, 158, 255, 0.12) 100%);
}

/* Dark mode stat icon */
.kids-context--dark .stat-icon {
  background: rgba(255, 255, 255, 0.1);
}

/* Dark mode progress track */
.kids-context--dark .track {
  background: rgba(255, 255, 255, 0.1);
}

/* Dark mode steps card */
.kids-context--dark .tone-sky {
  background: linear-gradient(180deg, rgba(120, 186, 255, 0.14), rgba(18, 22, 43, 0.92));
}

/* Dark mode water card */
.kids-context--dark .tone-mint {
  background: linear-gradient(180deg, rgba(70, 220, 160, 0.12), rgba(18, 22, 43, 0.92));
}

/* Dark mode sleep card */
.kids-context--dark .tone-violet {
  background: linear-gradient(180deg, rgba(180, 150, 255, 0.14), rgba(18, 22, 43, 0.92));
}

/* Dark mode mood card */
.kids-context--dark .tone-sun {
  background: linear-gradient(180deg, rgba(255, 206, 120, 0.14), rgba(18, 22, 43, 0.92));
}

/* Dark mode weekly bar track */
.kids-context--dark .bar-track {
  background: rgba(255, 255, 255, 0.14);
  box-shadow: inset 0 0 0 1px rgba(143, 154, 227, 0.12);
}

/* Dark mode quantity buttons */
.kids-context--dark .qty-btn {
  background: rgba(255, 255, 255, 0.12);
}

/* Dark mode mood buttons */
.kids-context--dark .mood-pick {
  background: rgba(255, 255, 255, 0.08);
}

/* Dark mode small labels */
.kids-context--dark .hero-score span,
.kids-context--dark .hero-score small,
.kids-context--dark .stat-label {
  color: rgba(198, 208, 240, 0.9);
}

/* Responsive layout for smaller screens */
@media (max-width: 960px) {
  .hero-card,
  .chart-card,
  .stats-grid,
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style>