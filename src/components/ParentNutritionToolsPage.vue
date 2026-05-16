<template>
  <div class="nutrition-page">
    <div class="page-bg" aria-hidden="true">
      <img
        class="page-bg__img"
        src="https://images.unsplash.com/photo-1543353071-873f17a7a088?auto=format&fit=crop&w=2400&q=90"
        alt=""
      />
      <div class="page-bg__overlay"></div>
      <div class="page-bg__grain"></div>
    </div>

    <header class="header" :class="{ scrolled: isScrolled }">
      <div class="header-inner">
        <RouterLink to="/" class="logo">
          <div class="logo-icon">
            <svg viewBox="0 0 36 36" fill="none">
              <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.5" />
              <path
                d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z"
                fill="currentColor"
              />
            </svg>
          </div>
          <span>HealthyKids</span>
        </RouterLink>

        <nav class="nav" aria-label="Nutrition page navigation">
          <RouterLink to="/" class="nav-a">Home</RouterLink>
          <RouterLink to="/parent-dashboard" class="nav-a">Dashboard</RouterLink>
          <RouterLink to="/parent-nutrition-tools" class="nav-a">Nutrition</RouterLink>
          <RouterLink to="/statistics" class="nav-a">Statistics</RouterLink>
          <RouterLink to="/young-person-dashboard" class="nav-a">Kids view</RouterLink>
        </nav>

        <div class="nav-cta">
          <RouterLink to="/parent-quiz" class="nav-link">Retake quiz</RouterLink>
          <RouterLink to="/parent-dashboard" class="nav-btn">
            Back to dashboard
            <svg width="11" height="11" viewBox="0 0 12 12">
              <path
                d="M2 6h8M7 3l3 3-3 3"
                stroke="currentColor"
                stroke-width="1.4"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </RouterLink>
        </div>
      </div>
    </header>

    <main class="page-main">
      <section class="hero-card">
        <div class="hero-copy">
          <p class="eyebrow">
            <span class="eyebrow-dot"></span>
            Nutrition support
          </p>

          <h1>Simple meal ideas for today.</h1>

          <p class="hero-text">
            Browse recipes from your database, filter by what your family needs, and use the food scorer when you want a quick check.
          </p>

          <div class="hero-actions">
            <button
              v-for="shortcut in quickStarts"
              :key="shortcut.id"
              class="quick-chip"
              type="button"
              :class="{ active: selectedCategory === shortcut.category }"
              @click="applyQuickStart(shortcut)"
            >
              {{ shortcut.label }}
            </button>
          </div>

          <div class="summary-row" aria-label="Recipe summary">
            <div>
              <strong>{{ recipeCount }}</strong>
              <span>recipes</span>
            </div>
            <div>
              <strong>{{ cuisineCount }}</strong>
              <span>cuisines</span>
            </div>
            <div>
              <strong>{{ categoryCount }}</strong>
              <span>categories</span>
            </div>
          </div>
        </div>

        <aside class="score-card" aria-label="Food scorer">
          <div class="score-card__head">
            <div>
              <p class="score-kicker">Food scorer</p>
              <h2>Check a food</h2>
            </div>
            <span class="score-status">Live</span>
          </div>

          <p class="score-help">Type one food and get a quick health score.</p>

          <div class="score-input-row">
            <input
              v-model="foodInput"
              type="text"
              placeholder="e.g. banana, yoghurt, chips"
              @keyup.enter="submitFoodPrediction"
              @input="clearPrediction"
            />
            <button
              type="button"
              :disabled="foodPredictionLoading || !foodInput.trim()"
              @click="submitFoodPrediction"
            >
              <span v-if="!foodPredictionLoading">Score</span>
              <span v-else class="spinner"></span>
            </button>
          </div>

          <p v-if="foodPredictionError" class="score-error">
            {{ foodPredictionError }}
          </p>

          <div v-if="foodPredictionCandidates.length" class="candidate-row">
            <span>Did you mean?</span>
            <button
              v-for="candidate in foodPredictionCandidates"
              :key="candidate"
              type="button"
              @click="chooseFoodCandidate(candidate)"
            >
              {{ candidate }}
            </button>
          </div>

          <Transition name="fade-up">
            <div v-if="foodPredictionResult" class="score-result">
              <div
                class="score-ring"
                :style="{ '--score-color': scoreColor(foodPredictionResult.health_score) }"
              >
                <svg viewBox="0 0 90 90" aria-hidden="true">
                  <circle cx="45" cy="45" r="35" class="ring-bg" />
                  <circle
                    cx="45"
                    cy="45"
                    r="35"
                    class="ring-fill"
                    :stroke-dasharray="`${scoreArc(foodPredictionResult.health_score)} 220`"
                  />
                </svg>
                <strong>{{ Math.round(foodPredictionResult.health_score) }}</strong>
              </div>

              <div class="score-detail">
                <h3>{{ foodPredictionResult.matched_food }}</h3>
                <span :class="['verdict-pill', scoreClass(foodPredictionResult.health_score)]">
                  {{ scoreVerdict(foodPredictionResult.health_score) }}
                </span>
                <p>{{ scoreTip(foodPredictionResult.health_score, foodPredictionResult.matched_food) }}</p>
                <button type="button" class="clear-score" @click="clearAndReset">
                  Score another food
                </button>
              </div>
            </div>
          </Transition>

          <div v-if="!foodPredictionResult && !foodPredictionLoading" class="example-row">
            <span>Try:</span>
            <button
              v-for="food in exampleFoods"
              :key="food"
              type="button"
              @click="tryExample(food)"
            >
              {{ food }}
            </button>
          </div>
        </aside>
      </section>

      <section class="controls-card" aria-label="Recipe filters">
        <div class="search-box">
          <label for="recipe-search">Find a recipe</label>
          <input
            id="recipe-search"
            v-model.trim="searchQuery"
            type="search"
            placeholder="Search by recipe, ingredient, or cuisine"
          />
        </div>

        <div class="filter-grid">
          <div class="filter-field">
            <label for="category-filter">Category</label>
            <select id="category-filter" v-model="selectedCategory">
              <option value="all">All categories</option>
              <option
                v-for="category in categoryOptions"
                :key="category"
                :value="category"
              >
                {{ category }}
              </option>
            </select>
          </div>

          <div class="filter-field">
            <label for="cuisine-filter">Cuisine</label>
            <select id="cuisine-filter" v-model="selectedCuisine">
              <option value="all">All cuisines</option>
              <option
                v-for="cuisine in cuisineOptions"
                :key="cuisine"
                :value="cuisine"
              >
                {{ cuisine }}
              </option>
            </select>
          </div>

          <div class="filter-field">
            <label for="need-filter">Family need</label>
            <select id="need-filter" v-model="selectedNeed">
              <option value="all">Any need</option>
              <option value="protein">Protein</option>
              <option value="fruit-veg">Fruit & veg</option>
              <option value="lunchbox-safe">Lunchbox friendly</option>
              <option value="quick">Quick option</option>
            </select>
          </div>
        </div>

        <div class="controls-footer">
          <p>
            Showing <strong>{{ filteredRecipes.length }}</strong> of
            <strong>{{ recipeCount }}</strong> recipes
          </p>
          <button v-if="hasActiveFilters" type="button" @click="resetFilters">
            Clear filters
          </button>
        </div>
      </section>

      <section v-if="nutritionLoading" class="state-card">
        <div class="state-icon"><span>&#x1F957;</span></div>
        <h2>Loading recipe ideas...</h2>
        <p>Fetching nutrition options from your database.</p>
      </section>

      <section v-else-if="nutritionError" class="state-card error-state">
        <div class="state-icon"><span>&#9888;</span></div>
        <h2>Could not load recipes</h2>
        <p>{{ nutritionError }}</p>
        <button type="button" @click="fetchRecipes">Try again</button>
      </section>

      <section v-else-if="filteredRecipes.length === 0" class="state-card">
        <div class="state-icon"><span>&#x1F50E;</span></div>
        <h2>No recipes match this search</h2>
        <p>Try clearing one filter or searching for a broader ingredient.</p>
        <button type="button" @click="resetFilters">Show all recipes</button>
      </section>

      <section v-else class="recipe-section">
        <div class="section-heading">
          <div>
            <p class="eyebrow compact">Database recipes</p>
            <h2>Choose one simple idea</h2>
          </div>
          <p>Open a card to see ingredients and steps.</p>
        </div>

        <div class="recipe-grid">
          <article
            v-for="recipe in visibleRecipes"
            :key="recipe.id"
            class="recipe-card"
          >
            <button
              type="button"
              class="recipe-card__top"
              @click="openRecipeModal(recipe)"
            >
              <div class="recipe-main">
                <span class="category-pill">{{ recipe.category || 'Recipe' }}</span>
                <h3>{{ recipe.name }}</h3>
                <p>{{ recipe.summary }}</p>
              </div>

              <span class="expand-icon" aria-hidden="true">+</span>
            </button>

            <div class="recipe-meta">
              <span>{{ recipe.area || 'Family' }}</span>
              <span>{{ recipe.effortLabel }}</span>
              <span>{{ recipe.needLabel }}</span>
            </div>
          </article>
        </div>

        <Teleport to="body">
          <Transition name="recipe-modal-fade">
            <div
              v-if="selectedRecipe"
              class="recipe-modal-backdrop"
              role="dialog"
              aria-modal="true"
              :aria-label="`${selectedRecipe.name} recipe details`"
              @click.self="closeRecipeModal"
            >
              <div class="recipe-modal">
                <button
                  type="button"
                  class="recipe-modal-close"
                  aria-label="Close recipe details"
                  @click="closeRecipeModal"
                >
                  ×
                </button>

                <div class="recipe-modal-head">
                  <span class="category-pill">{{ selectedRecipe.category || 'Recipe' }}</span>

                  <h2>{{ selectedRecipe.name }}</h2>

                  <p>{{ selectedRecipe.summary }}</p>

                  <div class="recipe-modal-meta">
                    <span>{{ selectedRecipe.area || 'Family' }}</span>
                    <span>{{ selectedRecipe.effortLabel }}</span>
                    <span>{{ selectedRecipe.needLabel }}</span>
                  </div>
                </div>

                <div class="recipe-modal-body">
                  <section
                    v-if="selectedRecipe.ingredientsList.length"
                    class="recipe-modal-block"
                  >
                    <h3>Ingredients</h3>
                    <ul>
                      <li
                        v-for="ingredient in selectedRecipe.ingredientsList"
                        :key="ingredient"
                      >
                        {{ ingredient }}
                      </li>
                    </ul>
                  </section>

                  <section
                    v-if="selectedRecipe.stepList.length"
                    class="recipe-modal-block"
                  >
                    <h3>Steps</h3>
                    <ol>
                      <li
                        v-for="step in selectedRecipe.stepList"
                        :key="step"
                      >
                        {{ step }}
                      </li>
                    </ol>
                  </section>

                  <section class="recipe-modal-tip">
                    <strong>Parent tip:</strong>
                    <span>{{ selectedRecipe.parentTip }}</span>
                  </section>
                </div>
              </div>
            </div>
          </Transition>
        </Teleport>

        <div v-if="filteredRecipes.length > visibleLimit" class="load-more-wrap">
          <button type="button" class="load-more" @click="visibleLimit += 12">
            Show more recipes
          </button>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'
