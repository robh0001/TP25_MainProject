<!--
  StatisticsPage.vue

  Creates the HealthyKids statistics page. It shows child health insights for weight,
  activity, sleep, and long-term trends using data from the insights API.

  API requirement:
  - Requires VITE_PARENT_DATA_INSIGHTS_API_BASE_URL.
  - Fetches child health insight data from the configured API URL.
  - Shows loading and error states if the API is unavailable.

  Accessibility:
  - Uses aria-labels, aria-live, role="status", role="alert", and aria-pressed.
  - Uses aria-current="page" for the active Statistics navigation link.
  - Uses data-hover-read-text for hover-to-read support.
  - Marks decorative SVGs and visual elements as aria-hidden where appropriate.
-->

<template>
  <div class="stats-page">
    <!-- Page header with logo, navigation, and quick actions -->
    <header class="header" :class="{ scrolled: isScrolled }" aria-label="HealthyKids statistics header">
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

        <!-- Main page navigation -->
        <nav class="nav" aria-label="Statistics page navigation">
          <RouterLink to="/" class="nav-a" data-hover-read-text="Go to home page">
            Home
          </RouterLink>

          <RouterLink to="/parent-dashboard" class="nav-a" data-hover-read-text="Go to parent dashboard">
            Dashboard
          </RouterLink>

          <RouterLink to="/parent-nutrition-tools" class="nav-a" data-hover-read-text="Go to nutrition page">
            Nutrition
          </RouterLink>

          <RouterLink
            to="/statistics"
            class="nav-a"
            aria-current="page"
            data-hover-read-text="Current page. Statistics."
          >
            Statistics
          </RouterLink>

          <RouterLink to="/young-person-dashboard" class="nav-a" data-hover-read-text="Go to kids view">
            Kids view
          </RouterLink>
        </nav>

        <!-- Header action links -->
        <div class="nav-cta">
          <RouterLink
            to="/parent-quiz"
            class="nav-link"
            data-hover-read-text="Retake the parent quiz"
          >
            Retake quiz
          </RouterLink>

          <RouterLink
            to="/parent-quiz"
            class="nav-btn"
            data-hover-read-text="Create a new family plan"
          >
            New Plan
            <svg aria-hidden="true" focusable="false" width="11" height="11" viewBox="0 0 12 12">
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

    <!-- Main statistics page content -->
    <main
      id="main-content"
      class="page-main"
      aria-labelledby="stats-page-title"
      aria-describedby="stats-page-description"
    >
      <!-- Loading state while insights are being fetched -->
      <div
        v-if="insightsLoading"
        class="state-view"
        role="status"
        aria-live="polite"
        data-hover-read-text="Getting your insights ready."
      >
        <div class="leaf-spinner" aria-hidden="true">
          <svg viewBox="0 0 60 60" fill="none" focusable="false">
            <path d="M30 8C17 18 14 28 30 52C46 28 43 18 30 8Z" fill="#276d45" opacity="0.15"/>
            <path d="M30 8C17 18 14 28 30 52C46 28 43 18 30 8Z" stroke="#276d45" stroke-width="2" stroke-dasharray="120" stroke-dashoffset="120" class="leaf-draw"/>
          </svg>
        </div>
        <p>Getting your insights ready...</p>
      </div>

      <!-- Error state when insights cannot be loaded -->
      <div
        v-else-if="insightsError"
        class="state-view state-error"
        role="alert"
        aria-live="assertive"
        :data-hover-read-text="`Could not load insights. ${insightsError}`"
      >
        <p>{{ insightsError }}</p>
        <button
          type="button"
          class="pill-btn"
          data-hover-read-text="Try loading insights again"
          @click="fetchInsights"
        >
          Try again
        </button>
      </div>

      <template v-else>
        <!-- Hero section introducing the statistics page -->
        <section class="hero">
          <div class="hero-copy" :class="{ 'is-visible': heroVisible }">
            <p
              class="eyebrow"
              data-hover-read-text="Australia. Children aged 5 to 12."
            >
              <span class="eyebrow-dot" aria-hidden="true"></span>
              Australia · Children aged 5-12
            </p>

            <h1
              id="stats-page-title"
              data-hover-read-text="The health picture for Australian kids"
            >
              The health<br/> <em>picture</em> for<br/>Australian kids
            </h1>

            <p
              id="stats-page-description"
              class="hero-sub"
              data-hover-read-text="Select a topic below to explore the numbers and what they mean for your family."
            >
              Select a topic below to explore the numbers - and what they mean for your family.
            </p>
          </div>

          <!-- Gender filter for BMI and trend data -->
          <div class="gender-toggle" :class="{ 'is-visible': heroVisible }">
            <p class="toggle-label">Viewing data for</p>
            <div class="toggle-pills">
              <button
                v-for="g in genders"
                :key="g.value"
                type="button"
                class="toggle-pill"
                :class="{ active: selectedGender === g.value }"
                :aria-pressed="selectedGender === g.value ? 'true' : 'false'"
                :data-hover-read-text="`${g.label}. ${selectedGender === g.value ? 'Selected' : 'Not selected'}. View statistics for ${g.label}.`"
                @click="selectedGender = g.value"
              >
                {{ g.label }}
              </button>
            </div>
          </div>
        </section>

        <!-- Main interactive insight explorer -->
        <section class="insight-explorer">
          <!-- Topic tabs for Weight, Activity, Sleep, and Trend -->
          <div class="explorer-tabs">
            <button
              v-for="(tab, i) in tabs"
              :key="tab.key"
              type="button"
              class="explorer-tab"
              :class="{ active: activeTab === i }"
              :aria-pressed="activeTab === i ? 'true' : 'false'"
              :data-hover-read-text="`${tab.label} section. ${activeTab === i ? 'Selected' : 'Not selected'}.`"
              @click="setTab(i)"
            >
              <span class="tab-icon" aria-hidden="true">{{ tab.icon }}</span>
              <span class="tab-label">{{ tab.label }}</span>
              <span class="tab-dot" :style="{ background: tab.color }" aria-hidden="true"></span>
            </button>
          </div>

          <transition name="panel-slide" mode="out-in">

            <!-- BMI Panel -->
            <div v-if="activeTab === 0" key="bmi" class="explorer-panel">
              <div class="panel-intro">
                <h2>{{ trendLabel }}'s weight picture</h2>
                <p>Tap a category to learn more.</p>
              </div>

              <div class="bmi-layout">
                <!-- BMI ring chart -->
                <div class="ring-wrap">
                  <svg class="ring-svg" viewBox="0 0 200 200">
                    <circle cx="100" cy="100" r="80" fill="none" stroke="#eef1ec" stroke-width="18"/>
                    <circle
                      v-for="(seg, i) in bmiRingSegs"
                      :key="seg.key"
                      cx="100" cy="100" r="80" fill="none"
                      :stroke="seg.color" stroke-width="18" stroke-linecap="round"
                      :stroke-dasharray="`${seg.dash} 502`"
                      :stroke-dashoffset="seg.offset"
                      :style="{ transition: `stroke-dasharray 0.9s ease ${i*0.15}s, stroke-dashoffset 0.9s ease ${i*0.15}s` }"
                      transform="rotate(-90 100 100)"
                    />
                    <text x="100" y="93" text-anchor="middle" class="ring-big">{{ combinedVal }}%</text>
                    <text x="100" y="112" text-anchor="middle" class="ring-sub">above healthy</text>
                  </svg>
                </div>

                <!-- BMI category cards -->
                <div class="bmi-cards">
                  <button
                    v-for="item in bmiChartData"
                    :key="item.key"
                    type="button"
                    class="bmi-cat-card"
                    :class="{ active: selectedBmi === item.key }"
                    :style="{ '--accent': item.color }"
                    :aria-expanded="selectedBmi === item.key ? 'true' : 'false'"
                    :aria-pressed="selectedBmi === item.key ? 'true' : 'false'"
                    :data-hover-read-text="`${item.label}. ${item.value} percent. About ${item.count} thousand kids. ${selectedBmi === item.key ? bmiNoteFor(item) : 'Select to learn more.'}`"
                    @click="selectedBmi = selectedBmi === item.key ? null : item.key"
                  >
                    <div class="cat-swatch" :style="{ background: item.color }"></div>
                    <div class="cat-body">
                      <span class="cat-name">{{ item.label }}</span>
                      <strong class="cat-pct">{{ item.value }}%</strong>
                      <span class="cat-count">{{ item.count }}k kids</span>
                    </div>
                    <div class="cat-arrow">
                      <svg aria-hidden="true" focusable="false" width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path :d="selectedBmi===item.key ? 'M4 6l4 4 4-4' : 'M6 4l4 4-4 4'" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </div>
                    <transition name="expand-note">
                      <div v-if="selectedBmi === item.key" class="cat-note">{{ bmiNoteFor(item) }}</div>
                    </transition>
                  </button>
                </div>
              </div>

              <!-- Parent-friendly BMI insight -->
              <div class="affirmation-strip">
                <svg class="aff-icon" width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 8v4l3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                <p>Small daily habits - a 20-minute walk, less screen time, earlier bedtimes - have the biggest long-term impact for kids in every category.</p>
              </div>
            </div>

            <!-- Activity Panel -->
            <div v-else-if="activeTab === 1" key="activity" class="explorer-panel">
              <div class="panel-intro">
                <h2>How active are kids really?</h2>
                <p>Choose an activity type to explore.</p>
              </div>

              <!-- Activity type filter buttons -->
              <div class="activity-type-pills">
                <button
                  v-for="a in activityTypes"
                  :key="a.value"
                  type="button"
                  class="activity-pill"
                  :class="{ active: selectedActivity === a.value }"
                  :aria-pressed="selectedActivity === a.value ? 'true' : 'false'"
                  :data-hover-read-text="`${a.label}. ${selectedActivity === a.value ? 'Selected' : 'Not selected'}.`"
                  @click="selectedActivity = a.value"
                >
                  {{ a.label }}
                </button>
              </div>

              <!-- Activity distribution bars -->
              <div class="activity-bars">
                <div
                  v-for="(item, i) in orderedActivityBands"
                  :key="item.label"
                  class="act-bar-card"
                  :class="{ highlight: activityFocusBand && item.label === activityFocusBand.label }"
                  :style="{ animationDelay: `${i * 0.07}s` }"
                  :data-hover-read-text="getActivityBandReadableText(item)"
                >
                  <div class="act-bar-label">{{ shorten(item.label) }}</div>
                  <div class="act-bar-track">
                    <div class="act-bar-fill" :style="{ width: cleanBarWidth(item.value, activityMaxVal) + '%', background: actColor(item.value) }"></div>
                  </div>
                  <div class="act-bar-pct">{{ item.value }}%</div>
                  <div v-if="activityFocusBand && item.label === activityFocusBand.label" class="act-bar-badge">Most common</div>
                </div>
              </div>

              <div class="affirmation-strip">
                <svg class="aff-icon" width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 8v4l3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                <p>{{ activityInsight }}</p>
              </div>
            </div>

            <!-- Sleep Panel -->
            <div v-else-if="activeTab === 2" key="sleep" class="explorer-panel">
              <div class="panel-intro">
                <h2>Are kids getting enough sleep?</h2>
                <p>Choose a sleep period below.</p>
              </div>

              <!-- Sleep period filter buttons -->
              <div class="activity-type-pills">
                <button
                  v-for="s in sleepTypes"
                  :key="s.value"
                  type="button"
                  class="activity-pill"
                  :class="{ active: selectedSleep === s.value }"
                  :aria-pressed="selectedSleep === s.value ? 'true' : 'false'"
                  :data-hover-read-text="`${s.label}. ${selectedSleep === s.value ? 'Selected' : 'Not selected'}.`"
                  @click="selectedSleep = s.value"
                >
                  {{ s.label }}
                </button>
              </div>

              <!-- Sleep distribution cards -->
              <div class="sleep-grid">
                <div
                  v-for="(item, i) in orderedSleepBands"
                  :key="item.label"
                  class="sleep-card"
                  :class="{ 'sleep-card--good': isSleepTargetBand(item.label), 'sleep-card--low': isLowSleepBand(item.label) }"
                  :style="{ animationDelay: `${i * 0.08}s` }"
                  :data-hover-read-text="getSleepBandReadableText(item)"
                >
                  <div class="sleep-moon">
                    <svg v-if="isSleepTargetBand(item.label)" width="28" height="28" viewBox="0 0 24 24" fill="none"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    <svg v-else width="28" height="28" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="5" stroke="currentColor" stroke-width="1.6"/><path d="M12 2v2M12 20v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M2 12h2M20 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                  </div>
                  <strong class="sleep-pct">{{ item.value }}%</strong>
                  <span class="sleep-label">{{ sleepShort(item.label) }}</span>
                  <div v-if="isSleepTargetBand(item.label)" class="sleep-badge">Target ✓</div>
                </div>
              </div>

              <!-- Recommended sleep target summary -->
              <div class="sleep-target-note">
                <div class="target-bar">
                  <div class="target-bar-fill" :style="{ width: sleepTargetPctNumber + '%' }"></div>
                </div>
                <p><strong>{{ sleepTargetPct }}%</strong> of kids reach the recommended 9-11 hours.</p>
              </div>

              <div class="affirmation-strip">
                <svg class="aff-icon" width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M12 8v4l3 3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
                <p>A consistent bedtime routine - even 30 minutes earlier - can meaningfully improve kids' focus, mood, and health over time.</p>
              </div>
            </div>

            <!-- Trend Panel -->
            <div v-else-if="activeTab === 3" key="trend" class="explorer-panel">
              <div class="panel-intro">
                <h2>How have things changed over time?</h2>
                <p>Hover or tap the dots to see exact values.</p>
              </div>

              <!-- Trend line chart -->
              <div class="chart-scroll">
                <svg viewBox="0 0 580 260" class="line-svg">
                  <line v-for="y in gridYs" :key="'g'+y" x1="52" :y1="tY(y)" x2="548" :y2="tY(y)" class="grid-line"/>
                  <text v-for="y in gridYs" :key="'l'+y" x="44" :y="tY(y)+4" text-anchor="end" class="axis-lbl">{{ y }}%</text>
                  <path :d="areaPath('overweight_obese_6_13')" class="area-fill"/>
                  <path :d="linePath('overweight_obese_6_13')" fill="none" stroke="#276d45" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" class="trend-line"/>
                  <path :d="linePath('obese_6_13')" fill="none" stroke="#7a5c1e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="trend-line" style="animation-delay:.2s"/>
                  <path :d="linePath('underweight_6_13')" fill="none" stroke="#7aab8a" stroke-width="1.8" stroke-dasharray="6 4" stroke-linecap="round" stroke-linejoin="round" class="trend-line" style="animation-delay:.4s"/>

                  <!-- Interactive trend points -->
                  <template v-for="metric in trendMetrics" :key="metric.key">
                    <circle
                      v-for="pt in trendPoints(metric.key)"
                      :key="pt.year"
                      :cx="pt.x"
                      :cy="pt.y"
                      r="5"
                      :fill="metric.color"
                      stroke="white"
                      stroke-width="2.5"
                      class="trend-dot"
                      tabindex="0"
                      role="img"
                      :aria-label="getTrendPointReadableText(metric, pt)"
                      :data-hover-read-text="getTrendPointReadableText(metric, pt)"
                      @mouseenter="trendHover = { metric, pt }"
                      @mouseleave="trendHover = null"
                      @focus="trendHover = { metric, pt }"
                      @blur="trendHover = null"
                    />
                  </template>

                  <!-- Tooltip for the active trend point -->
                  <g v-if="trendHover">
                    <line :x1="trendHover.pt.x" :x2="trendHover.pt.x" y1="20" y2="225" class="hover-rule"/>
                    <rect :x="ttX(trendHover.pt.x)" :y="Math.max(14, trendHover.pt.y-56)" width="158" height="44" rx="10" fill="white" filter="url(#sh)"/>
                    <text :x="ttX(trendHover.pt.x)+12" :y="Math.max(14,trendHover.pt.y-56)+16" class="tt-label">{{ trendHover.metric.label }}</text>
                    <text :x="ttX(trendHover.pt.x)+12" :y="Math.max(14,trendHover.pt.y-56)+34" class="tt-val">{{ trendHover.pt.year }} · {{ trendHover.pt.val }}%</text>
                    <defs>
                      <filter id="sh" x="-10%" y="-20%" width="120%" height="150%">
                        <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="rgba(26,74,48,.14)"/>
                      </filter>
                    </defs>
                  </g>
                  <text v-for="yr in trendYears" :key="'yr'+yr" :x="tX(yr)" y="249" text-anchor="middle" class="axis-lbl">{{ yr }}</text>
                </svg>
              </div>

              <!-- Trend legend -->
              <div class="trend-legend">
                <span v-for="m in trendMetrics" :key="m.key" class="leg-item">
                  <i :style="{ background: m.color }"></i>{{ m.label }}
                </span>
              </div>
            </div>

          </transition>
        </section>

        <!-- Quick facts summary cards -->
        <section class="fact-strip">
          <div
            v-for="(fact, i) in quickFacts"
            :key="i"
            class="fact-card"
            :style="{ '--c': fact.color, animationDelay: `${i * 0.1}s` }"
            :data-hover-read-text="`${fact.num}. ${fact.text}`"
          >
            <div class="fact-icon-wrap" :style="{ color: fact.color }">
              <svg aria-hidden="true" focusable="false" width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path :d="fact.svgPath" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <strong class="fact-num">{{ fact.num }}</strong>
            <p class="fact-text">{{ fact.text }}</p>
          </div>
        </section>
      </template>
    </main>

    <!-- Footer -->
    <footer
      class="stats-footer"
      aria-label="Website footer"
    >
      <div
        class="stats-footer-left"
        aria-label="Supporting families across Australia"
        data-hover-read-text
      >
        <span class="stats-live-dot" aria-hidden="true"></span>
        Supporting families across Australia
      </div>

      <div
        class="stats-footer-right"
        aria-label="UN Sustainable Development Goal 3, Good Health and Wellbeing. Developed by Team SYRBYX."
        data-hover-read-text
      >
        <span>UN SDG 3 · Good Health &amp; Wellbeing</span>
        <span class="stats-footer-divider" aria-hidden="true">·</span>
        <span>Developed by Team SYRBYX</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'

