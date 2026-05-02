<template>
  <div class="nutrition-page">
    <header class="header">
      <div class="header-inner">
        <RouterLink to="/" class="logo">
          <div class="logo-icon">
            <svg viewBox="0 0 36 36" fill="none">
              <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2" />
              <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor" />
              <path
                d="M18 13C15.5 15.5 15 19 18 23"
                stroke="white"
                stroke-width="1.2"
                stroke-linecap="round"
                fill="none"
                opacity="0.55"
              />
            </svg>
          </div>
          <span class="logo-text">HealthyKids</span>
        </RouterLink>

        <nav class="nav">
          <RouterLink to="/parent-dashboard" class="nav-a">Parent dashboard</RouterLink>
          <RouterLink to="/parent-roadmap" class="nav-a">Roadmap page</RouterLink>
          <RouterLink to="/young-person-dashboard" class="nav-a">Kids dashboard</RouterLink>
        </nav>

        <div class="nav-cta">
          <RouterLink to="/parent-quiz" class="nav-link">Retake quiz</RouterLink>
          <RouterLink to="/parent-dashboard" class="nav-btn">
            Back to dashboard
            <svg width="12" height="12" viewBox="0 0 12 12">
              <path
                d="M2 6h8M7 3l3 3-3 3"
                stroke="currentColor"
                stroke-width="1.3"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </RouterLink>
        </div>
      </div>
    </header>

    <main>
      <section class="hero">
        <div class="section-wrap hero-grid">
          <div>
            <div class="section-eyebrow">Epic 5 · Nutrition support tools</div>
            <h1 class="hero-title">
              Nutrition tools for<br />
              <em>fast parent decisions.</em>
            </h1>
            <details class="text-fold hero-fold">
              <summary>About this page</summary>
              <p class="hero-copy">
                A separate parent-side nutrition hub with meal ideas, snack ideas, and lunchbox food ideas
                organised in one place so you can find useful suggestions quickly and act with less effort.
              </p>
            </details>
            <div class="hero-tags">
              <span class="hero-tag">Meal ideas</span>
              <span class="hero-tag">Snack ideas</span>
              <span class="hero-tag">Lunchbox food ideas</span>
              <span class="hero-tag">{{ personalizedLabel }}</span>
            </div>
            <div class="hero-actions">
              <RouterLink to="/parent-entry" class="hero-action-solid">Parent access</RouterLink>
              <RouterLink to="/parent-quiz" class="hero-action-ghost">Build or refresh plan</RouterLink>
            </div>
          </div>

          <div class="hero-kpis">
            <article class="hero-kpi-card feature">
              <span>Recommended next move</span>
              <strong>{{ featuredSuggestion.title }}</strong>
              <details class="text-fold">
                <summary>Why we suggest this</summary>
                <p class="mini-fold-body">{{ featuredSuggestionReason }}</p>
              </details>
              <button type="button" class="mini-action" @click="applyRecommendedPath">Use recommended path</button>
            </article>
            <article class="hero-kpi-card">
              <span>Meal ideas</span>
              <strong>{{ moduleCounts.meal }}</strong>
              <details class="text-fold">
                <summary>What this covers</summary>
                <p>Structured breakfast, dinner, lunch, and after-school ideas.</p>
              </details>
            </article>
            <article class="hero-kpi-card">
              <span>Snack ideas</span>
              <strong>{{ moduleCounts.snack }}</strong>
              <details class="text-fold">
                <summary>What this covers</summary>
                <p>Quick pairings parents can use straight away for easier snack choices.</p>
              </details>
            </article>
            <article class="hero-kpi-card dark">
              <span>Lunchbox ideas</span>
              <strong>{{ moduleCounts.lunchbox }}</strong>
              <details class="text-fold">
                <summary>What this covers</summary>
                <p class="muted-on-dark">
                  Packable food combinations to make school lunch easier to repeat.
                </p>
              </details>
            </article>
          </div>
        </div>
      </section>

      <section class="purpose-section">
        <div class="section-wrap">
          <div class="purpose-grid">
            <article class="purpose-card dark">
              <span class="purpose-label">Why this page exists</span>
              <h2>{{ pagePurposeTitle }}</h2>
              <details class="text-fold text-fold--invert">
                <summary>More context</summary>
                <p>{{ pagePurposeBody }}</p>
              </details>
            </article>
            <article class="purpose-card">
              <span class="purpose-label">Best for right now</span>
              <h3>{{ recommendedMomentLabel }}</h3>
              <details class="text-fold">
                <summary>Learn more</summary>
                <p>{{ recommendedMomentBody }}</p>
              </details>
            </article>
            <article class="purpose-card">
              <span class="purpose-label">Simple parent rule</span>
              <h3>{{ parentRule.title }}</h3>
              <details class="text-fold">
                <summary>How to use it</summary>
                <p>{{ parentRule.body }}</p>
              </details>
            </article>
          </div>
        </div>
      </section>

      <section class="shortcut-section">
        <div class="section-wrap">
          <div class="section-head">
            <div>
              <div class="section-eyebrow">User Story 5.3</div>
              <h2 class="section-h2">Quick starts with minimal steps.</h2>
            </div>
            <details class="text-fold section-fold">
              <summary>How shortcuts work</summary>
              <p class="section-desc">
                Tap one shortcut to jump straight into the most common nutrition decisions parents face.
              </p>
            </details>
          </div>

          <div class="priority-card">
            <div>
              <div class="priority-label">Suggested starting point</div>
              <div class="priority-title">{{ suggestedShortcut.label }}</div>
              <details class="text-fold">
                <summary>Why start here</summary>
                <p class="priority-copy">{{ suggestedShortcutCopy }}</p>
              </details>
            </div>
            <button type="button" class="priority-btn" @click="applyQuickStart(suggestedShortcut)">
              Use this shortcut
            </button>
          </div>

          <div class="shortcut-grid">
            <article
              v-for="shortcut in nutritionQuickStarts"
              :key="shortcut.id"
              class="shortcut-tile"
            >
              <button type="button" class="shortcut-card" @click="applyQuickStart(shortcut)">
                <span class="shortcut-kicker">Quick start</span>
                <strong>{{ shortcut.label }}</strong>
              </button>
              <details class="text-fold shortcut-tile-more" @click.stop>
                <summary>Filters used</summary>
                <p class="shortcut-tile-more-body">{{ getShortcutDescription(shortcut) }}</p>
              </details>
            </article>
          </div>
        </div>
      </section>

      <section class="tool-section">
        <div class="section-wrap">
          <div class="section-head">
            <div>
              <div class="section-eyebrow">User Story 5.1 + 5.2</div>
              <h2 class="section-h2">One platform, three practical tools.</h2>
            </div>
            <details class="text-fold section-fold">
              <summary>Using filters</summary>
              <p class="section-desc">
                Switch modules or use the quick filters below to find a suggestion without digging through
                unstructured content.
              </p>
            </details>
          </div>

          <div class="module-tabs">
            <button
              v-for="option in moduleOptions"
              :key="option.value"
              type="button"
              class="module-tab"
              :class="{ active: activeModule === option.value }"
              @click="activeModule = option.value"
            >
              {{ option.label }}
            </button>
          </div>

          <div class="filter-panel">
            <div class="filter-group">
              <span class="filter-label">Moment</span>
              <div class="filter-chips">
                <button
                  v-for="option in momentOptions"
                  :key="option.value"
                  type="button"
                  class="filter-chip"
                  :class="{ active: selectedMoment === option.value }"
                  @click="selectedMoment = option.value"
                >
                  {{ option.label }}
                </button>
              </div>
            </div>

            <div class="filter-group">
              <span class="filter-label">Effort</span>
              <div class="filter-chips">
                <button
                  v-for="option in effortOptions"
                  :key="option.value"
                  type="button"
                  class="filter-chip"
                  :class="{ active: selectedEffort === option.value }"
                  @click="selectedEffort = option.value"
                >
                  {{ option.label }}
                </button>
              </div>
            </div>

            <div class="filter-group">
              <span class="filter-label">Need</span>
              <div class="filter-chips">
                <button
                  v-for="option in needOptions"
                  :key="option.value"
                  type="button"
                  class="filter-chip"
                  :class="{ active: selectedNeed === option.value }"
                  @click="selectedNeed = option.value"
                >
                  {{ option.label }}
                </button>
              </div>
            </div>
          </div>

          <div class="result-summary">
            <div>
              <div class="result-count">{{ filteredItems.length }} suggestions</div>
              <p class="result-line">{{ activeSummary }}</p>
            </div>
            <button type="button" class="reset-btn" @click="resetFilters">Reset filters</button>
          </div>

          <div class="active-filter-strip">
            <span class="active-filter-label">Current view</span>
            <div class="active-filter-pills">
              <span class="active-filter-pill">{{ activeModuleLabel }}</span>
              <span v-if="selectedMoment !== 'all'" class="active-filter-pill">{{ getMomentLabel(selectedMoment) }}</span>
              <span v-if="selectedEffort !== 'all'" class="active-filter-pill">{{ getEffortLabel(selectedEffort) }}</span>
              <span v-if="selectedNeed !== 'all'" class="active-filter-pill">{{ getNeedLabel(selectedNeed) }}</span>
              <span
                v-if="selectedMoment === 'all' && selectedEffort === 'all' && selectedNeed === 'all'"
                class="active-filter-pill neutral"
              >
                Broad browse mode
              </span>
            </div>
          </div>

          <div v-if="filteredItems.length === 0" class="empty-results-card">
            <h3>No nutrition suggestions match those filters.</h3>
            <p>Clear one filter and the tool will immediately show more useful options.</p>
            <button type="button" class="hero-action-solid empty-reset" @click="resetFilters">
              Show all suggestions
            </button>
          </div>

          <div v-else class="tool-groups">
            <section v-for="group in groupedItems" :key="group.key" class="tool-group">
              <button type="button" class="dropdown-head" @click="toggleGroup(group.key)">
                <div>
                  <div class="tool-group-kicker">{{ group.kicker }}</div>
                  <h3 class="tool-group-title">{{ group.title }}</h3>
                </div>
                <div class="dropdown-meta">
                  <div class="tool-group-count">{{ group.items.length }} shown · {{ moduleCounts[group.key] }} total</div>
                  <span class="dropdown-arrow" :class="{ open: isGroupOpen(group.key) }">⌄</span>
                </div>
              </button>

              <div v-if="!isGroupOpen(group.key)" class="collapsed-preview">
                <details class="text-fold collapsed-fold">
                  <summary>Peek at titles</summary>
                  <div class="collapsed-copy">
                    Compact preview below — expand the section header to browse everything.
                  </div>
                  <div class="preview-chip-row">
                    <span v-for="item in group.items.slice(0, 6)" :key="item.id" class="preview-chip">
                      {{ item.title }}
                    </span>
                  </div>
                </details>
              </div>

              <div v-else class="tool-card-grid">
                <article
                  v-for="item in group.items"
                  :key="item.id"
                  class="tool-card"
                  :class="['module-' + item.module, { featured: item.id === featuredSuggestion.id }]"
                >
                  <div class="tool-card-top">
                    <span class="tool-card-badge">{{ moduleMap[item.module].label }}</span>
                    <span class="tool-card-time">{{ item.timeLabel || getEffortLabel(item.effort) }}</span>
                  </div>
                  <div v-if="item.id === featuredSuggestion.id" class="featured-ribbon">Best fit right now</div>
                  <h4 class="tool-card-title">{{ item.title }}</h4>

                  <template v-if="item.module === 'meal'">
                    <div class="pill-row">
                      <span v-for="need in item.needs.slice(0, 3)" :key="need" class="mini-pill">
                        {{ getNeedLabel(need) }}
                      </span>
                    </div>
                  </template>

                  <details class="expand-card-fold">
                    <summary>Ingredients, steps &amp; extras</summary>
                    <div class="expand-card-inner">
                      <template v-if="item.module === 'meal'">
                        <p class="tool-card-summary">{{ item.summary }}</p>
                        <div class="detail-block">
                          <div class="detail-label">Use</div>
                          <div class="detail-value">{{ getMomentLabel(item.moment) }}</div>
                        </div>
                        <div class="detail-block">
                          <div class="detail-label">Ingredients</div>
                          <ul class="detail-list">
                            <li v-for="entry in item.items" :key="entry">{{ entry }}</li>
                          </ul>
                        </div>
                        <div class="detail-block">
                          <div class="detail-label">Steps</div>
                          <ol class="detail-list ordered">
                            <li v-for="step in item.steps" :key="step">{{ step }}</li>
                          </ol>
                        </div>
                        <div class="tool-tip">{{ item.benefit }}</div>
                      </template>

                      <template v-else-if="item.module === 'snack'">
                        <div class="swap-grid">
                          <div class="swap-box current">
                            <span>Pair one</span>
                            <strong>{{ item.pairLeft }}</strong>
                          </div>
                          <div class="swap-arrow">+</div>
                          <div class="swap-box better">
                            <span>Pair two</span>
                            <strong>{{ item.pairRight }}</strong>
                          </div>
                        </div>
                        <p v-if="item.reason" class="tool-card-summary">{{ item.reason }}</p>
                        <div class="tool-tip">{{ item.serving }}</div>
                        <div class="parent-move">
                          <span>Parent move</span>
                          <p>{{ item.parentMove }}</p>
                        </div>
                      </template>

                      <template v-else>
                        <div class="lunchbox-stack">
                          <div class="lunch-row">
                            <span>Base</span>
                            <strong>{{ item.base }}</strong>
                          </div>
                          <div class="lunch-row">
                            <span>Fresh</span>
                            <strong>{{ item.fresh }}</strong>
                          </div>
                          <div class="lunch-row">
                            <span>Extra</span>
                            <strong>{{ item.extra }}</strong>
                          </div>
                        </div>
                        <div class="tool-tip">{{ item.packTip }}</div>
                        <div class="parent-move">
                          <span>Parent move</span>
                          <p>{{ item.parentMove }}</p>
                        </div>
                      </template>
                    </div>
                  </details>
                </article>
              </div>
            </section>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'
