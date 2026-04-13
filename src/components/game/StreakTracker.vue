<template>
  <article class="adventure-panel streak-panel">
    <p class="panel-kicker">Streak power</p>
    <h3>🔥 {{ streak }} day streak</h3>
    <p v-if="milestone">Milestone reached: {{ milestone }} days bonus unlocked!</p>
    <p v-else>Keep going! Bonus rewards unlock at 3, 5, and 7 days.</p>
  </article>
</template>

<script setup>
defineProps({
  streak: {
    type: Number,
    required: true,
  },
  milestone: {
    type: Number,
    default: 0,
  },
})
</script>
