<!--
  KidsMealsPage.vue

  Creates the HealthyKids kids meals page. Children can check off meals,
  complete rainbow food goals, and update meal progress through playful taps.

  Store requirement:
  - Uses useKidsProgressStore for meal completion, rainbow goals, and progress values.
  - Calls kp.hydrate() when the page loads to restore saved kids progress.

  Accessibility:
  - Uses keyboard-friendly meal cards with tabindex, Enter, and Space support.
  - Uses aria-live for the meal and rainbow progress meter.
  - Uses aria-hidden for decorative plate visuals and icons where appropriate.
  - Includes screen-reader-only meal descriptions.
-->

<template>
  <KidsRouteShell page-label="Meals">
    <div class="kids-subpage meals-page" :class="{ 'kids-context--dark': isDarkMode }">
      <div class="page-shell">
      <!-- Hero section with animated plate and progress summary -->
      <header class="hero-nutrition">
        <!-- Decorative food plate visual -->
        <div class="hero-nutrition__plate" aria-hidden="true">
          <span class="ring ring--a"></span>
          <span class="ring ring--b"></span>
          <span class="plate-dot" style="--d: -12deg">🍳</span>
          <span class="plate-dot" style="--d: 78deg">🥝</span>
          <span class="plate-dot" style="--d: 168deg">🥛</span>
          <span class="plate-dot" style="--d: 258deg">🍇</span>
        </div>

        <!-- Hero copy and live progress meter -->
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

      <!-- Meal checklist cards -->
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
          <!-- Meal card heading -->
          <header class="meal-tile__head">
            <span class="meal-tile__emoji">{{ meal.emoji }}</span>
            <div>
              <span class="meal-tile__label">{{ meal.label }}</span>
              <h2>{{ meal.title }}</h2>
              <span class="meal-tile__time">{{ meal.time }}</span>
            </div>
          </header>

          <!-- Suggested meal items -->
          <div class="meal-tile__chips">
            <span v-for="item in meal.items" :key="item">{{ item }}</span>
          </div>

          <!-- Tap instruction changes when the meal is complete -->
          <span class="meal-tap-hint">{{ kp.daily.meals[meal.label] ? 'Nice! Tap to undo.' : 'Tap when you ate it' }}</span>

          <!-- Screen-reader-only meal description -->
          <p class="sr-only">{{ meal.description }}</p>
        </article>
      </section>

      <!-- Rainbow food goal checklist -->
      <section class="rainbow-dock">
        <h2 class="rainbow-dock__title">Rainbow check</h2>

        <!-- Rainbow goal buttons -->
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

// Reads the current kids theme so the page can switch between light and dark styles.
const { isDarkMode } = injectKidsTheme()

// Kids progress store containing meal, rainbow, and progress actions.
const kp = useKidsProgressStore()

// Restores saved kids progress when the page loads.
onMounted(() => {
  kp.hydrate()
})

// Meal card data shown in the meal checklist.
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

// Rainbow food goals shown in the rainbow checklist.
const goals = [
  { id: "red", icon: "🍎", title: "Something red" },
  { id: "crunch", icon: "🥒", title: "A crunch" },
  { id: "protein", icon: "🥚", title: "Protein power" },
  { id: "water", icon: "💧", title: "Extra water" },
]
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=DM+Sans:wght@400;500;700&display=swap");

/* Visually hides text while keeping it available to screen readers */
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

/* Main meals page wrapper */
.kids-subpage.meals-page {
  padding: 0 0 8px;
  color: var(--kids-ink);
}

/* Page layout container */
.page-shell {
  width: 100%;
  margin: 0 auto;
  display: grid;
  gap: 22px;
}

/* Hero nutrition card */
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

/* Decorative plate wrapper */
.hero-nutrition__plate {
  position: relative;
  width: clamp(148px, 38vw, 200px);
  aspect-ratio: 1;
  margin: 0 auto;
}

/* Decorative plate rings */
.ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 2px dashed rgba(68, 80, 102, 0.12);
}

/* Inner plate ring */
.ring--b {
  inset: 12%;
  border-style: solid;
  border-color: rgba(255, 140, 66, 0.28);
}

/* Floating food dots around the plate */
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

/* Small hero label */
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

/* Hero heading */
.hero-nutrition__copy h1 {
  margin: 0 0 8px;
  font-family: "Baloo 2", cursive;
  font-size: clamp(2rem, 5vw, 2.85rem);
  line-height: 1.02;
  color: var(--kids-ink);
}

/* Hero subtitle */
.hero-one-liner {
  margin: 0;
  font-size: 0.95rem;
  color: var(--kids-muted);
  font-weight: 500;
}

