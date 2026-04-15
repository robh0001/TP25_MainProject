<template>
  <div class="bmi-container">

    <div v-if="loading" class="status">Loading data...</div>
    <div v-else-if="error" class="status error">{{ error }}</div>

    <template v-else>

      <div class="btn-group">
        <button :class="['seg-btn', view === 'persons' ? 'active' : '']" @click="view = 'persons'">Persons</button>
        <button :class="['seg-btn', view === 'gender' ? 'active' : '']" @click="view = 'gender'">Gender-specific</button>
      </div>

      <!-- Persons stat cards -->
      <div v-if="view === 'persons'" class="stat-row">
        <div class="stat">
          <div class="stat-lbl">Total persons</div>
          <div class="stat-val">{{ totalPersons }}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Normal weight</div>
          <div class="stat-val">{{ pct('persons', indexFor('Normal')) }}%</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Overweight + obese</div>
          <div class="stat-val">{{ pct('persons', indexFor('Overweight + obese')) }}%</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Obese</div>
          <div class="stat-val">{{ pct('persons', indexFor('Obese')) }}%</div>
        </div>
      </div>

      <!-- Gender stat cards -->
      <div v-if="view === 'gender'" class="stat-row">
        <div class="stat">
          <div class="stat-lbl">Males total</div>
          <div class="stat-val">{{ totalMales }}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Males overweight + obese</div>
          <div class="stat-val">{{ pct('males', indexFor('Overweight + obese')) }}%</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Females total</div>
          <div class="stat-val">{{ totalFemales }}</div>
        </div>
        <div class="stat">
          <div class="stat-lbl">Females overweight + obese</div>
          <div class="stat-val">{{ pct('females', indexFor('Overweight + obese')) }}%</div>
        </div>
      </div>

      <!-- Persons view -->
      <div v-if="view === 'persons'" class="single-layout">
        <div class="donut-wrap">
          <canvas ref="personsCanvas"></canvas>
          <div class="donut-center">
            <div class="donut-center-val">{{ totalPersons }}</div>
            <div class="donut-center-lbl">All persons</div>
          </div>
        </div>
        <div class="legend">
          <div v-for="(label, i) in labels" :key="i" class="leg-row">
            <div class="leg-left">
              <span class="leg-swatch" :style="{ background: colors[i] }"></span>
              <span class="leg-label">{{ label }}</span>
            </div>
            <div class="leg-right">
              <span class="leg-pct">{{ pct('persons', i) }}%</span>
              <span class="leg-count">{{ data.persons[i].toLocaleString() }}k</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Gender-specific view -->
      <div v-if="view === 'gender'" class="gender-layout">
        <div class="gender-card">
          <div class="chart-title">Males</div>
          <div class="donut-wrap">
            <canvas ref="malesCanvas"></canvas>
            <div class="donut-center">
              <div class="donut-center-val">{{ totalMales }}</div>
              <div class="donut-center-lbl">Males</div>
            </div>
          </div>
          <div class="legend">
            <div v-for="(label, i) in labels" :key="i" class="leg-row">
              <div class="leg-left">
                <span class="leg-swatch" :style="{ background: colors[i] }"></span>
                <span class="leg-label">{{ label }}</span>
              </div>
              <div class="leg-right">
                <span class="leg-pct">{{ pct('males', i) }}%</span>
                <span class="leg-count">{{ data.males[i].toLocaleString() }}k</span>
              </div>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="gender-card">
          <div class="chart-title">Females</div>
          <div class="donut-wrap">
            <canvas ref="femalesCanvas"></canvas>
            <div class="donut-center">
              <div class="donut-center-val">{{ totalFemales }}</div>
              <div class="donut-center-lbl">Females</div>
            </div>
          </div>
          <div class="legend">
            <div v-for="(label, i) in labels" :key="i" class="leg-row">
              <div class="leg-left">
                <span class="leg-swatch" :style="{ background: colors[i] }"></span>
                <span class="leg-label">{{ label }}</span>
              </div>
              <div class="leg-right">
                <span class="leg-pct">{{ pct('females', i) }}%</span>
                <span class="leg-count">{{ data.females[i].toLocaleString() }}k</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import Papa from 'papaparse'

const view      = ref('persons')
const loading   = ref(true)
const error     = ref(null)

const personsCanvas = ref(null)
const malesCanvas   = ref(null)
const femalesCanvas = ref(null)

let personsChart = null
let malesChart   = null
let femalesChart = null

const colors = ['#0072B2', '#E69F00', '#D55E00', '#56B4E9', '#009E73']

const labels = ref([])
const data = ref({ persons: [], males: [], females: [] })

