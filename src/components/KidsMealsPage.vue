<template>
  <KidsRouteShell page-label="Meals">
    <div class="kids-subpage meals-page" :class="{ 'kids-context--dark': isDarkMode }">
      <div class="page-shell">
      <header class="hero-nutrition">
        <div class="hero-nutrition__plate" aria-hidden="true">
          <span class="ring ring--a"></span>
          <span class="ring ring--b"></span>
          <span class="plate-dot" style="--d: -12deg">🍳</span>
          <span class="plate-dot" style="--d: 78deg">🥝</span>
          <span class="plate-dot" style="--d: 168deg">🥛</span>
          <span class="plate-dot" style="--d: 258deg">🍇</span>
        </div>
        <div class="hero-nutrition__copy">
          <p class="hero-nibble">Fuel zone</p>
          <h1>Your day in bites</h1>
          <p class="hero-one-liner">Tap gray cards to check off today’s meals · tap rainbow bites too.</p>
          <p class="hero-progress-meter" aria-live="polite">
            <span class="meter-chip">Rainbow ring {{ kp.rainbowRingPct }}</span>
            <span class="meter-chip">Meals {{ kp.mealsCompleteCount }}/4</span>
          </p>
        </div>
      </header>

      <section class="meal-bento">
        <article
          v-for="meal in meals"
          :key="meal.label"
          tabindex="0"
          role="button"
          class="meal-tile"
          :class="[meal.tone, { 'meal-tile--done': kp.daily.meals[meal.label] }]"
          @click="kp.toggleMeal(meal.label)"
          @keyup.enter.prevent="kp.toggleMeal(meal.label)"
          @keyup.space.prevent="kp.toggleMeal(meal.label)"
        >
          <header class="meal-tile__head">
            <span class="meal-tile__emoji">{{ meal.emoji }}</span>
            <div>
              <span class="meal-tile__label">{{ meal.label }}</span>
              <h2>{{ meal.title }}</h2>
              <span class="meal-tile__time">{{ meal.time }}</span>
            </div>
          </header>
          <div class="meal-tile__chips">
            <span v-for="item in meal.items" :key="item">{{ item }}</span>
          </div>
          <span class="meal-tap-hint">{{ kp.daily.meals[meal.label] ? 'Nice! Tap to undo.' : 'Tap when you ate it' }}</span>
          <p class="sr-only">{{ meal.description }}</p>
        </article>
      </section>

      <section class="rainbow-dock">
        <h2 class="rainbow-dock__title">Rainbow check</h2>
        <ul class="rainbow-dock__list" role="list">
          <li v-for="goal in goals" :key="goal.id" role="presentation" class="rainbow-slot-wrap">
            <button
              type="button"
              class="rainbow-slot"
              :class="{ 'rainbow-slot--done': kp.daily.rainbow[goal.id] }"
              @click="kp.toggleRainbow(goal.id)"
            >
              <span class="rainbow-slot__check" aria-hidden="true">{{ kp.daily.rainbow[goal.id] ? '✓' : '' }}</span>
              <span class="rainbow-slot__icon" aria-hidden="true">{{ goal.icon }}</span>
              <span class="rainbow-slot__text">{{ goal.title }}</span>
            </button>
          </li>
        </ul>
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

onMounted(() => {
  kp.hydrate()
})

const meals = [
  {
    label: "Breakfast",
    title: "Sunshine starter",
    emoji: "☀️",
    description: "Bright start — fruit, grains, creamy bite.",
    items: ["Banana oats", "Berry yogurt", "Water sip"],

    time: "7:30 AM",
    tone: "tone-sun",
  },
  {
    label: "Lunch",
    title: "Superhero lunch box",
    emoji: "🦸",
    description: "Crunchy, colorful lunchbox-style plate.",
    items: ["Turkey wrap", "Carrot sticks", "Apple slices"],
    time: "12:15 PM",
    tone: "tone-sky",
  },
  {
    label: "Snack",
    title: "After-school boost",
    emoji: "⚡",
    description: "Playful snack for steady energy.",
    items: ["Cheese cubes", "Strawberries", "Crackers"],
    time: "3:30 PM",
    tone: "tone-mint",
  },
  {
    label: "Dinner",
    title: "Rainbow plate finish",
    emoji: "🌈",
    description: "Warm balanced dinner plate.",
    items: ["Chicken rice", "Broccoli trees", "Corn stars"],
    time: "6:30 PM",
    tone: "tone-violet",
  },
]

