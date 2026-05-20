<!--
  KidsGamesPage.vue

  Creates the HelthyKidz kids games page. Children can choose between different
  mini-games, view game instructions, and play the selected game inside the shared kids shell.

  Component requirement:
  - Uses KidsRouteShell for the shared kids layout.
  - Uses injectKidsTheme for light and dark mode styling.
  - Uses async game components so each game loads only when needed.
  - Reads route.query.game to open a specific game tab.

  Accessibility:
  - Uses aria-label for the games tab list and info buttons.
  - Marks decorative game icons as aria-hidden.
  - Uses click-outside behaviour for the info modal backdrop.
-->

<template>
  <KidsRouteShell page-label="Games">
    <div class="game-zone-page" :class="{ 'kids-context--dark': isDarkMode }">
      <main class="zone-shell">
      <!-- Hero section with current game summary and info button -->
      <section class="zone-hero">
        <div class="zone-hero-copy">
          <p class="zone-kicker">Games</p>
          <div class="zone-title-row">
            <h1>Pick a game and play</h1>
            <button type="button" class="info-btn" @click="showInfo = true" aria-label="Show game info">i</button>
          </div>
          <div class="zone-hero-side">
            <span>{{ currentGameMeta.short }}</span>
            <strong>{{ currentGameMeta.tag }}</strong>
          </div>
        </div>
      </section>

      <!-- Game selection tabs -->
      <section class="zone-tabs" role="tablist" aria-label="Kids games">
        <button
          v-for="game in gameCards"
          :key="game.id"
          type="button"
          class="zone-tab"
          :class="{ active: activeGame === game.id }"
          @click="activeGame = game.id"
        >
          <span class="zone-tab-icon" aria-hidden="true">{{ game.icon }}</span>
          <span class="zone-tab-copy">
            <strong>{{ game.title }}</strong>
            <small>{{ game.short }}</small>
          </span>
        </button>
      </section>

      <!-- Active game panel -->
      <section class="zone-panel">
        <header class="zone-panel-head">
          <div class="zone-panel-title-row">
            <p class="zone-kicker">{{ currentGameMeta.kicker }}</p>
            <h2>{{ currentGameMeta.title }}</h2>
          </div>
        </header>

        <!-- Bubble game -->
        <section v-if="activeGame === 'bubble'" class="game-shell">
          <BubbleAdventureGame />
        </section>

        <!-- Explorer matching game -->
        <section v-else-if="activeGame === 'explorer'" class="game-shell">
          <HealthyHabitsLab />
        </section>

        <!-- Hum It voice game -->
        <section v-else-if="activeGame === 'humit'" class="game-shell">
          <HumItGame />
        </section>

        <!-- Routine Rumble smash game -->
        <section v-else class="game-shell">
          <SmashWiggleGame />
        </section>
      </section>
      </main>

      <!-- Game information modal -->
      <div v-if="showInfo" class="info-modal-backdrop" @click.self="showInfo = false">
      <div class="info-modal">
        <div class="info-modal-head">
          <div>
            <p class="zone-kicker">How to play</p>
            <h3>{{ currentGameMeta.title }}</h3>
          </div>
          <button type="button" class="info-close" @click="showInfo = false" aria-label="Close info">×</button>
        </div>
        <p class="info-lead">{{ currentGameMeta.description }}</p>
        <ul class="info-list">
          <li v-for="item in currentGameMeta.instructions" :key="item">{{ item }}</li>
        </ul>
      </div>
      </div>
    </div>
  </KidsRouteShell>
</template>

<script setup>
import { computed, defineAsyncComponent, ref, watch } from "vue"
import { useRoute } from "vue-router"
import KidsRouteShell from "./KidsRouteShell.vue"
import { injectKidsTheme } from "../composables/useKidsTheme.js"

// Reads the current kids theme so the page can apply light or dark mode styling.
const { isDarkMode } = injectKidsTheme()

// Async game components keep the games page lighter by loading game files only when required.
const BubbleAdventureGame = defineAsyncComponent(() => import("./game/BubbleAdventureGame.vue"))
const HealthyHabitsLab = defineAsyncComponent(() => import("./game/HealthyHabitsLab.vue"))
const SmashWiggleGame = defineAsyncComponent(() => import("./game/SmashWiggleGame.vue"))
const HumItGame = defineAsyncComponent(() => import("./game/HumItGame.vue"))