// Insights API base URL from Vite environment variables.
const API_BASE_URL = import.meta.env.VITE_PARENT_DATA_INSIGHTS_API_BASE_URL

// User-selected filters and UI state.
const selectedGender   = ref('all')
const selectedActivity = ref('inactivity')
const selectedSleep    = ref('weeknight')
const selectedBmi      = ref(null)
const trendHover       = ref(null)
const activeTab        = ref(0)
const heroVisible      = ref(false)

// API loading, error, and response state.
const insightsLoading = ref(false)
const insightsError   = ref('')
const insightsData    = ref({
  bmi:      { all: [], boys: [], girls: [] },
  trend:    { all: [], boys: [], girls: [] },
  activity: { inactivity: [], light: [], moderate_vigorous: [] },
  sleep:    { weeknight: [], weekend: [], overall: [] },
})

// Colours used for BMI categories.
const COLORS = {
  underweight: '#7aab8a',
  normal:      '#276d45',
  overweight:  '#c4850a',
  obese:       '#8b3a3a',
}

// Trend lines displayed in the trend chart.
const trendMetrics = [
  { key: 'overweight_obese_6_13', label: 'Overweight + obese', color: '#276d45' },
  { key: 'obese_6_13',            label: 'Obese only',          color: '#7a5c1e' },
  { key: 'underweight_6_13',      label: 'Underweight',         color: '#7aab8a' },
]

