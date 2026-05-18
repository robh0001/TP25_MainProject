<!--
  ParentNutritionToolsPage.vue

  Creates the HealthyKids nutrition tools page. Parents can browse recipes, filter meal ideas,
  open recipe details, and score foods using the food health predictor.

  API requirement:
  - Requires VITE_NUTRITION_API_BASE_URL.
  - Uses GET /recipes to load recipe data.
  - Food scoring is handled by useFoodHealthPredictor.

  Accessibility:
  - Uses aria-labels, aria-live, role="alert", role="status", and role="dialog".
  - Uses data-hover-read-text for hover-to-read support.
  - Marks decorative images, icons, and SVGs as aria-hidden where appropriate.
-->
  
<template>
  <div class="nutrition-page">
    <!-- Decorative background image and overlay layers -->
    <div class="page-bg" aria-hidden="true">
      <img
        class="page-bg__img"
        src="https://images.unsplash.com/photo-1543353071-873f17a7a088?auto=format&fit=crop&w=2400&q=90"
        alt=""
        aria-hidden="true"
      />
      <div class="page-bg__overlay"></div>
      <div class="page-bg__grain"></div>
    </div>

    <!-- Page header with logo, navigation, and dashboard actions -->
    <header class="header" :class="{ scrolled: isScrolled }" aria-label="HealthyKids nutrition header">
      <div class="header-inner">
        <!-- HealthyKids logo link -->
        <RouterLink
          to="/"
          class="logo"
          aria-label="Go to HealthyKids home page"
          data-hover-read-text="Go to HealthyKids home page"
        >
          <div class="logo-icon" aria-hidden="true">
            <svg viewBox="0 0 36 36" fill="none" focusable="false">
              <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.5" />
              <path
                d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z"
                fill="currentColor"
              />
            </svg>
          </div>
          <span>HealthyKids</span>
        </RouterLink>

        <!-- Main navigation links -->
        <nav class="nav" aria-label="Nutrition page navigation">
          <RouterLink to="/" class="nav-a" data-hover-read-text="Go to home page">
            Home
          </RouterLink>

          <RouterLink to="/parent-dashboard" class="nav-a" data-hover-read-text="Go to parent dashboard">
            Dashboard
          </RouterLink>

          <RouterLink
            to="/parent-nutrition-tools"
            class="nav-a"
            aria-current="page"
            data-hover-read-text="Current page. Nutrition."
          >
            Nutrition
          </RouterLink>

          <RouterLink to="/statistics" class="nav-a" data-hover-read-text="Go to statistics page">
            Statistics
          </RouterLink>

          <RouterLink to="/young-person-dashboard" class="nav-a" data-hover-read-text="Go to kids view">
            Kids view
          </RouterLink>
        </nav>

        <!-- Header call-to-action links -->
        <div class="nav-cta">
          <RouterLink
            to="/parent-quiz"
            class="nav-link"
            data-hover-read-text="Retake the parent quiz"
          >
            Retake quiz
          </RouterLink>

          <RouterLink
            to="/parent-dashboard"
            class="nav-btn"
            data-hover-read-text="Back to dashboard"
          >
            Back to dashboard
            <svg aria-hidden="true" width="11" height="11" viewBox="0 0 12 12">
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

    <!-- Main nutrition page content -->
    <main
      id="main-content"
      class="page-main"
      aria-labelledby="nutrition-page-title"
      aria-describedby="nutrition-page-description"
    >
      <!-- Hero section with quick filters and food scorer -->
      <section class="hero-card" aria-label="Nutrition tools overview">
        <div class="hero-copy">
          <!-- Small section label -->
          <p class="eyebrow" data-hover-read-text="Nutrition support">
            <span class="eyebrow-dot" aria-hidden="true"></span>
            Nutrition support
          </p>

          <!-- Main page heading -->
          <h1 id="nutrition-page-title" data-hover-read-text="Simple meal ideas for today.">
            Simple meal ideas for today.
          </h1>

          <!-- Page description -->
          <p
            id="nutrition-page-description"
            class="hero-text"
            data-hover-read-text="Browse recipes from your database, filter by what your family needs, and use the food scorer when you want a quick check."
          >
            Browse recipes from your database, filter by what your family needs, and use the food scorer when you want a quick check.
          </p>

          <!-- Quick filter chips -->
          <div class="hero-actions" role="group" aria-label="Quick recipe filters">
            <button
              v-for="shortcut in quickStarts"
              :key="shortcut.id"
              class="quick-chip"
              type="button"
              :class="{ active: selectedCategory === shortcut.category && selectedNeed === shortcut.need }"
              :aria-pressed="selectedCategory === shortcut.category && selectedNeed === shortcut.need ? 'true' : 'false'"
              :data-hover-read-text="`${shortcut.label}. ${selectedCategory === shortcut.category && selectedNeed === shortcut.need ? 'Selected' : 'Not selected'}. Click to apply this recipe filter.`"
              @click="applyQuickStart(shortcut)"
            >
              {{ shortcut.label }}
            </button>
          </div>

          <!-- Recipe summary counts -->
          <div
            class="summary-row"
            aria-label="Recipe summary"
            :data-hover-read-text="`${recipeCount} recipes. ${cuisineCount} cuisines. ${categoryCount} categories.`"
          >
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

        <!-- Food scorer card -->
        <aside
          class="score-card"
          aria-labelledby="food-scorer-title"
          aria-describedby="food-scorer-description"
        >
          <div class="score-card__head">
            <div>
              <p class="score-kicker">Food scorer</p>
              <h2 id="food-scorer-title">Check a food</h2>
            </div>
          </div>

          <p id="food-scorer-description" class="score-help">
            Type one food and get a quick health score.
          </p>

          <!-- Food scorer input and submit button -->
          <div class="score-input-row">
            <div class="score-input-wrap">
              <label for="food-score-input" class="nutrition-sr-only">Food to score</label>
              <input
                id="food-score-input"
                v-model="foodInput"
                type="text"
                placeholder="e.g. banana or yoghurt"
                autocomplete="off"
                aria-describedby="food-score-help"
                data-hover-read-text="Food scorer input. Type one food, for example banana or yoghurt."
                @keyup.enter="submitFoodPrediction"
                @input="clearPrediction"
              />
              <p id="food-score-help" class="nutrition-sr-only">
                Enter one food name and press Score to receive a health score.
              </p>
            </div>

            <button
              type="button"
              :disabled="foodPredictionLoading || !foodInput.trim()"
              :aria-busy="foodPredictionLoading ? 'true' : 'false'"
              :aria-disabled="foodPredictionLoading || !foodInput.trim() ? 'true' : 'false'"
              :data-hover-read-text="foodPredictionLoading ? 'Scoring food. Please wait.' : 'Score this food.'"
              @click="submitFoodPrediction"
            >
              <span v-if="!foodPredictionLoading">Score</span>
              <span v-else class="spinner" aria-hidden="true"></span>
            </button>
          </div>

          <!-- Food scorer error message -->
          <p
            v-if="foodPredictionError"
            class="score-error"
            role="alert"
            aria-live="assertive"
            :data-hover-read-text="foodPredictionError"
          >
            {{ foodPredictionError }}
          </p>

          <!-- Suggested food matches -->
          <div
            v-if="foodPredictionCandidates.length"
            class="candidate-row"
            role="group"
            aria-label="Suggested food matches"
          >
            <span>Did you mean?</span>
            <button
              v-for="candidate in foodPredictionCandidates"
              :key="candidate"
              type="button"
              :data-hover-read-text="`Did you mean ${candidate}? Click to score ${candidate}.`"
              @click="chooseFoodCandidate(candidate)"
            >
              {{ candidate }}
            </button>
          </div>

          <!-- Food score result -->
          <Transition name="fade-up">
            <div
              v-if="foodPredictionResult"
              class="score-result"
              role="status"
              aria-live="polite"
              :data-hover-read-text="getFoodScoreReadableText(foodPredictionResult)"
            >
              <div
                class="score-ring"
                :style="{ '--score-color': scoreColor(foodPredictionResult.health_score) }"
                role="img"
                :aria-label="`${foodPredictionResult.matched_food} health score is ${Math.round(foodPredictionResult.health_score)} out of 100`"
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
                <p>{{ scoreTip(foodPredictionResult) }}</p>
                <button
                  type="button"
                  class="clear-score"
                  data-hover-read-text="Score another food"
                  @click="clearAndReset"
                >
                  Score another food
                </button>
              </div>
            </div>
          </Transition>

          <!-- Example foods shown before scoring -->
          <div
            v-if="!foodPredictionResult && !foodPredictionLoading"
            class="example-row"
            role="group"
            aria-label="Example foods"
          >
            <span>Try:</span>
            <button
              v-for="food in exampleFoods"
              :key="food"
              type="button"
              :data-hover-read-text="`Try scoring ${food}`"
              @click="tryExample(food)"
            >
              {{ food }}
            </button>
          </div>
        </aside>
      </section>

      <!-- Search and filter controls -->
      <section
        class="controls-card"
        aria-labelledby="recipe-filter-title"
        aria-describedby="recipe-filter-description"
      >
        <!-- Recipe search field -->
        <div class="search-box">
          <label for="recipe-search">Find a recipe</label>
          <input
            id="recipe-search"
            v-model.trim="searchQuery"
            type="search"
            placeholder="Search by recipe, ingredient, or cuisine"
            autocomplete="off"
            aria-describedby="recipe-search-help"
            data-hover-read-text="Find a recipe. Search by recipe, ingredient, or cuisine."
          />
          <p id="recipe-search-help" class="nutrition-sr-only">
            Type a recipe name, ingredient, or cuisine to filter the recipe list.
          </p>
        </div>

        <!-- Filter dropdowns -->
        <div class="filter-grid">
          <div class="filter-field">
            <label for="category-filter">Category</label>
            <select
              id="category-filter"
              v-model="selectedCategory"
              aria-describedby="category-filter-help"
              data-hover-read-text="Category filter. Choose a recipe category or all categories."
            >
              <option value="all">All categories</option>
              <option v-for="category in categoryOptions" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
            <p id="category-filter-help" class="nutrition-sr-only">
              Filter recipes by category.
            </p>
          </div>

          <div class="filter-field">
            <label for="cuisine-filter">Cuisine</label>
            <select
              id="cuisine-filter"
              v-model="selectedCuisine"
              aria-describedby="cuisine-filter-help"
              data-hover-read-text="Cuisine filter. Choose a cuisine or all cuisines."
            >
              <option value="all">All cuisines</option>
              <option v-for="cuisine in cuisineOptions" :key="cuisine" :value="cuisine">
                {{ cuisine }}
              </option>
            </select>
            <p id="cuisine-filter-help" class="nutrition-sr-only">
              Filter recipes by cuisine.
            </p>
          </div>

          <div class="filter-field">
            <label for="need-filter">Family need</label>
            <select
              id="need-filter"
              v-model="selectedNeed"
              aria-describedby="need-filter-help"
              data-hover-read-text="Family need filter. Choose a family need such as protein, fruit and vegetables, lunchbox friendly, quick option, or any need."
            >
              <option value="all">Any need</option>
              <option value="protein">Protein</option>
              <option value="fruit-veg">Fruit &amp; veg</option>
              <option value="lunchbox-safe">Lunchbox friendly</option>
              <option value="quick">Quick option</option>
            </select>
            <p id="need-filter-help" class="nutrition-sr-only">
              Filter recipes by the family need you want to support.
            </p>
          </div>
        </div>

        <!-- Filter summary and clear button -->
        <div class="controls-footer" aria-live="polite">
          <p
            id="recipe-filter-description"
            :data-hover-read-text="`Showing ${filteredRecipes.length} of ${recipeCount} recipes.`"
          >
            Showing <strong>{{ filteredRecipes.length }}</strong> of <strong>{{ recipeCount }}</strong> recipes
          </p>

          <button
            v-if="hasActiveFilters"
            type="button"
            data-hover-read-text="Clear all recipe filters"
            @click="resetFilters"
          >
            Clear filters
          </button>
        </div>

        <h2 id="recipe-filter-title" class="nutrition-sr-only">Recipe filters</h2>
      </section>

      <!-- Loading state -->
      <section
        v-if="nutritionLoading"
        class="state-card"
        role="status"
        aria-live="polite"
        data-hover-read-text="Loading recipe ideas. Fetching nutrition options from your database."
      >
        <div class="state-icon" aria-hidden="true"><span>&#x1F957;</span></div>
        <h2>Loading recipe ideas...</h2>
        <p>Fetching nutrition options from your database.</p>
      </section>

      <!-- Error state -->
      <section
        v-else-if="nutritionError"
        class="state-card error-state"
        role="alert"
        aria-live="assertive"
        :data-hover-read-text="`Could not load recipes. ${nutritionError}`"
      >
        <div class="state-icon" aria-hidden="true"><span>&#9888;</span></div>
        <h2>Could not load recipes</h2>
        <p>{{ nutritionError }}</p>
        <button type="button" data-hover-read-text="Try loading recipes again" @click="fetchRecipes">
          Try again
        </button>
      </section>

      <!-- Empty search/filter result state -->
      <section
        v-else-if="filteredRecipes.length === 0"
        class="state-card"
        role="status"
        aria-live="polite"
        data-hover-read-text="No recipes match this search. Try clearing one filter or searching for a broader ingredient."
      >
        <div class="state-icon" aria-hidden="true"><span>&#x1F50E;</span></div>
        <h2>No recipes match this search</h2>
        <p>Try clearing one filter or searching for a broader ingredient.</p>
        <button type="button" data-hover-read-text="Show all recipes" @click="resetFilters">
          Show all recipes
        </button>
      </section>

      <!-- Recipe results section -->
      <section v-else class="recipe-section" aria-labelledby="recipe-section-title">
        <div class="section-heading">
          <div>
            <p class="eyebrow compact">
              <span class="eyebrow-dot" aria-hidden="true"></span>
              Database recipes
            </p>
            <h2 id="recipe-section-title">Choose one simple idea</h2>
          </div>
          <p data-hover-read-text="Open a recipe card to see ingredients and steps in a popup.">
            Open a recipe card to see ingredients and steps.
          </p>
        </div>

        <!-- Recipe card grid -->
        <div class="recipe-grid">
          <article
            v-for="recipe in visibleRecipes"
            :key="recipe.id"
            class="recipe-card"
            :aria-labelledby="`recipe-title-${recipeDomId(recipe)}`"
            :data-hover-read-text="getRecipeReadableText(recipe)"
          >
            <button
              type="button"
              class="recipe-card__top"
              aria-haspopup="dialog"
              :data-hover-read-text="getRecipeReadableText(recipe)"
              @click="openRecipePopup(recipe)"
            >
              <div class="recipe-main">
                <span class="category-pill">{{ recipe.category || 'Recipe' }}</span>
                <h3 :id="`recipe-title-${recipeDomId(recipe)}`">{{ recipe.name }}</h3>
                <p>{{ recipe.summary }}</p>
              </div>
              <span class="expand-icon" aria-hidden="true">+</span>
            </button>

            <div class="recipe-meta" aria-label="Recipe details">
              <span>{{ recipe.area || 'Family' }}</span>
              <span>{{ recipe.effortLabel }}</span>
              <span>{{ recipe.needLabel }}</span>
            </div>
          </article>
        </div>

        <!-- Loads more recipes into the visible list -->
        <div v-if="filteredRecipes.length > visibleLimit" class="load-more-wrap">
          <button
            type="button"
            class="load-more"
            data-hover-read-text="Show more recipes"
            @click="visibleLimit += 12"
          >
            Show more recipes
          </button>
        </div>
      </section>
    </main>

    <!-- Recipe detail modal -->
    <Teleport to="body">
      <Transition name="recipe-modal-fade">
        <div
          v-if="selectedRecipe"
          class="recipe-modal-backdrop"
          role="presentation"
          @click.self="closeRecipePopup"
        >
          <section
            class="recipe-modal"
            role="dialog"
            aria-modal="true"
            :aria-labelledby="`recipe-modal-title-${recipeDomId(selectedRecipe)}`"
            :aria-describedby="`recipe-modal-summary-${recipeDomId(selectedRecipe)}`"
            :data-hover-read-text="getRecipeReadableText(selectedRecipe)"
          >
            <button
              type="button"
              class="recipe-modal-close"
              aria-label="Close recipe popup"
              data-hover-read-text="Close recipe popup"
              @click="closeRecipePopup"
            >
              ×
            </button>

            <div class="recipe-modal-head">
              <span class="category-pill">{{ selectedRecipe.category || 'Recipe' }}</span>

              <h2 :id="`recipe-modal-title-${recipeDomId(selectedRecipe)}`">
                {{ selectedRecipe.name }}
              </h2>

              <p :id="`recipe-modal-summary-${recipeDomId(selectedRecipe)}`">
                {{ selectedRecipe.summary }}
              </p>

              <div class="recipe-modal-meta" aria-label="Recipe summary">
                <span>{{ selectedRecipe.area || 'Family' }}</span>
                <span>{{ selectedRecipe.effortLabel }}</span>
                <span>{{ selectedRecipe.needLabel }}</span>
              </div>
            </div>

            <div class="recipe-modal-body">
              <!-- Recipe ingredients -->
              <div v-if="selectedRecipe.ingredientsList.length" class="recipe-modal-block">
                <h3>Ingredients</h3>
                <ul>
                  <li v-for="ingredient in selectedRecipe.ingredientsList" :key="ingredient">
                    {{ ingredient }}
                  </li>
                </ul>
              </div>

              <!-- Recipe method steps -->
              <div v-if="selectedRecipe.stepList.length" class="recipe-modal-block">
                <h3>Steps</h3>
                <ol>
                  <li v-for="step in selectedRecipe.stepList" :key="step">
                    {{ step }}
                  </li>
                </ol>
              </div>

              <!-- Parent-friendly recipe tip -->
              <div class="recipe-modal-tip" :data-hover-read-text="`Parent tip. ${selectedRecipe.parentTip}`">
                <strong>Parent tip:</strong>
                <span>{{ selectedRecipe.parentTip }}</span>
              </div>
            </div>
          </section>
        </div>
      </Transition>
    </Teleport>

    <!-- Floating scroll-to-top button -->
    <button
      v-show="isScrolled"
      type="button"
      class="nutrition-scroll-top-btn"
      aria-label="Back to top"
      data-hover-read-text="Back to top"
      @click="scrollToTop"
    >
      <svg aria-hidden="true" width="15" height="15" viewBox="0 0 14 14" fill="none">
        <path
          d="M7 12V2M3 6l4-4 4 4"
          stroke="currentColor"
          stroke-width="1.6"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </button>

    <!-- Footer bar -->
    <footer
      class="nutrition-inner-footer"
      aria-label="Website footer"
    >
      <div
        class="nutrition-inner-footer-left"
        aria-label="Supporting families across Australia"
        data-hover-read-text
      >
        <span class="nutrition-inner-footer-live-dot" aria-hidden="true"></span>
        Supporting families across Australia
      </div>

      <div
        class="nutrition-inner-footer-right"
        aria-label="UN Sustainable Development Goal 3, Good Health and Wellbeing. Developed by Team Syrbyx."
        data-hover-read-text
      >
        <span>UN SDG 3 · Good Health &amp; Wellbeing</span>
        <span class="nutrition-footer-divider" aria-hidden="true">·</span>
        <span>Developed by Team SYRBYX</span>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'
