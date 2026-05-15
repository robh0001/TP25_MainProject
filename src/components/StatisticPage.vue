<template>
    <div class="stats-page">
  
      <!-- Ambient background -->
      <div class="bg" aria-hidden="true">
        <div class="bg-blob blob-a"></div>
        <div class="bg-blob blob-b"></div>
        <div class="bg-blob blob-c"></div>
        <div class="bg-grid"></div>
      </div>
  
      <!-- Header -->
      <header class="site-header">
        <RouterLink to="/" class="brand">
          <div class="brand-mark">
            <svg viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.4"/>
              <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor"/>
            </svg>
          </div>
          <span class="brand-name">HealthyKids</span>
        </RouterLink>
        <nav class="nav-links">
          <RouterLink to="/parent-dashboard">Dashboard</RouterLink>
          <RouterLink to="/parent-roadmap">Roadmap</RouterLink>
          <RouterLink to="/young-person-dashboard">Kids view</RouterLink>
        </nav>
        <RouterLink to="/parent-dashboard" class="back-btn">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><path d="M10 3L5 8L10 13" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          Back
        </RouterLink>
      </header>
  
      <main class="page-main">
  
        <!-- Hero -->
        <section class="hero">
          <div class="hero-left">
            <div class="pill">
              <span class="pill-dot"></span>
              Health statistics · Australia
            </div>
            <h1 class="hero-title">Statistics</h1>
            <p class="hero-sub">Showing data for <strong>{{ profileSummary }}</strong></p>
          </div>
          <div class="insight-card">
            <p class="insight-eyebrow">Key insight</p>
            <h2 class="insight-title">{{ assistantTitle }}</h2>
            <p class="insight-body">{{ assistantMessage }}</p>
            <div class="insight-pulse"></div>
            <div class="insight-decoration" aria-hidden="true">
              <svg viewBox="0 0 200 200" fill="none"><circle cx="100" cy="100" r="80" stroke="rgba(255,255,255,0.06)" stroke-width="1"/><circle cx="100" cy="100" r="55" stroke="rgba(255,255,255,0.06)" stroke-width="1"/><circle cx="100" cy="100" r="30" stroke="rgba(255,255,255,0.08)" stroke-width="1"/></svg>
            </div>
          </div>
        </section>
  
        <!-- KPI Row -->
        <section class="kpi-row">
          <button
            v-for="card in kpiCards"
            :key="card.id"
            class="kpi-tile"
            :class="{ 'kpi-active': activeKpi === card.id, 'kpi-warn': card.warning }"
            @click="activeKpi = activeKpi === card.id ? null : card.id"
          >
            <div class="kpi-top">
              <div class="kpi-icon-wrap" :class="card.iconBg">
                <span class="kpi-icon">{{ card.icon }}</span>
              </div>
              <svg class="kpi-chevron" :class="{ rotated: activeKpi === card.id }" width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <strong class="kpi-val">{{ card.value }}</strong>
            <span class="kpi-label">{{ card.label }}</span>
            <transition name="slide-note">
              <p v-if="activeKpi === card.id" class="kpi-detail">{{ card.detail }}</p>
            </transition>
          </button>
        </section>
  
        <!-- Filters -->
        <section class="filter-bar">
          <div class="filter-label-wrap">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none"><path d="M2 4h12M4 8h8M6 12h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
            <span class="filter-label">Filter data</span>
          </div>
          <div class="filter-chips">
            <label class="chip-select">
              <span>Gender</span>
              <select v-model="selectedGender">
                <option value="all">All children</option>
                <option value="boys">Boys</option>
                <option value="girls">Girls</option>
              </select>
            </label>
            <label class="chip-select">
              <span>Activity type</span>
              <select v-model="selectedActivity">
                <option value="inactivity">Daily inactivity</option>
                <option value="light">Light activity</option>
                <option value="moderate_vigorous">Moderate & vigorous</option>
              </select>
            </label>
            <label class="chip-select">
              <span>Sleep period</span>
              <select v-model="selectedSleep">
                <option value="weeknight">Weeknight</option>
                <option value="weekend">Weekend night</option>
                <option value="overall">Per night avg</option>
              </select>
            </label>
          </div>
          <div class="filter-active-tag" v-if="selectedGender !== 'all'">
            {{ selectedGender }}
            <button @click="selectedGender = 'all'">×</button>
          </div>
        </section>
  
        <!-- Charts -->
        <div class="charts-grid">
  
          <!-- BMI Distribution — label | bar | stat -->
          <article class="chart-card bmi-card">
            <div class="chart-head">
              <div>
                <span class="kicker">BMI distribution</span>
                <h3>{{ trendLabel }} aged 5–12</h3>
              </div>
              <div class="chart-head-badge">
                <span class="badge-dot badge-green"></span>
                {{ bmiHealthyPct }}% healthy weight
              </div>
            </div>
  
            <div class="bmi-bars">
              <div
                v-for="item in bmiChartData"
                :key="item.key"
                class="bmi-row"
                :class="{ 'bmi-selected': selectedBmi === item.key }"
                @click="selectedBmi = selectedBmi === item.key ? null : item.key"
              >
                <!-- Label column -->
                <div class="bmi-label-col">
                  <span class="bmi-dot" :style="{ background: item.color }"></span>
                  <span class="bmi-name">{{ item.label }}</span>
                </div>
                <!-- Bar column -->
                <div class="bmi-bar-col">
                  <div class="bmi-track">
                    <div
                      class="bmi-fill"
                      :style="{ width: bmiBarWidth(item) + '%', background: item.color }"
                    ></div>
                  </div>
                </div>
                <!-- Stat column -->
                <div class="bmi-stat-col">
                  <strong class="bmi-pct">{{ item.value }}%</strong>
                  <span class="bmi-count">{{ item.count }}k children</span>
                </div>
              </div>
            </div>
  
            <transition name="slide-note">
              <div v-if="selectedBmiItem" class="chart-note chart-note--bmi">
                <div class="cn-icon">{{ selectedBmiIcon }}</div>
                <div>
                  <strong>{{ selectedBmiItem.label }}</strong>
                  <p>{{ selectedBmiInsight }}</p>
                </div>
              </div>
            </transition>
  
            <div class="bmi-source">Source: ABS National Health Survey 2017–18. Children aged 5–12.</div>
          </article>
  
          <!-- Trend line chart -->
          <article class="chart-card trend-card">
            <div class="chart-head">
              <div>
                <span class="kicker">Trend over time</span>
                <h3>Weight status 2010–2016</h3>
              </div>
            </div>
            <div class="line-wrap">
              <svg viewBox="0 0 580 260" class="line-svg">
                <line v-for="y in gridYs" :key="'g'+y" x1="52" :y1="tY(y)" x2="548" :y2="tY(y)" stroke="rgba(22,48,43,.07)" stroke-width="1"/>
                <text v-for="y in gridYs" :key="'l'+y" x="44" :y="tY(y)+4" text-anchor="end" class="axis-lbl">{{ y }}%</text>
                <path :d="areaPath('overweight_obese_6_13')" fill="rgba(224,122,82,.09)" />
                <path :d="linePath('overweight_obese_6_13')" fill="none" stroke="#e07a52" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" class="trend-line" />
                <path :d="linePath('obese_6_13')"            fill="none" stroke="#dc2626" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="trend-line" style="animation-delay:.2s"/>
                <path :d="linePath('underweight_6_13')"      fill="none" stroke="#4a9d89" stroke-width="2"   stroke-dasharray="6 4" stroke-linecap="round" stroke-linejoin="round" class="trend-line" style="animation-delay:.4s"/>
                <template v-for="metric in trendMetrics" :key="metric.key">
                  <circle v-for="pt in trendPoints(metric.key)" :key="pt.year" :cx="pt.x" :cy="pt.y" r="5" :fill="metric.color" stroke="white" stroke-width="2.5" class="trend-dot" @mouseenter="trendHover = { metric, pt }" @mouseleave="trendHover = null"/>
                </template>
                <g v-if="trendHover">
                  <line :x1="trendHover.pt.x" :x2="trendHover.pt.x" y1="20" y2="225" stroke="rgba(22,48,43,.12)" stroke-dasharray="4 3"/>
                  <rect :x="ttX(trendHover.pt.x)" :y="Math.max(14, trendHover.pt.y - 56)" width="162" height="44" rx="10" fill="white" filter="url(#ttShadow)"/>
                  <text :x="ttX(trendHover.pt.x)+13" :y="Math.max(14, trendHover.pt.y-56)+17" class="tt-label">{{ trendHover.metric.label }}</text>
                  <text :x="ttX(trendHover.pt.x)+13" :y="Math.max(14, trendHover.pt.y-56)+35" class="tt-val">{{ trendHover.pt.year }} · {{ trendHover.pt.val }}%</text>
                  <defs><filter id="ttShadow" x="-10%" y="-20%" width="120%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="rgba(22,48,43,.14)"/></filter></defs>
                </g>
                <text v-for="yr in trendYears" :key="'yr'+yr" :x="tX(yr)" y="249" text-anchor="middle" class="axis-lbl">{{ yr }}</text>
              </svg>
            </div>
            <div class="trend-legend">
              <span v-for="m in trendMetrics" :key="m.key" class="leg-item">
                <i :style="{ background: m.color }"></i>{{ m.label }}
              </span>
            </div>
          </article>
  
          <!-- Activity chart -->
          <article class="chart-card activity-card">
            <div class="chart-head">
              <div>
                <span class="kicker">Physical activity</span>
                <h3>{{ activityLabel }}</h3>
              </div>
              <div class="chart-head-badge chart-head-badge--amber">
                <span class="badge-dot badge-amber"></span>
                {{ activityTopLabel }}
              </div>
            </div>
            <div class="v-bars">
              <div class="v-bar-yaxis">
                <span v-for="y in activityYTicks" :key="y">{{ y }}%</span>
              </div>
              <div class="v-bar-plot">
                <div
                  v-for="item in activityBands"
                  :key="item.label"
                  class="v-bar-col"
                  :class="{ 'v-bar-active': selectedActivityBand === item.label, 'v-bar-peak': item.value === activityMaxVal }"
                  @mouseenter="selectedActivityBand = item.label"
                  @mouseleave="selectedActivityBand = null"
                >
                  <span class="v-bar-val">{{ item.value }}%</span>
                  <div class="v-bar-track">
                    <div class="v-bar-fill" :style="{ height: actBarH(item.value, activityMaxVal) + '%', background: actColor(item.value) }"></div>
                  </div>
                  <span class="v-bar-lbl">{{ shorten(item.label) }}</span>
                </div>
              </div>
            </div>
            <transition name="slide-note">
              <div v-if="selectedActivityBand" class="chart-note">
                <strong>{{ selectedActivityBand }}</strong> — {{ selectedActivityBandValue }}% of children fall in this band.
              </div>
            </transition>
          </article>
  
          <!-- Sleep chart -->
          <article class="chart-card sleep-card">
            <div class="chart-head">
              <div>
                <span class="kicker">Sleep patterns</span>
                <h3>{{ sleepLabel }}</h3>
              </div>
              <div class="chart-head-badge chart-head-badge--indigo">
                <span class="badge-dot badge-indigo"></span>
                {{ sleepTargetPct }}% reach target
              </div>
            </div>
            <div class="v-bars">
              <div class="v-bar-yaxis">
                <span v-for="y in sleepYTicks" :key="y">{{ y }}%</span>
              </div>
              <div class="v-bar-plot">
                <div
                  v-for="item in sleepBands"
                  :key="item.label"
                  class="v-bar-col"
                  :class="{ 'v-bar-active': selectedSleepBand === item.label, 'v-bar-peak': item.value === sleepMaxVal }"
                  @mouseenter="selectedSleepBand = item.label"
                  @mouseleave="selectedSleepBand = null"
                >
                  <span class="v-bar-val">{{ item.value }}%</span>
                  <div class="v-bar-track">
                    <div class="v-bar-fill" :style="{ height: actBarH(item.value, sleepMaxVal) + '%', background: sleepColor(item.label) }"></div>
                  </div>
                  <span class="v-bar-lbl">{{ sleepShort(item.label) }}</span>
                </div>
              </div>
            </div>
            <div class="sleep-rec">
              <span class="sleep-rec-icon">ℹ️</span>
              <p>{{ selectedSleepBand ? selectedSleepBand + ': ' + selectedSleepBandValue + '% of children.' : 'School-age children need 9–11 hrs of sleep per night for healthy development.' }}</p>
            </div>
          </article>
  
        </div>
      </main>
    </div>
  </template>
  
  <script setup>
  import { computed, ref, watch } from 'vue'
  import { RouterLink } from 'vue-router'
  
  const selectedGender   = ref('all')
  const selectedActivity = ref('inactivity')
  const selectedSleep    = ref('weeknight')
  const activeKpi            = ref(null)
  const trendHover           = ref(null)
  const selectedBmi          = ref(null)
  const selectedActivityBand = ref(null)
  const selectedSleepBand    = ref(null)
  
  const COLORS = {
    underweight: '#4a9d89',
    normal:      '#2d7060',
    overweight:  '#e07a52',
    obese:       '#dc2626',
  }
  const BMI_ICONS = { underweight: '📉', normal: '✅', overweight: '⚠️', obese: '🔴' }
  
  const trendMetrics = [
    { key: 'overweight_obese_6_13', label: 'Overweight + obese', color: '#e07a52' },
    { key: 'obese_6_13',            label: 'Obese only',          color: '#dc2626' },
    { key: 'underweight_6_13',      label: 'Underweight',         color: '#4a9d89' },
  ]
  
  const defaultStats = {
    bmi: {
      all:   [
        { key: 'underweight', label: 'Underweight',    count: 313.7,  value: 8.0  },
        { key: 'normal',      label: 'Healthy weight', count: 2613.1, value: 67.0 },
        { key: 'overweight',  label: 'Overweight',     count: 661.9,  value: 17.0 },
        { key: 'obese',       label: 'Obese',          count: 314.4,  value: 8.1  },
      ],
      boys:  [
        { key: 'underweight', label: 'Underweight',    count: 150.1,  value: 7.5  },
        { key: 'normal',      label: 'Healthy weight', count: 1332.8, value: 66.5 },
        { key: 'overweight',  label: 'Overweight',     count: 352.5,  value: 17.6 },
        { key: 'obese',       label: 'Obese',          count: 169.6,  value: 8.5  },
      ],
      girls: [
        { key: 'underweight', label: 'Underweight',    count: 162.5,  value: 8.6  },
        { key: 'normal',      label: 'Healthy weight', count: 1279.2, value: 67.8 },
        { key: 'overweight',  label: 'Overweight',     count: 306.3,  value: 16.2 },
        { key: 'obese',       label: 'Obese',          count: 140.4,  value: 7.4  },
      ],
    },
    trend: {
      all:   [
        { year: 2010, underweight_6_13: 5.4, normal_6_13: 73.7, obese_6_13: 6.6,  overweight_obese_6_13: 20.9 },
        { year: 2012, underweight_6_13: 5.0, normal_6_13: 71.1, obese_6_13: 7.0,  overweight_obese_6_13: 23.9 },
        { year: 2014, underweight_6_13: 7.1, normal_6_13: 67.1, obese_6_13: 6.6,  overweight_obese_6_13: 25.8 },
        { year: 2016, underweight_6_13: 6.8, normal_6_13: 66.3, obese_6_13: 6.6,  overweight_obese_6_13: 26.9 },
      ],
      boys:  [
        { year: 2010, underweight_6_13: 6.5, normal_6_13: 73.4, obese_6_13: 6.5,  overweight_obese_6_13: 20.1 },
        { year: 2012, underweight_6_13: 5.1, normal_6_13: 71.4, obese_6_13: 7.2,  overweight_obese_6_13: 23.4 },
        { year: 2014, underweight_6_13: 6.8, normal_6_13: 67.3, obese_6_13: 7.3,  overweight_obese_6_13: 25.9 },
        { year: 2016, underweight_6_13: 7.4, normal_6_13: 65.9, obese_6_13: 7.5,  overweight_obese_6_13: 26.8 },
      ],
      girls: [
        { year: 2010, underweight_6_13: 4.2, normal_6_13: 74.1, obese_6_13: 6.6,  overweight_obese_6_13: 21.7 },
        { year: 2012, underweight_6_13: 4.9, normal_6_13: 70.7, obese_6_13: 6.8,  overweight_obese_6_13: 24.4 },
        { year: 2014, underweight_6_13: 7.5, normal_6_13: 66.9, obese_6_13: 5.8,  overweight_obese_6_13: 25.6 },
        { year: 2016, underweight_6_13: 6.2, normal_6_13: 66.7, obese_6_13: 5.6,  overweight_obese_6_13: 27.0 },
      ],
    },
    activity: {
      inactivity:        [
        { label: 'Less than 9 hours',         value: 17.1 },
        { label: '9 to less than 10 hours',   value: 19.1 },
        { label: '10 to less than 11 hours',  value: 17.7 },
        { label: '11 to less than 12 hours',  value: 18.5 },
        { label: '12 to less than 13 hours',  value: 11.5 },
        { label: '13 to less than 14 hours',  value: 9.7  },
        { label: '14 hours or more',          value: 6.4  },
      ],
      light:             [
        { label: 'Less than 2 hours',         value: 6.2  },
        { label: '2 to less than 3 hours',    value: 22.6 },
        { label: '3 to less than 4 hours',    value: 44.3 },
        { label: '4 hours or more',           value: 26.9 },
      ],
      moderate_vigorous: [
        { label: 'Less than 30 minutes',      value: 22.2 },
        { label: '30 to less than 60 minutes',value: 30.2 },
        { label: '1 to less than 1.5 hours',  value: 24.9 },
        { label: '1.5 to less than 2 hours',  value: 14.4 },
        { label: '2 hours or more',           value: 8.3  },
      ],
    },
    sleep: {
      weeknight: [
        { label: 'Less than 6 hours',        value: 2.1  },
        { label: '6 to less than 7 hours',   value: 5.8  },
        { label: '7 to less than 8 hours',   value: 22.2 },
        { label: '8 to less than 9 hours',   value: 31.7 },
        { label: '9 to less than 10 hours',  value: 29.8 },
        { label: '10 hours or more',         value: 8.5  },
      ],
      weekend: [
        { label: 'Less than 6 hours',        value: 3.6  },
        { label: '6 to less than 7 hours',   value: 8.3  },
        { label: '7 to less than 8 hours',   value: 19.8 },
        { label: '8 to less than 9 hours',   value: 29.9 },
        { label: '9 to less than 10 hours',  value: 26.5 },
        { label: '10 hours or more',         value: 12.0 },
      ],
      overall: [
        { label: 'Less than 6 hours',        value: 2.1  },
        { label: '6 to less than 7 hours',   value: 5.9  },
        { label: '7 to less than 8 hours',   value: 22.6 },
        { label: '8 to less than 9 hours',   value: 33.2 },
        { label: '9 to less than 10 hours',  value: 28.9 },
        { label: '10 hours or more',         value: 7.3  },
      ],
    },
  }
  
  watch([selectedGender, selectedActivity, selectedSleep], () => {
    selectedBmi.value = null; trendHover.value = null
    selectedActivityBand.value = null; selectedSleepBand.value = null
  })
  
  const bmiChartData   = computed(() => (defaultStats.bmi[selectedGender.value] || defaultStats.bmi.all).map(i => ({ ...i, color: COLORS[i.key] || '#4a9d89' })))
  const bmiMax         = computed(() => Math.max(...bmiChartData.value.map(d => d.value), 1))
  const bmiHealthyPct  = computed(() => bmiChartData.value.find(d => d.key === 'normal')?.value || 0)
  const overweightVal  = computed(() => bmiChartData.value.find(d => d.key === 'overweight')?.value || 0)
  const obeseVal       = computed(() => bmiChartData.value.find(d => d.key === 'obese')?.value || 0)
  const combinedVal    = computed(() => Math.round((overweightVal.value + obeseVal.value) * 10) / 10)
  const trendLabel     = computed(() => selectedGender.value === 'boys' ? 'Boys' : selectedGender.value === 'girls' ? 'Girls' : 'All children')
  const profileSummary = computed(() => `${trendLabel.value}, Australia, ages 5–12`)
  const assistantTitle = computed(() => combinedVal.value >= 27 ? 'This group needs targeted support.' : combinedVal.value >= 22 ? 'Healthy routines can help.' : 'Tracking better than average.')
  const assistantMessage = computed(() => `For ${trendLabel.value.toLowerCase()}, about ${combinedVal.value}% are classified as overweight or obese. Use the activity and sleep charts below to identify practical opportunities.`)
  const selectedBmiItem    = computed(() => bmiChartData.value.find(d => d.key === selectedBmi.value))
  const selectedBmiIcon    = computed(() => BMI_ICONS[selectedBmi.value] || '📊')
  const selectedBmiInsight = computed(() => { const i = selectedBmiItem.value; return i ? `${i.value}% of ${trendLabel.value.toLowerCase()} are in this category, representing approximately ${i.count}k children nationally.` : '' })
  const trendRows  = computed(() => defaultStats.trend[selectedGender.value] || defaultStats.trend.all)
  const trendYears = computed(() => trendRows.value.map(r => r.year))
  const activityBands  = computed(() => defaultStats.activity[selectedActivity.value] || [])
  const sleepBands     = computed(() => defaultStats.sleep[selectedSleep.value] || [])
  const activityMaxVal = computed(() => Math.max(...activityBands.value.map(d => d.value), 1))
  const sleepMaxVal    = computed(() => Math.max(...sleepBands.value.map(d => d.value), 1))
  const activityLabel  = computed(() => selectedActivity.value === 'light' ? 'Light physical activity' : selectedActivity.value === 'moderate_vigorous' ? 'Moderate & vigorous activity' : 'Daily inactivity hours')
  const sleepLabel     = computed(() => selectedSleep.value === 'weekend' ? 'Weekend night sleep' : selectedSleep.value === 'overall' ? 'Per night average' : 'Weeknight sleep')
  const sleepTargetPct = computed(() => sleepBands.value.filter(b => /9 to less than 10|10 hours or more/i.test(b.label)).reduce((s, b) => s + b.value, 0).toFixed(1))
  const activityTopLabel = computed(() => { if (!activityBands.value.length) return ''; const top = activityBands.value.reduce((a, b) => b.value > a.value ? b : a); return `${shorten(top.label)} most common` })
  const selectedActivityBandValue = computed(() => activityBands.value.find(d => d.label === selectedActivityBand.value)?.value || 0)
  const selectedSleepBandValue    = computed(() => sleepBands.value.find(d => d.label === selectedSleepBand.value)?.value || 0)
  const activityYTicks = computed(() => { const m = activityMaxVal.value; return m > 40 ? [50,40,30,20,10,0] : m > 25 ? [40,30,20,10,0] : [30,20,10,0] })
  const sleepYTicks    = computed(() => { const m = sleepMaxVal.value; return m > 28 ? [35,28,21,14,7,0] : [30,20,10,0] })
  const kpiCards = computed(() => {
    const normal   = bmiChartData.value.find(d => d.key === 'normal')?.value || 0
    const lowAct   = defaultStats.activity.moderate_vigorous?.find(d => /less than 30/i.test(d.label))?.value || 0
    const lowSleep = (defaultStats.sleep.weeknight?.filter(d => /Less than 6|6 to less than 7/i.test(d.label))?.reduce((s, d) => s + d.value, 0) || 0)
    return [
      { id: 'normal',     icon: '✅', iconBg: 'icon-green',  label: 'Healthy BMI range',          value: `${normal}%`,                       detail: `${normal}% of ${trendLabel.value.toLowerCase()} are in a healthy BMI range.` },
      { id: 'overweight', icon: '⚖️', iconBg: 'icon-amber',  label: 'Overweight or obese',        value: `${combinedVal.value}%`,            warning: true, detail: 'Combined overweight and obese BMI categories for the selected group.' },
      { id: 'activity',   icon: '🏃', iconBg: 'icon-coral',  label: '< 30 min moderate activity', value: `${lowAct}%`,                       detail: 'Proportion of children in the lowest moderate/vigorous activity band.' },
      { id: 'sleep',      icon: '💤', iconBg: 'icon-indigo', label: '< 7 hrs sleep weeknights',   value: `${Math.round(lowSleep*10)/10}%`,   detail: 'Children sleeping under 7 hours on weeknights. Recommended is 9–11 hrs.' },
    ]
  })
  
  const gridYs = [0, 10, 20, 30]
  function tX(year) { const y = trendYears.value; const i = y.indexOf(year); return 60 + (i / (y.length - 1)) * 478 }
  function tY(val) { return 225 - (val / 35) * 190 }
  function trendPoints(metric) { return trendRows.value.map(row => ({ x: tX(row.year), y: tY(row[metric]), val: row[metric], year: row.year })) }
  function linePath(metric) { return trendPoints(metric).map((p, i) => (i === 0 ? `M${p.x},${p.y}` : `L${p.x},${p.y}`)).join(' ') }
  function areaPath(metric) { const pts = trendPoints(metric); const line = pts.map((p, i) => (i === 0 ? `M${p.x},${p.y}` : `L${p.x},${p.y}`)).join(' '); return `${line} L${pts.at(-1).x},225 L${pts[0].x},225 Z` }
  function ttX(x) { return x > 400 ? x - 172 : x + 14 }
  function bmiBarWidth(item) { return Math.round((item.value / bmiMax.value) * 100) }
  function actBarH(val, max) { return Math.max(4, (val / max) * 100) }
  function actColor(val) { return val >= 35 ? '#4a9d89' : val >= 20 ? '#2d7060' : val >= 10 ? '#e07a52' : '#dc2626' }
  function sleepColor(label) { return /9 to less than 10|10 hours or more/i.test(label) ? '#2d7060' : /8 to less than 9/i.test(label) ? '#4a9d89' : /7 to less than 8/i.test(label) ? '#e07a52' : '#dc2626' }
  function shorten(label) { return label.replace('Less than','<').replace('to less than','–').replace(' hours','h').replace(' hour','h').replace(' minutes','min').replace(' or more','+') }
  function sleepShort(label) { return shorten(label) }
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;0,700;1,300&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
  
  .stats-page {
    --ink:        #1a2e24;
    --ink-mid:    #3d5248;
    --ink-muted:  #617a6d;
    --sage:       #4a9d89;
    --sage-dark:  #2d7060;
    --sage-soft:  #e4f3ef;
    --sage-pale:  #f0f9f6;
    --coral:      #e07a52;
    --coral-soft: #fceee6;
    --bg:         #f2ede4;
    --bg-card:    rgba(255, 252, 247, 0.88);
    --border:     rgba(26, 46, 36, 0.09);
    --border-mid: rgba(26, 46, 36, 0.14);
    --shadow-sm:  0 2px 12px rgba(26,46,36,.06);
    --shadow-md:  0 8px 28px rgba(26,46,36,.09);
    --shadow-lg:  0 20px 56px rgba(26,46,36,.12);
    --r-sm: 12px; --r-md: 20px; --r-lg: 28px;
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
    color: var(--ink);
    background: var(--bg);
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
  }
  
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  a { color: inherit; text-decoration: none; }
  button { font: inherit; cursor: pointer; border: none; background: none; }
  select { font: inherit; }
  
  /* Background */
  .bg { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
  .bg-blob { position: absolute; border-radius: 50%; filter: blur(90px); opacity: 0.5; }
  .blob-a { width: 680px; height: 680px; top: -180px; right: -160px; background: radial-gradient(circle, #b4dbd3 0%, transparent 70%); }
  .blob-b { width: 480px; height: 480px; bottom: -60px; left: -100px; background: radial-gradient(circle, #edc9ad 0%, transparent 70%); }
  .blob-c { width: 340px; height: 340px; top: 48%; left: 40%; background: radial-gradient(circle, #cce8e1 0%, transparent 70%); opacity: 0.35; }
  .bg-grid { position: absolute; inset: 0; background-image: linear-gradient(rgba(26,46,36,.03) 1px, transparent 1px), linear-gradient(90deg, rgba(26,46,36,.03) 1px, transparent 1px); background-size: 52px 52px; }
  
  /* Header */
  .site-header { position: sticky; top: 0; z-index: 40; height: 66px; padding: 0 clamp(20px, 5vw, 60px); display: flex; align-items: center; justify-content: space-between; gap: 16px; background: rgba(242,237,228,.82); border-bottom: 1px solid var(--border); backdrop-filter: blur(24px); }
  .brand { display: flex; align-items: center; gap: 10px; font-family: 'Fraunces', Georgia, serif; font-size: 1.18rem; font-weight: 400; letter-spacing: -0.03em; }
  .brand-mark { width: 32px; height: 32px; display: grid; place-items: center; border-radius: 50%; background: white; border: 1px solid var(--border); box-shadow: var(--shadow-sm); color: var(--sage-dark); }
  .brand-mark svg { width: 20px; height: 20px; }
  .nav-links { display: flex; gap: 2px; }
  .nav-links a { padding: 6px 14px; border-radius: 999px; font-size: 0.82rem; font-weight: 700; color: var(--ink-muted); transition: background .15s, color .15s; }
  .nav-links a:hover, .nav-links a.router-link-active { background: white; color: var(--ink); }
  .back-btn { display: flex; align-items: center; gap: 6px; padding: 8px 18px; border-radius: 999px; background: white; border: 1px solid var(--border); font-size: 0.82rem; font-weight: 700; color: var(--ink); box-shadow: var(--shadow-sm); transition: box-shadow .15s, transform .15s; }
  .back-btn:hover { box-shadow: var(--shadow-md); transform: translateX(-2px); }
  
  /* Page layout */
  .page-main { position: relative; z-index: 2; width: min(1180px, calc(100% - 40px)); margin: 0 auto; padding: 36px 0 100px; }
  
  /* Hero */
  .hero { display: grid; grid-template-columns: 1fr 400px; gap: 20px; margin-bottom: 22px; align-items: stretch; }
  .hero-left { display: flex; flex-direction: column; justify-content: flex-end; padding: 4px 0; }
  .pill { display: inline-flex; align-items: center; gap: 8px; padding: 5px 14px; border-radius: 999px; border: 1px solid rgba(74,157,137,.3); background: rgba(74,157,137,.1); color: var(--sage-dark); font-size: 0.68rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 14px; width: fit-content; }
  .pill-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--coral); animation: pulse 2.2s ease-in-out infinite; }
  @keyframes pulse { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.5); opacity: .55; } }
  .hero-title { font-family: 'Fraunces', Georgia, serif; font-size: clamp(3.8rem, 7.5vw, 6.4rem); font-weight: 300; line-height: 0.88; letter-spacing: -0.07em; color: var(--ink); }
  .hero-sub { margin-top: 18px; color: var(--ink-muted); font-size: 1rem; line-height: 1.5; }
  .hero-sub strong { color: var(--ink); font-weight: 700; }
  
  /* Insight card */
  .insight-card { position: relative; overflow: hidden; padding: 32px; border-radius: var(--r-lg); background: linear-gradient(145deg, #1a2e24 0%, #254035 55%, #1e3a2f 100%); border: 1px solid rgba(255,255,255,.06); box-shadow: var(--shadow-lg); color: white; }
  .insight-eyebrow { font-size: 0.67rem; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(255,255,255,.4); margin-bottom: 14px; }
  .insight-title { font-family: 'Fraunces', Georgia, serif; font-size: clamp(1.5rem, 2.5vw, 2rem); font-weight: 400; line-height: 1.15; letter-spacing: -0.04em; margin-bottom: 14px; }
  .insight-body { color: rgba(255,255,255,.6); line-height: 1.7; font-size: 0.9rem; }
  .insight-pulse { position: absolute; bottom: -70px; right: -70px; width: 220px; height: 220px; border-radius: 50%; background: radial-gradient(circle, rgba(74,157,137,.3) 0%, transparent 70%); animation: breathe 4s ease-in-out infinite; }
  @keyframes breathe { 0%, 100% { transform: scale(1); opacity: .6; } 50% { transform: scale(1.25); opacity: 1; } }
  .insight-decoration { position: absolute; top: -20px; right: -20px; width: 180px; height: 180px; opacity: 0.5; pointer-events: none; }
  
  /* KPI row */
  .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 18px; }
  .kpi-tile { padding: 22px 20px; border-radius: var(--r-md); background: var(--bg-card); border: 1px solid var(--border); box-shadow: var(--shadow-sm); text-align: left; display: flex; flex-direction: column; gap: 7px; transition: transform .2s, box-shadow .2s, background .2s, border-color .2s; }
  .kpi-tile:hover, .kpi-active { transform: translateY(-3px); box-shadow: var(--shadow-md); background: white; border-color: var(--border-mid); }
  .kpi-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px; }
  .kpi-icon-wrap { width: 40px; height: 40px; border-radius: 13px; display: grid; place-items: center; font-size: 1.1rem; flex-shrink: 0; }
  .icon-green  { background: var(--sage-soft); }
  .icon-amber  { background: #fef3c7; }
  .icon-coral  { background: var(--coral-soft); }
  .icon-indigo { background: #eef2ff; }
  .kpi-chevron { color: var(--ink-muted); opacity: 0.5; transition: transform .2s; }
  .kpi-chevron.rotated { transform: rotate(180deg); opacity: 0.8; }
  .kpi-val { font-family: 'Fraunces', Georgia, serif; font-size: 2.5rem; font-weight: 300; letter-spacing: -0.06em; color: var(--sage-dark); line-height: 1; }
  .kpi-warn .kpi-val { color: var(--coral); }
  .kpi-label { font-size: 0.76rem; font-weight: 700; color: var(--ink-muted); line-height: 1.35; }
  .kpi-detail { padding-top: 12px; border-top: 1px solid var(--border); font-size: 0.81rem; color: var(--ink-muted); line-height: 1.6; }
  
  /* Filter bar */
  .filter-bar { display: flex; align-items: center; gap: 16px; margin-bottom: 22px; padding: 14px 20px; border-radius: var(--r-md); background: var(--bg-card); border: 1px solid var(--border); box-shadow: var(--shadow-sm); flex-wrap: wrap; }
  .filter-label-wrap { display: flex; align-items: center; gap: 7px; flex-shrink: 0; }
  .filter-label { font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: var(--ink-muted); white-space: nowrap; }
  .filter-label-wrap svg { color: var(--ink-muted); }
  .filter-chips { display: flex; gap: 10px; flex-wrap: wrap; flex: 1; }
  .chip-select { display: flex; align-items: center; gap: 8px; padding: 7px 16px; border-radius: 999px; background: white; border: 1px solid var(--border); cursor: pointer; transition: border-color .15s, box-shadow .15s; }
  .chip-select:focus-within { border-color: var(--sage); box-shadow: 0 0 0 3px rgba(74,157,137,.15); }
  .chip-select span { font-size: 0.7rem; font-weight: 800; color: var(--ink-muted); white-space: nowrap; }
  .chip-select select { border: none; outline: none; background: transparent; font-size: 0.82rem; font-weight: 700; color: var(--ink); cursor: pointer; }
  .filter-active-tag { display: inline-flex; align-items: center; gap: 6px; height: 30px; padding: 0 12px; border-radius: 999px; background: var(--sage-soft); border: 1px solid rgba(74,157,137,.25); color: var(--sage-dark); font-size: 0.76rem; font-weight: 700; margin-left: auto; }
  .filter-active-tag button { background: none; border: none; color: inherit; cursor: pointer; font-size: 1rem; line-height: 1; opacity: 0.7; }
  
  /* Charts grid */
  .charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .bmi-card, .trend-card { grid-column: 1 / -1; }
  .chart-card { padding: clamp(22px, 2.5vw, 30px); border-radius: var(--r-lg); background: var(--bg-card); border: 1px solid var(--border); box-shadow: var(--shadow-md); backdrop-filter: blur(16px); }
  .chart-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 24px; }
  .kicker { display: block; font-size: 0.67rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.13em; color: var(--sage-dark); margin-bottom: 5px; }
  .chart-head h3 { font-family: 'Fraunces', Georgia, serif; font-size: clamp(1.3rem, 2vw, 1.6rem); font-weight: 400; letter-spacing: -0.04em; color: var(--ink); line-height: 1.15; }
  .chart-head-badge { display: inline-flex; align-items: center; gap: 7px; padding: 7px 14px; border-radius: 999px; background: var(--sage-soft); border: 1px solid rgba(74,157,137,.2); font-size: 0.78rem; font-weight: 700; color: var(--sage-dark); white-space: nowrap; flex-shrink: 0; }
  .chart-head-badge--amber  { background: #fef3c7; border-color: rgba(217,119,6,.2); color: #92400e; }
  .chart-head-badge--indigo { background: #eef2ff; border-color: rgba(99,102,241,.2); color: #4338ca; }
  .badge-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
  .badge-green  { background: #2d7060; }
  .badge-amber  { background: #d97706; }
  .badge-indigo { background: #6366f1; }
  
  /* ── BMI bars: label | bar | stat ── */
  .bmi-bars { display: flex; flex-direction: column; gap: 10px; }
  
  .bmi-row {
    display: grid;
    grid-template-columns: 155px 1fr 130px;
    align-items: center;
    gap: 18px;
    padding: 14px 18px;
    border-radius: var(--r-sm);
    border: 1px solid transparent;
    cursor: pointer;
    transition: background .15s, border-color .15s, transform .18s, box-shadow .18s;
  }
  .bmi-row:hover        { background: white; border-color: var(--border); transform: translateX(4px); box-shadow: var(--shadow-sm); }
  .bmi-selected         { background: white; border-color: var(--border-mid); box-shadow: var(--shadow-sm); }
  
  .bmi-label-col { display: flex; align-items: center; gap: 10px; }
  .bmi-dot       { width: 10px; height: 10px; border-radius: 3px; flex-shrink: 0; }
  .bmi-name      { font-size: 0.9rem; font-weight: 700; color: var(--ink); }
  
  .bmi-bar-col   { flex: 1; }
  .bmi-track     { height: 28px; border-radius: 999px; background: rgba(26,46,36,.07); overflow: hidden; }
  .bmi-fill      { height: 100%; border-radius: inherit; transition: width 0.7s cubic-bezier(.34,1.56,.64,1); }
  
  .bmi-stat-col  { display: flex; flex-direction: column; align-items: flex-end; gap: 2px; }
  .bmi-pct       { font-family: 'Fraunces', Georgia, serif; font-size: 1.6rem; font-weight: 300; color: var(--ink); letter-spacing: -0.04em; line-height: 1; }
  .bmi-count     { font-size: 0.72rem; font-weight: 700; color: var(--ink-muted); }
  
  .chart-note { display: flex; align-items: flex-start; gap: 12px; margin-top: 14px; padding: 14px 18px; border-radius: var(--r-sm); background: var(--sage-soft); border: 1px solid rgba(74,157,137,.2); color: var(--ink); font-size: 0.86rem; line-height: 1.6; }
  .chart-note--bmi .cn-icon { font-size: 1.2rem; flex-shrink: 0; margin-top: 1px; }
  .chart-note strong { display: block; font-size: 0.88rem; font-weight: 800; margin-bottom: 2px; }
  .chart-note p { color: var(--ink-muted); margin: 0; }
  .bmi-source { margin-top: 12px; font-size: 0.72rem; color: var(--ink-muted); opacity: 0.65; }
  
  /* Trend chart */
  .line-wrap { overflow-x: auto; }
  .line-svg { width: 100%; min-width: 480px; overflow: visible; display: block; }
  .axis-lbl { fill: var(--ink-muted); font-size: 10.5px; font-weight: 700; font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }
  .trend-line { stroke-dasharray: 1200; stroke-dashoffset: 1200; animation: drawLine 1.6s ease forwards; }
  @keyframes drawLine { to { stroke-dashoffset: 0; } }
  .trend-dot { cursor: pointer; transition: r .15s; }
  .trend-dot:hover { r: 7; }
  .tt-label { fill: var(--ink-muted); font-size: 10px; font-weight: 800; font-family: 'Plus Jakarta Sans', sans-serif; }
  .tt-val   { fill: var(--ink);       font-size: 13px; font-weight: 800; font-family: 'Plus Jakarta Sans', sans-serif; }
  .trend-legend { display: flex; flex-wrap: wrap; gap: 18px; margin-top: 14px; padding-top: 14px; border-top: 1px solid var(--border); }
  .leg-item { display: flex; align-items: center; gap: 8px; font-size: 0.8rem; font-weight: 700; color: var(--ink-muted); }
  .leg-item i { width: 18px; height: 3px; border-radius: 999px; display: block; }
  
  /* Vertical bar charts */
  .v-bars { display: grid; grid-template-columns: 40px 1fr; gap: 8px; min-height: 300px; }
  .v-bar-yaxis { height: 240px; display: flex; flex-direction: column; justify-content: space-between; text-align: right; padding-bottom: 40px; font-size: 0.68rem; font-weight: 800; color: var(--ink-muted); }
  .v-bar-plot { display: grid; grid-template-columns: repeat(auto-fit, minmax(60px, 1fr)); gap: 8px; align-items: end; border-bottom: 1.5px solid var(--border-mid); }
  .v-bar-col { height: 280px; display: grid; grid-template-rows: 24px 1fr 44px; gap: 4px; align-items: end; text-align: center; cursor: pointer; }
  .v-bar-val { font-size: 0.78rem; font-weight: 800; color: var(--ink-muted); transition: color .15s; display: block; }
  .v-bar-active .v-bar-val, .v-bar-peak .v-bar-val { color: var(--ink); }
  .v-bar-track { width: clamp(36px, 58%, 56px); height: 210px; margin: 0 auto; display: flex; align-items: flex-end; border-radius: 12px 12px 4px 4px; background: rgba(26,46,36,.07); overflow: hidden; }
  .v-bar-fill { width: 100%; min-height: 6px; border-radius: inherit; transition: height .6s cubic-bezier(.34,1.56,.64,1), filter .15s; }
  .v-bar-active .v-bar-fill { filter: saturate(1.15) brightness(1.04); }
  .v-bar-peak .v-bar-fill { box-shadow: 0 -4px 12px rgba(0,0,0,.1); }
  .v-bar-lbl { font-size: 0.68rem; font-weight: 700; color: var(--ink-muted); line-height: 1.3; display: flex; align-items: flex-start; justify-content: center; padding-top: 7px; }
  
  .sleep-rec { display: flex; gap: 10px; align-items: flex-start; margin-top: 14px; padding: 13px 16px; border-radius: var(--r-sm); background: var(--sage-pale); border: 1px solid rgba(74,157,137,.18); font-size: 0.86rem; color: var(--sage-dark); line-height: 1.6; font-weight: 600; }
  .sleep-rec-icon { flex-shrink: 0; }
  .sleep-rec p { margin: 0; }
  
  /* Transitions */
  .slide-note-enter-active, .slide-note-leave-active { transition: opacity .2s, transform .2s; }
  .slide-note-enter-from, .slide-note-leave-to { opacity: 0; transform: translateY(-6px); }
  
  /* Responsive */
  @media (max-width: 1020px) {
    .hero { grid-template-columns: 1fr; }
    .kpi-row { grid-template-columns: repeat(2, 1fr); }
    .charts-grid { grid-template-columns: 1fr; }
    .bmi-card, .trend-card { grid-column: 1; }
    .bmi-row { grid-template-columns: 130px 1fr 100px; gap: 12px; }
  }
  @media (max-width: 640px) {
    .site-header { padding: 0 16px; }
    .nav-links { display: none; }
    .kpi-row { grid-template-columns: 1fr 1fr; }
    .filter-bar { flex-direction: column; align-items: flex-start; }
    .bmi-row { grid-template-columns: 110px 1fr 80px; gap: 10px; padding: 12px 14px; }
    .bmi-name { font-size: 0.82rem; }
    .bmi-pct { font-size: 1.3rem; }
    .v-bar-plot { grid-auto-flow: column; grid-auto-columns: 64px; grid-template-columns: none; overflow-x: auto; }
  }
  </style>