// Gender filter options.
const genders = [
  { value: 'all',   label: 'All children', icon: '' },
  { value: 'boys',  label: 'Boys',         icon: '' },
  { value: 'girls', label: 'Girls',        icon: '' },
]

// Main insight tabs.
const tabs = [
  { key: 'bmi',      label: 'Weight',   icon: '', color: '#1e6640' },
  { key: 'activity', label: 'Activity', icon: '', color: '#a86c00' },
  { key: 'sleep',    label: 'Sleep',    icon: '', color: '#2d5f82' },
  { key: 'trend',    label: 'Trend',    icon: '', color: '#6a9e7a' },
]

// Activity filter options.
const activityTypes = [
  { value: 'inactivity',        label: 'Inactivity',        icon: '' },
  { value: 'light',             label: 'Light activity',    icon: '' },
  { value: 'moderate_vigorous', label: 'Active & vigorous', icon: '' },
]

// Sleep filter options.
const sleepTypes = [
  { value: 'weeknight', label: 'Weeknights', icon: '' },
  { value: 'weekend',   label: 'Weekends',   icon: '' },
  { value: 'overall',   label: 'Per night',  icon: '' },
]

// Y-axis grid values for the trend chart.
const gridYs = [0, 10, 20, 30]

// Loads insights and starts the hero animation.
onMounted(() => {
  fetchInsights()
  setTimeout(() => { heroVisible.value = true }, 80)
})