import { nutritionQuickStarts, nutritionToolItems } from '../data/nutritionToolsData'

const { state } = useFamilyPlanStore()

const moduleOptions = [
  { value: 'all', label: 'All tools' },
  { value: 'meal', label: 'Meal ideas' },
  { value: 'snack', label: 'Snack ideas' },
  { value: 'lunchbox', label: 'Lunchbox ideas' },
]

const momentOptions = [
  { value: 'all', label: 'Any time' },
  { value: 'breakfast', label: 'Breakfast' },
  { value: 'after-school', label: 'After school' },
  { value: 'school-lunch', label: 'School lunch' },
  { value: 'dinner', label: 'Dinner' },
  { value: 'dessert', label: 'Dessert' },
]

const effortOptions = [
  { value: 'all', label: 'Any effort' },
  { value: 'under-5', label: 'Under 5 min' },
  { value: 'under-15', label: 'Under 15 min' },
  { value: 'make-ahead', label: 'Make-ahead' },
]

const needOptions = [
  { value: 'all', label: 'Any need' },
  { value: 'protein', label: 'Protein' },
  { value: 'fruit-veg', label: 'Fruit + veg' },
  { value: 'fussy-friendly', label: 'Fussy-friendly' },
  { value: 'budget', label: 'Budget' },
  { value: 'lunchbox-safe', label: 'Lunchbox-safe' },
]

