<template>
    <article class="mini-tool">
      <div class="tool-icon" :class="iconClass">{{ icon }}</div>
      <h4>{{ title }}</h4>
      <p>{{ description }}</p>
      <a href="#">{{ linkText }}</a>
    </article>
  </template>
  
  <script setup>
  defineProps({
    icon: String,
    title: String,
    description: String,
    linkText: String,
    iconClass: String,
  })
  </script>