import { useFoodHealthPredictor } from '../composables/useFoodHealthPredictor'

const API_BASE = import.meta.env.VITE_NUTRITION_API_BASE_URL

const { state } = useFamilyPlanStore()

const recipes = ref([])
const nutritionLoading = ref(false)
const nutritionError = ref('')

const searchQuery = ref('')
const selectedCategory = ref('all')
const selectedCuisine = ref('all')
const selectedNeed = ref('all')
const selectedRecipe = ref(null)
const visibleLimit = ref(12)
const isScrolled = ref(false)
const foodInput = ref('')

const {
  loading: foodPredictionLoading,
  error: foodPredictionError,
  result: foodPredictionResult,
  candidates: foodPredictionCandidates,
  predictFood,
  clearPrediction,
} = useFoodHealthPredictor()

const exampleFoods = ['banana', 'white bread', 'greek yoghurt', 'milo']

const quickStarts = computed(() => [
  { id: 'all', label: 'All ideas', category: 'all', cuisine: 'all', need: 'all' },
  { id: 'quick', label: 'Quick meals', category: 'all', cuisine: 'all', need: 'quick' },
  { id: 'lunchbox', label: 'Lunchbox friendly', category: 'all', cuisine: 'all', need: 'lunchbox-safe' },
])

const normalisedRecipes = computed(() => recipes.value.map(mapRecipe))