// Clears selected BMI card when gender changes.
watch([selectedGender], () => { selectedBmi.value = null })

// Changes the active insight tab.
function setTab(i) { activeTab.value = i; selectedBmi.value = null }

// Fetches child health insight data from the configured API.
async function fetchInsights() {
  if (!API_BASE_URL) { insightsError.value = 'Missing VITE_PARENT_DATA_INSIGHTS_API_BASE_URL.'; return }
  insightsLoading.value = true
  insightsError.value = ''
  try {
    const res = await fetch(API_BASE_URL, { headers: { Accept: 'application/json' } })
    const data = await res.json().catch(() => ({}))
    if (!res.ok) throw new Error(data.error || `API error ${res.status}`)
    insightsData.value = normalise(data)
  } catch (e) {
    insightsError.value = e.message || 'Unable to load insights.'
  } finally {
    insightsLoading.value = false
  }
}

// Normalises the API response into the page's expected data structure.
function normalise(data) {
  return {
    bmi: { all: normBmi(data?.bmi?.all), boys: normBmi(data?.bmi?.boys), girls: normBmi(data?.bmi?.girls) },
    trend: {
      all:   Array.isArray(data?.trend?.all)   ? data.trend.all   : [],
      boys:  Array.isArray(data?.trend?.boys)  ? data.trend.boys  : [],
      girls: Array.isArray(data?.trend?.girls) ? data.trend.girls : [],
    },
    activity: {
      inactivity:        normVal(data?.activity?.inactivity),
      light:             normVal(data?.activity?.light),
      moderate_vigorous: normVal(data?.activity?.moderate_vigorous),
    },
    sleep: {
      weeknight: normVal(data?.sleep?.weeknight),
      weekend:   normVal(data?.sleep?.weekend),
      overall:   normVal(data?.sleep?.overall),
    },
  }
}