import { useFamilyPlanStore } from '../stores/familyPlanStore'
import { useFoodHealthPredictor } from '../composables/useFoodHealthPredictor'

// Nutrition API base URL from the Vite environment file.
const API_BASE = import.meta.env.VITE_NUTRITION_API_BASE_URL

// Shared family plan state.
const { state } = useFamilyPlanStore()

// Parent concerns from the family plan store.
const concerns = computed(() => (Array.isArray(state.concerns) ? state.concerns : []))

// Recipe loading state.
const recipes = ref([])
const nutritionLoading = ref(false)
const nutritionError = ref('')

// Search, filter, modal, and scroll state.
const searchQuery = ref('')
const selectedCategory = ref('all')
const selectedCuisine = ref('all')
const selectedNeed = ref('all')
const selectedRecipe = ref(null)
const visibleLimit = ref(12)
const isScrolled = ref(false)

// Tracks page scroll so the header and back-to-top button can update.
function onScroll() {
  const scrollTop =
    window.scrollY ||
    document.documentElement.scrollTop ||
    document.body.scrollTop ||
    0

  isScrolled.value = scrollTop > 40
}

// Food scorer input value.
const foodInput = ref('')

// Food health predictor state and actions.
const {
  loading: foodPredictionLoading,
  error: foodPredictionError,
  result: foodPredictionResult,
  candidates: foodPredictionCandidates,
  predictFood,
  clearPrediction,
} = useFoodHealthPredictor()