const goals = [
  { id: "red", icon: "🍎", title: "Something red" },
  { id: "crunch", icon: "🥒", title: "A crunch" },
  { id: "protein", icon: "🥚", title: "Protein power" },
  { id: "water", icon: "💧", title: "Extra water" },
]
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=DM+Sans:wght@400;500;700&display=swap");

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.kids-subpage.meals-page {
  padding: 0 0 8px;
  color: var(--kids-ink);
}

.page-shell {
  width: 100%;
  margin: 0 auto;
  display: grid;
  gap: 22px;
}

.hero-nutrition {
  position: relative;
  overflow: hidden;
  padding: clamp(22px, 5vw, 30px);
  border-radius: 32px;
  background:
    radial-gradient(120% 80% at 10% -20%, rgba(255, 180, 120, 0.35), transparent 50%),
    radial-gradient(70% 60% at 100% 60%, rgba(120, 200, 255, 0.22), transparent 45%),
    var(--kids-surface);
  border: 1px solid var(--kids-border);
  box-shadow: var(--kids-card-shadow);
  display: grid;
  grid-template-columns: minmax(140px, 200px) minmax(0, 1fr);
  gap: 20px;
  align-items: center;
}

.hero-nutrition__plate {
  position: relative;
  width: clamp(148px, 38vw, 200px);
  aspect-ratio: 1;
  margin: 0 auto;
}

.ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px dashed rgba(68, 80, 102, 0.12);
}

.ring--b {
  inset: 12%;
  border-style: solid;
  border-color: rgba(255, 140, 66, 0.28);
}

.plate-dot {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 2.55rem;
  height: 2.55rem;
  margin: -1.27rem;
  display: grid;
  place-items: center;
  font-size: 1.45rem;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 10px 24px rgba(24, 25, 43, 0.1);
  transform: rotate(var(--d)) translateY(-58%) rotate(calc(-1 * var(--d)));
}

.hero-nibble {
  margin: 0 0 6px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 0.69rem;
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #c05621;
  background: rgba(255, 237, 213, 0.95);
  border: 1px solid rgba(251, 146, 60, 0.35);
}

.hero-nutrition__copy h1 {
  margin: 0 0 8px;
  font-family: "Baloo 2", cursive;
  font-size: clamp(2rem, 5vw, 2.85rem);
  line-height: 1.02;
  color: var(--kids-ink);
}

.hero-one-liner {
  margin: 0;
  font-size: 0.95rem;
  color: var(--kids-muted);
  font-weight: 500;
}

.hero-progress-meter {
  margin: 14px 0 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.meter-chip {
  display: inline-flex;
  align-items: center;
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 0.73rem;
  font-weight: 800;
  color: var(--kids-ink);
  background: rgba(68, 80, 102, 0.08);
  border: 1px solid rgba(68, 80, 102, 0.1);
}

.meal-bento {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

article.meal-tile {
  display: block;
  width: 100%;
  padding: 18px;
  border-radius: 26px;
  border: 1px solid var(--kids-border);
  box-shadow: var(--kids-card-shadow);
  transition: transform 0.22s ease, box-shadow 0.22s ease;
  cursor: pointer;
  font: inherit;
  color: inherit;
  text-align: inherit;
}

.meal-tile:hover {
  transform: translateY(-3px);
  box-shadow: 0 20px 40px rgba(24, 25, 43, 0.14);
}

.meal-tile:focus-visible {
  outline: 2px solid rgba(59, 158, 255, 0.7);
  outline-offset: 2px;
}

.meal-tile--done {
  box-shadow:
    inset 0 0 0 2px rgba(44, 201, 122, 0.45),
    var(--kids-card-shadow);
}

.meal-tap-hint {
  display: block;
  margin-top: 11px;
  font-size: 0.71rem;
  font-weight: 700;
  color: var(--kids-soft);
}

.meal-tile__head {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.meal-tile__emoji {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  font-size: 1.55rem;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.7);
}

.meal-tile__label {
  font-size: 0.63rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--kids-soft);
}

.meal-tile__head h2 {
  margin: 4px 0 6px;
  font-family: "Baloo 2", cursive;
  font-size: 1.2rem;
  line-height: 1.1;
  color: var(--kids-ink);
}

.meal-tile__time {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--kids-muted);
  font-variant-numeric: tabular-nums;
}