const moduleMap = {
  meal: { label: 'Meal idea', title: 'Meal ideas', kicker: 'Structured content' },
  snack: { label: 'Snack idea', title: 'Snack ideas', kicker: 'Quick wins' },
  lunchbox: { label: 'Lunchbox idea', title: 'Lunchbox food ideas', kicker: 'Packable support' },
}

const activeModule = ref('all')
const selectedMoment = ref('all')
const selectedEffort = ref('all')
const selectedNeed = ref('all')
const expandedGroups = ref(['meal', 'snack', 'lunchbox'])
const childName = computed(() => state.childName || 'your child')
const concerns = computed(() => state.concerns || [])

const personalizedLabel = computed(() => {
  if (state.concerns?.includes('Nutrition') || state.concerns?.includes('My child snacks too often')) return 'Nutrition focus'
  if (state.childName) return `For ${state.childName}`
  return 'Parent-friendly'
})

const primaryNutritionNeed = computed(() => {
  if (concerns.value.includes('Nutrition') || concerns.value.includes('My child snacks too often')) return 'protein'
  if (concerns.value.includes('Routine battles') || concerns.value.includes('Our family routine feels hard to manage')) return 'lunchbox-safe'
  if (concerns.value.includes('Sleep consistency') || concerns.value.includes('Bedtime feels inconsistent')) return 'budget'
  return 'fussy-friendly'
})