const recipeCount = computed(() => normalisedRecipes.value.length)

const categoryOptions = computed(() => uniqueValues(normalisedRecipes.value.map(recipe => recipe.category)))
const cuisineOptions = computed(() => uniqueValues(normalisedRecipes.value.map(recipe => recipe.area)))
const categoryCount = computed(() => categoryOptions.value.length)
const cuisineCount = computed(() => cuisineOptions.value.length)

const hasActiveFilters = computed(() =>
  searchQuery.value ||
  selectedCategory.value !== 'all' ||
  selectedCuisine.value !== 'all' ||
  selectedNeed.value !== 'all'
)

const filteredRecipes = computed(() => {
  const query = searchQuery.value.toLowerCase().trim()

  return normalisedRecipes.value.filter(recipe => {
    const searchable = `${recipe.name} ${recipe.area} ${recipe.category} ${recipe.ingredients}`.toLowerCase()

    if (query && !searchable.includes(query)) return false
    if (selectedCategory.value !== 'all' && recipe.category !== selectedCategory.value) return false
    if (selectedCuisine.value !== 'all' && recipe.area !== selectedCuisine.value) return false
    if (selectedNeed.value !== 'all' && !recipe.needs.includes(selectedNeed.value)) return false

    return true
  })
})

const visibleRecipes = computed(() => filteredRecipes.value.slice(0, visibleLimit.value))

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  fetchRecipes()
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)

  if (typeof document !== 'undefined') {
    document.body.classList.remove('recipe-modal-open')
  }
})