// Route and modal state.
const route = useRoute()
const showInfo = ref(false)

// Game metadata used for tabs, hero copy, and the info modal.
const gameCards = [
  {
    id: "bubble",
    icon: "🫧",
    kicker: "Bubble mission",
    title: "Healthy Bubble Game",
    short: "Pop bright healthy words",
    description: "Tap the bright target bubbles, dodge the wrong ones, and build a colorful word-pop streak.",
    helper: "Quick taps and bright bubble wins",
    tag: "Fast fingers fun",
    instructions: [
      "Tap the bright target bubbles as fast as you can.",
      "Skip the wrong bubble words so your score keeps growing.",
      "Build a combo streak to make the round feel extra fun.",
    ],
  },
  {
    id: "explorer",
    icon: "🧭",
    kicker: "Explorer mission",
    title: "Explorer Game",
    short: "Match bright healthy pairs",
    description: "Match colorful cards, unlock healthy combos, and discover smart little habit wins.",
    helper: "Calm matching and discovery play",
    tag: "Puzzle adventure fun",
    instructions: [
      "Pick two matching cards to make a healthy pair.",
      "Use the preview area to see what combo you are building.",
      "Finish a set to move ahead into the next explorer stage.",
    ],
  },
  {
    id: "humit",
    icon: "🎵",
    kicker: "Voice adventure",
    title: "Hum It!",
    short: "Your hum powers your creature",
    description:
      "Hum into the mic — pitch, volume, and steady tones shape a creature and beat Hum Hills challenges. Demo sliders work without a microphone.",
    helper: "Breathing, pitch play, and silly wins",
    tag: "Voice-driven fun",
    instructions: [
      "Allow the microphone when asked, or choose demo sliders if you cannot use a mic.",
      "Hum high, low, loud, soft, or stay silent — match what your creature asks for.",
      "There are no game overs: every hum teaches something and keeps the streak friendly.",
    ],
  },
  {
    id: "smash",
    icon: "🎈",
    kicker: "Smash mission",
    title: "Routine Rumble",
    short: "Smash healthy targets",
    description: "Swing the hero through food, water, sleep, and routine targets to power up every mission.",
    helper: "Big swings and happy habit power",
    tag: "Energetic action fun",
    instructions: [
      "Drag and swing the hero into the matching targets.",
      "Keep combos going to raise your score faster.",
      "Fill each mission meter to unlock the next healthy challenge.",
    ],
  },
]

// Currently selected game tab.
const activeGame = ref("bubble")

// Metadata for the currently selected game.
const currentGameMeta = computed(() => gameCards.find(game => game.id === activeGame.value) ?? gameCards[0])

// Opens a game directly when the URL contains a valid game query.
watch(
  () => route.query.game,
  value => {
    const next = typeof value === "string" ? value : "bubble"
    activeGame.value = gameCards.some(game => game.id === next) ? next : "bubble"
  },
  { immediate: true }
)
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap");

