<template>
  <div class="stats-page">
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
      <!-- Loading -->
      <div v-if="insightsLoading" class="state-view">
        <div class="leaf-spinner">
          <svg viewBox="0 0 60 60" fill="none">
            <path d="M30 8C17 18 14 28 30 52C46 28 43 18 30 8Z" fill="#276d45" opacity="0.15"/>
            <path d="M30 8C17 18 14 28 30 52C46 28 43 18 30 8Z" stroke="#276d45" stroke-width="2" stroke-dasharray="120" stroke-dashoffset="120" class="leaf-draw"/>
          </svg>
        </div>
        <p>Getting your insights ready...</p>
      </div>

      <!-- Error -->
      <div v-else-if="insightsError" class="state-view state-error">
        <p>{{ insightsError }}</p>
        <button class="pill-btn" @click="fetchInsights">Try again</button>
      </div>

      <template v-else>
        <!-- Hero -->
        <section class="hero">
          <div class="hero-copy" :class="{ 'is-visible': heroVisible }">
            <p class="eyebrow"><span class="eyebrow-dot"></span>Australia · Children aged 5-12</p>
            <h1>The health<br/>  <em>picture</em> for<br/>Australian kids</h1>
            <p class="hero-sub">Select a topic below to explore the numbers - and what they mean for your family.</p>
          </div>

          <div class="gender-toggle" :class="{ 'is-visible': heroVisible }">
            <p class="toggle-label">Viewing data for</p>
            <div class="toggle-pills">
              <button
                v-for="g in genders"
                :key="g.value"
                class="toggle-pill"
                :class="{ active: selectedGender === g.value }"
                @click="selectedGender = g.value"
              >
                {{ g.label }}
              </button>
            </div>
          </div>
        </section>

        <!-- Explorer -->
        <section class="insight-explorer">
          <div class="explorer-tabs">
            <button
              v-for="(tab, i) in tabs"
              :key="tab.key"
              class="explorer-tab"
              :class="{ active: activeTab === i }"
              @click="setTab(i)"
            >
              <span class="tab-icon">{{ tab.icon }}</span>
              <span class="tab-label">{{ tab.label }}</span>
              <span class="tab-dot" :style="{ background: tab.color }"></span>
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
                <div class="bmi-cards">
                  <button
                    v-for="item in bmiChartData"
                    :key="item.key"
                    class="bmi-cat-card"
                    :class="{ active: selectedBmi === item.key }"
                    :style="{ '--accent': item.color }"
                    @click="selectedBmi = selectedBmi === item.key ? null : item.key"
                  >
                    <div class="cat-swatch" :style="{ background: item.color }"></div>
                    <div class="cat-body">
                      <span class="cat-name">{{ item.label }}</span>
                      <strong class="cat-pct">{{ item.value }}%</strong>
                      <span class="cat-count">{{ item.count }}k kids</span>
                    </div>
                    <div class="cat-arrow">
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path :d="selectedBmi===item.key ? 'M4 6l4 4 4-4' : 'M6 4l4 4-4 4'" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </div>
                    <transition name="expand-note">
                      <div v-if="selectedBmi === item.key" class="cat-note">{{ bmiNoteFor(item) }}</div>
                    </transition>
                  </button>
                </div>
              </div>
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
              <div class="activity-type-pills">
                <button
                  v-for="a in activityTypes"
                  :key="a.value"
                  class="activity-pill"
                  :class="{ active: selectedActivity === a.value }"
                  @click="selectedActivity = a.value"
                >{{ a.label }}</button>
              </div>
              <div class="activity-bars">
                <div
                  v-for="(item, i) in orderedActivityBands"
                  :key="item.label"
                  class="act-bar-card"
                  :class="{ highlight: activityFocusBand && item.label === activityFocusBand.label }"
                  :style="{ animationDelay: `${i * 0.07}s` }"
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
              <div class="activity-type-pills">
                <button
                  v-for="s in sleepTypes"
                  :key="s.value"
                  class="activity-pill"
                  :class="{ active: selectedSleep === s.value }"
                  @click="selectedSleep = s.value"
                >{{ s.label }}</button>
              </div>
              <div class="sleep-grid">
                <div
                  v-for="(item, i) in orderedSleepBands"
                  :key="item.label"
                  class="sleep-card"
                  :class="{ 'sleep-card--good': isSleepTargetBand(item.label), 'sleep-card--low': isLowSleepBand(item.label) }"
                  :style="{ animationDelay: `${i * 0.08}s` }"
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
              <div class="chart-scroll">
                <svg viewBox="0 0 580 260" class="line-svg">
                  <line v-for="y in gridYs" :key="'g'+y" x1="52" :y1="tY(y)" x2="548" :y2="tY(y)" class="grid-line"/>
                  <text v-for="y in gridYs" :key="'l'+y" x="44" :y="tY(y)+4" text-anchor="end" class="axis-lbl">{{ y }}%</text>
                  <path :d="areaPath('overweight_obese_6_13')" class="area-fill"/>
                  <path :d="linePath('overweight_obese_6_13')" fill="none" stroke="#276d45" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" class="trend-line"/>
                  <path :d="linePath('obese_6_13')" fill="none" stroke="#7a5c1e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="trend-line" style="animation-delay:.2s"/>
                  <path :d="linePath('underweight_6_13')" fill="none" stroke="#7aab8a" stroke-width="1.8" stroke-dasharray="6 4" stroke-linecap="round" stroke-linejoin="round" class="trend-line" style="animation-delay:.4s"/>
                  <template v-for="metric in trendMetrics" :key="metric.key">
                    <circle
                      v-for="pt in trendPoints(metric.key)" :key="pt.year"
                      :cx="pt.x" :cy="pt.y" r="5"
                      :fill="metric.color" stroke="white" stroke-width="2.5"
                      class="trend-dot"
                      @mouseenter="trendHover = { metric, pt }"
                      @mouseleave="trendHover = null"
                    />
                  </template>
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
              <div class="trend-legend">
                <span v-for="m in trendMetrics" :key="m.key" class="leg-item">
                  <i :style="{ background: m.color }"></i>{{ m.label }}
                </span>
              </div>
            </div>

          </transition>

          <div class="step-nav">
            <button
              v-for="(tab, i) in tabs"
              :key="i"
              class="step-dot"
              :class="{ active: activeTab === i }"
              :style="activeTab === i ? { background: tab.color } : {}"
              @click="setTab(i)"
              :aria-label="tab.label"
            ></button>
          </div>
        </section>

        <!-- Quick facts -->
        <section class="fact-strip">
          <div
            v-for="(fact, i) in quickFacts"
            :key="i"
            class="fact-card"
            :style="{ '--c': fact.color, animationDelay: `${i * 0.1}s` }"
          >
            <div class="fact-icon-wrap" :style="{ color: fact.color }">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path :d="fact.svgPath" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <strong class="fact-num">{{ fact.num }}</strong>
            <p class="fact-text">{{ fact.text }}</p>
          </div>
        </section>
      </template>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'