const suggestedShortcut = computed(() => {
  if (concerns.value.includes('Nutrition') || concerns.value.includes('My child snacks too often')) {
    return nutritionQuickStarts.find(item => item.id === 'quick-afterschool') || nutritionQuickStarts[0]
  }
  if (concerns.value.includes('Routine battles') || concerns.value.includes('Our family routine feels hard to manage')) {
    return nutritionQuickStarts.find(item => item.id === 'quick-lunchbox') || nutritionQuickStarts[0]
  }
  return nutritionQuickStarts.find(item => item.id === 'quick-breakfast') || nutritionQuickStarts[0]
})

const suggestedShortcutCopy = computed(() => {
  if (suggestedShortcut.value.id === 'quick-afterschool') {
    return 'This gives you the fastest path to better after-school snack ideas with almost no decision friction.'
  }
  if (suggestedShortcut.value.id === 'quick-lunchbox') {
    return 'This opens packable, repeatable lunchbox support so tomorrow morning takes less thought.'
  }
  return 'This surfaces low-effort breakfast ideas so healthy choices are easy even on rushed mornings.'
})

const moduleCounts = computed(() =>
  nutritionToolItems.reduce((acc, item) => {
    acc[item.module] += 1
    return acc
  }, { meal: 0, snack: 0, lunchbox: 0 })
)

const filteredItems = computed(() =>
  nutritionToolItems.filter((item) => {
    if (activeModule.value !== 'all' && item.module !== activeModule.value) return false
    if (selectedMoment.value !== 'all' && item.moment !== selectedMoment.value) return false
    if (selectedEffort.value !== 'all' && item.effort !== selectedEffort.value) return false
    if (selectedNeed.value !== 'all' && !item.needs.includes(selectedNeed.value)) return false
    return true
  })
)

const featuredSuggestion = computed(() => {
  const preferredNeed = selectedNeed.value !== 'all' ? selectedNeed.value : primaryNutritionNeed.value
  return (
    filteredItems.value.find(item => item.needs.includes(preferredNeed)) ||
    filteredItems.value.find(item => item.module === activeModule.value) ||
    filteredItems.value[0] ||
    nutritionToolItems[0]
  )
})

const featuredSuggestionReason = computed(() => {
  if (selectedNeed.value !== 'all') {
    return `Best match for ${getNeedLabel(selectedNeed.value).toLowerCase()} with minimal extra thinking.`
  }
  if (concerns.value.includes('Nutrition') || concerns.value.includes('My child snacks too often')) {
    return `Chosen to reduce snack friction and make healthy options easier for ${childName.value}.`
  }
  if (concerns.value.includes('Routine battles') || concerns.value.includes('Our family routine feels hard to manage')) {
    return 'Chosen because repeatable food routines usually reduce daily parent effort fastest.'
  }
  return 'Chosen because it is practical, low-friction, and easy to act on today.'
})

const pagePurposeTitle = computed(() => {
  if (concerns.value.includes('Nutrition') || concerns.value.includes('My child snacks too often')) {
    return 'Turn nutrition stress into one easy next choice.'
  }
  if (concerns.value.includes('Routine battles') || concerns.value.includes('Our family routine feels hard to manage')) {
    return 'Make food routines easier to repeat on busy days.'
  }
  return 'Help parents choose quickly without overthinking meals and snacks.'
})

const pagePurposeBody = computed(() => {
  if (state.childName) {
    return `This tool is organised to help you choose the next useful food idea for ${state.childName} in just a few taps, whether the problem is breakfast, snacks, or lunchboxes.`
  }
  return 'This tool keeps meal ideas, snack ideas, and lunchbox support in one place so the next healthy choice feels obvious, not effortful.'
})

const recommendedMomentLabel = computed(() => getMomentLabel(suggestedShortcut.value.moment))

const recommendedMomentBody = computed(() => {
  if (suggestedShortcut.value.moment === 'after-school') {
    return 'After-school eating is often where decision fatigue hits. Start there if you want the biggest day-to-day win.'
  }
  if (suggestedShortcut.value.moment === 'school-lunch') {
    return 'Lunchboxes reward repetition. A few reliable packable formulas can lower stress for the whole week.'
  }
  return 'Breakfast is the fastest place to improve consistency because it repeats every day and can stay very simple.'
})

const parentRule = computed(() => {
  if (activeModule.value === 'snack') {
    return {
      title: 'Pair produce with staying power',
      body: 'For snack ideas, combine one fruit or veg with one filling side so the snack feels complete and lasts longer.',
    }
  }
  if (activeModule.value === 'lunchbox') {
    return {
      title: 'Repeatable beats perfect',
      body: 'Use 2 to 3 lunchbox formulas on rotation so healthy packing is realistic on school mornings.',
    }
  }
  return {
    title: 'Build from one easy win',
    body: 'Choose the smallest meal improvement you can repeat for the next few days before adding complexity.',
  }
})

const activeModuleLabel = computed(() => moduleOptions.find(option => option.value === activeModule.value)?.label || 'All tools')

const groupedItems = computed(() => {
  const order = activeModule.value === 'all' ? ['meal', 'snack', 'lunchbox'] : [activeModule.value]
  return order
    .map((key) => ({
      key,
      title: moduleMap[key].title,
      kicker: moduleMap[key].kicker,
      items: filteredItems.value.filter(item => item.module === key),
    }))
    .filter(group => group.items.length > 0)
})