/* Main games page wrapper and local colour tokens */
.game-zone-page {
  --coral: #ff6058;
  --sky: #3b9eff;
  --mint: #2cc97a;
  --amber: #ffb020;
  --violet: #9b72ff;
  --rose: #ff7eb3;
  --ink: var(--kids-ink, #18192b);
  --ink2: var(--kids-muted, #445066);
  --muted: var(--kids-soft, #5a6278);
  --border: var(--kids-border, rgba(238, 239, 245, 0.95));
  --white: #ffffff;
  --bg: var(--kids-bg, #f4f5fb);
  --card-shadow: var(--kids-card-shadow, 0 2px 16px rgba(24, 25, 43, 0.07));
  --card-shadow-hover: 0 12px 40px rgba(24, 25, 43, 0.13);

  font-family: "DM Sans", sans-serif;
  background: transparent;
  color: var(--ink);
  position: relative;
}

/* Dark mode hover shadow */
.game-zone-page.kids-context--dark {
  --card-shadow-hover: 0 18px 44px rgba(3, 7, 23, 0.45);
}

/* Dark mode hero card */
.kids-context--dark .zone-hero {
  background:
    radial-gradient(circle at 14% 16%, rgba(255, 176, 32, 0.12), transparent 26%),
    radial-gradient(circle at 88% 18%, rgba(155, 114, 255, 0.12), transparent 30%),
    linear-gradient(135deg, rgba(22, 26, 48, 0.95), rgba(14, 18, 36, 0.92));
  border-color: var(--border);
  box-shadow: var(--card-shadow);
}

/* Dark mode headings */
.kids-context--dark .zone-hero h1,
.kids-context--dark .zone-panel-head h2 {
  color: var(--ink);
}

/* Dark mode kicker text */
.kids-context--dark .zone-kicker {
  color: #c4b5fd;
}

/* Dark mode hero side label */
.kids-context--dark .zone-hero-side span {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
  border-color: var(--border);
  color: var(--muted);
  box-shadow: none;
}

/* Dark mode hero side tag */
.kids-context--dark .zone-hero-side strong {
  background: linear-gradient(135deg, rgba(255, 176, 32, 0.16), rgba(255, 126, 179, 0.1));
  border-color: var(--border);
  color: var(--ink);
  box-shadow: none;
}

/* Dark mode inactive game tabs */
.kids-context--dark .zone-tab:not(.active) {
  border-color: rgba(143, 154, 227, 0.22);
  background: linear-gradient(135deg, rgba(22, 26, 48, 0.88), rgba(14, 18, 36, 0.85));
  color: var(--ink);
  box-shadow: var(--card-shadow);
}

/* Dark mode inactive tab subtext */
.kids-context--dark .zone-tab:not(.active) .zone-tab-copy small {
  color: var(--muted);
  opacity: 1;
}

/* Dark mode tab icon */
.kids-context--dark .zone-tab-icon {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.05));
  box-shadow: 0 8px 18px rgba(3, 7, 23, 0.35);
}

/* Dark mode game panel */
.kids-context--dark .zone-panel {
  background:
    radial-gradient(circle at 90% 10%, rgba(255, 176, 32, 0.1), transparent 22%),
    radial-gradient(circle at 8% 16%, rgba(59, 158, 255, 0.08), transparent 18%),
    linear-gradient(180deg, rgba(18, 22, 43, 0.94), rgba(12, 16, 34, 0.92));
  border-color: var(--border);
  box-shadow: var(--card-shadow);
}

/* Dark mode info modal backdrop */
.kids-context--dark .info-modal-backdrop {
  background: rgba(3, 7, 23, 0.62);
}

/* Dark mode info modal */
.kids-context--dark .info-modal {
  background:
    radial-gradient(circle at 100% 0%, rgba(155, 114, 255, 0.12), transparent 30%),
    radial-gradient(circle at 0% 100%, rgba(255, 176, 32, 0.1), transparent 26%),
    rgba(18, 22, 43, 0.97);
  border-color: var(--border);
  color: var(--ink);
}

/* Dark mode info modal text */
.kids-context--dark .info-lead,
.kids-context--dark .info-list {
  color: var(--ink2);
}

/* Dark mode info buttons */
.kids-context--dark .info-btn,
.kids-context--dark .info-close {
  border-color: rgba(143, 154, 227, 0.35);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  color: #e0e7ff;
  box-shadow: var(--card-shadow);
}

/* Main page content width */
.zone-shell {
  position: relative;
  z-index: 1;
  width: min(1180px, calc(100% - 28px));
  margin: 0 auto;
  padding-bottom: 150px;
}

/* Hero container */
.zone-hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 24px;
  border-radius: 30px;
  background:
    radial-gradient(circle at 14% 16%, rgba(255, 176, 32, 0.22), transparent 26%),
    radial-gradient(circle at 88% 18%, rgba(155, 114, 255, 0.18), transparent 30%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(247, 246, 255, 0.96));
  border: 1.5px solid var(--border);
  box-shadow: var(--card-shadow);
  animation: headerDrop 0.7s cubic-bezier(0.22, 1, 0.36, 1) both, floatCard 5.8s ease-in-out infinite 0.8s;
  position: relative;
  overflow: hidden;
}

/* Hero text stack */
.zone-hero-copy {
  display: grid;
  gap: 12px;
  min-width: 0;
}

/* Hero title and info button row */
.zone-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* Animated rainbow strip at the bottom of the hero */
.zone-hero::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--coral), var(--amber), var(--mint), var(--sky), var(--violet), var(--rose));
  background-size: 400% 100%;
  animation: gradientWave 4s linear infinite;
}