// Example foods shown before the user scores a food.
const exampleFoods = ['banana', 'white bread', 'greek yoghurt', 'milo']

// Quick filter chips shown in the hero section.
const quickStarts = computed(() => [
  { id: 'all', label: 'All ideas', category: 'all', cuisine: 'all', need: 'all' },
  { id: 'quick', label: 'Quick meals', category: 'all', cuisine: 'all', need: 'quick' },
  { id: 'lunchbox', label: 'Lunchbox friendly', category: 'all', cuisine: 'all', need: 'lunchbox-safe' },
])

// Recipes converted into a consistent frontend format.
const normalisedRecipes = computed(() => recipes.value.map(mapRecipe))

// Total number of normalised recipes.
const recipeCount = computed(() => normalisedRecipes.value.length)

// Category options update based on the selected cuisine.
const categoryOptions = computed(() => {
  const base = selectedCuisine.value === 'all'
    ? normalisedRecipes.value
    : normalisedRecipes.value.filter(r => r.area === selectedCuisine.value)
  return uniqueValues(base.map(r => r.category))
})

// Cuisine options update based on the selected category.
const cuisineOptions = computed(() => {
  const base = selectedCategory.value === 'all'
    ? normalisedRecipes.value
    : normalisedRecipes.value.filter(r => r.category === selectedCategory.value)
  return uniqueValues(base.map(r => r.area))
})