const API_BASE_URL = import.meta.env.VITE_PARENT_DATA_INSIGHTS_API_BASE_URL

const selectedGender   = ref('all')
const selectedActivity = ref('inactivity')
const selectedSleep    = ref('weeknight')
const selectedBmi      = ref(null)
const trendHover       = ref(null)
const activeTab        = ref(0)
const heroVisible      = ref(false)

const insightsLoading = ref(false)
const insightsError   = ref('')
const insightsData    = ref({
  bmi:      { all: [], boys: [], girls: [] },
  trend:    { all: [], boys: [], girls: [] },
  activity: { inactivity: [], light: [], moderate_vigorous: [] },
  sleep:    { weeknight: [], weekend: [], overall: [] },
})

const COLORS = {
  underweight: '#7aab8a',
  normal:      '#276d45',
  overweight:  '#c4850a',
  obese:       '#8b3a3a',
}

const trendMetrics = [
  { key: 'overweight_obese_6_13', label: 'Overweight + obese', color: '#276d45' },
  { key: 'obese_6_13',            label: 'Obese only',          color: '#7a5c1e' },
  { key: 'underweight_6_13',      label: 'Underweight',         color: '#7aab8a' },
]

const genders = [
  { value: 'all',   label: 'All children', icon: '' },
  { value: 'boys',  label: 'Boys',         icon: '' },
  { value: 'girls', label: 'Girls',        icon: '' },
]

const tabs = [
  { key: 'bmi',      label: 'Weight',   icon: '', color: '#1e6640' },
  { key: 'activity', label: 'Activity', icon: '', color: '#a86c00' },
  { key: 'sleep',    label: 'Sleep',    icon: '', color: '#2d5f82' },
  { key: 'trend',    label: 'Trend',    icon: '', color: '#6a9e7a' },
]

const activityTypes = [
  { value: 'inactivity',        label: 'Inactivity',        icon: '' },
  { value: 'light',             label: 'Light activity',    icon: '' },
  { value: 'moderate_vigorous', label: 'Active & vigorous', icon: '' },
]

const sleepTypes = [
  { value: 'weeknight', label: 'Weeknights', icon: '' },
  { value: 'weekend',   label: 'Weekends',   icon: '' },
  { value: 'overall',   label: 'Per night',  icon: '' },
]

const gridYs = [0, 10, 20, 30]

onMounted(() => {
  fetchInsights()
  setTimeout(() => { heroVisible.value = true }, 80)
})

watch([selectedGender], () => { selectedBmi.value = null })

function setTab(i) { activeTab.value = i; selectedBmi.value = null }

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
function normBmi(rows) {
  if (!Array.isArray(rows)) return []
  return rows.map(r => ({ key: r.key, label: r.label || r.key, count: Number(r.count||0), value: Number(r.value||0) }))
}
function normVal(rows) {
  if (!Array.isArray(rows)) return []
  return rows.map(r => ({ label: r.label||'', value: Number(r.value||0) }))
}

const bmiChartData = computed(() =>
  (insightsData.value.bmi[selectedGender.value] || []).map(item => ({ ...item, color: COLORS[item.key] || '#7aab8a' }))
)
const overweightVal = computed(() => bmiChartData.value.find(i => i.key==='overweight')?.value || 0)
const obeseVal      = computed(() => bmiChartData.value.find(i => i.key==='obese')?.value || 0)
const combinedVal   = computed(() => Math.round((overweightVal.value + obeseVal.value) * 10) / 10)
const trendLabel    = computed(() =>
  selectedGender.value==='boys' ? 'Boys' : selectedGender.value==='girls' ? 'Girls' : 'All children'
)
const trendRows     = computed(() => insightsData.value.trend[selectedGender.value] || [])
const trendYears    = computed(() => trendRows.value.map(r => r.year))
const activityBands = computed(() => insightsData.value.activity[selectedActivity.value] || [])
const sleepBands    = computed(() => insightsData.value.sleep[selectedSleep.value] || [])
const orderedActivityBands = computed(() => [...activityBands.value].sort((a,b) => actOrder(a.label)-actOrder(b.label)))
const orderedSleepBands    = computed(() => [...sleepBands.value].sort((a,b) => sleepOrder(a.label)-sleepOrder(b.label)))
const activityMaxVal       = computed(() => Math.max(...activityBands.value.map(i => i.value), 1))
const activityFocusBand    = computed(() => {
  if (!activityBands.value.length) return null
  return activityBands.value.reduce((h,i) => i.value > h.value ? i : h)
})
const sleepTargetPct = computed(() =>
  sleepBands.value.filter(i => /9 to less than 10|10 hours or more/i.test(i.label))
    .reduce((s,i) => s+i.value, 0).toFixed(1)
)
const sleepTargetPctNumber = computed(() => Number(sleepTargetPct.value || 0))

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