/* Decorative hero glow blob */
.zone-hero::before {
  content: "";
  position: absolute;
  width: 180px;
  height: 180px;
  right: -40px;
  top: -36px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(59, 158, 255, 0.24), rgba(59, 158, 255, 0));
  animation: blobDrift 7s ease-in-out infinite;
}

/* Hero entrance animation */
@keyframes headerDrop {
  from { transform: translateY(-40px) scale(0.97); opacity: 0; }
  to { transform: translateY(0) scale(1); opacity: 1; }
}

/* Rainbow strip animation */
@keyframes gradientWave {
  0% { background-position: 0%; }
  100% { background-position: 400%; }
}

/* Decorative blob movement */
@keyframes blobDrift {
  0%, 100% { transform: translate3d(0, 0, 0) scale(1); }
  50% { transform: translate3d(-18px, 12px, 0) scale(1.08); }
}

/* Gentle floating animation for cards */
@keyframes floatCard {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

/* Glow animation for hero chips */
@keyframes pillGlow {
  0%, 100% { box-shadow: var(--card-shadow); }
  50% { box-shadow: 0 14px 28px rgba(122, 111, 255, 0.18); }
}

/* Pulse animation for info button */
@keyframes pulseRing {
  0%, 100% { transform: scale(1); box-shadow: var(--card-shadow); }
  50% { transform: scale(1.08); box-shadow: 0 14px 28px rgba(255, 126, 179, 0.24); }
}

/* Small uppercase section label */
.zone-kicker {
  margin: 0;
  color: var(--violet);
  font-size: 0.68rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

/* Larger gradient hero kicker */
.zone-hero-copy .zone-kicker {
  font-size: clamp(1rem, 1.6vw, 1.25rem);
  letter-spacing: 0.16em;
  background: linear-gradient(135deg, #ff9a3e, #ff5fa2 55%, #6f6dff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 6px 18px rgba(111, 109, 255, 0.18);
}

/* Hero and panel headings */
.zone-hero h1,
.zone-panel-head h2 {
  margin: 10px 0 0;
  font-size: clamp(1.72rem, 2.7vw, 2.2rem);
  line-height: 1.02;
  font-family: "Baloo 2", cursive;
}

/* Hero chips wrapper */
.zone-hero-side {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

/* Shared hero chip styling */
.zone-hero-side span,
.zone-hero-side strong {
  border-radius: 18px;
  padding: 11px 14px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(246, 241, 255, 0.96));
  border: 1.5px solid var(--border);
  box-shadow: var(--card-shadow);
  animation: pillGlow 4s ease-in-out infinite;
  font-size: 0.84rem;
}

/* Hero short description chip */
.zone-hero-side span {
  background: linear-gradient(135deg, rgba(241, 248, 255, 0.96), rgba(236, 245, 255, 0.94));
  color: var(--muted);
  font-weight: 700;
}

/* Hero tag chip */
.zone-hero-side strong {
  background: linear-gradient(135deg, rgba(255, 249, 239, 0.96), rgba(255, 243, 233, 0.94));
  color: var(--ink);
}

/* Game tab grid */
.zone-tabs {
  margin-top: 18px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

/* Game tab button */
.zone-tab {
  border: 2px solid rgba(24, 25, 43, 0.12);
  border-radius: 24px;
  min-height: 88px;
  padding: 14px 16px;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(246, 245, 255, 0.92));
  display: flex;
  align-items: center;
  gap: 14px;
  text-align: left;
  cursor: pointer;
  box-shadow: var(--card-shadow);
  transition: transform 0.24s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.24s ease, border-color 0.24s ease;
}

/* Game tab hover state */
.zone-tab:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: var(--card-shadow-hover);
}

/* Active game tab */
.zone-tab.active {
  background: linear-gradient(135deg, #63b3ff, #7f88ff, #9b8cff);
  color: #fff;
  border-color: transparent;
  animation: floatCard 4.2s ease-in-out infinite;
  box-shadow: 0 18px 36px rgba(123, 101, 255, 0.24);
}

/* Game tab icon box */
.zone-tab-icon {
  width: 68px;
  height: 68px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #ffffff, #eaf0ff);
  font-size: 2rem;
  flex: 0 0 auto;
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 12px 22px rgba(41, 62, 121, 0.16);
}

/* Active tab icon style */
.zone-tab.active .zone-tab-icon {
  background: rgba(255, 255, 255, 0.16);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.22);
}

/* Icon hover movement */
.zone-tab:hover .zone-tab-icon {
  transform: rotate(-8deg) scale(1.12);
}

/* Game tab text stack */
.zone-tab-copy {
  display: grid;
  gap: 4px;
}

/* Game tab title */
.zone-tab-copy strong {
  font-size: 0.92rem;
  font-family: "Baloo 2", cursive;
}

/* Game tab description */
.zone-tab-copy small {
  color: inherit;
  opacity: 0.84;
  line-height: 1.4;
  font-size: 0.74rem;
}

/* Main game panel */
.zone-panel {
  margin-top: 18px;
  border-radius: 30px;
  padding: 20px;
  background:
    radial-gradient(circle at 90% 10%, rgba(255, 176, 32, 0.14), transparent 22%),
    radial-gradient(circle at 8% 16%, rgba(59, 158, 255, 0.08), transparent 18%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.97), rgba(246, 247, 255, 0.95));
  border: 1.5px solid var(--border);
  box-shadow: var(--card-shadow);
  position: relative;
  overflow: hidden;
}

/* Decorative glow in the game panel */
.zone-panel::after {
  content: "";
  position: absolute;
  inset: auto -20% -55% auto;
  width: 280px;
  height: 280px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(155, 114, 255, 0.2), rgba(155, 114, 255, 0));
  animation: blobDrift 8s ease-in-out infinite reverse;
}