function onScroll() {
  isScrolled.value = window.scrollY > 40
}

async function fetchRecipes() {
  if (!API_BASE) {
    nutritionError.value = 'Missing VITE_NUTRITION_API_BASE_URL. Add it to your .env file.'
    return
  }

  nutritionLoading.value = true
  nutritionError.value = ''

  try {
    const response = await fetch(`${API_BASE}/recipes`)
    const data = await response.json().catch(() => ({}))

    if (!response.ok) {
      throw new Error(data.error || `Recipe API failed with status ${response.status}`)
    }

    recipes.value = Array.isArray(data) ? data : data.recipes || []
  } catch (error) {
    nutritionError.value = error.message || 'Unable to load recipes from the database.'
  } finally {
    nutritionLoading.value = false
  }
}

function mapRecipe(recipe) {
  const name = recipe.name || recipe.recipe_name || 'Recipe idea'
  const area = recipe.area || recipe.cuisine_area || 'Family'
  const category = recipe.category || 'Meal'
  const ingredients = recipe.ingredients || ''
  const steps = recipe.steps || ''
  const ingredientsList = splitList(ingredients)
  const stepList = splitSteps(steps)
  const needs = detectNeeds({ name, category, ingredients })
  const effort = detectEffort(ingredientsList, stepList)

  return {
    id: recipe.id || `${name}-${area}`,
    name,
    area,
    category,
    ingredients,
    steps,
    ingredientsList,
    stepList,
    needs,
    effort,
    effortLabel: effort === 'quick' ? 'Quick' : effort === 'medium' ? 'Simple' : 'Plan ahead',
    needLabel: needs.includes('protein')
      ? 'Protein'
      : needs.includes('fruit-veg')
        ? 'Fruit & veg'
        : needs.includes('lunchbox-safe')
          ? 'Lunchbox'
          : 'Family friendly',
    summary: buildSummary(area, category, ingredientsList),
    parentTip: buildParentTip(needs, effort),
  }
}