const activeSummary = computed(() => {
  const parts = []
  if (activeModule.value !== 'all') parts.push(moduleMap[activeModule.value].title.toLowerCase())
  if (selectedMoment.value !== 'all') parts.push(getMomentLabel(selectedMoment.value).toLowerCase())
  if (selectedEffort.value !== 'all') parts.push(getEffortLabel(selectedEffort.value).toLowerCase())
  if (selectedNeed.value !== 'all') parts.push(getNeedLabel(selectedNeed.value).toLowerCase())
  if (!parts.length) return 'Showing all nutrition suggestions across meal ideas, snack ideas, and lunchbox food ideas.'
  return `Filtered for ${parts.join(' + ')}.`
})

function applyQuickStart(shortcut) {
  activeModule.value = shortcut.module
  selectedMoment.value = shortcut.moment
  selectedEffort.value = shortcut.effort
  selectedNeed.value = shortcut.need
}

function applyRecommendedPath() {
  applyQuickStart(suggestedShortcut.value)
}

function toggleGroup(key) {
  if (expandedGroups.value.includes(key)) {
    expandedGroups.value = expandedGroups.value.filter(item => item !== key)
    return
  }
  expandedGroups.value = [...expandedGroups.value, key]
}

function isGroupOpen(key) {
  return expandedGroups.value.includes(key)
}

function resetFilters() {
  activeModule.value = 'all'
  selectedMoment.value = 'all'
  selectedEffort.value = 'all'
  selectedNeed.value = 'all'
}

function getShortcutDescription(shortcut) {
  const detail = []
  if (shortcut.module !== 'all') detail.push(moduleMap[shortcut.module].title)
  if (shortcut.moment !== 'all') detail.push(getMomentLabel(shortcut.moment))
  if (shortcut.need !== 'all') detail.push(getNeedLabel(shortcut.need))
  return detail.join(' · ') || 'Opens with broad browse settings.'
}

function getMomentLabel(value) {
  return momentOptions.find(option => option.value === value)?.label || 'Any time'
}

function getEffortLabel(value) {
  return effortOptions.find(option => option.value === value)?.label || 'Any effort'
}

function getNeedLabel(value) {
  return needOptions.find(option => option.value === value)?.label || 'Any need'
}
</script>

<style scoped>
:global(:root) {
  --c-black:#0a0b0a; --c-900:#111312; --c-800:#1c1f1d; --c-700:#2d3230;
  --c-500:#52605a; --c-400:#7a8880; --c-300:#a8b5ae; --c-100:#e8ece9;
  --c-50:#f4f5f2; --c-white:#ffffff;
  --c-green:#16a34a; --c-green-pale:#dcfce7; --c-green-soft:#f0fdf4;
  --c-amber:#d97706; --c-amber-soft:#fffbeb;
  --c-blue:#2563eb; --c-blue-soft:#eff6ff;
  --c-pink:#db2777; --c-pink-soft:#fdf2f8;
  --border:rgba(10,11,10,0.08); --border-mid:rgba(10,11,10,0.14);
  --shadow-xs:0 1px 4px rgba(0,0,0,0.06); --shadow-sm:0 2px 12px rgba(0,0,0,0.07);
  --shadow-md:0 8px 28px rgba(0,0,0,0.09);
  --f-display:'Fraunces', Georgia, serif;
  --f-body:'General Sans','Helvetica Neue',ui-sans-serif,sans-serif;
  --f-mono:'JetBrains Mono',monospace;
  --section-v:clamp(72px,8vw,108px);
}

:global(*, *::before, *::after){box-sizing:border-box}
:global(body){margin:0;font-family:var(--f-body),system-ui;background:var(--c-white);color:var(--c-black);-webkit-font-smoothing:antialiased;overflow-x:hidden}

.nutrition-page{min-height:100vh;background:linear-gradient(180deg,#ffffff 0%, #f4f5f2 100%)}
.header{position:sticky;top:0;z-index:30;background:rgba(255,255,255,.92);border-bottom:1px solid var(--border);backdrop-filter:blur(18px)}
.header-inner,.section-wrap{max-width:1280px;margin:0 auto;padding:0 40px}
.header-inner{height:76px;display:flex;align-items:center;justify-content:space-between}
.logo{display:flex;align-items:center;gap:9px;text-decoration:none;color:var(--c-black)}
.logo-icon{width:28px;height:28px;color:var(--c-black)}
.logo-text{font-family:var(--f-display);font-size:1.22rem;color:var(--c-black);letter-spacing:-.03em}
.nav{display:flex;align-items:center;gap:2px}
.nav-a,.nav-link{height:36px;padding:0 12px;display:flex;align-items:center;font-size:.86rem;font-weight:500;color:var(--c-500);text-decoration:none;border-radius:8px;transition:all .18s}
.nav-a:hover,.nav-link:hover{color:var(--c-black);background:var(--c-50)}
.nav-cta{display:flex;align-items:center;gap:8px}
.nav-btn{height:38px;padding:0 16px;display:inline-flex;align-items:center;gap:7px;font-size:.86rem;font-weight:600;color:var(--c-white);background:var(--c-black);text-decoration:none;border-radius:10px;border:1px solid var(--c-900);transition:all .2s}
.nav-btn:hover{background:var(--c-800);transform:translateY(-1px)}

.hero,.shortcut-section,.tool-section{padding:var(--section-v) 0}
.hero-grid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(320px,.9fr);gap:24px;align-items:start}
.section-eyebrow{display:inline-flex;align-items:center;height:26px;padding:0 11px;border-radius:999px;border:1px solid var(--border-mid);font-size:.68rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--c-500);margin-bottom:18px}
.hero-title,.section-h2{margin:0;font-family:var(--f-display);font-weight:400;letter-spacing:-.03em;line-height:1.02}
.hero-title{font-size:clamp(2.2rem,4vw,4rem);margin-bottom:14px}
.section-h2{font-size:clamp(1.9rem,3.2vw,3rem)}
em{font-style:italic;color:var(--c-green)}
.hero-copy{font-size:.98rem;line-height:1.75;color:var(--c-500);max-width:42rem;margin:0}
.hero-tags{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.hero-tag,.mini-pill{display:inline-flex;align-items:center;border-radius:999px;font-weight:700}
.hero-tag{height:30px;padding:0 12px;background:var(--c-green-soft);border:1px solid rgba(22,163,74,.18);color:var(--c-green);font-size:.74rem}
.hero-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:18px}
.hero-action-solid,.hero-action-ghost,.priority-btn,.reset-btn,.mini-action{border:none;height:44px;padding:0 18px;border-radius:12px;display:inline-flex;align-items:center;justify-content:center;text-decoration:none;font-size:.88rem;font-weight:600;transition:all .2s ease;cursor:pointer}
.hero-action-solid,.priority-btn{background:var(--c-black);border:1px solid var(--c-900);color:var(--c-white)}
.hero-action-solid:hover,.priority-btn:hover{background:var(--c-800);transform:translateY(-1px)}
.hero-action-ghost,.reset-btn{background:transparent;border:1px solid var(--border-mid);color:var(--c-500)}
.hero-action-ghost:hover,.reset-btn:hover{background:var(--c-50);color:var(--c-black)}
.reset-btn{font-size:.86rem}

