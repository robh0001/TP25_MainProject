<template>
  <div class="container">

    <div v-if="loading" class="status">Loading data...</div>
    <div v-else-if="error" class="status error">{{ error }}</div>

    <template v-else>

      <div class="btn-group">
        <button :class="['seg-btn', view === 'sleep' ? 'active' : '']" @click="view = 'sleep'">Sleep distribution</button>
        <button :class="['seg-btn', view === 'inactivity' ? 'active' : '']" @click="view = 'inactivity'">Physical inactivity distribution</button>
      </div>

      <!-- Sleep stat cards -->
      <div v-if="view === 'sleep'" class="stat-row">
        <div class="stat">
          <div class="stat-lbl">Peak band (week night)</div>
          <div class="stat-val">{{ sleepStats.peakWeeknight }}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Peak band (weekend)</div>
          <div class="stat-val">{{ sleepStats.peakWeekend }}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Less than 7hrs (week night)</div>
          <div class="stat-val">{{ sleepStats.under7Weeknight }}%</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Sleeping 10hrs+ (weekend)</div>
          <div class="stat-val">{{ sleepStats.over10Weekend }}%</div>
        </div>
      </div>

      <!-- Inactivity stat cards -->
      <div v-if="view === 'inactivity'" class="stat-row">
        <div class="stat">
          <div class="stat-lbl">Peak inactivity band</div>
          <div class="stat-val">{{ inactivityStats.peak }}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Less than 9hrs inactive</div>
          <div class="stat-val">{{ inactivityStats.under9 }}%</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">12hrs or more inactive</div>
          <div class="stat-val">{{ inactivityStats.over12 }}%</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">9 to 12hrs inactive</div>
          <div class="stat-val">{{ inactivityStats.mid }}%</div>
        </div>
      </div>

      <!-- Sleep chart -->
      <div v-if="view === 'sleep'" class="chart-card">
        <div class="card-title">Sleep duration distribution</div>
        <div class="card-sub">Ages 5-17 · % of children per duration band</div>
        <div class="leg">
          <span class="leg-item"><span class="leg-sq" style="background:#0072B2"></span>Week night</span>
          <span class="leg-item"><span class="leg-sq" style="background:#E69F00"></span>Weekend night</span>
        </div>
        <div style="position:relative; width:100%; height:300px;">
          <canvas ref="sleepCanvas" role="img" aria-label="Grouped bar chart of sleep duration for children aged 5 to 17">Most children sleep 8 to 9 hours per night.</canvas>
        </div>
      </div>

      <!-- Inactivity chart -->
      <div v-if="view === 'inactivity'" class="chart-card">
        <div class="card-title">Physical inactivity distribution</div>
        <div class="card-sub">Ages 5-17 · % of children per inactivity band</div>
        <div class="leg">
          <span class="leg-item"><span class="leg-sq" style="background:#D55E00"></span>Average daily inactivity</span>
        </div>
        <div style="position:relative; width:100%; height:300px;">
          <canvas ref="inactivityCanvas" role="img" aria-label="Bar chart of physical inactivity hours for children aged 5 to 17">Most children are inactive between 9 and 12 hours per day.</canvas>
        </div>
      </div>

    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import Papa from 'papaparse'

const view    = ref('sleep')
const loading = ref(true)
const error   = ref(null)

const sleepCanvas      = ref(null)
const inactivityCanvas = ref(null)

let sleepChart      = null
let inactivityChart = null

const sleepRows      = ref([])
const inactivityRows = ref([])

// ---------- CSV loading ----------
async function parseCSV(path) {
  const res  = await fetch(path)
  const text = await res.text()
  return new Promise((resolve, reject) => {
    Papa.parse(text, {
      header: true,
      skipEmptyLines: true,
      complete: r => resolve(r.data),
      error:    e => reject(e)
    })
  })
}

async function loadData() {
  try {
    const [sleep, inactivity] = await Promise.all([
      parseCSV('/sleep_weekend_week.csv'),
      parseCSV('/physical_inactivity.csv')
    ])
    sleepRows.value      = sleep
    inactivityRows.value = inactivity
    loading.value        = false
  } catch (e) {
    error.value   = 'Failed to load data: ' + e.message
    loading.value = false
  }
}

// ---------- Sleep helpers ----------
const sleepLabels = ['Less than 6h', '6 to 7h', '7 to 8h', '8 to 9h', '9 to 10h', '10h or more']

function sleepDataFor(prefix) {
  return sleepRows.value
    .filter(r => r.category.startsWith(prefix))
    .map(r => parseFloat(r.value_5_17))
}

const sleepStats = computed(() => {
  const wn = sleepDataFor('Weeknight')
  const we = sleepDataFor('Weekend')
  const maxWn = Math.max(...wn)
  const maxWe = Math.max(...we)
  return {
    peakWeeknight:   sleepLabels[wn.indexOf(maxWn)] + ' · ' + maxWn.toFixed(1) + '%',
    peakWeekend:     sleepLabels[we.indexOf(maxWe)] + ' · ' + maxWe.toFixed(1) + '%',
    under7Weeknight: ((wn[0] || 0) + (wn[1] || 0)).toFixed(1),
    over10Weekend:   (we[5] || 0).toFixed(1)
  }
})