.meal-tile__chips {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.meal-tile__chips span {
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 0.73rem;
  font-weight: 700;
  background: rgba(68, 80, 102, 0.09);
  color: var(--kids-ink);
}

.tone-sun { background: linear-gradient(155deg, #fff7ed, rgba(255, 255, 255, 0.93)); }
.tone-sky { background: linear-gradient(155deg, #eff6ff, rgba(255, 255, 255, 0.93)); }
.tone-mint { background: linear-gradient(155deg, #ecfdf5, rgba(255, 255, 255, 0.93)); }
.tone-violet { background: linear-gradient(155deg, #f5f3ff, rgba(255, 255, 255, 0.93)); }

.rainbow-dock {
  padding: 18px;
  border-radius: 26px;
  background: var(--kids-surface);
  border: 1px solid var(--kids-border);
  box-shadow: var(--kids-card-shadow);
}

.rainbow-dock__title {
  margin: 0 0 14px;
  font-family: "Baloo 2", cursive;
  font-size: 1.15rem;
  color: var(--kids-ink);
}

.rainbow-dock__list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.rainbow-slot-wrap {
  margin: 0;
  padding: 0;
}

.rainbow-slot {
  width: 100%;
  margin: 0;
  padding: 12px 8px;
  border: none;
  border-radius: 18px;
  background: rgba(68, 80, 102, 0.07);
  color: inherit;
  font: inherit;
  cursor: pointer;
  text-align: center;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  position: relative;
}

.rainbow-slot:hover {
  transform: scale(1.02);
}

.rainbow-slot:focus-visible {
  outline: 2px solid rgba(59, 158, 255, 0.75);
  outline-offset: 2px;
}

.rainbow-slot--done {
  background: rgba(44, 201, 122, 0.16);
  box-shadow: inset 0 0 0 2px rgba(44, 201, 122, 0.35);
}

.rainbow-slot__check {
  position: absolute;
  top: 6px;
  right: 8px;
  font-size: 0.78rem;
  font-weight: 900;
  color: #16925a;
}

.kids-context--dark .rainbow-slot__check {
  color: #6ee7b7;
}

.rainbow-slot__icon {
  font-size: 1.55rem;
  line-height: 1;
}

.rainbow-slot__text {
  font-size: 0.71rem;
  font-weight: 700;
  color: var(--kids-ink);
  line-height: 1.25;
}

/* Dark */
.kids-context--dark .hero-nutrition {
  background:
    radial-gradient(120% 80% at 10% -20%, rgba(255, 140, 80, 0.12), transparent 50%),
    radial-gradient(70% 60% at 100% 55%, rgba(99, 155, 255, 0.14), transparent 45%),
    var(--kids-surface);
}

.kids-context--dark .plate-dot {
  background: rgba(24, 30, 55, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.kids-context--dark .meal-tile__emoji {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.08);
}

.kids-context--dark .meal-tile__chips span {
  background: rgba(255, 255, 255, 0.07);
}

.kids-context--dark .tone-sun { background: linear-gradient(155deg, rgba(255, 167, 80, 0.15), rgba(18, 22, 43, 0.95)); }
.kids-context--dark .tone-sky { background: linear-gradient(155deg, rgba(120, 186, 255, 0.14), rgba(18, 22, 43, 0.95)); }
.kids-context--dark .tone-mint { background: linear-gradient(155deg, rgba(70, 220, 160, 0.12), rgba(18, 22, 43, 0.95)); }
.kids-context--dark .tone-violet { background: linear-gradient(155deg, rgba(180, 150, 255, 0.14), rgba(18, 22, 43, 0.95)); }

.kids-context--dark .rainbow-slot {
  background: rgba(255, 255, 255, 0.06);
}

.kids-context--dark .rainbow-slot--done {
  background: rgba(44, 201, 122, 0.12);
  box-shadow: inset 0 0 0 2px rgba(74, 222, 128, 0.32);
}

.kids-context--dark .hero-nibble {
  color: #fed7aa;
  background: rgba(251, 146, 60, 0.16);
  border-color: rgba(251, 146, 60, 0.3);
}

@media (max-width: 720px) {
  .hero-nutrition {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-nibble {
    margin-left: auto;
    margin-right: auto;
  }

  .meal-bento {
    grid-template-columns: 1fr;
  }

  .rainbow-dock__list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
