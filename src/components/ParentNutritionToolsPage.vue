<template>
  <div class="nutrition-page">

    <!-- HEADER -->
    <header class="header">
      <div class="header-inner">
        <RouterLink to="/" class="logo">
          <div class="logo-mark">
            <svg viewBox="0 0 36 36" fill="none">
              <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.4"/>
              <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor"/>
              <path d="M18 13C15.5 15.5 15 19 18 23" stroke="white" stroke-width="1.3" stroke-linecap="round" fill="none" opacity="0.6"/>
            </svg>
          </div>
          <span>HealthyKids</span>
        </RouterLink>

        <nav class="nav">
          <RouterLink to="/parent-dashboard" class="nav-a">Dashboard</RouterLink>
          <RouterLink to="/parent-roadmap" class="nav-a">Roadmap</RouterLink>
          <RouterLink to="/young-person-dashboard" class="nav-a">Kids view</RouterLink>
        </nav>

        <RouterLink to="/parent-dashboard" class="back-btn">
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M9 2L4 7l5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Back
        </RouterLink>
      </div>
    </header>

    <!-- HERO: TWO PANEL LAYOUT -->
    <section class="hero-section">
      <div class="hero-left">
        <div class="hero-label">Nutrition support</div>
        <h1 class="hero-h1">
          What should<br/>
          <span class="hero-accent">{{ childName }}</span><br/>
          eat today?
        </h1>
        <p class="hero-sub">Meal ideas, snack combos, lunchbox builds, and a live food-score tool - all shaped around your family's actual plan.</p>

        <div class="hero-stat-row">
          <div class="hero-stat">
            <div class="hs-num">{{ moduleCounts.meal }}</div>
            <div class="hs-lbl">Meal ideas</div>
          </div>
          <div class="hero-stat-div"></div>
          <div class="hero-stat">
            <div class="hs-num">{{ moduleCounts.snack }}</div>
            <div class="hs-lbl">Snack combos</div>
          </div>
          <div class="hero-stat-div"></div>
          <div class="hero-stat">
            <div class="hs-num">{{ moduleCounts.lunchbox }}</div>
            <div class="hs-lbl">Lunchbox builds</div>
          </div>
        </div>

        <div class="hero-path-row">
          <button
            v-for="shortcut in nutritionQuickStarts.slice(0, 3)"
            :key="shortcut.id"
            class="path-chip"
            :class="{ active: activeModule === shortcut.module && selectedMoment === shortcut.moment }"
            @click="applyQuickStart(shortcut)"
          >
            {{ shortcut.label }}
          </button>
        </div>
      </div>

      <!-- AI SCORER - RIGHT PANEL -->
      <div class="hero-right">
        <div class="ai-panel">
          <div class="ai-panel-header">
            <div class="ai-indicator">
              <span class="ai-dot"></span>
              AI food scorer
            </div>
            <div class="ai-model-badge">Claude-powered</div>
          </div>

          <div class="ai-prompt-area">
            <p class="ai-prompt-label">Type any food - get a health score instantly</p>
            <div class="ai-input-row">
              <input
                v-model="foodInput"
                class="ai-input"
                type="text"
                placeholder="e.g. banana, white bread, milo..."
                @keyup.enter="submitFoodPrediction"
                @input="clearPrediction"
              />
              <button
                class="ai-submit"
                :class="{ loading: foodPredictionLoading }"
                :disabled="foodPredictionLoading || !foodInput.trim()"
                @click="submitFoodPrediction"
              >
                <span v-if="!foodPredictionLoading">Score it</span>
                <span v-else class="ai-spinner"></span>
              </button>
            </div>

            <div v-if="foodPredictionError" class="ai-error">
              {{ foodPredictionError }}
            </div>

            <div v-if="foodPredictionCandidates.length" class="ai-candidates">
              <span class="ai-candidates-label">Did you mean?</span>
              <button
                v-for="c in foodPredictionCandidates"
                :key="c"
                class="ai-candidate-btn"
                @click="chooseFoodCandidate(c)"
              >{{ c }}</button>
            </div>
          </div>

          <!-- RESULT -->
          <Transition name="result-fade">
            <div v-if="foodPredictionResult" class="ai-result">
              <div class="ai-result-score-col">
                <div
                  class="ai-score-ring"
                  :class="scoreClass(foodPredictionResult.health_score)"
                >
                  <svg viewBox="0 0 80 80" class="ring-svg">
                    <circle cx="40" cy="40" r="32" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="7"/>
                    <circle
                      cx="40" cy="40" r="32"
                      fill="none"
                      :stroke="scoreColor(foodPredictionResult.health_score)"
                      stroke-width="7"
                      stroke-linecap="round"
                      :stroke-dasharray="`${(foodPredictionResult.health_score / 100) * 201} 201`"
                      transform="rotate(-90 40 40)"
                      class="ring-fill"
                    />
                  </svg>
                  <div class="ring-number">{{ Math.round(foodPredictionResult.health_score) }}</div>
                </div>
                <div class="score-verdict" :class="scoreClass(foodPredictionResult.health_score)">
                  {{ scoreVerdict(foodPredictionResult.health_score) }}
                </div>
              </div>

              <div class="ai-result-detail">
                <div class="ai-matched-food">{{ foodPredictionResult.matched_food }}</div>
                <div class="ai-category-pill">{{ foodPredictionResult.category }}</div>

                <div class="ai-score-bar-block">
                  <div class="ai-bar-track">
                    <div
                      class="ai-bar-fill"
                      :style="{ width: foodPredictionResult.health_score + '%', background: scoreColor(foodPredictionResult.health_score) }"
                    ></div>
                  </div>
                  <div class="ai-bar-labels">
                    <span>0</span>
                    <span>50</span>
                    <span>100</span>
                  </div>
                </div>

                <div class="ai-tip-block">
                  {{ scoreTip(foodPredictionResult.health_score, foodPredictionResult.matched_food) }}
                </div>

                <button class="ai-clear-btn" @click="clearAndReset">
                  Score another food
                </button>
              </div>
            </div>
          </Transition>

          <!-- IDLE EXAMPLES -->
          <div v-if="!foodPredictionResult && !foodPredictionLoading" class="ai-idle-examples">
            <span class="idle-label">Try:</span>
            <button v-for="ex in exampleFoods" :key="ex" class="idle-chip" @click="tryExample(ex)">
              {{ ex }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- FILTER RAIL -->
    <section class="filter-section">
      <div class="filter-wrap">
        <div class="filter-rail">
          <div class="filter-group">
            <span class="fg-label">Type</span>
            <div class="fg-chips">
              <button
                v-for="opt in moduleOptions"
                :key="opt.value"
                class="fg-chip"
                :class="{ active: activeModule === opt.value }"
                @click="activeModule = opt.value"
              >
                <span class="chip-dot" :class="'dot-' + opt.value"></span>
                {{ opt.label }}
              </button>
            </div>
          </div>

          <div class="filter-divider"></div>

          <div class="filter-group">
            <span class="fg-label">When</span>
            <div class="fg-chips">
              <button
                v-for="opt in momentOptions"
                :key="opt.value"
                class="fg-chip"
                :class="{ active: selectedMoment === opt.value }"
                @click="selectedMoment = opt.value"
              >{{ opt.label }}</button>
            </div>
          </div>

          <div class="filter-divider"></div>

          <div class="filter-group">
            <span class="fg-label">Effort</span>
            <div class="fg-chips">
              <button
                v-for="opt in effortOptions"
                :key="opt.value"
                class="fg-chip"
                :class="{ active: selectedEffort === opt.value }"
                @click="selectedEffort = opt.value"
              >{{ opt.label }}</button>
            </div>
          </div>

          <div class="filter-divider"></div>

          <div class="filter-group">
            <span class="fg-label">Need</span>
            <div class="fg-chips">
              <button
                v-for="opt in needOptions"
                :key="opt.value"
                class="fg-chip"
                :class="{ active: selectedNeed === opt.value }"
                @click="selectedNeed = opt.value"
              >{{ opt.label }}</button>
            </div>
          </div>

          <button v-if="hasActiveFilters" class="reset-pill" @click="resetFilters">
            <svg width="10" height="10" viewBox="0 0 10 10"><path d="M1 1l8 8M9 1L1 9" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
            Clear
          </button>
        </div>

        <div class="result-bar">
          <div class="rb-count">
            <span class="rb-num">{{ filteredItems.length }}</span>
            <span class="rb-lbl">suggestions</span>
          </div>
          <div class="rb-tags">
            <span v-if="selectedMoment !== 'all'" class="rb-tag">{{ getMomentLabel(selectedMoment) }}</span>
            <span v-if="selectedEffort !== 'all'" class="rb-tag">{{ getEffortLabel(selectedEffort) }}</span>
            <span v-if="selectedNeed !== 'all'" class="rb-tag">{{ getNeedLabel(selectedNeed) }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- EMPTY STATE -->
    <section v-if="filteredItems.length === 0" class="empty-section">
      <div class="empty-wrap">
        <div class="empty-icon">🥗</div>
        <h2>No matches for those filters</h2>
        <p>Relax one filter and options will appear immediately.</p>
        <button class="reset-btn" @click="resetFilters">Show everything</button>
      </div>
    </section>

    <!-- CONTENT GROUPS -->
    <section v-else class="content-section">
      <div class="content-wrap">

        <!-- FEATURED CARD (pinned to top if result exists) -->
        <div v-if="featuredSuggestion" class="featured-banner">
          <div class="fb-label">
            <svg width="12" height="12" viewBox="0 0 12 12"><path d="M6 1l1.5 3h3l-2.4 1.8.9 3L6 7.2 3 8.8l.9-3L1.5 4h3z" fill="currentColor"/></svg>
            Best match right now
          </div>
          <div class="fb-content">
            <div class="fb-left">
              <div class="fb-module-pill" :class="'pill-' + featuredSuggestion.module">
                {{ moduleMap[featuredSuggestion.module].label }}
              </div>
              <h3 class="fb-title">{{ featuredSuggestion.title }}</h3>
              <p class="fb-reason">{{ featuredSuggestionReason }}</p>
            </div>
            <div class="fb-right">
              <div class="fb-effort-chip">{{ featuredSuggestion.timeLabel || getEffortLabel(featuredSuggestion.effort) }}</div>
              <button class="fb-expand-btn" @click="expandFeatured = !expandFeatured">
                {{ expandFeatured ? 'Collapse' : 'See details' }}
                <svg width="12" height="12" viewBox="0 0 12 12" :style="{ transform: expandFeatured ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }">
                  <path d="M2 4l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/>
                </svg>
              </button>
            </div>
          </div>

          <Transition name="expand">
            <div v-if="expandFeatured" class="fb-expanded">
              <MealCardExpanded v-if="featuredSuggestion.module === 'meal'" :item="featuredSuggestion" :getMomentLabel="getMomentLabel" :getNeedLabel="getNeedLabel"/>
              <SnackCardExpanded v-else-if="featuredSuggestion.module === 'snack'" :item="featuredSuggestion"/>
              <LunchboxCardExpanded v-else :item="featuredSuggestion"/>
            </div>
          </Transition>
        </div>

        <!-- GROUPED TOOL CARDS -->
        <div v-for="group in groupedItems" :key="group.key" class="tool-group">
          <div class="tg-header">
            <div class="tg-header-left">
              <div class="tg-dot" :class="'dot-' + group.key"></div>
              <h2 class="tg-title">{{ group.title }}</h2>
              <span class="tg-count">{{ group.items.length }}</span>
            </div>
            <button class="tg-toggle" @click="toggleGroup(group.key)">
              {{ isGroupOpen(group.key) ? 'Collapse' : 'Expand all' }}
            </button>
          </div>

          <!-- COLLAPSED PREVIEW STRIP -->
          <div v-if="!isGroupOpen(group.key)" class="tg-preview">
            <div
              v-for="item in group.items"
              :key="item.id"
              class="preview-row"
              :class="{ featured: item.id === featuredSuggestion?.id }"
              @click="openItem(item)"
            >
              <div class="pr-left">
                <span class="pr-dot" :class="'dot-' + item.module"></span>
                <span class="pr-title">{{ item.title }}</span>
              </div>
              <div class="pr-right">
                <span class="pr-effort">{{ item.timeLabel || getEffortLabel(item.effort) }}</span>
                <svg width="12" height="12" viewBox="0 0 12 12" class="pr-arrow"><path d="M4 2l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/></svg>
              </div>
            </div>
          </div>

          <!-- EXPANDED CARD GRID -->
          <div v-else class="tg-grid">
            <article
              v-for="item in group.items"
              :key="item.id"
              class="tool-card"
              :class="['tc-' + item.module, { 'tc-featured': item.id === featuredSuggestion?.id, 'tc-open': openItems.includes(item.id) }]"
            >
              <div class="tc-head" @click="toggleItem(item.id)">
                <div class="tc-head-left">
                  <span class="tc-badge" :class="'badge-' + item.module">{{ moduleMap[item.module].label }}</span>
                  <span v-if="item.id === featuredSuggestion?.id" class="tc-star">★ Best fit</span>
                </div>
                <span class="tc-time">{{ item.timeLabel || getEffortLabel(item.effort) }}</span>
              </div>

              <h4 class="tc-title" @click="toggleItem(item.id)">{{ item.title }}</h4>

              <div v-if="item.module === 'meal'" class="tc-pills">
                <span v-for="need in item.needs.slice(0, 3)" :key="need" class="tc-pill">
                  {{ getNeedLabel(need) }}
                </span>
              </div>

              <Transition name="tc-expand">
                <div v-if="openItems.includes(item.id)" class="tc-body">
                  <MealCardExpanded v-if="item.module === 'meal'" :item="item" :getMomentLabel="getMomentLabel" :getNeedLabel="getNeedLabel"/>
                  <SnackCardExpanded v-else-if="item.module === 'snack'" :item="item"/>
                  <LunchboxCardExpanded v-else :item="item"/>
                </div>
              </Transition>

              <button class="tc-toggle-btn" @click="toggleItem(item.id)">
                <span>{{ openItems.includes(item.id) ? 'Less' : 'See how' }}</span>
                <svg width="11" height="11" viewBox="0 0 11 11" :style="{ transform: openItems.includes(item.id) ? 'rotate(180deg)' : 'none', transition: 'transform .2s' }">
                  <path d="M1 3l4.5 4.5L10 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" fill="none"/>
                </svg>
              </button>
            </article>
          </div>
        </div>

      </div>
    </section>

  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'
import { useFoodHealthPredictor } from '../composables/useFoodHealthPredictor'
import { nutritionQuickStarts, nutritionToolItems } from '../data/nutritionToolsData'

const { state } = useFamilyPlanStore()
const childName  = computed(() => state.childName || 'your child')
const concerns   = computed(() => state.concerns || [])

const foodInput = ref('')
const {
  loading:    foodPredictionLoading,
  error:      foodPredictionError,
  result:     foodPredictionResult,
  candidates: foodPredictionCandidates,
  predictFood,
  clearPrediction,
} = useFoodHealthPredictor()

const exampleFoods = ['banana', 'white bread', 'greek yoghurt', 'milo', 'carrot sticks', 'potato chips']

function submitFoodPrediction() {
  if (foodInput.value.trim()) predictFood(foodInput.value.trim())
}
function chooseFoodCandidate(c) { foodInput.value = c; predictFood(c) }
function tryExample(ex)         { foodInput.value = ex; predictFood(ex) }
function clearAndReset()        { foodInput.value = ''; clearPrediction() }

function scoreClass(score) {
  if (score >= 70) return 'score-good'
  if (score >= 40) return 'score-mid'
  return 'score-low'
}
function scoreColor(score) {
  if (score >= 70) return '#22c55e'
  if (score >= 40) return '#f59e0b'
  return '#ef4444'
}
function scoreVerdict(score) {
  if (score >= 80) return 'Excellent'
  if (score >= 65) return 'Good'
  if (score >= 45) return 'Okay'
  if (score >= 25) return 'Limited'
  return 'Low'
}
function scoreTip(score, food) {
  if (score >= 70) return `${food} is a solid choice — great for energy and packed with nutrients.`
  if (score >= 40) return `${food} is fine occasionally — pair it with something more nutritious to balance the meal.`
  return `${food} scores low. Look for a swap or save it for a treat rather than a regular option.`
}

// ─── Filter state ─────────────────────────────────────────────────────────────
const activeModule   = ref('all')
const selectedMoment = ref('all')
const selectedEffort = ref('all')
const selectedNeed   = ref('all')
const expandedGroups = ref([])
const openItems      = ref([])
const expandFeatured = ref(false)

const hasActiveFilters = computed(() =>
  activeModule.value !== 'all' || selectedMoment.value !== 'all' ||
  selectedEffort.value !== 'all' || selectedNeed.value !== 'all'
)

// ─── Options ──────────────────────────────────────────────────────────────────
const moduleOptions = [
  { value: 'all',      label: 'All' },
  { value: 'meal',     label: 'Meals' },
  { value: 'snack',    label: 'Snacks' },
  { value: 'lunchbox', label: 'Lunchbox' },
]
const momentOptions = [
  { value: 'all',          label: 'Any time' },
  { value: 'breakfast',    label: 'Breakfast' },
  { value: 'after-school', label: 'After school' },
  { value: 'school-lunch', label: 'School lunch' },
  { value: 'dinner',       label: 'Dinner' },
  { value: 'dessert',      label: 'Dessert' },
]
const effortOptions = [
  { value: 'all',        label: 'Any' },
  { value: 'under-5',   label: '< 5 min' },
  { value: 'under-15',  label: '< 15 min' },
  { value: 'make-ahead', label: 'Make-ahead' },
]
const needOptions = [
  { value: 'all',            label: 'Any' },
  { value: 'protein',        label: 'Protein' },
  { value: 'fruit-veg',      label: 'Fruit & veg' },
  { value: 'fussy-friendly', label: 'Fussy kids' },
  { value: 'budget',         label: 'Budget' },
  { value: 'lunchbox-safe',  label: 'Lunchbox-safe' },
]
const moduleMap = {
  meal:     { label: 'Meal',     title: 'Meal ideas' },
  snack:    { label: 'Snack',    title: 'Snack ideas' },
  lunchbox: { label: 'Lunchbox', title: 'Lunchbox builds' },
}

// ─── Counts ───────────────────────────────────────────────────────────────────
const moduleCounts = computed(() =>
  nutritionToolItems.reduce((acc, item) => {
    acc[item.module] = (acc[item.module] || 0) + 1
    return acc
  }, { meal: 0, snack: 0, lunchbox: 0 })
)

// ─── Filtering ────────────────────────────────────────────────────────────────
const filteredItems = computed(() =>
  nutritionToolItems.filter(item => {
    if (activeModule.value !== 'all'   && item.module  !== activeModule.value)          return false
    if (selectedMoment.value !== 'all' && item.moment  !== selectedMoment.value)        return false
    if (selectedEffort.value !== 'all' && item.effort  !== selectedEffort.value)        return false
    if (selectedNeed.value   !== 'all' && !item.needs?.includes(selectedNeed.value))    return false
    return true
  })
)

const primaryNutritionNeed = computed(() => {
  if (concerns.value.some(c => /snack|nutrition/i.test(c))) return 'protein'
  if (concerns.value.some(c => /routine/i.test(c)))         return 'lunchbox-safe'
  return 'fussy-friendly'
})

const featuredSuggestion = computed(() => {
  const preferredNeed = selectedNeed.value !== 'all' ? selectedNeed.value : primaryNutritionNeed.value
  return (
    filteredItems.value.find(item => item.needs?.includes(preferredNeed)) ||
    filteredItems.value[0] || null
  )
})

const featuredSuggestionReason = computed(() => {
  if (selectedNeed.value !== 'all')
    return `Best match for ${getNeedLabel(selectedNeed.value).toLowerCase()} with minimal effort.`
  if (concerns.value.some(c => /snack|nutrition/i.test(c)))
    return `Chosen to reduce snack friction and make healthy options easy for ${childName.value}.`
  return 'Practical, low-friction, and ready to use today.'
})

const groupedItems = computed(() => {
  const order = activeModule.value === 'all'
    ? ['meal', 'snack', 'lunchbox']
    : [activeModule.value]
  return order
    .map(key => ({
      key,
      title: moduleMap[key].title,
      items: filteredItems.value.filter(i => i.module === key),
    }))
    .filter(g => g.items.length > 0)
})

// ─── Actions ──────────────────────────────────────────────────────────────────
function applyQuickStart(shortcut) {
  activeModule.value   = shortcut.module
  selectedMoment.value = shortcut.moment
  selectedEffort.value = shortcut.effort
  selectedNeed.value   = shortcut.need
  expandedGroups.value = shortcut.module !== 'all' ? [shortcut.module] : []
}
function toggleGroup(key) {
  expandedGroups.value = expandedGroups.value.includes(key)
    ? expandedGroups.value.filter(k => k !== key)
    : [...expandedGroups.value, key]
}
function isGroupOpen(key) { return expandedGroups.value.includes(key) }

function toggleItem(id) {
  openItems.value = openItems.value.includes(id)
    ? openItems.value.filter(i => i !== id)
    : [...openItems.value, id]
}
function openItem(item) {
  // When clicking a preview row, expand the group and open the card
  if (!expandedGroups.value.includes(item.module)) {
    expandedGroups.value = [...expandedGroups.value, item.module]
  }
  if (!openItems.value.includes(item.id)) {
    openItems.value = [...openItems.value, item.id]
  }
  setTimeout(() => {
    document.getElementById(`item-${item.id}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }, 100)
}
function resetFilters() {
  activeModule.value   = 'all'
  selectedMoment.value = 'all'
  selectedEffort.value = 'all'
  selectedNeed.value   = 'all'
  expandedGroups.value = []
  openItems.value      = []
}

// ─── Label helpers ────────────────────────────────────────────────────────────
function getMomentLabel(v) { return momentOptions.find(o => o.value === v)?.label || 'Any time' }
function getEffortLabel(v) { return effortOptions.find(o => o.value === v)?.label || 'Any' }
function getNeedLabel(v)   { return needOptions.find(o => o.value === v)?.label || 'Any' }
</script>

<!-- ─── INLINE SUB-COMPONENTS ─────────────────────────────────────────────── -->
<script>
// Inline sub-components so the file is self-contained
const MealCardExpanded = {
  props: ['item', 'getMomentLabel', 'getNeedLabel'],
  template: `
    <div class="expanded-body">
      <p class="exp-summary">{{ item.summary }}</p>
      <div class="exp-row">
        <div class="exp-block">
          <div class="exp-label">Best for</div>
          <div class="exp-val">{{ getMomentLabel(item.moment) }}</div>
        </div>
        <div class="exp-block" v-if="item.needs?.length">
          <div class="exp-label">Covers</div>
          <div class="exp-pills">
            <span v-for="n in item.needs" :key="n" class="exp-pill">{{ getNeedLabel(n) }}</span>
          </div>
        </div>
      </div>
      <div v-if="item.items?.length" class="exp-section">
        <div class="exp-label">Ingredients</div>
        <ul class="exp-list">
          <li v-for="ing in item.items" :key="ing">{{ ing }}</li>
        </ul>
      </div>
      <div v-if="item.steps?.length" class="exp-section">
        <div class="exp-label">Steps</div>
        <ol class="exp-list ordered">
          <li v-for="step in item.steps" :key="step">{{ step }}</li>
        </ol>
      </div>
      <div v-if="item.benefit" class="exp-tip">{{ item.benefit }}</div>
    </div>
  `
}

const SnackCardExpanded = {
  props: ['item'],
  template: `
    <div class="expanded-body">
      <div class="exp-pair-grid">
        <div class="exp-pair-box left">
          <div class="exp-label">Pair one</div>
          <strong>{{ item.pairLeft }}</strong>
        </div>
        <div class="exp-plus">+</div>
        <div class="exp-pair-box right">
          <div class="exp-label">Pair two</div>
          <strong>{{ item.pairRight }}</strong>
        </div>
      </div>
      <p v-if="item.reason" class="exp-summary">{{ item.reason }}</p>
      <div v-if="item.serving" class="exp-tip">{{ item.serving }}</div>
      <div v-if="item.parentMove" class="exp-move">
        <div class="exp-label">Parent move</div>
        <p>{{ item.parentMove }}</p>
      </div>
    </div>
  `
}

const LunchboxCardExpanded = {
  props: ['item'],
  template: `
    <div class="expanded-body">
      <div class="exp-lunchbox">
        <div class="exp-lb-row base">
          <span class="exp-label">Base</span>
          <strong>{{ item.base }}</strong>
        </div>
        <div class="exp-lb-row fresh">
          <span class="exp-label">Fresh</span>
          <strong>{{ item.fresh }}</strong>
        </div>
        <div class="exp-lb-row extra">
          <span class="exp-label">Extra</span>
          <strong>{{ item.extra }}</strong>
        </div>
      </div>
      <div v-if="item.packTip" class="exp-tip">{{ item.packTip }}</div>
      <div v-if="item.parentMove" class="exp-move">
        <div class="exp-label">Parent move</div>
        <p>{{ item.parentMove }}</p>
      </div>
    </div>
  `
}

export default { components: { MealCardExpanded, SnackCardExpanded, LunchboxCardExpanded } }
</script>

<style scoped>
/* ─── TOKENS ──────────────────────────────────────────────────────────────── */
:global(:root) {
  --ink:      #0d0f0e;
  --ink-80:   #1a1d1b;
  --ink-60:   #3a3f3c;
  --ink-40:   #6b726d;
  --ink-20:   #a8b0ab;
  --ink-10:   #dde3de;
  --ink-05:   #f1f4f1;
  --paper:    #fafbf9;
  --white:    #ffffff;

  --green:    #15803d;
  --green-m:  #16a34a;
  --green-b:  #22c55e;
  --green-bg: #f0fdf4;
  --green-bd: rgba(21,128,61,.18);

  --amber:    #d97706;
  --amber-bg: #fffbeb;
  --amber-bd: rgba(217,119,6,.2);

  --blue:     #2563eb;
  --blue-bg:  #eff6ff;
  --blue-bd:  rgba(37,99,235,.18);

  --red:      #dc2626;
  --red-bg:   #fef2f2;

  --border:   rgba(13,15,14,.08);
  --border-m: rgba(13,15,14,.13);

  --sh-xs: 0 1px 3px rgba(0,0,0,.05);
  --sh-sm: 0 2px 10px rgba(0,0,0,.07);
  --sh-md: 0 6px 24px rgba(0,0,0,.09);

  --ff-display: 'Playfair Display', Georgia, serif;
  --ff-body:    'DM Sans', 'Helvetica Neue', sans-serif;
  --ff-mono:    'DM Mono', monospace;
}

:global(*, *::before, *::after) { box-sizing: border-box }
:global(body) {
  margin: 0;
  font-family: var(--ff-body);
  background: var(--paper);
  color: var(--ink);
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

/* ─── GOOGLE FONTS ────────────────────────────────────────────────────────── */
:global(head)::after {
  content: '';
}

/* ─── HEADER ──────────────────────────────────────────────────────────────── */
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(250,251,249,.94);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(16px);
}
.header-inner {
  max-width: 1380px;
  margin: 0 auto;
  padding: 0 40px;
  height: 68px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 9px;
  text-decoration: none;
  color: var(--ink);
  font-family: var(--ff-display);
  font-size: 1.18rem;
  font-weight: 700;
  letter-spacing: -.02em;
}
.logo-mark { width: 26px; height: 26px; flex-shrink: 0 }
.nav { display: flex; gap: 2px }
.nav-a {
  height: 34px;
  padding: 0 12px;
  display: flex;
  align-items: center;
  font-size: .83rem;
  font-weight: 500;
  color: var(--ink-40);
  text-decoration: none;
  border-radius: 8px;
  transition: all .15s;
}
.nav-a:hover { color: var(--ink); background: var(--ink-05) }
.back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 34px;
  padding: 0 14px;
  border-radius: 9px;
  border: 1px solid var(--border-m);
  background: var(--white);
  color: var(--ink-40);
  font-size: .82rem;
  font-weight: 600;
  text-decoration: none;
  transition: all .15s;
}
.back-btn:hover { color: var(--ink); background: var(--ink-05) }

/* ─── HERO ────────────────────────────────────────────────────────────────── */
.hero-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 540px;
  border-bottom: 1px solid var(--border);
}

/* Left */
.hero-left {
  padding: 64px 56px 56px 40px;
  max-width: 720px;
  margin: 0 auto 0 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.hero-label {
  display: inline-flex;
  align-items: center;
  height: 24px;
  padding: 0 10px;
  border-radius: 999px;
  background: var(--ink-05);
  border: 1px solid var(--border-m);
  font-size: .66rem;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--ink-40);
  margin-bottom: 22px;
  width: fit-content;
}
.hero-h1 {
  font-family: var(--ff-display);
  font-size: clamp(2.6rem, 4.5vw, 4.4rem);
  font-weight: 700;
  line-height: .98;
  letter-spacing: -.03em;
  color: var(--ink);
  margin: 0 0 20px;
}
.hero-accent {
  color: var(--green-m);
  font-style: italic;
}
.hero-sub {
  max-width: 36rem;
  font-size: 1rem;
  line-height: 1.72;
  color: var(--ink-40);
  margin: 0 0 32px;
}
.hero-stat-row {
  display: flex;
  align-items: center;
  gap: 0;
  padding: 18px 22px;
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: var(--sh-xs);
  width: fit-content;
  margin-bottom: 24px;
}
.hero-stat { text-align: center; padding: 0 24px }
.hs-num {
  font-family: var(--ff-display);
  font-size: 2rem;
  font-weight: 700;
  color: var(--ink);
  line-height: 1;
}
.hs-lbl {
  font-size: .7rem;
  font-weight: 600;
  color: var(--ink-20);
  margin-top: 4px;
  text-transform: uppercase;
  letter-spacing: .06em;
}
.hero-stat-div { width: 1px; height: 44px; background: var(--border); flex-shrink: 0 }
.hero-path-row { display: flex; flex-wrap: wrap; gap: 10px }
.path-chip {
  height: 36px;
  padding: 0 16px;
  border-radius: 999px;
  border: 1px solid var(--border-m);
  background: var(--white);
  font-size: .82rem;
  font-weight: 600;
  color: var(--ink-60);
  cursor: pointer;
  transition: all .18s;
}
.path-chip:hover { border-color: var(--green-bd); color: var(--green-m); background: var(--green-bg) }
.path-chip.active { background: var(--green-m); border-color: var(--green-m); color: var(--white) }

/* Right: AI Panel */
.hero-right {
  background: var(--ink-80);
  border-left: 1px solid rgba(255,255,255,.06);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 40px;
}
.ai-panel {
  width: 100%;
  max-width: 460px;
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 24px;
  padding: 28px;
  backdrop-filter: blur(10px);
}
.ai-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 22px;
}
.ai-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: .76rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: rgba(255,255,255,.45);
}
.ai-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--green-b);
  box-shadow: 0 0 8px rgba(34,197,94,.6);
  animation: ai-pulse 2s ease-in-out infinite;
}
@keyframes ai-pulse {
  0%,100% { box-shadow: 0 0 6px rgba(34,197,94,.5) }
  50%      { box-shadow: 0 0 14px rgba(34,197,94,.9) }
}
.ai-model-badge {
  height: 22px;
  padding: 0 9px;
  border-radius: 999px;
  background: rgba(34,197,94,.15);
  border: 1px solid rgba(34,197,94,.25);
  font-size: .62rem;
  font-weight: 800;
  color: var(--green-b);
  letter-spacing: .06em;
}
.ai-prompt-label {
  font-size: .82rem;
  color: rgba(255,255,255,.5);
  margin: 0 0 12px;
  line-height: 1.5;
}
.ai-input-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 8px;
}
.ai-input {
  height: 48px;
  padding: 0 16px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,.12);
  background: rgba(255,255,255,.06);
  color: var(--white);
  font-family: var(--ff-body);
  font-size: .9rem;
  outline: none;
  transition: border-color .2s;
}
.ai-input::placeholder { color: rgba(255,255,255,.25) }
.ai-input:focus { border-color: rgba(34,197,94,.5); background: rgba(255,255,255,.08) }
.ai-submit {
  height: 48px;
  padding: 0 20px;
  border-radius: 12px;
  border: none;
  background: var(--green-m);
  color: white;
  font-family: var(--ff-body);
  font-size: .88rem;
  font-weight: 700;
  cursor: pointer;
  transition: all .18s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 90px;
}
.ai-submit:hover:not(:disabled) { background: var(--green) }
.ai-submit:disabled { opacity: .5; cursor: not-allowed }
.ai-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg) } }

.ai-error {
  margin-top: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  background: rgba(220,38,38,.15);
  border: 1px solid rgba(220,38,38,.25);
  color: #fca5a5;
  font-size: .78rem;
  line-height: 1.45;
}
.ai-candidates { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 12px; align-items: center }
.ai-candidates-label { font-size: .7rem; color: rgba(255,255,255,.4); font-weight: 600 }
.ai-candidate-btn {
  height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  border: 1px solid rgba(34,197,94,.25);
  background: rgba(34,197,94,.1);
  color: var(--green-b);
  font-size: .74rem;
  font-weight: 700;
  cursor: pointer;
  transition: all .15s;
}
.ai-candidate-btn:hover { background: rgba(34,197,94,.2) }

/* Result */
.ai-result {
  display: grid;
  grid-template-columns: 100px 1fr;
  gap: 16px;
  align-items: start;
  margin-top: 22px;
  padding: 18px;
  border-radius: 18px;
  background: rgba(255,255,255,.05);
  border: 1px solid rgba(255,255,255,.1);
}
.ai-result-score-col { display: flex; flex-direction: column; align-items: center; gap: 8px }
.ai-score-ring {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ring-svg { position: absolute; inset: 0; width: 100%; height: 100% }
.ring-fill { transition: stroke-dasharray .8s cubic-bezier(.4,0,.2,1) }
.ring-number {
  position: relative;
  z-index: 1;
  font-family: var(--ff-display);
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--white);
  line-height: 1;
}
.score-verdict {
  font-size: .7rem;
  font-weight: 800;
  letter-spacing: .1em;
  text-transform: uppercase;
}
.score-good  .score-verdict, .score-good.score-verdict  { color: #4ade80 }
.score-mid   .score-verdict, .score-mid.score-verdict   { color: #fbbf24 }
.score-low   .score-verdict, .score-low.score-verdict   { color: #f87171 }

.ai-matched-food {
  font-size: 1rem;
  font-weight: 700;
  color: var(--white);
  margin-bottom: 6px;
  text-transform: capitalize;
}
.ai-category-pill {
  display: inline-flex;
  height: 20px;
  padding: 0 8px;
  border-radius: 999px;
  background: rgba(255,255,255,.08);
  font-size: .65rem;
  font-weight: 700;
  color: rgba(255,255,255,.5);
  align-items: center;
  margin-bottom: 12px;
}
.ai-score-bar-block { margin-bottom: 12px }
.ai-bar-track { height: 7px; border-radius: 999px; background: rgba(255,255,255,.1); overflow: hidden; margin-bottom: 4px }
.ai-bar-fill { height: 100%; border-radius: 999px; transition: width .8s cubic-bezier(.4,0,.2,1) }
.ai-bar-labels { display: flex; justify-content: space-between; font-size: .58rem; color: rgba(255,255,255,.3); font-family: var(--ff-mono) }
.ai-tip-block {
  font-size: .78rem;
  line-height: 1.55;
  color: rgba(255,255,255,.55);
  margin-bottom: 12px;
}
.ai-clear-btn {
  height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,.15);
  background: transparent;
  color: rgba(255,255,255,.5);
  font-size: .72rem;
  font-weight: 700;
  cursor: pointer;
  transition: all .15s;
}
.ai-clear-btn:hover { background: rgba(255,255,255,.07); color: rgba(255,255,255,.8) }

/* Idle examples */
.ai-idle-examples { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 18px; align-items: center }
.idle-label { font-size: .7rem; color: rgba(255,255,255,.3); font-weight: 600 }
.idle-chip {
  height: 26px;
  padding: 0 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,.1);
  background: rgba(255,255,255,.04);
  color: rgba(255,255,255,.45);
  font-size: .72rem;
  font-weight: 600;
  cursor: pointer;
  transition: all .15s;
}
.idle-chip:hover { background: rgba(255,255,255,.08); color: rgba(255,255,255,.8); border-color: rgba(255,255,255,.2) }

/* ─── FILTER RAIL ─────────────────────────────────────────────────────────── */
.filter-section {
  background: var(--white);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 68px;
  z-index: 50;
  box-shadow: 0 2px 12px rgba(0,0,0,.04);
}
.filter-wrap { max-width: 1380px; margin: 0 auto; padding: 0 40px }
.filter-rail {
  display: flex;
  align-items: center;
  gap: 0;
  overflow-x: auto;
  scrollbar-width: none;
  padding: 14px 0;
}
.filter-rail::-webkit-scrollbar { display: none }
.filter-group { display: flex; align-items: center; gap: 10px; flex-shrink: 0 }
.fg-label {
  font-size: .66rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: var(--ink-20);
  white-space: nowrap;
}
.fg-chips { display: flex; gap: 6px }
.fg-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 0 13px;
  border-radius: 999px;
  border: 1px solid var(--border-m);
  background: var(--ink-05);
  font-size: .78rem;
  font-weight: 600;
  color: var(--ink-60);
  cursor: pointer;
  transition: all .15s;
  white-space: nowrap;
}
.fg-chip:hover { background: var(--ink-10); color: var(--ink) }
.fg-chip.active { background: var(--ink); border-color: var(--ink); color: var(--white) }
.chip-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}
.dot-all     { background: var(--ink-20) }
.dot-meal    { background: var(--green-m) }
.dot-snack   { background: var(--amber) }
.dot-lunchbox{ background: var(--blue) }

.filter-divider {
  width: 1px;
  height: 28px;
  background: var(--border);
  margin: 0 16px;
  flex-shrink: 0;
}
.reset-pill {
  display: flex;
  align-items: center;
  gap: 5px;
  height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  border: 1px solid var(--border-m);
  background: var(--white);
  font-size: .72rem;
  font-weight: 700;
  color: var(--ink-40);
  cursor: pointer;
  margin-left: 12px;
  flex-shrink: 0;
  transition: all .15s;
}
.reset-pill:hover { background: var(--red-bg); color: var(--red); border-color: rgba(220,38,38,.2) }
.result-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 0;
  border-top: 1px solid var(--border);
}
.rb-count { display: flex; align-items: baseline; gap: 5px }
.rb-num {
  font-family: var(--ff-display);
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--ink);
}
.rb-lbl { font-size: .76rem; color: var(--ink-40); font-weight: 500 }
.rb-tags { display: flex; gap: 7px }
.rb-tag {
  height: 22px;
  padding: 0 9px;
  border-radius: 999px;
  background: var(--green-bg);
  border: 1px solid var(--green-bd);
  font-size: .66rem;
  font-weight: 700;
  color: var(--green-m);
  display: inline-flex;
  align-items: center;
}

/* ─── EMPTY ───────────────────────────────────────────────────────────────── */
.empty-section { padding: 80px 40px; text-align: center }
.empty-wrap { max-width: 440px; margin: 0 auto }
.empty-icon { font-size: 3.5rem; margin-bottom: 20px }
.empty-wrap h2 {
  font-family: var(--ff-display);
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--ink);
  margin: 0 0 10px;
}
.empty-wrap p { color: var(--ink-40); margin: 0 0 22px }
.reset-btn {
  height: 44px;
  padding: 0 22px;
  border-radius: 12px;
  border: none;
  background: var(--ink);
  color: var(--white);
  font-size: .88rem;
  font-weight: 700;
  cursor: pointer;
  transition: all .18s;
}
.reset-btn:hover { background: var(--ink-80); transform: translateY(-1px) }

/* ─── CONTENT SECTION ────────────────────────────────────────────────────── */
.content-section { padding: 40px 0 80px }
.content-wrap { max-width: 1380px; margin: 0 auto; padding: 0 40px; display: flex; flex-direction: column; gap: 48px }

/* Featured banner */
.featured-banner {
  background: var(--green-bg);
  border: 1.5px solid var(--green-bd);
  border-radius: 24px;
  padding: 24px 28px;
  box-shadow: 0 4px 20px rgba(21,128,61,.08);
}
.fb-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: .66rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: var(--green-m);
  margin-bottom: 16px;
}
.fb-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}
.fb-module-pill {
  display: inline-flex;
  height: 22px;
  padding: 0 10px;
  border-radius: 999px;
  font-size: .65rem;
  font-weight: 700;
  margin-bottom: 10px;
}
.pill-meal    { background: var(--green-bg); color: var(--green-m); border: 1px solid var(--green-bd) }
.pill-snack   { background: var(--amber-bg); color: var(--amber);   border: 1px solid var(--amber-bd) }
.pill-lunchbox{ background: var(--blue-bg);  color: var(--blue);    border: 1px solid var(--blue-bd)  }
.fb-title {
  font-family: var(--ff-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--ink);
  letter-spacing: -.02em;
  margin: 0 0 8px;
  line-height: 1.15;
}
.fb-reason { font-size: .85rem; color: var(--ink-40); margin: 0; line-height: 1.6 }
.fb-right { display: flex; flex-direction: column; align-items: flex-end; gap: 10px; flex-shrink: 0 }
.fb-effort-chip {
  height: 26px;
  padding: 0 10px;
  border-radius: 999px;
  background: var(--white);
  border: 1px solid var(--border-m);
  font-size: .72rem;
  font-weight: 700;
  color: var(--ink-40);
  display: inline-flex;
  align-items: center;
}
.fb-expand-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 38px;
  padding: 0 16px;
  border-radius: 10px;
  border: 1px solid var(--green-bd);
  background: var(--white);
  color: var(--green-m);
  font-size: .82rem;
  font-weight: 700;
  cursor: pointer;
  transition: all .15s;
}
.fb-expand-btn:hover { background: var(--green-bg) }
.fb-expanded { margin-top: 20px; padding-top: 20px; border-top: 1px solid var(--green-bd) }

/* Tool groups */
.tool-group {}
.tg-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 14px;
  border-bottom: 2px solid var(--border);
  margin-bottom: 16px;
}
.tg-header-left { display: flex; align-items: center; gap: 12px }
.tg-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0 }
.tg-title {
  font-family: var(--ff-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--ink);
  letter-spacing: -.02em;
  margin: 0;
}
.tg-count {
  height: 24px;
  min-width: 24px;
  border-radius: 999px;
  padding: 0 8px;
  background: var(--ink-05);
  border: 1px solid var(--border-m);
  font-family: var(--ff-mono);
  font-size: .7rem;
  font-weight: 700;
  color: var(--ink-40);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.tg-toggle {
  height: 32px;
  padding: 0 14px;
  border-radius: 999px;
  border: 1px solid var(--border-m);
  background: var(--white);
  font-size: .78rem;
  font-weight: 700;
  color: var(--ink-40);
  cursor: pointer;
  transition: all .15s;
}
.tg-toggle:hover { color: var(--ink); background: var(--ink-05) }

/* Preview strip (collapsed) */
.tg-preview { display: flex; flex-direction: column; gap: 4px }
.preview-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-radius: 12px;
  background: var(--white);
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all .15s;
  gap: 12px;
}
.preview-row:hover { border-color: var(--border-m); box-shadow: var(--sh-xs); transform: translateX(3px) }
.preview-row.featured { border-color: var(--green-bd); background: var(--green-bg) }
.pr-left { display: flex; align-items: center; gap: 10px; min-width: 0 }
.pr-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0 }
.pr-title { font-size: .88rem; font-weight: 600; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis }
.pr-right { display: flex; align-items: center; gap: 10px; flex-shrink: 0 }
.pr-effort { font-size: .72rem; color: var(--ink-20); font-weight: 600; font-family: var(--ff-mono) }
.pr-arrow { color: var(--ink-20) }

/* Card grid (expanded) */
.tg-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.tool-card {
  background: var(--white);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 0;
  box-shadow: var(--sh-xs);
  transition: box-shadow .2s, transform .2s;
}
.tool-card:hover { box-shadow: var(--sh-sm) }
.tc-meal     { border-top: 3px solid var(--green-m) }
.tc-snack    { border-top: 3px solid var(--amber) }
.tc-lunchbox { border-top: 3px solid var(--blue) }
.tc-featured { box-shadow: 0 0 0 2px rgba(21,128,61,.15), var(--sh-sm) }
.tc-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  cursor: pointer;
}
.tc-head-left { display: flex; align-items: center; gap: 8px }
.tc-badge {
  height: 20px;
  padding: 0 8px;
  border-radius: 999px;
  font-size: .62rem;
  font-weight: 800;
  display: inline-flex;
  align-items: center;
  text-transform: uppercase;
  letter-spacing: .06em;
}
.badge-meal     { background: var(--green-bg); color: var(--green-m) }
.badge-snack    { background: var(--amber-bg); color: var(--amber) }
.badge-lunchbox { background: var(--blue-bg);  color: var(--blue) }
.tc-star { font-size: .66rem; font-weight: 800; color: var(--green-m) }
.tc-time { font-family: var(--ff-mono); font-size: .66rem; color: var(--ink-20); font-weight: 700 }
.tc-title {
  font-family: var(--ff-display);
  font-size: 1.08rem;
  font-weight: 700;
  color: var(--ink);
  line-height: 1.2;
  letter-spacing: -.01em;
  margin: 0 0 12px;
  cursor: pointer;
}
.tc-title:hover { color: var(--green-m) }
.tc-pills { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px }
.tc-pill {
  height: 20px;
  padding: 0 8px;
  border-radius: 999px;
  background: var(--ink-05);
  border: 1px solid var(--border);
  font-size: .64rem;
  font-weight: 700;
  color: var(--ink-60);
  display: inline-flex;
  align-items: center;
}
.tc-body { padding-top: 16px; border-top: 1px solid var(--border) }
.tc-toggle-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: auto;
  padding-top: 14px;
  height: 28px;
  background: none;
  border: none;
  font-size: .76rem;
  font-weight: 700;
  color: var(--ink-40);
  cursor: pointer;
  transition: color .15s;
  padding-left: 0;
}
.tc-toggle-btn:hover { color: var(--green-m) }

/* ─── EXPANDED CONTENT (shared by inline components) ─────────────────────── */
:deep(.expanded-body) { display: flex; flex-direction: column; gap: 14px }
:deep(.exp-summary) { font-size: .84rem; color: var(--ink-40); line-height: 1.7; margin: 0 }
:deep(.exp-row) { display: grid; grid-template-columns: 1fr 1fr; gap: 14px }
:deep(.exp-block) {}
:deep(.exp-label) {
  font-size: .62rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: var(--ink-20);
  margin-bottom: 6px;
}
:deep(.exp-val) { font-size: .84rem; font-weight: 600; color: var(--ink) }
:deep(.exp-pills) { display: flex; flex-wrap: wrap; gap: 6px }
:deep(.exp-pill) {
  height: 20px;
  padding: 0 8px;
  border-radius: 999px;
  background: var(--ink-05);
  border: 1px solid var(--border);
  font-size: .64rem;
  font-weight: 700;
  color: var(--ink-60);
  display: inline-flex;
  align-items: center;
}
:deep(.exp-section) {}
:deep(.exp-list) {
  margin: 0;
  padding-left: 18px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: .82rem;
  color: var(--ink-60);
  line-height: 1.55;
}
:deep(.exp-list.ordered) { padding-left: 20px }
:deep(.exp-tip) {
  padding: 12px 14px;
  border-radius: 12px;
  background: var(--green-bg);
  border: 1px solid var(--green-bd);
  font-size: .8rem;
  color: var(--green);
  line-height: 1.55;
}
:deep(.exp-move) {
  padding: 12px 14px;
  border-radius: 12px;
  background: var(--ink-05);
  border: 1px solid var(--border);
}
:deep(.exp-move p) { margin: 6px 0 0; font-size: .8rem; color: var(--ink-40); line-height: 1.6 }
:deep(.exp-pair-grid) { display: grid; grid-template-columns: 1fr auto 1fr; gap: 10px; align-items: center }
:deep(.exp-pair-box) { padding: 12px 14px; border-radius: 14px; border: 1px solid var(--border) }
:deep(.exp-pair-box.left)  { background: var(--ink-05) }
:deep(.exp-pair-box.right) { background: var(--green-bg); border-color: var(--green-bd) }
:deep(.exp-pair-box strong) { display: block; font-size: .86rem; color: var(--ink); line-height: 1.4 }
:deep(.exp-plus) { font-family: var(--ff-display); font-size: 1.4rem; color: var(--ink-20); text-align: center }
:deep(.exp-lunchbox) { display: flex; flex-direction: column; gap: 8px }
:deep(.exp-lb-row) { padding: 10px 14px; border-radius: 12px; border: 1px solid var(--border) }
:deep(.exp-lb-row.base)  { background: var(--ink-05) }
:deep(.exp-lb-row.fresh) { background: var(--green-bg); border-color: var(--green-bd) }
:deep(.exp-lb-row.extra) { background: var(--blue-bg);  border-color: var(--blue-bd) }
:deep(.exp-lb-row strong) { display: block; font-size: .86rem; color: var(--ink); margin-top: 4px }

/* ─── TRANSITIONS ─────────────────────────────────────────────────────────── */
.result-fade-enter-active { transition: all .4s cubic-bezier(.4,0,.2,1) }
.result-fade-enter-from   { opacity: 0; transform: translateY(10px) }
.expand-enter-active, .expand-leave-active { transition: all .25s ease; overflow: hidden }
.expand-enter-from, .expand-leave-to       { opacity: 0; max-height: 0 }
.expand-enter-to, .expand-leave-from       { opacity: 1; max-height: 600px }
.tc-expand-enter-active, .tc-expand-leave-active { transition: all .22s ease; overflow: hidden }
.tc-expand-enter-from, .tc-expand-leave-to       { opacity: 0; max-height: 0 }
.tc-expand-enter-to, .tc-expand-leave-from       { opacity: 1; max-height: 800px }

/* ─── RESPONSIVE ──────────────────────────────────────────────────────────── */
@media (max-width: 1100px) {
  .hero-section { grid-template-columns: 1fr }
  .hero-right { border-left: none; border-top: 1px solid rgba(255,255,255,.06) }
  .tg-grid { grid-template-columns: repeat(2, 1fr) }
}
@media (max-width: 860px) {
  .hero-left, .hero-right { padding: 40px 24px }
  .header-inner, .filter-wrap, .content-wrap { padding-left: 24px; padding-right: 24px }
  .tg-grid { grid-template-columns: 1fr }
  .fb-content { flex-direction: column }
  :deep(.exp-row)      { grid-template-columns: 1fr }
  :deep(.exp-pair-grid){ grid-template-columns: 1fr }
  :deep(.exp-plus)     { display: none }
}
@media (max-width: 640px) {
  .nav { display: none }
  .hero-stat-row { flex-wrap: wrap }
  .hero-stat-div { display: none }
  .hero-stat { padding: 0 16px }
  .fb-right { width: 100%; flex-direction: row; justify-content: space-between }
}
</style>