/* Panel heading row */
.zone-panel-title-row {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 10px;
}

/* Active game component wrapper */
.game-shell {
  margin-top: 16px;
}

/* Shared info buttons */
.info-btn,
.info-close {
  width: 48px;
  height: 48px;
  border-radius: 999px;
  border: 1.5px solid rgba(107, 45, 255, 0.18);
  background: linear-gradient(135deg, rgba(243, 240, 255, 0.98), rgba(232, 242, 255, 0.96));
  color: #5d57d8;
  font-weight: 900;
  font-size: 1.3rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: var(--card-shadow);
  flex: 0 0 auto;
  animation: pulseRing 3.2s ease-in-out infinite;
}

/* Full-screen info modal backdrop */
.info-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 20;
  display: grid;
  place-items: center;
  padding: 20px;
  background: rgba(24, 25, 43, 0.28);
  backdrop-filter: blur(10px);
}

/* Info modal card */
.info-modal {
  width: min(560px, 100%);
  border-radius: 28px;
  padding: 22px;
  background:
    radial-gradient(circle at 100% 0%, rgba(155, 114, 255, 0.16), transparent 30%),
    radial-gradient(circle at 0% 100%, rgba(255, 176, 32, 0.16), transparent 26%),
    rgba(255, 255, 255, 0.98);
  border: 1.5px solid var(--border);
  box-shadow: var(--card-shadow-hover);
  animation: headerDrop 0.28s ease-out, floatCard 5.2s ease-in-out infinite 0.4s;
}

/* Info modal header */
.info-modal-head {
  display: flex;
  align-items: start;
  justify-content: space-between;
  gap: 12px;
}

/* Info modal title */
.info-modal h3 {
  margin: 8px 0 0;
  font-family: "Baloo 2", cursive;
  font-size: 1.45rem;
  color: var(--ink);
}

/* Info modal description */
.info-lead {
  margin-top: 14px;
  color: var(--ink2);
  line-height: 1.6;
  font-size: 0.92rem;
}

/* Info modal instruction list */
.info-list {
  margin: 16px 0 0;
  padding-left: 18px;
  color: var(--ink2);
  display: grid;
  gap: 10px;
}

/* Info list marker colour */
.info-list li::marker {
  color: var(--coral);
}

/* Tablet layout */
@media (max-width: 880px) {
  .zone-hero,
  .zone-tabs {
    display: grid;
    grid-template-columns: 1fr;
  }
}

/* Small-screen header layout */
@media (max-width: 640px) {
  .zone-header {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>