// ---------- Inactivity helpers ----------
function inactivityRowsFor(heading) {
  return inactivityRows.value.filter(r =>
    r.section_heading &&
    r.section_heading.trim() === heading &&
    r.category !== 'Total persons' &&
    r.category.trim() !== heading.trim()
  )
}

function inactivityDataFor(heading) {
  return inactivityRowsFor(heading).map(r => parseFloat(r.value_5_17))
}

function inactivityLabelsFor(heading) {
  return inactivityRowsFor(heading).map(r => r.category)
}

const inactivityStats = computed(() => {
  const avg  = inactivityDataFor('Average daily inactivity')
  const lbls = inactivityLabelsFor('Average daily inactivity')
  const maxVal = Math.max(...avg)
  const over12 = avg
    .filter((_, i) => {
      const l = lbls[i] || ''
      return l.includes('12') || l.includes('13') || l.includes('14')
    })
    .reduce((a, b) => a + b, 0)
  const mid = avg
    .filter((_, i) => {
      const l = lbls[i] || ''
      return l.includes('9') || l.includes('10') || l.includes('11')
    })
    .reduce((a, b) => a + b, 0)
  return {
    peak:   lbls[avg.indexOf(maxVal)] + ' · ' + maxVal.toFixed(1) + '%',
    under9: (avg[0] || 0).toFixed(1),
    over12: over12.toFixed(1),
    mid:    mid.toFixed(1)
  }
})

// ---------- Chart axes ----------
const xAxis = {
  grid:   { display: false },
  border: { display: false },
  ticks:  { color: '#888', font: { size: 11 }, maxRotation: 30 }
}
const yAxis = {
  beginAtZero: true,
  grid:   { color: 'rgba(128,128,128,0.12)' },
  border: { display: false },
  ticks:  { color: '#888', font: { size: 11 }, callback: v => v + '%' }
}

// ---------- Chart builders ----------
function buildSleepChart() {
  if (!sleepCanvas.value) return
  sleepChart?.destroy()
  sleepChart = new Chart(sleepCanvas.value, {
    type: 'bar',
    data: {
      labels: sleepLabels,
      datasets: [
        { label: 'Week night',    data: sleepDataFor('Weeknight'), backgroundColor: '#0072B2', borderRadius: 4, borderSkipped: false },
        { label: 'Weekend night', data: sleepDataFor('Weekend'),   backgroundColor: '#E69F00', borderRadius: 4, borderSkipped: false }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: c => ` ${c.dataset.label}: ${c.parsed.y.toFixed(1)}%` } }
      },
      scales: { x: xAxis, y: { ...yAxis, max: 40 } }
    }
  })
}

function buildInactivityChart() {
  if (!inactivityCanvas.value) return
  inactivityChart?.destroy()
  const avgData  = inactivityDataFor('Average daily inactivity')
  const avgLabls = inactivityLabelsFor('Average daily inactivity')
  inactivityChart = new Chart(inactivityCanvas.value, {
    type: 'bar',
    data: {
      labels: avgLabls,
      datasets: [
        { label: 'Avg daily inactivity', data: avgData, backgroundColor: '#D55E00', borderRadius: 4, borderSkipped: false }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: c => ` ${c.dataset.label}: ${c.parsed.y.toFixed(1)}%` } }
      },
      scales: { x: xAxis, y: { ...yAxis, max: 25 } }
    }
  })
}

// ---------- Watchers ----------
watch(view, async (val) => {
  await nextTick()
  if (val === 'sleep') buildSleepChart()
  else                 buildInactivityChart()
})

watch(loading, async (val) => {
  if (!val && !error.value) {
    await nextTick()
    buildSleepChart()
  }
})

onMounted(() => { loadData() })
</script>

<style scoped>
.container    { padding: 1.5rem; font-family: sans-serif; max-width: 800px; }
.status       { font-size: 14px; color: #888; padding: 1rem 0; }
.status.error { color: #c0392b; }
.btn-group    { display: flex; gap: 8px; margin-bottom: 1.25rem; justify-content: center; }
.seg-btn      { padding: 6px 20px; font-size: 13px; border-radius: 8px; border: 0.5px solid #ccc; background: transparent; color: #666; cursor: pointer; transition: all 0.15s; }
.seg-btn.active { background: #f0f0f0; color: #111; border-color: #999; font-weight: 500; }
.stat-row     { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 10px; margin-bottom: 1.25rem; }
.stat         { background: #f5f5f5; border-radius: 8px; padding: 12px 14px; }
.stat-lbl     { font-size: 11px; color: #888; margin-bottom: 4px; }
.stat-val     { font-size: 16px; font-weight: 500; color: #111; }
.chart-card   { background: #fff; border: 0.5px solid #e0e0e0; border-radius: 12px; padding: 1rem 1.25rem; }
.card-title   { font-size: 14px; font-weight: 500; color: #111; margin-bottom: 3px; }
.card-sub     { font-size: 11px; color: #aaa; margin-bottom: 12px; }
.leg          { display: flex; flex-wrap: wrap; gap: 14px; margin-bottom: 12px; }
.leg-item     { display: flex; align-items: center; gap: 5px; font-size: 11px; color: #666; }
.leg-sq       { width: 9px; height: 9px; border-radius: 2px; flex-shrink: 0; }
</style>