const quickFacts = computed(() => [
  { svgPath: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z', num: `${combinedVal.value}%`, text: `of ${trendLabel.value.toLowerCase()} are above a healthy weight`, color: '#1e6640' },
  { svgPath: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z', num: `${sleepTargetPct.value}%`, text: 'reach the recommended 9-11 hours of sleep per night', color: '#2d5f82' },
  { svgPath: 'M13 2L3 14h9l-1 8 10-12h-9l1-8z', num: `${activityFocusBand.value?.value||0}%`, text: `in the most common ${activityTypes.find(a=>a.value===selectedActivity.value)?.label.toLowerCase()} band`, color: '#a86c00' },
])

const activityInsight = computed(() => {
  if (selectedActivity.value==='inactivity')
    return 'Reducing inactive time - even by 30 minutes per day - is linked to better sleep and a healthier weight for children.'
  if (selectedActivity.value==='light')
    return 'Light activity like walking or playing outside counts! Every bit of movement helps build healthy habits early.'
  return 'Vigorous play - running, swimming, team sports - is the most beneficial for heart health and mood.'
})

function tX(year) {
  const years = trendYears.value
  if (years.length <= 1) return 60
  return 60 + (years.indexOf(year) / (years.length - 1)) * 478
}
function tY(value)  { return 225 - (Number(value||0) / 35) * 190 }
function trendPoints(metric) {
  return trendRows.value.map(row => ({ x: tX(row.year), y: tY(row[metric]), val: row[metric], year: row.year }))
}
function linePath(metric) {
  const pts = trendPoints(metric)
  if (!pts.length) return ''
  return pts.map((p,i) => (i===0?`M${p.x},${p.y}`:`L${p.x},${p.y}`)).join(' ')
}
function areaPath(metric) {
  const pts = trendPoints(metric)
  if (!pts.length) return ''
  const line = pts.map((p,i) => (i===0?`M${p.x},${p.y}`:`L${p.x},${p.y}`)).join(' ')
  return `${line} L${pts.at(-1).x},225 L${pts[0].x},225 Z`
}
function ttX(x) { return x > 400 ? x - 170 : x + 14 }
function cleanBarWidth(value, max) { return Math.max(4, (Number(value||0)/max)*100) }
function actColor(value) {
  if (value >= 35) return '#276d45'
  if (value >= 20) return '#3a8f5e'
  if (value >= 10) return '#c4850a'
  return '#8b3a3a'
}
function shorten(label) {
  return String(label||'').replace('Less than','<').replace('to less than','-')
    .replace(' hours','h').replace(' hour','h').replace(' minutes','min').replace(' or more','+')
}
function sleepShort(label) { return shorten(label) }
function bmiNoteFor(item) {
  const map = {
    underweight: 'Children here may benefit from nutritional support. A GP can give personalised guidance.',
    normal:      'Great news - these kids are in a healthy weight range. Keeping current routines going is the key.',
    overweight:  `${item.value}% of ${trendLabel.value.toLowerCase()} fall here. Small lifestyle changes can help reverse this trend.`,
    obese:       `This is the highest-risk category. HealthyKids routines are built to support families with gradual, lasting changes.`,
  }
  return map[item.key] || `${item.value}% of ${trendLabel.value.toLowerCase()} are in this category.`
}
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
function sleepOrder(label) {
  const t = String(label||'').toLowerCase()
  if (t.includes('less than 6')) return 1; if (t.includes('6 to less than 7')) return 2
  if (t.includes('7 to less than 8')) return 3; if (t.includes('8 to less than 9')) return 4
  if (t.includes('9 to less than 10')) return 5; if (t.includes('10 hours or more')) return 6
  return 99
}
function isSleepTargetBand(label) { return /9 to less than 10|10 hours or more/i.test(label) }
function isLowSleepBand(label)    { return /less than 6|6 to less than 7|7 to less than 8|8 to less than 9/i.test(label) }
</script>

<style scoped>

.stats-page {
  --bg:          #f2ede4;
  --surface:     rgba(255, 252, 247, 0.95);
  --surface-2:   rgba(255, 252, 247, 0.6);
  --border:      rgba(18, 53, 47, 0.09);
  --border-mid:  rgba(18, 53, 47, 0.15);
  --ink:         #12352f;
  --ink-2:       #64736d;
  --ink-3:       #9aaba5;
  --green:       #236b60;
  --green-mid:   #327c70;
  --green-light: #e4f0ed;
  --green-pale:  #f0f7f5;
  --pine:        #12352f;
  --sage:        #5a9080;
  --amber:       #d96d4d;
  --amber-soft:  rgba(242, 138, 104, 0.12);
  --sky:         #3a6b8a;
  --sky-soft:    #eaf2f8;
  --warn:        #8b3a3a;
  --warn-soft:   rgba(220, 38, 38, 0.08);
  --r:           14px;
  --r-lg:        22px;
  --r-xl:        32px;
  --shadow:      0 2px 8px rgba(18, 53, 47, 0.06), 0 8px 28px rgba(18, 53, 47, 0.09);
  --shadow-lift: 0 12px 40px rgba(18, 53, 47, 0.18);

  position: relative;
  min-height: 100vh;
  background: var(--bg);
  color: var(--ink);
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
  font-size: 1rem;
  line-height: 1.6;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
a { color: inherit; text-decoration: none; }
button { border: none; background: none; font: inherit; cursor: pointer; }


.bg-layer {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(110px);
  opacity: 0.38;
}
.orb-1 { width: 680px; height: 680px; top: -200px; right: -160px; background: radial-gradient(circle, #b4d8cc, transparent 70%); }
.orb-2 { width: 500px; height: 500px; bottom: -120px; left: -140px; background: radial-gradient(circle, #c8d8c8, transparent 70%); }
.orb-3 { width: 320px; height: 320px; top: 50%; left: 42%; opacity: 0.2; background: radial-gradient(circle, #b8d0e4, transparent 70%); }


.site-header {
  position: sticky;
  top: 0;
  z-index: 50;
  height: 68px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 0 clamp(20px, 5vw, 56px);
  background: rgba(242, 237, 228, 0.82);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.18rem;
  font-weight: 400;
  letter-spacing: -0.03em;
}
.brand-icon {
  width: 32px;
  height: 32px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: white;
  border: 1px solid var(--border);
  color: var(--green);
  box-shadow: 0 1px 4px rgba(18,53,47,.1);
}
.brand-icon svg { width: 19px; height: 19px; }

.nav { display: flex; gap: 2px; }
.nav a {
  padding: 6px 14px;
  border-radius: 999px;
  color: var(--ink-2);
  font-size: 0.84rem;
  font-weight: 700;
  transition: background .15s, color .15s;
}
.nav a:hover, .nav a.router-link-active { background: white; color: var(--ink); }

.back-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  border-radius: 999px;
  background: white;
  border: 1px solid var(--border);
  color: var(--ink);
  font-size: 0.84rem;
  font-weight: 700;
  box-shadow: 0 1px 4px rgba(18,53,47,.07);
  transition: box-shadow .18s, transform .18s;
}
.back-link:hover { box-shadow: var(--shadow); transform: translateY(-1px); }


.page-main {
  position: relative;
  z-index: 2;
  width: min(1140px, calc(100% - 40px));
  margin: 0 auto;
  padding: 40px 0 100px;
}


.state-view {
  min-height: 320px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  border-radius: var(--r-xl);
  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  text-align: center;
  padding: 48px;
  color: var(--ink-2);
}
.state-error { border-color: rgba(139,58,58,.15); background: var(--warn-soft); color: var(--warn); }
.leaf-spinner svg { width: 56px; height: 56px; }
.leaf-draw { animation: leafDraw 1.6s ease infinite alternate; }
@keyframes leafDraw { from { stroke-dashoffset: 120; } to { stroke-dashoffset: 0; } }

.eyebrow {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--green);
  margin-bottom: 10px;
}
.eyebrow-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--green);
  flex-shrink: 0;
}


.hero {
  display: grid;
  grid-template-columns: 1fr 288px;
  gap: 20px;
  align-items: stretch;
  margin-bottom: 20px;
}

.hero-copy {
  padding: 32px 36px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-xl);
  box-shadow: var(--shadow);
  opacity: 0;
  transform: translateY(14px);
  transition: opacity .6s ease, transform .6s ease;
}
.hero-copy.is-visible { opacity: 1; transform: none; }

.hero-copy h1 {
  font-family: 'Fraunces', Georgia, serif;
  font-size: clamp(2.2rem, 3.8vw, 3.6rem);
  font-weight: 400;
  line-height: 1.03;
  letter-spacing: -0.05em;
  color: var(--pine);
  margin-bottom: 14px;
}
.hero-copy h1 em { font-style: italic; color: var(--green); }
.hero-sub {
  color: var(--ink-2);
  font-size: 1rem;
  line-height: 1.65;
  max-width: 480px;
}

.gender-toggle {
  padding: 24px 26px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-xl);
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  justify-content: center;
  opacity: 0;
  transform: translateY(14px);
  transition: opacity .6s .1s ease, transform .6s .1s ease;
}
.gender-toggle.is-visible { opacity: 1; transform: none; }

.toggle-label {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--ink-3);
  margin-bottom: 12px;
}
.toggle-pills { display: flex; flex-direction: column; gap: 8px; }
.toggle-pill {
  display: flex;
  align-items: center;
  padding: 11px 14px;
  border-radius: var(--r);
  background: rgba(255,252,247,.7);
  border: 1px solid var(--border);
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--ink-2);
  transition: all .18s ease;
}
.toggle-pill:hover { background: var(--green-pale); color: var(--ink); }
.toggle-pill.active {
  background: var(--green-pale);
  border-color: var(--green);
  color: var(--green);
}


.insight-explorer {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r-xl);
  box-shadow: var(--shadow);
  overflow: hidden;
  margin-bottom: 20px;
}

