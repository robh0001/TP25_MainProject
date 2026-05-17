<template>
  <div class="home-page" :class="{ 'home-loaded': isLoaded }">

    <!-- Background -->
    <div class="home-bg" data-hover-read-ignore="true" aria-hidden="true">
      <img
        class="home-bg-img"
        src="https://images.unsplash.com/photo-1542037104857-ffbb0b9155fb?auto=format&fit=crop&w=2400&q=90"
        alt=""
        aria-hidden="true"
      />
      <div class="home-bg-overlay"></div>
      <div class="home-bg-vignette"></div>
      <div class="home-bg-grain"></div>
    </div>

    <!-- Header -->
    <header class="home-header" aria-label="Website header">
      <RouterLink
        to="/"
        class="home-logo"
        aria-label="Go to HealthyKids home page"
      >
        <div class="home-logo-icon" aria-hidden="true">
          <svg
            viewBox="0 0 36 36"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
            focusable="false"
          >
            <circle cx="18" cy="18" r="17" stroke="currentColor" stroke-width="1.2"/>
            <path d="M18 7C11.5 11.5 9.5 17 18 27C26.5 17 24.5 11.5 18 7Z" fill="currentColor"/>
            <path d="M18 13C15.5 15.5 15 19 18 23" stroke="white" stroke-width="1.2" stroke-linecap="round" fill="none" opacity="0.55"/>
          </svg>
        </div>

        <span class="home-logo-text">HealthyKids</span>
      </RouterLink>

      <RouterLink
        to="/parent-entry"
        class="home-header-pill"
        aria-label="Go to parent portal"
      >
        Parent portal
        <svg
          width="12"
          height="12"
          viewBox="0 0 12 12"
          aria-hidden="true"
          focusable="false"
        >
          <path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </RouterLink>
    </header>

    <!-- Main -->
    <main
      class="home-main"
      aria-label="HealthyKids home page introduction"
    >
      <div class="home-copy">

        <div
          class="home-eyebrow"
          aria-label="Australia 2026"
          data-hover-read-text
        >
          <span class="home-eyebrow-dot" aria-hidden="true"></span>
          Australia · 2026
        </div>

        <h1
          class="home-headline"
          aria-label="Healthier families start here."
          data-hover-read-text
        >
          <span class="home-headline-line home-headline-line-1">Healthier</span>
          <span class="home-headline-line home-headline-line-2">families</span>
          <span class="home-headline-line home-headline-line-3">start here.</span>
        </h1>

        <p class="home-sub">
          A personalised health plan for children aged 5-12,
          built around nutrition, movement, sleep and daily routine.
        </p>

        <div
          class="home-ctas"
          aria-label="Primary actions"
        >
          <RouterLink
            to="/parent-entry"
            class="home-cta home-cta--primary"
            aria-label="Enter the HealthyKids site"
          >
            Enter site
          </RouterLink>
        </div>

        <div
          class="home-pills"
          aria-label="HealthyKids quick highlights"
        >
          <span
            class="home-pill"
            aria-label="More than 12,000 Australian families supported"
            data-hover-read-text
          >
            <span class="home-pill-dot" aria-hidden="true"></span>
            12,000+ families
          </span>

          <span
            class="home-pill"
            aria-label="Suitable for children aged 5 to 12"
            data-hover-read-text
          >
            <span class="home-pill-dot" aria-hidden="true"></span>
            Ages 5-12
          </span>

          <span
            class="home-pill"
            aria-label="Three minute onboarding"
            data-hover-read-text
          >
            <span class="home-pill-dot" aria-hidden="true"></span>
            3-min onboarding
          </span>
        </div>
      </div>
    </main>

    <!-- Footer bar -->
    <footer
      class="home-footer"
      aria-label="Website footer"
    >
      <div
        class="home-footer-left"
        aria-label="Supporting families across Australia"
        data-hover-read-text
      >
        <span class="home-live-dot" aria-hidden="true"></span>
        Supporting families across Australia
      </div>

      <div
        class="home-footer-right"
        aria-label="UN Sustainable Development Goal 3, Good Health and Wellbeing. Developed by Team Syrbyx."
        data-hover-read-text
      >
        <span>UN SDG 3 · Good Health &amp; Wellbeing</span>
        <span class="home-footer-divider" aria-hidden="true">·</span>
        <span>Developed by Team Syrbyx</span>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { onMounted, ref } from 'vue'

const isLoaded = ref(false)
onMounted(() => { setTimeout(() => { isLoaded.value = true }, 80) })
</script>

