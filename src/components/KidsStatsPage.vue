<template>
  <KidsRouteShell page-label="Stats">
    <div class="kids-subpage stats-page" :class="{ 'kids-context--dark': isDarkMode }">
      <div class="page-shell">
        <header class="hero-card">
          <div class="hero-copy">
            <span class="kicker">Stats</span>
            <h1>Move your healthy score</h1>
            <p>Tap cups, moods, moves — yesterday’s pretend numbers become today’s playful controls.</p>
          </div>
          <div class="hero-score" aria-live="polite">
            <span>Live score</span>
            <strong>{{ kp.heroScorePct }}%</strong>
            <small>Updates from Meals, rainbow, taps here &amp; wins</small>
          </div>
        </header>

        <section class="stats-grid">
          <article class="stat-card tone-sky">
            <div class="stat-top">
              <span class="stat-icon">👟</span>
              <span class="stat-label">Steps</span>
            </div>
            <strong>{{ kp.stepsDisplay }}</strong>
            <p>Charge your step spark — each tap boosts your goal bar!</p>
            <div class="track"><span :style="{ width: kp.stepsProgressPct }"></span></div>
            <button type="button" class="stat-push" @click="kp.pulseSteps">Add a walk burst +</button>
          </article>

          <article class="stat-card tone-mint">
            <div class="stat-top">
              <span class="stat-icon">💧</span>
              <span class="stat-label">Water</span>
            </div>
            <strong>{{ kp.waterDisplay }}</strong>
            <p>Use + / − to log cups (counts toward rainbow water too).</p>
            <div class="track"><span :style="{ width: kp.waterProgressPct }"></span></div>
            <div class="qty-row">
              <button type="button" class="qty-btn" @click="kp.addWater(-1)" aria-label="Remove one cup">−</button>
              <span class="qty-label">{{ kp.daily.waterGlasses }} cups</span>
              <button type="button" class="qty-btn" @click="kp.addWater(1)" aria-label="Add one cup">+</button>
            </div>
          </article>

          <article class="stat-card tone-violet">
            <div class="stat-top">
              <span class="stat-icon">🌙</span>
              <span class="stat-label">Sleep</span>
            </div>
            <strong>{{ kp.sleepDisplay }}</strong>
            <p>Flip the switch if bedtime felt solid last night.</p>
            <div class="track"><span :style="{ width: kp.sleepProgressPct }"></span></div>
            <button
              type="button"
              class="stat-chip-toggle"
              :class="{ active: kp.daily.sleepStars }"
              @click="kp.toggleSleepFlag"
            >
              {{ kp.daily.sleepStars ? '🌟 Great sleep vibes' : 'Tap if sleep rocked' }}
            </button>
          </article>

          <article class="stat-card tone-sun">
            <div class="stat-top">
              <span class="stat-icon">{{ kp.moodEmoji }}</span>
              <span class="stat-label">Mood</span>
            </div>
            <strong>{{ kp.moodLabel }}</strong>
            <p>Mood Mixer — pick whatever matches your energy!</p>
            <div class="track"><span :style="{ width: kp.moodProgressPct }"></span></div>
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

        <section class="chart-card">
          <div class="chart-copy">
            <span class="kicker alt">Week view</span>
            <h2>This week’s rhythm</h2>
            <p>Bright tower on the far right is LIVE from your score meter above!</p>
          </div>

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

const { isDarkMode } = injectKidsTheme()
const kp = useKidsProgressStore()

const moodEmojis = ["😌", "🤪", "😊", "⚡"]

onMounted(() => {
  kp.hydrate()
})

function clampPct(n) {
  return Math.min(99, Math.max(4, Number(n) || 0))
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=DM+Sans:wght@400;500;700&display=swap");

.kids-subpage.stats-page {
  padding: 0 0 8px;
  color: var(--kids-ink);
}

.page-shell {
  width: 100%;
  margin: 0 auto;
  display: grid;
  gap: 20px;
}

.hero-card,
.chart-card,
.stat-card,
.summary-card {
  background: var(--kids-surface);
  border: 1px solid var(--kids-border);
  box-shadow: var(--kids-card-shadow);
}

.hero-card {
  padding: 28px;
  border-radius: 34px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 220px;
  gap: 18px;
  align-items: center;
}

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

.kicker.alt {
  background: rgba(44, 201, 122, 0.14);
  color: #188353;
}

.hero-copy h1,
.chart-copy h2 {
  margin: 12px 0 8px;
  font-family: "Baloo 2", cursive;
  line-height: 1;
  color: var(--kids-ink);
}

.hero-copy h1 {
  font-size: clamp(1.95rem, 3.6vw, 2.9rem);
}

.hero-copy p,
.chart-copy p,
.stat-card p,
.summary-card p {
  margin: 0;
  color: var(--kids-muted);
  line-height: 1.65;
  font-size: 0.92rem;
}

.hero-score {
  min-height: 180px;
  border-radius: 30px;
  display: grid;
  place-items: center;
  text-align: center;
  background: radial-gradient(circle, #ffffff 0%, #eaf7ff 58%, #d6ebff 100%);
}

.hero-score span,
.bar-label,
.stat-label {
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--kids-soft);
}

.hero-score strong {
  font-family: "Baloo 2", cursive;
  font-size: 2.8rem;
  line-height: 1;
  color: var(--kids-ink);
}

.hero-score small {
  color: var(--kids-muted);
  font-weight: 700;
}

.stats-grid,
.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}