async function loadCSV() {
  try {
    const response = await fetch('/bmi_5_17.csv')
    const text = await response.text()
    Papa.parse(text, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        const rows = results.data
        const personRows = rows.filter(r => r.bmi_group.startsWith('Persons') && !r.bmi_group.includes('Overweight_Obese'))
        const maleRows   = rows.filter(r => r.bmi_group.startsWith('Males')   && !r.bmi_group.includes('Overweight_Obese'))
        const femaleRows = rows.filter(r => r.bmi_group.startsWith('Females') && !r.bmi_group.includes('Overweight_Obese'))

        labels.value = personRows.map(r => r.bmi_group.replace('Persons_', '').replace(/_/g, ' '))

        data.value = {
          persons: personRows.map(r => parseFloat(r.bmi_5_17_years)),
          males:   maleRows.map(r   => parseFloat(r.bmi_5_17_years)),
          females: femaleRows.map(r => parseFloat(r.bmi_5_17_years))
        }
        loading.value = false
      },
      error: (err) => { error.value = 'Failed to parse CSV: ' + err.message; loading.value = false }
    })
  } catch (err) {
    error.value = 'Failed to load CSV: ' + err.message
    loading.value = false
  }
}

function totalOf(key) { return data.value[key].reduce((a, b) => a + b, 0) }

function pct(key, i) {
  const tot = totalOf(key)
  if (!tot || i < 0) return '0.0'
  return (data.value[key][i] / tot * 100).toFixed(1)
}

function indexFor(label) { return labels.value.indexOf(label) }

const totalPersons = computed(() => (totalOf('persons') / 1000).toFixed(2) + 'M')
const totalMales   = computed(() => (totalOf('males')   / 1000).toFixed(2) + 'M')
const totalFemales = computed(() => (totalOf('females') / 1000).toFixed(2) + 'M')

function makeChart(canvas, key) {
  return new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: labels.value,
      datasets: [{ data: data.value[key], backgroundColor: colors, borderWidth: 2, borderColor: 'transparent', hoverOffset: 8 }]
    },
    options: { cutout: '68%', plugins: { legend: { display: false } } }
  })
}

watch(view, async (val) => {
  personsChart?.destroy()
  malesChart?.destroy()
  femalesChart?.destroy()
  await nextTick()
  if (val === 'persons') {
    personsChart = makeChart(personsCanvas.value, 'persons')
  } else {
    malesChart   = makeChart(malesCanvas.value, 'males')
    femalesChart = makeChart(femalesCanvas.value, 'females')
  }
})

watch(loading, async (val) => {
  if (!val && !error.value) {
    await nextTick()
    personsChart = makeChart(personsCanvas.value, 'persons')
  }
})

onMounted(() => { loadCSV() })
</script>

<style scoped>
.bmi-container { padding: 1.5rem; font-family: sans-serif; max-width: 800px; }
.status { font-size: 14px; color: #888; padding: 1rem 0; }
.status.error { color: #c0392b; }
.btn-group { display: flex; gap: 8px; margin-bottom: 1.25rem; justify-content: center; }
.seg-btn { padding: 6px 20px; font-size: 13px; border-radius: 8px; border: 0.5px solid #ccc; background: transparent; color: #666; cursor: pointer; transition: all 0.15s; }
.seg-btn.active { background: #f0f0f0; color: #111; border-color: #999; font-weight: 500; }

.stat-row { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 10px; margin-bottom: 1.25rem; }
.stat { background: #f5f5f5; border-radius: 8px; padding: 12px 14px; }
.stat-lbl { font-size: 11px; color: #888; margin-bottom: 4px; }
.stat-val { font-size: 20px; font-weight: 500; color: #111; }

.single-layout { display: flex; flex-direction: column; align-items: center; gap: 1rem; }
.gender-layout { display: flex; gap: 1.5rem; align-items: flex-start; }
.gender-card { flex: 1; display: flex; flex-direction: column; align-items: center; }
.chart-title { font-size: 13px; font-weight: 500; color: #666; margin-bottom: 10px; }
.donut-wrap { position: relative; width: 200px; height: 200px; flex-shrink: 0; }
.donut-wrap canvas { width: 200px !important; height: 200px !important; }
.donut-center { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; pointer-events: none; }
.donut-center-val { font-size: 20px; font-weight: 500; color: #111; }
.donut-center-lbl { font-size: 11px; color: #888; margin-top: 2px; }
.legend { width: auto; margin-top: 0.5rem; display: flex; flex-direction: column; gap: 3px; }
.leg-row { display: flex; align-items: center; justify-content: flex-start; gap: 6px; padding: 2px 4px; }
.leg-left { display: flex; align-items: center; gap: 7px; flex: 1; }
.leg-swatch { width: 9px; height: 9px; border-radius: 2px; flex-shrink: 0; }
.leg-label { font-size: 12px; color: #666; }
.leg-right { display: flex; flex-direction: row; align-items: center; gap: 4px; }
.leg-pct { font-size: 12px; font-weight: 500; color: #111; }
.leg-count { font-size: 11px; color: #aaa; }
.divider { width: 0.5px; background: #eee; align-self: stretch; }
</style>