.explorer-tabs {
  display: flex;
  border-bottom: 1px solid var(--border);
  background: rgba(255, 252, 247, 0.6);
}
.explorer-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 12px;
  font-size: 0.84rem;
  font-weight: 700;
  color: var(--ink-2);
  border-bottom: 2.5px solid transparent;
  transition: color .18s, border-color .18s, background .18s;
}
.explorer-tab:hover { background: rgba(255,255,255,.7); color: var(--ink); }
.explorer-tab.active { background: white; color: var(--ink); border-bottom-color: var(--green); }
.tab-icon { font-size: 0.95rem; }
.tab-dot { width: 5px; height: 5px; border-radius: 50%; opacity: 0; transition: opacity .2s; flex-shrink: 0; }
.explorer-tab.active .tab-dot { opacity: 1; }

.explorer-panel { padding: clamp(20px, 3vw, 34px); }

.panel-intro { margin-bottom: 22px; }
.panel-intro h2 {
  font-family: 'Fraunces', Georgia, serif;
  font-size: clamp(1.5rem, 2.5vw, 2rem);
  font-weight: 400;
  letter-spacing: -0.04em;
  line-height: 1.1;
  color: var(--pine);
  margin-bottom: 4px;
}
.panel-intro p { color: var(--ink-2); font-size: 0.96rem; line-height: 1.6; }

/* Panel transitions */
.panel-slide-enter-active { transition: opacity .32s ease, transform .32s ease; }
.panel-slide-leave-active { transition: opacity .18s ease, transform .18s ease; }
.panel-slide-enter-from { opacity: 0; transform: translateX(20px); }
.panel-slide-leave-to   { opacity: 0; transform: translateX(-12px); }


.bmi-layout { display: grid; grid-template-columns: 200px 1fr; gap: 24px; align-items: start; }
.ring-wrap { display: flex; justify-content: center; }
.ring-svg { width: 200px; height: 200px; }
.ring-big {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 30px;
  font-weight: 400;
  fill: var(--pine);
}
.ring-sub {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 10.5px;
  font-weight: 800;
  fill: var(--ink-3);
  text-transform: uppercase;
  letter-spacing: .09em;
}

.bmi-cards { display: flex; flex-direction: column; gap: 9px; }
.bmi-cat-card {
  display: grid;
  grid-template-columns: 9px 1fr auto;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border-radius: var(--r-lg);
  background: rgba(255, 252, 247, 0.7);
  border: 1px solid var(--border);
  text-align: left;
  transition: all .22s ease;
  position: relative;
  overflow: hidden;
}
.bmi-cat-card:hover {
  background: white;
  box-shadow: var(--shadow);
  transform: translateX(3px);
}
.bmi-cat-card.active {
  border-color: var(--accent, var(--green));
  background: white;
  box-shadow: var(--shadow);
}
.cat-swatch { width: 9px; height: 44px; border-radius: 5px; flex-shrink: 0; }
.cat-body { display: flex; flex-direction: column; gap: 2px; }
.cat-name {
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--ink-2);
}
.cat-pct {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.75rem;
  font-weight: 400;
  line-height: 1;
  color: var(--ink);
}
.cat-count { font-size: 0.78rem; font-weight: 600; color: var(--ink-3); }
.cat-arrow { color: var(--ink-3); flex-shrink: 0; transition: color .2s; }
.bmi-cat-card.active .cat-arrow { color: var(--accent, var(--green)); }
.cat-note {
  grid-column: 1 / -1;
  padding: 11px 13px;
  margin-top: 6px;
  border-radius: var(--r);
  background: var(--green-pale);
  border: 1px solid rgba(35, 107, 96, 0.12);
  font-size: 0.88rem;
  line-height: 1.65;
  color: var(--ink-2);
}
.expand-note-enter-active, .expand-note-leave-active { transition: opacity .22s ease, transform .22s ease; }
.expand-note-enter-from, .expand-note-leave-to { opacity: 0; transform: translateY(-5px); }

.affirmation-strip {
  display: flex;
  align-items: flex-start;
  gap: 11px;
  margin-top: 20px;
  padding: 14px 18px;
  border-radius: var(--r-lg);
  background: var(--amber-soft);
  border: 1px solid rgba(242, 138, 104, 0.18);
}
.aff-icon { color: var(--amber); flex-shrink: 0; margin-top: 1px; }
.affirmation-strip p {
  font-size: 0.92rem;
  line-height: 1.65;
  color: var(--ink-2);
  font-weight: 600;
}

.activity-type-pills { display: flex; gap: 7px; flex-wrap: wrap; margin-bottom: 20px; }
.activity-pill {
  padding: 7px 16px;
  border-radius: 999px;
  background: rgba(255,252,247,.8);
  border: 1px solid var(--border);
  font-size: 0.84rem;
  font-weight: 700;
  color: var(--ink-2);
  transition: all .18s ease;
}
.activity-pill:hover { background: white; color: var(--ink); box-shadow: var(--shadow); }
.activity-pill.active {
  background: var(--green);
  border-color: var(--green);
  color: white;
}