// Normalises BMI rows from the API.
function normBmi(rows) {
  if (!Array.isArray(rows)) return []
  return rows.map(r => ({ key: r.key, label: r.label || r.key, count: Number(r.count||0), value: Number(r.value||0) }))
}

// Normalises generic label/value rows from the API.
function normVal(rows) {
  if (!Array.isArray(rows)) return []
  return rows.map(r => ({ label: r.label||'', value: Number(r.value||0) }))
}

// BMI data for the selected gender.
const bmiChartData = computed(() =>
  (insightsData.value.bmi[selectedGender.value] || []).map(item => ({ ...item, color: COLORS[item.key] || '#7aab8a' }))
)

// Weight category summary values.
const overweightVal = computed(() => bmiChartData.value.find(i => i.key==='overweight')?.value || 0)
const obeseVal      = computed(() => bmiChartData.value.find(i => i.key==='obese')?.value || 0)
const combinedVal   = computed(() => Math.round((overweightVal.value + obeseVal.value) * 10) / 10)

// User-facing label for the selected gender.
const trendLabel    = computed(() =>
  selectedGender.value==='boys' ? 'Boys' : selectedGender.value==='girls' ? 'Girls' : 'All children'
)

// Trend and chart data for the selected filters.
const trendRows     = computed(() => insightsData.value.trend[selectedGender.value] || [])
const trendYears    = computed(() => trendRows.value.map(r => r.year))
const activityBands = computed(() => insightsData.value.activity[selectedActivity.value] || [])
const sleepBands    = computed(() => insightsData.value.sleep[selectedSleep.value] || [])