// Summary counts for filter options.
const categoryCount = computed(() => categoryOptions.value.length)
const cuisineCount = computed(() => cuisineOptions.value.length)

// Checks whether any recipe filters are active.
const hasActiveFilters = computed(() =>
  searchQuery.value ||
  selectedCategory.value !== 'all' ||
  selectedCuisine.value !== 'all' ||
  selectedNeed.value !== 'all'
)

// Applies search, category, cuisine, and family-need filters.
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

// Smoothly scrolls the page back to the top.
function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  })
}

// Limits how many filtered recipes are displayed at once.
const visibleRecipes = computed(() => filteredRecipes.value.slice(0, visibleLimit.value))

// Adds or removes the body class when the recipe modal opens or closes.
watch(
  selectedRecipe,
  recipe => {
    if (typeof document === 'undefined') return
    document.body.classList.toggle('recipe-modal-open', Boolean(recipe))
  },
  { immediate: true }
)


// Resets category if it no longer exists after cuisine changes.
watch(selectedCuisine, () => {
  // If the currently selected category no longer exists for this cuisine, reset it
  if (selectedCategory.value !== 'all' && !categoryOptions.value.includes(selectedCategory.value)) {
    selectedCategory.value = 'all'
  }
  visibleLimit.value = 12
})

// Resets cuisine if it no longer exists after category changes.
watch(selectedCategory, () => {
  // If the currently selected cuisine no longer exists for this category, reset it
  if (selectedCuisine.value !== 'all' && !cuisineOptions.value.includes(selectedCuisine.value)) {
    selectedCuisine.value = 'all'
  }
  visibleLimit.value = 12
})

