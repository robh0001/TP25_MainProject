<template>
    <article class="step-card">
      <h4>{{ title }}</h4>
      <p>{{ description }}</p>
    </article>
  </template>
  
  <script setup>
  defineProps({
    title: String,
    description: String,
  })
  </script>