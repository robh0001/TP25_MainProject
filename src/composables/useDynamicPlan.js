import { ref } from 'vue'

const API_BASE = import.meta.env.VITE_GET_FAMILY_PLAN_API_BASE_URL

const DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

export function useDynamicPlan() {
  const rawPlan = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchPlan(username) {
    if (!username) {
      console.warn('fetchPlan stopped: missing username')
      return
    }

    if (!API_BASE) {
      error.value = 'Missing VITE_GET_FAMILY_PLAN_API_BASE_URL'
      console.error(error.value)
      return
    }

    loading.value = true
    error.value = null

    const url = `${API_BASE}/family-plan?username=${encodeURIComponent(username)}`

    try {
      const response = await fetch(url)
      const data = await response.json().catch(() => ({}))

      if (!response.ok) {
        throw new Error(data.error || `Failed to load plan: HTTP ${response.status}`)
      }

      rawPlan.value = data.plan || null
    } catch (err) {
      console.error('Failed to fetch dynamic family plan:', err)
      error.value = err.message || 'Failed to load family plan'
    } finally {
      loading.value = false
    }
  }

  function getWeek(weekNumber) {
    return rawPlan.value?.weeks?.find((week) => week.weekNumber === weekNumber) || null
  }

  function getTimeSlots(weekNumber, dayName) {
    const week = getWeek(weekNumber)
    if (!week) return []

    const day = (week.days || []).find((item) => item.dayName === dayName)
    return day?.timeSlots || []
  }

  function getTodaySlots(weekNumber, dayName, savedDoneState = {}) {
    return getTimeSlots(weekNumber, dayName).map((slot) => {
      const todaySlotId = `today-schedule-${slot.id}`

      return {
        ...slot,
        id: todaySlotId,
        done: Boolean(savedDoneState[todaySlotId]),
      }
    })
  }

  function buildRoadmapWeeks(roadmapProgress = {}, plannerOverrides = {}) {
    if (!rawPlan.value?.weeks?.length) return []

    return rawPlan.value.weeks.map((week) => {
      const dailyPlan = DAY_NAMES.map((dayName) => {
        const dbDay = (week.days || []).find((day) => day.dayName === dayName)
        const rawSlots = dbDay?.timeSlots || []

        const timeSlots = rawSlots.map((slot) => {
          const override = plannerOverrides[slot.id]
          const category = override?.category || slot.category

          const merged = override
            ? {
                ...slot,
                ...override,
                category,
                categoryLabel: getCategoryLabel(category),
              }
            : slot

          return {
            ...merged,
            done: Boolean(roadmapProgress[slot.id]),
          }
        })

        const completed = timeSlots.filter((slot) => slot.done).length
        const progress = timeSlots.length
          ? Math.round((completed / timeSlots.length) * 100)
          : 0

        return {
          day: dayName,
          actions: [],
          timeSlots,
          completed,
          progress,
        }
      })

      const dailyCompleted = dailyPlan.reduce((sum, day) => sum + day.completed, 0)
      const dailyTotal = dailyPlan.reduce((sum, day) => sum + day.timeSlots.length, 0)

      const progress = dailyTotal
        ? Math.round((dailyCompleted / dailyTotal) * 100)
        : 0

      let status = 'Not started'
      let statusKey = 'not-started'

      if (progress > 0 && progress < 100) {
        status = 'In progress'
        statusKey = 'in-progress'
      }

      if (progress === 100) {
        status = 'Completed'
        statusKey = 'completed'
      }

      return {
        id: week.weekNumber,
        week: week.weekNumber,
        title: week.theme || `Week ${week.weekNumber}`,
        icon: getWeekIcon(week.weekNumber),
        summary: `${dailyTotal} scheduled actions loaded from your family plan.`,
        detail: '',
        parentTip: '',
        actions: [],
        dailyPlan,
        dailyCompleted,
        dailyTotal,
        weeklyCompleted: 0,
        totalItems: dailyTotal,
        completed: dailyCompleted,
        progress,
        status,
        statusKey,
        feedbackTitle: '',
        feedback: '',
      }
    })
  }

  function getCategoryLabel(category) {
    const labels = {
      nutrition: 'Nutrition',
      movement: 'Movement',
      sleep: 'Wind-down',
      routine: 'Routine',
      family: 'Family',
    }

    return labels[category] || 'Routine'
  }

  function getWeekIcon(weekNumber) {
    const icons = {
      1: '🌱',
      2: '🔄',
      3: '💪',
      4: '🏆',
    }

    return icons[weekNumber] || '🌱'
  }

  return {
    rawPlan,
    loading,
    error,
    fetchPlan,
    getWeek,
    getTimeSlots,
    getTodaySlots,
    buildRoadmapWeeks,
  }
}