// Sets up page listeners and loads recipes when the component mounts.
onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('keydown', handleRecipeModalKeydown)

  onScroll()

  fetchRecipes()
})

// Cleans up listeners and modal body class when leaving the page.
onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('keydown', handleRecipeModalKeydown)

  if (typeof document !== 'undefined') {
    document.body.classList.remove('recipe-modal-open')
  }
})

// Fetches recipe data from the nutrition API.
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

// Converts one backend recipe object into the format used by the page.
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

// Splits ingredient text into a short list.
function splitList(value) {
  if (!value) return []

  return String(value)
    .replace(/[\[\]']/g, '')
    .split(/,|\n|;/)
    .map(item => item.trim())
    .filter(Boolean)
    .slice(0, 10)
}

// Splits recipe steps into a readable ordered list.
function splitSteps(value) {
  if (!value) return []

  const cleaned = String(value)
    .replace(/\r/g, '')
    .replace(/\s+/g, ' ')
    .trim()

  const splitByNumber = cleaned.split(/(?:^|\s)(?:\d+\.|Step \d+:)/i).map(step => step.trim()).filter(Boolean)
  const splitBySentence = cleaned.split(/\.\s+/).map(step => step.trim()).filter(Boolean)

  return (splitByNumber.length > 1 ? splitByNumber : splitBySentence)
    .map(step => (step.endsWith('.') ? step : `${step}.`))
    .slice(0, 6)
}

// Category groups used to infer recipe needs.
const PROTEIN_CATEGORIES = new Set(['chicken', 'beef', 'pork', 'lamb', 'seafood', 'goat'])
const FRUIT_VEG_CATEGORIES = new Set(['vegetarian', 'vegan', 'side dish', 'side', 'salad'])
const LUNCHBOX_CATEGORIES = new Set([
  'snack', 'lunch', 'appetizer', 'starter',
  'world breakfast', 'south indian breakfast', 'indian breakfast', 'breakfast',
])
const QUICK_CATEGORIES = new Set([
  'snack', 'appetizer', 'starter', 'breakfast',
  'south indian breakfast', 'indian breakfast', 'world breakfast',
])

// Detects family needs such as protein, fruit and veg, lunchbox-friendly, or quick.
function detectNeeds(recipe) {
  const text = `${recipe.name} ${recipe.ingredients}`.toLowerCase()
  const cat = String(recipe.category).toLowerCase()
  const needs = []

  if (
    PROTEIN_CATEGORIES.has(cat) ||
    /chicken|egg|paneer|tofu|soy chunk|fish|prawn|shrimp|crab|mussel|squid|salmon|tuna|lentil|dal|beans|legume|yoghurt|yogurt|beef|mutton|lamb|pork|turkey|mince|keema|cheese|cottage|meat|goat/.test(text)
  ) {
    needs.push('protein')
  }

  if (
    FRUIT_VEG_CATEGORIES.has(cat) ||
    /vegetable|veggie|fruit|spinach|palak|carrot|peas|matar|tomato|lettuce|capsicum|broccoli|zucchini|courgette|onion|garlic|ginger|celery|leek|mushroom|pepper|aubergine|eggplant|cucumber|pumpkin|squash|corn|asparagus|kale|cabbage|cauliflower|beetroot|radish|turnip|apple|banana|mango|berry|lemon|lime|orange|avocado|coconut/.test(text)
  ) {
    needs.push('fruit-veg')
  }

  if (
    LUNCHBOX_CATEGORIES.has(cat) ||
    /wrap|sandwich|roll|burrito|dosa|idli|rice|pasta|noodle|flatbread|tortilla|pita|roti|chapati|muffin|fritter|ball|bite|skewer|dumpling|spring roll|sushi|salad/.test(text)
  ) {
    needs.push('lunchbox-safe')
  }

  if (
    QUICK_CATEGORIES.has(cat) ||
    /quick|easy|simple|bread|toast|rice|egg|stir.?fry|pan.?fry|saut[eé]|grill|boil|steam|instant|ready|one.?pan|one.?pot|speedy|fast/.test(text)
  ) {
    needs.push('quick')
  }

  return needs.length ? [...new Set(needs)] : ['family-friendly']
}

// Estimates whether a recipe is quick, medium, or plan-ahead.
function detectEffort(ingredientsList, stepList) {
  if (ingredientsList.length <= 5 && stepList.length <= 4) return 'quick'
  if (ingredientsList.length <= 9 && stepList.length <= 6) return 'medium'
  return 'plan-ahead'
}

// Builds the short recipe card summary.
function buildSummary(area, category, ingredientsList) {
  const ingredientsText = ingredientsList.slice(0, 3).join(', ')
  return `${area} ${category.toLowerCase()} idea${ingredientsText ? ` with ${ingredientsText}` : ''}.`
}

// Builds a parent-friendly tip based on recipe need and effort.
function buildParentTip(needs, effort) {
  if (needs.includes('lunchbox-safe')) return 'Pack sauces or wet ingredients separately so the meal stays fresh.'
  if (needs.includes('protein')) return 'Serve a small portion first, then offer more if your child is still hungry.'
  if (needs.includes('fruit-veg')) return 'Keep one familiar item on the plate to make the new food feel less overwhelming.'
  if (effort === 'plan-ahead') return 'Prepare one ingredient earlier in the day to reduce pressure at mealtime.'
  return 'Keep the first attempt simple and repeat it before adding more changes.'
}

// Returns sorted unique values for dropdown filters.
function uniqueValues(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b))
}

