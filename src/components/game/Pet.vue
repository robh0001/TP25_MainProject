<template>
  <article class="adventure-panel pet-panel">
    <p class="panel-kicker">Buddy pet</p>
    <div class="pet-avatar" :class="petMood">{{ petEmoji }}</div>
    <h3>{{ petName }}</h3>
    <p>{{ moodMessage }}</p>

    <div class="pet-shop">
      <button
        v-for="skin in petSkins"
        :key="skin.id"
        type="button"
        class="pet-skin-btn"
        :disabled="activeSkin === skin.id"
        @click="$emit('buySkin', skin)"
      >
        {{ skin.icon }} {{ skin.label }} ({{ skin.cost }} coins)
      </button>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  streak: {
    type: Number,
    default: 0,
  },
  completedQuestCount: {
    type: Number,
    default: 0,
  },
  activeSkin: {
    type: String,
    default: 'seedling',
  },
})

defineEmits(['buySkin'])

const petName = 'Milo the Habit Fox'
const petSkins = [
  { id: 'seedling', label: 'Seedling', icon: '🦊', cost: 0 },
  { id: 'ocean', label: 'Ocean Suit', icon: '🦊🌊', cost: 18 },
  { id: 'space', label: 'Space Suit', icon: '🦊🚀', cost: 24 },
]

const petMood = computed(() => {
  if (props.completedQuestCount >= 3) return 'happy'
  if (props.completedQuestCount >= 1) return 'calm'
  return 'sleepy'
})

const petEmoji = computed(() => {
  if (props.activeSkin === 'space') return '🦊🚀'
  if (props.activeSkin === 'ocean') return '🦊🌊'
  return petMood.value === 'happy' ? '🦊✨' : petMood.value === 'calm' ? '🦊' : '🦊💤'
})

const moodMessage = computed(() => {
  if (petMood.value === 'happy') return `Milo is super happy! ${props.streak}-day streak power!`
  if (petMood.value === 'calm') return 'Milo is cheering you on. One more quest for happy mode.'
  return 'Milo feels sleepy. Finish a quest to wake up your buddy.'
})
</script>
