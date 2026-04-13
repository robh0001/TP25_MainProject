import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { adventureWorlds } from '../data/adventureData'

const STORAGE_KEY = 'healthysteps-adventure'
const DAILY_RESET_HOUR = 4

function getCurrentDayKey() {
  const now = new Date()
  if (now.getHours() < DAILY_RESET_HOUR) {
    now.setDate(now.getDate() - 1)
  }
  return now.toISOString().slice(0, 10)
}

function flattenQuests(worlds) {
  return worlds.flatMap((world) =>
    world.levels.flatMap((level) =>
      level.quests.map((quest) => ({
        ...quest,
        worldId: world.id,
        worldName: world.name,
        level: level.level,
      }))
    )
  )
}

export const useAdventureStore = defineStore('adventure', () => {
  const xp = ref(0)
  const coins = ref(0)
  const level = ref(1)
  const streak = ref(0)
  const lastCompletedDay = ref('')
  const completedQuestIds = ref([])
  const lastResetDay = ref(getCurrentDayKey())
  const activePetSkin = ref('seedling')
  const ownedPetSkins = ref(['seedling'])
  const rewardFlash = ref(null)
  const worlds = ref(adventureWorlds)

  const allQuests = computed(() => flattenQuests(worlds.value))
  const dailyQuests = computed(() =>
    allQuests.value.filter((quest) => quest.level <= level.value).slice(0, 4)
  )
  const xpForNextLevel = computed(() => level.value * 120)
  const levelProgress = computed(() => Math.min(100, Math.round((xp.value / xpForNextLevel.value) * 100)))
  const activeWorldId = computed(() => {
    const available = worlds.value.filter((world) => world.unlockLevel <= level.value)
    return available[available.length - 1]?.id ?? worlds.value[0].id
  })
  const unlockedWorldIds = computed(() =>
    worlds.value.filter((world) => world.unlockLevel <= level.value).map((world) => world.id)
  )
  const streakMilestone = computed(() => {
    if (streak.value >= 7) return 7
    if (streak.value >= 5) return 5
    if (streak.value >= 3) return 3
    return 0
  })

  function saveToStorage() {
    if (typeof window === 'undefined') return
    const payload = {
      xp: xp.value,
      coins: coins.value,
      level: level.value,
      streak: streak.value,
      lastCompletedDay: lastCompletedDay.value,
      completedQuestIds: completedQuestIds.value,
      lastResetDay: lastResetDay.value,
      activePetSkin: activePetSkin.value,
      ownedPetSkins: ownedPetSkins.value,
    }
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
  }

  function loadFromStorage() {
    if (typeof window === 'undefined') return
    const raw = window.localStorage.getItem(STORAGE_KEY)
    if (!raw) return

    try {
      const saved = JSON.parse(raw)
      xp.value = saved.xp ?? 0
      coins.value = saved.coins ?? 0
      level.value = saved.level ?? 1
      streak.value = saved.streak ?? 0
      lastCompletedDay.value = saved.lastCompletedDay ?? ''
      completedQuestIds.value = saved.completedQuestIds ?? []
      lastResetDay.value = saved.lastResetDay ?? getCurrentDayKey()
      activePetSkin.value = saved.activePetSkin ?? 'seedling'
      ownedPetSkins.value = saved.ownedPetSkins ?? ['seedling']
    } catch (error) {
      window.localStorage.removeItem(STORAGE_KEY)
    }
  }

  function resetDailyQuestsIfNeeded() {
    const today = getCurrentDayKey()
    if (lastResetDay.value === today) return
    completedQuestIds.value = []
    rewardFlash.value = null
    lastResetDay.value = today
    saveToStorage()
  }

  function checkLevelUp() {
    while (xp.value >= level.value * 120) {
      level.value += 1
    }
  }

  function updateStreak() {
    const today = getCurrentDayKey()
    if (lastCompletedDay.value === today) return

    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)
    const yesterdayKey = yesterday.toISOString().slice(0, 10)

    streak.value = lastCompletedDay.value === yesterdayKey ? streak.value + 1 : 1
    lastCompletedDay.value = today

    if (streak.value === 3 || streak.value === 5 || streak.value === 7) {
      coins.value += streak.value
      rewardFlash.value = {
        title: `${streak.value}-day streak bonus`,
        xp: 0,
        coins: streak.value,
        message: 'Awesome consistency! Bonus coins unlocked.',
      }
    }
  }

  function completeQuest(questId) {
    const quest = dailyQuests.value.find((item) => item.id === questId)
    if (!quest || completedQuestIds.value.includes(questId)) return

    completedQuestIds.value.push(questId)
    xp.value += quest.xp
    coins.value += quest.coins
    rewardFlash.value = {
      title: quest.name,
      xp: quest.xp,
      coins: quest.coins,
      message: 'Awesome job! You completed a healthy quest.',
    }

    updateStreak()
    checkLevelUp()
    saveToStorage()
  }

  function closeRewardFlash() {
    rewardFlash.value = null
  }

  function buyPetSkin(skinId, cost) {
    if (ownedPetSkins.value.includes(skinId)) {
      activePetSkin.value = skinId
      saveToStorage()
      return true
    }

    if (coins.value < cost) return false
    coins.value -= cost
    ownedPetSkins.value.push(skinId)
    activePetSkin.value = skinId
    saveToStorage()
    return true
  }

  return {
    xp,
    coins,
    level,
    streak,
    worlds,
    rewardFlash,
    completedQuestIds,
    activePetSkin,
    ownedPetSkins,
    dailyQuests,
    activeWorldId,
    unlockedWorldIds,
    levelProgress,
    xpForNextLevel,
    streakMilestone,
    loadFromStorage,
    saveToStorage,
    resetDailyQuestsIfNeeded,
    completeQuest,
    closeRewardFlash,
    buyPetSkin,
  }
})