.stat-card {
  padding: 20px;
  border-radius: 28px;
}

.stat-top {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  background: rgba(255, 255, 255, 0.72);
  font-size: 1.4rem;
}

.stat-card strong {
  display: block;
  margin-bottom: 6px;
  font-family: "Baloo 2", cursive;
  font-size: 1.7rem;
  color: var(--kids-ink);
}

.track {
  height: 10px;
  margin-top: 14px;
  margin-bottom: 12px;
  border-radius: 999px;
  overflow: hidden;
  background: rgba(24, 25, 43, 0.08);
}

.track span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #56d4ff, #2cc97a);
  transition: width 0.25s ease;
}

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

.stat-push:active,
.stat-chip-toggle:active {
  transform: scale(0.98);
}

.stat-chip-toggle {
  background: rgba(68, 80, 102, 0.1);
}

.stat-chip-toggle.active {
  box-shadow: inset 0 0 0 2px rgba(44, 201, 122, 0.45);
  background: rgba(44, 201, 122, 0.15);
}

.qty-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

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

.qty-label {
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--kids-soft);
}

.mood-pick-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

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

.mood-pick.active {
  box-shadow:
    inset 0 0 0 2px rgba(251, 191, 36, 0.55),
    0 10px 20px rgba(251, 191, 36, 0.15);
  transform: translateY(-2px);
}

.chart-card {
  padding: 24px;
  border-radius: 30px;
  display: grid;
  grid-template-columns: 290px minmax(0, 1fr);
  gap: 18px;
}

.bars {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 12px;
  align-items: end;
  min-height: 240px;
}

.bar-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.bar-value {
  font-size: 0.68rem;
  font-weight: 800;
  color: var(--kids-soft);
}

.bar-track {
  width: 100%;
  height: 160px;
  border-radius: 18px;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
  background: rgba(68, 80, 102, 0.12);
}

.bar-fill {
  width: 100%;
  border-radius: 18px;
  transition: height 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: linear-gradient(180deg, #8ae5ff 0%, #3b9eff 42%, #2cc97a 100%);
}

.summary-card {
  padding: 20px;
  border-radius: 26px;
}

.summary-icon {
  display: inline-flex;
  margin-bottom: 12px;
  font-size: 2rem;
}

.summary-card strong {
  display: block;
  margin-bottom: 6px;
  font-family: "Baloo 2", cursive;
  font-size: 1.2rem;
  color: var(--kids-ink);
}

.tone-sky {
  background: linear-gradient(180deg, #eff7ff, rgba(255, 255, 255, 0.96));
}
.tone-mint {
  background: linear-gradient(180deg, #ebfff6, rgba(255, 255, 255, 0.96));
}
.tone-violet {
  background: linear-gradient(180deg, #f6f0ff, rgba(255, 255, 255, 0.96));
}
.tone-sun {
  background: linear-gradient(180deg, #fff7e6, rgba(255, 255, 255, 0.96));
}

.kids-context--dark .kicker {
  background: rgba(59, 158, 255, 0.2);
  color: #bae6fd;
}

.kids-context--dark .kicker.alt {
  background: rgba(74, 222, 128, 0.16);
  color: #bbf7d0;
}

.kids-context--dark .hero-score {
  background:
    radial-gradient(circle, rgba(40, 50, 90, 0.95) 0%, rgba(18, 24, 48, 0.98) 68%, rgba(59, 158, 255, 0.12) 100%);
}

.kids-context--dark .stat-icon {
  background: rgba(255, 255, 255, 0.1);
}

.kids-context--dark .track {
  background: rgba(255, 255, 255, 0.1);
}

.kids-context--dark .tone-sky {
  background: linear-gradient(180deg, rgba(120, 186, 255, 0.14), rgba(18, 22, 43, 0.92));
}

.kids-context--dark .tone-mint {
  background: linear-gradient(180deg, rgba(70, 220, 160, 0.12), rgba(18, 22, 43, 0.92));
}

.kids-context--dark .tone-violet {
  background: linear-gradient(180deg, rgba(180, 150, 255, 0.14), rgba(18, 22, 43, 0.92));
}

.kids-context--dark .tone-sun {
  background: linear-gradient(180deg, rgba(255, 206, 120, 0.14), rgba(18, 22, 43, 0.92));
}

.kids-context--dark .bar-track {
  background: rgba(255, 255, 255, 0.14);
  box-shadow: inset 0 0 0 1px rgba(143, 154, 227, 0.12);
}

.kids-context--dark .qty-btn {
  background: rgba(255, 255, 255, 0.12);
}

.kids-context--dark .mood-pick {
  background: rgba(255, 255, 255, 0.08);
}

.kids-context--dark .hero-score span,
.kids-context--dark .hero-score small,
.kids-context--dark .stat-label {
  color: rgba(198, 208, 240, 0.9);
}

@media (max-width: 960px) {
  .hero-card,
  .chart-card,
  .stats-grid,
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style>