// Ordered visual bands for activity and sleep charts.
const orderedActivityBands = computed(() => [...activityBands.value].sort((a,b) => actOrder(a.label)-actOrder(b.label)))
const orderedSleepBands    = computed(() => [...sleepBands.value].sort((a,b) => sleepOrder(a.label)-sleepOrder(b.label)))

// Activity chart helpers.
const activityMaxVal       = computed(() => Math.max(...activityBands.value.map(i => i.value), 1))
const activityFocusBand    = computed(() => {
  if (!activityBands.value.length) return null
  return activityBands.value.reduce((h,i) => i.value > h.value ? i : h)
})

// Percentage of children who reach the target sleep range.
const sleepTargetPct = computed(() =>
  sleepBands.value.filter(i => /9 to less than 10|10 hours or more/i.test(i.label))
    .reduce((s,i) => s+i.value, 0).toFixed(1)
)
const sleepTargetPctNumber = computed(() => Number(sleepTargetPct.value || 0))

// Builds ring chart segments from BMI data.
const bmiRingSegs = computed(() => {
  const total = bmiChartData.value.reduce((s,i) => s+i.value, 0) || 100
  const circ = 2 * Math.PI * 80
  let offset = 0
  return bmiChartData.value.map(item => {
    const dash = (item.value / total) * circ
    const seg = { key: item.key, color: item.color, dash, offset: -offset }
    offset += dash
    return seg
  })
})

