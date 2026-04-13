<template>
  <div class="adventure-progress">
    <div class="adventure-progress-meta">
      <strong>{{ label }}</strong>
      <span>{{ value }}%</span>
    </div>
    <div class="adventure-progress-track">
      <div class="adventure-progress-fill" :style="{ width: `${value}%` }"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    default: 'Level progress',
  },
  value: {
    type: Number,
    default: 0,
  },
})
</script>