/* Progress meter chip row */
.hero-progress-meter {
  margin: 14px 0 0;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

/* Progress meter chip */
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

/* Meal card grid */
.meal-bento {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

/* Individual meal tile */
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

/* Meal hover effect */
.meal-tile:hover {
  transform: translateY(-3px);
  box-shadow: 0 20px 40px rgba(24, 25, 43, 0.14);
}

/* Keyboard focus style for meal tiles */
.meal-tile:focus-visible {
  outline: 2px solid rgba(59, 158, 255, 0.7);
  outline-offset: 2px;
}

/* Completed meal tile state */
.meal-tile--done {
  box-shadow:
    inset 0 0 0 2px rgba(44, 201, 122, 0.45),
    var(--kids-card-shadow);
}

/* Meal tap hint */
.meal-tap-hint {
  display: block;
  margin-top: 11px;
  font-size: 0.71rem;
  font-weight: 700;
  color: var(--kids-soft);
}

/* Meal tile heading row */
.meal-tile__head {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

/* Meal emoji box */
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

/* Meal label */
.meal-tile__label {
  font-size: 0.63rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--kids-soft);
}

/* Meal title */
.meal-tile__head h2 {
  margin: 4px 0 6px;
  font-family: "Baloo 2", cursive;
  font-size: 1.2rem;
  line-height: 1.1;
  color: var(--kids-ink);
}

/* Meal time label */
.meal-tile__time {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--kids-muted);
  font-variant-numeric: tabular-nums;
}

/* Meal item chips row */
.meal-tile__chips {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* Meal item chip */
.meal-tile__chips span {
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 0.73rem;
  font-weight: 700;
  background: rgba(68, 80, 102, 0.09);
  color: var(--kids-ink);
}

/* Breakfast card tone */
.tone-sun { background: linear-gradient(155deg, #fff7ed, rgba(255, 255, 255, 0.93)); }

/* Lunch card tone */
.tone-sky { background: linear-gradient(155deg, #eff6ff, rgba(255, 255, 255, 0.93)); }

/* Snack card tone */
.tone-mint { background: linear-gradient(155deg, #ecfdf5, rgba(255, 255, 255, 0.93)); }

/* Dinner card tone */
.tone-violet { background: linear-gradient(155deg, #f5f3ff, rgba(255, 255, 255, 0.93)); }

/* Rainbow checklist card */
.rainbow-dock {
  padding: 18px;
  border-radius: 26px;
  background: var(--kids-surface);
  border: 1px solid var(--kids-border);
  box-shadow: var(--kids-card-shadow);
}

/* Rainbow checklist title */
.rainbow-dock__title {
  margin: 0 0 14px;
  font-family: "Baloo 2", cursive;
  font-size: 1.15rem;
  color: var(--kids-ink);
}

/* Rainbow goal grid */
.rainbow-dock__list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

/* Rainbow goal list wrapper */
.rainbow-slot-wrap {
  margin: 0;
  padding: 0;
}

/* Rainbow goal button */
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

/* Rainbow goal hover effect */
.rainbow-slot:hover {
  transform: scale(1.02);
}

/* Keyboard focus style for rainbow goals */
.rainbow-slot:focus-visible {
  outline: 2px solid rgba(59, 158, 255, 0.75);
  outline-offset: 2px;
}

/* Completed rainbow goal state */
.rainbow-slot--done {
  background: rgba(44, 201, 122, 0.16);
  box-shadow: inset 0 0 0 2px rgba(44, 201, 122, 0.35);
}

/* Rainbow goal checkmark */
.rainbow-slot__check {
  position: absolute;
  top: 6px;
  right: 8px;
  font-size: 0.78rem;
  font-weight: 900;
  color: #16925a;
}

/* Dark mode rainbow goal checkmark */
.kids-context--dark .rainbow-slot__check {
  color: #6ee7b7;
}

/* Rainbow goal icon */
.rainbow-slot__icon {
  font-size: 1.55rem;
  line-height: 1;
}

/* Rainbow goal text */
.rainbow-slot__text {
  font-size: 0.71rem;
  font-weight: 700;
  color: var(--kids-ink);
  line-height: 1.25;
}

/* Dark mode hero nutrition card */
.kids-context--dark .hero-nutrition {
  background:
    radial-gradient(120% 80% at 10% -20%, rgba(255, 140, 80, 0.12), transparent 50%),
    radial-gradient(70% 60% at 100% 55%, rgba(99, 155, 255, 0.14), transparent 45%),
    var(--kids-surface);
}

/* Dark mode plate food dots */
.kids-context--dark .plate-dot {
  background: rgba(24, 30, 55, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

/* Dark mode meal emoji box */
.kids-context--dark .meal-tile__emoji {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.08);
}

/* Dark mode meal item chips */
.kids-context--dark .meal-tile__chips span {
  background: rgba(255, 255, 255, 0.07);
}

/* Dark mode breakfast card tone */
.kids-context--dark .tone-sun { background: linear-gradient(155deg, rgba(255, 167, 80, 0.15), rgba(18, 22, 43, 0.95)); }

/* Dark mode lunch card tone */
.kids-context--dark .tone-sky { background: linear-gradient(155deg, rgba(120, 186, 255, 0.14), rgba(18, 22, 43, 0.95)); }

/* Dark mode snack card tone */
.kids-context--dark .tone-mint { background: linear-gradient(155deg, rgba(70, 220, 160, 0.12), rgba(18, 22, 43, 0.95)); }

/* Dark mode dinner card tone */
.kids-context--dark .tone-violet { background: linear-gradient(155deg, rgba(180, 150, 255, 0.14), rgba(18, 22, 43, 0.95)); }

/* Dark mode rainbow goal button */
.kids-context--dark .rainbow-slot {
  background: rgba(255, 255, 255, 0.06);
}

/* Dark mode completed rainbow goal */
.kids-context--dark .rainbow-slot--done {
  background: rgba(44, 201, 122, 0.12);
  box-shadow: inset 0 0 0 2px rgba(74, 222, 128, 0.32);
}

/* Dark mode fuel zone label */
.kids-context--dark .hero-nibble {
  color: #fed7aa;
  background: rgba(251, 146, 60, 0.16);
  border-color: rgba(251, 146, 60, 0.3);
}

/* Responsive layout for smaller screens */
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