// Applies a quick-start recipe filter.
function applyQuickStart(shortcut) {
  selectedCategory.value = shortcut.category
  selectedCuisine.value = shortcut.cuisine
  selectedNeed.value = shortcut.need
  searchQuery.value = ''
  visibleLimit.value = 12
}

// Clears all recipe filters and closes any selected recipe.
function resetFilters() {
  searchQuery.value = ''
  selectedCategory.value = 'all'
  selectedCuisine.value = 'all'
  selectedNeed.value = 'all'
  selectedRecipe.value = null
  visibleLimit.value = 12
}

// Opens the recipe detail modal.
function openRecipePopup(recipe) {
  selectedRecipe.value = recipe
}

// Closes the recipe detail modal.
function closeRecipePopup() {
  selectedRecipe.value = null
}

// Closes the recipe modal when Escape is pressed.
function handleRecipeModalKeydown(event) {
  if (event.key === 'Escape' && selectedRecipe.value) {
    closeRecipePopup()
  }
}

// Sends the typed food to the food health predictor.
function submitFoodPrediction() {
  if (foodInput.value.trim()) predictFood(foodInput.value.trim())
}

// Uses a suggested candidate as the food scorer input.
function chooseFoodCandidate(candidate) {
  foodInput.value = candidate
  predictFood(candidate)
}

