<template>
  <header class="topbar">
    <RouterLink to="/" class="brand brand-link">
      <div class="brand-icon">❤</div>
      <span>HealthySteps</span>
    </RouterLink>

    <nav class="nav-links">
      <a href="#how-it-works">How it works</a>
      <a href="#resources">Resources</a>
      <a href="#community">Community</a>
    </nav>

    <RouterLink to="/parent-quiz" class="btn btn-primary header-btn">Get Started</RouterLink>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>