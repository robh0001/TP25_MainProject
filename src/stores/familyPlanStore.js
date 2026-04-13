import { reactive } from 'vue'

const STORAGE_KEY = 'healthysteps-family-plan'

const defaultPlan = {
  childName: '',
  ageRange: '',
  habits: [],
  concerns: [],
  struggle: '',
  confidence: '',
  supportStyle: '',
  recommendations: [],
  nextAction: '',
  mission: '',
  streakDays: 0,
}

const state = reactive(loadInitialState())

function loadInitialState() {
  if (typeof window === 'undefined') {
    return { ...defaultPlan }
  }

  const saved = window.localStorage.getItem(STORAGE_KEY)
  if (!saved) {
    return { ...defaultPlan }
  }

  try {
    const parsed = JSON.parse(saved)
    return { ...defaultPlan, ...parsed }
  } catch (error) {
    return { ...defaultPlan }
  }
}

function savePlan(plan) {
  Object.assign(state, plan)

  if (typeof window !== 'undefined') {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
  }
}

function clearPlan() {
  Object.assign(state, { ...defaultPlan })

  if (typeof window !== 'undefined') {
    window.localStorage.removeItem(STORAGE_KEY)
  }
}

export function useFamilyPlanStore() {
  return {
    state,
    savePlan,
    clearPlan,
  }
}