.text-fold{border-radius:14px;background:var(--c-50);border:1px solid var(--border);overflow:hidden;margin:12px 0 0;width:fit-content;max-width:42rem}
.text-fold.summary-spaced{margin-top:8px}
.text-fold summary{
  cursor:pointer;list-style:none;padding:11px 16px;font-size:.76rem;font-weight:700;color:var(--c-700);
  letter-spacing:.04em;text-transform:uppercase;display:flex;align-items:center;gap:8px;user-select:none;
}
.text-fold summary::-webkit-details-marker{display:none}
.text-fold summary::before{content:'⌄';font-size:.8rem;display:inline-block;transition:transform .18s;color:var(--c-green)}
.text-fold[open] summary::before{transform:rotate(180deg)}
.text-fold .mini-fold-body,
.text-fold:not(.text-fold--invert) > p{padding:0 16px 14px;margin:0;font-size:.82rem;line-height:1.6;color:var(--c-500)}
.hero-fold{text-align:left;background:rgba(248,249,246,.94)}
.hero-fold summary{padding:11px 16px;color:var(--c-700)}
.hero-fold > .hero-copy{padding:0 16px 14px;display:block;text-align:left}
.text-fold.section-fold,
.text-fold.collapsed-fold{max-width:none;width:100%;background:rgba(255,255,255,.92)}
.collapsed-copy{font-size:.84rem;color:var(--c-500);margin:0 16px 10px;line-height:1.55}

.text-fold--invert{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.16)}
.text-fold--invert summary{color:rgba(255,252,246,.92)}
.text-fold--invert > p{color:rgba(255,254,251,.74);padding:0 16px 14px;margin:0}

.section-fold{margin-top:0}
.section-desc{margin:0;padding:2px 16px 14px;font-size:.98rem;line-height:1.75;color:var(--c-500)}

.shortcut-section .shortcut-tile{display:flex;flex-direction:column;gap:10px;background:transparent}
.shortcut-tile-more{font-size:inherit;width:100%;margin:0;border-radius:12px;background:var(--c-50);border:1px solid var(--border)}
.shortcut-tile-more summary{font-size:.7rem;font-weight:700;color:var(--c-600)}
.shortcut-tile-more-body{margin:0 14px 12px;font-size:.8rem;line-height:1.55;color:var(--c-600)}

.muted-on-dark{color:rgba(255,255,255,.7)!important;margin:0}