.activity-bars { display: flex; flex-direction: column; gap: 9px; }
.act-bar-card {
  display: grid;
  grid-template-columns: 108px 1fr 54px;
  gap: 12px;
  align-items: center;
  padding: 12px 16px;
  border-radius: var(--r-lg);
  background: rgba(255, 252, 247, 0.7);
  border: 1px solid var(--border);
  position: relative;
  animation: fadeSlide .35s ease both;
  transition: background .18s, box-shadow .18s;
}
.act-bar-card:hover { background: white; box-shadow: var(--shadow); }
.act-bar-card.highlight {
  border-color: rgba(217, 109, 77, 0.3);
  background: var(--amber-soft);
}
@keyframes fadeSlide { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: none; } }
.act-bar-label { font-size: 0.82rem; font-weight: 700; color: var(--ink-2); }
.act-bar-track { height: 8px; border-radius: 999px; background: rgba(18,53,47,.07); overflow: hidden; }
.act-bar-fill { height: 100%; border-radius: inherit; transition: width .7s ease; }
.act-bar-pct { font-size: 0.9rem; font-weight: 800; color: var(--ink); text-align: right; }
.act-bar-badge {
  position: absolute;
  right: 62px;
  top: -9px;
  padding: 2px 10px;
  border-radius: 999px;
  background: var(--amber);
  color: white;
  font-size: 0.66rem;
  font-weight: 800;
  letter-spacing: .06em;
  text-transform: uppercase;
}

.sleep-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(112px, 1fr));
  gap: 10px;
  margin-bottom: 20px;
}
.sleep-card {
  padding: 18px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 7px;
  border-radius: var(--r-lg);
  text-align: center;
  background: rgba(139,58,58,.05);
  border: 1px solid rgba(139,58,58,.12);
  color: var(--warn);
  animation: fadeUp .35s ease both;
  transition: transform .18s ease, box-shadow .18s ease;
  position: relative;
}
.sleep-card:hover { transform: translateY(-3px); box-shadow: var(--shadow); }
.sleep-card--good {
  background: rgba(35, 107, 96, 0.06);
  border-color: rgba(35, 107, 96, 0.18);
  color: var(--green);
}
@keyframes fadeUp { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
.sleep-moon { display: flex; align-items: center; justify-content: center; opacity: 0.75; }
.sleep-pct {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.75rem;
  font-weight: 400;
  line-height: 1;
}
.sleep-label {
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: .04em;
  opacity: 0.8;
}
.sleep-badge {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  padding: 2px 10px;
  border-radius: 999px;
  background: var(--green);
  color: white;
  font-size: 0.66rem;
  font-weight: 800;
  white-space: nowrap;
  letter-spacing: .04em;
}
.sleep-target-note { margin-bottom: 16px; }
.target-bar { height: 7px; border-radius: 999px; background: rgba(18,53,47,.08); overflow: hidden; margin-bottom: 9px; }
.target-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--green-mid), var(--green));
  border-radius: inherit;
  transition: width .8s ease;
}
.sleep-target-note p { font-size: 0.9rem; color: var(--ink-2); }
.sleep-target-note strong { color: var(--green); font-weight: 700; }


.chart-scroll { overflow-x: auto; margin-bottom: 16px; }
.line-svg { width: 100%; min-width: 460px; display: block; overflow: visible; }
.grid-line { stroke: rgba(18,53,47,.06); stroke-width: 1; }
.area-fill { fill: rgba(35,107,96,.07); }
.axis-lbl {
  fill: var(--ink-3);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 10.5px;
  font-weight: 700;
}
.trend-line { stroke-dasharray: 1200; stroke-dashoffset: 1200; animation: draw 1.4s ease forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }
.trend-dot { cursor: pointer; transition: r .15s; }
.trend-dot:hover { r: 7; }
.hover-rule { stroke: rgba(18,53,47,.1); stroke-dasharray: 4 3; }
.tt-label { fill: var(--ink-2); font-family: 'Plus Jakarta Sans', sans-serif; font-size: 10.5px; font-weight: 800; }
.tt-val   { fill: var(--ink);   font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px;   font-weight: 800; }
.trend-legend { display: flex; flex-wrap: wrap; gap: 16px; padding-top: 14px; border-top: 1px solid var(--border); }
.leg-item { display: flex; align-items: center; gap: 8px; color: var(--ink-2); font-size: 0.82rem; font-weight: 700; }
.leg-item i { width: 18px; height: 2.5px; display: block; border-radius: 999px; }


.step-nav {
  display: flex;
  justify-content: center;
  gap: 9px;
  padding: 18px 0 4px;
  border-top: 1px solid var(--border);
}
.step-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--border-mid); transition: all .2s ease; }
.step-dot.active { transform: scale(1.45); }
.step-dot:hover:not(.active) { background: var(--ink-3); transform: scale(1.2); }

.fact-strip { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.fact-card {
  padding: 22px 20px;
  border-radius: var(--r-xl);
  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
  animation: fadeSlide .45s ease both;
  transition: transform .22s ease, box-shadow .22s ease;
}
.fact-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-lift); }
.fact-icon-wrap {
  width: 38px;
  height: 38px;
  border-radius: var(--r);
  display: grid;
  place-items: center;
  background: var(--green-pale);
  border: 1px solid rgba(35,107,96,.12);
  margin-bottom: 14px;
}
.fact-num {
  display: block;
  font-family: 'Fraunces', Georgia, serif;
  font-size: 2.6rem;
  font-weight: 400;
  line-height: 1;
  letter-spacing: -0.05em;
  color: var(--c, var(--green));
  margin-bottom: 6px;
}
.fact-text {
  font-size: 0.9rem;
  color: var(--ink-2);
  line-height: 1.6;
  font-weight: 600;
}

.pill-btn {
  padding: 10px 24px;
  border-radius: 999px;
  background: var(--green);
  color: white;
  font-size: 0.88rem;
  font-weight: 800;
  transition: background .18s, box-shadow .18s;
}
.pill-btn:hover { background: var(--green-mid); box-shadow: 0 4px 16px rgba(35,107,96,.28); }

