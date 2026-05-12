import { ref } from 'vue'

const API_BASE = import.meta.env.VITE_FOOD_AI_API_BASE_URL

export function useFoodHealthPredictor() {
  const loading = ref(false)
  const error = ref(null)
  const result = ref(null)
  const candidates = ref([])

  async function predictFood(foodName) {
    const cleanFoodName = foodName?.trim()

    if (!cleanFoodName) {
      error.value = 'Please enter a food name.'
      result.value = null
      candidates.value = []
      return
    }

    if (!API_BASE) {
      error.value = 'Missing VITE_FOOD_AI_API_BASE_URL'
      result.value = null
      candidates.value = []
      return
    }

    loading.value = true
    error.value = null
    result.value = null
    candidates.value = []

    try {
      const response = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          food_name: cleanFoodName,
        }),
      })

      const data = await response.json().catch(() => ({}))

      if (!response.ok) {
        throw new Error(data.message || `Prediction failed: HTTP ${response.status}`)
      }

      if (!data.success) {
        if (data.status === 'multiple_matches') {
          candidates.value = data.candidates || []
          error.value = data.message || 'Multiple foods matched. Please choose one.'
          return
        }

        error.value = data.message || 'Could not predict this food.'
        return
      }

      result.value = data.data
    } catch (err) {
      error.value = err.message || 'Could not connect to the AI prediction API.'
    } finally {
      loading.value = false
    }
  }

  function clearPrediction() {
    error.value = null
    result.value = null
    candidates.value = []
  }

  return {
    loading,
    error,
    result,
    candidates,
    predictFood,
    clearPrediction,
  }
}