.hero-kpis{display:grid;gap:14px}
.hero-kpi-card{padding:22px;background:var(--c-white);border:1px solid var(--border);border-radius:20px;box-shadow:var(--shadow-sm)}
.hero-kpi-card.feature{background:linear-gradient(145deg,#f0fdf4,#ffffff);border-color:rgba(22,163,74,.16)}
.hero-kpi-card span{display:block;font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:8px}
.hero-kpi-card strong{display:block;font-family:var(--f-display);font-size:1.9rem;font-weight:400;color:var(--c-black);line-height:1.05;margin-bottom:8px}
.hero-kpi-card p{margin:0;font-size:.82rem;color:var(--c-500);line-height:1.6}
.hero-kpi-card .text-fold{width:100%;background:rgba(255,255,255,.88);margin-bottom:12px;margin-top:0}
.hero-kpi-card.feature .mini-fold-body{color:var(--c-700)}
.hero-kpi-card.dark{background:var(--c-900);border-color:rgba(255,255,255,.06)}
.hero-kpi-card.dark strong{color:var(--c-white)}
.hero-kpi-card.dark span{color:rgba(255,255,255,.4)}
.hero-kpi-card.dark .mini-action{color:var(--c-green-soft)}
.hero-kpi-card.dark strong + .text-fold{border-color:rgba(255,255,255,.14);background:rgba(255,255,255,.06)}
.hero-kpi-card.dark .text-fold summary{color:rgba(237,246,239,.94)}
.hero-kpi-card.dark .text-fold .mini-fold-body,
.hero-kpi-card.dark > .text-fold > .muted-on-dark{color:rgba(239,246,239,.74)!important}
.mini-action{margin-top:8px;height:38px;padding:0 14px;background:var(--c-white);border:1px solid rgba(22,163,74,.22);color:var(--c-green);font-size:.8rem;border-radius:10px;width:fit-content}
.mini-action:hover{background:var(--c-green-soft)}

.purpose-card .text-fold{border-radius:14px;background:rgba(0,0,0,.06);margin-top:10px;width:100%;max-width:none}

.purpose-section{padding-top:0;padding-bottom:20px}
.purpose-grid{display:grid;grid-template-columns:1.2fr .9fr .9fr;gap:16px}
.purpose-card{padding:24px;border-radius:22px;background:var(--c-white);border:1px solid var(--border);box-shadow:var(--shadow-sm)}
.purpose-card.dark{background:var(--c-900);border-color:rgba(255,255,255,.06)}
.purpose-label{display:block;font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:10px}
.purpose-card.dark .purpose-label{color:rgba(255,255,255,.35)}
.purpose-card h2,.purpose-card h3{margin:0 0 6px;font-family:var(--f-display);font-weight:400;letter-spacing:-.02em;line-height:1.15}
.purpose-card h2{font-size:1.8rem;color:var(--c-white)}
.purpose-card h3{font-size:1.25rem;color:var(--c-black)}
.purpose-card.dark .text-fold--invert{border-color:rgba(255,255,255,.14)}

.priority-copy{margin:0;font-size:.88rem;color:var(--c-500);line-height:1.7}

.section-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,.8fr);gap:24px;align-items:end;margin-bottom:28px}

.priority-card{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:20px;align-items:center;padding:24px 26px;border-radius:22px;background:linear-gradient(145deg,#f0fdf4,#ffffff);border:1px solid rgba(22,163,74,.18);box-shadow:var(--shadow-sm);margin-bottom:18px}
.priority-label{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-green);margin-bottom:8px}
.priority-title{font-family:var(--f-display);font-size:1.45rem;color:var(--c-black);letter-spacing:-.02em;margin-bottom:6px}
.priority-copy{padding:10px 0 14px;margin:0}
.priority-card .text-fold{width:100%;margin-top:0}

.shortcut-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.shortcut-card{
  padding:18px 20px;width:100%;border-radius:18px;background:var(--c-white);border:1px solid var(--border);
  box-shadow:var(--shadow-xs);text-align:left;cursor:pointer;transition:all .2s;display:block;
}
.shortcut-card:hover{transform:translateY(-3px);box-shadow:var(--shadow-md)}
.shortcut-kicker{display:block;font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:8px}
.shortcut-card strong{display:block;font-family:var(--f-display);font-size:1.05rem;color:var(--c-black)}
.module-tabs{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:18px}
.module-tab,.filter-chip{border:none;cursor:pointer;transition:all .18s ease}
.module-tab{height:42px;padding:0 16px;border-radius:999px;background:var(--c-white);border:1px solid var(--border-mid);font-size:.86rem;font-weight:700;color:var(--c-500)}
.module-tab.active{background:var(--c-black);border-color:var(--c-black);color:var(--c-white)}
.filter-panel{padding:22px;background:var(--c-white);border:1px solid var(--border);border-radius:22px;box-shadow:var(--shadow-sm);display:grid;gap:16px}
.filter-group{display:grid;grid-template-columns:92px 1fr;gap:14px;align-items:start}
.filter-label{display:block;padding-top:8px;font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400)}
.filter-chips{display:flex;flex-wrap:wrap;gap:10px}
.filter-chip{height:38px;padding:0 14px;border-radius:999px;background:var(--c-50);border:1px solid var(--border);font-size:.8rem;font-weight:700;color:var(--c-500)}
.filter-chip.active{background:var(--c-green-soft);border-color:rgba(22,163,74,.22);color:var(--c-green)}
.result-summary{display:flex;justify-content:space-between;align-items:center;gap:20px;margin:20px 0 22px}
.result-count{font-family:var(--f-display);font-size:1.5rem;color:var(--c-black);letter-spacing:-.02em}
.result-line{margin:6px 0 0;font-size:.88rem;color:var(--c-500);line-height:1.55}
.dropdown-head{width:100%;display:flex;justify-content:space-between;align-items:center;gap:18px;padding:18px 20px;border-radius:20px;background:var(--c-white);border:1px solid var(--border);box-shadow:var(--shadow-sm);text-align:left;cursor:pointer;color:inherit;font:inherit;border-style:solid}
.dropdown-meta{display:flex;align-items:center;gap:12px}
.dropdown-arrow{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:var(--c-50);color:var(--c-500);font-size:1rem;transition:transform .18s ease}
.dropdown-arrow.open{transform:rotate(180deg)}
.tool-group-kicker{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:6px}
.tool-group-title{margin:0;font-family:var(--f-display);font-size:1.5rem;font-weight:400;color:var(--c-black)}
.tool-group-count{height:28px;padding:0 12px;border-radius:999px;background:var(--c-green-soft);color:var(--c-green);font-size:.76rem;font-weight:700;display:inline-flex;align-items:center}
.collapsed-preview{padding:12px 0 6px}