/* ── Responsive ── */
@media (max-width: 900px) {
  .hero { grid-template-columns: 1fr; }
  .bmi-layout { grid-template-columns: 1fr; }
  .ring-wrap { display: none; }
  .fact-strip { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 640px) {
  .nav { display: none; }
  .tab-label { display: none; }
  .explorer-tab { padding: 14px 8px; }
  .act-bar-card { grid-template-columns: 80px 1fr 44px; }
  .fact-strip { grid-template-columns: 1fr; }
  .sleep-grid { grid-template-columns: repeat(3, 1fr); }
  .toggle-pills { flex-direction: row; flex-wrap: wrap; }
}

.stats-page {
  --bg: #f5f6f5;
  --surface: #ffffff;
  --surface-2: #f0f2f0;
  --border: rgba(26,74,48,.07);
  --border-mid: rgba(26,74,48,.13);
  --ink: #111c11;
  --ink-2: #4d5e4d;
  --ink-3: #8a9e8a;
  --green: #1e6640;
  --green-mid: #2e845a;
  --green-light: #e3eeea;
  --green-pale: #f0f7f3;
  --pine: #132e20;
  --sage: #6a9e7a;
  --amber: #a86c00;
  --amber-soft: #fdf4e3;
  --sky: #2d5f82;
  --sky-soft: #e8f1f8;
  --warn: #7a3030;
  --warn-soft: #f7eded;
  --r: 12px;
  --r-lg: 20px;
  --r-xl: 28px;
  --shadow: 0 1px 3px rgba(26,74,48,.05), 0 6px 20px rgba(26,74,48,.07);
  --shadow-lift: 0 6px 28px rgba(26,74,48,.12);

  position: relative; min-height: 100vh;
  background: var(--bg); color: var(--ink);
  font-family: 'Inter', system-ui, sans-serif;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
a { color: inherit; text-decoration: none; }
button { border: none; background: none; font: inherit; cursor: pointer; }

/* ── Background ── */
.bg-layer { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
.orb { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.4; }
.orb-1 { width: 640px; height: 640px; top: -200px; right: -160px; background: radial-gradient(circle, #a8d8b8, transparent 70%); }
.orb-2 { width: 480px; height: 480px; bottom: -100px; left: -120px; background: radial-gradient(circle, #c8dac8, transparent 70%); }
.orb-3 { width: 300px; height: 300px; top: 55%; left: 45%; opacity: 0.25; background: radial-gradient(circle, #b8d4e8, transparent 70%); }

/* ── Header ── */
.site-header {
  position: sticky; top: 0; z-index: 50; height: 60px;
  display: flex; align-items: center; justify-content: space-between; gap: 16px;
  padding: 0 clamp(16px, 5vw, 56px);
  background: rgba(245,246,245,.92); border-bottom: 1px solid var(--border);
  backdrop-filter: blur(20px);
}
.brand { display: flex; align-items: center; gap: 9px; font-family: 'Fraunces', serif; font-size: 1.05rem; letter-spacing: -0.02em; font-weight: 400; }
.brand-icon { width: 30px; height: 30px; display: grid; place-items: center; border-radius: 50%; background: white; border: 1px solid var(--border); color: var(--green); box-shadow: 0 1px 4px rgba(26,74,48,.08); }
.brand-icon svg { width: 17px; height: 17px; }
.nav { display: flex; gap: 2px; }
.nav a { padding: 5px 12px; border-radius: 8px; color: var(--ink-2); font-size: 0.82rem; font-weight: 500; transition: background .15s, color .15s; }
.nav a:hover, .nav a.router-link-active { background: white; color: var(--ink); }
.back-link {
  display: flex; align-items: center; gap: 5px;
  padding: 6px 14px; border-radius: 8px;
  background: white; border: 1px solid var(--border);
  font-size: 0.82rem; font-weight: 500; color: var(--ink-2);
  box-shadow: 0 1px 3px rgba(26,74,48,.06);
  transition: box-shadow .2s, color .2s;
}
.back-link:hover { box-shadow: var(--shadow); color: var(--ink); }

/* ── Main ── */
.page-main {
  position: relative; z-index: 2;
  width: min(1060px, calc(100% - 32px));
  margin: 0 auto; padding: 40px 0 100px;
}

/* ── State views ── */
.state-view {
  min-height: 340px; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 16px;
  border-radius: var(--r-xl); background: var(--surface);
  border: 1px solid var(--border); text-align: center; padding: 48px; color: var(--ink-2);
}
.state-error { border-color: rgba(139,58,58,.16); background: var(--warn-soft); color: var(--warn); }
.leaf-spinner svg { width: 64px; height: 64px; animation: leafSpin 2s linear infinite; }
.leaf-draw { animation: leafDraw 1.6s ease infinite alternate; }
@keyframes leafDraw { from { stroke-dashoffset: 120; } to { stroke-dashoffset: 0; } }
@keyframes leafSpin { to { transform: rotate(360deg); } }

/* ── Eyebrow ── */
.eyebrow { font-size: 0.67rem; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; color: var(--green); margin-bottom: 10px; }

/* ── Hero ── */
.hero { display: grid; grid-template-columns: 1fr 268px; gap: 20px; align-items: center; margin-bottom: 20px; }
.hero-copy { opacity: 0; transform: translateY(14px); transition: opacity .55s ease, transform .55s ease; }
.hero-copy.is-visible { opacity: 1; transform: none; }
.hero-copy h1 { font-family: 'Fraunces', serif; font-size: clamp(2.1rem, 3.8vw, 3.4rem); font-weight: 300; line-height: 1.1; letter-spacing: -0.04em; color: var(--pine); margin-bottom: 12px; }
.hero-copy h1 em { font-style: italic; color: var(--green); }
.hero-sub { color: var(--ink-2); line-height: 1.65; font-size: 0.93rem; max-width: 440px; font-weight: 400; }

.gender-toggle {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-lg); padding: 18px 20px; box-shadow: var(--shadow);
  opacity: 0; transform: translateY(14px); transition: opacity .55s .1s ease, transform .55s .1s ease;
}
.gender-toggle.is-visible { opacity: 1; transform: none; }
.toggle-label { font-size: 0.67rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--ink-3); margin-bottom: 10px; }
.toggle-pills { display: flex; flex-direction: column; gap: 6px; }
.toggle-pill {
  display: flex; align-items: center;
  padding: 9px 13px; border-radius: var(--r);
  background: var(--surface-2); border: 1.5px solid transparent;
  font-size: 0.86rem; font-weight: 500; color: var(--ink-2);
  transition: all .15s ease;
}
.toggle-pill:hover { background: var(--green-pale); color: var(--ink); }
.toggle-pill.active { background: var(--green-pale); border-color: var(--green); color: var(--green); font-weight: 600; }

/* ── Explorer ── */
.insight-explorer {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--r-lg); box-shadow: var(--shadow);
  overflow: hidden; margin-bottom: 20px;
}
.explorer-tabs { display: flex; border-bottom: 1px solid var(--border); background: var(--surface-2); }
.explorer-tab {
  flex: 1; display: flex; align-items: center; justify-content: center; gap: 7px;
  padding: 14px 10px; font-size: 0.82rem; font-weight: 500; color: var(--ink-2);
  border-bottom: 2px solid transparent;
  transition: color .18s, border-color .18s, background .18s;
}
.explorer-tab:hover { background: rgba(255,255,255,.7); color: var(--ink); }
.explorer-tab.active { background: var(--surface); color: var(--ink); border-bottom-color: var(--green); font-weight: 600; }
.tab-icon { font-size: 0.95rem; }
.tab-dot { width: 5px; height: 5px; border-radius: 50%; opacity: 0; transition: opacity .2s; flex-shrink: 0; }
.explorer-tab.active .tab-dot { opacity: 1; }

.explorer-panel { padding: clamp(18px, 2.8vw, 32px); }
.panel-intro { margin-bottom: 20px; }
.panel-intro h2 { font-family: 'Fraunces', serif; font-size: clamp(1.3rem, 2.2vw, 1.75rem); font-weight: 300; letter-spacing: -0.03em; color: var(--pine); margin-bottom: 3px; }
.panel-intro p { color: var(--ink-3); font-size: 0.86rem; font-weight: 400; }

.panel-slide-enter-active { transition: opacity .35s ease, transform .35s ease; }
.panel-slide-leave-active { transition: opacity .2s ease, transform .2s ease; }
.panel-slide-enter-from { opacity: 0; transform: translateX(24px); }
.panel-slide-leave-to   { opacity: 0; transform: translateX(-16px); }

/* ── BMI ── */
.bmi-layout { display: grid; grid-template-columns: 200px 1fr; gap: 24px; align-items: start; }
.ring-wrap { display: flex; justify-content: center; }
.ring-svg { width: 200px; height: 200px; }
.ring-big { font-family: 'Fraunces', serif; font-size: 28px; font-weight: 400; fill: var(--pine); }
.ring-sub { font-family: 'Nunito', sans-serif; font-size: 10px; font-weight: 700; fill: var(--ink-3); text-transform: uppercase; letter-spacing: .08em; }

.bmi-cards { display: flex; flex-direction: column; gap: 8px; }
.bmi-cat-card {
  display: grid; grid-template-columns: 8px 1fr auto;
  align-items: center; gap: 14px;
  padding: 13px 15px; border-radius: var(--r);
  background: var(--surface-2); border: 1.5px solid transparent;
  text-align: left; transition: all .2s ease; position: relative; overflow: hidden;
}
.bmi-cat-card:hover { background: white; box-shadow: var(--shadow); transform: translateX(2px); }
.bmi-cat-card.active { border-color: var(--accent, var(--green)); background: white; box-shadow: var(--shadow); }
.cat-swatch { width: 8px; height: 40px; border-radius: 4px; flex-shrink: 0; }
.cat-body { display: flex; flex-direction: column; gap: 1px; }
.cat-name { font-size: 0.72rem; font-weight: 600; letter-spacing: .05em; text-transform: uppercase; color: var(--ink-2); }
.cat-pct { font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 400; line-height: 1; color: var(--ink); }
.cat-count { font-size: 0.74rem; font-weight: 400; color: var(--ink-3); }
.cat-arrow { color: var(--ink-3); flex-shrink: 0; transition: color .2s; }
.bmi-cat-card.active .cat-arrow { color: var(--accent, var(--green)); }
.cat-note {
  grid-column: 1 / -1; padding: 10px 12px; margin-top: 4px;
  border-radius: 8px; background: var(--green-pale); border: 1px solid var(--border);
  font-size: 0.84rem; line-height: 1.6; color: var(--ink-2); font-weight: 400;
}
.expand-note-enter-active, .expand-note-leave-active { transition: opacity .2s ease, transform .2s ease; }
.expand-note-enter-from, .expand-note-leave-to { opacity: 0; transform: translateY(-4px); }

/* ── Affirmation ── */
.affirmation-strip {
  display: flex; align-items: flex-start; gap: 11px;
  margin-top: 18px; padding: 13px 16px;
  border-radius: var(--r); background: var(--green-pale); border: 1px solid rgba(30,102,64,.12);
}
.aff-icon { color: var(--green); flex-shrink: 0; margin-top: 1px; }
.affirmation-strip p { font-size: 0.85rem; line-height: 1.6; color: var(--ink-2); font-weight: 400; }

/* ── Activity pills ── */
.activity-type-pills { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 18px; }
.activity-pill {
  padding: 7px 15px; border-radius: var(--r);
  background: var(--surface-2); border: 1.5px solid transparent;
  font-size: 0.82rem; font-weight: 500; color: var(--ink-2);
  transition: all .15s ease;
}
.activity-pill:hover { background: var(--green-pale); color: var(--ink); }
.activity-pill.active { background: var(--green-pale); border-color: var(--green); color: var(--green); font-weight: 600; }

/* ── Activity bars ── */
.activity-bars { display: flex; flex-direction: column; gap: 8px; }
.act-bar-card {
  display: grid; grid-template-columns: 100px 1fr 52px;
  gap: 12px; align-items: center;
  padding: 11px 14px; border-radius: var(--r);
  background: var(--surface-2); border: 1.5px solid transparent;
  animation: fadeSlide .35s ease both; position: relative;
  transition: background .18s, box-shadow .18s;
}
.act-bar-card:hover { background: white; box-shadow: var(--shadow); }
.act-bar-card.highlight { border-color: rgba(168,108,0,.25); background: var(--amber-soft); }
@keyframes fadeSlide { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: none; } }
.act-bar-label { font-size: 0.79rem; font-weight: 500; color: var(--ink-2); }
.act-bar-track { height: 8px; border-radius: 999px; background: rgba(26,74,48,.07); overflow: hidden; }
.act-bar-fill { height: 100%; border-radius: inherit; transition: width .7s ease; }
.act-bar-pct { font-size: 0.86rem; font-weight: 600; color: var(--ink); text-align: right; }
.act-bar-badge {
  position: absolute; right: 60px; top: -9px;
  padding: 2px 9px; border-radius: 4px;
  background: var(--amber); color: white;
  font-size: 0.65rem; font-weight: 600; letter-spacing: .05em; text-transform: uppercase;
}

.sleep-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: 8px; margin-bottom: 18px; }
.sleep-card {
  padding: 16px 10px; display: flex; flex-direction: column; align-items: center; gap: 6px;
  border-radius: var(--r-lg); text-align: center;
  background: rgba(122,48,48,.05); border: 1px solid rgba(122,48,48,.1); color: var(--warn);
  animation: fadeUp .35s ease both;
  transition: transform .18s ease, box-shadow .18s ease; position: relative;
}
.sleep-card:hover { transform: translateY(-3px); box-shadow: var(--shadow); }
.sleep-card--good { background: rgba(30,102,64,.06); border-color: rgba(30,102,64,.16); color: var(--green); }
@keyframes fadeUp { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
.sleep-moon { display: flex; align-items: center; justify-content: center; opacity: 0.7; }
.sleep-pct { font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 300; line-height: 1; }
.sleep-label { font-size: 0.7rem; font-weight: 500; letter-spacing: .03em; color: currentColor; opacity: 0.8; }
.sleep-badge {
  position: absolute; top: -9px; left: 50%; transform: translateX(-50%);
  padding: 2px 9px; border-radius: 4px;
  background: var(--green); color: white;
  font-size: 0.64rem; font-weight: 600; white-space: nowrap; letter-spacing: .04em;
}
.sleep-target-note { margin-bottom: 14px; }
.target-bar { height: 6px; border-radius: 999px; background: var(--surface-2); overflow: hidden; margin-bottom: 8px; }
.target-bar-fill { height: 100%; background: linear-gradient(90deg, var(--green-mid), var(--green)); border-radius: inherit; transition: width .8s ease; }
.sleep-target-note p { font-size: 0.85rem; color: var(--ink-2); font-weight: 400; }
.sleep-target-note strong { color: var(--green); font-weight: 600; }


.chart-scroll { overflow-x: auto; margin-bottom: 16px; }
.line-svg { width: 100%; min-width: 460px; display: block; overflow: visible; }
.grid-line { stroke: rgba(26,74,48,.06); stroke-width: 1; }
.area-fill { fill: rgba(39,109,69,.07); }
.axis-lbl { fill: var(--ink-3); font-family: 'Inter', sans-serif; font-size: 10px; font-weight: 600; }
.trend-line { stroke-dasharray: 1200; stroke-dashoffset: 1200; animation: draw 1.4s ease forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }
.trend-dot { cursor: pointer; transition: r .15s; }
.trend-dot:hover { r: 7; }
.hover-rule { stroke: rgba(26,74,48,.09); stroke-dasharray: 4 3; }
.tt-label { fill: var(--ink-2); font-family: 'Inter', sans-serif; font-size: 10px; font-weight: 600; }
.tt-val   { fill: var(--ink);   font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600; }
.trend-legend { display: flex; flex-wrap: wrap; gap: 14px; padding-top: 14px; border-top: 1px solid var(--border); }
.leg-item { display: flex; align-items: center; gap: 7px; color: var(--ink-2); font-size: 0.79rem; font-weight: 500; }
.leg-item i { width: 16px; height: 2px; display: block; border-radius: 999px; }

.step-nav { display: flex; justify-content: center; gap: 8px; padding: 16px 0 2px; border-top: 1px solid var(--border); }
.step-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--border-mid); transition: all .2s ease; }
.step-dot.active { transform: scale(1.4); }
.step-dot:hover:not(.active) { background: var(--ink-3); transform: scale(1.15); }

.fact-strip { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.fact-card {
  padding: 20px 18px; border-radius: var(--r-lg);
  background: var(--surface); border: 1px solid var(--border); box-shadow: var(--shadow);
  animation: fadeSlide .4s ease both;
  transition: transform .2s ease, box-shadow .2s ease;
}
.fact-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-lift); }
.fact-icon-wrap {
  width: 36px; height: 36px; border-radius: var(--r);
  display: grid; place-items: center;
  background: var(--green-pale);
  margin-bottom: 12px;
}
.fact-num { display: block; font-family: 'Fraunces', serif; font-size: 2.2rem; font-weight: 300; line-height: 1; letter-spacing: -0.04em; color: var(--c, var(--green)); margin-bottom: 5px; }
.fact-text { font-size: 0.83rem; color: var(--ink-2); line-height: 1.55; font-weight: 400; }

.pill-btn { padding: 9px 22px; border-radius: var(--r); background: var(--green); color: white; font-size: 0.86rem; font-weight: 600; transition: background .18s, box-shadow .18s; }
.pill-btn:hover { background: var(--green-mid); box-shadow: 0 4px 14px rgba(30,102,64,.25); }

@media (max-width: 860px) {
  .hero { grid-template-columns: 1fr; }
  .bmi-layout { grid-template-columns: 1fr; }
  .ring-wrap { display: none; }
  .fact-strip { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 640px) {
  .nav { display: none; }
  .tab-label { display: none; }
  .explorer-tab { padding: 14px 8px; }
  .act-bar-card { grid-template-columns: 80px 1fr 42px; }
  .fact-strip { grid-template-columns: 1fr; }
  .sleep-grid { grid-template-columns: repeat(3, 1fr); }
  .toggle-pills { flex-direction: row; flex-wrap: wrap; }
}

.header {
  position: sticky;
  top: 0;
  z-index: 80;
  width: 100%;
  background: rgba(246, 239, 229, 0.88);
  border-bottom: 1px solid rgba(18, 53, 47, 0.08);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}

.header-inner {
  width: min(1160px, calc(100% - 32px));
  height: 82px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #12352f;
  font-family: 'Fraunces', Georgia, serif;
  font-size: 1.28rem;
  font-weight: 500;
  letter-spacing: -0.035em;
  white-space: nowrap;
}

.logo-icon {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  color: #236b60;
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(35, 107, 96, 0.22);
  box-shadow: 0 10px 24px rgba(18, 53, 47, 0.08);
}

.logo-icon svg {
  width: 19px;
  height: 19px;
}

.nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-a {
  padding: 10px 14px;
  border-radius: 12px;
  color: #52635d;
  font-size: 0.92rem;
  font-weight: 700;
  text-decoration: none;
  transition: background 0.18s ease, color 0.18s ease, transform 0.18s ease;
}

.nav-a:hover,
.nav-a.router-link-active {
  background: #ffffff;
  color: #12352f;
}

.nav-cta {
  display: flex;
  align-items: center;
  gap: 14px;
}

.nav-link {
  color: #52635d;
  font-size: 0.9rem;
  font-weight: 800;
  text-decoration: none;
}

.nav-link:hover {
  color: #12352f;
}

.nav-btn {
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 999px;
  background: #236b60;
  color: #ffffff;
  font-size: 0.92rem;
  font-weight: 900;
  text-decoration: none;
  box-shadow: 0 18px 38px rgba(35, 107, 96, 0.24);
  transition: transform 0.18s ease, background 0.18s ease, box-shadow 0.18s ease;
}

.nav-btn:hover {
  transform: translateY(-1px);
  background: #1d5d53;
  box-shadow: 0 22px 44px rgba(35, 107, 96, 0.3);
}
</style>