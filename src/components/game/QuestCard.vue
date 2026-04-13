<template>
  <button
    class="quest-card"
    :class="{ completed }"
    type="button"
    :disabled="completed"
    @click="$emit('complete', quest.id)"
  >
    <div class="quest-icon">{{ completed ? '✅' : '🎯' }}</div>
    <div class="quest-content">
      <strong>{{ quest.name }}</strong>
      <p>{{ quest.goal }}</p>
      <small>+{{ quest.xp }} XP • +{{ quest.coins }} coins</small>
    </div>
  </button>
</template>

<script setup>
defineProps({
  quest: {
    type: Object,
    required: true,
  },
  completed: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['complete'])
</script>
