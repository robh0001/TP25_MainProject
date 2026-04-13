<template>
    <div class="section-heading center narrow">
      <span v-if="badge" class="badge" :class="badgeClass">{{ badge }}</span>
      <h2>{{ title }}</h2>
      <p>{{ description }}</p>
    </div>
  </template>
  
  <script setup>
  defineProps({
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      default: '',
    },
    badge: {
      type: String,
      default: '',
    },
    badgeClass: {
      type: String,
      default: 'yellow',
    },
  })
  </script>