// Scores one of the example foods.
function tryExample(food) {
  foodInput.value = food
  predictFood(food)
}

// Clears the food scorer input and result.
function clearAndReset() {
  foodInput.value = ''
  clearPrediction()
}

// Returns the CSS class for a food score.
function scoreClass(score) {
  if (score >= 70) return 'score-good'
  if (score >= 40) return 'score-mid'
  return 'score-low'
}

// Returns the ring colour for a food score.
function scoreColor(score) {
  if (score >= 70) return '#327c70'
  if (score >= 40) return '#e6865f'
  return '#dc2626'
}

// Converts a score into SVG stroke length.
function scoreArc(score) {
  return Math.max(0, Math.min(100, score)) * 2.2
}

// Returns a short verdict for a food score.
function scoreVerdict(score) {
  if (score >= 80) return 'Excellent'
  if (score >= 65) return 'Good'
  if (score >= 45) return 'Okay'
  if (score >= 25) return 'Limited'
  return 'Low'
}

// Returns a parent-friendly score tip.
function scoreTip(result) {
  if (result?.tip) return result.tip
  if (result?.advice) return result.advice
  if (result?.recommendation) return result.recommendation
  if (result?.message) return result.message

  return 'Use this score as a quick guide and balance the food with the rest of the day.'
}

// Creates a safe DOM id for recipe headings and modal labels.
function recipeDomId(recipe) {
  return String(recipe?.id || recipe?.name || 'recipe')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
}

// Builds readable recipe text for hover-to-read.
function getRecipeReadableText(recipe) {
  return `${recipe.name}. ${recipe.category || 'Recipe'}. ${recipe.area || 'Family cuisine'}. ${recipe.effortLabel}. ${recipe.needLabel}. ${recipe.summary}`.replace(/\s+/g, ' ').trim()
}

// Builds readable food score text for hover-to-read and screen readers.
function getFoodScoreReadableText(result) {
  const score = Math.round(result.health_score)
  const verdict = scoreVerdict(result.health_score)
  const tip = scoreTip(result)

  return `${result.matched_food}. Health score ${score} out of 100. ${verdict}. ${tip}`
}
</script>