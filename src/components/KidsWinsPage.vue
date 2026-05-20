<!--
  KidsWinsPage.vue

  Creates the HelthyKidz kids wins page. Children can tap win cards to earn XP,
  track challenge progress, and view unlocked badges.

  Store requirement:
  - Uses useKidsProgressStore for XP, badges, daily win taps, and challenge progress.
  - Calls kp.hydrate() when the page loads to restore saved kids progress.

  Accessibility:
  - Uses keyboard-friendly win cards with tabindex, Enter, and Space support.
  - Uses aria-hidden for decorative emoji and visual-only elements.
  - Uses role="presentation" for the decorative progress track.
-->

<template>
  <KidsRouteShell page-label="Wins">
    <div class="kids-subpage wins-page" :class="{ 'kids-context--dark': isDarkMode }">
      <div class="page-shell">
        <!-- Hero section introducing the wins page -->
        <header class="hero-card">
          <div class="hero-copy">
            <span class="kicker">Wins</span>
            <h1>Wins trophy room</h1>
            <p>Tap a win card → XP shoots up everywhere (Stats score + Meals boost too)!</p>
          </div>

          <!-- Decorative trophy bubble -->
          <div class="trophy-bubble" aria-hidden="true">🏆</div>
        </header>

        <!-- Challenge progress summary -->
        <section class="challenge-card">
          <div>
            <span class="kicker alt">Challenge</span>
            <h2>Veggie Champion</h2>
            <p>Every tap earns XP toward the sparkly badge vault below.</p>
          </div>

          <!-- XP progress for the active challenge -->
          <div class="challenge-score">
            <strong>{{ kp.challengeXp }} / {{ kp.challengeMax }} XP</strong>
            <div class="track" role="presentation">
              <span :style="{ width: kp.challengePct + '%' }"></span>
            </div>
            <small class="xp-hint">Need another {{ Math.max(0, kp.challengeMax - kp.challengeXp) }} XP before legend mode.</small>
          </div>
        </section>

        <!-- Tap-to-earn win cards -->
        <section class="wins-grid">
          <article
            v-for="win in wins"
            :key="win.id"
            class="win-card"
            role="button"
            tabindex="0"
            @click="kp.tapWin(win.id)"
            @keyup.enter.prevent="kp.tapWin(win.id)"
            @keyup.space.prevent="kp.tapWin(win.id)"
          >
            <span class="win-icon">{{ win.icon }}</span>
            <strong>{{ win.title }}</strong>
            <p>{{ win.text }}</p>
            <span class="win-ping">{{ (kp.daily.winPings && kp.daily.winPings[win.id]) || 0 }} cheers today · keeps {{ kp.xpPerWinTap }} XP each!</span>
          </article>
        </section>

        <!-- Badge shelf showing earned and locked badges -->
        <section class="badges-card">
          <div class="badges-head">
            <div>
              <span class="kicker alt">Badge shelf</span>
              <h2>Stars charged up</h2>
            </div>

            <!-- Visual star progress row -->
            <div class="stars-row" aria-hidden="true">
              <span
                v-for="n in 5"
                :key="n"
                class="star"
                :class="{ earned: kp.starsEarnedComputed >= n }"
              >★</span>
            </div>
          </div>

          <!-- Badge cards from the kids progress store -->
          <div class="badge-grid">
            <article
              v-for="badge in kp.badgesDeck"
              :key="badge.id"
              class="badge-item"
              :class="{ unlocked: badge.earned }"
            >
              <span class="badge-emoji">{{ badge.icon }}</span>
              <strong>{{ badge.title }}</strong>
              <p>{{ badge.text }}</p>
              <span class="badge-state">{{ badge.earned ? 'Unlocked!' : 'Keep playing' }}</span>
            </article>
          </div>
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

// Reads the current kids theme so the page can switch between light and dark context styles.
const { isDarkMode } = injectKidsTheme()

// Kids progress store containing XP, badges, challenge progress, and win tap actions.
const kp = useKidsProgressStore()

// Win card data shown in the trophy room.
const wins = [
  { id: 'veggie', icon: '🥦', title: 'Healthy bites hero', text: 'Stack fruit + veggie combos like a ninja.' },
  { id: 'water', icon: '💧', title: 'Water power', text: 'Hydration rockets when you slam those cups!' },
  { id: 'sleep', icon: '🌙', title: 'Sleep star', text: 'Flip the sleepy switch anytime you rocked rest.' },
  { id: 'energy', icon: '⚡', title: 'Energy hero', text: 'Run, jump, wiggle — then celebrate here!' },
]

// Restores saved kids progress when the page loads.
onMounted(() => {
  kp.hydrate()
})
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=DM+Sans:wght@400;500;700&display=swap");

