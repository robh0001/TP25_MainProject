<template>
  <header v-if="!isGameRoute" class="topbar">
    <RouterLink to="/" class="brand brand-link">
      <div class="brand-icon">❤</div>
      <span>HealthySteps</span>
    </RouterLink>

    <nav class="nav-links">
      <a href="#how-it-works">How it works</a>
      <a href="#resources">Resources</a>
      <a href="#parent-child-paths">Choose your path</a>
      <RouterLink to="/parent-dashboard">Parent dashboard</RouterLink>
    </nav>

    <div class="header-actions">
      <RouterLink to="/parent-dashboard" class="btn btn-outline-neutral header-btn">Parent dashboard</RouterLink>
      <RouterLink to="/parent-quiz" class="btn btn-primary header-btn">Start parent quiz</RouterLink>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useRoute } from 'vue-router'

const route = useRoute()
const isGameRoute = computed(() => route.path === '/young-person-dashboard')
</script>