// Summary fact cards shown below the explorer.
const quickFacts = computed(() => [
  { svgPath: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z', num: `${combinedVal.value}%`, text: `of ${trendLabel.value.toLowerCase()} are above a healthy weight`, color: '#1e6640' },
  { svgPath: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z', num: `${sleepTargetPct.value}%`, text: 'reach the recommended 9-11 hours of sleep per night', color: '#2d5f82' },
  { svgPath: 'M13 2L3 14h9l-1 8 10-12h-9l1-8z', num: `${activityFocusBand.value?.value||0}%`, text: `in the most common ${activityTypes.find(a=>a.value===selectedActivity.value)?.label.toLowerCase()} band`, color: '#a86c00' },
])

// Parent-friendly activity insight text.
const activityInsight = computed(() => {
  if (selectedActivity.value==='inactivity')
    return 'Reducing inactive time - even by 30 minutes per day - is linked to better sleep and a healthier weight for children.'
  if (selectedActivity.value==='light')
    return 'Light activity like walking or playing outside counts! Every bit of movement helps build healthy habits early.'
  return 'Vigorous play - running, swimming, team sports - is the most beneficial for heart health and mood.'
})

// Calculates X position for a trend year.
function tX(year) {
  const years = trendYears.value
  if (years.length <= 1) return 60
  return 60 + (years.indexOf(year) / (years.length - 1)) * 478
}

// Calculates Y position for a percentage value.
function tY(value)  { return 225 - (Number(value||0) / 35) * 190 }

// Converts trend rows into SVG point coordinates.
function trendPoints(metric) {
  return trendRows.value.map(row => ({ x: tX(row.year), y: tY(row[metric]), val: row[metric], year: row.year }))
}

// Builds an SVG line path for a trend metric.
function linePath(metric) {
  const pts = trendPoints(metric)
  if (!pts.length) return ''
  return pts.map((p,i) => (i===0?`M${p.x},${p.y}`:`L${p.x},${p.y}`)).join(' ')
}

// Builds the filled area path under a trend line.
function areaPath(metric) {
  const pts = trendPoints(metric)
  if (!pts.length) return ''
  const line = pts.map((p,i) => (i===0?`M${p.x},${p.y}`:`L${p.x},${p.y}`)).join(' ')
  return `${line} L${pts.at(-1).x},225 L${pts[0].x},225 Z`
}

// Keeps the tooltip inside the visible chart area.
function ttX(x) { return x > 400 ? x - 170 : x + 14 }

// Calculates bar width as a percentage of the maximum value.
function cleanBarWidth(value, max) { return Math.max(4, (Number(value||0)/max)*100) }

// Chooses a colour for activity bars.
function actColor(value) {
  if (value >= 35) return '#276d45'
  if (value >= 20) return '#3a8f5e'
  if (value >= 10) return '#c4850a'
  return '#8b3a3a'
}

// Shortens long band labels for compact visual cards.
function shorten(label) {
  return String(label||'').replace('Less than','<').replace('to less than','-')
    .replace(' hours','h').replace(' hour','h').replace(' minutes','min').replace(' or more','+')
}

// Shortens sleep labels.
function sleepShort(label) { return shorten(label) }

// Provides explanatory notes for BMI categories.
function bmiNoteFor(item) {
  const map = {
    underweight: 'Children here may benefit from nutritional support. A GP can give personalised guidance.',
    normal:      'Great news - these kids are in a healthy weight range. Keeping current routines going is the key.',
    overweight:  `${item.value}% of ${trendLabel.value.toLowerCase()} fall here. Small lifestyle changes can help reverse this trend.`,
    obese:       `This is the highest-risk category. HealthyKids routines are built to support families with gradual, lasting changes.`,
  }
  return map[item.key] || `${item.value}% of ${trendLabel.value.toLowerCase()} are in this category.`
}

// Sorts activity bands into a logical display order.
function actOrder(label) {
  const t = String(label||'').toLowerCase()
  if (t.includes('less than 30')) return 1; if (t.includes('30 to less than 60')) return 2
  if (t.includes('1 to less than 1.5')) return 3; if (t.includes('1.5 to less than 2')) return 4
  if (t.includes('2 hours or more')) return 5; if (t.includes('less than 9')) return 1
  if (t.includes('9 to less than 10')) return 2; if (t.includes('10 to less than 11')) return 3
  if (t.includes('11 to less than 12')) return 4; if (t.includes('12 to less than 13')) return 5
  if (t.includes('13 to less than 14')) return 6; if (t.includes('14 hours or more')) return 7
  if (t.includes('less than 2')) return 1; if (t.includes('2 to less than 3')) return 2
  if (t.includes('3 to less than 4')) return 3; if (t.includes('4 hours or more')) return 4
  return 99
}

// Sorts sleep bands into a logical display order.
function sleepOrder(label) {
  const t = String(label||'').toLowerCase()
  if (t.includes('less than 6')) return 1; if (t.includes('6 to less than 7')) return 2
  if (t.includes('7 to less than 8')) return 3; if (t.includes('8 to less than 9')) return 4
  if (t.includes('9 to less than 10')) return 5; if (t.includes('10 hours or more')) return 6
  return 99
}

// Checks whether a sleep band is within the recommended target.
function isSleepTargetBand(label) { return /9 to less than 10|10 hours or more/i.test(label) }

// Checks whether a sleep band is below the recommended target.
function isLowSleepBand(label)    { return /less than 6|6 to less than 7|7 to less than 8|8 to less than 9/i.test(label) }

// Builds readable text for activity cards.
function getActivityBandReadableText(item) {
  const mostCommon = activityFocusBand.value && item.label === activityFocusBand.value.label
  return `${shorten(item.label)}. ${item.value} percent.${mostCommon ? ' Most common activity band.' : ''}`
}

// Builds readable text for sleep cards.
function getSleepBandReadableText(item) {
  const target = isSleepTargetBand(item.label)
  const low = isLowSleepBand(item.label)

  if (target) return `${sleepShort(item.label)}. ${item.value} percent. This is within the recommended sleep target.`
  if (low) return `${sleepShort(item.label)}. ${item.value} percent. This is below the recommended sleep target.`

  return `${sleepShort(item.label)}. ${item.value} percent.`
}

// Builds readable text for trend chart points.
function getTrendPointReadableText(metric, pt) {
  return `${metric.label}. ${pt.year}. ${pt.val} percent.`
}
</script>