/* Main wins page wrapper */
.kids-subpage.wins-page {
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
.challenge-card,
.win-card,
.badges-card,
.badge-item {
  background: var(--kids-surface);
  border: 1px solid var(--kids-border);
  box-shadow: var(--kids-card-shadow);
}

/* Hero card layout */
.hero-card {
  padding: 28px;
  border-radius: 34px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 180px;
  gap: 18px;
  align-items: center;
}

/* Small label pill */
.kicker {
  display: inline-flex;
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(255, 126, 179, 0.13);
  color: #c33f7d;
  font-size: 0.74rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

/* Alternative label style used for challenge and badge sections */
.kicker.alt {
  background: rgba(255, 176, 32, 0.14);
  color: #b96f00;
}

/* Shared heading style */
.hero-copy h1,
.challenge-card h2,
.badges-head h2 {
  margin: 12px 0 8px;
  font-family: "Baloo 2", cursive;
  line-height: 1;
  color: var(--kids-ink);
}

/* Main hero title sizing */
.hero-copy h1 {
  font-size: clamp(1.95rem, 3.6vw, 2.9rem);
}

/* Shared paragraph style */
.hero-copy p,
.challenge-card p,
.win-card p,
.badge-item p {
  margin: 0;
  color: var(--kids-muted);
  line-height: 1.65;
  font-size: 0.92rem;
}

/* Animated trophy decoration */
.trophy-bubble {
  width: 148px;
  height: 148px;
  margin-inline: auto;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 3.3rem;
  background:
    radial-gradient(circle, #ffffff 0%, #fff0c7 58%, #ffd970 100%);
  box-shadow:
    inset 0 0 0 12px rgba(255, 255, 255, 0.7),
    0 20px 44px rgba(255, 176, 32, 0.18);
  animation: bob 3s ease-in-out infinite;
}

/* Floating animation for trophy bubble */
@keyframes bob {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}

/* Challenge progress card */
.challenge-card {
  padding: 24px;
  border-radius: 30px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 280px;
  gap: 18px;
  align-items: center;
}

/* Challenge XP number */
.challenge-score strong {
  display: block;
  margin-bottom: 12px;
  font-family: "Baloo 2", cursive;
  font-size: 1.7rem;
  color: var(--kids-ink);
}

/* XP hint below the progress track */
.xp-hint {
  display: block;
  margin-top: 10px;
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--kids-soft);
}

/* Win and badge card titles */
.win-card strong,
.badge-item strong {
  display: block;
  margin-bottom: 6px;
  font-family: "Baloo 2", cursive;
  font-size: 1.14rem;
  color: var(--kids-ink);
}

/* Interactive win card */
.win-card {
  cursor: pointer;
  transition:
    transform 0.14s ease,
    box-shadow 0.14s ease;
}

/* Tap feedback for win cards */
.win-card:active {
  transform: scale(0.99);
}

/* Keyboard focus style for win cards */
.win-card:focus-visible {
  outline: 2px solid rgba(251, 191, 36, 0.75);
  outline-offset: 3px;
}

/* Daily cheer count text */
.win-ping {
  display: inline-block;
  margin-top: 12px;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.03em;
  color: var(--kids-soft);
}

/* Icon boxes for wins and badges */
.win-icon,
.badge-emoji {
  display: inline-grid;
  place-items: center;
  width: 58px;
  height: 58px;
  margin-bottom: 12px;
  border-radius: 18px;
  background: rgba(155, 114, 255, 0.1);
  font-size: 1.7rem;
}

/* Unearned star style */
.star {
  color: var(--kids-soft);
  opacity: 0.65;
}

/* Earned star style */
.star.earned {
  color: #ffb020;
  opacity: 1;
  text-shadow: 0 0 14px rgba(255, 176, 32, 0.5);
}

/* XP progress track */
.track {
  height: 14px;
  border-radius: 999px;
  overflow: hidden;
  background: rgba(68, 80, 102, 0.12);
}

/* XP progress fill */
.track span {
  display: block;
  height: 100%;
  width: 68%;
  border-radius: inherit;
  background: linear-gradient(90deg, #ffb020 0%, #ff7eb3 100%);
  transition: width 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Dark mode progress track */
.kids-context--dark .track {
  background: rgba(255, 255, 255, 0.1);
}

/* Dark mode trophy bubble */
.kids-context--dark .trophy-bubble {
  background:
    radial-gradient(circle, rgba(40, 48, 88, 1) 0%, rgba(20, 26, 52, 1) 70%, rgba(255, 200, 100, 0.15) 100%);
  box-shadow:
    inset 0 0 0 12px rgba(255, 255, 255, 0.06),
    0 20px 44px rgba(3, 7, 23, 0.5);
}

/* Dark mode kicker */
.kids-context--dark .kicker {
  background: rgba(255, 126, 179, 0.2);
  color: #fbcfe8;
}

/* Dark mode alternate kicker */
.kids-context--dark .kicker.alt {
  background: rgba(255, 176, 32, 0.18);
  color: #fcd34d;
}

/* Dark mode unearned stars */
.kids-context--dark .star {
  color: rgba(226, 234, 255, 0.35);
}

/* Dark mode icon boxes */
.kids-context--dark .win-icon,
.kids-context--dark .badge-emoji {
  background: rgba(255, 255, 255, 0.08);
}

/* Responsive grids for win and badge cards */
.wins-grid,
.badge-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
}

/* Card spacing */
.win-card,
.badge-item {
  padding: 20px;
  border-radius: 26px;
}

/* Badge shelf container */
.badges-card {
  padding: 24px;
  border-radius: 30px;
}

/* Badge shelf header */
.badges-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  margin-bottom: 18px;
}

/* Star row layout */
.stars-row {
  display: flex;
  gap: 8px;
  font-size: 1.6rem;
}

/* Badge card animation */
.badge-item {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}

/* Unlocked badge emphasis */
.badge-item.unlocked {
  box-shadow:
    inset 0 0 0 2px rgba(44, 201, 122, 0.35),
    var(--kids-card-shadow);
}

/* Locked badge style */
.badge-item:not(.unlocked) {
  opacity: 0.74;
}

/* Badge status label */
.badge-state {
  display: inline-block;
  margin-top: 11px;
  font-size: 0.71rem;
  font-weight: 900;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: #188353;
}

/* Dark mode badge status */
.kids-context--dark .badge-state {
  color: #6ee7b7;
}

/* Dark mode locked badge style */
.kids-context--dark .badge-item:not(.unlocked) {
  opacity: 0.55;
}

/* Responsive layout for smaller screens */
@media (max-width: 960px) {
  .hero-card,
  .challenge-card,
  .wins-grid,
  .badge-grid {
    grid-template-columns: 1fr;
  }

  .badges-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>