function splitList(value) {
  if (!value) return []

  return String(value)
    .replace(/[\[\]']/g, '')
    .split(/,|\n|;/)
    .map(item => item.trim())
    .filter(Boolean)
    .slice(0, 10)
}

function splitSteps(value) {
  if (!value) return []

  const cleaned = String(value)
    .replace(/\r/g, '')
    .replace(/\s+/g, ' ')
    .trim()

  const splitByNumber = cleaned
    .split(/(?:^|\s)(?:\d+\.|Step \d+:)/i)
    .map(step => step.trim())
    .filter(Boolean)

  const splitBySentence = cleaned
    .split(/\.\s+/)
    .map(step => step.trim())
    .filter(Boolean)

  return (splitByNumber.length > 1 ? splitByNumber : splitBySentence)
    .map(step => (step.endsWith('.') ? step : `${step}.`))
    .slice(0, 6)
}

function detectNeeds(recipe) {
  const text = `${recipe.name} ${recipe.category} ${recipe.ingredients}`.toLowerCase()
  const needs = []

  if (/chicken|egg|paneer|tofu|soy|fish|beans|lentil|dal|yoghurt|yogurt|beef|mutton/.test(text)) {
    needs.push('protein')
  }

  if (/vegetable|fruit|spinach|palak|carrot|peas|matar|tomato|lettuce|capsicum|beans|broccoli/.test(text)) {
    needs.push('fruit-veg')
  }

  if (/wrap|sandwich|roll|burrito|dosa|idli|rice|pasta|noodle/.test(text)) {
    needs.push('lunchbox-safe')
  }

  if (/quick|easy|simple|bread|toast|rice|egg/.test(text)) {
    needs.push('quick')
  }

  return needs.length ? [...new Set(needs)] : ['family-friendly']
}

function detectEffort(ingredientsList, stepList) {
  if (ingredientsList.length <= 5 && stepList.length <= 4) return 'quick'
  if (ingredientsList.length <= 9 && stepList.length <= 6) return 'medium'
  return 'plan-ahead'
}

function buildSummary(area, category, ingredientsList) {
  const ingredientsText = ingredientsList.slice(0, 3).join(', ')
  return `${area} ${category.toLowerCase()} idea${ingredientsText ? ` with ${ingredientsText}` : ''}.`
}

function buildParentTip(needs, effort) {
  if (needs.includes('lunchbox-safe')) return 'Pack sauces or wet ingredients separately so the meal stays fresh.'
  if (needs.includes('protein')) return 'Serve a small portion first, then offer more if your child is still hungry.'
  if (needs.includes('fruit-veg')) return 'Keep one familiar item on the plate to make the new food feel less overwhelming.'
  if (effort === 'plan-ahead') return 'Prepare one ingredient earlier in the day to reduce pressure at mealtime.'
  return 'Keep the first attempt simple and repeat it before adding more changes.'
}

function uniqueValues(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b))
}

function applyQuickStart(shortcut) {
  selectedCategory.value = shortcut.category
  selectedCuisine.value = shortcut.cuisine
  selectedNeed.value = shortcut.need
  searchQuery.value = ''
  visibleLimit.value = 12
}

function resetFilters() {
  searchQuery.value = ''
  selectedCategory.value = 'all'
  selectedCuisine.value = 'all'
  selectedNeed.value = 'all'
  selectedRecipe.value = null
  visibleLimit.value = 12

  if (typeof document !== 'undefined') {
    document.body.classList.remove('recipe-modal-open')
  }
}

function openRecipeModal(recipe) {
  selectedRecipe.value = recipe

  if (typeof document !== 'undefined') {
    document.body.classList.add('recipe-modal-open')
  }
}

function closeRecipeModal() {
  selectedRecipe.value = null

  if (typeof document !== 'undefined') {
    document.body.classList.remove('recipe-modal-open')
  }
}

function submitFoodPrediction() {
  if (foodInput.value.trim()) predictFood(foodInput.value.trim())
}

function chooseFoodCandidate(candidate) {
  foodInput.value = candidate
  predictFood(candidate)
}

function tryExample(food) {
  foodInput.value = food
  predictFood(food)
}

function clearAndReset() {
  foodInput.value = ''
  clearPrediction()
}

function scoreClass(score) {
  if (score >= 70) return 'score-good'
  if (score >= 40) return 'score-mid'
  return 'score-low'
}

function scoreColor(score) {
  if (score >= 70) return '#327c70'
  if (score >= 40) return '#e6865f'
  return '#dc2626'
}

function scoreArc(score) {
  return Math.max(0, Math.min(100, score)) * 2.2
}

function scoreVerdict(score) {
  if (score >= 80) return 'Excellent'
  if (score >= 65) return 'Good'
  if (score >= 45) return 'Okay'
  if (score >= 25) return 'Limited'
  return 'Low'
}

function scoreTip(score, food) {
  if (score >= 70) return `${food} is a strong everyday option.`
  if (score >= 40) return `${food} can work sometimes. Pair it with fruit, vegetables, protein, or water.`
  return `${food} is better kept as an occasional treat rather than a regular option.`
}
</script>