.active-filter-strip{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:0 0 22px}
.active-filter-label{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400)}
.active-filter-pills{display:flex;flex-wrap:wrap;gap:8px}
.active-filter-pill{height:28px;padding:0 12px;border-radius:999px;background:var(--c-white);border:1px solid var(--border);display:inline-flex;align-items:center;font-size:.74rem;font-weight:700;color:var(--c-500)}
.active-filter-pill.neutral{background:var(--c-50)}
.empty-results-card{padding:30px;border-radius:24px;background:var(--c-white);border:1px solid var(--border);box-shadow:var(--shadow-sm);text-align:center}
.empty-results-card h3{margin:0 0 10px;font-family:var(--f-display);font-size:1.4rem;font-weight:400;color:var(--c-black)}
.empty-reset{margin:0 auto}
.tool-groups{display:grid;gap:20px}
.preview-chip-row{display:flex;flex-wrap:wrap;gap:10px}
.preview-chip{display:inline-flex;align-items:center;min-height:34px;padding:8px 12px;border-radius:999px;background:var(--c-white);border:1px solid var(--border);font-size:.76rem;font-weight:600;color:var(--c-700)}
.tool-card-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding-top:16px}
.tool-card{padding:22px;border-radius:22px;background:var(--c-white);border:1px solid var(--border);box-shadow:var(--shadow-sm);display:flex;flex-direction:column;gap:0}
.tool-card.featured{box-shadow:0 0 0 2px rgba(22,163,74,.12),var(--shadow-md)}
.tool-card.module-meal{border-top:4px solid var(--c-green)}
.tool-card.module-snack{border-top:4px solid var(--c-amber)}
.tool-card.module-lunchbox{border-top:4px solid var(--c-blue)}
.tool-card-top{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:14px}
.featured-ribbon{display:inline-flex;align-items:center;height:24px;padding:0 10px;border-radius:999px;background:var(--c-green-soft);color:var(--c-green);font-size:.68rem;font-weight:700;letter-spacing:.04em;margin-bottom:10px}
.tool-card-badge{height:24px;padding:0 10px;border-radius:999px;background:var(--c-50);font-size:.68rem;font-weight:700;display:inline-flex;align-items:center;color:var(--c-500)}
.tool-card-time{font-family:var(--f-mono);font-size:.68rem;font-weight:700;color:var(--c-400)}
.tool-card-title{margin:0 0 14px;font-family:var(--f-display);font-size:1.18rem;font-weight:400;line-height:1.2;color:var(--c-black)}
.pill-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}

.expand-card-fold{margin-top:auto;width:100%;border-radius:16px;background:var(--c-50);border:1px solid var(--border);overflow:hidden}
.expand-card-fold summary{cursor:pointer;list-style:none;padding:13px 16px;font-size:.73rem;font-weight:800;color:var(--c-700);letter-spacing:.08em;text-transform:uppercase;user-select:none}
.expand-card-fold summary::-webkit-details-marker{display:none}
.expand-card-fold summary::before{content:'⌄ ';color:var(--c-green)}
.expand-card-fold[open] summary{border-bottom:1px solid rgba(10,11,10,.06);margin-bottom:2px;padding-bottom:12px}
.expand-card-inner{padding:6px 16px 18px}

.tool-card-summary{margin:0 0 14px;font-size:.84rem;color:var(--c-500);line-height:1.7}
.mini-pill{height:24px;padding:0 10px;background:var(--c-50);color:var(--c-500);font-size:.68rem;border:1px solid var(--border);display:inline-flex;align-items:center}
.detail-block{margin-bottom:14px}
.detail-label{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:8px}
.detail-value{font-size:.82rem;font-weight:600;color:var(--c-700)}
.detail-list{margin:0;padding-left:18px;display:grid;gap:6px;font-size:.8rem;color:var(--c-700);line-height:1.55}
.detail-list.ordered{padding-left:20px}
.tool-tip{padding:14px 15px;margin:12px 0 14px;border-radius:14px;background:var(--c-green-soft);border:1px solid rgba(22,163,74,.12);font-size:.8rem;color:var(--c-700);line-height:1.55}
.swap-grid{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;align-items:center;margin-bottom:14px}
.swap-box{padding:14px;border-radius:16px;border:1px solid var(--border)}
.swap-box span,.parent-move span,.lunch-row span{display:block;font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--c-400);margin-bottom:6px}
.swap-box strong,.lunch-row strong{font-size:.88rem;color:var(--c-black);line-height:1.45}
.swap-box.current{background:var(--c-50)}
.swap-box.better{background:var(--c-green-soft);border-color:rgba(22,163,74,.16)}
.swap-arrow{font-family:var(--f-display);font-size:1.4rem;color:var(--c-400);text-align:center}
.parent-move{padding:14px;margin-bottom:14px;border-radius:14px;background:var(--c-50);border:1px solid var(--border)}
.parent-move p{margin:0;font-size:.8rem;color:var(--c-500);line-height:1.6}
.lunchbox-stack{display:grid;gap:10px;margin-bottom:14px}
.lunch-row{padding:13px 14px;border-radius:14px;background:var(--c-blue-soft);border:1px solid rgba(37,99,235,.12)}
.expand-card-inner .tool-tip{margin-bottom:0}
.expand-card-inner .parent-move:last-child{margin-bottom:4px}

@media(max-width:1100px){
  .hero-grid,.section-head,.priority-card,.purpose-grid{grid-template-columns:1fr}
  .shortcut-grid,.tool-card-grid{grid-template-columns:repeat(2,1fr)}
}

@media(max-width:760px){
  .header-inner,.section-wrap{padding-left:24px;padding-right:24px}
  .nav,.nav-link{display:none}
  .filter-group{grid-template-columns:1fr}
  .result-summary,.dropdown-head{flex-direction:column;align-items:flex-start}
  .shortcut-grid,.tool-card-grid,.swap-grid{grid-template-columns:1fr}
}
</style>
