import { defineStore } from 'pinia'

const STORAGE_KEY = 'hk-kids-progress-v2'

export function calendarDayKey() {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function weekdayInitial() {
  const n = new Date().getDay()
  const map = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
  return map[n]
}

function loadRaw() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) return JSON.parse(raw)
  } catch {
    //
  }
  return null
}

function defaultDaily() {
  return {
    meals: {},
    rainbow: {},
    waterGlasses: 3,
    stepBurst: 0,
    mood: 2,
    sleepStars: true,
    winPings: {}, // slug -> pings today (capped)
  }
}

export const useKidsProgressStore = defineStore('kidsProgress', {
  state: () => ({
    dailyKey: '',
    daily: defaultDaily(),
    /** Earlier days in Mon–Sat order-ish; Sun uses live score for bar chart tail */
    weekHistory: [
      { label: 'M', value: 66 },
      { label: 'T', value: 82 },
      { label: 'W', value: 74 },
      { label: 'T', value: 88 },
      { label: 'F', value: 79 },
      { label: 'S', value: 92 },
    ],
    challengeXp: 340,
    challengeMax: 500,
    xpPerWinTap: 24,
    winLifetime: {}, // slug -> count
  }),

  getters: {
    heroScorePct() {
      const d = this.daily
      const mealsDone = ['Breakfast', 'Lunch', 'Snack', 'Dinner'].filter((k) => d.meals[k]).length
      const rbDone = ['red', 'crunch', 'protein', 'water'].filter((k) => d.rainbow[k]).length
      let score = 18
      score += Math.round((mealsDone / 4) * 28)
      score += Math.round((rbDone / 4) * 28)
      score += Math.min(8, d.waterGlasses) * 3
      score += Math.min(7, d.stepBurst) * 2
      score += d.mood >= 3 ? 8 : d.mood * 2
      if (d.sleepStars) score += 6
      return Math.min(99, score)
    },
    waterDisplay() {
      const g = Math.min(8, this.daily.waterGlasses)
      return `${g} / 8`
    },
    waterProgressPct() {
      return `${Math.round(Math.min(this.daily.waterGlasses / 8, 1) * 100)}%`
    },
    stepsDisplay() {
      const base = 6800 + this.daily.stepBurst * 120
      return base.toLocaleString()
    },
    stepsProgressPct() {
      const pct = Math.min(100, ((6800 + this.daily.stepBurst * 120) / 10000) * 100)
      return `${Math.round(pct)}%`
    },
    sleepDisplay() {
      return this.daily.sleepStars ? '8h+' : '~7h'
    },
    sleepProgressPct() {
      return this.daily.sleepStars ? '92%' : '68%'
    },
    moodLabel() {
      const labels = ['Chill', 'Silly', 'Happy', 'Power mode']
      return labels[this.daily.mood] || 'Happy'
    },
    moodProgressPct() {
      return `${60 + this.daily.mood * 10}%`
    },
    moodEmoji() {
      return ['😌', '🤪', '😊', '⚡'][this.daily.mood] || '😊'
    },
    weekBars() {
      const today = weekdayInitial()
      return [...this.weekHistory, { label: today, value: this.heroScorePct }]
    },
    mealsCompleteCount() {
      return ['Breakfast', 'Lunch', 'Snack', 'Dinner'].filter((k) => this.daily.meals[k]).length
    },
    rainbowCompleteCount() {
      return ['red', 'crunch', 'protein', 'water'].filter((k) => this.daily.rainbow[k]).length
    },
    rainbowRingPct() {
      const done = this.rainbowCompleteCount
      return `${Math.round((done / 4) * 100)}%`
    },
    challengePct() {
      return Math.round((Math.min(this.challengeXp, this.challengeMax) / this.challengeMax) * 100)
    },
    starsEarnedComputed() {
      return Math.min(5, Math.max(1, Math.floor(this.challengeXp / 100)))
    },
    summaryCards() {
      return [
        { icon: '🔥', title: `${this.heroScorePct}% today`, text: 'Meals, rainbow bites, and Stats tab moves add up!' },
        { icon: '⭐', title: `${this.starsEarnedComputed}/5 sparkle stars`, text: 'Stack XP — tap Wins for bonus bursts!' },
        { icon: '🚀', title: 'Mini mission board', text: `Rainbow ${this.rainbowCompleteCount}/4 · Meals ${this.mealsCompleteCount}/4.` },
      ]
    },
    badgesDeck() {
      return [
        { id: 'streak', icon: '🔥', title: 'Streak vibes', text: 'Level up past 380 XP!', earned: this.challengeXp >= 355 },
        { id: 'rainbow', icon: '🌈', title: 'Rainbow plate', text: 'Check off all rainbow circles on Meals!', earned: this.rainbowCompleteCount >= 4 },
        { id: 'water', icon: '🚰', title: 'Sip superstar', text: 'Dial water to 8/8 under Stats!', earned: this.daily.waterGlasses >= 8 },
        { id: 'games', icon: '🎮', title: 'XP climber', text: 'Keep earning XP everywhere.', earned: this.challengeXp >= 400 },
      ]
    },
  },

  actions: {
    hydrate() {
      const raw = loadRaw()
      const tk = calendarDayKey()
      if (raw) {
        if (typeof raw.challengeXp === 'number') this.challengeXp = raw.challengeXp
        if (raw.weekHistory?.length === 6) this.weekHistory = raw.weekHistory
        if (raw.winLifetime && typeof raw.winLifetime === 'object') this.winLifetime = raw.winLifetime
      }

      const sameCalendarDay = Boolean(raw?.dailyKey && raw.dailyKey === tk && raw.daily && typeof raw.daily === 'object')
      if (sameCalendarDay) {
        this.dailyKey = tk
        this.daily = { ...defaultDaily(), ...raw.daily }
        if (typeof this.daily.winPings !== 'object') this.daily.winPings = {}
      } else {
        this.dailyKey = tk
        this.daily = defaultDaily()
      }
      this.persist()
    },

    persist() {
      try {
        localStorage.setItem(
          STORAGE_KEY,
          JSON.stringify({
            dailyKey: this.dailyKey,
            daily: this.daily,
            weekHistory: this.weekHistory,
            challengeXp: this.challengeXp,
            winLifetime: this.winLifetime,
          }),
        )
      } catch {
        //
      }
    },

    toggleMeal(label) {
      this.daily.meals = {
        ...this.daily.meals,
        [label]: !this.daily.meals[label],
      }
      if (this.daily.meals[label]) this.challengeXp = Math.min(999, this.challengeXp + 8)
      this.persist()
    },

    toggleRainbow(id) {
      this.daily.rainbow = {
        ...this.daily.rainbow,
        [id]: !this.daily.rainbow[id],
      }
      if (this.daily.rainbow[id]) this.challengeXp = Math.min(999, this.challengeXp + 10)
      this.persist()
    },

    addWater(delta) {
      this.daily.waterGlasses = Math.min(12, Math.max(0, this.daily.waterGlasses + delta))
      if (delta > 0) this.challengeXp = Math.min(999, this.challengeXp + 4)
      this.persist()
    },

    pulseSteps() {
      this.daily.stepBurst = Math.min(12, this.daily.stepBurst + 1)
      this.challengeXp = Math.min(999, this.challengeXp + 3)
      this.persist()
    },

    setMood(index) {
      this.daily.mood = Math.max(0, Math.min(3, index))
      this.persist()
    },

    toggleSleepFlag() {
      this.daily.sleepStars = !this.daily.sleepStars
      this.persist()
    },

    tapWin(slug) {
      const pings = this.daily.winPings?.[slug] || 0
      if (pings >= 6) return
      this.daily.winPings = {
        ...(this.daily.winPings || {}),
        [slug]: pings + 1,
      }
      this.winLifetime = {
        ...(this.winLifetime || {}),
        [slug]: (this.winLifetime[slug] || 0) + 1,
      }
      this.challengeXp = Math.min(999, this.challengeXp + this.xpPerWinTap)
      this.persist()
    },
  },
})
